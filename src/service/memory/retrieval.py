from __future__ import annotations

import logging
from typing import List, Optional

from src.service.memory.models import MemoryObject
from src.service.memory.repository import db_list

logger = logging.getLogger(__name__)

_MAX_CONTEXT_ITEMS = 20


def retrieve_for_context(
    *,
    tenant_id: str,
    domain: Optional[str] = None,
    limit: int = _MAX_CONTEXT_ITEMS,
) -> List[MemoryObject]:
    """
    Retrieve active memory objects for upstream context assembly.

    V1.0 strategy: deterministic — fetch active objects, filter by domain,
    rank by confidence descending then recency. No semantic ranking yet.
    """
    limit = min(limit, _MAX_CONTEXT_ITEMS)

    try:
        items = db_list(
            tenant_id=tenant_id,
            activation_state="active",
            domain=domain,
            limit=limit,
        )
    except Exception:
        logger.exception("PEM retrieval failed for tenant %s domain %s", tenant_id, domain)
        return []

    return items
