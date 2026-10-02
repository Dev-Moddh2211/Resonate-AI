from dataclasses import asdict, dataclass, field
from typing import Any

@dataclass
class Source:
    source_id: str
    source_name: str
    source_type: str
    document_type: str
    source_uri: str
    version: str
    effective_date: str | None
    authority_level: str
    language: str = "en"
    contains_pii: bool = False
    status: str = "active"

@dataclass
class Chunk:
    chunk_id: str
    record_id: str
    document_id: str
    title: str
    content: str
    category: str
    source_id: str
    source: str
    section: str
    source_location: str
    page: int | None
    version: str
    effective_date: str | None
    authority_level: str
    pii: bool
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
