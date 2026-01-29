"""
Envelope Seal

Defines the irreversible transition from ingress
(mutable) to execution (immutable).
"""

from src.service.envelope import IngressEnvelope
from src.service.tenant.guards import assert_tenant_context_immutable
from src.service.tenant.context import peek_tenant_context


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

    if envelope.tenant_context is None:
        raise RuntimeError("Tenant context missing")

    # If an execution tenant context is already established, enforce it matches.
    current = peek_tenant_context()
    if current is not None:
        assert_tenant_context_immutable(envelope.tenant_context.tenant_id)

    envelope.mutable = False
    return envelope
