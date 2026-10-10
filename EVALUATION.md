# Results and remaining verification

Recorded from outputs shared during the project walkthrough. No missing model output has been reconstructed as a real result.

## Live observations: Lessons 1–4

| Lesson | Actual observation | What the evidence supports |
|---|---|---|
| 1. Prompting | A broad prompt produced a long embedding explanation. The specific prompt produced a campus-club analogy, three key points, and a practice question. | Specifying audience and structure changed the presentation in these runs. |
| 2. Saved preferences | With MIS, mornings, and 25 minutes loaded, the response proposed two 25-minute morning sessions. After changing the file to evenings and reloading, it proposed two 25-minute evening sessions. | Application-supplied preferences affected the response. Proposed weekdays were suggestions. |
| 3. Embeddings | Vectors had 3,072 dimensions. Laptop/computer similarity was 0.959; laptop/pizza was 0.718; computer/pizza was 0.712. | Related sentences ranked higher in this example; similarity is not a confidence probability. |
| 3. Revised comparison | Replacing pizza with “I need a portable computer for my classes” gave 0.912 with laptop and 0.916 with computer. | The replacement was more similar to the other two sentences than the pizza sentence in the observed outputs. |
| 4. Grounded answer | Retrieved S1 at 0.758, S2 at 0.633, S3 at 0.561. Answer: biology final December 10, 9 AM, worth 20%, citing S1. | The answer matched the supplied fictional record. |
| 4. Missing information | Retrieved S1 at 0.727, S2 at 0.663, S3 at 0.623. Answer: “Not available in these records.” | The model did not invent a room number in this run. |

These are demonstration outputs, not a benchmark. Named embedding dimensions and word analogies in the basic explanation are simplified illustrations, not universal properties of all embedding models.

## Live verification still needed: Lessons 5–7

| Lesson | Pass criteria | Current status |
|---|---|---|
| 5. Calculator | Gemini calls the Python calculator, receives 110% for current grade 85%, final weight 20%, target 90%, and explains that the target is impossible without extra credit. | Calculator and SDK orchestration passed locally with scripted responses; live model decision pending. |
| 6. MCP | Tools are discovered; Gemini selects and uses a tool; Friday library answer matches 10 PM and Coding Circle matches 2–3 PM, free. Trace records the actual tool call. | Real local MCP discovery and calls passed; live Gemini-to-MCP decision pending. Use the corrected explicit bridge. |
| 7. Agent | Trace shows retrieval/calculator use as needed; answer uses returned facts, reports any unattainable grade target accurately, and proposes a plan consistent with supplied preferences. | SDK orchestration passed using scripted responses and synthetic embeddings; live behavior pending. |

Exact wording may vary. A fluent answer without the relevant tool trace does not establish that tool use worked.

## Errors encountered

- Some generation requests returned 503 high-demand errors. Subsequent preference demos succeeded.
- An additional Lesson 4 run returned 429 quota exhaustion. Further live verification is paused until quota is available.
- The original direct MCP-session configuration failed during SDK copying before a model request. The notebook now discovers schemas and uses an explicit bounded function-call bridge.

## Update after the live run

For each pending lesson, add the date, question, relevant tool trace, answer, and whether it meets the pass criteria. Remove sensitive account details from shared output. Update the README status only after observing successful runs. The optional computing-project deadline check also remains unrecorded.

No video has been recorded and no LinkedIn post has been published as part of these tests.
