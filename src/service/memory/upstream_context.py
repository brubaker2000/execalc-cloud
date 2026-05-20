from __future__ import annotations

import logging
from typing import Optional

from src.service.memory.models import MemoryContext
from src.service.memory.retrieval import retrieve_for_context

logger = logging.getLogger(__name__)


def assemble_context(
    *,
    tenant_id: str,
    scenario_type: str,
    domain: Optional[str] = None,
) -> MemoryContext:
    """
    Assemble PEM memory context for upstream reasoning.

    Called before the decision engine runs. Returns a MemoryContext containing
    active, relevant memory objects for the tenant. Empty context is valid —
    the reasoning engine proceeds normally if no memory is available.
    """
    items = retrieve_for_context(tenant_id=tenant_id, domain=domain)

    if items:
        logger.debug(
            "PEM context assembled for tenant %s: %d items (domain=%s)",
            tenant_id, len(items), domain,
        )
    else:
        logger.debug("PEM context empty for tenant %s (domain=%s)", tenant_id, domain)

    return MemoryContext(
        tenant_id=tenant_id,
        scenario_type=scenario_type,
        domain=domain,
        items=items,
    )
