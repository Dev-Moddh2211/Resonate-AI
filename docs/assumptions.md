# Assumptions register

## A1 — Preliminary fields

- **Assumption:** The prototype collects the fields in `business_requirements.md`.
- **Why needed:** A conversation and handoff require a defined information model.
- **Impact:** The assistant can demonstrate completeness without deciding creditworthiness.
- **Replacement:** Validate field necessity, definitions, and retention with the lender.

## A2 — Required fields

- **Assumption:** Name, business identity/type, purpose, requested amount, and contact number are required for preliminary review.
- **Why needed:** The prototype needs a deterministic completeness check.
- **Impact:** Missing values produce `incomplete`; this is not an eligibility policy.
- **Replacement:** Replace with approved operational requirements.

## A3 — Reviewable profile

- **Assumption:** A complete, consistent profile may be labelled `preliminary_qualified`.
- **Why needed:** No official thresholds or policy source was supplied.
- **Impact:** It means suitable for further discussion only, never approval.
- **Replacement:** Use approved effective-dated qualification criteria.
