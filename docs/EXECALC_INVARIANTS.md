# Execalc Invariants (Non-Negotiable Build Contracts)

This document is the source of truth for Execalc's true north. If code behavior conflicts with any invariant below, the code is wrong and must be corrected.

## 1) Product Purpose (North Star)

Execalc is a governed judgment system that enables organizations to use advanced AI safely in real operations by enforcing:
- tenant isolation
- verified identity and authority
- controlled tool use
- explicit memory governance
- auditability

## 2) Definitions

- Tenant: an organization namespace. Tenants must be isolated by construction.
- Actor: the authenticated identity operating within a tenant (user/service).
- Request context: the single, authoritative per-request execution context that binds tenant + actor and guarantees cleanup.
- Ingress envelope: the structured input used to derive tenant context (not arbitrary payload fields).
- Connector: an integration that can read from or act on external systems.

## 3) Tenant Isolation (Hard Requirement)

- No cross-tenant reads, writes, memory access, or connector access is permitted.
- Every persisted object that is tenant-scoped must include tenant_id and be queried with tenant_id enforced.
- Any attempt to operate without a tenant context is a hard failure (deny-by-default).

## 4) Actor Identity and Authority (Hard Requirement)

- Actor identity and role must be derived from the auth layer (verified claims), not from request payload.
- Dev harness identity injection (e.g., headers) is permitted only when explicitly gated by a dedicated dev mode flag, and must never be enabled by default.
- Authorization is enforced centrally via role/policy checks; no scattered ad hoc permission logic.

## 5) Request Context Integrity (Hard Requirement)

- Tenant + actor context must be established exactly once per request via a single authoritative wrapper.
- Cleanup must always occur, including on exceptions (no context bleed).
- Context storage must be request-scoped (e.g., ContextVar) and never global mutable state.

## 6) Memory Governance (Hard Requirement)

- Memory writes are explicit, deliberate operations (no implicit auto-save).
- Memory is tenant-scoped and actor-attributed with provenance metadata.
- Memory classes must support:
  - active (eligible to influence runtime)
  - dormant (stored, recallable, but does not influence runtime)
- Global runtime logic (reflexes) must respect the publication gate doctrine; tenant/private material is never promoted globally.

## 7) Connector and Tool Governance (Hard Requirement)

- Connectors are tenant-scoped and credential-scoped; credentials are never shared across tenants.
- Default posture is read-only; action-capable tools require explicit enablement and policy gating.
- All tool calls must execute inside the request context and be logged.

## 8) Auditability (Hard Requirement)

- Every request must be traceable with:
  - request id / trace id
  - tenant id
  - actor id + role
  - policy decisions (allow/deny)
  - connector/tool invocation records
- Logging must minimize sensitive content and favor metadata over raw payloads.

## 9) Reliability and Build Gates (Hard Requirement)

- The repo must include tests that prove the invariants:
  - no tenant/actor bleed across requests
  - deny-by-default without tenant context
  - dev harness gated and off by default
  - tenant_id enforcement in persistence/query paths (as implemented)
- Changes that violate these invariants must fail CI/tests and be blocked from release.

## 10) Operating Principle

Early rigor prevents downstream defects. Prefer preventive structure at ingress and enforcement boundaries over reactive patching.
