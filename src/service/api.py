import logging
import os

from flask import Flask, jsonify, request

from src.service.auth.claims import AuthError, VerifiedClaims, claims_from_request

from src.service.ingress_runner import execute_ingress
from src.service.tenant.errors import InvalidTenantPayload
from src.service.tenant.registry import ensure_tenant_registered, enforcement_enabled

# Optional DB persistence (enabled via env var)
try:
    from src.service.db.postgres import get_conn, insert_execution_record, get_execution_record, upsert_tenant
except Exception:
    get_conn = None  # type: ignore
    insert_execution_record = None  # type: ignore
    get_execution_record = None  # type: ignore

# Integrations
from src.service.integrations.bootstrap import default_registry
from src.service.integrations.connector import ConnectorContext
from src.service.integrations.policy import ConnectorPolicy, ConnectorPolicyError
from src.service.integrations.credentials import EnvCredentialStore, CredentialStoreError, CredentialRequirementPolicy
from src.service.integrations.registry import ConnectorRegistryError


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

_CONNECTOR_REGISTRY = default_registry()
_CONNECTOR_POLICY = ConnectorPolicy.from_env()

_CREDENTIAL_STORE_ERROR = None
try:
    _CREDENTIAL_STORE = EnvCredentialStore.from_env()
except CredentialStoreError as e:
    logging.exception("Failed to load credential store from env")
    _CREDENTIAL_STORE = None
    _CREDENTIAL_STORE_ERROR = str(e)
except Exception as e:
    logging.exception("Failed to load credential store from env")
    _CREDENTIAL_STORE = None
    _CREDENTIAL_STORE_ERROR = f"unexpected_error: {e}"

_CREDENTIAL_REQ_POLICY_ERROR = None
try:
    _CREDENTIAL_REQ_POLICY = CredentialRequirementPolicy.from_env()
except CredentialStoreError as e:
    logging.exception("Failed to load credential requirement policy from env")
    _CREDENTIAL_REQ_POLICY = CredentialRequirementPolicy(required_by_tenant=None)
    _CREDENTIAL_REQ_POLICY_ERROR = str(e)
except Exception as e:
    logging.exception("Failed to load credential requirement policy from env")
    _CREDENTIAL_REQ_POLICY = CredentialRequirementPolicy(required_by_tenant=None)
    _CREDENTIAL_REQ_POLICY_ERROR = f"unexpected_error: {e}"




def _dev_harness_enabled() -> bool:
    return os.getenv("EXECALC_DEV_HARNESS", "0").strip().lower() in ("1", "true", "yes", "on")


def _require_dev_harness():
    if not _dev_harness_enabled():
        return False, ({"ok": False, "error": "forbidden"}, 403)
    return True, None

def _claims_or_denial():
    """Return (claims, denial) where denial is a (payload, status) tuple."""
    try:
        return claims_from_request(request), None
    except AuthError as e:
        return None, ({"ok": False, "error": str(e)}, 403)


def _persist_enabled() -> bool:
    return os.getenv("EXECALC_PERSIST_EXECUTIONS", "0").strip().lower() in ("1", "true", "yes", "on")


def _persist_execution(record) -> dict:
    """
    Best-effort persistence. Never breaks the request path unless you explicitly want it to.
    """
    if not _persist_enabled():
        return {"persisted": False}

    if insert_execution_record is None:
        return {"persisted": False, "persist_table": "execution_records", "persist_error": "db module not available"}

    try:
        # If canonical tenant registry enforcement is enabled, persistence must not create tenants.
        if enforcement_enabled():
            ensure_tenant_registered(record.tenant_id)
        else:
            # Enforcement disabled: best-effort ensure tenant exists to satisfy FK.
            upsert_tenant(tenant_id=record.tenant_id, tenant_name=record.tenant_id)

        insert_execution_record(
            tenant_id=record.tenant_id,
            envelope_id=record.envelope_id,
            result=record.result,
        )
        return {"persisted": True, "persist_table": "execution_records"}

    except Exception as e:
        logging.exception("Failed to persist execution record")
        return {"persisted": False, "persist_table": "execution_records", "persist_error": str(e)}



def _enforce_tenant_access(required_tenant_id: str):
    """
    DEV HARNESS ONLY.
    In production, tenant and role must come from real auth (session/JWT/IAP), not headers.
    """
    hdr_tenant = request.headers.get("X-Tenant-Id")
    role = (request.headers.get("X-Role") or "").strip().lower()

    if not hdr_tenant or hdr_tenant != required_tenant_id:
        return False, ({"ok": False, "error": "forbidden"}, 403)

    if role not in ("admin", "operator"):
        return False, ({"ok": False, "error": "forbidden"}, 403)

    return True, None


def _connector_ctx_from_body(body: dict, claims: VerifiedClaims) -> ConnectorContext:
    """Build ConnectorContext from verified claims + sanitized request body."""
    tenant_id = claims.tenant_id
    if not tenant_id:
        raise ValueError("tenant_id claim is required")

    body_tenant = body.get("tenant_id")
    if body_tenant is not None and not isinstance(body_tenant, str):
        raise ValueError("tenant_id must be a string")
    if body_tenant and body_tenant != tenant_id:
        raise ValueError("tenant_id mismatch (claims vs body)")

    body_actor = body.get("actor_id")
    if body_actor is not None and not isinstance(body_actor, str):
        raise ValueError("actor_id must be a string")
    if body_actor and body_actor != claims.user_id:
        raise ValueError("actor_id mismatch (claims vs body)")

    if "scopes" in body:
        raise ValueError("scopes must not be provided in request body; use X-Scopes header")

    return ConnectorContext(tenant_id=tenant_id, actor_id=claims.user_id, scopes=claims.scopes)



def _require_credentials_or_error(connector_name: str, ctx: ConnectorContext):
    """Enforce per-tenant credential requirements for a connector.

    Returns None if allowed, otherwise returns a (payload, http_status) tuple.
    """
    try:
        required = _CREDENTIAL_REQ_POLICY.requires_credentials(ctx.tenant_id, connector_name)
    except Exception as e:
        logging.exception("Credential requirement evaluation failed")
        return {"ok": False, "error": f"credential_requirement_eval_failed: {e}"}, 500

    if not required:
        return None

    if _CREDENTIAL_STORE is None:
        payload = {"ok": False, "error": f"Credentials required for '{connector_name}' but credential store unavailable"}
        if _CREDENTIAL_STORE_ERROR:
            payload["credential_store_error"] = _CREDENTIAL_STORE_ERROR
        return payload, 500

    try:
        st = _CREDENTIAL_STORE.status(ctx.tenant_id, connector_name)
    except CredentialStoreError as e:
        return {"ok": False, "error": f"credential_store_error: {e}"}, 500

    if not st.configured:
        return {"ok": False, "error": f"Credentials required for '{connector_name}' but not configured"}, 412

    return None


@app.route("/status", methods=["GET"])
def status():
    logging.info("Received status request")

    allowed, denial = _require_dev_harness()
    if not allowed:
        return denial

    claims, denial = _claims_or_denial()
    if denial:
        return denial

    tenant_q = request.args.get("tenant_id")
    if claims.tenant_id and tenant_q and tenant_q != claims.tenant_id:
        return jsonify({"ok": False, "error_type": "InvalidTenantPayload", "error": "tenant_id mismatch (claims vs query)"}), 400

    tenant_id = claims.tenant_id or tenant_q or "tenant_test_001"
    raw_input = {"tenant_id": tenant_id}

    try:
        record = execute_ingress(
            raw_input,
            user_id=claims.user_id,
            role=claims.role,
            fn=lambda: {"status": "OK"},
            resolved_tenant_id=claims.tenant_id,
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
    allowed, denial = _require_dev_harness()
    if not allowed:
        return denial

    claims, denial = _claims_or_denial()
    if denial:
        return denial

    raw_input = request.get_json(silent=True) or {}

    try:
        record = execute_ingress(
            raw_input,
            user_id=claims.user_id,
            role=claims.role,
            fn=lambda: {"received": True},
            resolved_tenant_id=claims.tenant_id,
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
    If tenant claim is present, returns only connectors enabled for that tenant.
    If tenant claim is NOT present, requires role=admin and returns all connectors (ops/diagnostics).
    """
    allowed, denial = _require_dev_harness()
    if not allowed:
        return denial

    claims, denial = _claims_or_denial()
    if denial:
        return denial

    available = list(_CONNECTOR_REGISTRY.list())

    if claims.tenant_id:
        if claims.role not in ("admin", "operator"):
            return {"ok": False, "error": "forbidden"}, 403
        tenant_id = claims.tenant_id
        try:
            allowed_connectors = _CONNECTOR_POLICY.allowed_connectors(tenant_id, available)

            credentials = {}
            credentials_error = None

            if _CREDENTIAL_STORE is None:
                credentials_error = _CREDENTIAL_STORE_ERROR
            else:
                for cname in allowed_connectors:
                    try:
                        required = _CREDENTIAL_REQ_POLICY.requires_credentials(tenant_id, cname)
                        st = _CREDENTIAL_STORE.status(tenant_id, cname)
                        credentials[cname] = {"configured": st.configured, "required": required}
                    except CredentialStoreError as e:
                        credentials_error = str(e)
                        break

            resp = {"ok": True, "connectors": allowed_connectors, "credentials": credentials}
            if credentials_error:
                resp["credentials_error"] = credentials_error
            return resp

        except ConnectorPolicyError as e:
            return {"ok": False, "error": str(e)}, 500

    if claims.role != "admin":
        return {"ok": False, "error": "forbidden"}, 403

    policy_summary = {
        "allowlist_set": _CONNECTOR_POLICY.allowlist_by_tenant is not None,
        "allowlist_entries": 0 if _CONNECTOR_POLICY.allowlist_by_tenant is None else len(_CONNECTOR_POLICY.allowlist_by_tenant),
        "required_scopes_set": _CONNECTOR_POLICY.required_scopes_by_connector is not None,
        "required_scopes_entries": 0 if _CONNECTOR_POLICY.required_scopes_by_connector is None else len(_CONNECTOR_POLICY.required_scopes_by_connector),
    }
    return {"ok": True, "connectors": available, "policy": policy_summary}


@app.post("/integrations/<name>/healthcheck")
def connector_healthcheck(name: str):
    allowed, denial = _require_dev_harness()
    if not allowed:
        return denial

    claims, denial = _claims_or_denial()
    if denial:
        return denial
    if claims.role not in ("admin", "operator"):
        return {"ok": False, "error": "forbidden"}, 403

    body = request.get_json(force=True, silent=False) or {}

    try:
        ctx = _connector_ctx_from_body(body, claims)
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

    cred_denial = _require_credentials_or_error(name, ctx)
    if cred_denial is not None:
        return cred_denial

    data = connector.healthcheck(ctx)
    return {"ok": True, "data": data}


@app.post("/integrations/<name>/fetch")
def connector_fetch(name: str):
    allowed, denial = _require_dev_harness()
    if not allowed:
        return denial

    claims, denial = _claims_or_denial()
    if denial:
        return denial
    if claims.role not in ("admin", "operator"):
        return {"ok": False, "error": "forbidden"}, 403

    body = request.get_json(force=True, silent=False) or {}

    try:
        ctx = _connector_ctx_from_body(body, claims)
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

    cred_denial = _require_credentials_or_error(name, ctx)
    if cred_denial is not None:
        return cred_denial

    data = connector.fetch(ctx, query)
    return {"ok": True, "data": data}


@app.get("/executions/<envelope_id>")
def get_execution(envelope_id: str):
    """
    Tenant-scoped retrieval of an execution record.
    Requires tenant claim.
    """
    allowed, denial = _require_dev_harness()
    if not allowed:
        return denial

    claims, denial = _claims_or_denial()
    if denial:
        return denial
    if claims.role not in ("admin", "operator"):
        return {"ok": False, "error": "forbidden"}, 403
    if not claims.tenant_id:
        return {"ok": False, "error": "tenant_id claim is required"}, 400

    tenant_id = claims.tenant_id

    if get_execution_record is None:
        return {"ok": False, "error": "db module not available"}, 500

    try:
        rec = get_execution_record(tenant_id=tenant_id, envelope_id=envelope_id)
        if rec is None:
            return {"ok": False, "error": "not found"}, 404
        return {"ok": True, "data": rec}
    except Exception as e:
        logging.exception("Unhandled error in /executions/<envelope_id>")
        return {"ok": False, "error_type": e.__class__.__name__, "error": str(e)}, 500


@app.get("/db-info")
def db_info():
    """
    Dev/ops diagnostic endpoint.
    Reports whether DB persistence is enabled and what tables exist in the target DB.
    """
    allowed, denial = _require_dev_harness()
    if not allowed:
        return denial

    claims, denial = _claims_or_denial()
    if denial:
        return denial
    if claims.role != "admin":
        return {"ok": False, "error": "forbidden"}, 403

    info = {
        "ok": True,
        "persist_enabled": _persist_enabled(),
        "db_module_available": get_conn is not None,
        "target_table": "execution_records",
    }

    if get_conn is None:
        return info

    try:
        conn = get_conn()
        try:
            with conn, conn.cursor() as cur:
                cur.execute(
                    "SELECT table_schema, table_name "
                    "FROM information_schema.tables "
                    "WHERE table_schema NOT IN ('pg_catalog','information_schema') "
                    "ORDER BY table_schema, table_name;"
                )
                rows = cur.fetchall()
                info["tables"] = [{"schema": r[0], "name": r[1]} for r in rows]

                cur.execute(
                    "SELECT ordinal_position, column_name, data_type "
                    "FROM information_schema.columns "
                    "WHERE table_schema='public' AND table_name='execution_records' "
                    "ORDER BY ordinal_position;"
                )
                cols = cur.fetchall()
                if cols:
                    info["execution_records_columns"] = [
                        {"pos": c[0], "name": c[1], "type": c[2]} for c in cols
                    ]
        finally:
            conn.close()
    except Exception as e:
        logging.exception("Unhandled error in /db-info")
        return {"ok": False, "error_type": e.__class__.__name__, "error": str(e)}, 500

    return info


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="127.0.0.1", port=port, debug=True)
