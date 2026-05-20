import unittest

from src.service.memory.admission import AdmissionError, build, validate


class TestValidate(unittest.TestCase):
    def _valid_gaqp(self, **overrides):
        base = dict(
            tenant_id="t1",
            memory_class="gaqp_claim",
            content="Some claim content.",
            summary="A summary.",
            source_kind="qcr_nugget",
            source_ref="claim_001",
            origin_surface="qcr_corpus",
            activation_state="active",
            claim_type="doctrine",
            memory_family=None,
        )
        base.update(overrides)
        return base

    def _valid_structural(self, **overrides):
        base = dict(
            tenant_id="t1",
            memory_class="structural",
            content="Tenant operates in automotive sector.",
            summary="Industry context.",
            source_kind="operator_direct",
            source_ref="manual_001",
            origin_surface="admin",
            activation_state="active",
            claim_type=None,
            memory_family="organizational",
        )
        base.update(overrides)
        return base

    def test_valid_gaqp_claim_passes(self):
        validate(**self._valid_gaqp())  # should not raise

    def test_valid_structural_passes(self):
        validate(**self._valid_structural())  # should not raise

    def test_missing_tenant_raises(self):
        with self.assertRaises(AdmissionError):
            validate(**self._valid_gaqp(tenant_id=""))

    def test_invalid_memory_class_raises(self):
        with self.assertRaises(AdmissionError):
            validate(**self._valid_gaqp(memory_class="unknown"))

    def test_gaqp_missing_claim_type_raises(self):
        with self.assertRaises(AdmissionError):
            validate(**self._valid_gaqp(claim_type=None))

    def test_gaqp_with_memory_family_raises(self):
        with self.assertRaises(AdmissionError):
            validate(**self._valid_gaqp(memory_family="strategic"))

    def test_structural_missing_family_raises(self):
        with self.assertRaises(AdmissionError):
            validate(**self._valid_structural(memory_family=None))

    def test_structural_with_claim_type_raises(self):
        with self.assertRaises(AdmissionError):
            validate(**self._valid_structural(claim_type="doctrine"))

    def test_invalid_activation_state_raises(self):
        with self.assertRaises(AdmissionError):
            validate(**self._valid_gaqp(activation_state="sleeping"))

    def test_invalid_claim_type_raises(self):
        with self.assertRaises(AdmissionError):
            validate(**self._valid_gaqp(claim_type="made_up_type"))


class TestBuild(unittest.TestCase):
    def test_build_gaqp_object(self):
        obj = build(
            tenant_id="t1",
            memory_class="gaqp_claim",
            content="Agents provide labor. Execalc provides judgment.",
            summary="Labor vs judgment doctrine.",
            source_kind="qcr_nugget",
            source_ref="claim_abc",
            origin_surface="qcr_corpus",
            claim_type="doctrine",
            domain="strategy",
            confidence=1.0,
        )
        self.assertEqual(obj.tenant_id, "t1")
        self.assertEqual(obj.memory_class, "gaqp_claim")
        self.assertEqual(obj.claim_type, "doctrine")
        self.assertIsNone(obj.memory_family)
        self.assertTrue(len(obj.memory_id) >= 16)

    def test_build_structural_object(self):
        obj = build(
            tenant_id="t1",
            memory_class="structural",
            content="Tenant is a PE firm focused on healthcare.",
            summary="Tenant industry context.",
            source_kind="operator_direct",
            source_ref="setup_001",
            origin_surface="admin",
            memory_family="organizational",
        )
        self.assertEqual(obj.memory_class, "structural")
        self.assertEqual(obj.memory_family, "organizational")
        self.assertIsNone(obj.claim_type)


if __name__ == "__main__":
    unittest.main()
