from dataclasses import dataclass, asdict
import time

MESSAGES = {"missed_opportunity":"Ask whether they also need financing for the expansion.", "compliance_gap":"Do not imply guaranteed approval.", "rising_frustration":"Acknowledge the concern before continuing.", "payment_difficulty":"Ask about the repayment concern.", "callback_needed":"Confirm the requested callback time."}

class NudgeEngine:
    def __init__(self, cooldowns=None):
        self.cooldowns = cooldowns or {"missed_opportunity":30,"compliance_gap":10,"rising_frustration":30,"payment_difficulty":30,"callback_needed":30}
        self.last_shown = {}; self.active = {}; self.history = []
    def consider(self, signal, now_ms=None):
        now_ms = now_ms if now_ms is not None else int(time.time()*1000)
        thresholds = {"compliance_gap": .85, "rising_frustration": .75, "payment_difficulty": .80, "missed_opportunity": .75, "callback_needed": .80}
        if signal.confidence < thresholds.get(signal.signal_id, .75): return None
        previous = self.last_shown.get(signal.signal_id)
        if previous is not None and now_ms - previous < self.cooldowns.get(signal.signal_id, 30)*1000: return None
        nudge = {"nudge_id":f"{signal.call_id}:{signal.signal_id}:{now_ms}","call_id":signal.call_id,"signal_id":signal.signal_id,"category":signal.topic,"priority":signal.priority.upper(),"confidence":signal.confidence,"evidence":signal.evidence,"text":MESSAGES[signal.signal_id],"timestamp_ms":signal.timestamp_ms,"status":"active","expires_at":signal.expires_at}
        self.last_shown[signal.signal_id] = now_ms; self.active[signal.signal_id] = nudge; self.history.append(nudge); return nudge
    def expire(self, now_iso):
        for key, nudge in list(self.active.items()):
            if nudge["expires_at"] <= now_iso:
                nudge["status"] = "expired"; self.active.pop(key, None)
