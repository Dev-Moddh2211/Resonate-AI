# Technology decisions

| Technology/decision | Purpose | Reason | Alternative | Tradeoff/limitation |
|---|---|---|---|
| YAML rule layer | Store business rules | Rules remain reviewable and separate from prompts | Hardcode in prompt | Requires evaluator later; criteria are placeholders |
| Explicit state machine | Control conversation transitions | Transitions and failures are testable | Free-form agent loop | Less flexible, safer and explainable |
| Retrieval contract | Connect Q2 to the future agent | Q1 must consume trusted context | Hardcoded FAQs | Requires source/version/confidence metadata |
| Document-first Category 1 | Establish the foundation | No runtime need exists yet | Add framework/database now | Smaller scope; services come later |
