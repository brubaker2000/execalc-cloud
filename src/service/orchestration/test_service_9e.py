from __future__ import annotations

import unittest
from unittest.mock import patch

from src.service.gaqp.models import ActivationBundle
from src.service.orchestration.service import run_orchestration


def _empty_bundle(**kwargs) -> ActivationBundle:
    return ActivationBundle(
        activated_claims=[],
        activation_rationale=[],
        corpus_scope="structural",
        confidence_floor=0.50,
    )


class TestOrchestration9E(unittest.TestCase):

    # ------------------------------------------------------------------
    # corpus_intelligence present on all turn classes
    # ------------------------------------------------------------------

    def test_corpus_intelligence_present_on_decision_seeking(self):
        with patch("src.service.orchestration.service.activate", side_effect=_empty_bundle):
            out = run_orchestration(user_text="What should we do?")
        self.assertIn("corpus_intelligence", out)
        self.assertIn("activated_claims", out["corpus_intelligence"])

    def test_corpus_intelligence_present_on_conversational(self):
        with patch("src.service.orchestration.service.activate", side_effect=_empty_bundle):
            out = run_orchestration(user_text="Tell me more.")
        self.assertIn("corpus_intelligence", out)

    def test_corpus_intelligence_present_on_action_proposing(self):
        with patch("src.service.orchestration.service.activate", side_effect=_empty_bundle):
            out = run_orchestration(user_text="Draft the next move.")
        self.assertIn("corpus_intelligence", out)

    def test_corpus_intelligence_present_on_execution_seeking(self):
        with patch("src.service.orchestration.service.activate", side_effect=_empty_bundle):
            out = run_orchestration(user_text="Go ahead.")
        self.assertIn("corpus_intelligence", out)

    def test_corpus_intelligence_present_on_evidence_seeking(self):
        with patch("src.service.orchestration.service.activate", side_effect=_empty_bundle):
            out = run_orchestration(user_text="What evidence do we have?")
        self.assertIn("corpus_intelligence", out)

    # ------------------------------------------------------------------
    # corpus_claims_count in rail_state
    # ------------------------------------------------------------------

    def test_rail_state_includes_corpus_claims_count_zero(self):
        with patch("src.service.orchestration.service.activate", side_effect=_empty_bundle):
            out = run_orchestration(user_text="What should we do?")
        self.assertIn("corpus_claims_count", out["rail_state"])
        self.assertEqual(out["rail_state"]["corpus_claims_count"], 0)

    def test_rail_state_corpus_claims_count_reflects_bundle(self):
        from src.service.gaqp.activation import _dict_to_claim
        from datetime import UTC, datetime

        row = {
            "claim_id": "cid-1", "tenant_id": "t-1", "source_envelope_id": "e-1",
            "claim_type": "tradeoff", "domain": "strategy",
            "content": "Test claim.", "confidence_level": "seed",
            "confidence_score": 0.50, "admission_status": "admitted",
            "corpus_scope": "tenant", "extraction_method": "direct_field",
            "provenance": {"source_kind": "decision_artifact", "source_ref": "e-1", "actor_id": "u-1"},
            "activation_scope": "universal", "activation_triggers": [],
            "corroboration_profile": {}, "contradiction_refs": [], "support_refs": [],
            "fingerprint": "fp1", "schema_version": "stage9_v1",
            "created_at": datetime.now(UTC).isoformat(),
            "updated_at": datetime.now(UTC).isoformat(),
        }
        claim = _dict_to_claim(row)
        bundle_with_claim = ActivationBundle(
            activated_claims=[claim],
            activation_rationale=["Universal activation: claim fires on all scenarios."],
            corpus_scope="structural",
            confidence_floor=0.50,
        )

        with patch("src.service.orchestration.service.activate", return_value=bundle_with_claim):
            out = run_orchestration(user_text="What should we do?")
        self.assertEqual(out["rail_state"]["corpus_claims_count"], 1)

    # ------------------------------------------------------------------
    # evidence_seeking — now live, not a stub
    # ------------------------------------------------------------------

    def test_evidence_seeking_rail_mode_is_corpus_evidence(self):
        with patch("src.service.orchestration.service.activate", side_effect=_empty_bundle):
            out = run_orchestration(user_text="What evidence do we have?")
        self.assertEqual(out["rail_state"]["mode"], "corpus_evidence")

    def test_evidence_seeking_empty_corpus_message(self):
        with patch("src.service.orchestration.service.activate", side_effect=_empty_bundle):
            out = run_orchestration(user_text="Show me the data.")
        self.assertIn("No corpus claims matched", out["assistant_message"])
        self.assertNotIn("not yet available", out["assistant_message"])
        self.assertNotIn("planned Stage 9", out["assistant_message"])

    def test_evidence_seeking_nonempty_corpus_message(self):
        from src.service.gaqp.activation import _dict_to_claim
        from datetime import UTC, datetime

        row = {
            "claim_id": "cid-2", "tenant_id": "t-1", "source_envelope_id": "e-1",
            "claim_type": "observation", "domain": "strategy",
            "content": "Evidence claim.", "confidence_level": "seed",
            "confidence_score": 0.50, "admission_status": "admitted",
            "corpus_scope": "tenant", "extraction_method": "direct_field",
            "provenance": {"source_kind": "decision_artifact", "source_ref": "e-1", "actor_id": "u-1"},
            "activation_scope": "universal", "activation_triggers": [],
            "corroboration_profile": {}, "contradiction_refs": [], "support_refs": [],
            "fingerprint": "fp2", "schema_version": "stage9_v1",
            "created_at": datetime.now(UTC).isoformat(),
            "updated_at": datetime.now(UTC).isoformat(),
        }
        claim = _dict_to_claim(row)
        bundle = ActivationBundle(
            activated_claims=[claim],
            activation_rationale=["Universal activation: claim fires on all scenarios."],
            corpus_scope="structural",
            confidence_floor=0.50,
        )

        with patch("src.service.orchestration.service.activate", return_value=bundle):
            out = run_orchestration(user_text="What evidence do we have?")
        self.assertIn("1 corpus claim(s)", out["assistant_message"])

    # ------------------------------------------------------------------
    # existing turn class modes unaffected
    # ------------------------------------------------------------------

    def test_decision_rail_mode_unchanged(self):
        with patch("src.service.orchestration.service.activate", side_effect=_empty_bundle):
            out = run_orchestration(user_text="What should we do?")
        self.assertEqual(out["rail_state"]["mode"], "decision")

    def test_conversational_rail_mode_unchanged(self):
        with patch("src.service.orchestration.service.activate", side_effect=_empty_bundle):
            out = run_orchestration(user_text="Talk this through with me.")
        self.assertEqual(out["rail_state"]["mode"], "conversation")


if __name__ == "__main__":
    unittest.main()
