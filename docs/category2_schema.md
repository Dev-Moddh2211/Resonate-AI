# Knowledge record schema

Chunks are JSON records with `record_id`, `chunk_id`, `document_id`, `title`, `content`, `category`, `source_id`, `source`, `section`, `source_location`, `page`, `version`, `effective_date`, `authority_level`, `pii`, and `tags`. `content` is cleaned source text; `source_id` and location provide citation traceability; authority/version prevent synthetic content being mistaken for policy.

Representative records are generated in `data/processed/chunks.json` for product, qualification, FAQ, documents, objection, and PII categories. The schema is intentionally shared across Category 1's contract: retrieval wraps each record with content, source, source_id, metadata, confidence, version, and effective_at.
