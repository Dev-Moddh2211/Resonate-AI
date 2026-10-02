"""Incremental WAV reader for Category 5.

This module only supplies audio bytes. It deliberately does not turn a
prepared transcript into an ASR result.
"""
from dataclasses import dataclass
from pathlib import Path
import wave

@dataclass(frozen=True)
class RawAudioChunk:
    call_id: str
    chunk_id: str
    timestamp_ms: int
    duration_ms: int
    pcm: bytes
    sample_rate: int
    channels: int
    speaker: str | None = None

    def channel(self, index, speaker):
        """Return one channel as mono PCM, using fixture channel identity."""
        if self.channels == 1:
            return self
        sample_width = 2
        frame_width = sample_width * self.channels
        pcm = b"".join(self.pcm[i + index * sample_width:i + (index + 1) * sample_width]
                       for i in range(0, len(self.pcm), frame_width))
        return RawAudioChunk(self.call_id, f"{self.chunk_id}-{speaker}", self.timestamp_ms,
                             self.duration_ms, pcm, self.sample_rate, 1, speaker)

def wav_chunks(path, call_id, chunk_duration_ms=1000):
    path = Path(path)
    with wave.open(str(path), "rb") as source:
        rate, channels, width = source.getframerate(), source.getnchannels(), source.getsampwidth()
        frames = max(1, int(rate * chunk_duration_ms / 1000))
        sequence = 0
        while True:
            pcm = source.readframes(frames)
            if not pcm: break
            sequence += 1
            duration = round(len(pcm) / (rate * channels * width) * 1000)
            yield RawAudioChunk(call_id, f"audio-{sequence:03d}", round((sequence-1)*chunk_duration_ms), duration, pcm, rate, channels)
