"""Replaceable local ASR adapters. No synthetic transcript fallback is used."""
from dataclasses import dataclass
import os, shutil, subprocess, tempfile, time, wave

@dataclass
class ASRResult:
    text: str | None
    error: str | None
    started_ns: int
    completed_ns: int
    confidence: float | None = None
    segments: list | None = None

def _wav(path, chunk):
    with wave.open(path, "wb") as out:
        out.setnchannels(chunk.channels); out.setsampwidth(2); out.setframerate(chunk.sample_rate); out.writeframes(chunk.pcm)

class ChunkASR:
    def __init__(self, executable=None): self.executable = executable or os.getenv("REALTIME_ASR_COMMAND")
    def transcribe(self, chunk):
        started = time.perf_counter_ns()
        if not self.executable or not shutil.which(self.executable): return ASRResult(None, "No configured ASR executable/model; audio chunk was not transcribed.", started, time.perf_counter_ns())
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav") as f:
                _wav(f.name, chunk); result = subprocess.run([self.executable, f.name], text=True, capture_output=True, timeout=30, check=False)
            if result.returncode: return ASRResult(None, result.stderr.strip() or "ASR process failed", started, time.perf_counter_ns())
            return ASRResult(result.stdout.strip() or None, None, started, time.perf_counter_ns())
        except Exception as exc: return ASRResult(None, str(exc), started, time.perf_counter_ns())

class FasterWhisperASR:
    """Local faster-whisper adapter; model loading is lazy and cached."""
    def __init__(self, model_size=None, device=None, compute_type=None):
        self.model_size = model_size or os.getenv("ASR_MODEL", "base.en")
        self.device = device or os.getenv("ASR_DEVICE", "cpu")
        self.compute_type = compute_type or os.getenv("ASR_COMPUTE_TYPE", "int8")
        self.model = None
    def transcribe(self, chunk):
        started = time.perf_counter_ns()
        try:
            from faster_whisper import WhisperModel
            if self.model is None: self.model = WhisperModel(self.model_size, device=self.device, compute_type=self.compute_type)
            with tempfile.NamedTemporaryFile(suffix=".wav") as f:
                _wav(f.name, chunk); segments, _ = self.model.transcribe(f.name, beam_size=1, vad_filter=False); rows = list(segments)
            text = " ".join(s.text.strip() for s in rows).strip(); conf = (sum(getattr(s, "avg_logprob", 0.0) for s in rows) / len(rows)) if rows else None
            return ASRResult(text or None, None, started, time.perf_counter_ns(), conf, [{"start": s.start, "end": s.end, "text": s.text.strip()} for s in rows])
        except ImportError: return ASRResult(None, "faster-whisper is not installed; install it and download the model first.", started, time.perf_counter_ns())
        except Exception as exc: return ASRResult(None, f"Local ASR failed: {exc}", started, time.perf_counter_ns())
