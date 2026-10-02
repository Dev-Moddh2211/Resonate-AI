# Category 5 demo results

These are actual deterministic transcript-replay runs from `ReplayStream`, not fabricated audio recordings. Each sequence had a live event loop: the first chunk was processed, the signal/nudge was emitted, and only then did the replay end. `occurred_before_call_end` therefore demonstrates incremental ordering for the transcript simulation.

| scenario | trigger | nudge | before end | limitation |
|---|---:|---|---|---|
| compliance gap | 1.0s | Do not imply guaranteed approval. | yes | no audio/ASR |
| missed opportunity | 1.0s | Ask about expansion financing. | yes | no audio/ASR |
| rising frustration | 1.0s | Acknowledge concern. | yes | no audio/ASR |
| noisy ambiguity | 1.0s | none | no | synthetic text only |

The required actual audio/live-dashboard demonstration recording does not exist in this checkout and is intentionally not claimed.
