from __future__ import annotations

import argparse
import logging
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from src.service.db.postgres import get_conn
from src.service.decision_loop.models import DecisionReport, SensitivityVariable
from src.service.gaqp.corpus import insert_claims
from src.service.gaqp.extraction import extract_claims

logger = logging.getLogger(__name__)

_DEFAULT_BATCH_SIZE = 50


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------

@dataclass
class BackfillSummary:
    records_read: int = 0
    records_skipped: int = 0     # missing payload or reconstruction error
    claims_extracted: int = 0
    claims_inserted: int = 0
    claims_skipped: int = 0      # duplicate fingerprint — idempotent
    claims_failed: int = 0
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "records_read": self.records_read,
            "records_skipped": self.records_skipped,
            "claims_extracted": self.claims_extracted,
            "claims_inserted": self.claims_inserted,
            "claims_skipped": self.claims_skipped,
            "claims_failed": self.claims_failed,
            "errors": self.errors,
        }


# ---------------------------------------------------------------------------
# Report reconstruction
# ---------------------------------------------------------------------------

def _report_from_dict(result: Dict[str, Any]) -> DecisionReport:
    """
    Reconstruct a DecisionReport from the execution_records.result payload.

    result["report"] holds report fields; result["audit"] holds the audit dict.
    Missing fields fall back to safe empty values so older records reconstruct cleanly.
    """
    report_dict = result.get("report") or {}
    audit = result.get("audit") or {}

    sensitivity_raw = report_dict.get("sensitivity") or []
    sensitivity = [
        SensitivityVariable(name=s["name"], impact=s["impact"])
        for s in sensitivity_raw
        if isinstance(s, dict) and "name" in s and "impact" in s
    ]

    return DecisionReport(
        executive_summary=str(report_dict.get("executive_summary") or ""),
        confidence=report_dict.get("confidence") or "unknown",
        confidence_rationale=list(report_dict.get("confidence_rationale") or []),
        governing_objective=str(report_dict.get("governing_objective") or ""),
        tradeoffs=dict(report_dict.get("tradeoffs") or {}),
        sensitivity=sensitivity,
        next_actions=list(report_dict.get("next_actions") or []),
        audit=audit,
        value_assessment=str(report_dict.get("value_assessment") or ""),
        risk_reward_assessment=str(report_dict.get("risk_reward_assessment") or ""),
        supply_demand_assessment=str(report_dict.get("supply_demand_assessment") or ""),
        asset_assessment=str(report_dict.get("asset_assessment") or ""),
        liability_assessment=str(report_dict.get("liability_assessment") or ""),
        actors=list(report_dict.get("actors") or []),
        incentives=list(report_dict.get("incentives") or []),
        asymmetries=list(report_dict.get("asymmetries") or []),
        execution_trace=dict(report_dict.get("execution_trace") or {}),
    )


# ---------------------------------------------------------------------------
# DB fetch
# ---------------------------------------------------------------------------

def _fetch_page(
    *,
    conn: Any,
    after_record_id: int,
    tenant_id: Optional[str],
    batch_size: int,
) -> List[Tuple[int, str, str, Dict[str, Any]]]:
    """
    Fetch one page of execution_records with full result payload.

    Uses record_id as a forward cursor — stable and index-friendly.
    Only ok=true records are included (failed runs produce no useful reports).
    Returns list of (record_id, tenant_id, envelope_id, result).
    """
    if tenant_id:
        sql = """
            SELECT record_id, tenant_id, envelope_id, result
            FROM execution_records
            WHERE ok = true AND record_id > %s AND tenant_id = %s
            ORDER BY record_id ASC
            LIMIT %s
        """
        params: tuple = (after_record_id, tenant_id, batch_size)
    else:
        sql = """
            SELECT record_id, tenant_id, envelope_id, result
            FROM execution_records
            WHERE ok = true AND record_id > %s
            ORDER BY record_id ASC
            LIMIT %s
        """
        params = (after_record_id, batch_size)

    with conn.cursor() as cur:
        cur.execute(sql, params)
        rows = cur.fetchall() or []
    return [(int(r[0]), str(r[1]), str(r[2]), r[3]) for r in rows]


# ---------------------------------------------------------------------------
# Main backfill
# ---------------------------------------------------------------------------

def run_backfill(
    *,
    tenant_id: Optional[str] = None,
    batch_size: int = _DEFAULT_BATCH_SIZE,
    dry_run: bool = False,
    limit: Optional[int] = None,
) -> BackfillSummary:
    """
    Backfill GAQP corpus from existing execution_records.

    Reads ok=true records in ascending record_id order, reconstructs
    DecisionReport, runs Stage 9B extraction, and persists admitted claims
    via Stage 9C corpus persistence.

    Fingerprint idempotency makes this safe to run multiple times.
    Per-record errors are isolated — a bad record is skipped, not fatal.
    """
    summary = BackfillSummary()
    conn = get_conn()
    cursor = 0

    try:
        while True:
            page = _fetch_page(
                conn=conn,
                after_record_id=cursor,
                tenant_id=tenant_id,
                batch_size=batch_size,
            )
            if not page:
                break

            for record_id, t_id, envelope_id, result in page:
                if limit is not None and summary.records_read >= limit:
                    break

                summary.records_read += 1
                cursor = record_id

                if not result or "report" not in result:
                    summary.records_skipped += 1
                    continue

                try:
                    report = _report_from_dict(result)
                except Exception as exc:
                    summary.records_skipped += 1
                    msg = f"{envelope_id}: reconstruction failed — {exc}"
                    summary.errors.append(msg)
                    logger.warning(msg)
                    continue

                try:
                    claims = extract_claims(
                        report=report,
                        tenant_id=t_id,
                        source_envelope_id=envelope_id,
                        actor_id="backfill",
                    )
                except Exception as exc:
                    summary.records_skipped += 1
                    msg = f"{envelope_id}: extraction failed — {exc}"
                    summary.errors.append(msg)
                    logger.warning(msg)
                    continue

                summary.claims_extracted += len(claims)

                if dry_run:
                    admitted = [c for c in claims if c.admission_status == "admitted"]
                    summary.claims_inserted += len(admitted)
                    continue

                try:
                    insert_summary = insert_claims(claims)
                    summary.claims_inserted += insert_summary.inserted
                    summary.claims_skipped += insert_summary.skipped
                    summary.claims_failed += insert_summary.failed
                except Exception as exc:
                    msg = f"{envelope_id}: persistence failed — {exc}"
                    summary.errors.append(msg)
                    logger.warning(msg)

            if limit is not None and summary.records_read >= limit:
                break

    finally:
        conn.close()

    return summary


# ---------------------------------------------------------------------------
# CLI entrypoint
# ---------------------------------------------------------------------------

def _build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="backfill",
        description="Backfill GAQP corpus from existing execution_records.",
    )
    p.add_argument(
        "--tenant-id",
        default=None,
        help="Restrict backfill to a single tenant. Default: all tenants.",
    )
    p.add_argument(
        "--batch-size",
        type=int,
        default=_DEFAULT_BATCH_SIZE,
        help=f"Records per DB fetch. Default: {_DEFAULT_BATCH_SIZE}.",
    )
    p.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Max records to process. Default: unlimited.",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Extract and count claims but do not write to corpus.",
    )
    p.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
    )
    return p


if __name__ == "__main__":
    args = _build_arg_parser().parse_args()
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s %(levelname)s %(name)s — %(message)s",
    )

    summary = run_backfill(
        tenant_id=args.tenant_id,
        batch_size=args.batch_size,
        dry_run=args.dry_run,
        limit=args.limit,
    )

    print(f"records_read:      {summary.records_read}")
    print(f"records_skipped:   {summary.records_skipped}")
    print(f"claims_extracted:  {summary.claims_extracted}")
    print(f"claims_inserted:   {summary.claims_inserted}")
    print(f"claims_skipped:    {summary.claims_skipped}")
    print(f"claims_failed:     {summary.claims_failed}")
    if summary.errors:
        print(f"errors ({len(summary.errors)}):")
        for e in summary.errors:
            print(f"  {e}")

    sys.exit(1 if summary.claims_failed else 0)
