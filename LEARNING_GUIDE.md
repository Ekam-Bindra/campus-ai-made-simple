# Start here: seven hands-on Gemini lessons

Build understanding by running an example, changing one thing, and checking what happened. You do not need prior AI experience. The notebook uses Python; you can start by reading the comments and changing the marked strings and numbers.

**Project:** [Campus AI Made Simple](https://github.com/Ekam-Bindra/campus-ai-made-simple)

**Launch:** [Open the notebook in Google Colab](https://colab.research.google.com/github/Ekam-Bindra/campus-ai-made-simple/blob/main/Campus_AI_Made_Simple.ipynb)

## Before you begin

- A Google account, browser, and internet connection.
- Your own Gemini API key from [Google AI Studio](https://aistudio.google.com/api-keys).
- Access to the generation and embedding models configured in the notebook. API quota and possible charges depend on your project and account configuration.
- About 90–150 minutes for a first walkthrough, excluding API interruptions. You can also complete one lesson at a time.

All syllabus, event, and library records are fictional. They are practice data, not real campus schedules. No personal documents are needed.

**Testing status:** the author has shared live Gemini outputs for Lessons 1–4. Lessons 5–7 have local tool/integration checks; live Gemini verification is pending. Expected behavior below describes what to check, not a promise that every run will pass. See [EVALUATION.md](EVALUATION.md).

## 0. Set up from scratch

1. Open the Colab link above. If you want to retain your edits, save a copy to your Google Drive using Colab's File menu. An alternative is to download `Campus_AI_Made_Simple.ipynb` from this repository and upload it to Colab.
2. Read the opening explanation. A **cell** is a block of code or text; a **runtime** is the temporary Python environment running your code.
3. Run the first code cell, which starts with `%pip install`. Use the play button beside it or Shift + Enter. Wait for it to finish before continuing.
4. Run the helper-writing cell beginning `from pathlib import Path`. It creates `campus_ai.py` and `campus_mcp_server.py` in the runtime. You do not need to upload those files separately in Colab.
5. Run the setup cell beginning `import getpass`. Enter your key only into the hidden input prompt. Do not paste it into notebook source, a screenshot, an issue, or a commit.
6. Check that a one-sentence explanation of a language model appears. This is your first live API request; if it errors, use the troubleshooting section before moving on.
7. Run the lesson cells in order. If one succeeds, preserve its output rather than rerunning it unnecessarily.

The setup uses `gemini-flash-latest` for generation and `gemini-embedding-001` for embeddings. If a model is unavailable, check your available models before editing `MODEL` or `EMBED_MODEL`, then rerun setup so the `campus` object uses the change. Model aliases can change over time.

### Optional: run on your computer instead

Clone or download the repository, open a terminal in its root folder, and use Python 3.10+:

```bash
python -m venv .venv
```

Activate the environment:

```bash
# macOS / Linux
source .venv/bin/activate
```

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Then install and launch:

```bash
python -m pip install -r requirements.txt
python -m jupyterlab Campus_AI_Made_Simple.ipynb
```

Run the same notebook setup cells. Local lesson instructions below are identical. Jupyter notebooks support the top-level `await` used in Lesson 6; these cells are not standalone terminal scripts.

## 1. Prompting: ask for the explanation you need

**Goal:** see how audience, format, and constraints affect a response. A prompt is the instruction and context you send to the model.

### Run

1. Find **“1. Prompting: make your learning goal explicit.”**
2. Read the two prompts in the next code cell. The first says `Explain embeddings.` The second specifies a college beginner, three short bullets, a campus-club analogy, and a practice question.
3. Run that cell once. It makes two generation requests.
4. Compare the outputs: does the specific response follow the format, avoid unexplained jargon, and leave the practice answer for you to attempt?

### Change one thing

Replace the topic in **both** prompts with `database normalization` or a topic you are studying. Keep the audience and format instructions. Run the comparison again only if you have quota available.

### Check your understanding

- Which version is easier for a beginner to follow, and why?
- Did either response contain something you should verify against course materials?
- Why is a shorter answer not automatically a more accurate one?

**Completion evidence:** one observed difference between the responses and one improvement you would make to the specific prompt. The second answer need not be “better” to complete the experiment.

## 2. Saved preferences: personalize with supplied context

**Goal:** distinguish application-managed storage from the model remembering something by itself.

### Run

1. Find **“2. Context vs saved preferences.”**
2. Read the saved values: major `MIS`, study time `mornings`, and session length `25` minutes.
3. Run the cell. It saves `student_preferences.json`, asks for study suggestions without the preferences, reloads the file, and sends the same task with the preferences attached.
4. Check the printed preferences and compare the two answers. The personalized answer should propose two 25-minute morning sessions suitable for an MIS student.

### Change one thing

Change `"study_time": "mornings"` to `"study_time": "evenings"` in the save call and rerun the cell. Verify that the printed file values and suggested sessions now use evenings. Rerunning this full cell makes two more generation requests.

### Check your understanding

- The application loads the JSON and supplies it in the prompt. It does not retrain Gemini.
- If the application stops supplying preferences, the model has no access to this file through this request.
- If the file is deleted, `load_preferences` raises a file error; the current notebook does not silently restore it.
- A suggested Tuesday or Thursday is a proposal, not proof of your actual availability.

**Completion evidence:** a changed preference appears both in the loaded values and in the answer, or you record where the model failed to follow it.

## 3. Embeddings: compare sentences numerically

**Goal:** understand an embedding as a learned numerical representation of text. Cosine similarity compares vector direction; it does not measure whether a statement is true.

### Run

1. Find **“3. Embeddings: compare meaning as vectors.”**
2. Read the three sentences: buying a laptop, purchasing a computer, and eating pizza.
3. Predict which pair should be most similar before running the cell.
4. Run it and inspect the vector dimension count and three pairwise similarity scores.
5. Compare the ranking with your prediction. Do not expect identical numbers across model versions or configurations.

### Change one thing

Replace `I love eating pizza` with `I need a portable computer for my classes`, then rerun. The helper caches repeated embeddings in the current `campus` object, so unchanged inputs can be reused.

### Check your understanding

- Did the replacement sentence rank as more similar to the first two?
- A score of `0.959` is not “95.9% correct.”
- Similarity can miss distinctions such as negation. Optionally compare “I want to buy a laptop” with “I do not want to buy a laptop.” Record what happens rather than assuming the result.

**Completion evidence:** the sentence pairs, actual scores, dimension count, and a short explanation of the observed ranking.

## 4. RAG: retrieve records and answer with evidence

**Goal:** observe retrieval-augmented generation: search records, supply relevant text, and generate an answer using that context.

### Run

1. Find **“4. Retrieval-augmented generation (RAG).”**
2. Run the cell and read the five fictional records it prints. The first search embeds the records, which uses embedding quota as well as generation quota for the answers.
3. For the biology exam question, inspect the retrieved records and the final citation.
4. Compare the answer directly with **S1**: December 10 at 9 AM, worth 20% of the final grade.
5. Read the missing-room answer. No record contains a room, so the expected response is `Not available in these records.`

### Change one thing

Add a new code cell after the lesson and run:

```python
print(campus.rag("When is the computing project deadline?"))
```

The supporting record is **S2**, and the deadline is December 5. Then, if quota permits, ask a question absent from the records:

```python
print(campus.rag("What is the biology professor's email address?"))
```

### Check your understanding

- Does the cited record support every factual claim in the answer?
- A retrieved record may be similar to your question without containing the answer.
- The similarity score is not confidence in the generated answer.
- One correct refusal to invent information does not establish reliability for every future question.

**Completion evidence:** one supported answer with a valid citation and one missing-information response. Record failures as issues rather than marking them as passes.

## 5. Function calling: let Python calculate

**Goal:** separate a model choosing a tool from software executing the calculation.

### Run

1. Find **“5. Tool calling: let Python do arithmetic.”**
2. Read the example: average on **all non-final work** = 85%; final weight = 20%; desired overall grade = 90%.
3. Run the cell. The manual Python calculation prints first; the live Gemini request follows.
4. Inspect `TOOL CALL`, `TOOL RESULT`, and `EXPLANATION`. The function should be `required_exam_score` with weight `0.2`, not `20`.
5. Confirm the returned required score is **110%** and `possible_without_extra_credit` is **False**. The model should preserve that result and explain that the target is unattainable without extra credit under this formula.

The calculation is:

```text
required score = (target - current × (1 - final weight)) / final weight
               = (90 - 85 × 0.8) / 0.2
               = 110
```

### Change one thing

Change the manual target from `90.0` to `85.0` **and** the prompt's desired overall grade from `90%` to `85%`. Rerun. The required final score is now 85%, which is attainable under the example's assumptions.

### If generation is unavailable

You can still run this in a separate code cell without a Gemini request:

```python
print(required_exam_score(85.0, 0.20, 90.0))
```

This checks Python arithmetic, not live Gemini tool selection. If only the manual result appears before an API error, do not mark the live lesson as passed.

**Completion evidence:** actual function-call and result traces, plus an explanation consistent with the calculation. A text-only answer is insufficient evidence of tool execution.

## 6. MCP: use tools from a separate server

**Goal:** distinguish the MCP client, the MCP server, and Gemini's tool choice. MCP is a protocol for connecting tools; it is not a model or database.

This lesson has **two code cells**. It can be postponed if you are short on time, but both stages are needed to verify the complete live example.

### Stage A: discover and call a tool locally

1. Find **“6. MCP: discover tools from a separate server.”**
2. Confirm setup created `campus_mcp_server.py`.
3. Run the first MCP cell beginning `import sys`. The notebook launches the server as a subprocess; you do not need a second terminal or a manually running server.
4. Check that `DISCOVERED TOOLS` lists `get_library_hours` and `list_campus_events`.
5. Confirm the Friday library tool returns `Closes at 10 PM` and marks its data as fictional.

This stage does not call Gemini. It can work while generation quota is exhausted.

### Stage B: let Gemini select MCP tools

1. Run the next cell beginning `async def gemini_mcp_demo():`.
2. It discovers tool schemas, sends them to Gemini, executes requested tools through MCP, and returns their results to the model.
3. Inspect actual `MCP TOOL` and `MCP RESULT` lines. The Friday question should use the tools for both the event and library hours.
4. Check the answer: Coding Circle is free, runs 2–3 PM, and the fictional library closes at 10 PM.

### Change one thing

In Stage B's question string, replace `Friday` with `Saturday` and rerun Stage B. Expected facts: Community Garden volunteering, 10 AM to noon, free; library closes at 6 PM.

For a local-only missing-data experiment, change `Friday` to `Monday` in Stage A's `session.call_tool(...)` arguments. The library tool should return `Not available`.

### Check your understanding

- **Client:** notebook code using `ClientSession`.
- **Server:** `campus_mcp_server.py`, which exposes the functions and their schemas.
- **Model:** Gemini, which requests tools in Stage B.
- The explicit bridge allows only discovered tool names and limits the exchange to three model turns.

**Completion evidence:** discovery output, actual MCP calls/results, and a live final answer consistent with them. Local discovery alone does not verify Stage B. This separate MCP lesson is not connected to the final agent in Lesson 7.

## 7. Bounded agent workflow: combine tools for a task

**Goal:** see a model use more than one tool to respond to a multi-step request within defined limits.

### Run

1. Find **“7. A small agentic workflow.”**
2. Read the task: find the biology exam date/weight, calculate the score needed for 90% overall from an 85% non-final average, and propose two 25-minute morning sessions before the exam.
3. Run the cell once. It can make several generation requests and embedding requests if the record vectors are not already cached.
4. Inspect `TOOL`, `RESULT`, and `Observed tool calls` before reading the final answer.
5. Check every requirement below.

| Check | Expected evidence |
|---|---|
| Exam information | Retrieved S1 supports December 10, 9 AM, and 20% |
| Calculation | Calculator receives the correct inputs and returns 110% |
| Interpretation | Answer flags the target as impossible without extra credit |
| Study proposal | Two 25-minute morning sessions before the fictional exam |
| Availability | Times are proposed, not claimed to be your actual free slots |
| Action scope | No claim that calendar events were created |

### Change one thing

Change `90% overall` to `85% overall` in `question` and rerun. The calculator should return 85%. Alternatively, change the requested sessions from mornings to evenings. In this lesson that preference comes from the question string; it does **not** automatically load the Lesson 2 preference file.

### Check your understanding

- Which tool provided facts, and which performed arithmetic?
- Did the final answer use the returned evidence accurately?
- The agent uses record search and the calculator directly. It does not use the Lesson 6 MCP server, access real campus systems, or write calendar events.
- The SDK configuration bounds automatic function-calling exchanges. This is a small teaching workflow, not a production autonomous assistant.

**Completion evidence:** actual tool traces and a final response meeting the task constraints. If the tool limit is reached or the answer omits a requirement, record the issue and simplify the request before another run.

## Troubleshooting

| Problem | What to do |
|---|---|
| `NameError` for `campus`, `client`, `types`, or `Path` | Run installation, helper-writing, and setup cells in order in the same runtime. Lesson 6 Stage B also needs Stage A definitions. |
| `ModuleNotFoundError` | Run installation and helper-writing cells. If you restart the runtime, run setup again. |
| API key/permission error | Check that the key belongs to a project you can use, that API access is configured, and that the selected model is available. |
| `429 RESOURCE_EXHAUSTED` | Read the error's quota metric and check AI Studio usage/limits. Stop repeated retries; a daily quota error is different from a per-minute limit. Limits apply per project, so another key for that same project does not restore quota. |
| `503 UNAVAILABLE` | Pause and retry the failed cell later; model demand/capacity can be temporary. Do not rerun all earlier lessons. |
| Missing model / `404` | Check available models and update the relevant model variable, then rerun setup. |
| Preference file missing | Run the Lesson 2 save step again. Runtime files may disappear when a session ends. |
| MCP server missing / process exits | Run helper-writing setup, check `campus_mcp_server.py` exists, and run Stage A before Stage B. |
| MCP `_asyncio.Future` copying error | Use this repository's corrected explicit bridge in Stage B; do not pass a live MCP session directly in Gemini's tool configuration. |
| No tool trace | Keep the result marked unverified; inspect the prompt and configuration. A plausible final sentence does not prove a tool was used. |
| Tool/turn limit reached | Simplify the task and inspect the trace. Record the issue instead of removing bounds just to obtain an answer. |
| Different wording or scores | Judge evidence and constraints rather than exact phrasing. Record model IDs and actual outputs. |

For official explanations, see [Gemini rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) and [Gemini troubleshooting](https://ai.google.dev/gemini-api/docs/troubleshooting). Daily request limits reset at midnight Pacific according to Google's rate-limit documentation; check your active quota rather than treating an error's suggested retry delay as a guaranteed reset.

If you switch to another authorized project's API key, rerun setup to recreate the client and `campus` object. If `GEMINI_API_KEY` is already set in the environment, setup uses that value instead of prompting; update or remove it in your own runtime before entering another key. Do not print credentials.

## Keep your own learning log

Copy this table into a separate document. Expected answers in this guide are not your observed results.

| Lesson | What I changed | What I actually observed | Pass / issue / pending | What I learned |
|---|---|---|---|---|
| 1. Prompting | | | | |
| 2. Preferences | | | | |
| 3. Embeddings | | | | |
| 4. RAG | | | | |
| 5. Function calling | | | | |
| 6. MCP: local + live | | | | |
| 7. Agent workflow | | | | |

Save the prompts, non-sensitive outputs, and tool traces you actually saw. If sharing a notebook, remove keys and private data. You do not need a video or a perfect run to document useful learning; preserve pending checks and failures honestly.

## Optional local developer checks

From the repository root with dependencies installed:

```bash
python run_lessons_5_6_7_checks.py
```

These checks execute real local functions/MCP calls and use scripted model replies plus synthetic embedding fixtures for SDK orchestration. They do not call live Gemini or replace live verification. They write a local report; review it before committing any changed results.

## Continue learning

- [Google Gen AI Python SDK](https://github.com/googleapis/python-genai)
- [Gemini embeddings](https://ai.google.dev/gemini-api/docs/embeddings)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Project evaluation and testing scope](EVALUATION.md)

After each lesson, explain the component in your own words and identify one limit. That is the learning goal, beyond obtaining a fluent model answer.
