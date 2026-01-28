import unittest

from src.service.tenant.actor_context import set_actor_context, clear_actor_context
from src.service.tenant.authz import assert_actor_has_permission, assert_actor_role_in
from src.service.tenant.errors import Unauthorized


class TestAuthz(unittest.TestCase):
    def tearDown(self):
        try:
            clear_actor_context()
        except Exception:
            pass

    def test_admin_can_write(self):
        set_actor_context(user_id="u1", role="admin")
        assert_actor_has_permission("tenant:write")  # should not raise

    def test_viewer_cannot_write(self):
        set_actor_context(user_id="u2", role="viewer")
        with self.assertRaises(Unauthorized):
            assert_actor_has_permission("tenant:write")

    def test_unknown_role_denied(self):
        set_actor_context(user_id="u3", role="weird_role")
        with self.assertRaises(Unauthorized):
            assert_actor_has_permission("tenant:read")

    def test_role_whitelist(self):
        set_actor_context(user_id="u4", role="operator")
        assert_actor_role_in(["admin", "operator"])  # should not raise
        with self.assertRaises(Unauthorized):
            assert_actor_role_in(["admin"])  # operator not allowed


if __name__ == "__main__":
    unittest.main()
