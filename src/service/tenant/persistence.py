import os
import sqlite3

from src.service.tenant.errors import TenantAlreadyExists

# Always write to the tenant DB inside this package directory (never repo root).
DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), "tenants.db")


def _db_path() -> str:
    return os.environ.get("TENANTS_DB_PATH") or DEFAULT_DB_PATH


def _ensure_schema(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS tenants (
            tenant_id   TEXT PRIMARY KEY,
            name        TEXT NOT NULL,
            status      TEXT NOT NULL,
            created_at  TEXT NOT NULL
        );
        '''
    )
    conn.commit()


def _connect() -> sqlite3.Connection:
    path = _db_path()

    # If TENANTS_DB_PATH points to a file in a non-existent directory, create it.
    if path != ":memory:":
        d = os.path.dirname(path)
        if d:
            os.makedirs(d, exist_ok=True)

    conn = sqlite3.connect(path, timeout=10)
    _ensure_schema(conn)
    return conn


def create_tenant(tenant_id: str, name: str, status: str, created_at: str) -> None:
    conn = _connect()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tenants (tenant_id, name, status, created_at) VALUES (?, ?, ?, ?)",
            (tenant_id, name, status, created_at),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise TenantAlreadyExists(f"Tenant ID {tenant_id} already exists.")
    finally:
        conn.close()


def get_tenant(tenant_id: str):
    conn = _connect()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT tenant_id, name, status, created_at FROM tenants WHERE tenant_id = ?",
            (tenant_id,),
        )
        return cursor.fetchone()
    finally:
        conn.close()
