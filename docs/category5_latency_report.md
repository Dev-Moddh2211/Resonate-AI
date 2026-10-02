# Category 5 latency report

No audio replay latency report is claimed. The repository has no real audio fixture and no connected streaming ASR provider, so ASR P50/P95, audio duration, and true end-to-end audio latency are **not available**.

The deterministic transcript-replay test was run with Python 3, `replay_speed=1.0` in deterministic mode for repeatable unit tests. Its measured stages are transcript ingestion, signal detection, nudge generation, and an unimplemented delivery boundary. They are implementation timings, not production or ASR benchmarks. Use `python3 -m unittest discover -s tests -p '*category*_test.py'` to reproduce.
