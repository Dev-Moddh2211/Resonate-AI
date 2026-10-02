# AI Business Loan Qualification Assistant

Category 1 foundation for a preliminary business-loan qualification assistant. It helps a small-business owner share basic information, receive trusted general information from the Q2 knowledge base when retrieval is confident, and get a structured human handoff. It never approves or denies a loan, promises approval, or invents terms.

## Status

Category 1 = COMPLETE. Category 2 = IMPLEMENTED. Category 3 = IMPLEMENTED as a provider-neutral callable webhook prototype. Category 4 = IMPLEMENTED as localized prototypes. Category 5 = PARTIAL: incremental pre-labelled transcript replay, signal detection, nudge controls, polling boundary, and tests; streaming ASR, audio replay, and dashboard delivery remain unimplemented.

Category 2 provides a local, traceable knowledge-base pipeline: synthetic-prototype source inventory, format-aware extraction, cleaning, PII redaction, section-aware chunking, metadata indexing, retrieval, citations, and evaluation cases. Q1 is connected to the Q2 knowledge base at runtime: `ConversationManager` invokes the Q2 retriever for knowledge-grounded questions and preserves source metadata/citations. Deterministic qualification rules handle structured fields; when no trusted KB result exists, Q1 uses safe fallback or escalation rather than inventing information. Run `python -m knowledge_base.cli "What documents are needed?"` or `python -m unittest discover -s tests -p '*category2_test.py'`.

## Structure

`docs/` contains scope, requirements, architecture, state/failure design, assumptions, safety, evidence, examples, and traceability. `config/` contains reviewable YAML policies and Category 2 taxonomy/terminology. `knowledge_base/` contains extraction, processing, chunking, indexing, and retrieval.

## Setup

Install backend dependencies with `python -m pip install -r requirements.txt`. For the Vite frontend, run `npm install` in `frontend/`, copy `frontend/.env.example` to `frontend/.env.local`, and set `VITE_API_BASE_URL=http://localhost:8080`. Start the backend with `python -m voice_agent.http_server` and the frontend with `npm run dev` from `frontend/`. Never commit `.env`, credentials, recordings, transcripts, or customer data.

## Deployment

The frontend is a static React/Vite site deployed to Vercel. Set the project root to `frontend`, build command to `npm run build`, output directory to `dist`, and `VITE_API_BASE_URL` to the public Render service URL, for example `https://loan-assistant-api.onrender.com`.

The backend is a Render Web Service. Install with `pip install -r requirements.txt` and use the start command `python -m voice_agent.http_server`. The server binds to `0.0.0.0` and reads Render's `PORT` (falling back to `8080` locally). Set `FRONTEND_ORIGIN` to the Vercel origin; comma-separated origins are supported for local plus deployed testing. Required backend variables are `ASR_MODEL`, `ASR_DEVICE`, `ASR_COMPUTE_TYPE`, and `FRONTEND_ORIGIN`. Faster-Whisper may download/load the model during startup or first realtime use; downloaded model files are not committed and persistent local storage must not be assumed on Render Free.

The backend exposes `GET /health`, the existing `/api/*` endpoints, and `/realtime/events`. Browser microphone access requires user permission and a secure context (HTTPS in deployment; localhost is allowed for local development). No API secrets belong in `VITE_*` variables.

## Security note

Only synthetic test data belongs in this repository. Treat future customer fields, recordings, and transcripts as controlled PII; do not commit them.

## Not implemented

Run `python -m voice_agent.http_server` and expose `/voice/start` over HTTPS to a configured telephony provider. The manager uses the Category 2 retriever, deterministic qualification configuration, grounded source metadata, safe fallback, conflict preservation, and human escalation. The webhook is a prototype: state is in memory and transfer is a handoff, not a claimed live human connection. Local browser/JSON clients can call `ConversationManager` directly.
