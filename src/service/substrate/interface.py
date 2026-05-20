from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class SubstrateCallClass(str, Enum):
    CONVERSATIONAL = "CONVERSATIONAL"
    CLASSIFICATION = "CLASSIFICATION"
    CORPUS_RETRIEVAL = "CORPUS_RETRIEVAL"
    STRUCTURED_SYNTHESIS = "STRUCTURED_SYNTHESIS"
    ACTION_FRAMING = "ACTION_FRAMING"
    EXECUTION_GATE = "EXECUTION_GATE"
    AUDIT_NARRATION = "AUDIT_NARRATION"


class CoverageLevel(str, Enum):
    FULL = "FULL"
    PARTIAL = "PARTIAL"
    MINIMAL = "MINIMAL"


class ModelTier(str, Enum):
    ECONOMY = "ECONOMY"
    STANDARD = "STANDARD"
    CAPABLE = "CAPABLE"


@dataclass
class SubstrateRequest:
    call_class: SubstrateCallClass
    governance_coverage: CoverageLevel
    system_prompt: str
    user_turn: str
    tenant_id: str
    call_id: str
    max_tokens: int = 1024
    output_schema: Optional[Dict[str, Any]] = None
    override_tier: Optional[ModelTier] = None


@dataclass
class SubstrateResponse:
    content: str
    provider: str
    model: str
    input_tokens: int
    output_tokens: int
    call_id: str
    latency_ms: int
    structured_output: Optional[Dict[str, Any]] = None
