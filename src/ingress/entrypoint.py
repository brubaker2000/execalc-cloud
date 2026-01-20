"""
Execalc Cloud v1 — Ingress Entrypoint

This module defines the sole entry point into the Execalc runtime.
All requests must pass through this boundary.
No execution occurs here.
"""

class IngressError(Exception):
    """Base exception for ingress violations."""
    pass


class TenantResolutionError(IngressError):
    """Raised when tenant identity cannot be resolved."""
    pass


class ExecutionNotPermitted(IngressError):
    """Raised when execution is attempted at ingress."""
    pass


def handle_request(request):
    """
    Ingress handler.

    This function intentionally does not execute any logic.
    Its responsibilities are limited to:
    - Verifying that a tenant context exists
    - Refusing all further processing

    Any attempt to extend behavior here must be explicitly justified
    against Cloud v1 governance.
    """

    tenant_id = getattr(request, "tenant_id", None)

    if tenant_id is None:
        raise TenantResolutionError(
            "Tenant identity is required at ingress."
        )

    raise ExecutionNotPermitted(
        "Execution is not permitted at ingress. "
        "Requests must pass governance before processing."
    )
