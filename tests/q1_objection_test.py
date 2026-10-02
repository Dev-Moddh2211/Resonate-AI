import unittest

from voice_agent.http_server import calls, process_request
from voice_agent.manager import ConversationManager


def state_at_funding_purpose(call_id="q1"):
    manager = ConversationManager()
    state, _ = manager.start(call_id)
    state.customer_profile["full_name"] = "Alex Kumar"
    state.business_details.update({"business_name": "Acme", "business_type": "retail"})
    state.current_stage = "LOAN_REQUIREMENT"
    state.qualification_data = {"state": "incomplete", "missing": ["loan_purpose", "requested_loan_amount", "contact_number"]}
    return manager, state


class Q1ObjectionTests(unittest.TestCase):
    def test_interest_question_answers_from_kb_and_repeats_same_field(self):
        manager, state = state_at_funding_purpose()
        result = manager.respond(state, "I'm not sure I want a loan. What is the interest rate?")
        self.assertTrue(result["state"]["last_sources"])
        self.assertEqual(result["state"]["loan_requirement"], {})
        self.assertEqual(result["state"]["qualification_data"]["missing"][0], "loan_purpose")
        self.assertIn("funding", result["response"])

    def test_valid_purpose_is_stored_and_advances(self):
        manager, state = state_at_funding_purpose()
        result = manager.respond(state, "I need the loan to buy equipment.")
        self.assertEqual(result["state"]["loan_requirement"]["loan_purpose"], "equipment")
        self.assertEqual(result["state"]["qualification_data"]["missing"][0], "requested_loan_amount")

    def test_generic_objection_preserves_qualification_state(self):
        manager, state = state_at_funding_purpose()
        result = manager.respond(state, "I'm worried about taking on debt right now.")
        self.assertEqual(result["state"]["loan_requirement"], {})
        self.assertEqual(result["state"]["qualification_data"]["missing"][0], "loan_purpose")
        self.assertIn("funding", result["response"])

    def test_unsupported_question_uses_safe_fallback_and_preserves_state(self):
        manager, state = state_at_funding_purpose()
        result = manager.respond(state, "What is the best recipe for mango cake?")
        self.assertIn("funding", result["response"])
        self.assertEqual(result["state"]["loan_requirement"], {})
        self.assertEqual(result["state"]["qualification_data"]["missing"][0], "loan_purpose")

    def test_http_stateful_turn_uses_same_call_state(self):
        manager, state = state_at_funding_purpose("http-q1")
        calls["http-q1"] = state
        response, returned = process_request("/voice/turn", {"CallSid": ["http-q1"], "Speech": ["What is the interest rate?"]})
        self.assertIs(returned, state)
        self.assertIn("funding", response)
        self.assertEqual(calls["http-q1"].qualification_data["missing"][0], "loan_purpose")


if __name__ == "__main__":
    unittest.main()
