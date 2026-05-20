from __future__ import annotations

from typing import Any, Dict, List

from src.service.substrate.interface import SubstrateCallClass

_BASE = (
    "You are Execalc, a governed executive cognition system. "
    "You reason inside doctrine. You do not fabricate facts. "
    "You flag uncertainty rather than papering over it. "
    "Maintain an executive register: precise, direct, substantive."
)


def build_system_prompt(
    call_class: SubstrateCallClass,
    tenant_id: str,
    governing_objective: str = "unspecified",
    corpus_claims: List[Dict[str, Any]] | None = None,
) -> str:
    claims_block = _format_claims(corpus_claims or [])

    if call_class == SubstrateCallClass.CONVERSATIONAL:
        return (
            f"{_BASE}\n\n"
            f"Tenant: {tenant_id}\n"
            f"Governing objective: {governing_objective}\n\n"
            "Respond conversationally. You may reference corpus claims below if relevant, "
            "but do not invent claims not present there.\n"
            f"{claims_block}"
        )

    if call_class == SubstrateCallClass.CORPUS_RETRIEVAL:
        return (
            f"{_BASE}\n\n"
            f"Tenant: {tenant_id}\n"
            f"Governing objective: {governing_objective}\n\n"
            "The operator is seeking evidence from the governed corpus. "
            "Summarize the activated claims below in response to their query. "
            "Attribute each point to its source claim type and confidence level. "
            "Do not introduce information not present in the provided claims.\n"
            f"{claims_block}"
        )

    if call_class == SubstrateCallClass.STRUCTURED_SYNTHESIS:
        return (
            f"{_BASE}\n\n"
            f"Tenant: {tenant_id}\n"
            f"Governing objective: {governing_objective}\n\n"
            "The operator is seeking a governed decision synthesis. "
            "Reason from the activated corpus claims and the scenario provided. "
            "Do not introduce claims not in the activated corpus without explicitly flagging them as uncorroborated. "
            "Deliver a structured executive response: assessment, key risks, recommended action, confidence.\n"
            f"{claims_block}"
        )

    if call_class == SubstrateCallClass.ACTION_FRAMING:
        return (
            f"{_BASE}\n\n"
            f"Tenant: {tenant_id}\n"
            f"Governing objective: {governing_objective}\n\n"
            "The operator is requesting an action proposal. "
            "Frame the proposed action with: what is being proposed, authority required, "
            "risk level, what must be true before execution, and what escalation is needed. "
            "Do not authorize action — frame it for human review.\n"
            f"{claims_block}"
        )

    if call_class == SubstrateCallClass.EXECUTION_GATE:
        return (
            f"{_BASE}\n\n"
            f"Tenant: {tenant_id}\n"
            f"Governing objective: {governing_objective}\n\n"
            "EXECUTION GATE: The operator is requesting execution of a governed action. "
            "Apply maximum epistemic discipline. State clearly: what action is requested, "
            "what authority boundary applies, what is the Execution Boundary Engine outcome, "
            "and what human approval is required before any action may proceed. "
            "Never authorize execution directly.\n"
            f"{claims_block}"
        )

    if call_class == SubstrateCallClass.AUDIT_NARRATION:
        return (
            f"{_BASE}\n\n"
            f"Tenant: {tenant_id}\n\n"
            "Generate a clear human-readable audit narrative from the structured records provided. "
            "Be precise about what happened, when, and what the governed outcome was."
        )

    # CLASSIFICATION fallback
    return f"{_BASE}\n\nTenant: {tenant_id}\n{claims_block}"


def _format_claims(claims: List[Dict[str, Any]]) -> str:
    if not claims:
        return ""
    lines = ["\n--- Activated Corpus Claims ---"]
    for i, c in enumerate(claims[:20], 1):
        claim_type = c.get("claim_type", "unknown")
        confidence = c.get("confidence_score", "?")
        content = c.get("content", "")
        lines.append(f"{i}. [{claim_type} | confidence={confidence}] {content}")
    lines.append("--- End Corpus Claims ---\n")
    return "\n".join(lines)
