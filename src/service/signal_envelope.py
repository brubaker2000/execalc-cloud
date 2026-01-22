"""
Signal Envelope Contract

Immutable container for execution outputs:
signals, judgments, artifacts, and metrics.

This file defines structure only.
No execution, routing, or persistence logic is permitted here.
"""

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(frozen=True)
class SignalEnvelope:
    """
    Immutable execution output container.
    """

    # Primary outputs (signals, judgments, artifacts)
    outputs: Dict[str, Any]

    # Optional execution metadata (durations, counters, flags)
    meta: Dict[str, Any] = field(default_factory=dict)
