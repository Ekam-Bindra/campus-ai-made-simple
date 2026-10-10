# Lessons 5–7: execution report

No live Gemini calls were made. No user credential was accessed. All model replies and embedding vectors in SDK integration checks were explicitly scripted test fixtures. They verify code orchestration, not genuine model decisions, semantic retrieval quality, or generated answer quality.

The MCP server and calculator executed for real. All campus records are fictional.

## Lesson 5 direct calculator (real Python)

```text
{
  "required_exam_percent": 110.0,
  "possible_without_extra_credit": false,
  "target_already_secured_at_zero_exam_score": false
}
```

## Calculator edge checks

```text
PASS: reachable target, invalid weights, and non-finite inputs
```

## Lesson 5 exact notebook cell; scripted model, real SDK and calculator

```text
MANUAL CHECK: {'required_exam_percent': 110.0, 'possible_without_extra_credit': False, 'target_already_secured_at_zero_exam_score': False}
TOOL CALL: required_exam_score {'current_grade': 85.0, 'final_weight': 0.2, 'target_grade': 90.0}
TOOL RESULT: {'result': {'required_exam_percent': 110.0, 'possible_without_extra_credit': False, 'target_already_secured_at_zero_exam_score': False}}
EXPLANATION: SCRIPTED TEST RESPONSE: calculator result is {"required_exam_percent": 110.0, "possible_without_extra_credit": false, "target_already_secured_at_zero_exam_score": false}. Target requires more than 100%.

```

## Lesson 6 MCP discovery and Friday call (real local server)

```text
DISCOVERED TOOLS: ['get_library_hours', 'list_campus_events']
TOOL RESULT: {"fictional": true, "day": "Friday", "hours": "Closes at 10 PM"}

```

## Lesson 6 exact Gemini-to-MCP notebook cell; scripted model, real SDK/server

```text
MCP TOOL: get_library_hours {'day': 'Friday'}
MCP RESULT: {'content': [{'type': 'text', 'text': '{"fictional": true, "day": "Friday", "hours": "Closes at 10 PM"}'}], 'structuredContent': {'result': '{"fictional": true, "day": "Friday", "hours": "Closes at 10 PM"}'}, 'isError': False}
MCP TOOL: list_campus_events {'day': 'Friday'}
MCP RESULT: {'content': [{'type': 'text', 'text': '{"fictional": true, "day": "Friday", "events": [{"name": "Coding Circle", "start": "2 PM", "end": "3 PM", "cost": 0}]}'}], 'structuredContent': {'result': '{"fictional": true, "day": "Friday", "events": [{"name": "Coding Circle", "start": "2 PM", "end": "3 PM", "cost": 0}]}'}, 'isError': False}
SCRIPTED TEST RESPONSE: Friday Coding Circle runs 2–3 PM and the fictional library closes at 10 PM.

```

## Lesson 6 additional real calls

```text
{
  "get_library_hours Saturday": {
    "fictional": true,
    "day": "Saturday",
    "hours": "Closes at 6 PM"
  },
  "list_campus_events Saturday": {
    "fictional": true,
    "day": "Saturday",
    "events": [
      {
        "name": "Community Garden volunteering",
        "start": "10 AM",
        "end": "noon",
        "cost": 0
      }
    ]
  },
  "get_library_hours Monday": {
    "fictional": true,
    "day": "Monday",
    "hours": "Not available"
  }
}
```

## Lesson 7 exact notebook cell; scripted model and vectors, real SDK/local tools

```text
TOOL: search_campus_records {'query': 'biology final exam date and weight'}
RESULT: search_campus_records {'result': [{'source_id': 'S1', 'title': 'Sample biology syllabus', 'text': 'The biology final exam is December 10 at 9 AM. It is worth 20% of the final grade. Homework is worth 30%.'}, {'source_id': 'S2', 'title': 'Sample computing syllabus', 'text': 'The computing final exam is December 12 at 2 PM. The project deadline is December 5. Office hours are Tuesday at 3 PM.'}, {'source_id': 'S3', 'title': 'Sample campus events', 'text': 'Friday: Coding Circle, a free technology workshop, runs from 2 PM to 3 PM. Saturday: Community Garden volunteering runs from 10 AM to noon.'}]}
TOOL: required_exam_score {'current_grade': 85.0, 'final_weight': 0.2, 'target_grade': 90.0}
RESULT: required_exam_score {'result': {'required_exam_percent': 110.0, 'possible_without_extra_credit': False, 'target_already_secured_at_zero_exam_score': False}}
Observed tool calls: 2
SCRIPTED TEST RESPONSE: Biology final December 10 at 9 AM; weight 20% [S1]. Calculator returned 110%, impossible without extra credit. Proposed morning sessions: December 8 and 9, 25 minutes each; confirm availability. Nothing booked.

```

## SDK round-trip verification

```text
PASS: real calculator result and actual S1 text returned to scripted endpoint
```

## Remaining live checks

- Gemini selecting the right calculator arguments in Lesson 5.
- Gemini choosing and using the MCP tools in Lesson 6.
- Real embeddings, genuine tool selection, final source citations, and task constraints in Lesson 7.
- Rate limits, account access, model-specific behavior, and live response latency.

The original Lesson 6 bridge failed before contacting a model: the installed SDK attempted to deep-copy a live MCP session and raised TypeError involving an asyncio.Future. The notebook now discovers MCP schemas and uses an explicit function-call loop instead. The corrected bridge passed the scripted-response integration test.

The MCP subprocess also received an isolated dependency directory for these tests; a normal Colab pip installation does not need that testing path.
