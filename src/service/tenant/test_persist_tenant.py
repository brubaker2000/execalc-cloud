import os
import sqlite3
import tempfile
import unittest

from src.service.tenant.errors import TenantAlreadyExists
from src.service.tenant.persistence import create_tenant, get_tenant


class TestTenantPersistence(unittest.TestCase):
    def setUp(self):
        # Create a temp SQLite DB file and force persistence layer to use it.
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.tmp.close()
        os.environ["TENANTS_DB_PATH"] = self.tmp.name

        # Create schema in the temp DB.
        conn = sqlite3.connect(self.tmp.name)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tenants (
                tenant_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )
        conn.commit()
        conn.close()

    def tearDown(self):
        # Clean up temp DB.
        try:
            os.remove(self.tmp.name)
        except Exception:
            pass
        os.environ.pop("TENANTS_DB_PATH", None)

    def test_create_and_get_tenant(self):
        create_tenant("tenant-1", "Tenant One", "active", "2026-01-01T00:00:00Z")
        row = get_tenant("tenant-1")
        self.assertEqual(row[0], "tenant-1")
        self.assertEqual(row[1], "Tenant One")
        self.assertEqual(row[2], "active")
        self.assertEqual(row[3], "2026-01-01T00:00:00Z")

    def test_duplicate_tenant_raises(self):
        create_tenant("tenant-1", "Tenant One", "active", "2026-01-01T00:00:00Z")
        with self.assertRaises(TenantAlreadyExists):
            create_tenant("tenant-1", "Tenant One Again", "active", "2026-01-01T00:00:00Z")


if __name__ == "__main__":
    unittest.main()
