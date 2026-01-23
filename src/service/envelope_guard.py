"""
Envelope Guards

Enforces execution-time invariants.
"""

from src.service.envelope import IngressEnvelope


def assert_envelope_sealed(envelope: IngressEnvelope) -> None:
    """
    Raise if the envelope is not sealed for execution.
    """

    if envelope.mutable:
        raise RuntimeError("Envelope must be sealed before execution")
