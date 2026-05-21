from __future__ import annotations

import dataclasses
import logging
import uuid
from datetime import UTC, datetime
from typing import Dict, List, Optional

from src.service.qualitative_capture.deconstructor import deconstruct_event
from src.service.qualitative_capture.models import AtomicNugget, ConversationEvent
from src.service.qualitative_capture.repository import (
    insert_audit_event,
    insert_nugget,
    list_rail_artifacts_pending_deconstruction,
    mark_artifact_deconstructed,
    update_artifact_deconstruction_status,
)

logger = logging.getLogger(__name__)

_MEMORIALIZED_CONFIDENCE = 0.91
_MEMORIALIZED_CONFIDENCE_LEVEL = "strong"
_MACHINE_CONFIDENCE = 0.72
_MACHINE_CONFIDENCE_LEVEL = "developing"

# Synthetic author injected on the event so deconstructor has a valid user_id
_SYNTHETIC_USER_ID = "system:second_order"
_SYNTHETIC_ROLE = "system"


def process_pending_artifacts(
    *,
    tenant_id: str,
    batch_size: int = 10,
) -> Dict:
    """
    Run one batch of second-order deconstruction for a tenant.

    Picks up to batch_size artifacts in 'pending' status, ordered by actioned_at
    (oldest first).  Each artifact is converted into a synthetic ConversationEvent
    and run through the standard deconstructor.  Resulting nuggets receive
    generation_depth=2 and a confidence floor derived from is_memorialized.

    Returns a summary dict: {processed, nuggets_created, skipped, failed}.
    Depth limit is enforced at artifact creation time — this worker never writes
    generation_depth > 2 and rail artifacts derived from depth-2 nuggets should
    not be queued for second-order deconstruction.
    """
    summary: Dict[str, int] = {
        "processed": 0,
        "nuggets_created": 0,
        "skipped": 0,
        "failed": 0,
    }

    try:
        artifacts = list_rail_artifacts_pending_deconstruction(
            tenant_id=tenant_id, limit=batch_size
        )
    except Exception:
        logger.exception(
            "second_order: failed to load pending artifacts for tenant %s", tenant_id
        )
        return summary

    for artifact in artifacts:
        artifact_id = artifact["artifact_id"]
        try:
            _process_artifact(artifact, tenant_id, summary)
        except Exception:
            logger.exception(
                "second_order: unhandled error for artifact %s tenant %s",
                artifact_id, tenant_id,
            )
            try:
                update_artifact_deconstruction_status(
                    artifact_id=artifact_id, tenant_id=tenant_id, new_status="pending"
                )
            except Exception:
                pass
            summary["failed"] += 1

    return summary


def _process_artifact(artifact: Dict, tenant_id: str, summary: Dict) -> None:
    artifact_id = artifact["artifact_id"]

    update_artifact_deconstruction_status(
        artifact_id=artifact_id, tenant_id=tenant_id, new_status="in_progress"
    )
    _audit(
        tenant_id=tenant_id,
        event_kind="artifact.deconstruction_started",
        source_object_type="rail_artifact",
        source_object_id=artifact_id,
    )

    nuggets = _deconstruct_one_artifact(artifact)

    if not nuggets:
        update_artifact_deconstruction_status(
            artifact_id=artifact_id, tenant_id=tenant_id, new_status="skipped"
        )
        _audit(
            tenant_id=tenant_id,
            event_kind="artifact.deconstruction_skipped",
            source_object_type="rail_artifact",
            source_object_id=artifact_id,
            payload={"reason": "no_claims_detected"},
        )
        summary["skipped"] += 1
        return

    nugget_ids: List[str] = []
    for nugget in nuggets:
        try:
            insert_nugget(nugget)
            nugget_ids.append(nugget.nugget_id)
            _audit(
                tenant_id=tenant_id,
                event_kind="nugget.created",
                source_object_type="rail_artifact",
                source_object_id=artifact_id,
                payload={"nugget_id": nugget.nugget_id, "claim_type": nugget.claim_type},
            )
            summary["nuggets_created"] += 1
        except Exception:
            logger.exception(
                "second_order: insert_nugget failed for artifact %s", artifact_id
            )

    mark_artifact_deconstructed(
        artifact_id=artifact_id, tenant_id=tenant_id, nugget_ids=nugget_ids
    )
    _audit(
        tenant_id=tenant_id,
        event_kind="artifact.deconstruction_complete",
        source_object_type="rail_artifact",
        source_object_id=artifact_id,
        payload={"nugget_count": len(nugget_ids)},
    )
    summary["processed"] += 1


def _deconstruct_one_artifact(artifact: Dict) -> List[AtomicNugget]:
    """
    Convert a rail artifact into generation_depth=2 nuggets.

    Wraps the artifact_text in a synthetic ConversationEvent so the standard
    deconstructor can run unchanged.  Each resulting nugget is patched with
    second-order metadata via dataclasses.replace (the model is frozen).
    """
    is_memorialized = bool(artifact.get("is_memorialized"))
    confidence_score = _MEMORIALIZED_CONFIDENCE if is_memorialized else _MACHINE_CONFIDENCE
    confidence_level = _MEMORIALIZED_CONFIDENCE_LEVEL if is_memorialized else _MACHINE_CONFIDENCE_LEVEL

    synthetic_event = ConversationEvent(
        event_id=uuid.uuid4().hex,
        tenant_id=artifact["tenant_id"],
        session_id=artifact["session_id"],
        user_id=_SYNTHETIC_USER_ID,
        role=_SYNTHETIC_ROLE,
        message_text=artifact["artifact_text"],
        created_at=datetime.now(UTC),
    )

    first_pass = deconstruct_event(synthetic_event)

    return [
        dataclasses.replace(
            n,
            generation_depth=2,
            selection_method="second_order",
            source_rail_artifact_id=artifact["artifact_id"],
            confidence_score=confidence_score,
            confidence_level=confidence_level,
        )
        for n in first_pass
    ]


def _audit(
    *,
    tenant_id: str,
    event_kind: str,
    source_object_type: Optional[str] = None,
    source_object_id: Optional[str] = None,
    payload: Optional[Dict] = None,
) -> None:
    try:
        insert_audit_event(
            audit_id=uuid.uuid4().hex,
            tenant_id=tenant_id,
            event_kind=event_kind,
            source_object_type=source_object_type,
            source_object_id=source_object_id,
            payload=payload or {},
        )
    except Exception:
        logger.warning(
            "second_order: audit write failed for event_kind %s", event_kind
        )
