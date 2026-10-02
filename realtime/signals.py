from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
import re, time

@dataclass
class Signal:
    signal_id: str; call_id: str; timestamp_ms: int; confidence: float; evidence: str; priority: str; topic: str; expires_at: str; status: str = "candidate"

RULES = {
 "missed_opportunity": ("medium", .75, ["expanding", "another location", "second business", "inventory too"]),
 "compliance_gap": ("high", .85, ["definitely approved", "guaranteed approval", "guarantee"]),
 "rising_frustration": ("high", .75, ["frustrating", "frustrated", "already explained twice", "fed up"]),
 "payment_difficulty": ("high", .80, ["worried about repayments", "cannot manage", "payment is too high", "cicilan berat"]),
 "callback_needed": ("medium", .80, ["call me", "callback", "call tomorrow", "contact me"]),
}

def detect(event, context):
    text = event.text.casefold()
    if any(marker in text for marker in ("[noise]", "unclear", "maybe not clear")):
        return []
    found = []
    for signal_id, (priority, threshold, phrases) in RULES.items():
        phrase = next((p for p in phrases if p in text), None)
        if not phrase: continue
        if signal_id == "compliance_gap" and event.speaker != "agent": continue
        if signal_id != "compliance_gap" and event.speaker != "customer": continue
        confidence = min(.99, threshold + (.08 if len(text.split()) > 3 else 0))
        topic = "repayment" if signal_id == "payment_difficulty" else "callback" if signal_id == "callback_needed" else "compliance" if signal_id == "compliance_gap" else "opportunity" if signal_id == "missed_opportunity" else "sentiment"
        found.append(Signal(signal_id, event.call_id, event.timestamp_ms, confidence, event.text[:180], priority, topic, (datetime.now(timezone.utc)+timedelta(seconds=20)).isoformat()))
    return found
