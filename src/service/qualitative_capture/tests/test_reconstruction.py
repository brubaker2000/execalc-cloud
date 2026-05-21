import unittest
from datetime import UTC, datetime

from src.service.qualitative_capture.models import AtomicNugget, ExecutiveConclusion
from src.service.qualitative_capture.reconstruction import reconstruct_from_nuggets


def _make_nugget(claim_type: str, rail_candidate: bool = True, score: float = 0.50, **kw) -> AtomicNugget:
    defaults = dict(
        nugget_id=f"n_{claim_type}_{id(claim_type)}",
        tenant_id="t1",
        session_id="s1",
        source_event_id="evt1",
        claim_text=f"This is a {claim_type} claim with enough text to be eligible.",
        claim_type=claim_type,
        domain="strategy",
        confidence_level="seed",
        confidence_score=score,
        provenance_source="session:s1",
        activation_scope="tenant_specific",
        polarity="neutral",
        durability_class="enduring",
        evidence_status="argued",
        freshness_class="timeless",
        selection_method="machine_extracted",
        generation_depth=1,
        rail_candidate=rail_candidate,
        created_at=datetime.now(UTC),
    )
    defaults.update(kw)
    return AtomicNugget(**defaults)


class TestReconstructFromNuggets(unittest.TestCase):
    def test_cluster_threshold_not_met_returns_empty(self):
        nuggets = [_make_nugget("doctrine")]
        result = reconstruct_from_nuggets(nuggets, tenant_id="t1", session_id="s1")
        self.assertEqual(result, [])

    def test_cluster_meets_threshold_produces_conclusion(self):
        nuggets = [
            _make_nugget("doctrine", nugget_id="n1"),
            _make_nugget("doctrine", nugget_id="n2"),
        ]
        result = reconstruct_from_nuggets(nuggets, tenant_id="t1", session_id="s1")
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], ExecutiveConclusion)
        self.assertEqual(result[0].rail_card_type, "executive_conclusion")

    def test_risk_cluster_maps_to_risk_card(self):
        nuggets = [
            _make_nugget("risk", nugget_id="r1"),
            _make_nugget("risk", nugget_id="r2"),
        ]
        result = reconstruct_from_nuggets(nuggets, tenant_id="t1", session_id="s1")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].rail_card_type, "risk")

    def test_non_rail_candidate_cluster_skipped(self):
        nuggets = [
            _make_nugget("observation", rail_candidate=False, nugget_id="o1"),
            _make_nugget("observation", rail_candidate=False, nugget_id="o2"),
        ]
        result = reconstruct_from_nuggets(nuggets, tenant_id="t1", session_id="s1")
        self.assertEqual(result, [])

    def test_multiple_claim_types_produce_multiple_conclusions(self):
        nuggets = [
            _make_nugget("doctrine", nugget_id="d1"),
            _make_nugget("doctrine", nugget_id="d2"),
            _make_nugget("risk", nugget_id="r1"),
            _make_nugget("risk", nugget_id="r2"),
        ]
        result = reconstruct_from_nuggets(nuggets, tenant_id="t1", session_id="s1")
        self.assertEqual(len(result), 2)

    def test_empty_nugget_list_returns_empty(self):
        result = reconstruct_from_nuggets([], tenant_id="t1", session_id="s1")
        self.assertEqual(result, [])

    def test_conclusion_carries_correct_metadata(self):
        nuggets = [
            _make_nugget("doctrine", nugget_id="d1", score=0.72),
            _make_nugget("doctrine", nugget_id="d2", score=0.50),
        ]
        result = reconstruct_from_nuggets(nuggets, tenant_id="t1", session_id="s1")
        c = result[0]
        self.assertEqual(c.tenant_id, "t1")
        self.assertEqual(c.session_id, "s1")
        self.assertEqual(c.domain, "strategy")
        self.assertAlmostEqual(c.reconstruction_confidence, 0.61, places=1)
        self.assertIn("d1", c.source_nugget_ids)


if __name__ == "__main__":
    unittest.main()
