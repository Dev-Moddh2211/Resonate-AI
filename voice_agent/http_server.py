"""Minimal provider-neutral HTTP interface and Twilio-compatible voice webhook."""
import html, json, os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from pathlib import Path
import threading, uuid
from realtime.audio import wav_chunks
from realtime.asr import FasterWhisperASR
from realtime.pipeline import RealtimePipeline

from .manager import ConversationManager

manager = ConversationManager()
calls = {}
realtime_calls = {}
WEB_PAGE = Path(__file__).resolve().parent.parent / "web" / "index.html"

def allowed_origins():
    configured = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
    return {origin.strip() for origin in configured.split(",") if origin.strip()}

def event_json(event):
    out = {"timestamp_ms": event.get("chunk", event.get("audio", {})).timestamp_ms if hasattr(event.get("chunk", event.get("audio", {})), "timestamp_ms") else event.get("timestamp_ms"),
           "signals": [s.__dict__ for s in event.get("signals", [])], "nudges": event.get("nudges", [])}
    chunk = event.get("chunk")
    if chunk: out["transcript"] = {"speaker": chunk.speaker, "text": chunk.text, "timestamp_ms": chunk.timestamp_ms}
    if event.get("audio"): out["asr"] = {"error": event["audio"].get("asr_error"), "latency_ms": (event["audio"]["asr_completed_ns"]-event["audio"]["asr_started_ns"])/1e6}
    return out


def process_request(path: str, data: dict[str, list[str]]) -> tuple[str, object | None]:
    """Process one form-encoded voice request and return speech/state.

    Keeping this exact dispatch path callable makes state persistence testable
    without depending on an operating-system socket in local test runners.
    """
    call_id = data.get("CallSid", ["local"])[0]
    if path == "/voice/start":
        calls[call_id], text = manager.start(call_id)
        return text, calls[call_id]
    if path != "/voice/turn":
        raise ValueError("not found")
    state = calls.get(call_id)
    if state is None:
        state, _ = manager.start(call_id)
        calls[call_id] = state
    result = manager.respond(state, data.get("Speech", [""])[0])
    # respond mutates state in place; retain that same state object for the
    # next request associated with this CallSid.
    calls[call_id] = state
    return result["response"], state


def api_payload(state, response=""):
    snapshot = state.to_dict()
    return {"response": response, "state": snapshot,
            "escalated": snapshot["escalation_required"],
            "qualification_state": snapshot["qualification_data"].get("state"),
            "sources": snapshot["last_sources"]}


def twiml(text, gather=True):
    suffix = '<Gather input="speech" action="/voice/turn" method="POST" speechTimeout="auto"/>' if gather else ''
    return f'<Response><Say>{html.escape(text)}</Say>{suffix}</Response>'


class Handler(BaseHTTPRequestHandler):
    def _cors_headers(self):
        origin = self.headers.get("Origin")
        if origin in allowed_origins():
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(204); self._cors_headers(); self.end_headers()

    def do_GET(self):
        if self.path == "/health":
            return self._json({"status": "ok"})
        if self.path.startswith("/realtime/events"):
            query = parse_qs(self.path.split("?", 1)[1] if "?" in self.path else "")
            call_id = query.get("call_id", [""])[0]; cursor = int(query.get("cursor", [0])[0])
            item = realtime_calls.get(call_id)
            if not item: self.send_error(404); return
            events, next_cursor = item["pipeline"].poll(cursor)
            self._json({"call_id": call_id, "events": [event_json(e) for e in events], "cursor": next_cursor, "completed": item["completed"]}); return
        if self.path != "/":
            self.send_error(404); return
        body = WEB_PAGE.read_bytes()
        self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

    def do_POST(self):
        raw = self.rfile.read(int(self.headers.get("Content-Length", 0))).decode()
        if self.path.startswith("/api/"):
            data = json.loads(raw or "{}")
            call_id = data.get("call_id")
            if self.path == "/api/conversation/start":
                state, text = manager.start(call_id, data.get("market", "global"))
                calls[state.call_id] = state
                return self._json(api_payload(state, text) | {"call_id": state.call_id})
            if self.path == "/api/conversation/turn":
                state = calls.get(call_id)
                if state is None:
                    self.send_error(400, "Unknown call_id"); return
                result = manager.respond(state, data.get("message", ""))
                calls[call_id] = state
                return self._json(api_payload(state, result["response"]) | {"call_id": call_id})
            if self.path == "/api/conversation/end":
                calls.pop(call_id, None)
                return self._json({"ended": True, "call_id": call_id})
            if self.path == "/api/realtime/start":
                call_id = data.get("call_id") or f"demo-{uuid.uuid4().hex[:8]}"
                wav_path = data.get("audio_path")
                if not wav_path: return self._json({"error": "audio_path is required"})
                item = {"pipeline": RealtimePipeline(), "completed": False}
                realtime_calls[call_id] = item
                def run():
                    asr = FasterWhisperASR(data.get("model"))
                    import time
                    for chunk in wav_chunks(wav_path, call_id, int(data.get("chunk_ms", 1000))):
                        if data.get("replay_speed", 1) == 1: time.sleep(chunk.duration_ms / 1000)
                        item["pipeline"].process_audio_chunk(chunk, asr)
                    item["completed"] = True
                threading.Thread(target=run, daemon=True).start()
                return self._json({"call_id": call_id, "cursor": 0})
            self.send_error(404); return
        data = parse_qs(raw)
        try:
            text, _ = process_request(self.path, data)
        except ValueError:
            self.send_error(404); return
        body = twiml(text).encode()
        self.send_response(200); self.send_header("Content-Type", "application/xml"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

    def _json(self, payload):
        body = json.dumps(payload).encode()
        self.send_response(200); self._cors_headers(); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)


def main():
    host = "0.0.0.0"
    port = int(os.getenv("PORT", "8080"))
    HTTPServer((host, port), Handler).serve_forever()


if __name__ == "__main__":
    main()
