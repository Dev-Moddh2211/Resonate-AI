# Future knowledge-base contract

Category 2 will expose a retrieval interface consumed by the future Category 3 conversation manager. A request contains `query`, minimal `conversation_context`, and optional `topic`/`locale`. A response contains `records[]` with `content`, `source`, `source_id`, `metadata`, `confidence`, and `version`/`effective_at`, plus retrieval status.

The manager answers only when records are trusted and sufficiently relevant. It retains source/version metadata for evidence. Empty or low-confidence results trigger fallback; the model must not compensate with memorized policy or a giant prompt. Changing embeddings/storage must not change the state-machine contract.
