# TENANT_CONTROL_PLANE.md

## Status
Canonical doctrine — v1.0

## What the TCP Is

The Tenant Control Plane (TCP) is the sterile governance container that sits above and separate from the Execalc runtime. It is mounted before the runtime begins. It is never modified during live execution. It governs who may operate, what they may do, and what constraints apply — before any reasoning or action begins.

The TCP is not plumbing. It is the structural guarantee that makes multi-tenancy safe by construction rather than by convention.

> The TCP is to Execalc what a sterile field is to surgery. You do not operate and sterilize at the same time.

---

## Why It Cannot Be Inline

A common architectural mistake is embedding tenant governance logic inline with runtime logic — checking permissions as part of the reasoning flow, validating tenant state as a side effect of processing.

This produces:
- **Cross-tenant contamination risk** — if the runtime shares any state across calls, tenant isolation depends on every code path being correct
- **Audit opacity** — governance decisions happen inside the reasoning flow and cannot be cleanly separated in the audit trail
- **Schema evolution problems** — changes to tenant governance require changes to runtime logic
- **Compliance fragility** — the governance boundary is not a hard boundary; it is a convention

The TCP solves this by being structurally separate. It is mounted once. It governs everything. The runtime operates inside it.

---

## What the TCP Governs

**Identity** — who is the authenticated operator, what tenant do they belong to, what role do they hold

**Isolation** — hard enforcement that no object, query, memory read, or connector access crosses tenant boundaries

**RBAC** — what actions are permitted for this actor in this tenant under current policy

**Compliance cartridges** — which compliance overlays are active for this tenant and at what enforcement level

**Schema evolution** — version control of tenant configuration; changes to governance state are versioned, not in-place mutations

**Session initialization state** — the governance baseline that is verified at session start and preserved at session close

---

## TCP Lifecycle

```
Session request arrives
    ↓
TCP mounted (identity verified, tenant confirmed, RBAC loaded, compliance state loaded)
    ↓
Runtime operates within TCP constraints (no TCP modifications during execution)
    ↓
Session closes (governance state preserved for next session)
    ↓
TCP unmounted
```

The TCP is never partially mounted. It either mounts completely or the session is denied. A partial governance state is a governance failure.

---

## Reports To

The TCP reports to the platform governance layer (Devo / system administration). It does not report to operators. Operators operate within the TCP; they do not configure it during live sessions. Tenant administrators may configure the TCP between sessions through authorized governance channels.

---

## Relationship to Other Architecture

| Component | Relationship |
|---|---|
| EXECALC_INVARIANTS.md §3 | Tenant isolation invariant — the TCP is the enforcement mechanism |
| Compliance Cartridge Architecture | Compliance cartridges are loaded by the TCP at session initialization |
| Runtime ≠ Reasoning separation | TCP is a runtime governance layer; reasoning operates within it |
| Audit Requirements | TCP lifecycle events (mount, state changes, unmount) are auditable events |
| Betty / Sub-Agent Protocols | All sub-agents operate within the TCP; none may modify it |

---

## Non-Negotiables

- The TCP must be mounted before any runtime logic executes
- The TCP must not be modifiable by any operator-facing action during live execution
- Any attempt to bypass or modify the TCP in-session is a hard security event
- TCP state must be persisted at session close for continuity; it is not rebuilt from scratch each session for active tenants
