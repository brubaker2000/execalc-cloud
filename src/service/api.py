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

# Integrations
from src.service.integrations.bootstrap import default_registry
from src.service.integrations.connector import ConnectorContext
from src.service.integrations.policy import ConnectorPolicy, ConnectorPolicyError
from src.service.integrations.registry import ConnectorRegistryError


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

_CONNECTOR_REGISTRY = default_registry()
_CONNECTOR_POLICY = ConnectorPolicy.from_env()


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


def _connector_ctx_from_body(body: dict) -> ConnectorContext:
    tenant_id = body.get("tenant_id")
    if not tenant_id or not isinstance(tenant_id, str):
        raise ValueError("tenant_id is required")

    actor_id = body.get("actor_id")
    if actor_id is not None and not isinstance(actor_id, str):
        raise ValueError("actor_id must be a string")

    scopes = body.get("scopes")
    if scopes is not None:
        if not isinstance(scopes, list) or not all(isinstance(x, str) for x in scopes):
            raise ValueError("scopes must be a list of strings")

    return ConnectorContext(tenant_id=tenant_id, actor_id=actor_id, scopes=scopes)


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


@app.get("/integrations")
def list_integrations():
    """
    If tenant_id is provided, returns only connectors enabled for that tenant.
    Otherwise returns all available connectors (for ops/diagnostics use).
    """
    available = list(_CONNECTOR_REGISTRY.list())
    tenant_id = request.args.get("tenant_id")

    if tenant_id:
        if not isinstance(tenant_id, str):
            return {"ok": False, "error": "tenant_id must be a string"}, 400
        try:
            allowed = _CONNECTOR_POLICY.allowed_connectors(tenant_id, available)
            return {"ok": True, "connectors": allowed}
        except ConnectorPolicyError as e:
            return {"ok": False, "error": str(e)}, 500

    return {"ok": True, "connectors": available}


@app.post("/integrations/<name>/healthcheck")
def connector_healthcheck(name: str):
    body = request.get_json(force=True, silent=False) or {}

    try:
        ctx = _connector_ctx_from_body(body)
    except ValueError as e:
        return {"ok": False, "error": str(e)}, 400

    try:
        connector = _CONNECTOR_REGISTRY.get(name)
    except ConnectorRegistryError as e:
        return {"ok": False, "error": str(e)}, 404

    try:
        _CONNECTOR_POLICY.authorize_or_raise(name, ctx, _CONNECTOR_REGISTRY.list())
    except ConnectorPolicyError as e:
        return {"ok": False, "error": str(e)}, 500
    except PermissionError as e:
        return {"ok": False, "error": str(e)}, 403

    data = connector.healthcheck(ctx)
    return {"ok": True, "data": data}


@app.post("/integrations/<name>/fetch")
def connector_fetch(name: str):
    body = request.get_json(force=True, silent=False) or {}

    try:
        ctx = _connector_ctx_from_body(body)
    except ValueError as e:
        return {"ok": False, "error": str(e)}, 400

    query = body.get("query") or {}
    if not isinstance(query, dict):
        return {"ok": False, "error": "query must be an object"}, 400

    try:
        connector = _CONNECTOR_REGISTRY.get(name)
    except ConnectorRegistryError as e:
        return {"ok": False, "error": str(e)}, 404

    try:
        _CONNECTOR_POLICY.authorize_or_raise(name, ctx, _CONNECTOR_REGISTRY.list())
    except ConnectorPolicyError as e:
        return {"ok": False, "error": str(e)}, 500
    except PermissionError as e:
        return {"ok": False, "error": str(e)}, 403

    data = connector.fetch(ctx, query)
    return {"ok": True, "data": data}


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="127.0.0.1", port=port, debug=True)
