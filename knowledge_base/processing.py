"""Deterministic cleaning, quality checks, PII and duplicate helpers."""
import hashlib, re

BOILERPLATE = re.compile(r"^(home|menu|navigation|cookie settings|subscribe|privacy policy|terms of use|contact us)$", re.I)
PII = [("email", re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")), ("phone", re.compile(r"(?<!\d)(?:\+?\d[\d ()-]{8,}\d)(?!\d)")), ("name", re.compile(r"\b(?:name|customer)\s*:\s*[A-Z][\w -]+", re.I))]

def clean(text: str) -> str:
    lines, seen = [], set()
    for raw in text.splitlines():
        line = re.sub(r"\s+", " ", raw).strip()
        if not line or BOILERPLATE.match(line): continue
        key = line.casefold()
        if key not in seen: lines.append(line); seen.add(key)
    return "\n".join(lines)

def pii_findings(text: str) -> list[dict]:
    return [{"type": kind, "match": m.group(0)} for kind, rx in PII for m in rx.finditer(text)]

def redact(text: str) -> tuple[str, list[dict]]:
    findings = pii_findings(text)
    out = text
    for f in findings: out = out.replace(f["match"], f"[{f['type'].upper()} REDACTED]")
    return out, findings

def fingerprint(text: str) -> str:
    return hashlib.sha256(re.sub(r"\W+", " ", text.casefold()).strip().encode()).hexdigest()

def similarity(a: str, b: str) -> float:
    sa, sb = set(re.findall(r"\w+", a.casefold())), set(re.findall(r"\w+", b.casefold()))
    return len(sa & sb) / max(1, len(sa | sb))

def near_duplicate(a: str, b: str, threshold: float = .55) -> bool:
    """Flag candidate duplicates; callers retain both until reviewed."""
    return similarity(a, b) >= threshold
