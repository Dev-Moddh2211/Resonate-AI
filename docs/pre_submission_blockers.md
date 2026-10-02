# Pre-submission blockers

This is a red-team audit. No evidence is inferred from documentation alone.

## A. Critical implementation blockers

- **Q1 runtime grounding is present but not fully demonstrated for every required conversational form.** A live FAQ and product question reached `Retriever.search` and returned source metadata. A low-confidence policy question safely escalated. An objection phrased while the agent was still collecting qualification data was handled as a qualification response rather than a KB objection response. The required objection call must therefore exercise the supported question path and preserve its result.
- **Deployment is configuration-only until live provider checks are performed.** The intended flow is Vercel frontend plus Render backend; local build/configuration checks do not prove deployed health, CORS, HTTPS, or microphone behavior.

## B. Mandatory evidence blockers

- No actual Q1 recordings, transcripts, and observed results.
- No two Philippines recordings and no two Indonesia recordings.
- No native-speaker validation or genuine Indonesian regional-accent validation.
- No recorded browser live-demo walkthrough.
- No browser T5 receipt measurements or valid ASR/signal/nudge/delivery/end-to-end P50/P95 measurements.
- Q4 WAV fixtures exist in the working tree but are ignored by `*.wav` and are not Git-tracked; the final submission must intentionally include or separately deliver the required fixtures.
- No final assessment video.

## C. Deployment verification

Still required: actual Render `/health`, CORS preflight from the Vercel origin, HTTPS browser access, microphone permission, realtime replay, ASR model loading, and frontend-to-backend API calls. Repository configuration alone is not deployment verification.

## D. Optional / non-blocking improvements

- Replace synthetic source material with authorized business documents.
- Add automated browser tests for realtime display.
- Add true production diarization and durable multi-worker event storage.
- Keep public/demo source limitations and deployment configuration explicit; do not treat local checks as live deployment evidence.
