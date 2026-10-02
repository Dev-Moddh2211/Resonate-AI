import re
import uuid
from typing import Any

from knowledge_base.retrieval import Retriever

from .rules import evaluate, extract_values
from .state import ConversationState
from .localization import detect_language, load_market, localized_text


HUMAN = re.compile(r"\b(human|person|specialist|agent|representative|petugas|orang|manusia|call me back|bicara dengan)\b", re.I)
UNAUTHORIZED = re.compile(r"\b(approve|approval|guarantee|guaranteed|underwrite|legal advice|financial advice)\b", re.I)
OBJECTION = re.compile(
    r"\b(?:not sure|hesitat(?:e|ion)|concern(?:ed)?|worried|afford|too expensive|"
    r"don't want|do not want|rather not|uncomfortable|why should i|is this safe|"
    r"interest|rate|eligible|eligibility|qualif(?:y|ied|ication)|policy|"
    r"speak to (?:a )?(?:human|person|specialist)|need help)\b", re.I
)


class ConversationManager:
    def __init__(self, retriever: Retriever | None = None):
        self.retriever = retriever or Retriever.load()

    def start(self, call_id: str | None = None, market: str = "global") -> tuple[ConversationState, str]:
        state = ConversationState(call_id or str(uuid.uuid4()))
        state.market = market if market in {"philippines", "indonesia"} else "global"
        if state.market != "global":
            state.language, state.detected_register, state.voice_profile, state.localization_mode = load_market(state.market)
            return state, localized_text(state.market, "greeting", state.detected_register)
        return state, ("Hello, I’m the business-loan qualification assistant. "
                       "I can collect details for a preliminary review, but I can’t approve a loan. "
                       "Would you like to continue?")

    def respond(self, state: ConversationState, message: str) -> dict[str, Any]:
        state.last_user_message = message
        state.history.append({"role": "user", "content": message})
        if state.market != "global":
            state.language, state.detected_register = detect_language(state.market, message, state.detected_register)
        if HUMAN.search(message):
            return self._escalate(state, "human_requested", localized_text(state.market, "escalation", state.detected_register))
        if UNAUTHORIZED.search(message) and any(x in message.casefold() for x in ("approve", "guarantee", "underwrite")):
            return self._escalate(state, "unauthorized_decision", localized_text(state.market, "unauthorized", state.detected_register))

        missing_before = evaluate(state).get("missing", [])
        values = extract_values(message, missing_before[0] if missing_before else None)
        # Questions and objections raised while collecting a field must not be
        # interpreted as an answer to that field. Route them through the same
        # grounded KB path, then repeat the still-missing qualification prompt.
        if (missing_before and state.current_stage != "GREETING" and not values
                and (self._looks_like_question(message) or OBJECTION.search(message))):
            return self._knowledge_answer(state, message, resume_field=missing_before[0])

        self._merge(state, values)
        if values:
            state.qualification_data = evaluate(state)

        # A useful data-bearing utterance is handled as an answer even when
        # it contains words such as "need" or "what". Knowledge intent is
        # considered only after structured extraction has found no fields.
        if self._looks_like_question(message) and not values:
            return self._knowledge_answer(state, message)
        state.qualification_data = evaluate(state)
        missing = state.qualification_data.get("missing", [])
        if missing:
            field = missing[0]
            prompts = {"full_name": "What is your full name?", "business_name": "What is your business name?", "business_type": "What type of business do you run?", "loan_purpose": "What would you mainly use the funding for?", "requested_loan_amount": "Roughly how much are you looking to borrow?", "contact_number": "What is the best contact number for a callback?"}
            state.current_stage = "BASIC_CUSTOMER_DETAILS" if field in ("full_name", "contact_number") else "BUSINESS_DETAILS" if field in ("business_name", "business_type") else "LOAN_REQUIREMENT"
            prompt = prompts.get(field, f"Could you provide your {field.replace('_', ' ')}?")
            return self._result(state, localized_text(state.market, "clarify", state.detected_register, prompt))
        state.current_stage = "QUALIFICATION"
        return self._result(state, localized_text(state.market, "closing", state.detected_register))

    def _merge(self, state, values):
        for key, value in values.items():
            target = state.customer_profile if key == "full_name" else state.loan_requirement if key in ("loan_purpose", "requested_loan_amount") else state.business_details
            old = target.get(key)
            if old is not None and old != value:
                state.conflicts.append({"field": key, "original": old, "new": value})
            elif old is None:
                target[key] = value

    def _looks_like_question(self, message):
        return "?" in message or any(w in message.casefold() for w in ("what", "how", "can i", "do i", "documents", "repay", "process", "interest", "rate", "need"))

    def _knowledge_answer(self, state, message, resume_field=None):
        # Retrieval scores alone can be inflated by generic words such as
        # "policy". Require a business-domain signal before speaking.
        domain_terms = ("loan", "borrow", "fund", "business", "document", "repay", "payment", "qualification", "eligible", "application", "rate", "interest", "approval")
        if not any(term in message.casefold() for term in domain_terms) and (not OBJECTION.search(message) or resume_field is None):
            if resume_field is None:
                return self._escalate(state, "unsupported_question", localized_text(state.market, "fallback", state.detected_register))
            return self._resume_qualification(state, localized_text(state.market, "fallback", state.detected_register), resume_field)
        result = self.retriever.search(message, top_k=3)
        state.retrieved_context = result.get("results", [])
        state.last_sources = [{k: r.get(k) for k in ("source", "source_id", "chunk_id", "confidence", "version", "page")} for r in state.retrieved_context]
        state.retrieval_confidence = state.retrieved_context[0]["confidence"] if state.retrieved_context else None
        if result["status"] == "no_trusted_result" or state.retrieval_confidence == "low":
            if resume_field is None:
                return self._escalate(state, "unsupported_question", localized_text(state.market, "fallback", state.detected_register))
            return self._resume_qualification(state, localized_text(state.market, "fallback", state.detected_register), resume_field)
        answer = state.retrieved_context[0]["content"].split("\n")[0].strip()
        return self._resume_qualification(state, answer, resume_field)

    def _resume_qualification(self, state, response, field=None):
        """Answer a side question without consuming or changing its field."""
        state.qualification_data = evaluate(state)
        field = field or state.qualification_data.get("missing", [None])[0]
        prompts = {"full_name": "What is your full name?", "business_name": "What is your business name?", "business_type": "What type of business do you run?", "loan_purpose": "What would you mainly use the funding for?", "requested_loan_amount": "Roughly how much are you looking to borrow?", "contact_number": "What is the best contact number for a callback?"}
        state.current_stage = "BASIC_CUSTOMER_DETAILS" if field in ("full_name", "contact_number") else "BUSINESS_DETAILS" if field in ("business_name", "business_type") else "LOAN_REQUIREMENT"
        if field:
            response = f"{response}\n\n{prompts.get(field, f'Could you provide your {field.replace("_", " ")}')}"
        return self._result(state, response)

    def _escalate(self, state, reason, text):
        state.escalation_required, state.escalation_reason, state.current_stage = True, reason, "ESCALATED"
        return self._result(state, text)

    def _result(self, state, response):
        state.history.append({"role": "assistant", "content": response})
        return {"response": response, "state": state.to_dict()}
