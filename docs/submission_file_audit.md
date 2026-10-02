# Final submission file audit

Read-only packaging audit performed 2026-10-02. No application code, tests,
`.gitignore`, or existing documentation/evidence was changed. This report is
the only requested new file. The ZIP command below was not executed.

## Inventory summary

- 2,799 files and 382 directories were found recursively (excluding `.git`
  from the reported inventory), including generated dependencies and caches.
- 138 files were Git-tracked before this report; the working tree was clean.
- The source/evidence inventory excluding `frontend/node_modules/`,
  `frontend/dist/`, Python `__pycache__/`, and `frontend/.wrangler/` contains
  143 files.
- The dominant generated tree is `frontend/node_modules/` (about 304 MB);
  `frontend/dist/` is about 252 KB. The source, docs, data, evaluation, and
  evidence are about 2 MB.

| Area | Files / size | Git status | Recommendation |
|---|---:|---|---|
| `config/` | 8 / 32 KB | tracked | INCLUDE: business and realtime rules |
| `data/raw/synthetic/` | 7 / 28 KB | tracked | INCLUDE: synthetic source pack |
| `data/processed/` | 3 / 100 KB | tracked | INCLUDE: chunks, index, processing report |
| `docs/` | 41 before this report / 164 KB | tracked | INCLUDE: architecture, setup, limitations, evidence and production plan |
| `evaluation/` | 6 / 24 KB | tracked | INCLUDE: retrieval, localization, demo and false-positive results |
| `evidence/category1/` | 5 / 20 KB | tracked | INCLUDE: scripts and capture-status placeholders |
| `evidence/category5/` | 9 / 1.1 MB | mixed; transcript ignored | INCLUDE: WAV fixtures and documented results |
| `frontend/src/` plus configs | 5 / 36 KB | tracked | INCLUDE: current React/Vite frontend |
| `frontend/package-lock.json` | 1 | tracked | INCLUDE: dependency reproducibility |
| `knowledge_base/` | 11 source files / 100 KB | source tracked | INCLUDE source; exclude bytecode |
| `localization/` | 13 / 52 KB | tracked | INCLUDE: Philippines and Indonesia artifacts |
| `realtime/` | 10 source files / 88 KB | source tracked | INCLUDE replay, ASR, signals and nudges |
| `recordings/` | 4 Markdown / 16 KB | ignored | Optional transcripts only; no recordings present |
| `tests/` | 6 source files / 76 KB | tracked | INCLUDE tests; exclude bytecode |
| `voice_agent/` | 6 source files / 100 KB | tracked | INCLUDE backend; exclude bytecode |
| `web/` | 1 / 8 KB | tracked | INCLUDE: backend `GET /` fallback |

Root files `README.md`, `requirements.txt`, `.env.example`, `.gitignore`,
`frontend/.env.example`, `frontend/package.json`, `frontend/package-lock.json`,
`frontend/vite.config.ts`, and `frontend/index.html` should be included.

## INCLUDE

```text
config/ data/ docs/ evaluation/ evidence/ frontend/src/ knowledge_base/
localization/ realtime/ recordings/ tests/ voice_agent/ web/
README.md requirements.txt .env.example .gitignore
frontend/.env.example frontend/index.html frontend/package.json
frontend/package-lock.json frontend/vite.config.ts
```

All four expected synthetic Q4 fixtures exist and should be included for
reproducibility:

```text
evidence/category5/audio/compliance.wav        247,436 bytes
evidence/category5/audio/missed_opportunity.wav 305,148 bytes
evidence/category5/audio/frustration.wav       357,072 bytes
evidence/category5/audio/noisy_ambiguous.wav   223,444 bytes
```

`evidence/category5/README.md` identifies these as synthetic macOS text-to-
speech PCM recordings with no customer information. Include
`evidence/category5/transcripts/real_asr_results.md` and the existing
`recordings/category4/*_transcript.md` files only as transcript evidence; they
are not call recordings.

## EXCLUDE

```text
.git/ .DS_Store .env (if created) .env.* (except *.env.example)
frontend/node_modules/ frontend/dist/ frontend/.wrangler/
**/__pycache__/ **/*.pyc **/.pytest_cache/ *.log *.mp3 *.m4a
downloaded Faster-Whisper/model caches (none found in this repository)
```

No `.pem`, `.key`, database/SQLite file, private key, customer recording,
confidential document, or actual secret-bearing environment file was found.
The node_modules secret-store filenames are third-party dependency files and
are excluded as generated dependencies, not because a project secret exists.

## USER ACTION REQUIRED

The repository status documents these as missing or unverified and they must
not be claimed as complete: three real Q1 calls with transcripts/results; two
Philippines and two Indonesia real market recordings; Q4 browser live-demo
recording, screenshots/receipt, and real latency evidence; final assessment
video; live Render/Vercel health, CORS, HTTPS, and microphone verification; and
an authorized real Q2 business source pack if required. Current Q2 sources are
explicitly synthetic. No evidence should be fabricated.

## REQUIRED BUT GITIGNORED

| Path | Status | Packaging action |
|---|---|---|
| `evidence/category5/transcripts/real_asr_results.md` | ignored required Q4 ASR evidence | explicitly include |
| `evidence/category5/audio/*.wav` | required synthetic fixtures | explicitly include |
| `recordings/category4/*_transcript.md` | ignored available transcripts only | include optionally; not recordings |
| `frontend/node_modules/`, `frontend/dist/`, `.wrangler/`, `__pycache__/`, `*.pyc` | generated | safe to omit |

## Security check

`.env.example` and `frontend/.env.example` contain variable names, local URLs,
and empty/placeholders only. No API key, token, password, credential, private
machine path (`/Users/`, `/home/`, Desktop, Documents, Downloads), or personal
file was found. `data/raw/synthetic/pii_form.md` is intentionally synthetic
PII-shaped test data and is documented as such; it is not customer information.

## Legacy / unused

`web/index.html` is still used: `docs/deployment_audit.md` and the backend
identify it as the `GET /` fallback. Include it. `frontend/dist/` is generated
and should be excluded. `recordings/` is non-empty but has no audio/video.

## Final ZIP structure

```text
Resonate-AI-Submission/
├── config/  data/raw/synthetic/  data/processed/  docs/  evaluation/
├── evidence/category1/  evidence/category5/
├── frontend/src/  frontend/index.html  frontend/package.json
├── frontend/package-lock.json  frontend/vite.config.ts  frontend/.env.example
├── knowledge_base/  localization/  realtime/  recordings/  tests/ voice_agent/
├── web/index.html
├── README.md  requirements.txt  .env.example  .gitignore
```

## Safe ZIP command (not executed)

Run from the repository parent only after adding any user-captured evidence:

```bash
cd /Users/devashishkumarmoddh
zip -r Resonate-AI-Submission.zip Resonate-AI \
  -x 'Resonate-AI/.git/*' 'Resonate-AI/.DS_Store' \
     'Resonate-AI/.env' 'Resonate-AI/frontend/.env' \
     'Resonate-AI/.env.local' 'Resonate-AI/.env.production' \
     'Resonate-AI/.env.development' 'Resonate-AI/.env.test' \
     'Resonate-AI/frontend/.env.local' 'Resonate-AI/frontend/.env.production' \
     'Resonate-AI/frontend/.env.development' 'Resonate-AI/frontend/.env.test' \
     'Resonate-AI/frontend/node_modules/*' 'Resonate-AI/frontend/dist/*' \
     'Resonate-AI/frontend/.wrangler/*' 'Resonate-AI/**/__pycache__/*' \
     'Resonate-AI/**/*.pyc' 'Resonate-AI/**/*.log' \
     'Resonate-AI/**/*.mp3' 'Resonate-AI/**/*.m4a'
```

Afterward, inspect `unzip -l` to confirm both `.env.example` files are present
and no `.env` is present. Existing WAVs are included by this filesystem ZIP
command regardless of Git ignore status.

## Final answers

1. 2,799 files and 382 directories inspected; 138 files tracked before this report.
2. Definitely exclude generated dependencies/build output, `.git`, caches,
   bytecode, `.DS_Store`, real env files, logs, model weights, and private data.
3. Definitely include source, docs, templates, lockfiles, tests, synthetic data,
   evaluation, evidence, frontend/backend/realtime/localization, `web/`, and all
   four Q4 WAVs.
4. Required-but-ignored paths are listed above; especially the Q4 transcript,
   WAVs, and optional localization transcripts.
5. Secrets/private data found: none; synthetic PII-shaped data only.
6. `web/` is needed. `recordings/` does not satisfy the recording requirement.
7. All four expected Q4 WAV fixtures exist.
8. Nothing must be removed from the repository itself; ZIP exclusion is enough.
