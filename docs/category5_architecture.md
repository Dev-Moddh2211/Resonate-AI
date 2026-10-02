# Category 5 architecture

`ReplayStream` yields one timestamped, pre-labelled transcript/audio chunk at a time and can sleep at configured real-time speed. `RealtimePipeline` records an incremental transcript event, extracts signals from the current bounded event (not the complete call), applies `NudgeEngine` thresholds/cooldowns/deduplication, and exposes event/nudge history for a polling dashboard integration.

The replay path is the reliable available mode. Browser Web Speech and external provider streaming are not claimed as live ASR integrations here. Speaker separation uses simulation metadata. Delivery is represented as a polling-compatible event list; WebSocket delivery can be added at the HTTP boundary without changing signal contracts.

Latency values are measured with a monotonic clock per processed chunk. P50/P95 are reported by `realtime.metrics`; small replay samples are not production benchmarks. At 10x traffic, in-memory state, synchronous extraction, one process, and no durable queue become bottlenecks. Noisy audio can cause ASR text uncertainty; mitigation is exact evidence, speaker filtering, higher thresholds, confirmation, and suppression rather than speculative nudges.
