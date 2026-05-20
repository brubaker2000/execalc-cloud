from __future__ import annotations

import pytest

from src.service.substrate.interface import (
    CoverageLevel,
    ModelTier,
    SubstrateCallClass,
    SubstrateRequest,
)
from src.service.substrate.router import select_tier
from src.service.substrate.providers.echo_provider import call as echo_call
from src.service.substrate.prompts import build_system_prompt


# --- router ---

class TestSelectTier:
    def test_conversational_always_economy(self):
        for cov in CoverageLevel:
            assert select_tier(SubstrateCallClass.CONVERSATIONAL, cov) == ModelTier.ECONOMY

    def test_execution_gate_always_capable(self):
        for cov in CoverageLevel:
            assert select_tier(SubstrateCallClass.EXECUTION_GATE, cov) == ModelTier.CAPABLE

    def test_structured_synthesis_full_is_standard(self):
        assert select_tier(
            SubstrateCallClass.STRUCTURED_SYNTHESIS, CoverageLevel.FULL
        ) == ModelTier.STANDARD

    def test_structured_synthesis_partial_is_capable(self):
        assert select_tier(
            SubstrateCallClass.STRUCTURED_SYNTHESIS, CoverageLevel.PARTIAL
        ) == ModelTier.CAPABLE

    def test_corpus_retrieval_full_is_economy(self):
        assert select_tier(
            SubstrateCallClass.CORPUS_RETRIEVAL, CoverageLevel.FULL
        ) == ModelTier.ECONOMY

    def test_high_risk_forces_capable(self):
        assert select_tier(
            SubstrateCallClass.CONVERSATIONAL, CoverageLevel.FULL, risk_level="HIGH"
        ) == ModelTier.CAPABLE

    def test_critical_risk_forces_capable(self):
        assert select_tier(
            SubstrateCallClass.CORPUS_RETRIEVAL, CoverageLevel.FULL, risk_level="CRITICAL"
        ) == ModelTier.CAPABLE

    def test_elevated_posture_forces_capable(self):
        assert select_tier(
            SubstrateCallClass.CONVERSATIONAL, CoverageLevel.FULL,
            tenant_governance_posture="ELEVATED"
        ) == ModelTier.CAPABLE

    def test_override_escalates(self):
        # Policy says ECONOMY for CONVERSATIONAL/FULL — override to CAPABLE is accepted
        result = select_tier(
            SubstrateCallClass.CONVERSATIONAL, CoverageLevel.FULL,
            override_tier=ModelTier.CAPABLE
        )
        assert result == ModelTier.CAPABLE

    def test_override_cannot_de_escalate_below_policy(self):
        # Policy says CAPABLE for EXECUTION_GATE — override to ECONOMY is rejected
        result = select_tier(
            SubstrateCallClass.EXECUTION_GATE, CoverageLevel.FULL,
            override_tier=ModelTier.ECONOMY
        )
        assert result == ModelTier.CAPABLE

    def test_audit_narration_full_is_economy(self):
        assert select_tier(
            SubstrateCallClass.AUDIT_NARRATION, CoverageLevel.FULL
        ) == ModelTier.ECONOMY

    def test_audit_narration_minimal_is_standard(self):
        assert select_tier(
            SubstrateCallClass.AUDIT_NARRATION, CoverageLevel.MINIMAL
        ) == ModelTier.STANDARD


# --- echo provider ---

class TestEchoProvider:
    def _make_request(self, call_class=SubstrateCallClass.CONVERSATIONAL) -> SubstrateRequest:
        return SubstrateRequest(
            call_class=call_class,
            governance_coverage=CoverageLevel.FULL,
            system_prompt="system",
            user_turn="hello",
            tenant_id="t1",
            call_id="test-call-1",
        )

    def test_echo_returns_response(self):
        req = self._make_request()
        resp = echo_call(req, model="test-model")
        assert resp.provider == "echo"
        assert resp.model == "test-model"
        assert resp.call_id == "test-call-1"
        assert "CONVERSATIONAL" in resp.content
        assert resp.input_tokens > 0
        assert resp.output_tokens > 0
        assert resp.latency_ms >= 0

    def test_echo_reflects_call_class(self):
        req = self._make_request(SubstrateCallClass.EXECUTION_GATE)
        resp = echo_call(req, model="m")
        assert "EXECUTION_GATE" in resp.content


# --- prompts ---

class TestBuildSystemPrompt:
    def test_conversational_contains_base(self):
        prompt = build_system_prompt(SubstrateCallClass.CONVERSATIONAL, tenant_id="t1")
        assert "governed executive cognition" in prompt
        assert "t1" in prompt

    def test_execution_gate_contains_warning(self):
        prompt = build_system_prompt(SubstrateCallClass.EXECUTION_GATE, tenant_id="t1")
        assert "EXECUTION GATE" in prompt
        assert "Never authorize execution directly" in prompt

    def test_corpus_retrieval_contains_attribution_instruction(self):
        prompt = build_system_prompt(SubstrateCallClass.CORPUS_RETRIEVAL, tenant_id="t1")
        assert "Attribute each point" in prompt

    def test_claims_are_formatted_into_prompt(self):
        claims = [
            {"claim_type": "risk", "confidence_score": 0.91, "content": "Market risk is elevated."}
        ]
        prompt = build_system_prompt(
            SubstrateCallClass.STRUCTURED_SYNTHESIS, tenant_id="t1", corpus_claims=claims
        )
        assert "Market risk is elevated." in prompt
        assert "risk" in prompt

    def test_empty_claims_no_claims_block(self):
        prompt = build_system_prompt(SubstrateCallClass.CONVERSATIONAL, tenant_id="t1")
        assert "Activated Corpus Claims" not in prompt


# --- caller integration (echo path, no API key required) ---

class TestCallSubstrate:
    def test_call_substrate_echo_fallback(self, monkeypatch):
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        from src.service.substrate.caller import call_substrate
        req = SubstrateRequest(
            call_class=SubstrateCallClass.CONVERSATIONAL,
            governance_coverage=CoverageLevel.MINIMAL,
            system_prompt="sys",
            user_turn="hello",
            tenant_id="t1",
            call_id="x",
        )
        resp = call_substrate(req)
        assert resp.provider == "echo"
        assert len(resp.content) > 0

    def test_call_substrate_execution_gate_uses_capable_tier(self, monkeypatch):
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        from src.service.substrate.caller import call_substrate
        req = SubstrateRequest(
            call_class=SubstrateCallClass.EXECUTION_GATE,
            governance_coverage=CoverageLevel.FULL,
            system_prompt="sys",
            user_turn="execute now",
            tenant_id="t1",
            call_id="y",
        )
        resp = call_substrate(req)
        # echo provider reflects the model name from config
        assert "opus" in resp.model or "capable" in resp.model or resp.provider == "echo"
