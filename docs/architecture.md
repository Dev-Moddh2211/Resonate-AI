# Shared architecture

```text
Caller → Voice interface → ASR → Conversation manager
                              ↙              ↘
                    Future KB/RAG        Configured rules
                              ↘              ↙
                Response generation → validation → TTS → Caller

Future Category 5: live audio → streaming ASR → signals → nudge engine
                              → controls → dashboard/WebSocket/API
```

## Current versus planned

**Implemented now (Category 1):** documented scope, YAML rule/configuration boundaries, state/failure design, contracts, and test/evidence plans. **Planned later:** Category 2 ingestion/retrieval; Category 3 voice, ASR/TTS, and conversation runtime; Category 4 localization; Category 5 real-time intelligence. No planned component is functional in this repository.

Voice handles audio, state management owns flow, rules own deterministic decisions, retrieval owns trusted context, generation turns approved context into language, validation blocks unsafe claims, and external actions are adapters requiring authorization.

The boundaries permit replacing a provider or embedding model without rewriting the state machine. Future components are not presented as implemented.
