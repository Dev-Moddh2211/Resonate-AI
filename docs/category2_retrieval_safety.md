# Retrieval safety

The local retriever uses lexical similarity as an explainable offline substitute for embeddings. Scores are ranking signals, not probabilities: below 0.12 returns `no_trusted_result`; 0.12–0.219 is low, 0.22–0.349 medium, and 0.35+ high. Because all current sources are synthetic, results are never official policy. Conflicts and version changes require review; no result is forced for an unknown query.
