# GOVERNANCE GAP REGISTER
# docs/build_plan/GOVERNANCE_GAP_REGISTER.md

**Status:** Active gap register — architecture hardening input  
**Authority:** Synthesized from multi-session gap analysis; reviewed against current repo state  
**Purpose:** Identify where the Execalc build plan is thin between doctrine and governed runtime  
**Date:** 2026-04-13

---

## Orienting Principle

The remaining weaknesses in the Execalc build are not in doctrine naming.
The doctrine is strong.

The weakness is in **governed runtime seams**: the control points between what the system believes and what the system does.

A system with elegant doctrine and weak seams becomes an ordinary chatbot wearing executive language.

This register names the seams.

---

## How to Use This Register

Each gap is categorized into one of three buckets:

- **Bucket 1 — Runtime Judgment Gaps:** How the system classifies, reasons, and produces output
- **Bucket 2 — Governance and Control Gaps:** How the system enforces, overrides, and audits
- **Bucket 3 — Product and Build Gaps:** How the system presents, measures, and scales

Each entry includes: current repo coverage, gap description, and recommended artifact.

---

## Repo Coverage Baseline

The following docs provide partial coverage for some gaps. They are not sufficient — they are starting points.

| Existing Doc | What it covers | What it misses |
|---|---|---|
| `PERSISTENT_MEMORY_ADMISSION_AND_CLASSIFICATION_DOCTRINE.md` | Admission criteria | Admission workflow, decay, promotion process |
| `EXECALC_RUNTIME_OBJECT_MODEL.md` | Object schemas | Evidence types, provenance, action proposal contract |
| `GOVERNANCE_ENFORCEMENT_REGISTER.md` | Enforcement domains | Authority matrix, execution rights, action contract |
| `EXECUTIVE_KNOWLEDGE_ENGINE_STRATA.md` | Strata named | Synthesis provenance chain, thinker eligibility rules |
| `CORE_7_REMEDIATION_DIRECTIVE.md` | Framework scaffolding | Seam-level control points below framework level |

---

## Bucket 1 — Runtime Judgment Gaps

These are the seams where classification, reasoning, and output generation can drift silently.

---

### GAP-RJ-01: Scenario Arbitration Rules

**Current coverage:** Scenario taxonomy exists in runtime object model. Entry criteria are conceptual.

**Gap:** No conflict resolution. When a prompt is simultaneously a deal, a people issue, and a crisis, there is no canonical rule for:
- primary scenario selection
- secondary scenario overlays
- tie-breaking logic
- escalation when scenario cannot be confidently resolved

Without this, two valid runs from the same input can produce different pathways. This is a classification consistency failure.

**Recommended artifact:** `docs/architecture/SCENARIO_ARBITRATION_RULES.md`

---

### GAP-RJ-02: Scenario Registry Specification

**Current coverage:** Scenario types are named. No machine-usable registry exists.

**Gap:** A taxonomy is not a registry. Each scenario needs a structured object:
- scenario_id, name, description
- entry criteria, exclusion criteria
- trigger signatures
- required fields, optional fields
- precedence rank, default pathway
- eligible cartridges
- expected artifact type
- disqualifying conditions

Until this exists, "scenario-driven runtime" is conceptual, not operational.

**Recommended artifact:** `docs/architecture/SCENARIO_REGISTRY_SPECIFICATION.md`

---

### GAP-RJ-03: Scenario Evaluation and Testing Doctrine

**Current coverage:** None.

**Gap:** No benchmark standard for scenario classification quality. The system needs:
- a canonical scenario test pack
- gold-label examples for each scenario type
- edge cases, false positives, mixed-signal prompts
- expected routing results
- measurable accuracy standard

Without this, scenario detection is a doctrine claim without an accuracy floor.

**Recommended artifact:** `docs/build_plan/SCENARIO_CLASSIFICATION_TEST_DOCTRINE.md`

---

### GAP-RJ-04: Input Normalization Contract

**Current coverage:** None.

**Gap:** Before scenario detection, the system must define what it is allowed to do with raw user input:
- What can be extracted vs. inferred vs. assumed?
- What is raw input vs. normalized input vs. inferred fact?
- What is user-stated fact vs. system-derived inference vs. missing fact?

This is one of the most consequential hidden seams in the architecture. A loose normalization layer produces unreliable scenario detection downstream.

**Recommended artifact:** `docs/architecture/INPUT_NORMALIZATION_CONTRACT.md`

---

### GAP-RJ-05: Evidence and Provenance Model

**Current coverage:** Outputs described as "attributable and auditable." No evidence taxonomy defined.

**Gap:** Every claim in a decision artifact should point to an evidence class. Canonical evidence types needed:
- user-asserted fact
- uploaded document
- retrieved memory (with memory_id)
- system-derived inference
- external source (with trust tier)
- teammate opinion
- quantitative record

Without evidence typing, auditability is a narrative claim, not a runtime property.

**Recommended artifact:** `docs/architecture/EVIDENCE_AND_PROVENANCE_MODEL.md`

---

### GAP-RJ-06: Confidence Model Calibration

**Current coverage:** Confidence field exists in decision artifact schema.

**Gap:** No formula or ruleset defines how confidence is earned. Confidence needs to be a function of:
- evidence quality and completeness
- contradiction load
- scenario classification clarity
- model agreement
- memory recency and relevance

Without calibration, "confidence" is cosmetic language rather than governed judgment.

**Recommended artifact:** `docs/governance/CONFIDENCE_MODEL_CALIBRATION.md`

---

### GAP-RJ-07: Synthesis Provenance Chain *(added)*

**Current coverage:** EKE strata are defined with trust tiers. No cross-strata synthesis tracking.

**Gap:** When the EKE synthesizes across multiple strata (Monolith + Client Cartridge + Memory), the output's provenance is not recorded. The system cannot answer:
- Which strata contributed to this synthesis?
- At what weight?
- Were there conflicts between strata that were silently resolved?

If synthesis provenance cannot be traced, the auditability claim for decision artifacts is hollow.

**Recommended artifact:** `docs/architecture/SYNTHESIS_PROVENANCE_CHAIN.md`

---

### GAP-RJ-08: Reflex Priority Ordering *(added)*

**Current coverage:** Reflex taxonomy named in PSA directive. No priority ordering.

**Gap:** When multiple reflexes fire simultaneously (e.g., Risk Reflex + Contradiction Reflex on the same input), which prevails? The system needs:
- a canonical reflex precedence table
- rules for concurrent activation
- suppression logic when reflexes conflict
- operator notification when reflex collisions occur

**Recommended artifact:** `docs/architecture/REFLEX_PRIORITY_ORDERING.md` (or section within PROACTIVE_SOLUTIONS_ARCHITECTURE.md)

---

### GAP-RJ-09: Signal Suppression Rules *(added)*

**Current coverage:** Signal surfacing model covers when to surface. No suppression doctrine.

**Gap:** Over-surfacing erodes operator trust as quickly as under-surfacing. The system needs explicit rules for:
- when a signal should NOT be surfaced
- suppression thresholds per posture mode
- what is logged when a signal is suppressed
- how suppression history informs future thresholds

**Recommended artifact:** Section within `docs/architecture/EXECALC_REASONING_STACK.md` or standalone doc

---

### GAP-RJ-10: Thinker Contribution Rules

**Current coverage:** Thinker concept defined in EKE strata.

**Gap:** No eligibility rules. The system needs:
- qualification criteria for a thinker to be admitted to the Monolith
- maximum weight any single thinker can carry
- rules for thinker conflict (when two thinkers disagree)
- how conflicts are exposed to the operator
- how temporary instruments differ from canonized thinkers
- deprecation and removal rules

Without these, "thinkers" become a conceptual bucket rather than a governed knowledge primitive.

**Recommended artifact:** `docs/architecture/THINKER_CONTRIBUTION_RULES.md`

---

## Bucket 2 — Governance and Control Gaps

These are the seams where authority, enforcement, and institutional integrity can fail.

---

### GAP-GC-01: Authority Matrix and Execution Rights

**Current coverage:** Role model and governance enforcement domains exist. No authority matrix.

**Gap:** The system needs a concrete matrix: who may perform each governed action:
- view, classify, compare
- approve, escalate, execute
- override, dissent, appeal
- promote to memory, demote, expire
- publish externally
- change cartridges or organizational objectives
- modify tenant authority structure

This matrix must map directly to the Execution Boundary Engine.

**Recommended artifact:** `docs/governance/AUTHORITY_MATRIX_AND_EXECUTION_RIGHTS.md`

---

### GAP-GC-02: Override, Dissent, and Appeals Doctrine

**Current coverage:** Human authority described as final. No structured override mechanism.

**Gap:** The system needs a governed record when an operator overrides a system recommendation:
- what was recommended
- what was overridden to
- rationale (optional but encouraged)
- downstream outcome (if trackable)
- whether the override should influence future weighting

This is central to learning, auditability, and governance integrity. Without it, overrides disappear into chat history.

**Recommended artifact:** `docs/governance/OVERRIDE_DISSENT_AND_APPEALS_DOCTRINE.md`

---

### GAP-GC-03: Action Proposal Contract

**Current coverage:** Decision artifacts exist. Handoff from judgment to action is undefined.

**Gap:** The system needs a canonical object for a proposed action with mandatory fields before execution can occur:
- action_id, action_type, scenario_id, artifact_id
- proposing agent (human or system)
- reversibility classification (reversible / partially reversible / irreversible)
- required proof for each reversibility class
- authorization level required
- expiration timestamp
- downstream dependencies

Irreversible actions require a higher proof standard than reversible ones. This is where many systems become dangerous.

**Recommended artifact:** `docs/architecture/ACTION_PROPOSAL_CONTRACT.md`

---

### GAP-GC-04: Failure-Mode Doctrine

**Current coverage:** None.

**Gap:** The plan lacks a doctrine for what the system does when it cannot safely judge:
- insufficient evidence
- contradictory evidence
- scenario collision
- policy conflict
- weak provenance
- stale memory
- low-confidence route selection

A board-grade system must have a governed failure posture — not just an answer posture. Silent degradation is worse than transparent failure.

**Recommended artifact:** `docs/governance/FAILURE_MODE_DOCTRINE.md`

---

### GAP-GC-05: Conflict-of-Governance Doctrine

**Current coverage:** Governance layers defined separately. No explicit conflict resolution ladder.

**Gap:** When organizational objectives, tenant rules, operator intent, and Prime Directive outputs conflict, the system needs one explicit resolution hierarchy:
- which layer prevails
- when escalation is mandatory
- how conflicts are logged
- what happens when no layer can safely resolve

This is especially critical once cartridges and tenant-level objectives are active.

**Recommended artifact:** `docs/governance/CONFLICT_OF_GOVERNANCE_DOCTRINE.md`

---

### GAP-GC-06: Memory Admission Review Workflow

**Current coverage:** Admission criteria defined in doctrine doc. Workflow is absent.

**Gap:** The process that converts a memory candidate into governed memory needs explicit specification:
- who or what approves
- which classes are auto-admitted vs. human-reviewed
- what can be promoted, demoted, expired, quarantined, or contested
- what happens to downstream artifacts that referenced a memory unit later demoted
- audit trail for admission decisions

Bad admitted memory contaminates downstream reasoning indefinitely. This is a high-risk gap.

**Recommended artifact:** `docs/architecture/MEMORY_ADMISSION_REVIEW_WORKFLOW.md`

---

### GAP-GC-07: Temporal Decay Model for Memory *(added)*

**Current coverage:** Admission promotion ladder defined. No expiration or decay model.

**Gap:** Admitted memory does not have a half-life. Different claim types decay at different rates:
- an observation from last week vs. a strategic principle from last year
- a market condition assessment vs. a governance invariant
- a session-specific heuristic vs. a canonical organizational rule

Without a decay model, stale memory silently corrupts current reasoning.

**Recommended artifact:** Section within `docs/architecture/PERSISTENT_MEMORY_SYSTEM.md`

---

### GAP-GC-08: Session-to-Persistent Promotion Boundary *(added)*

**Current coverage:** Session context and persistent memory exist as concepts. Boundary not specified.

**Gap:** The system needs explicit rules for what triggers promotion from session context to memory candidate:
- which signal types are eligible at session end
- what triggers immediate mid-session promotion
- what is automatically discarded
- who can manually flag a session signal for promotion

Without this, the boundary between ephemeral and durable is arbitrary.

**Recommended artifact:** Section within `docs/architecture/PERSISTENT_MEMORY_SYSTEM.md`

---

### GAP-GC-09: Audit Trail Format Specification *(added)*

**Current coverage:** Auditability described throughout governance docs. No format spec.

**Gap:** The system needs a canonical audit trail format defining:
- which events are audited (mandatory list)
- required fields for each audit record
- who can read audit records
- retention policy
- tamper evidence requirements

Without this, "auditable" is a marketing claim.

**Recommended artifact:** `docs/governance/AUDIT_TRAIL_FORMAT_SPECIFICATION.md`

---

## Bucket 3 — Product and Build Gaps

These are the seams where the system's runtime meets users, surfaces, and organizational scale.

---

### GAP-PB-01: Cartridge Packaging Standard

**Current coverage:** Cartridges named and stratified. No packaging spec.

**Gap:** Each cartridge needs a standard package definition:
- name, sponsor, scope
- objectives and guardrails
- polarity, triggers, exclusions
- version, owner, review cadence
- dependencies, deactivation conditions
- trust tier, tenant scope
- conflict rules with other cartridges

Without this, cartridges are a conceptual bucket rather than a governed product primitive.

**Recommended artifact:** `docs/architecture/CARTRIDGE_PACKAGING_STANDARD.md`

---

### GAP-PB-02: Artifact Family Taxonomy

**Current coverage:** Single decision artifact type in runtime object model.

**Gap:** A single artifact type is too broad. The system likely needs a family with shared spine plus scenario-specific modules:
- DecisionArtifact (general)
- DiligenceArtifact
- EscalationArtifact
- ComparisonArtifact
- ExecutionArtifact
- BoardBrief
- PostmortemArtifact

Otherwise the artifact schema either bloats with optional fields or becomes too generic to be useful.

**Recommended artifact:** `docs/architecture/ARTIFACT_FAMILY_TAXONOMY.md`

---

### GAP-PB-03: Comparison Doctrine

**Current coverage:** `GET /decision/compare` endpoint exists. No comparison doctrine.

**Gap:** Comparison needs its own rules:
- what counts as comparable (same scenario only, or cross-scenario?)
- what is normalized before comparison
- how changed assumptions are surfaced
- what metrics are displayed
- when comparison is recommended proactively
- what a comparison artifact looks like

Comparison is one of the most defensible enterprise advantages. It needs doctrine, not just an endpoint.

**Recommended artifact:** `docs/architecture/COMPARISON_DOCTRINE.md`

---

### GAP-PB-04: Surface-by-Surface Output Contract

**Current coverage:** Five product surfaces named. No per-surface contracts.

**Gap:** Each surface needs its own output contract:
- Chat: what must always appear, what is optional, what is suppressed
- Betty: agent-specific output format, escalation triggers, authority limits
- IFD: intake artifact format, routing output, enrichment standard
- Bridge: cross-tenant artifact format, neutrality requirements, approval surface
- Admin: governance view, authority management, override interface

Product coherence is won or lost at the surface contract level.

**Recommended artifact:** `docs/product/SURFACE_OUTPUT_CONTRACTS.md`

---

### GAP-PB-05: Quality Measurement Doctrine

**Current coverage:** None.

**Gap:** The system needs canonical success measures for judgment quality — not uptime or speed:
- scenario classification accuracy rate
- operator override rate (and trend)
- false-confidence rate (high confidence, wrong outcome)
- action reversal rate
- memory contamination rate
- compare usefulness rating
- clarity lift score
- time-compression value (decision latency before vs. after)

Without these, Execalc cannot defend its own claims.

**Recommended artifact:** `docs/build_plan/QUALITY_MEASUREMENT_DOCTRINE.md`

---

### GAP-PB-06: Onboarding and Tenant Bootstrapping Model

**Current coverage:** None.

**Gap:** Multi-tenant enterprise systems require a defined first-run process:
- tenant profile and organizational objectives
- role mappings and authority matrix setup
- approved integrations
- cartridge selection
- memory posture (what is auto-admitted vs. manual)
- trust boundary configuration
- initial scenario test pack

A weak onboarding model creates downstream governance debt that is very hard to unwind.

**Recommended artifact:** `docs/product/TENANT_ONBOARDING_MODEL.md`

---

### GAP-PB-07: Doctrine-to-Code Traceability

**Current coverage:** Strong conceptual doctrine stack. No mapping from doctrine objects to implementation objects.

**Gap:** The system needs explicit traceability from each doctrine primitive to its implementation counterpart:

| Doctrine object | Implementation target |
|---|---|
| Scenario Registry | Code module / API schema |
| Artifact schema | API response contract |
| Authority Matrix | Policy enforcement module |
| Cartridge package | Versioned config object |
| Memory admission | Storage service + admission gate |
| Prime Directive evaluation | Required fields in artifact |
| Reflex definition | Trigger rules + activation logic |

Without this, CLAUDE.md can be elegant while the repo drifts in a different direction.

**Recommended artifact:** `docs/build_plan/DOCTRINE_TO_CODE_TRACEABILITY.md`

---

## Summary: The Six Most Dangerous Gaps

These six gaps are where a governed system quietly becomes an ordinary chatbot wearing executive language:

| Rank | Gap | Why it is dangerous |
|---|---|---|
| 1 | Scenario arbitration (GAP-RJ-01) | Without conflict resolution, classification is non-deterministic |
| 2 | Input normalization contract (GAP-RJ-04) | Loose intake poisons all downstream reasoning |
| 3 | Evidence and provenance model (GAP-RJ-05) | Without evidence typing, auditability is a claim, not a property |
| 4 | Authority matrix + action proposal contract (GAP-GC-01 + GC-03) | Without execution rights, governance is advisory only |
| 5 | Memory admission workflow (GAP-GC-06) | Bad admitted memory contaminates reasoning indefinitely |
| 6 | Doctrine-to-code traceability (GAP-PB-07) | Without mapping, doctrine and implementation diverge silently |

---

## Recommended Build Sequencing

### Wave 1 — Before any memory or heuristic build begins
- GAP-RJ-04: Input normalization contract
- GAP-RJ-05: Evidence and provenance model
- GAP-GC-06: Memory admission review workflow
- GAP-GC-07: Temporal decay model (within PERSISTENT_MEMORY_SYSTEM.md)

### Wave 2 — Before EKE activation or cartridge work begins
- GAP-RJ-01: Scenario arbitration rules
- GAP-RJ-02: Scenario registry specification
- GAP-RJ-07: Synthesis provenance chain
- GAP-PB-01: Cartridge packaging standard
- GAP-RJ-10: Thinker contribution rules

### Wave 3 — Before any governed execution capability
- GAP-GC-01: Authority matrix and execution rights
- GAP-GC-03: Action proposal contract
- GAP-GC-02: Override, dissent, and appeals doctrine
- GAP-GC-04: Failure-mode doctrine

### Wave 4 — Before multi-tenant production
- GAP-GC-05: Conflict-of-governance doctrine
- GAP-GC-09: Audit trail format specification
- GAP-PB-06: Tenant onboarding model
- GAP-PB-07: Doctrine-to-code traceability

### Wave 5 — Before external narrative or market claims
- GAP-PB-05: Quality measurement doctrine
- GAP-PB-04: Surface-by-surface output contract
- GAP-PB-03: Comparison doctrine
- GAP-PB-02: Artifact family taxonomy

---

## Gap Count Summary

| Bucket | Count |
|---|---|
| Runtime Judgment Gaps | 10 |
| Governance and Control Gaps | 9 |
| Product and Build Gaps | 7 |
| **Total** | **26** |

---

*Gap register established: 2026-04-13. Review and update at the start of each build wave. Gaps should be closed by creating the recommended artifact or explicitly accepting the risk in writing.*
