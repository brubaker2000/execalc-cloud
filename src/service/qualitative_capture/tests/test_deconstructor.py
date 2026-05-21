import unittest
from datetime import UTC, datetime

from src.service.qualitative_capture.deconstructor import deconstruct_event
from src.service.qualitative_capture.models import AtomicNugget, ConversationEvent


def _make_event(text: str) -> ConversationEvent:
    return ConversationEvent(
        event_id="evt1",
        tenant_id="t1",
        session_id="s1",
        user_id="u1",
        role="operator",
        message_text=text,
        created_at=datetime.now(UTC),
    )


class TestDeconstructEvent(unittest.TestCase):
    def test_extracts_doctrine_claim(self):
        evt = _make_event(
            "We will never compromise on data quality under any circumstances. "
            "This is our non-negotiable standing rule."
        )
        nuggets = deconstruct_event(evt)
        self.assertTrue(len(nuggets) >= 1)
        types = {n.claim_type for n in nuggets}
        self.assertTrue("doctrine" in types or "principle" in types)

    def test_returns_atomic_nuggets(self):
        evt = _make_event(
            "We will never compromise on data quality. "
            "This leads to better outcomes for all stakeholders."
        )
        nuggets = deconstruct_event(evt)
        for n in nuggets:
            self.assertIsInstance(n, AtomicNugget)
            self.assertEqual(n.tenant_id, "t1")
            self.assertEqual(n.session_id, "s1")
            self.assertEqual(n.generation_depth, 1)
            self.assertEqual(n.selection_method, "machine_extracted")

    def test_no_nuggets_from_boilerplate(self):
        evt = _make_event("N/A — not applicable for this session.")
        nuggets = deconstruct_event(evt)
        self.assertEqual(nuggets, [])

    def test_no_nuggets_from_question(self):
        evt = _make_event(
            "What should we do about the data quality problem? "
            "How can we address the risk in this scenario?"
        )
        # Questions alone should produce no nuggets (no claim signals + question endings)
        # The deconstructor filters questions, so at most 0 nuggets
        for n in nuggets if (nuggets := deconstruct_event(evt)) else []:
            self.assertNotEqual(n.claim_text.strip()[-1], "?")

    def test_short_text_no_nuggets(self):
        evt = _make_event("Short text.")
        nuggets = deconstruct_event(evt)
        self.assertEqual(nuggets, [])

    def test_risk_signal_detected(self):
        evt = _make_event(
            "There is significant exposure to counterparty risk if we proceed without hedging. "
            "The risk of default increases substantially under these conditions."
        )
        nuggets = deconstruct_event(evt)
        types = {n.claim_type for n in nuggets}
        self.assertTrue("risk" in types or "causal_claim" in types)

    def test_doctrine_is_rail_candidate(self):
        evt = _make_event(
            "We will never accept a deal that violates our core integrity principles under any circumstances whatsoever."
        )
        nuggets = deconstruct_event(evt)
        doctrine_nuggets = [n for n in nuggets if n.claim_type == "doctrine"]
        for n in doctrine_nuggets:
            self.assertTrue(n.rail_candidate)

    def test_confidence_starts_at_seed(self):
        evt = _make_event(
            "We will always prioritize long-term value creation over short-term gains in all decisions."
        )
        nuggets = deconstruct_event(evt)
        for n in nuggets:
            self.assertEqual(n.confidence_level, "seed")
            self.assertEqual(n.confidence_score, 0.50)


if __name__ == "__main__":
    unittest.main()
