# Execalc

**Governed, normative, and informed intelligence infrastructure for executive judgment.**

---

## What Execalc Is

Most AI products are thin wrappers around large language models. They provide a user interface and some integrations, but they do not impose structure on the reasoning process. They are ungoverned AI systems.

Execalc is different.

Execalc is a **judgment superstrate** — a governance and reasoning layer that sits above the language model and controls how it operates. The language model is the computational substrate. The governance architecture is the product.

Three properties define the system:

- **Governed** — the regulative layer: tenant isolation, verified identity, controlled tool use, auditability. Every responsible AI deployment requires this. It is necessary but not the product.
- **Normative** — the constitutive layer: the Prime Directive, the three evaluation lenses, the Core 7 frameworks. These are not restrictions on the model. They are what the system *is*. The system is built to pursue value and clarity, not merely prevented from harm.
- **Informed** — the knowledge layer: the Executive Knowledge Engine corpus, a curated bench of strategic thinkers, and organizational memory — activated by situation recognition, not keyword search.

The LLM is the engine. The normative architecture and informed corpus are the product.

---

## The Problem It Solves

Ungoverned AI excels at generating information. It does not reliably produce judgment.

In an enterprise setting, the distinction matters:

- **Information without discipline** can produce confident-sounding answers built on untested assumptions
- **Inconsistent decision logic** means two prompts describing the same situation in slightly different ways produce entirely different recommendations
- **No institutional memory** means the organization cannot trace why a recommendation was made or which assumptions were used
- **No enforcement of objectives** means the system drifts from organizational priorities over time

Execalc addresses this by converting raw AI capability into a **governed decision system**: one that enforces objectives, requires structured evaluation before output, produces auditable decision artifacts, and accumulates organizational knowledge over time.

---

## The Strategic Design

### Judgment Before Speed

Most AI products in the market today are orchestration systems. They chain prompts, build software, automate execution. They are optimized for velocity. They assume intent is correct.

Execalc occupies a different lane. It **interrogates intent before it accelerates**. It surfaces what is assumed, what is untested, and what is at risk before execution begins.

The real category distinction is not AI vs. AI. It is **acceleration vs. governance**.

### The Prime Directive

Every governed output passes through a three-lens evaluation before delivery:

1. **Assets vs. Liabilities** — does this action improve or degrade the balance sheet position?
2. **Risk / Reward** — is the risk/reward balance explicit and acceptable?
3. **Supply / Demand** — is there a real structural imbalance being leveraged or exposed?

All three lenses must be evaluated — not all three must be favorable. An unfavorable lens that was seen, named, and knowingly accepted is a sound decision. An unevaluated lens is a governance failure.

> *The sin is not an unfavorable lens. The sin is an unevaluated one.*

### Necessary Friction

Execalc does not eliminate deliberation — it compresses it into governed logic.

There are two types of friction in decision-making:
- **Bad friction** (meetings that could be a document, re-explaining context, tool-switching) — eliminate it
- **Necessary friction** (assumption testing, conflict detection, risk surface exposure) — compress it into the system, never remove it

Organizations that eliminate necessary friction do not move faster. They accelerate toward mistakes. Execalc encodes necessary friction as structural gates that execute faster and more consistently than manual deliberation — while ensuring they still execute.

### Organizational Memory

Execalc is designed to accumulate institutional knowledge over time. Every governed decision produces a traceable artifact. Every admitted memory unit must pass a structured admission filter. The organization's decision history becomes a compounding asset — not a pile of chat logs.

---

## Current Build State

| Stage | Description | Status |
|---|---|---|
| 4A–4C | Decision Loop Engine | Complete |
| 5A | Decision Journal Retrieval (`GET /decision/<id>`) | Complete |
| 5B | Decision Journal Timeline (`GET /decision/recent`) | Complete |
| 5C | Smoke Harness Coverage | Complete |
| 6 | Persistence Hardening + Operational Defaults | Complete |
| 7A | Postgres Integration, lazy-loaded driver, service layer | Complete |
| 7B | `/decision/compare` endpoint + compare engine | Complete |
| 4B | Stability invariants + drift monitor + decision guardrails | Complete |

**Active branch:** `claude/codebase-audit-ltOXr`  
**Test suite:** 34 decision loop unit tests passing

---

## Architecture Properties

The following properties are enforced by construction — they are not features to be added later:

| Property | Enforcement Mechanism |
|---|---|
| Tenant isolation | Hard — no cross-tenant reads, writes, memory, or connector access |
| Deny-by-default | No operation proceeds without verified tenant + actor context |
| Audit trail | Every request produces a traceable record (request ID, tenant, actor, policy decisions) |
| Memory governance | No implicit memory writes; all persistence is explicit and attributed |
| Connector scope | Read-only by default; action-capable tools require explicit enablement |
| Runtime/reasoning separation | Deterministic gates fire before any LLM invocation |
| Refusal logging | BLOCK and ESCALATE events are auditable outcomes |

---

## Canonical Doctrine

The architecture is governed by a doctrine hierarchy maintained in `docs/`:

| Document | Role |
|---|---|
| `docs/EXECALC_INVARIANTS.md` | Hard contracts — nothing overrides these |
| `docs/CANON.md` | Index of all canonical doctrine |
| `docs/vision/TRUE_NORTH.md` | Product identity anchor |
| `docs/vision/STAGE_MAP.md` | What gets built and in what order |
| `docs/architecture/PRIME_DIRECTIVE_RUNTIME_ENFORCEMENT.md` | The governance gate |
| `docs/architecture/RUNTIME_REASONING_SEPARATION.md` | Why the platform governs the model, not the reverse |
| `docs/product/JUDGMENT_SUPERSTRATE_POSITIONING.md` | Competitive positioning doctrine |
| `docs/governance/SECURITY_POSTURE_AND_COMPLIANCE_DESIGNATION.md` | Compliance readiness and designation process |

---

## Developer Quick-Start

### Prerequisites
- Python 3.11+
- pip

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run compile check
```bash
python -m compileall -q src/service && echo compile_ok
```

### Run tests
```bash
pytest -q src/service/decision_loop/
```

Tests requiring a live Postgres instance will show as errors when the database is unavailable — this is expected behavior for the DB integration test slice.

### Branch and push protocol
```bash
# All current work targets:
git push -u origin claude/codebase-audit-ltOXr
```

On network failure, retry up to 4× with exponential backoff (2s, 4s, 8s, 16s).

### Key API endpoints (when service is running)
| Endpoint | Purpose |
|---|---|
| `POST /decision/run` | Submit a scenario for governed decision analysis |
| `GET /decision/<id>` | Retrieve a specific decision artifact |
| `GET /decision/recent` | Timeline of recent decision artifacts |
| `GET /decision/compare` | Compare two decision artifacts |
| `GET /health` | Service health check |

---

## Engineering Operating Rules

- Small diffs, one purpose per commit
- Every change includes a compile and test verification step before push
- No secrets in git — use environment variables and secret management
- Admin and diagnostic endpoints are explicitly gated
- If a failure mode repeats, it becomes a runbook or a test
- Governance before capability. Determinism before scale. Auditability before speed.

---

*Execalc: industrial-grade organizational cognition.*
