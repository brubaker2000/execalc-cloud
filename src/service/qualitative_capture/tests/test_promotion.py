import unittest
from unittest.mock import patch

from src.service.qualitative_capture.models import PromotionCandidate
from src.service.qualitative_capture.promotion import (
    approve_candidate,
    nominate_for_promotion,
    reject_candidate,
)


class TestNominateForPromotion(unittest.TestCase):
    @patch("src.service.qualitative_capture.promotion.insert_promotion_candidate")
    def test_operator_nomination(self, mock_insert):
        mock_insert.return_value = True
        candidate = nominate_for_promotion(
            tenant_id="t1",
            candidate_text="We will never compromise on data quality.",
            proposed_claim_type="doctrine",
            nominated_by="operator",
            source_artifact_id="a1",
            nominated_by_user_id="u1",
            nomination_rationale="Repeated across 3 sessions.",
        )
        self.assertIsInstance(candidate, PromotionCandidate)
        self.assertEqual(candidate.review_status, "pending")
        self.assertEqual(candidate.nominated_by, "operator")
        mock_insert.assert_called_once()

    @patch("src.service.qualitative_capture.promotion.insert_promotion_candidate")
    def test_system_auto_nomination(self, mock_insert):
        mock_insert.return_value = True
        candidate = nominate_for_promotion(
            tenant_id="t1",
            candidate_text="AI produces value faster than humans can absorb.",
            proposed_claim_type="doctrine",
            nominated_by="system_auto",
            source_conclusion_id="c1",
        )
        self.assertEqual(candidate.nominated_by, "system_auto")

    def test_invalid_nominator_raises(self):
        with self.assertRaises(ValueError):
            nominate_for_promotion(
                tenant_id="t1",
                candidate_text="Some text.",
                proposed_claim_type="doctrine",
                nominated_by="random_person",
                source_artifact_id="a1",
            )

    def test_no_source_raises(self):
        with self.assertRaises(ValueError):
            nominate_for_promotion(
                tenant_id="t1",
                candidate_text="Some text.",
                proposed_claim_type="doctrine",
                nominated_by="operator",
            )


class TestApproveCandidate(unittest.TestCase):
    @patch("src.service.qualitative_capture.promotion.update_candidate_review", return_value=True)
    def test_approve_returns_true(self, mock_update):
        result = approve_candidate(candidate_id="cand1", tenant_id="t1", reviewed_by="u1")
        self.assertTrue(result)
        mock_update.assert_called_once()

    @patch("src.service.qualitative_capture.promotion.update_candidate_review", return_value=False)
    def test_approve_not_found_returns_false(self, mock_update):
        result = approve_candidate(candidate_id="missing", tenant_id="t1", reviewed_by="u1")
        self.assertFalse(result)


class TestRejectCandidate(unittest.TestCase):
    @patch("src.service.qualitative_capture.promotion.update_candidate_review", return_value=True)
    def test_reject_returns_true(self, mock_update):
        result = reject_candidate(
            candidate_id="cand1", tenant_id="t1",
            reviewed_by="u1", rejection_reason="Not strong enough.",
        )
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
