# Business rules

The future system separates information extraction, rule evaluation, and response generation. A model may extract candidate values, but deterministic code evaluates `config/qualification_rules.yaml`. The response layer can explain a state; it cannot create a state or turn preliminary qualification into approval.

States are `incomplete`, `needs_clarification`, `preliminary_qualified`, `preliminary_not_qualified`, `human_review`, and `escalated`. Missing data is evaluated before qualification. Ambiguity and unresolved conflicts prevent a confident state. `preliminary_qualified` means suitable for further discussion only.

Current criteria are prototype assumptions because no approved lender policy was supplied. They must be replaced by versioned, business-approved criteria and sources before production.
