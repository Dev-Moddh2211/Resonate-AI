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

**Implemented now (Category 1):** documented scope, YAML rule/configuration boundaries, deterministic qualification state/failure design, the Q1 conversation runtime, and its Q2 knowledge-base retrieval integration. **Planned later:** production source/provider expansion, Category 3 voice/ASR/TTS providers, Category 4 localization, and Category 5 real-time intelligence. The local Q1 runtime uses the Q2 retriever for knowledge-grounded questions, preserves source metadata, and safely falls back when no trusted result exists.

Voice handles audio, state management owns flow, rules own deterministic decisions, retrieval owns trusted context, generation turns approved context into language, validation blocks unsafe claims, and external actions are adapters requiring authorization.

The boundaries permit replacing a provider or embedding model without rewriting the state machine. Future components are not presented as implemented.
