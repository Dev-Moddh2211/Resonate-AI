from .models import Chunk
from .processing import clean, redact

def make_chunks(doc: dict, source: dict, category: str, tags: list[str] | None = None) -> list[Chunk]:
    result = []
    for i, section in enumerate(doc["sections"], 1):
        text, findings = redact(clean(section["content"]))
        if not text: continue
        record = f"{source['source_id']}-R{i:03d}"
        result.append(Chunk(f"{record}-C001", record, doc["document_id"], doc["title"], text, category, source["source_id"], source["source_name"], section["heading"], f"section:{i}", None, source["version"], source.get("effective_date"), source["authority_level"], bool(findings), list(tags or [])))
    return result
