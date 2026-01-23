"""
Judgment Link

Immutable structural linkage between:
- an execution
- a judgment
- the resulting signal envelope

Structure only. No behavior or logic permitted.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class JudgmentLink:
    """
    Immutable linkage record.
    """

    execution_id: str
    judgment_id: str
    signal_envelope_id: Optional[str] = None
