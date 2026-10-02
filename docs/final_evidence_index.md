# Final evidence index

This index distinguishes repository evidence from user-capture evidence.

## Question 1

- Implementation: `voice_agent/manager.py`, `voice_agent/rules.py`, `knowledge_base/retrieval.py`.
- Runtime tests: `tests/category3_test.py`.
- Required recordings/transcripts/results: `evidence/category1/` — **USER ACTION REQUIRED**.

## Question 2

- Synthetic source pack: `data/raw/synthetic/`.
- Pipeline and schema: `knowledge_base/`, `docs/category2_*.md`.
- Query-level results: `evaluation/retrieval_results.json` and `evaluation/retrieval_tests.json`.
- Limitation: no real business source pack was supplied.

## Question 3

- Configurations: `localization/philippines/`, `localization/indonesia/`.
- Examples: `docs/category3_localization_evidence.md`.
- Four real market recordings and native/accent validation: **USER ACTION REQUIRED**.

## Question 4

- Audio/replay/ASR: `evidence/category5/audio/`, `realtime/`.
- Scenario results: `evaluation/category5_demo_results.json`.
- Browser dashboard, live screen recording, and browser-receipt latency: **USER ACTION REQUIRED**.

## Final submission

README, setup, environment templates, architecture, limitations, and production plan exist. Video walkthrough, real call recordings, and deployment runtime verification remain outstanding.
