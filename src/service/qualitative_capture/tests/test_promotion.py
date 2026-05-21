import unittest
from unittest.mock import MagicMock, call, patch

from src.service.qualitative_capture.models import AtomicNugget, PromotionCandidate
from src.service.qualitative_capture.promotion import (
    _build_canon_nugget,
    approve_candidate,
    nominate_for_promotion,
    reject_candidate,
)

_MOD = "src.service.qualitative_capture.promotion"

_CANDIDATE = {
    "candidate_id": "cand1",
    "tenant_id": "t1",
    "source_artifact_id": "art1",
    "source_conclusion_id": None,
    "candidate_text": "We will never compromise on data quality.",
    "proposed_claim_type": "doctrine",
    "nominated_by": "operator",
    "nominated_by_user_id": "u1",
    "nominated_at": "2026-05-20T00:00:00+00:00",
    "nomination_rationale": None,
    "review_status": "pending",
    "reviewed_by": None,
    "reviewed_at": None,
    "rejection_reason": None,
    "canon_nugget_id": None,
}


class TestNominateForPromotion(unittest.TestCase):
    @patch(f"{_MOD}.insert_promotion_candidate")
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

    @patch(f"{_MOD}.insert_promotion_candidate")
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


class TestBuildCanonNugget(unittest.TestCase):
    def _build(self, domain=None):
        return _build_canon_nugget(_CANDIDATE, domain=domain, approved_by="u1")

    def test_returns_atomic_nugget(self):
        nugget = self._build()
        self.assertIsInstance(nugget, AtomicNugget)

    def test_confidence_is_structural(self):
        nugget = self._build()
        self.assertEqual(nugget.confidence_score, 1.00)
        self.assertEqual(nugget.confidence_level, "structural")

    def test_selection_method_is_canon_approved(self):
        nugget = self._build()
        self.assertEqual(nugget.selection_method, "canon_approved")

    def test_claim_text_matches_candidate_text(self):
        nugget = self._build()
        self.assertEqual(nugget.claim_text, _CANDIDATE["candidate_text"])

    def test_claim_type_matches_proposed(self):
        nugget = self._build()
        self.assertEqual(nugget.claim_type, "doctrine")

    def test_domain_defaults_to_strategy(self):
        nugget = self._build(domain=None)
        self.assertEqual(nugget.domain, "strategy")

    def test_domain_override_applied(self):
        nugget = self._build(domain="capital")
        self.assertEqual(nugget.domain, "capital")

    def test_durability_and_freshness_enduring(self):
        nugget = self._build()
        self.assertEqual(nugget.durability_class, "enduring")
        self.assertEqual(nugget.freshness_class, "timeless")

    def test_rail_candidate_true(self):
        nugget = self._build()
        self.assertTrue(nugget.rail_candidate)

    def test_provenance_author_is_approver(self):
        nugget = self._build()
        self.assertEqual(nugget.provenance_author, "u1")


class TestApproveCandidate(unittest.TestCase):
    @patch(f"{_MOD}._admit_to_pem")
    @patch(f"{_MOD}.update_candidate_review", return_value=True)
    @patch(f"{_MOD}.insert_nugget", return_value=True)
    @patch(f"{_MOD}.get_promotion_candidate", return_value=_CANDIDATE)
    def test_approve_returns_true(self, mock_get, mock_insert, mock_update, mock_pem):
        result = approve_candidate(candidate_id="cand1", tenant_id="t1", reviewed_by="u1")
        self.assertTrue(result)

    @patch(f"{_MOD}.get_promotion_candidate", return_value=None)
    def test_approve_not_found_returns_false(self, mock_get):
        result = approve_candidate(candidate_id="missing", tenant_id="t1", reviewed_by="u1")
        self.assertFalse(result)

    @patch(f"{_MOD}._admit_to_pem")
    @patch(f"{_MOD}.update_candidate_review", return_value=True)
    @patch(f"{_MOD}.insert_nugget", return_value=True)
    @patch(f"{_MOD}.get_promotion_candidate", return_value=_CANDIDATE)
    def test_creates_canon_nugget(self, mock_get, mock_insert, mock_update, mock_pem):
        approve_candidate(candidate_id="cand1", tenant_id="t1", reviewed_by="u1")
        mock_insert.assert_called_once()
        nugget = mock_insert.call_args[0][0]
        self.assertIsInstance(nugget, AtomicNugget)
        self.assertEqual(nugget.confidence_score, 1.00)
        self.assertEqual(nugget.selection_method, "canon_approved")

    @patch(f"{_MOD}._admit_to_pem")
    @patch(f"{_MOD}.update_candidate_review", return_value=True)
    @patch(f"{_MOD}.insert_nugget", return_value=True)
    @patch(f"{_MOD}.get_promotion_candidate", return_value=_CANDIDATE)
    def test_canon_nugget_id_passed_to_update(self, mock_get, mock_insert, mock_update, mock_pem):
        approve_candidate(candidate_id="cand1", tenant_id="t1", reviewed_by="u1")
        _, kwargs = mock_update.call_args
        self.assertIsNotNone(kwargs.get("canon_nugget_id"))
        self.assertEqual(kwargs["review_status"], "approved")

    @patch(f"{_MOD}._admit_to_pem")
    @patch(f"{_MOD}.update_candidate_review", return_value=True)
    @patch(f"{_MOD}.insert_nugget", return_value=True)
    @patch(f"{_MOD}.get_promotion_candidate", return_value=_CANDIDATE)
    def test_pem_admission_called(self, mock_get, mock_insert, mock_update, mock_pem):
        approve_candidate(candidate_id="cand1", tenant_id="t1", reviewed_by="u1")
        mock_pem.assert_called_once()

    @patch(f"{_MOD}._admit_to_pem")
    @patch(f"{_MOD}.update_candidate_review", return_value=True)
    @patch(f"{_MOD}.insert_nugget", side_effect=Exception("db down"))
    @patch(f"{_MOD}.get_promotion_candidate", return_value=_CANDIDATE)
    def test_insert_failure_does_not_block_approval(self, mock_get, mock_insert, mock_update, mock_pem):
        result = approve_candidate(candidate_id="cand1", tenant_id="t1", reviewed_by="u1")
        self.assertTrue(result)

    @patch(f"{_MOD}._admit_to_pem")
    @patch(f"{_MOD}.update_candidate_review", return_value=True)
    @patch(f"{_MOD}.insert_nugget", return_value=True)
    @patch(f"{_MOD}.get_promotion_candidate", return_value=_CANDIDATE)
    def test_domain_passed_to_nugget(self, mock_get, mock_insert, mock_update, mock_pem):
        approve_candidate(candidate_id="cand1", tenant_id="t1", reviewed_by="u1", domain="capital")
        nugget = mock_insert.call_args[0][0]
        self.assertEqual(nugget.domain, "capital")


class TestRejectCandidate(unittest.TestCase):
    @patch(f"{_MOD}.update_candidate_review", return_value=True)
    def test_reject_returns_true(self, mock_update):
        result = reject_candidate(
            candidate_id="cand1", tenant_id="t1",
            reviewed_by="u1", rejection_reason="Not strong enough.",
        )
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
