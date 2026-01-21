"""
Envelope Seal

Defines the irreversible transition from ingress
(mutable) to execution (immutable).
"""

from src.service.envelope import IngressEnvelope
from src.service.tenant.guards import assert_tenant_context_immutable


def seal_envelope(envelope: IngressEnvelope) -> IngressEnvelope:
    """
    Seal the envelope for execution.

    Preconditions:
    - Tenant context must be present
    - Envelope must still be mutable

    Postconditions:
    - Envelope is marked immutable
    """

    if not envelope.mutable:
        raise RuntimeError("Envelope is already sealed")

    # Enforce tenant context immutability
    assert_tenant_context_immutable({"tenant_context": envelope.tenant_context})

    envelope.mutable = False
    return envelope

