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
