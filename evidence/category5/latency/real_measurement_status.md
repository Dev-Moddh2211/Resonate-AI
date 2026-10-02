# Real latency measurement status

The model and WAV replay executed, but no valid stage percentile set was produced. The actual adapter path emitted zero signals and zero nudges because every ASR event carried speaker `unknown`; the existing latency list only records timings while processing an emitted signal/nudge. Accordingly ASR P50/P95, signal P50/P95, nudge P50/P95, delivery P50/P95, and end-to-end audio-to-dashboard P50/P95 are **not available**, rather than zero.

The four replays processed 13 real 1-second-or-shorter chunks in total. This is execution evidence, not a latency percentile claim.
