"""Real local tools + actual SDK orchestration with explicitly scripted model replies.

No live Gemini requests or credentials. Synthetic embedding fixtures only test wiring.
"""
import ast
import asyncio
import contextlib
import io
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT / 'campus_ai_starter' if (ROOT / 'campus_ai_starter').is_dir() else ROOT
DEPS = ROOT / 'test_dependencies'
sys.path.insert(0, str(DEPS))
sys.path.insert(0, str(PROJECT))
import httpx
from google import genai
from google.genai import types
from campus_ai import CampusAssistant, DOCUMENTS, required_exam_score

nb = json.loads((PROJECT/'Campus_AI_Made_Simple.ipynb').read_text())
report = []
def record(title, result):
    report.append({'check': title, 'result': result})
    print(title, result)

def model_reply(parts):
    return httpx.Response(200, json={
        'candidates': [{'content': {'role': 'model', 'parts': parts}, 'finishReason': 'STOP'}]})

http_requests = []
def mocked_api(request):
    """Script server responses; the real SDK executes the actual local functions."""
    payload = json.loads(request.content)
    http_requests.append({'path': request.url.path, 'payload': payload})
    if request.url.path.endswith((':embedContent', ':batchEmbedContents')):
        content = payload.get('content', {})
        if 'requests' in payload:
            content = payload['requests'][0].get('content', {})
        text = json.dumps(content).lower()
        # Orthogonal test fixtures, NOT genuine Gemini embeddings.
        v = [1.0, 0, 0, 0, 0]
        for i,word in enumerate(['biology','computing','campus events','library','study group']):
            if word in text:
                v = [float(j == i) for j in range(5)]
                break
        if 'requests' in payload:
            return httpx.Response(200,json={'embeddings': [{'values': v} for _ in payload['requests']]})
        return httpx.Response(200,json={'embedding': {'values': v}})

    declarations = [d['name'] for t in payload.get('tools',[]) for d in t.get('functionDeclarations',[])]
    tool_results = []
    for content in payload.get('contents',[]):
        for part in content.get('parts',[]):
            if 'functionResponse' in part:
                tool_results.append(part['functionResponse'])
    done = {x['name'] for x in tool_results}
    if 'search_campus_records' in declarations:
        if 'search_campus_records' not in done:
            return model_reply([{'functionCall': {'name':'search_campus_records', 'args':{'query':'biology final exam date and weight'}}}])
        if 'required_exam_score' not in done:
            return model_reply([{'functionCall': {'name':'required_exam_score','args':{'current_grade':85.0,'final_weight':0.20,'target_grade':90.0}}}])
        # Deliberately scripted text: NOT a Gemini-generated study plan.
        return model_reply([{'text':'SCRIPTED TEST RESPONSE: Biology final December 10 at 9 AM; weight 20% [S1]. Calculator returned 110%, impossible without extra credit. Proposed morning sessions: December 8 and 9, 25 minutes each; confirm availability. Nothing booked.'}])
    if 'get_library_hours' in declarations:
        if 'get_library_hours' not in done or 'list_campus_events' not in done:
            return model_reply([
                {'functionCall': {'name':'get_library_hours','args':{'day':'Friday'}}},
                {'functionCall': {'name':'list_campus_events','args':{'day':'Friday'}}}])
        return model_reply([{'text':'SCRIPTED TEST RESPONSE: Friday Coding Circle runs 2–3 PM and the fictional library closes at 10 PM.'}])
    if 'required_exam_score' in declarations:
        if not tool_results:
            return model_reply([{'functionCall': {'name':'required_exam_score','args':{'current_grade':85.0,'final_weight':0.20,'target_grade':90.0}}}])
        result = tool_results[-1]['response'].get('result',tool_results[-1]['response'])
        return model_reply([{'text':f'SCRIPTED TEST RESPONSE: calculator result is {json.dumps(result)}. Target requires more than 100%.'}])
    raise AssertionError('Unexpected scripted request: ' + str(declarations))

transport = httpx.MockTransport(mocked_api)
client = genai.Client(api_key='offline-test-placeholder', http_options=types.HttpOptions(
    client_args={'transport':transport}, async_client_args={'transport':transport}))
MODEL = 'gemini-flash-latest'
campus = CampusAssistant(client)
namespace = dict(globals())

def run_sync_cell(index):
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        exec(''.join(nb['cells'][index]['source']),namespace)
    return output.getvalue()

async def run_async_cell(index):
    source = ''.join(nb['cells'][index]['source'])
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        compiled = compile(source,f'notebook-cell-{index}','exec',flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
        await eval(compiled,namespace)
    return output.getvalue()

record('Lesson 5 direct calculator (real Python)',required_exam_score(85,.2,90))
assert required_exam_score(85,.2,90)['required_exam_percent']==110
assert required_exam_score(85,.2,85)['required_exam_percent']==85
for values in [(85,0,90),(85,20,90),(float('nan'),.2,90)]:
    try: required_exam_score(*values)
    except ValueError: continue
    raise AssertionError('Invalid input accepted')
record('Calculator edge checks','PASS: reachable target, invalid weights, and non-finite inputs')

lesson5 = run_sync_cell(14)
assert 'TOOL CALL: required_exam_score' in lesson5 and '110.0' in lesson5
record('Lesson 5 exact notebook cell; scripted model, real SDK and calculator',lesson5)

async def checks():
    # MCP subprocess must load packages installed in this isolated test directory.
    os.environ['PYTHONPATH'] = str(DEPS)
    os.chdir(PROJECT)
    # Exact discovery cell; real subprocess and protocol, no model simulation here.
    # The MCP SDK filters inherited env vars, so provide this testing path explicitly.
    source = ''.join(nb['cells'][16]['source'])
    source = source.replace('args=[str(Path("campus_mcp_server.py").resolve())])',
        'args=[str(Path("campus_mcp_server.py").resolve())], env={"PYTHONPATH": str(DEPS)})')
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        await eval(compile(source,'mcp-discovery','exec',flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT),namespace)
    discovery=output.getvalue()
    assert 'get_library_hours' in discovery and '10 PM' in discovery
    record('Lesson 6 MCP discovery and Friday call (real local server)',discovery)
    # Run exact Gemini+MCP notebook cell with scripted remote replies.
    bridge = await run_async_cell(17)
    assert 'MCP TOOL: get_library_hours' in bridge and 'MCP TOOL: list_campus_events' in bridge
    assert 'Coding Circle' in bridge and '10 PM' in bridge
    record('Lesson 6 exact Gemini-to-MCP notebook cell; scripted model, real SDK/server',bridge)
    from mcp import ClientSession
    from mcp.client.stdio import stdio_client
    async with stdio_client(namespace['server_params']) as (read,write):
        async with ClientSession(read,write) as session:
            await session.initialize()
            outputs={}
            for tool,day in [('get_library_hours','Saturday'),('list_campus_events','Saturday'),('get_library_hours','Monday')]:
                result=await session.call_tool(tool,{'day':day})
                outputs[tool+' '+day]=json.loads(result.content[0].text)
            assert outputs['get_library_hours Saturday']['hours']=='Closes at 6 PM'
            assert outputs['get_library_hours Monday']['hours']=='Not available'
            record('Lesson 6 additional real calls',outputs)

asyncio.run(asyncio.wait_for(checks(),timeout=30))
lesson7=run_sync_cell(19)
assert 'TOOL: search_campus_records' in lesson7 and 'TOOL: required_exam_score' in lesson7
assert 'Observed tool calls: 2' in lesson7
record('Lesson 7 exact notebook cell; scripted model and vectors, real SDK/local tools',lesson7)

# Verify actual tool results sent back through the SDK, rather than only matching printed text.
responses=[part['functionResponse'] for req in http_requests for content in req['payload'].get('contents',[]) for part in content.get('parts',[]) if 'functionResponse' in part]
assert any(r['name']=='required_exam_score' and '110.0' in json.dumps(r['response']) for r in responses)
assert any(r['name']=='search_campus_records' and DOCUMENTS[0]['text'] in json.dumps(r['response']) for r in responses)
record('SDK round-trip verification','PASS: real calculator result and actual S1 text returned to scripted endpoint')

destination=ROOT/'Lesson_5_6_7_Test_Report.md'
lines=['# Lessons 5–7: execution report','',
       'No live Gemini calls were made. No user credential was accessed. All model replies and embedding vectors in SDK integration checks were explicitly scripted test fixtures. They verify code orchestration, not genuine model decisions, semantic retrieval quality, or generated answer quality.','',
       'The MCP server and calculator executed for real. All campus records are fictional.','']
for item in report:
    result=item['result']
    if not isinstance(result,str):result=json.dumps(result,indent=2)
    lines+=['## '+item['check'],'','```text',result,'```','']
lines+=['## Remaining live checks','',
        '- Gemini selecting the right calculator arguments in Lesson 5.',
        '- Gemini choosing and using the MCP tools in Lesson 6.',
        '- Real embeddings, genuine tool selection, final source citations, and task constraints in Lesson 7.',
        '- Rate limits, account access, model-specific behavior, and live response latency.',
        '', 'The original Lesson 6 bridge failed before contacting a model: the installed SDK attempted to deep-copy a live MCP session and raised TypeError involving an asyncio.Future. The notebook now discovers MCP schemas and uses an explicit function-call loop instead. The corrected bridge passed the scripted-response integration test.','',
        'The MCP subprocess also received an isolated dependency directory for these tests; a normal Colab pip installation does not need that testing path.','']
destination.write_text('\n'.join(lines),encoding='utf-8')
print('ALL CHECKS PASSED. Report:',destination)
