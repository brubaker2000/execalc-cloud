from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Dict, List, Literal, Optional

# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

MemoryClass = Literal["gaqp_claim", "structural"]

ActivationState = Literal["active", "deferred", "reference_only", "dormant"]

SourceKind = Literal[
    "qcr_nugget",       # GAQP claim that reached structural confidence
    "qcr_preserved",    # human-memorialized item from the rail
    "qcr_promotion",    # operator-promoted canon candidate
    "operator_direct",  # admitted directly by operator command
    "decision_artifact",# derived from a decision envelope
]

MemoryFamily = Literal[
    "strategic",
    "decision",
    "organizational",
    "heuristic",
    "clarity",
    "constraint",
    "relationship",
]

ACTIVATION_STATES = ["active", "deferred", "reference_only", "dormant"]
MEMORY_CLASSES = ["gaqp_claim", "structural"]
SOURCE_KINDS = [
    "qcr_nugget", "qcr_preserved", "qcr_promotion",
    "operator_direct", "decision_artifact",
]
MEMORY_FAMILIES = [
    "strategic", "decision", "organizational",
    "heuristic", "clarity", "constraint", "relationship",
]


# ---------------------------------------------------------------------------
# MemoryObject — the canonical PEM corpus unit
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class MemoryObject:
    memory_id: str
    tenant_id: str
    memory_class: MemoryClass          # gaqp_claim (Class A) or structural (Class B)
    activation_state: ActivationState
    content: str
    summary: str
    source_kind: SourceKind
    source_ref: str                    # FK to originating object
    origin_surface: str

    # Class A fields (GAQP claims)
    claim_type: Optional[str] = None   # one of the 24 GAQP canonical types
    domain: Optional[str] = None

    # Class B fields (structural memory)
    memory_family: Optional[MemoryFamily] = None

    # Optional provenance and links
    actor_id: Optional[str] = None
    admission_reason: Optional[str] = None
    confidence: Optional[float] = None
    related_memory_ids: List[str] = field(default_factory=list)
    supersedes: Optional[str] = None   # memory_id of object this replaces

    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    archived_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "memory_id": self.memory_id,
            "tenant_id": self.tenant_id,
            "memory_class": self.memory_class,
            "activation_state": self.activation_state,
            "content": self.content,
            "summary": self.summary,
            "source_kind": self.source_kind,
            "source_ref": self.source_ref,
            "origin_surface": self.origin_surface,
            "claim_type": self.claim_type,
            "domain": self.domain,
            "memory_family": self.memory_family,
            "actor_id": self.actor_id,
            "admission_reason": self.admission_reason,
            "confidence": self.confidence,
            "related_memory_ids": list(self.related_memory_ids),
            "supersedes": self.supersedes,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "archived_at": self.archived_at.isoformat() if self.archived_at else None,
        }


# ---------------------------------------------------------------------------
# MemoryContext — assembled context injected into upstream reasoning
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class MemoryContext:
    tenant_id: str
    scenario_type: str
    domain: Optional[str]
    items: List[MemoryObject]           # active, relevant memory objects
    assembled_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @property
    def is_empty(self) -> bool:
        return len(self.items) == 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tenant_id": self.tenant_id,
            "scenario_type": self.scenario_type,
            "domain": self.domain,
            "item_count": len(self.items),
            "items": [m.to_dict() for m in self.items],
            "assembled_at": self.assembled_at.isoformat(),
        }
