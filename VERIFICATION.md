# Verification

## Local code and infrastructure

- PASS: Calculator returns 110% for the target example and marks it unattainable without extra credit; reachable example returns 85%.
- PASS: Invalid weights and non-finite inputs are rejected.
- PASS: Cosine similarity and ranking helpers.
- PASS: RAG prompt retains source IDs and evidence.
- PASS: JSON preference round-trip.
- PASS: Notebook Python cells compile, excluding installation magic; notebook schema validates.
- PASS: Python helper modules compile.
- PASS: Real local MCP stdio handshake, tool discovery, and Friday/Saturday/missing-day calls.
- PASS: Actual Gemini SDK orchestration with scripted API replies invokes the real calculator and local tools.

Synthetic model replies and embedding fixtures test wiring. They do not verify live model decisions or semantic retrieval quality. See `Lesson_5_6_7_Test_Report.md` for detailed scope.

## Live Gemini evidence

The author supplied successful live outputs for Lessons 1–4: prompt comparison, reloaded study preferences, 3,072-dimensional embeddings, and grounded versus missing-information answers. See `EVALUATION.md`.

Lessons 5–7 await live verification after quota becomes available. No project API key is included. Notebook outputs are cleared; the results document preserves non-sensitive observations.


## Repository review — October 10, 2026

- PASS: Public project files are at the repository root, including README and notebook; cover asset is present.
- PASS: README links to the beginner guide and the Colab notebook.
- PASS: Relative document links resolve; notebook code compiles with notebook-style top-level await; outputs are clear.
- PASS: Corrected local checks resolve installed MCP dependencies instead of requiring a scratch-only directory. Real calculator and local MCP calls, plus scripted SDK round trips, passed again.
- Updated: Sharing guide reflects the current no-video plan.

This review did not make live Gemini requests and does not change the pending status of Lessons 5–7.
