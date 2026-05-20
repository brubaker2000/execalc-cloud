import unittest
from datetime import UTC, datetime

from src.service.memory.models import MemoryContext, MemoryObject


class TestMemoryObject(unittest.TestCase):
    def _make(self, **overrides):
        defaults = dict(
            memory_id="abc123",
            tenant_id="t1",
            memory_class="gaqp_claim",
            activation_state="active",
            content="AI produces value faster than humans can absorb it.",
            summary="Fire hose doctrine",
            source_kind="qcr_nugget",
            source_ref="claim_001",
            origin_surface="qcr_corpus",
            claim_type="doctrine",
            domain="strategy",
        )
        defaults.update(overrides)
        return MemoryObject(**defaults)

    def test_to_dict_contains_required_fields(self):
        obj = self._make()
        d = obj.to_dict()
        self.assertEqual(d["memory_id"], "abc123")
        self.assertEqual(d["tenant_id"], "t1")
        self.assertEqual(d["memory_class"], "gaqp_claim")
        self.assertEqual(d["activation_state"], "active")
        self.assertEqual(d["claim_type"], "doctrine")
        self.assertIsNone(d["memory_family"])

    def test_structural_object(self):
        obj = self._make(
            memory_class="structural",
            memory_family="organizational",
            claim_type=None,
            domain=None,
        )
        d = obj.to_dict()
        self.assertEqual(d["memory_class"], "structural")
        self.assertEqual(d["memory_family"], "organizational")
        self.assertIsNone(d["claim_type"])

    def test_is_frozen(self):
        obj = self._make()
        with self.assertRaises(Exception):
            obj.content = "mutated"  # type: ignore


class TestMemoryContext(unittest.TestCase):
    def test_is_empty_when_no_items(self):
        ctx = MemoryContext(
            tenant_id="t1",
            scenario_type="draft_trade",
            domain=None,
            items=[],
        )
        self.assertTrue(ctx.is_empty)

    def test_to_dict_shape(self):
        ctx = MemoryContext(
            tenant_id="t1",
            scenario_type="draft_trade",
            domain="strategy",
            items=[],
        )
        d = ctx.to_dict()
        self.assertEqual(d["tenant_id"], "t1")
        self.assertEqual(d["item_count"], 0)
        self.assertIn("assembled_at", d)


if __name__ == "__main__":
    unittest.main()
