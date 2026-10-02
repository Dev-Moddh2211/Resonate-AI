"""In-process polling registry for a live replay session."""
from threading import Lock
from .pipeline import RealtimePipeline

class RealtimeRegistry:
    def __init__(self): self._items={}; self._lock=Lock()
    def create(self, call_id):
        with self._lock: self._items[call_id]=RealtimePipeline(); return self._items[call_id]
    def poll(self, call_id, cursor=0):
        pipeline=self._items.get(call_id)
        if pipeline is None: return {"call_id":call_id,"cursor":cursor,"events":[],"error":"unknown_call"}
        events,next_cursor=pipeline.poll(cursor)
        return {"call_id":call_id,"cursor":next_cursor,"events":[self._json(e) for e in events]}
    @staticmethod
    def _json(event):
        result=dict(event); chunk=result.get("chunk")
        if chunk: result["chunk"]={"chunk_id":chunk.chunk_id,"timestamp_ms":chunk.timestamp_ms,"speaker":chunk.speaker,"text":chunk.text}
        result["signals"]=[getattr(s,"__dict__",s) for s in result.get("signals",[])]
        return result
