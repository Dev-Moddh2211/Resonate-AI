# Deployment audit

## Target configuration

- Frontend: React/Vite/TypeScript static build on Vercel.
- Backend: Python `voice_agent.http_server` on a Render Web Service.
- Backend start command: `python -m voice_agent.http_server`.
- Backend bind: `0.0.0.0`; port: `int(os.getenv("PORT", "8080"))`.

## Required environment variables

Backend:

- `PORT` — supplied by Render.
- `FRONTEND_ORIGIN` — the Vercel origin, such as `https://loan-assistant.vercel.app`; local default is `http://localhost:5173`.
- `ASR_MODEL` — defaults to `base.en`.
- `ASR_DEVICE` — defaults to `cpu`.
- `ASR_COMPUTE_TYPE` — defaults to `int8`.

Frontend:

- `VITE_API_BASE_URL` — the Render backend origin, such as `https://loan-assistant-api.onrender.com`.

Do not put secrets in `VITE_*` variables. The Faster-Whisper model is downloaded/loaded at runtime as needed; it is not stored in Git and Render Free persistent local storage is not assumed.

## Deployment checks

The backend provides `GET /health` without initializing ASR. Browser API requests use `VITE_API_BASE_URL`; the backend permits configured origins and handles CORS preflight. Browser microphone access requires permission and HTTPS (secure context), with localhost supported during development.

## Deployment boundary

The Render service is the Python backend/API. Its `GET /` handler serves the legacy `web/index.html` fallback, while `/api/*`, `/voice/*`, and `/realtime/*` are backend endpoints. The React/Vite/TypeScript frontend is intended to be built and deployed separately to Vercel.

The repository contains only synthetic demo WAV fixtures under `evidence/category5/audio/`; recordings, model files, credentials, and customer information are excluded by `.gitignore` and must not be added.

## Provider settings

Vercel:

1. Root directory: `frontend`.
2. Build command: `npm run build`.
3. Output directory: `dist`.
4. Environment variable: `VITE_API_BASE_URL=https://<render-service>.onrender.com`.

Render Web Service:

1. Build command: `pip install -r requirements.txt`.
2. Start command: `python -m voice_agent.http_server`.
3. Environment variables: `FRONTEND_ORIGIN`, `ASR_MODEL=base.en`, `ASR_DEVICE=cpu`, and `ASR_COMPUTE_TYPE=int8`; Render supplies `PORT`.
