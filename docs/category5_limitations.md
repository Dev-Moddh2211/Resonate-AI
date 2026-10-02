# Category 5 limitations

- The verified path is a pre-labelled transcript replay, not continuous ASR.
- WAV chunking and optional ASR integration exist, but no real demo audio fixture or ASR model/provider is installed.
- Speaker labels come from test metadata.
- Polling is exposed by `RealtimePipeline.poll`; a React dashboard consumer is not connected.
- Delivery timing is zero because delivery is not implemented; latency output must not be presented as an end-to-end production measurement.
- In-memory state is not suitable for multi-process or 10x production scaling.
