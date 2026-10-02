# Category 5 streaming audit

The executable path now has an incremental WAV reader (`realtime.audio.wav_chunks`), a local `FasterWhisperASR` adapter, and synthetic PCM WAV fixtures under `evidence/category5/audio/`. `POST /api/realtime/start` starts a background 1.0x replay; `GET /realtime/events?call_id=...&cursor=...` is the polling boundary used by the browser dashboard.

Only text returned by the ASR adapter enters detection. If faster-whisper is absent, the event contains an explicit ASR error and no transcript is fabricated. The executable evidence uses the selected `base.en` model on CPU with `int8`; model-comparison transcripts and signal outcomes are recorded in `evidence/category5/transcripts/real_asr_results.md`. This documents ASR and signal execution for the fixture; it does not by itself establish browser delivery or production latency percentiles.

Speaker labels for ASR output are `unknown`; this stack has no true diarization. Pre-labelled `ReplayStream` remains available for deterministic unit tests only and must not be used as ASR evidence.
