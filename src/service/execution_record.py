"""
Execution Record

Represents a single execution outcome within Execalc.
This is a pure data contract — no storage, no logic.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from datetime import datetime
from src.service.tenant.context import TenantContext


@dataclass
class ExecutionRecord:
    """
    Immutable record of what occurred during an execution.
    """

    # Stable identity
    tenant_context: TenantContext

    # Optional seat / user attribution (future)
    seat_id: Optional[str] = None

    # Input snapshot at execution time
    input: Dict[str, Any] = field(default_factory=dict)

    # Output / result snapshot
    output: Dict[str, Any] = field(default_factory=dict)

    # Execution metadata
    meta: Dict[str, Any] = field(default_factory=dict)

    # Timestamp of execution
    executed_at: datetime = field(default_factory=datetime.utcnow)
