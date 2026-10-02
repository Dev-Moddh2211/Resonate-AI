from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class ConversationState:
    call_id: str
    current_stage: str = "GREETING"
    customer_profile: dict[str, Any] = field(default_factory=dict)
    business_details: dict[str, Any] = field(default_factory=dict)
    loan_requirement: dict[str, Any] = field(default_factory=dict)
    qualification_data: dict[str, Any] = field(default_factory=dict)
    last_user_intent: str | None = None
    last_user_message: str | None = None
    retrieved_context: list[dict[str, Any]] = field(default_factory=list)
    retrieval_confidence: str | None = None
    last_sources: list[dict[str, Any]] = field(default_factory=list)
    escalation_required: bool = False
    escalation_reason: str | None = None
    lead_action_status: str = "not_created"
    history: list[dict[str, str]] = field(default_factory=list)
    conflicts: list[dict[str, Any]] = field(default_factory=list)
    clarification_attempts: int = 0
    market: str = "global"
    language: str = "English"
    detected_register: str = "neutral"
    voice_profile: str = "en-US-neutral"
    localization_mode: str = "default"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
