# Execalc Cloud v1 — Multi-Tenancy Model

This document defines the non-negotiable multi-tenancy rules for Execalc Cloud v1.
All persistence, execution, governance, and observability must conform to this model.

---

## 1. Tenant Definition

- A tenant is the highest isolation boundary in Execalc Cloud.
- A tenant may represent:
  - An organization
  - A firm
  - A client account
- Tenants are first-class entities and are never implicit.

---

## 2. Tenant Identity

- Every request must resolve to exactly one tenant.
- Tenant identity is resolved at ingress.
- No anonymous or multi-tenant execution contexts are permitted.
- Tenant identity is immutable for the lifetime of a request.

---

## 3. Isolation Guarantees

Execalc Cloud v1 enforces strict isolation across tenants:

- No shared data stores without explicit tenant partitioning
- No shared execution state
- No shared memory
- No cross-tenant inference or leakage

Isolation is enforced by design, not by convention.

---

## 4. Namespace Scoping

- All persisted data is tenant-scoped.
- All governance decisions are tenant-aware.
- All audit logs are tenant-scoped.
- Namespaces may exist within a tenant, but never across tenants.

---

## 5. Governance Per Tenant

- Governance invariants apply globally.
- Governance enforcement occurs per tenant.
- Tenant-specific policies may restrict behavior further, but never loosen global constraints.
- No tenant may override Cloud v1 governance invariants.

---

## 6. Execution Context

- Execution contexts are created per request, per tenant.
- Execution contexts are destroyed after request completion.
- No execution context persists across tenants or requests.

---

## 7. Observability and Audit

- All audit trails are tenant-segregated.
- Operators may only view audit data for their own tenant.
- Cross-tenant observability is prohibited.

---

## 8. What Multi-Tenancy Is Not

Cloud v1 explicitly excludes:
- Shared “global” tenant execution
- Soft isolation via naming conventions
- Post-hoc data filtering for isolation
- Cross-tenant optimization or learning

---

## 9. Invariants

The following are invariant in Cloud v1:
- Tenant identity is mandatory
- Isolation is absolute
- No execution without tenant context
- No data without tenant ownership

---

Multi-tenancy in Execalc Cloud exists to guarantee trust, not to optimize convenience.
