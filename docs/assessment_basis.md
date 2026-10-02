# Assessment basis and implementation boundary

## Assessment requirements extracted from `ai_assignment.pdf`

The assessment evaluates functional outcomes, grounded responses, reliability, measurable evidence, and explainable technical choices. It requires Q1's voice agent to use Q2's knowledge base, avoid hardcoded FAQ/policy answers, handle qualification, objections, unsupported questions, and human escalation, and provide calls/transcripts/results in the final submission. Later requirements cover a production-ready knowledge base (Q2), localized Philippines/Indonesia voice bots (Q3), and real-time call insights/nudges (Q4).

## Project-owner instructions

The pasted implementation brief narrows this run to Category 1 only, freezes business-loan qualification as the Q1 use case, requires the documents/configuration in this repository, and explicitly prohibits implementing Categories 2–5. Those instructions control the current implementation scope.

## Decisions made for this repository

The project uses a preliminary qualification assistant, not a lending decision system. Where the assessment specifies behavior but not business thresholds, the repository records a prototype assumption and leaves the criterion configurable. No official policy, customer record, integration, test result, or performance number is fabricated.
