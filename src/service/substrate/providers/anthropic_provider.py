from __future__ import annotations

import time

from src.service.substrate.interface import SubstrateRequest, SubstrateResponse


def call(request: SubstrateRequest, model: str, api_key: str) -> SubstrateResponse:
    try:
        import anthropic
    except ImportError as e:
        raise RuntimeError(
            "anthropic package is not installed. Add 'anthropic' to requirements.txt."
        ) from e

    client = anthropic.Anthropic(api_key=api_key)

    start = time.monotonic()
    response = client.messages.create(
        model=model,
        max_tokens=request.max_tokens,
        system=request.system_prompt,
        messages=[{"role": "user", "content": request.user_turn}],
    )
    latency_ms = int((time.monotonic() - start) * 1000)

    content = response.content[0].text if response.content else ""
    return SubstrateResponse(
        content=content,
        provider="anthropic",
        model=model,
        input_tokens=response.usage.input_tokens,
        output_tokens=response.usage.output_tokens,
        call_id=request.call_id,
        latency_ms=latency_ms,
    )
