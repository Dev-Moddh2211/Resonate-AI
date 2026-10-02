# Retrieval evaluation

Run `python -m knowledge_base.evaluate` after building the index, or run the test suite. The JSON cases and honest results are stored in `evaluation/retrieval_tests.json` and `evaluation/retrieval_results.json`. The five required cases cover product, policy, qualification, FAQ, and objection, followed by unknown, irrelevant, ambiguous, version/conflict, terminology, noisy, and conversational cases. Results are generated from the actual index; low-confidence and wrong-source cases remain visible.

The known generic query was previously lexical-only: `What documents are needed?` ranked the broad product chunk (`SRC-001-R003`, 0.1804) first because it shared the word “documents”. After hybrid retrieval, heading/semantic/category signals rank a more specific FAQ or document result first. This is a measured ranking change, not an accuracy claim; the complete result and score are regenerated in `evaluation/retrieval_results.json`.
