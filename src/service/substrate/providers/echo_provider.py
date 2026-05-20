from __future__ import annotations

import time

from src.service.substrate.interface import SubstrateRequest, SubstrateResponse


def call(request: SubstrateRequest, model: str) -> SubstrateResponse:
    """Test provider — reflects the prompt back without a real API call."""
    start = time.monotonic()
    content = (
        f"[echo:{model}] call_class={request.call_class.value} "
        f"coverage={request.governance_coverage.value} | {request.user_turn[:120]}"
    )
    latency_ms = int((time.monotonic() - start) * 1000)
    return SubstrateResponse(
        content=content,
        provider="echo",
        model=model,
        input_tokens=len(request.system_prompt.split()) + len(request.user_turn.split()),
        output_tokens=len(content.split()),
        call_id=request.call_id,
        latency_ms=latency_ms,
    )
