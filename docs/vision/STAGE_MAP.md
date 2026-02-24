# Execalc Build Stage Map (1–6)

## Stage 1 — Repo and Runtime Skeleton
**Purpose:** Establish the minimum runnable service and development discipline.

**Deliverables:**
- Service boots cleanly (local + container)
- Health check endpoints
- Configuration strategy (env, secrets placeholders)
- Test harness exists (even if minimal)
- Logging baseline
- Folder/module conventions locked

**Exit condition:** A new developer can run the service and tests predictably.

---

## Stage 2 — Multi-Tenancy Spine and Governance Boundaries
**Purpose:** Prevent entropy before features exist.

**Deliverables:**
- Tenant registration and enforcement (`tenant_id` required, verified, scoped)
- Tenant isolation rules (data, storage, connectors, logs)
- Governed ingress envelope (structured input object + validation)
- Permission boundaries (what can execute vs what can only draft)
- Audit log spine (who/what/when/tenant/context)
- Deterministic error taxonomy (invalid tenant, invalid envelope, policy violations)

**Exit condition:** The system cannot accidentally cross tenants, execute unsafe actions, or accept unstructured drift at ingress.

---

## Stage 3 — Delegation Guardrails and Canon Spine
**Purpose:** Allow controlled delegation without turning Execalc into an agent swarm.

**Deliverables:**
- Delegation model: Execalc issues commands; workers execute bounded tasks
- Policy gating: draft vs execute separation
- Proof-gated state transitions (no irreversible action without proof)
- Canonical invariants enforced by tests (Prime Directive invariants, tenant invariants)
- Kill-switches: per-tenant, per-workflow, per-integration disablement

**Exit condition:** Delegation is possible, but cannot escape governance, cannot self-escalate, and cannot mutate doctrine.

---

## Stage 4 — Connectors and Storage Driver Middleware
**Purpose:** Integrations become pluggable and safe without custom spaghetti.

**Deliverables:**
- Standard connector interface (read/write, auth, scopes, retry semantics)
- Credential store pattern (tenant-scoped, audited access)
- Storage driver middleware routing (tenant + namespace + driver)
- Connector sandboxing (rate limits, allowlists, content restrictions)
- Observability hooks (structured logs, connector metrics, failure reasons)

**Exit condition:** Any new integration can be added without violating isolation, logging, or governance.

---

## Stage 5 — Executive Knowledge Runtime
**Purpose:** Enable governed cognition as a repeatable execution path.

**Deliverables:**
- Scenario object model (Executive Scenarios trigger first)
- Activation pathway model (Scenario → Pathway → Carats/Thinkers → Prime Directive)
- Heuristic coding system admission rules (domain/source/confidence/role tags)
- Memory classes (active vs dormant; dormant does not trigger reflexes)
- Synthesis output contracts (boardroom format, traceability metadata)
- Regression suite for judgment-quality invariants (consistency checks)

**Exit condition:** Given the same inputs, Execalc produces structured, governed, traceable judgment—without ad hoc reasoning drift.

---

## Stage 6 — Production-Grade Sovereign Cognition Platform
**Purpose:** Make the system deployable and extensible without rewrites.

**Deliverables:**
- Production readiness: secure deployment, config hardening, secrets management, CI/CD gates
- Compliance scaffolding: audit logs, retention controls, access controls, tenant data lifecycle
- Replayability: execution record retrieval + deterministic re-run capability (where applicable)
- Safe extensibility: module registry (dormant modules can be registered without activation)
- Performance and reliability baselines: timeouts, quotas, backpressure, graceful degradation
- Operator controls: approve/deny gates, policy overrides (logged), per-tenant feature flags

**Exit condition:** You can onboard many tenants, add new capability modules, and run governed cognition reliably—without compromising isolation or doctrine.

---

## Locked Definition of Stage 6 Complete

Stage 6 is complete when Execalc is:

1. **Multi-tenant safe by default** (nothing works without tenant scoping)
2. **Governed by invariant enforcement** (tests enforce non-negotiables)
3. **Extensible without mutation** (new modules integrate through registries/interfaces)
4. **Auditable and replayable** (every meaningful action and judgment is traceable)
5. **Execution-subordinate** (if labor workers exist, they cannot generate strategy or escalate privileges)
6. **Operationally shippable** (deployment, monitoring hooks, and kill-switches exist)

**Stage 6 is not feature complete. Stage 6 is structurally complete.**
