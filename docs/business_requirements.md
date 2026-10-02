# Customer information model

| Field | Classification | Why / when | Example | If unknown | Sensitive? |
|---|---|---|---|---|---|
| `full_name` | required | Identify caller early | Test Customer A | Ask once; mark incomplete | Yes |
| `business_name` | required | Identify business | Example Business 01 | Clarify or mark incomplete | Yes |
| `business_type` | required | Understand context | retail shop | Clarify broad category | Potentially |
| `years_in_business` | conditional | Use only if approved rules require tenure | 4 years | Do not infer | No |
| `annual_revenue_range` | optional/conditional | Preliminary profile if policy requires it | 10–25 lakh | Record unknown | Financial |
| `requested_loan_amount` | required | Understand request | 5 lakh | Clarify amount/range | Financial |
| `loan_purpose` | required | Route request/questions | equipment purchase | Ask broad purpose | Potentially |
| `existing_business_loan` | optional/conditional | Relevant only under approved criteria | yes, approximate balance | Record unknown | Financial |
| `preferred_callback_time` | optional | Arrange follow-up | weekday afternoon | Offer available path | No |
| `contact_number` | required | Follow-up route | synthetic test number | Cannot promise callback | Yes |
| `email` | optional | Alternative follow-up | test@example.invalid | Continue without it | Yes |
| `additional_notes` | optional | Capture volunteered context | seasonal cash flow | Do not solicit extra detail | May be sensitive |

Required status is a prototype workflow choice, not official lender policy; the owner must confirm fields and retention rules.
