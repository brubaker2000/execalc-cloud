"""
Judgment Record

Immutable record of a decision made during execution.
Captures what was decided, by whom, and why.
"""

from dataclasses import dataclass, field
from typing import Any, Dict
from datetime import datetime, timezone


@dataclass(frozen=True)
class JudgmentRecord:
    """
    Immutable judgment record.
    """

    # Unique identifier for this judgment
    judgment_id: str

    # Human-readable description of the decision
    decision: str

    # Rationale or supporting explanation
    rationale: str

    # Execution metadata (scenario, execution_id, etc.)
    context: Dict[str, Any] = field(default_factory=dict)

    # Timestamp (UTC, immutable)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
