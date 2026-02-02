# Execalc Cloud v1

## Execalc Build Doctrine

Execalc is not a conventional web application. It is a governed cognition layer that must remain auditable, tenant-safe, and security-first as it scales.

**Non-negotiables**
- **Governance-first architecture:** Capabilities must be policy-aware by default (deny-by-default where applicable). “Helpful” is not sufficient; behavior must be correct under governance constraints.
- **Multi-tenant isolation as a core property:** Every read/write path must be tenant-scoped, with explicit enforcement that prevents cross-tenant access by construction.
- **Security posture designed for high assurance:** Assume adversarial and misconfiguration scenarios. Diagnostic surfaces are privileged surfaces and must be guarded.
- **Trust is the product:** Correctness includes determinism, explainability, and auditability. We optimize for repeatable, provable behavior over clever output.
- **Upgradeable auth model:** Development harnesses may use headers for tenant/role to validate flows, but production must derive identity/tenant from real authentication (JWT/IAP/session) without architectural rewrites.
- **Change discipline:** Each increment should be testable, evidenced (logs/persistence), and documented. Fixes become repeatable playbooks, not tribal knowledge.
- **Tooling resilience:** When platform tooling becomes unstable, we isolate state, re-baseline quickly, and codify recovery procedures to reduce fragility over time.

Execalc is an executive-grade cognition platform designed to sit above large language models and govern their use through structured judgment, principled constraints, and auditable decision logic.

This repository is the canonical Cloud v1 trunk.

## Purpose
- Establish a governed, production-grade cloud foundation
- Enforce decision quality through explicit principles (value creation, asymmetry, risk discipline)
- Treat LLMs as substrates, not authorities
- Enable secure, multi-tenant executive cognition at enterprise scale

## Status
Cloud Version 1 — initial scaffold.
Architecture, protocols, and governance are locked prior to implementation.

## Non-Goals
- This is not an agent playground
- This is not prompt engineering
- This is not an experimentation sandbox

All additions to this repository must respect:
- Governance before capability
- Determinism before scale
- Auditability before speed

---
Execalc: industrial-grade organizational cognition.

## Gcloud crash recovery in Cloud Shell

### Symptom
`gcloud` crashes with:
`TypeError: string indices must be integers, not 'str'`

This can show up on commands like:
- `gcloud run deploy ...`
- `gcloud builds submit ...`
- `gcloud auth print-access-token ...`

### Likely cause
A corrupted or inconsistent local gcloud config/state in the active `CLOUDSDK_CONFIG` directory.

### Fast fix (isolate to a clean config directory)
1. Create a clean config directory and point gcloud at it:
   - `mkdir -p "$HOME/.config/gcloud-execalc-clean"`
   - `export CLOUDSDK_CONFIG="$HOME/.config/gcloud-execalc-clean"`

2. Authenticate (Cloud Shell is usually already authenticated, but this forces a usable local state):
   - `gcloud auth login j.brubaker@playerscapital.net --brief`

3. Set the project explicitly:
   - `gcloud config set project execalc-core`

4. Verify gcloud is healthy:
   - `gcloud auth print-access-token >/dev/null && echo token_ok`

5. Deploy again:
   - `gcloud run deploy execalc-api --source . --region us-east1 --project execalc-core --quiet`

### Make it persistent for future shells (optional)
Add to `~/.bashrc`:
- `export CLOUDSDK_CONFIG=$HOME/.config/gcloud-execalc-clean`

If you previously set `CLOUDSDK_CONFIG` to a temporary directory (like `/tmp/...`), remove that old export and replace it with the persistent path above.

## Execalc Build Doctrine

Execalc is built as a governed, multi-tenant execution engine — not a demo app and not a thin wrapper around an LLM.
This repository is intentionally structured to compound correctness, security, and operational proof over time.

### Design commitments
- Cloud-first deployment: containerized service built from source and run on managed infrastructure.
- Multi-tenant by design: tenant context is explicit, enforced, and persisted in a tenant-scoped data model.
- Governance-first execution: policies (allowlists, scopes, role gates) are enforced in the request path.
- Best-effort persistence and auditability: executions are recorded to durable storage and retrievable by tenant scope.
- Operational proof over folklore: runbooks, decision records, and doctrine live in-repo as the canonical memory.

### Engineering operating rules
- Small diffs, one purpose per commit.
- Every change includes a verification step (compile/tests) before deploy.
- No secrets in git, ever (use environment variables and secret management).
- Admin/diagnostic endpoints are explicitly gated.
- If a failure mode repeats, it becomes a runbook or a test.
