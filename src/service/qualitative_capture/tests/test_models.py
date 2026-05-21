import unittest
from datetime import UTC, datetime

from src.service.qualitative_capture.models import (
    AtomicNugget,
    ConversationEvent,
    ExecutiveConclusion,
    PreservedIdea,
    PromotionCandidate,
    RailArtifact,
    RightRailCard,
)


class TestConversationEvent(unittest.TestCase):
    def _make(self, **kw):
        defaults = dict(
            event_id="evt1",
            tenant_id="t1",
            session_id="s1",
            user_id="u1",
            role="operator",
            message_text="We will never compromise on data quality.",
            created_at=datetime.now(UTC),
        )
        defaults.update(kw)
        return ConversationEvent(**defaults)

    def test_to_dict_has_required_fields(self):
        e = self._make()
        d = e.to_dict()
        self.assertEqual(d["event_id"], "evt1")
        self.assertEqual(d["role"], "operator")
        self.assertIsNone(d["token_count"])

    def test_is_frozen(self):
        e = self._make()
        with self.assertRaises(Exception):
            e.role = "system"  # type: ignore


class TestAtomicNugget(unittest.TestCase):
    def _make(self, **kw):
        defaults = dict(
            nugget_id="n1",
            tenant_id="t1",
            session_id="s1",
            source_event_id="evt1",
            claim_text="We will never compromise on data quality.",
            claim_type="doctrine",
            domain="strategy",
            confidence_level="seed",
            confidence_score=0.50,
            provenance_source="session:s1",
            activation_scope="tenant_specific",
            polarity="neutral",
            durability_class="enduring",
            evidence_status="argued",
            freshness_class="timeless",
            selection_method="machine_extracted",
            generation_depth=1,
            created_at=datetime.now(UTC),
        )
        defaults.update(kw)
        return AtomicNugget(**defaults)

    def test_to_dict_shape(self):
        n = self._make()
        d = n.to_dict()
        self.assertEqual(d["nugget_id"], "n1")
        self.assertEqual(d["claim_type"], "doctrine")
        self.assertEqual(d["generation_depth"], 1)
        self.assertIsNone(d["expires_at"])

    def test_defaults(self):
        n = self._make()
        self.assertEqual(n.activation_triggers, [])
        self.assertFalse(n.rail_candidate)


class TestPreservedIdea(unittest.TestCase):
    def test_to_dict_shape(self):
        idea = PreservedIdea(
            idea_id="i1",
            tenant_id="t1",
            nugget_id="n1",
            session_id="s1",
            source_event_id="evt1",
            selected_text="Fire hose problem.",
            memorialized_by="u1",
            memorialized_at=datetime.now(UTC),
        )
        d = idea.to_dict()
        self.assertEqual(d["idea_id"], "i1")
        self.assertEqual(d["corroboration_count"], 1)
        self.assertIsNone(d["structural_threshold_crossed_at"])


class TestExecutiveConclusion(unittest.TestCase):
    def test_to_dict_shape(self):
        c = ExecutiveConclusion(
            conclusion_id="c1",
            tenant_id="t1",
            session_id="s1",
            conclusion_text="We have identified 3 doctrine signals.",
            source_nugget_ids=["n1", "n2"],
            claim_types_present=["doctrine"],
            reconstruction_confidence=0.50,
            domain="strategy",
            polarity="neutral",
            rail_card_type="executive_conclusion",
            generated_at=datetime.now(UTC),
        )
        d = c.to_dict()
        self.assertEqual(d["conclusion_id"], "c1")
        self.assertEqual(len(d["source_nugget_ids"]), 2)
        self.assertIsNone(d["promoted_to_artifact_id"])


class TestRightRailCard(unittest.TestCase):
    def test_to_dict_shape(self):
        card = RightRailCard(
            card_id="card1",
            tenant_id="t1",
            session_id="s1",
            card_type="executive_conclusion",
            card_text="Key conclusion.",
            is_memorialized=False,
            is_pinned=False,
            is_dismissed=False,
            display_rank=0,
            created_at=datetime.now(UTC),
        )
        d = card.to_dict()
        self.assertFalse(d["is_dismissed"])
        self.assertIsNone(d["artifact_id"])


class TestRailArtifact(unittest.TestCase):
    def test_to_dict_shape(self):
        a = RailArtifact(
            artifact_id="a1",
            tenant_id="t1",
            session_id="s1",
            source_card_id="card1",
            artifact_text="Key conclusion.",
            card_type="executive_conclusion",
            is_memorialized=False,
            operator_action="preserved",
            actioned_at=datetime.now(UTC),
            second_order_deconstruction_status="pending",
        )
        d = a.to_dict()
        self.assertEqual(d["second_order_deconstruction_status"], "pending")
        self.assertEqual(d["second_order_nugget_ids"], [])


class TestPromotionCandidate(unittest.TestCase):
    def test_to_dict_shape(self):
        c = PromotionCandidate(
            candidate_id="cand1",
            tenant_id="t1",
            candidate_text="We will never compromise on data quality.",
            proposed_claim_type="doctrine",
            nominated_by="operator",
            nominated_at=datetime.now(UTC),
            review_status="pending",
        )
        d = c.to_dict()
        self.assertEqual(d["review_status"], "pending")
        self.assertIsNone(d["canon_nugget_id"])


if __name__ == "__main__":
    unittest.main()
