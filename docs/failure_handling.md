# Failure handling

| Situation | Behavior | State/result |
|---|---|---|
| Known information | Retrieve trusted context, answer with source/version | Continue |
| Unknown information | State it is unavailable, offer alternative or human help | Escalate when unresolved |
| Low confidence | Do not answer confidently; ask or hand off | `human_review`/`escalated` |
| Conflicting information | Identify conflict and ask which value is correct; never silently overwrite | `needs_clarification`/`human_review` |
| Human request | Acknowledge, preserve context, create handoff, offer transfer/callback | `escalated` |
| System failure | Plain fallback without technical internals; mark recovery | `escalated` |

Fallback language: “I don’t have a verified answer for that. I can record the question and arrange human assistance.”
