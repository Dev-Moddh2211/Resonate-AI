"""Format-aware extraction into a small intermediate document model."""
from pathlib import Path
import csv, json, re

def extract(path: str) -> dict:
    p = Path(path)
    suffix = p.suffix.lower()
    text = p.read_text(encoding="utf-8")
    if suffix in {".json"}:
        value = json.loads(text)
        blocks = [{"heading": x.get("question", x.get("title", "record")), "content": x.get("answer", json.dumps(x))} for x in value] if isinstance(value, list) else [{"heading": "data", "content": json.dumps(value)}]
    elif suffix == ".csv":
        rows = list(csv.DictReader(text.splitlines()))
        blocks = [{"heading": f"row {i+1}", "content": "; ".join(f"{k}: {v}" for k,v in row.items() if v)} for i,row in enumerate(rows)]
    else:
        if suffix in {".md", ".html", ".htm"}:
            text = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", " ", text, flags=re.I)
            text = re.sub(r"<[^>]+>", " ", text)
        blocks, heading, buf = [], "", []
        for line in text.splitlines():
            if re.match(r"^\s{0,3}#{1,6}\s+", line):
                if buf: blocks.append({"heading": heading or p.stem, "content": "\n".join(buf)})
                heading, buf = re.sub(r"^\s*#+\s*", "", line).strip(), []
            elif line.strip(): buf.append(line.strip())
        if buf: blocks.append({"heading": heading or p.stem, "content": "\n".join(buf)})
    return {"document_id": p.stem, "title": p.stem.replace("_", " ").title(), "sections": blocks, "path": str(p)}
