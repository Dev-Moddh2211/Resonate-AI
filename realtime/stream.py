from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import time

@dataclass(frozen=True)
class AudioChunk:
    call_id: str
    chunk_id: str
    timestamp_ms: int
    duration_ms: int
    speaker: str
    text: str
    sequence: int
    received_at: str

class ReplayStream:
    """Replay pre-labelled test transcript chunks incrementally, never as a batch."""
    def __init__(self, call_id, chunks, chunk_duration_ms=1000, replay_speed=1.0, deterministic=False):
        self.call_id, self.chunks = call_id, list(chunks)
        self.chunk_duration_ms, self.replay_speed = chunk_duration_ms, replay_speed
        self.deterministic, self.paused = deterministic, False
        self.index = 0
    def pause(self): self.paused = True
    def restart(self): self.paused = False
    def __iter__(self):
        while self.index < len(self.chunks):
            while self.paused: time.sleep(.01)
            item = self.chunks[self.index]; self.index += 1
            if not self.deterministic and self.index > 1:
                time.sleep(self.chunk_duration_ms / 1000 / max(self.replay_speed, .01))
            yield AudioChunk(self.call_id, f"chunk-{self.index:03d}", item.get("timestamp_ms", (self.index-1)*self.chunk_duration_ms), item.get("duration_ms", self.chunk_duration_ms), item["speaker"], item["text"], self.index, datetime.now(timezone.utc).isoformat())
