"""
Execution Record Contract

Represents the immutable output of a single execution.
Structure only — no storage or processing logic.
"""

from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Any, Dict


@dataclass(frozen=True)
class ExecutionRecord:
    tenant_id: str
    envelope_id: str

    result: Dict[str, Any]

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
