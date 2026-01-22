"""
Artifact Attribution Contract

Defines how any produced artifact (judgment, signal, memo,
recommendation, synthesis) is attributed to identity and execution.
Structure only. No logic permitted.
"""

from dataclasses import dataclass
from typing import Optional
from src.service.tenant.context import TenantContext
from src.service.execution_record import ExecutionRecord


@dataclass(frozen=True)
class ArtifactAttribution:
    """
    Immutable attribution metadata for any produced artifact.
    """

    tenant_context: TenantContext
    execution_record: ExecutionRecord

    # Optional seat / actor identifier (future use)
    seat_id: Optional[str] = None
