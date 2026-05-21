import unittest
from unittest.mock import call, patch

from src.service.qualitative_capture.decay import apply_decay_pass

_MOD = "src.service.qualitative_capture.decay"


def _ephemeral_nugget(nugget_id="n1", confidence_score=0.50):
    return {
        "nugget_id": nugget_id,
        "tenant_id": "t1",
        "confidence_score": confidence_score,
        "confidence_level": "seed",
    }


def _medium_term_nugget(nugget_id="n2", confidence_score=0.72):
    return {
        "nugget_id": nugget_id,
        "tenant_id": "t1",
        "confidence_score": confidence_score,
        "confidence_level": "developing",
        "created_at": "2023-01-01T00:00:00+00:00",
    }


def _date_sensitive_nugget(nugget_id="n3", confidence_score=0.50):
    return {
        "nugget_id": nugget_id,
        "tenant_id": "t1",
        "confidence_score": confidence_score,
        "confidence_level": "seed",
        "created_at": "2025-01-01T00:00:00+00:00",
    }


class TestApplyDecayPass(unittest.TestCase):
    @patch(f"{_MOD}.insert_audit_event", return_value=True)
    @patch(f"{_MOD}.update_nugget_confidence", return_value=True)
    @patch(f"{_MOD}.list_stale_date_sensitive_nuggets", return_value=[])
    @patch(f"{_MOD}.list_stale_medium_term_nuggets", return_value=[])
    @patch(f"{_MOD}.list_expired_ephemeral_nuggets", return_value=[])
    def test_returns_summary_dict(self, *_):
        result = apply_decay_pass(tenant_id="t1")
        self.assertIn("expired", result)
        self.assertIn("flagged_medium_term", result)
        self.assertIn("flagged_date_sensitive", result)
        self.assertIn("failed", result)

    @patch(f"{_MOD}.insert_audit_event", return_value=True)
    @patch(f"{_MOD}.update_nugget_confidence", return_value=True)
    @patch(f"{_MOD}.list_stale_date_sensitive_nuggets", return_value=[])
    @patch(f"{_MOD}.list_stale_medium_term_nuggets", return_value=[])
    @patch(f"{_MOD}.list_expired_ephemeral_nuggets")
    def test_expires_ephemeral_nuggets(self, mock_list, *_):
        mock_list.return_value = [_ephemeral_nugget()]
        result = apply_decay_pass(tenant_id="t1")
        self.assertEqual(result["expired"], 1)

    @patch(f"{_MOD}.insert_audit_event", return_value=True)
    @patch(f"{_MOD}.update_nugget_confidence", return_value=True)
    @patch(f"{_MOD}.list_stale_date_sensitive_nuggets", return_value=[])
    @patch(f"{_MOD}.list_stale_medium_term_nuggets", return_value=[])
    @patch(f"{_MOD}.list_expired_ephemeral_nuggets")
    def test_expired_nugget_set_to_zero_confidence(self, mock_list, mock_mt, mock_ds, mock_update, mock_audit):
        mock_list.return_value = [_ephemeral_nugget(nugget_id="n1")]
        apply_decay_pass(tenant_id="t1")
        _, kwargs = mock_update.call_args
        self.assertEqual(kwargs["new_score"], 0.0)
        self.assertEqual(kwargs["nugget_id"], "n1")

    @patch(f"{_MOD}.insert_audit_event", return_value=True)
    @patch(f"{_MOD}.update_nugget_confidence", return_value=True)
    @patch(f"{_MOD}.list_stale_date_sensitive_nuggets", return_value=[])
    @patch(f"{_MOD}.list_stale_medium_term_nuggets", return_value=[])
    @patch(f"{_MOD}.list_expired_ephemeral_nuggets")
    def test_expired_nugget_emits_audit_event(self, mock_list, mock_mt, mock_ds, mock_update, mock_audit):
        mock_list.return_value = [_ephemeral_nugget()]
        apply_decay_pass(tenant_id="t1")
        kinds = [c.kwargs["event_kind"] for c in mock_audit.call_args_list]
        self.assertIn("nugget.expired", kinds)

    @patch(f"{_MOD}.insert_audit_event", return_value=True)
    @patch(f"{_MOD}.update_nugget_confidence", return_value=True)
    @patch(f"{_MOD}.list_stale_date_sensitive_nuggets", return_value=[])
    @patch(f"{_MOD}.list_stale_medium_term_nuggets", return_value=[])
    @patch(f"{_MOD}.list_expired_ephemeral_nuggets")
    def test_canon_nugget_is_exempt_from_expiry(self, mock_list, mock_mt, mock_ds, mock_update, mock_audit):
        mock_list.return_value = [_ephemeral_nugget(confidence_score=1.0)]
        apply_decay_pass(tenant_id="t1")
        mock_update.assert_not_called()

    @patch(f"{_MOD}.insert_audit_event", return_value=True)
    @patch(f"{_MOD}.update_nugget_confidence", return_value=True)
    @patch(f"{_MOD}.list_stale_date_sensitive_nuggets", return_value=[])
    @patch(f"{_MOD}.list_stale_medium_term_nuggets")
    @patch(f"{_MOD}.list_expired_ephemeral_nuggets", return_value=[])
    def test_flags_stale_medium_term(self, mock_exp, mock_mt, mock_ds, mock_update, mock_audit):
        mock_mt.return_value = [_medium_term_nugget()]
        result = apply_decay_pass(tenant_id="t1")
        self.assertEqual(result["flagged_medium_term"], 1)
        kinds = [c.kwargs["event_kind"] for c in mock_audit.call_args_list]
        self.assertIn("nugget.decay_review_requested", kinds)

    @patch(f"{_MOD}.insert_audit_event", return_value=True)
    @patch(f"{_MOD}.update_nugget_confidence", return_value=True)
    @patch(f"{_MOD}.list_stale_date_sensitive_nuggets", return_value=[])
    @patch(f"{_MOD}.list_stale_medium_term_nuggets")
    @patch(f"{_MOD}.list_expired_ephemeral_nuggets", return_value=[])
    def test_medium_term_does_not_change_score(self, mock_exp, mock_mt, mock_ds, mock_update, mock_audit):
        mock_mt.return_value = [_medium_term_nugget()]
        apply_decay_pass(tenant_id="t1")
        mock_update.assert_not_called()

    @patch(f"{_MOD}.insert_audit_event", return_value=True)
    @patch(f"{_MOD}.update_nugget_confidence", return_value=True)
    @patch(f"{_MOD}.list_stale_date_sensitive_nuggets")
    @patch(f"{_MOD}.list_stale_medium_term_nuggets", return_value=[])
    @patch(f"{_MOD}.list_expired_ephemeral_nuggets", return_value=[])
    def test_flags_stale_date_sensitive(self, mock_exp, mock_mt, mock_ds, mock_update, mock_audit):
        mock_ds.return_value = [_date_sensitive_nugget()]
        result = apply_decay_pass(tenant_id="t1")
        self.assertEqual(result["flagged_date_sensitive"], 1)
        kinds = [c.kwargs["event_kind"] for c in mock_audit.call_args_list]
        self.assertIn("nugget.staleness_flagged", kinds)

    @patch(f"{_MOD}.insert_audit_event", return_value=True)
    @patch(f"{_MOD}.update_nugget_confidence", return_value=True)
    @patch(f"{_MOD}.list_stale_date_sensitive_nuggets", return_value=[])
    @patch(f"{_MOD}.list_stale_medium_term_nuggets", return_value=[])
    @patch(f"{_MOD}.list_expired_ephemeral_nuggets",
           side_effect=Exception("db down"))
    def test_db_failure_on_list_does_not_crash(self, *_):
        result = apply_decay_pass(tenant_id="t1")
        self.assertIsInstance(result, dict)

    @patch(f"{_MOD}.insert_audit_event", return_value=True)
    @patch(f"{_MOD}.update_nugget_confidence", side_effect=Exception("db lock"))
    @patch(f"{_MOD}.list_stale_date_sensitive_nuggets", return_value=[])
    @patch(f"{_MOD}.list_stale_medium_term_nuggets", return_value=[])
    @patch(f"{_MOD}.list_expired_ephemeral_nuggets")
    def test_update_failure_increments_failed(self, mock_list, *_):
        mock_list.return_value = [_ephemeral_nugget()]
        result = apply_decay_pass(tenant_id="t1")
        self.assertEqual(result["failed"], 1)
        self.assertEqual(result["expired"], 0)

    @patch(f"{_MOD}.insert_audit_event", return_value=True)
    @patch(f"{_MOD}.update_nugget_confidence", return_value=True)
    @patch(f"{_MOD}.list_stale_date_sensitive_nuggets", return_value=[])
    @patch(f"{_MOD}.list_stale_medium_term_nuggets", return_value=[])
    @patch(f"{_MOD}.list_expired_ephemeral_nuggets", return_value=[])
    def test_batch_size_forwarded(self, mock_list, *_):
        apply_decay_pass(tenant_id="t1", batch_size=25)
        mock_list.assert_called_once_with(tenant_id="t1", limit=25)


if __name__ == "__main__":
    unittest.main()
