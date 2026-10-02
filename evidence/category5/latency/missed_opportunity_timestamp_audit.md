# Missed-opportunity timestamp audit

This is an audit of the real stereo WAV replay using FasterWhisper `tiny.en`, CPU `int8`, 1000 ms chunks, and approximately 1.0x replay.

## Missed opportunity

- Source: `evidence/category5/audio/missed_opportunity.wav`
- Total duration: 4767 ms
- First trigger chunk: `audio-001`
- Chunk interval: 0–1000 ms; `timestamp_ms=0`, `duration_ms=1000`
- Speaker source: right/customer stereo channel
- Actual ASR output: `We are expanding.`
- Signal: `missed_opportunity`, evidence `We are expanding.`, timestamp `0 ms`
- Nudge: `Ask whether they also need financing for the expansion.`, timestamp `0 ms`

Conclusion: **0 ms is correct.** The first customer chunk legitimately contains the complete `expanding` trigger. The later chunks contain additional, imperfect ASR fragments (`to another loop.`, `and need`, `inventory final.`, `and sing.`), but they are not needed to trigger the existing rule. No timestamp was changed to improve presentation.

## Cross-checks

- Compliance: `audio-003`, interval 2000–3000 ms; actual agent ASR output `guaranteed.`; signal and nudge timestamp `2000 ms`.
- Frustration: `audio-004`, interval 3000–4000 ms; actual customer ASR output `is frustrating.`; signal and nudge timestamp `3000 ms`.

In each case, signal detection runs immediately after the ASR event for that chunk, and the signal/nudge timestamp is the actual replay chunk start timestamp. The implementation does not use wall-clock time for these event timestamps.
