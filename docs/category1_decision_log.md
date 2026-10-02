# Category 1 decision log

## Business-loan qualification

The assessment permits several Q1 use cases. Business-loan qualification was selected and frozen because it gives the project a concrete information-collection, qualification, objection, fallback, and handoff workflow without claiming underwriting.

## Rules outside the LLM

Qualification states and safety boundaries are configuration-driven so they can be reviewed and changed without rewriting a prompt. The tradeoff is a later evaluator to validate extracted values.

## Knowledge-base dependency

Policy and product answers must come from Category 2 retrieval with source, confidence, and version metadata. This avoids a disconnected voice bot and hardcoded policy prompt, but requires a trustworthy source corpus before Q3.

## Planned and mocked integrations

Voice, retrieval, CRM, transfer, localization, and streaming are planned or interface-only because their providers, sources, and business approvals are not available in Category 1. No mock is described as production-ready.

## Simplicity and assumptions

The architecture is document-first and intentionally avoids premature services or infrastructure. Required fields and the complete-profile preliminary state are explicit assumptions, not lender policy, and must be replaced with approved criteria.
