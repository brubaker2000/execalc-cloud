"""
Postgres DB helpers (Cloud SQL via local proxy or Cloud Run connector)

This module is intentionally minimal:
- One connection factory
- One insert function for execution_records

All configuration comes from environment variables.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict
from typing import Any, Dict, Optional

import psycopg2
from psycopg2.extras import Json


def _env(name: str, default: Optional[str] = None) -> str:
    val = os.getenv(name, default)
    if val is None or val == "":
        raise RuntimeError(f"Missing required environment variable: {name}")
    return val


def get_conn():
    """
    Connect to Postgres using env vars.

    Required:
      EXECALC_DB_HOST
      EXECALC_DB_NAME
      EXECALC_DB_USER
      EXECALC_DB_PASSWORD

    Optional:
      EXECALC_DB_PORT (default 5432)
    """
    host = _env("EXECALC_DB_HOST")
    dbname = _env("EXECALC_DB_NAME")
    user = _env("EXECALC_DB_USER")
    password = _env("EXECALC_DB_PASSWORD")
    port = int(os.getenv("EXECALC_DB_PORT", "5432"))

    return psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password,
    )


def insert_execution_record(
    *,
    tenant_id: str,
    envelope_id: str,
    result: Dict[str, Any],
) -> None:
    """
    Persist a single ExecutionRecord payload to Postgres.

    The DB schema enforces tenant_id FK integrity and (tenant_id, envelope_id) uniqueness.
    """
    ok = bool(result.get("ok"))

    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO execution_records (tenant_id, envelope_id, ok, result)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (tenant_id, envelope_id) DO NOTHING
                """,
                (tenant_id, envelope_id, ok, Json(result)),
            )
    finally:
        conn.close()


def get_execution_record(*, tenant_id: str, envelope_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a single execution record by (tenant_id, envelope_id).
    Returns None if not found.
    """
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                """
                SELECT tenant_id, envelope_id, ok, result, created_at
                FROM execution_records
                WHERE tenant_id = %s AND envelope_id = %s
                """,
                (tenant_id, envelope_id),
            )
            row = cur.fetchone()
            if not row:
                return None
            t_id, e_id, ok, result, created_at = row
            return {
                "tenant_id": t_id,
                "envelope_id": e_id,
                "ok": bool(ok),
                "result": result,
                "created_at": created_at.isoformat(),
            }
    finally:
        conn.close()


def upsert_tenant(*, tenant_id: str, tenant_name: str) -> None:
    """
    Ensure a tenant row exists in Postgres.

    This prevents FK failures when persisting execution_records.
    """
    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO tenants (tenant_id, tenant_name, created_at)
                VALUES (%s, %s, now())
                ON CONFLICT (tenant_id) DO UPDATE
                SET tenant_name = EXCLUDED.tenant_name
                """,
                (tenant_id, tenant_name),
            )
    finally:
        conn.close()
