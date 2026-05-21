import unittest
from unittest.mock import patch

from src.service.qualitative_capture.session_packet import (
    SessionIntelligencePacket,
    _find_core_breakthrough,
    _infer_session_title,
    generate_session_packet,
)


def _nugget(claim_type: str, confidence: float = 0.50, rail_candidate: bool = False) -> dict:
    return {
        "nugget_id": f"n_{claim_type}_{id(claim_type)}",
        "claim_text": f"This is a {claim_type} claim with important content.",
        "claim_type": claim_type,
        "domain": "strategy",
        "confidence_score": confidence,
        "confidence_level": "seed",
        "polarity": "neutral",
        "rail_candidate": rail_candidate,
        "selection_method": "machine_extracted",
        "created_at": "2026-05-20T00:00:00+00:00",
    }


class TestInferSessionTitle(unittest.TestCase):
    def test_empty_nuggets_returns_fallback(self):
        title = _infer_session_title([], domain=None)
        self.assertIn("Empty session", title)

    def test_single_type_appears_in_title(self):
        nuggets = [_nugget("doctrine")] * 3
        title = _infer_session_title(nuggets, domain="strategy")
        self.assertIn("doctrine", title)
        self.assertIn("strategy", title)

    def test_domain_appears_in_title(self):
        nuggets = [_nugget("risk")]
        title = _infer_session_title(nuggets, domain="capital")
        self.assertIn("capital", title)

    def test_no_domain_omits_brackets(self):
        nuggets = [_nugget("doctrine")]
        title = _infer_session_title(nuggets, domain=None)
        self.assertNotIn("[", title)


class TestFindCoreBreakthrough(unittest.TestCase):
    def test_empty_returns_none(self):
        self.assertIsNone(_find_core_breakthrough([]))

    def test_rail_candidate_preferred(self):
        nuggets = [
            _nugget("observation", confidence=0.91, rail_candidate=False),
            _nugget("doctrine", confidence=0.50, rail_candidate=True),
        ]
        result = _find_core_breakthrough(nuggets)
        self.assertIn("doctrine", result)

    def test_doctrine_preferred_over_other_rail_candidates(self):
        nuggets = [
            _nugget("risk", confidence=0.91, rail_candidate=True),
            _nugget("doctrine", confidence=0.72, rail_candidate=True),
        ]
        result = _find_core_breakthrough(nuggets)
        self.assertIn("doctrine", result)

    def test_returns_claim_text(self):
        nuggets = [_nugget("doctrine", confidence=0.72, rail_candidate=True)]
        result = _find_core_breakthrough(nuggets)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)


class TestGenerateSessionPacket(unittest.TestCase):
    @patch("src.service.qualitative_capture.session_packet.list_conclusions", return_value=[])
    @patch("src.service.qualitative_capture.session_packet.list_promotion_candidates", return_value=[])
    @patch("src.service.qualitative_capture.session_packet.list_preserved_ideas_for_session", return_value=[])
    @patch("src.service.qualitative_capture.session_packet.list_nuggets")
    def test_returns_packet(self, mock_nuggets, mock_ideas, mock_promo, mock_conclusions):
        mock_nuggets.return_value = [
            _nugget("doctrine", confidence=0.72, rail_candidate=True),
            _nugget("risk", confidence=0.50),
        ]
        packet = generate_session_packet(tenant_id="t1", session_id="s1", domain="strategy")
        self.assertIsInstance(packet, SessionIntelligencePacket)
        self.assertEqual(packet.session_id, "s1")
        self.assertEqual(packet.tenant_id, "t1")
        self.assertEqual(packet.nugget_count, 2)
        self.assertFalse(packet.is_empty)

    @patch("src.service.qualitative_capture.session_packet.list_conclusions", return_value=[])
    @patch("src.service.qualitative_capture.session_packet.list_promotion_candidates", return_value=[])
    @patch("src.service.qualitative_capture.session_packet.list_preserved_ideas_for_session", return_value=[])
    @patch("src.service.qualitative_capture.session_packet.list_nuggets", return_value=[])
    def test_empty_session_is_empty(self, mock_nuggets, mock_ideas, mock_promo, mock_conclusions):
        packet = generate_session_packet(tenant_id="t1", session_id="s1")
        self.assertTrue(packet.is_empty)
        self.assertEqual(packet.nugget_count, 0)
        self.assertIsNone(packet.core_breakthrough)

    @patch("src.service.qualitative_capture.session_packet.list_conclusions", return_value=[])
    @patch("src.service.qualitative_capture.session_packet.list_promotion_candidates", return_value=[])
    @patch("src.service.qualitative_capture.session_packet.list_preserved_ideas_for_session", return_value=[])
    @patch("src.service.qualitative_capture.session_packet.list_nuggets")
    def test_doctrine_candidates_populated(self, mock_nuggets, *_):
        mock_nuggets.return_value = [
            _nugget("doctrine", confidence=0.72),
            _nugget("principle", confidence=0.50),
            _nugget("risk", confidence=0.50),
        ]
        packet = generate_session_packet(tenant_id="t1", session_id="s1")
        self.assertEqual(len(packet.doctrine_candidates), 2)

    @patch("src.service.qualitative_capture.session_packet.list_conclusions", return_value=[])
    @patch("src.service.qualitative_capture.session_packet.list_promotion_candidates", return_value=[])
    @patch("src.service.qualitative_capture.session_packet.list_preserved_ideas_for_session", return_value=[])
    @patch("src.service.qualitative_capture.session_packet.list_nuggets")
    def test_to_dict_is_serializable(self, mock_nuggets, *_):
        mock_nuggets.return_value = [_nugget("doctrine", confidence=0.72)]
        packet = generate_session_packet(tenant_id="t1", session_id="s1")
        d = packet.to_dict()
        self.assertIn("session_title", d)
        self.assertIn("core_breakthrough", d)
        self.assertIn("claim_type_breakdown", d)
        self.assertIn("doctrine_candidates", d)
        self.assertIn("decisions_made", d)
        self.assertIn("open_questions", d)

    @patch("src.service.qualitative_capture.session_packet.list_conclusions", return_value=[])
    @patch("src.service.qualitative_capture.session_packet.list_promotion_candidates", return_value=[])
    @patch("src.service.qualitative_capture.session_packet.list_preserved_ideas_for_session", return_value=[])
    @patch("src.service.qualitative_capture.session_packet.list_nuggets", side_effect=Exception("db down"))
    def test_db_failure_returns_empty_packet(self, *_):
        packet = generate_session_packet(tenant_id="t1", session_id="s1")
        self.assertTrue(packet.is_empty)


if __name__ == "__main__":
    unittest.main()
