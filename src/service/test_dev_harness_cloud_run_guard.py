import importlib
import os
import sys


def _clear_api_module():
    sys.modules.pop("src.service.api", None)


def _restore_env(key: str, old_value: str | None):
    if old_value is None:
        os.environ.pop(key, None)
    else:
        os.environ[key] = old_value


def test_cloud_run_rejects_dev_harness_enabled():
    old_ks = os.environ.get("K_SERVICE")
    old_h = os.environ.get("EXECALC_DEV_HARNESS")
    try:
        os.environ["K_SERVICE"] = "execalc-api"
        os.environ["EXECALC_DEV_HARNESS"] = "1"
        _clear_api_module()

        try:
            importlib.import_module("src.service.api")
            assert False, "Expected RuntimeError when dev harness is enabled on Cloud Run"
        except RuntimeError as e:
            assert "EXECALC_DEV_HARNESS must be disabled on Cloud Run" in str(e)
    finally:
        _restore_env("K_SERVICE", old_ks)
        _restore_env("EXECALC_DEV_HARNESS", old_h)
        _clear_api_module()


def test_cloud_run_allows_dev_harness_disabled():
    old_ks = os.environ.get("K_SERVICE")
    old_h = os.environ.get("EXECALC_DEV_HARNESS")
    try:
        os.environ["K_SERVICE"] = "execalc-api"
        os.environ["EXECALC_DEV_HARNESS"] = "0"
        _clear_api_module()

        importlib.import_module("src.service.api")
    finally:
        _restore_env("K_SERVICE", old_ks)
        _restore_env("EXECALC_DEV_HARNESS", old_h)
        _clear_api_module()
