from __future__ import annotations

import os
from dataclasses import dataclass

from src.service.substrate.interface import ModelTier


@dataclass(frozen=True)
class ProviderSpec:
    provider: str
    model: str


def _env(key: str, default: str) -> str:
    return os.environ.get(key, default)


def get_provider_spec(tier: ModelTier) -> ProviderSpec:
    """Return the (provider, model) for a given tier, driven by environment config."""
    if tier == ModelTier.ECONOMY:
        return ProviderSpec(
            provider=_env("SUBSTRATE_ECONOMY_PROVIDER", "anthropic"),
            model=_env("SUBSTRATE_ECONOMY_MODEL", "claude-haiku-4-5-20251001"),
        )
    if tier == ModelTier.STANDARD:
        return ProviderSpec(
            provider=_env("SUBSTRATE_STANDARD_PROVIDER", "anthropic"),
            model=_env("SUBSTRATE_STANDARD_MODEL", "claude-sonnet-4-6"),
        )
    # CAPABLE
    return ProviderSpec(
        provider=_env("SUBSTRATE_CAPABLE_PROVIDER", "anthropic"),
        model=_env("SUBSTRATE_CAPABLE_MODEL", "claude-opus-4-7"),
    )


def anthropic_api_key() -> str | None:
    return os.environ.get("ANTHROPIC_API_KEY")
