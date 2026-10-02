# Conversation flow

| State | Purpose | Exit | Failure / next states |
|---|---|---|---|
| `GREETING` | Introduce assistant and preliminary scope | consent or decline | decline → close |
| `PURPOSE_CONSENT` | Confirm purpose and permission | consent | unclear → clarification |
| `BASIC_CUSTOMER_DETAILS` | Collect identity/contact | complete | missing → clarification/incomplete |
| `BUSINESS_DETAILS` | Collect business context | complete | conflict → human_review |
| `LOAN_REQUIREMENT` | Collect amount and purpose | complete | ambiguity → clarification |
| `QUALIFICATION` | Run deterministic rules | explicit preliminary state | missing/conflict → incomplete/human_review |
| `QUESTIONS_OBJECTIONS` | Retrieve Q2 KB answer or use safe fallback | resolved/no question | unsupported → escalation |
| `NEXT_STEP` | Explain state and path | accepted next step | human request → escalated |
| `CLOSING` | Summarize and end | ended | system error → escalated |

Normal flow: `GREETING → PURPOSE_CONSENT → BASIC_CUSTOMER_DETAILS → BUSINESS_DETAILS → LOAN_REQUIREMENT → QUALIFICATION → QUESTIONS_OBJECTIONS → NEXT_STEP → CLOSING`. Any state may enter clarification; human request/system failure may enter `escalated`.

## Communication style and examples

The future agent is professional, concise, clear, non-pushy, transparent about uncertainty, respectful, and willing to clarify. It avoids guarantees, fabricated information, repetitive questions, and unnecessary explanation.

“I can collect details for preliminary review, but I can’t approve a loan. What would you use the funding for?” If the customer does not know revenue, record unknown rather than guess. For “Can you guarantee approval?” say: “I can’t guarantee approval. I can collect details for preliminary review or connect you with a person.”
