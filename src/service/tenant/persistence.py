"""
Tenant Persistence Service

Mutation-only layer.
Validation happens upstream.
"""

import sqlite3
from typing import Dict, Any


class TenantPersistenceError(Exception):
    pass


DB_PATH = "src/service/tenant/tenant.db"


def persist_tenant(validated_payload: Dict[str, Any]) -> Dict[str, Any]:
    required_fields = ["tenant_id", "tenant_name"]
    missing = [f for f in required_fields if f not in validated_payload]
    if missing:
        raise TenantPersistenceError(f"Missing fields: {missing}")

    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO tenants (
                tenant_id,
                name
            )
            VALUES (?, ?)
            """,
            (
                validated_payload["tenant_id"],
                validated_payload["tenant_name"],
            ),
        )

        conn.commit()

        return {
            "status": "persisted",
            "tenant_id": validated_payload["tenant_id"],
        }

    except sqlite3.IntegrityError as e:
        raise TenantPersistenceError(str(e))

    finally:
        if conn:
            conn.close()
