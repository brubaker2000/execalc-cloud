import logging
import os

from flask import Flask, jsonify, request

from src.service.ingress_runner import execute_ingress
from src.service.tenant.errors import InvalidTenantPayload

# Optional DB persistence (enabled via env var)
try:
    from src.service.db.postgres import insert_execution_record
except Exception:
    insert_execution_record = None  # type: ignore


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


def _persist_enabled() -> bool:
    return os.getenv("EXECALC_PERSIST_EXECUTIONS", "0").strip().lower() in ("1", "true", "yes", "on")


def _persist_execution(record) -> dict:
    """
    Best-effort persistence. Never breaks the request path unless you explicitly want it to.
    """
    if not _persist_enabled():
        return {"persisted": False}

    if insert_execution_record is None:
        return {"persisted": False, "persist_error": "db module not available"}

    try:
        insert_execution_record(
            tenant_id=record.tenant_id,
            envelope_id=record.envelope_id,
            result=record.result,
        )
        return {"persisted": True}
    except Exception as e:
        logging.exception("Failed to persist execution record")
        return {"persisted": False, "persist_error": str(e)}


@app.route("/status", methods=["GET"])
def status():
    logging.info("Received status request")

    tenant_id = request.args.get("tenant_id") or "tenant_test_001"
    raw_input = {"tenant_id": tenant_id}

    try:
        record = execute_ingress(
            raw_input,
            user_id="u1",
            role="viewer",
            fn=lambda: {"status": "OK"},
        )
    except InvalidTenantPayload as e:
        return jsonify({"ok": False, "error_type": "InvalidTenantPayload", "error": str(e)}), 400
    except Exception as e:
        logging.exception("Unhandled error in /status")
        return jsonify({"ok": False, "error_type": e.__class__.__name__, "error": str(e)}), 500

    response = {
        "tenant_id": record.tenant_id,
        "envelope_id": record.envelope_id,
        **record.result,
        **_persist_execution(record),
    }
    status_code = 200 if response.get("ok") else 400
    return jsonify(response), status_code


@app.route("/ingress", methods=["POST"])
def ingress():
    raw_input = request.get_json(silent=True) or {}

    try:
        record = execute_ingress(
            raw_input,
            user_id="u1",
            role="viewer",
            fn=lambda: {"received": True},
        )
    except InvalidTenantPayload as e:
        return jsonify({"ok": False, "error_type": "InvalidTenantPayload", "error": str(e)}), 400
    except Exception as e:
        logging.exception("Unhandled error in /ingress")
        return jsonify({"ok": False, "error_type": e.__class__.__name__, "error": str(e)}), 500

    response = {
        "tenant_id": record.tenant_id,
        "envelope_id": record.envelope_id,
        **record.result,
        **_persist_execution(record),
    }
    status_code = 200 if response.get("ok") else 400
    return jsonify(response), status_code


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="127.0.0.1", port=port, debug=True)
