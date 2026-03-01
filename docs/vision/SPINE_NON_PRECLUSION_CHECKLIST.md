# Spine Non-Preclusion Checklist

Use this checklist for every capability proposed in a feature chat. If any item is **No**, the spine must be adjusted in **Stage 2–4** (not later).

---

## A) Capability Definition
- **A1.** What is the capability in one sentence?
- **A2.** What is the unit of work (object) it operates on (e.g., Deal, Thread, CommentCluster, ClaimSignal)?
- **A3.** What is the output contract (what Execalc produces, format, metadata)?

---

## B) Ingress Discipline
- **B1.** What are the input sources (public web, internal email, CRM, docs)?
- **B2.** Can input be represented as a governed envelope with schema validation?
- **B3.** Does input require role-weighting or source credibility scoring?

---

## C) Governance and Risk
- **C1.** What are the irreversible actions (if any)?
- **C2.** What proof is required before any irreversible action?
- **C3.** What are the highest-risk false positives and false negatives?
- **C4.** What thresholds are required to promote a heuristic (volume, confidence, corroboration)?

---

## D) Tenant Isolation
- **D1.** Does any data cross tenants? (**Must be No** unless explicitly designed and approved.)
- **D2.** Are all artifacts stored in tenant-namespaced storage paths?
- **D3.** Are credentials and connectors tenant-scoped with audit logging?

---

## E) Execution and Delegation
- **E1.** Does the capability require draft behavior only, or execute actions?
- **E2.** If execute: where are the operator approval gates?
- **E3.** Can any worker initiate actions without an Execalc-issued command? (**Must be No**.)
- **E4.** Is the workflow representable as a finite set of states with allowed transitions?

---

## F) Memory and Heuristics
- **F1.** Does it create memory entries? If yes, what class (active vs dormant)?
- **F2.** What metadata is stored (domain, source, confidence, role, timestamps)?
- **F3.** What is the eviction/retention posture and audit requirement?

---

## G) Observability and Control
- **G1.** Is every step logged with `tenant_id` + `capability_id` + `execution_id`?
- **G2.** Is there a kill-switch for this capability (tenant-level and global)?
- **G3.** Can the system replay the decision path and show why the alert/recommendation occurred?

---

## H) Minimal Viable Experiment
- **H1.** What is the smallest real-world test that proves value?
- **H2.** What would falsify the hypothesis?
- **H3.** What is the success metric (accuracy, latency, adoption, reduced time-to-decision)?

---

## Operating Rule for Feature Chats

When you bring a capability back into dev chat, bring it back in this format:

1. Capability one-liner
2. Object model
3. Ingress sources + envelope schema notes
4. Governance risks + proof gates
5. Required primitives (what the spine must support)
6. Minimal viable experiment + success metric

This ensures the dev spine evolves to accommodate future modules without becoming feature-driven chaos.
