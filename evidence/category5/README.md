# Category 5 executable evidence

The WAV files in `audio/` are synthetic macOS text-to-speech recordings and contain no customer information. They are real PCM WAV files, not transcript fixtures.

Install the optional engine and run `python -m voice_agent.http_server`, then open `http://localhost:8080` and choose **Start WAV replay**:

```bash
python -m pip install faster-whisper
```

The server releases chunks at 1.0x, calls `FasterWhisperASR`, appends only returned ASR text, detects signals, and exposes them through `GET /realtime/events?call_id=...&cursor=...`.

The selected demo model is `base.en`, loaded on CPU with `int8`. The frustration model comparison is recorded in `transcripts/real_asr_results.md`; the same fixture, channel mapping, replay/chunking, detector, and thresholds produced the frustration signal in all three base.en runs and in none of the three fresh tiny.en runs. Failures are explicit and never substitute scenario text. Fixture channel labels are used for this evidence; there is no general-purpose diarization.
