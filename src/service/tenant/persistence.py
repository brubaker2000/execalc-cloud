import os
import sqlite3

# Always write to the tenant DB inside this package directory (never repo root).
DB_PATH = os.path.join(os.path.dirname(__file__), "tenants.db")

def create_tenant(tenant_id, name, status, created_at):
    # Short timeout + explicit close prevents most Cloud Shell lock hiccups.
    conn = sqlite3.connect(DB_PATH, timeout=10)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tenants (tenant_id, name, status, created_at) VALUES (?, ?, ?, ?)",
            (tenant_id, name, status, created_at),
        )
        conn.commit()
    finally:
        conn.close()

def get_tenant(tenant_id: str):
    conn = sqlite3.connect(DB_PATH, timeout=10)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT tenant_id, name, status, created_at FROM tenants WHERE tenant_id = ?",
            (tenant_id,),
        )
        row = cursor.fetchone()
        return row
    finally:
        conn.close()
