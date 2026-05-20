from __future__ import annotations

from src.service.substrate.config import anthropic_api_key, get_provider_spec
from src.service.substrate.interface import SubstrateRequest, SubstrateResponse
from src.service.substrate.router import select_tier


def call_substrate(request: SubstrateRequest) -> SubstrateResponse:
    """
    Main entry point. Selects tier, resolves provider, dispatches the call.
    Falls back to echo provider when no API key is configured.
    """
    tier = select_tier(
        call_class=request.call_class,
        coverage=request.governance_coverage,
        override_tier=request.override_tier,
    )
    spec = get_provider_spec(tier)

    if spec.provider == "anthropic":
        key = anthropic_api_key()
        if not key:
            return _echo_fallback(request, spec.model)
        from src.service.substrate.providers.anthropic_provider import call
        return call(request, model=spec.model, api_key=key)

    # echo is the explicit test provider
    if spec.provider == "echo":
        return _echo_fallback(request, spec.model)

    raise ValueError(f"Unknown substrate provider: {spec.provider!r}")


def _echo_fallback(request: SubstrateRequest, model: str) -> SubstrateResponse:
    from src.service.substrate.providers.echo_provider import call
    return call(request, model=model)
