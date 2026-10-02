# Real-time polling dashboard boundary

`GET /realtime/events?call_id=<id>&cursor=<n>` is the intended browser contract. It returns only events produced since the cursor, including incremental transcript chunks, signals, and nudges. The registry is in-process and not durable or multi-worker safe.
