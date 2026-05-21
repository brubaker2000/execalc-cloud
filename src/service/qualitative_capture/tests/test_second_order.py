import unittest
from unittest.mock import call, patch

from src.service.qualitative_capture.second_order import (
    _deconstruct_one_artifact,
    process_pending_artifacts,
)


def _artifact(
    artifact_id: str = "a1",
    tenant_id: str = "t1",
    session_id: str = "s1",
    is_memorialized: bool = False,
    artifact_text: str = (
        "We will not compromise on data quality. "
        "There is a risk that poor pipelines erode trust in our numbers."
    ),
) -> dict:
    return {
        "artifact_id": artifact_id,
        "tenant_id": tenant_id,
        "session_id": session_id,
        "source_card_id": "card1",
        "artifact_text": artifact_text,
        "card_type": "risk",
        "is_memorialized": is_memorialized,
        "operator_action": "preserved",
        "actioned_by": "user1",
        "actioned_at": "2026-05-20T00:00:00+00:00",
        "second_order_deconstruction_status": "pending",
        "second_order_nugget_ids": [],
        "deconstructed_at": None,
    }


_REPO = "src.service.qualitative_capture.second_order"


class TestDeconstructOneArtifact(unittest.TestCase):
    def test_returns_list_of_nuggets(self):
        nuggets = _deconstruct_one_artifact(_artifact())
        self.assertIsInstance(nuggets, list)

    def test_nuggets_are_generation_depth_2(self):
        nuggets = _deconstruct_one_artifact(_artifact())
        for n in nuggets:
            self.assertEqual(n.generation_depth, 2)

    def test_nuggets_have_second_order_selection_method(self):
        nuggets = _deconstruct_one_artifact(_artifact())
        for n in nuggets:
            self.assertEqual(n.selection_method, "second_order")

    def test_nuggets_reference_source_artifact(self):
        nuggets = _deconstruct_one_artifact(_artifact(artifact_id="artX"))
        for n in nuggets:
            self.assertEqual(n.source_rail_artifact_id, "artX")

    def test_machine_artifact_gets_developing_confidence(self):
        nuggets = _deconstruct_one_artifact(_artifact(is_memorialized=False))
        for n in nuggets:
            self.assertAlmostEqual(n.confidence_score, 0.72)
            self.assertEqual(n.confidence_level, "developing")

    def test_memorialized_artifact_gets_strong_confidence(self):
        nuggets = _deconstruct_one_artifact(_artifact(is_memorialized=True))
        for n in nuggets:
            self.assertAlmostEqual(n.confidence_score, 0.91)
            self.assertEqual(n.confidence_level, "strong")

    def test_empty_artifact_text_returns_empty(self):
        nuggets = _deconstruct_one_artifact(_artifact(artifact_text="Ok."))
        self.assertEqual(nuggets, [])


class TestProcessPendingArtifacts(unittest.TestCase):
    @patch(f"{_REPO}.insert_audit_event", return_value=True)
    @patch(f"{_REPO}.mark_artifact_deconstructed", return_value=True)
    @patch(f"{_REPO}.insert_nugget", return_value=True)
    @patch(f"{_REPO}.update_artifact_deconstruction_status", return_value=True)
    @patch(f"{_REPO}.list_rail_artifacts_pending_deconstruction")
    def test_returns_summary_dict(self, mock_list, mock_status, mock_insert,
                                  mock_mark, mock_audit):
        mock_list.return_value = [_artifact()]
        result = process_pending_artifacts(tenant_id="t1")
        self.assertIn("processed", result)
        self.assertIn("nuggets_created", result)
        self.assertIn("skipped", result)
        self.assertIn("failed", result)

    @patch(f"{_REPO}.insert_audit_event", return_value=True)
    @patch(f"{_REPO}.mark_artifact_deconstructed", return_value=True)
    @patch(f"{_REPO}.insert_nugget", return_value=True)
    @patch(f"{_REPO}.update_artifact_deconstruction_status", return_value=True)
    @patch(f"{_REPO}.list_rail_artifacts_pending_deconstruction")
    def test_processes_artifact_with_detectable_claims(
        self, mock_list, mock_status, mock_insert, mock_mark, mock_audit
    ):
        mock_list.return_value = [_artifact()]
        result = process_pending_artifacts(tenant_id="t1")
        self.assertGreaterEqual(result["processed"], 1)
        self.assertGreater(result["nuggets_created"], 0)
        self.assertEqual(result["skipped"], 0)

    @patch(f"{_REPO}.insert_audit_event", return_value=True)
    @patch(f"{_REPO}.update_artifact_deconstruction_status", return_value=True)
    @patch(f"{_REPO}.list_rail_artifacts_pending_deconstruction")
    def test_artifact_with_no_claims_is_skipped(
        self, mock_list, mock_status, mock_audit
    ):
        mock_list.return_value = [_artifact(artifact_text="Ok.")]
        result = process_pending_artifacts(tenant_id="t1")
        self.assertEqual(result["skipped"], 1)
        self.assertEqual(result["processed"], 0)
        # Status transitions: in_progress → skipped
        calls = [c.kwargs["new_status"] for c in mock_status.call_args_list]
        self.assertIn("in_progress", calls)
        self.assertIn("skipped", calls)

    @patch(f"{_REPO}.list_rail_artifacts_pending_deconstruction",
           side_effect=Exception("db down"))
    def test_db_failure_on_list_returns_zero_summary(self, _):
        result = process_pending_artifacts(tenant_id="t1")
        self.assertEqual(result["processed"], 0)
        self.assertEqual(result["nuggets_created"], 0)
        self.assertEqual(result["failed"], 0)

    @patch(f"{_REPO}.insert_audit_event", return_value=True)
    @patch(f"{_REPO}.mark_artifact_deconstructed", return_value=True)
    @patch(f"{_REPO}.insert_nugget", return_value=True)
    @patch(f"{_REPO}.update_artifact_deconstruction_status",
           side_effect=Exception("lock timeout"))
    @patch(f"{_REPO}.list_rail_artifacts_pending_deconstruction")
    def test_status_update_failure_increments_failed(
        self, mock_list, mock_status, mock_insert, mock_mark, mock_audit
    ):
        mock_list.return_value = [_artifact()]
        result = process_pending_artifacts(tenant_id="t1")
        self.assertEqual(result["failed"], 1)

    @patch(f"{_REPO}.insert_audit_event", return_value=True)
    @patch(f"{_REPO}.mark_artifact_deconstructed", return_value=True)
    @patch(f"{_REPO}.insert_nugget", return_value=True)
    @patch(f"{_REPO}.update_artifact_deconstruction_status", return_value=True)
    @patch(f"{_REPO}.list_rail_artifacts_pending_deconstruction")
    def test_batch_size_passed_to_repo(self, mock_list, *_):
        mock_list.return_value = []
        process_pending_artifacts(tenant_id="t1", batch_size=5)
        mock_list.assert_called_once_with(tenant_id="t1", limit=5)

    @patch(f"{_REPO}.insert_audit_event", return_value=True)
    @patch(f"{_REPO}.mark_artifact_deconstructed", return_value=True)
    @patch(f"{_REPO}.insert_nugget", return_value=True)
    @patch(f"{_REPO}.update_artifact_deconstruction_status", return_value=True)
    @patch(f"{_REPO}.list_rail_artifacts_pending_deconstruction")
    def test_audit_events_emitted(self, mock_list, mock_status, mock_insert,
                                   mock_mark, mock_audit):
        mock_list.return_value = [_artifact()]
        process_pending_artifacts(tenant_id="t1")
        kinds = [c.kwargs["event_kind"] for c in mock_audit.call_args_list]
        self.assertIn("artifact.deconstruction_started", kinds)
        self.assertIn("artifact.deconstruction_complete", kinds)


if __name__ == "__main__":
    unittest.main()
