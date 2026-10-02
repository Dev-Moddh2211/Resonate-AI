import time
from .signals import detect
from .nudges import NudgeEngine

class RealtimePipeline:
    def __init__(self, nudge_engine=None): self.nudges = nudge_engine or NudgeEngine(); self.events=[]; self.latencies=[]; self.transcript=[]
    def process(self, chunk):
        t1 = time.perf_counter_ns(); self.transcript.append({"speaker":chunk.speaker,"text":chunk.text,"timestamp_ms":chunk.timestamp_ms})
        t2 = time.perf_counter_ns(); signals = detect(chunk, self.transcript); t3 = time.perf_counter_ns(); emitted=[]
        for signal in signals:
            t4=time.perf_counter_ns(); nudge=self.nudges.consider(signal, chunk.timestamp_ms); t5=time.perf_counter_ns()
            if nudge: emitted.append(nudge)
            self.latencies.append({"call_id":chunk.call_id,"chunk_id":chunk.chunk_id,"audio_timestamp_ms":chunk.timestamp_ms,"asr_ms":(t2-t1)/1e6,"signal_ms":(t3-t2)/1e6,"nudge_ms":(t5-t4)/1e6,"delivery_ms":0.0,"end_to_end_ms":(t5-t1)/1e6})
        result={"chunk":chunk,"signals":signals,"nudges":emitted}; self.events.append(result); return result
    def poll(self, after_index=0):
        """Polling boundary: returns only events produced since the cursor."""
        return self.events[after_index:], len(self.events)
    def process_audio_chunk(self, chunk, asr):
        """Run actual chunk bytes through ASR before detection when available."""
        # Synthetic demo fixtures encode speaker identity in channels. This is
        # fixture metadata, not general-purpose ASR diarization.
        speaker_chunks = ([chunk.channel(0, "agent"), chunk.channel(1, "customer")]
                          if chunk.channels == 2 else [chunk])
        results = [(part, asr.transcribe(part)) for part in speaker_chunks]
        if len(results) > 1:
            outputs = []
            for part, result in results:
                outputs.append(self._process_asr_result(part, result))
            return outputs
        return self._process_asr_result(chunk, results[0][1])

    def _process_asr_result(self, chunk, result):
        event = {"call_id": chunk.call_id, "chunk_id": chunk.chunk_id, "timestamp_ms": chunk.timestamp_ms,
                 "asr_error": result.error, "asr_started_ns": result.started_ns, "asr_completed_ns": result.completed_ns}
        if not result.text:
            self.events.append({"audio": event, "transcript": None, "signals": [], "nudges": []})
            return self.events[-1]
        from .stream import AudioChunk
        speaker = chunk.speaker or "unknown"
        transcript = AudioChunk(chunk.call_id, chunk.chunk_id, chunk.timestamp_ms, chunk.duration_ms, speaker, result.text, 0, "")
        output = self.process(transcript); output["audio"] = event; return output
