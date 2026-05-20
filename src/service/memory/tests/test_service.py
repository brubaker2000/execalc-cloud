import unittest
from unittest.mock import MagicMock, patch

from src.service.memory.models import MemoryContext, MemoryObject
from src.service.memory import admit_memory, get_memory, list_memory, get_upstream_context, update_memory_state
from src.service.memory.admission import AdmissionError


def _make_obj(**overrides):
    from datetime import UTC, datetime
    defaults = dict(
        memory_id="mem001",
        tenant_id="t1",
        memory_class="gaqp_claim",
        activation_state="active",
        content="AI produces value faster than humans can absorb.",
        summary="Fire hose doctrine.",
        source_kind="qcr_nugget",
        source_ref="claim_001",
        origin_surface="qcr_corpus",
        claim_type="doctrine",
        domain="strategy",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    defaults.update(overrides)
    return MemoryObject(**defaults)


class TestAdmitMemory(unittest.TestCase):
    @patch("src.service.memory.service.db_insert")
    def test_admit_gaqp_claim(self, mock_insert):
        mock_insert.return_value = True
        obj = admit_memory(
            tenant_id="t1",
            memory_class="gaqp_claim",
            content="Some doctrine.",
            summary="Doctrine summary.",
            source_kind="qcr_nugget",
            source_ref="claim_001",
            origin_surface="qcr_corpus",
            claim_type="doctrine",
            domain="strategy",
        )
        self.assertEqual(obj.tenant_id, "t1")
        self.assertEqual(obj.claim_type, "doctrine")
        mock_insert.assert_called_once()

    @patch("src.service.memory.service.db_insert")
    def test_admit_validation_failure_raises(self, mock_insert):
        with self.assertRaises(AdmissionError):
            admit_memory(
                tenant_id="t1",
                memory_class="gaqp_claim",
                content="Missing claim type.",
                summary="Summary.",
                source_kind="qcr_nugget",
                source_ref="claim_001",
                origin_surface="qcr_corpus",
                # claim_type intentionally omitted
            )
        mock_insert.assert_not_called()


class TestGetMemory(unittest.TestCase):
    @patch("src.service.memory.service.db_get")
    def test_returns_object_when_found(self, mock_get):
        mock_get.return_value = _make_obj()
        result = get_memory(tenant_id="t1", memory_id="mem001")
        self.assertIsNotNone(result)
        self.assertEqual(result.memory_id, "mem001")

    @patch("src.service.memory.service.db_get")
    def test_returns_none_when_not_found(self, mock_get):
        mock_get.return_value = None
        result = get_memory(tenant_id="t1", memory_id="missing")
        self.assertIsNone(result)


class TestListMemory(unittest.TestCase):
    @patch("src.service.memory.service.db_list")
    def test_returns_list(self, mock_list):
        mock_list.return_value = [_make_obj()]
        result = list_memory(tenant_id="t1")
        self.assertEqual(len(result), 1)

    @patch("src.service.memory.service.db_list")
    def test_returns_empty_on_db_error(self, mock_list):
        mock_list.side_effect = Exception("db down")
        result = list_memory(tenant_id="t1")
        self.assertEqual(result, [])


class TestGetUpstreamContext(unittest.TestCase):
    @patch("src.service.memory.upstream_context.retrieve_for_context")
    def test_returns_context_with_items(self, mock_retrieve):
        mock_retrieve.return_value = [_make_obj()]
        ctx = get_upstream_context(tenant_id="t1", scenario_type="draft_trade", domain="strategy")
        self.assertIsInstance(ctx, MemoryContext)
        self.assertEqual(len(ctx.items), 1)
        self.assertFalse(ctx.is_empty)

    @patch("src.service.memory.upstream_context.retrieve_for_context")
    def test_returns_empty_context_on_failure(self, mock_retrieve):
        mock_retrieve.side_effect = Exception("retrieval failed")
        ctx = get_upstream_context(tenant_id="t1", scenario_type="draft_trade")
        self.assertIsInstance(ctx, MemoryContext)
        self.assertTrue(ctx.is_empty)


class TestUpdateMemoryState(unittest.TestCase):
    @patch("src.service.memory.service.db_get")
    @patch("src.service.memory.service.db_update_state")
    def test_valid_state_update(self, mock_update, mock_get):
        mock_update.return_value = True
        mock_get.return_value = _make_obj(activation_state="deferred")
        result = update_memory_state(
            tenant_id="t1", memory_id="mem001",
            new_state="deferred", actor_id="u1",
        )
        self.assertIsNotNone(result)
        self.assertEqual(result.activation_state, "deferred")

    def test_invalid_state_raises(self):
        with self.assertRaises(ValueError):
            update_memory_state(
                tenant_id="t1", memory_id="mem001",
                new_state="sleeping",
            )


if __name__ == "__main__":
    unittest.main()
