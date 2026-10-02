# Category 1 decision log

## Business-loan qualification

The assessment permits several Q1 use cases. Business-loan qualification was selected and frozen because it gives the project a concrete information-collection, qualification, objection, fallback, and handoff workflow without claiming underwriting.

## Rules outside the LLM

Qualification states and safety boundaries are configuration-driven so they can be reviewed and changed without rewriting a prompt. The tradeoff is a later evaluator to validate extracted values.

## Knowledge-base dependency

Policy and product answers come from the Category 2 retriever with source, confidence, and version metadata. Q1 invokes that retriever at runtime for knowledge-grounded questions; if no trusted result exists, it falls back safely or escalates rather than inventing an answer. The current source corpus is synthetic and must be replaced with authorized sources before production use.

## Planned and mocked integrations

External voice providers, CRM, transfer, and production streaming remain planned or interface-only because their providers and business approvals are not available in Category 1. The local Q1-to-Q2 retrieval integration is implemented; no mock is described as production-ready.

## Simplicity and assumptions

The architecture is document-first and intentionally avoids premature services or infrastructure. Required fields and the complete-profile preliminary state are explicit assumptions, not lender policy, and must be replaced with approved criteria.
