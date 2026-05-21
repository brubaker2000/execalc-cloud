import os
import sys
import unittest
from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

import src.service.api as api


def _idea(**kw):
    from src.service.qualitative_capture.models import PreservedIdea
    defaults = dict(
        idea_id="idea1",
        tenant_id="t1",
        nugget_id="n1",
        session_id="s1",
        source_event_id="e1",
        selected_text="Fire hose principle.",
        memorialized_by="user1",
        memorialized_at=datetime(2026, 5, 20, tzinfo=UTC),
    )
    return PreservedIdea(**{**defaults, **kw})


def _packet_dict():
    return {
        "session_id": "s1",
        "tenant_id": "t1",
        "generated_at": "2026-05-20T00:00:00+00:00",
        "session_title": "doctrine [strategy]",
        "core_breakthrough": "We will not compromise on quality.",
        "nugget_count": 2,
        "claim_type_breakdown": {"doctrine": 2},
        "top_nuggets": [],
        "doctrine_candidates": [],
        "decisions_made": [],
        "open_questions": [],
        "preserved_ideas": [],
        "pending_promotions": [],
        "executive_conclusions": [],
        "domain": "strategy",
    }


def _event(**kw):
    from src.service.qualitative_capture.models import ConversationEvent
    defaults = dict(
        event_id="evt1",
        tenant_id="t1",
        session_id="s1",
        user_id="u1",
        role="operator",
        message_text="We will not compromise.",
        created_at=datetime(2026, 5, 20, tzinfo=UTC),
    )
    return ConversationEvent(**{**defaults, **kw})


def _candidate(**kw):
    from src.service.qualitative_capture.models import PromotionCandidate
    defaults = dict(
        candidate_id="cand1",
        tenant_id="t1",
        candidate_text="We never compromise.",
        proposed_claim_type="doctrine",
        nominated_by="operator",
        nominated_at=datetime(2026, 5, 20, tzinfo=UTC),
        review_status="pending",
        source_artifact_id="art1",
    )
    return PromotionCandidate(**{**defaults, **kw})


_MOD = "src.service.api"
_HEADERS = {"X-User-Id": "u1", "X-Role": "operator", "X-Tenant-Id": "t1"}


class TestQCRApiBase(unittest.TestCase):
    def setUp(self):
        # Pin sys.modules to the module object we imported at file load time.
        # test_dev_harness_cloud_run_guard pops "src.service.api" from sys.modules;
        # if it's missing, @patch resolves a fresh reimport whose names differ from
        # the handlers registered on api.app, so patches have no effect.
        sys.modules["src.service.api"] = api
        os.environ["EXECALC_DEV_HARNESS"] = "1"
        os.environ["EXECALC_PERSIST_EXECUTIONS"] = "0"
        self.client = api.app.test_client()

    def tearDown(self):
        os.environ.pop("EXECALC_DEV_HARNESS", None)
        os.environ.pop("EXECALC_PERSIST_EXECUTIONS", None)


class TestQCRIngestEvent(TestQCRApiBase):
    @patch(f"{_MOD}.insert_nugget", return_value=True)
    @patch(f"{_MOD}.deconstruct_event", return_value=[])
    @patch(f"{_MOD}.ingest_event")
    def test_returns_event_id(self, mock_ingest, mock_dec, mock_insert):
        mock_ingest.return_value = _event()
        resp = self.client.post(
            "/qcr/events",
            headers=_HEADERS,
            json={"session_id": "s1", "message_text": "We will always own quality."},
        )
        self.assertEqual(resp.status_code, 200)
        body = resp.get_json()
        self.assertTrue(body["ok"])
        self.assertEqual(body["event_id"], "evt1")
        self.assertIn("nuggets_extracted", body)

    @patch(f"{_MOD}.insert_nugget", return_value=True)
    @patch(f"{_MOD}.deconstruct_event", return_value=[])
    @patch(f"{_MOD}.ingest_event")
    def test_rejects_missing_session_id(self, mock_ingest, *_):
        resp = self.client.post(
            "/qcr/events",
            headers=_HEADERS,
            json={"message_text": "We will not compromise."},
        )
        self.assertEqual(resp.status_code, 400)

    @patch(f"{_MOD}.insert_nugget", return_value=True)
    @patch(f"{_MOD}.deconstruct_event", return_value=[])
    @patch(f"{_MOD}.ingest_event")
    def test_rejects_missing_message_text(self, *_):
        resp = self.client.post(
            "/qcr/events",
            headers=_HEADERS,
            json={"session_id": "s1"},
        )
        self.assertEqual(resp.status_code, 400)

    @patch(f"{_MOD}.insert_nugget", return_value=True)
    @patch(f"{_MOD}.deconstruct_event", return_value=[])
    @patch(f"{_MOD}.ingest_event", side_effect=ValueError("invalid role"))
    def test_propagates_value_error_as_400(self, *_):
        resp = self.client.post(
            "/qcr/events",
            headers=_HEADERS,
            json={"session_id": "s1", "message_text": "Msg.", "role": "hacker"},
        )
        self.assertEqual(resp.status_code, 400)

    def test_rejects_non_operator_role(self):
        headers = {**_HEADERS, "X-Role": "viewer"}
        resp = self.client.post("/qcr/events", headers=headers, json={})
        self.assertEqual(resp.status_code, 403)


class TestQCRMemorialize(TestQCRApiBase):
    @patch(f"{_MOD}.memorialize")
    def test_returns_idea(self, mock_mem):
        mock_mem.return_value = _idea()
        resp = self.client.post(
            "/qcr/ideas",
            headers=_HEADERS,
            json={
                "session_id": "s1",
                "source_event_id": "e1",
                "selected_text": "Fire hose.",
                "claim_type": "observation",
            },
        )
        self.assertEqual(resp.status_code, 200)
        body = resp.get_json()
        self.assertTrue(body["ok"])
        self.assertIn("idea", body)
        self.assertEqual(body["idea"]["idea_id"], "idea1")

    @patch(f"{_MOD}.memorialize")
    def test_rejects_missing_source_event_id(self, _):
        resp = self.client.post(
            "/qcr/ideas",
            headers=_HEADERS,
            json={"session_id": "s1", "selected_text": "Fire hose.", "claim_type": "observation"},
        )
        self.assertEqual(resp.status_code, 400)

    @patch(f"{_MOD}.memorialize")
    def test_rejects_empty_selected_text(self, _):
        resp = self.client.post(
            "/qcr/ideas",
            headers=_HEADERS,
            json={"session_id": "s1", "source_event_id": "e1", "selected_text": "  "},
        )
        self.assertEqual(resp.status_code, 400)


class TestQCRSessionPacket(TestQCRApiBase):
    @patch(f"{_MOD}.generate_session_packet")
    def test_returns_packet(self, mock_gen):
        mock_pkt = MagicMock()
        mock_pkt.to_dict.return_value = _packet_dict()
        mock_gen.return_value = mock_pkt

        resp = self.client.get("/qcr/session/s1/packet", headers=_HEADERS)
        self.assertEqual(resp.status_code, 200)
        body = resp.get_json()
        self.assertTrue(body["ok"])
        self.assertIn("packet", body)
        self.assertEqual(body["packet"]["session_id"], "s1")

    @patch(f"{_MOD}.generate_session_packet")
    def test_forwards_domain_query_param(self, mock_gen):
        mock_pkt = MagicMock()
        mock_pkt.to_dict.return_value = _packet_dict()
        mock_gen.return_value = mock_pkt

        self.client.get("/qcr/session/s1/packet?domain=capital", headers=_HEADERS)
        _, kwargs = mock_gen.call_args
        self.assertEqual(kwargs["domain"], "capital")


class TestQCRSessionRail(TestQCRApiBase):
    @patch(f"{_MOD}.get_session_rail", return_value=[{"card_id": "c1"}])
    def test_returns_cards(self, _):
        resp = self.client.get("/qcr/session/s1/rail", headers=_HEADERS)
        self.assertEqual(resp.status_code, 200)
        body = resp.get_json()
        self.assertTrue(body["ok"])
        self.assertEqual(body["count"], 1)


class TestQCRGetNuggets(TestQCRApiBase):
    @patch(f"{_MOD}.search_claims", return_value=[{"nugget_id": "n1"}])
    def test_query_mode_delegates_to_search(self, mock_search):
        resp = self.client.get("/qcr/nuggets?q=doctrine", headers=_HEADERS)
        self.assertEqual(resp.status_code, 200)
        body = resp.get_json()
        self.assertTrue(body["ok"])
        self.assertEqual(body["count"], 1)
        mock_search.assert_called_once()

    @patch(f"{_MOD}.retrieve_doctrine", return_value=[{"nugget_id": "n2"}])
    def test_category_doctrine_delegates(self, mock_retrieve):
        resp = self.client.get("/qcr/nuggets?category=doctrine", headers=_HEADERS)
        self.assertEqual(resp.status_code, 200)
        mock_retrieve.assert_called_once()

    @patch(f"{_MOD}.retrieve_risks", return_value=[])
    def test_category_risks_delegates(self, mock_retrieve):
        resp = self.client.get("/qcr/nuggets?category=risks", headers=_HEADERS)
        self.assertEqual(resp.status_code, 200)
        mock_retrieve.assert_called_once()

    def test_no_category_or_query_returns_400(self):
        resp = self.client.get("/qcr/nuggets", headers=_HEADERS)
        self.assertEqual(resp.status_code, 400)


class TestQCRSecondOrderRun(TestQCRApiBase):
    @patch(f"{_MOD}.process_pending_artifacts",
           return_value={"processed": 3, "nuggets_created": 7, "skipped": 1, "failed": 0})
    def test_returns_summary(self, mock_proc):
        resp = self.client.post(
            "/qcr/second-order/run", headers=_HEADERS, json={"batch_size": 10}
        )
        self.assertEqual(resp.status_code, 200)
        body = resp.get_json()
        self.assertTrue(body["ok"])
        self.assertEqual(body["processed"], 3)
        self.assertEqual(body["nuggets_created"], 7)

    @patch(f"{_MOD}.process_pending_artifacts", return_value={"processed": 0, "nuggets_created": 0, "skipped": 0, "failed": 0})
    def test_default_batch_size(self, mock_proc):
        self.client.post("/qcr/second-order/run", headers=_HEADERS, json={})
        _, kwargs = mock_proc.call_args
        self.assertEqual(kwargs["batch_size"], 10)

    def test_invalid_batch_size_returns_400(self):
        resp = self.client.post(
            "/qcr/second-order/run", headers=_HEADERS, json={"batch_size": "nope"}
        )
        self.assertEqual(resp.status_code, 400)

    def test_out_of_range_batch_size_returns_400(self):
        resp = self.client.post(
            "/qcr/second-order/run", headers=_HEADERS, json={"batch_size": 999}
        )
        self.assertEqual(resp.status_code, 400)


class TestQCRPromotion(TestQCRApiBase):
    @patch(f"{_MOD}.nominate_for_promotion")
    def test_nominate_returns_candidate_id(self, mock_nom):
        mock_nom.return_value = _candidate()
        resp = self.client.post(
            "/qcr/promotion/nominate",
            headers=_HEADERS,
            json={
                "candidate_text": "We never compromise.",
                "proposed_claim_type": "doctrine",
                "source_artifact_id": "art1",
            },
        )
        self.assertEqual(resp.status_code, 200)
        body = resp.get_json()
        self.assertTrue(body["ok"])
        self.assertEqual(body["candidate_id"], "cand1")

    def test_nominate_rejects_missing_source(self):
        resp = self.client.post(
            "/qcr/promotion/nominate",
            headers=_HEADERS,
            json={"candidate_text": "X", "proposed_claim_type": "doctrine"},
        )
        self.assertEqual(resp.status_code, 400)

    @patch(f"{_MOD}.approve_candidate", return_value=True)
    def test_approve_returns_true(self, _):
        resp = self.client.post("/qcr/promotion/cand1/approve", headers=_HEADERS)
        self.assertEqual(resp.status_code, 200)
        body = resp.get_json()
        self.assertTrue(body["ok"])
        self.assertTrue(body["approved"])

    @patch(f"{_MOD}.reject_candidate", return_value=True)
    def test_reject_returns_true(self, _):
        resp = self.client.post(
            "/qcr/promotion/cand1/reject",
            headers=_HEADERS,
            json={"rejection_reason": "Not strong enough yet."},
        )
        self.assertEqual(resp.status_code, 200)
        body = resp.get_json()
        self.assertTrue(body["ok"])
        self.assertTrue(body["rejected"])


class TestQCRDecayRun(TestQCRApiBase):
    @patch(f"{_MOD}.apply_decay_pass",
           return_value={"expired": 2, "flagged_medium_term": 1, "flagged_date_sensitive": 3, "failed": 0})
    def test_returns_summary(self, mock_decay):
        resp = self.client.post("/qcr/decay/run", headers=_HEADERS, json={"batch_size": 50})
        self.assertEqual(resp.status_code, 200)
        body = resp.get_json()
        self.assertTrue(body["ok"])
        self.assertEqual(body["expired"], 2)
        self.assertEqual(body["flagged_medium_term"], 1)
        self.assertEqual(body["flagged_date_sensitive"], 3)

    @patch(f"{_MOD}.apply_decay_pass",
           return_value={"expired": 0, "flagged_medium_term": 0, "flagged_date_sensitive": 0, "failed": 0})
    def test_default_batch_size(self, mock_decay):
        self.client.post("/qcr/decay/run", headers=_HEADERS, json={})
        _, kwargs = mock_decay.call_args
        self.assertEqual(kwargs["batch_size"], 50)

    def test_invalid_batch_size_returns_400(self):
        resp = self.client.post("/qcr/decay/run", headers=_HEADERS, json={"batch_size": "bad"})
        self.assertEqual(resp.status_code, 400)

    def test_out_of_range_batch_size_returns_400(self):
        resp = self.client.post("/qcr/decay/run", headers=_HEADERS, json={"batch_size": 9999})
        self.assertEqual(resp.status_code, 400)


if __name__ == "__main__":
    unittest.main()
