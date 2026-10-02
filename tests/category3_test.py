import unittest
from voice_agent.manager import ConversationManager
from voice_agent.rules import extract_values


class Category3Tests(unittest.TestCase):
    def setUp(self):
        self.m = ConversationManager(); self.s, _ = self.m.start("test")

    def test_grounded_answer_has_retrieval_sources(self):
        result = self.m.respond(self.s, "What documents are needed?")
        self.assertTrue(result["state"]["last_sources"])

    def test_unknown_escalates(self):
        result = self.m.respond(self.s, "What is the policy for quantum gardening on Mars?")
        self.assertTrue(result["state"]["escalation_required"])

    def test_human_request_is_immediate(self):
        result = self.m.respond(self.s, "I want to speak to a human")
        self.assertEqual(result["state"]["escalation_reason"], "human_requested")

    def test_extraction_is_not_qualification(self):
        result = self.m.respond(self.s, "I need around twenty five lakh for equipment")
        self.assertEqual(result["state"]["loan_requirement"]["loan_purpose"], "equipment")
        self.assertNotEqual(result["state"]["qualification_data"]["state"], "preliminary_qualified")

    def test_conflict_is_preserved(self):
        self.m.respond(self.s, "We have been in business for 5 years")
        result = self.m.respond(self.s, "Actually we have been running for 2 years")
        self.assertTrue(result["state"]["conflicts"])
        self.assertEqual(result["state"]["qualification_data"]["state"], "human_review")

    def test_indian_amount_formats(self):
        cases = {"15 lakh": 1500000, "15.5 lakhs": 1550000, "1 crore": 10000000,
                 "2,500,000": 2500000, "2500000": 2500000, "₹15 lakh": 1500000,
                 "15 lacs": 1500000, "15 lac": 1500000}
        for phrase, expected in cases.items():
            with self.subTest(phrase=phrase):
                self.assertEqual(extract_values(f"I need a loan of {phrase}")["requested_loan_amount"], expected)

    def test_multi_turn_state_persists(self):
        self.m.respond(self.s, "My name is Rahul Sharma")
        self.m.respond(self.s, "I run a small retail business")
        self.m.respond(self.s, "We have been operating for four years")
        self.assertEqual(self.s.customer_profile["full_name"], "Rahul Sharma")
        self.assertEqual(self.s.business_details["business_type"], "retail")
        self.assertEqual(self.s.business_details["years_in_business"], 4)

    def test_call_ids_are_isolated(self):
        from voice_agent.http_server import calls
        calls.clear()
        first, _ = self.m.start("local")
        calls["local"] = first
        self.m.respond(first, "My name is Rahul Sharma")
        self.assertEqual(calls["local"].customer_profile["full_name"], "Rahul Sharma")
        other, _ = self.m.start("new-call")
        self.assertNotIn("full_name", other.customer_profile)

    def test_out_of_order_and_multi_field_extraction(self):
        result = self.m.respond(self.s, "I run a retail business and have been operating for four years.")
        self.assertEqual(result["state"]["business_details"]["business_type"], "retail")
        self.assertEqual(result["state"]["business_details"]["years_in_business"], 4)

        result = self.m.respond(self.s, "I need around 15 lakh for equipment.")
        self.assertEqual(result["state"]["loan_requirement"]["requested_loan_amount"], 1500000)
        self.assertEqual(result["state"]["loan_requirement"]["loan_purpose"], "equipment")

    def test_name_and_business_name_extraction(self):
        result = self.m.respond(self.s, "My name is Rahul Sharma and my company is ABC Retail.")
        self.assertEqual(result["state"]["customer_profile"]["full_name"], "Rahul Sharma")
        self.assertEqual(result["state"]["business_details"]["business_name"], "ABC Retail")

    def test_four_turn_state_contains_all_data(self):
        for message in ("My name is Rahul Sharma", "I run a retail business",
                        "We have been operating for four years", "I need 15 lakh for equipment"):
            self.m.respond(self.s, message)
        self.assertEqual(self.s.customer_profile["full_name"], "Rahul Sharma")
        self.assertEqual(self.s.business_details["business_type"], "retail")
        self.assertEqual(self.s.business_details["years_in_business"], 4)
        self.assertEqual(self.s.loan_requirement["requested_loan_amount"], 1500000)
        self.assertEqual(self.s.loan_requirement["loan_purpose"], "equipment")

    def test_http_multi_turn_same_callsid_and_isolation(self):
        from voice_agent.http_server import calls, process_request
        calls.clear()
        process_request("/voice/start", {"CallSid": ["A"]})
        for message in ("My name is Rahul Sharma", "I run a retail business",
                        "I have been running it for four years", "I need around 15 lakh for new equipment"):
            process_request("/voice/turn", {"CallSid": ["A"], "Speech": [message]})
        self.assertEqual(calls["A"].customer_profile["full_name"], "Rahul Sharma")
        self.assertEqual(calls["A"].business_details["business_type"], "retail")
        self.assertEqual(calls["A"].business_details["years_in_business"], 4)
        self.assertEqual(calls["A"].loan_requirement["requested_loan_amount"], 1500000)
        process_request("/voice/turn", {"CallSid": ["B"], "Speech": ["I run a retail business"]})
        self.assertNotIn("full_name", calls["B"].customer_profile)
        self.assertEqual(calls["A"].customer_profile["full_name"], "Rahul Sharma")

    def test_browser_api_contract_uses_same_call_id(self):
        from voice_agent.http_server import calls, api_payload
        calls.clear()
        state, greeting = self.m.start("browser-test")
        calls[state.call_id] = state
        result = self.m.respond(state, "My name is Rahul Sharma")
        payload = api_payload(state, result["response"])
        self.assertEqual(payload["call_id"] if "call_id" in payload else state.call_id, "browser-test")
        self.assertEqual(payload["state"]["customer_profile"]["full_name"], "Rahul Sharma")

    def test_stage_aware_standalone_answers(self):
        from voice_agent.rules import extract_values
        cases = [("full_name", "Rahul Kumar", "Rahul Kumar"), ("business_name", "ABC Retail", "ABC Retail"),
                 ("business_type", "Retail", "retail"), ("years_in_business", "Four years", 4.0),
                 ("requested_loan_amount", "15 lakh", 1500000), ("loan_purpose", "Equipment", "equipment")]
        for field, text, expected in cases:
            self.assertEqual(extract_values(text, field)[field], expected)

    def test_http_browser_style_funding_purpose_advances_stage(self):
        from voice_agent.http_server import calls, process_request
        calls.clear()
        process_request("/voice/start", {"CallSid": ["q1-browser"]})
        _, state = process_request("/voice/turn", {"CallSid": ["q1-browser"], "Speech": ["Madhura stationery"]})
        self.assertEqual(state.business_details["business_name"], "Madhura stationery")
        _, state = process_request("/voice/turn", {"CallSid": ["q1-browser"], "Speech": ["Stationery shop"]})
        self.assertEqual(state.business_details["business_type"], "stationery shop")
        response, state = process_request("/voice/turn", {"CallSid": ["q1-browser"], "Speech": ["To grow my business"]})
        self.assertEqual(state.loan_requirement["loan_purpose"], "expansion")
        self.assertNotIn("funding for", response)

    def test_http_browser_style_natural_and_alternate_purposes(self):
        from voice_agent.http_server import calls, process_request
        for answer, expected in (("To grow my business for more sales and more profit", "expansion"),
                                 ("I will use it for inventory", "inventory"),
                                 ("I need money to expand my shop", "expansion"),
                                 ("working capital", "working_capital")):
            calls.clear()
            process_request("/voice/start", {"CallSid": ["purpose-test"]})
            _, state = process_request("/voice/turn", {"CallSid": ["purpose-test"], "Speech": [answer]})
            self.assertEqual(state.loan_requirement["loan_purpose"], expected)

    def test_http_repeated_answer_and_conflicting_correction(self):
        from voice_agent.http_server import calls, process_request
        calls.clear()
        process_request("/voice/start", {"CallSid": ["repeat-test"]})
        process_request("/voice/turn", {"CallSid": ["repeat-test"], "Speech": ["equipment"]})
        process_request("/voice/turn", {"CallSid": ["repeat-test"], "Speech": ["equipment"]})
        _, state = process_request("/voice/turn", {"CallSid": ["repeat-test"], "Speech": ["inventory"]})
        self.assertEqual(state.loan_requirement["loan_purpose"], "equipment")
        self.assertEqual(len(state.conflicts), 1)
        self.assertEqual(state.qualification_data["state"], "human_review")
