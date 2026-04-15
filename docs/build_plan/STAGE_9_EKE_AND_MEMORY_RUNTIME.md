# STAGE_9_EKE_AND_MEMORY_RUNTIME.md

## Status
Spec — not yet built

## Owner
Build / Architecture

## Stage Number
Stage 9

## One-Line Purpose
Stage 9 activates the Executive Knowledge Engine corpus, wires the memory admission pipeline, brings the first Carat online, and makes compliance cartridges toggleable — converting the governance infrastructure from doc-only to runtime reality.

---

## What Stage 9 Starts From

After Stage 8, the system:
- Makes real LLM judgment calls governed by the Reflex/Activation cascade
- Applies Prime Directive evaluation on every output
- Runs Recursive Reintegration before delivery
- Records full session audit trails

What Stage 8 does **not** deliver:
- The EKE corpus is referenced in the activation pathway but no corpus loader exists
- Memory is referenced in the context package but no memory runtime exists
- Carats are referenced in the priority order but no Carat objects exist
- Compliance cartridges are specced but not toggleable
- Every session starts with no persistent context from prior sessions

Stage 9 closes these gaps in order. Each sub-stage makes the context package richer.

---

## Sub-Stage Breakdown

Stage 9 is delivered in five sequential sub-stages. Exit condition of each must be met before the next begins.

---

### Sub-Stage 9A: EKE Corpus Loader + Scenario-to-Corpus Mapping

**What it builds:** The runtime layer that loads EKE corpus entries (Monolith entries, Thought Leadership Nuggets) into the Stage 4 Activation Pathway based on detected scenario.

**Current state:** 230 seed corpus entries exist in `docs/corpus/EKE_MONOLITH_SEED_CORPUS.md` as documentation. No loader exists. The activation pathway has a `corpus_entries` slot in the context package that is always empty.

**Deliverables:**

1. **Corpus storage model**
   - Schema from `docs/architecture/EXECUTIVE_KNOWLEDGE_ENGINE_CORPUS_SCHEMA.md`
   - Corpus entries storable and retrievable by: corpus_id, thinker, theme, scenario associations, stratum
   - Initial storage: flat file or SQLite for Stage 9; Postgres path available

2. **Corpus seed loader**
   - Load the 230 seed entries from the existing corpus document into the storage model
   - Validate against the 19-column schema defined in the Manifest
   - Entries that fail schema validation are logged but not loaded

3. **Scenario-to-corpus mapping**
   - From `REFLEX_AND_ACTIVATION_SYSTEM.md`: pre-loaded corpus associations for each of the five scenario buckets
   - Mapping: when Scenario X is detected, pull corpus entries Y, Z, W
   - Initial mapping covers the five scenario buckets (Growth/Opportunity, Deal/Capital, Org/Execution, Risk/Defense, Strategic Insight)
   - Full per-scenario mapping is the follow-on spec `SCENARIO_CORPUS_MAPPING.md`

4. **Context package integration**
   - When Scenario is detected in Stage 2, the corpus loader fires during Stage 4 (Activation Pathway)
   - Relevant corpus entries appear in `corpus_entries` slot of the context package
   - LLM in Stage 5 has corpus context available; this is the difference between an informed judgment call and a blank-page call

**New file:** `src/service/eke/corpus_loader.py`
**New file:** `src/service/eke/scenario_corpus_map.py`

**Exit condition:**
- Given a detected scenario, corpus entries are loaded and appear in the context package
- LLM judgment call receives corpus context for the scenario type
- Seed corpus validated and loaded without errors
- Audit trail records which corpus entries were loaded for each session

---

### Sub-Stage 9B: Memory Admission Endpoint + Six-Test Filter

**What it builds:** The governed memory pipeline — the system through which raw observations become admitted memory units that persist across sessions.

**Current state:** Memory is entirely doc-only. The memory slot in the context package is always empty. There is no endpoint for submitting memory candidates, no admission filter, and no storage model for admitted memory.

**Deliverables:**

1. **Memory candidate submission endpoint**
   - `POST /memory/submit` — accepts a raw claim for admission review
   - Input: raw text + source + session context
   - Triggers admission pipeline

2. **Six-test admission filter** (runtime implementation)
   - Test 1: Stand-alone (can it be understood without conversation context?)
   - Test 2: Disputability (can it be challenged?)
   - Test 3: Governance (does it fall within the claim type taxonomy?)
   - Test 4: Activation (is there a scenario where this claim changes a decision?)
   - Test 5: Durability (will it remain relevant beyond this session?)
   - Test 6: Composability (can it combine with other claims?)
   - Evaluation: Premium tier model (this is judgment, not labor)
   - Verdict: admit / reject with stated reason

3. **Memory storage model**
   - Schema includes: claim text, claim type, confidence, scope, activation state, time horizon, sensitivity, provenance, promotion status
   - Promotion states: Observed → Candidate → Admitted → Weighted → Canonical
   - Active vs. Dormant flag (active = eligible to influence runtime reasoning)
   - Tenant-scoped: no cross-tenant memory

4. **Memory retrieval for context package**
   - During Stage 4 (Activation Pathway), query admitted memory for entries relevant to the detected scenario
   - Active memory loads into `operator_memory` slot of context package
   - Dormant memory is not loaded (does not trigger reflexes)

5. **Memory admission endpoint**
   - `GET /memory/admitted` — list admitted memory for current tenant
   - `GET /memory/candidates` — list pending candidates
   - `POST /memory/promote/<id>` — promote a candidate to admitted (requires operator confirmation)

**New file:** `src/service/memory/admission.py`
**New file:** `src/service/memory/storage.py`

**Exit condition:**
- Submitting a claim to `POST /memory/submit` runs it through the six-test filter
- Admitted claims appear in the `operator_memory` slot of subsequent context packages
- Rejected claims are logged with stated reason
- Active vs. dormant state is enforced (dormant claims do not load into the context package)
- Tenant isolation enforced: no cross-tenant memory
- Journaling (storing raw conversation turns) is not treated as admission — only governed claims that pass the six tests are in active memory

---

### Sub-Stage 9C: First Carat Activation

**What it builds:** The first functioning Carat — a strategic overlay that modifies the reasoning context when activated. This proves the Carat architecture works end-to-end before the full Carat library is built.

**Current state:** Carat registry standard is specced. Zero Carat instances exist. The `active_carats` slot in the context package is always empty.

**Deliverables:**

1. **Carat object model** (runtime)
   - Schema from `CARAT_REGISTRY_STANDARD.md`
   - Carat: id, name, activation_criteria, context_injections, constraint_injections, scenario_eligibility, priority, audit_requirements
   - Storage: flat file or database, tenant-scoped

2. **Carat activation check** (in Stage 4 — Activation Pathway)
   - On scenario detection, check Carat registry for eligible Carats
   - Eligibility: scenario matches Carat's scenario_eligibility list
   - Conflict detection: two active Carats with contradictory constraints → arbitration (see note)
   - Eligible Carats load into `active_carats` slot

3. **First Carat: Growth Mode Overlay**
   - Scenario eligibility: Scenarios 1 (Market Expansion), 2 (New Product Launch), 21 (Opportunity Discovery)
   - Context injection: "Evaluate all options against growth ceiling metrics. Prioritize options that expand TAM or extend runway."
   - Constraint injection: none (this is a priming Carat, not a constraint Carat)
   - Priority: standard

4. **Carat audit trail**
   - Every Carat activation/suppression event appears in the session audit trail
   - Which Carats were eligible, which were activated, which were suppressed and why

**Note on arbitration:** Full Carat arbitration rules are a follow-on spec (`CARAT_ARBITRATION_RULES.md`). For Stage 9C, if two Carats conflict, escalate to operator. Do not silently resolve.

**Exit condition:**
- Growth Mode Carat activates correctly for eligible scenarios
- Carat context injection appears in context package before LLM call
- Carat activation event appears in audit trail
- Non-eligible scenarios do not load the Carat
- Existing tests pass

---

### Sub-Stage 9D: Compliance Cartridge Toggle

**What it builds:** The first compliance cartridge that can be toggled by a tenant admin — making compliance a runtime governance layer rather than hardcoded behavior.

**Current state:** Compliance cartridge architecture is fully specced. No compliance cartridge exists in runtime. The compliance slot in the context package is always empty.

**Deliverables:**

1. **Compliance cartridge object model**
   - Schema from `COMPLIANCE_CARTRIDGE_ARCHITECTURE.md`
   - Fields: cartridge_id, name, tier, active, constraints, audit_requirements, activation_timestamp, activated_by
   - Toggle: tenant admin level only — no operator or associate can toggle compliance state
   - Toggle event is auditable and timestamped

2. **First cartridge: HIPAA**
   - Constraints: PII handling rules, minimum necessary standard, breach notification requirement, PHI segregation
   - When active: first gate in judgment cascade before all other evaluation
   - Constraint injection: every LLM judgment call receives HIPAA constraints in compliance slot
   - Block conditions: any output that would produce a HIPAA-violating recommendation is blocked before delivery

3. **Second cartridge: SOC 2**
   - Constraints: data access logging, availability requirements, change management controls
   - Same toggle architecture as HIPAA

4. **Multi-compliance conflict handling**
   - If two compliance cartridges are active and produce contradictory constraints: escalate to tenant admin
   - Do not silently resolve; do not block all activity — escalate with explicit description of the conflict

5. **Admin endpoint**
   - `POST /compliance/toggle` — activate or deactivate a compliance cartridge (admin only)
   - `GET /compliance/active` — list currently active cartridges
   - `GET /compliance/audit` — log of all toggle events with actor and timestamp

**Exit condition:**
- HIPAA cartridge can be toggled by tenant admin
- When active, HIPAA constraints appear in every context package as the first slot
- LLM judgment call receives compliance constraints before scenario logic or Carats
- Toggle event is audited
- Non-admin cannot toggle compliance state
- SOC 2 cartridge works on same architecture
- Multi-compliance conflict correctly escalates rather than silently resolving

---

### Sub-Stage 9E: Cross-Session Persistent Memory

**What it builds:** Memory that persists across sessions — so the operator's governed admitted claims are available in every subsequent session, not lost when the session ends.

**Current state:** After sub-stage 9B, memory is admitted and stored. But each new session starts fresh — the activation pathway does not load memory from prior sessions. This is the gap.

**Deliverables:**

1. **Session memory initialization**
   - At session start, query the tenant's admitted memory store
   - Load all Active-state memory units into the session context
   - Dormant memory is not loaded but is available for explicit retrieval

2. **Memory weight updating**
   - After each session, update the weight/confidence of admitted memory units that were activated
   - Memory units that activated and proved relevant increase in confidence
   - Memory units not activated in N sessions begin dormancy promotion

3. **Governance gap escalation** (from PSA spec)
   - A proactive signal surfaced three times without operator resolution becomes a Governance Gap
   - Governance Gaps are flagged at session start: "This implication has been surfaced in three sessions without resolution."
   - Governance Gaps are stored in the memory system and persist across sessions

4. **Memory retrieval endpoint**
   - `GET /memory/active` — all Active-state memory units for current tenant
   - `GET /memory/governance-gaps` — all unresolved Governance Gaps
   - `POST /memory/resolve/<id>` — mark a Governance Gap as resolved (with resolution note)

**Exit condition:**
- Admitted memory from session 1 is available in session 2 without re-submission
- Active memory loads into context package at session start
- Dormant memory does not auto-load (must be explicitly retrieved)
- Governance Gap persistence works across sessions
- Memory weight updating is functional (confidence increases with activation)
- All memory operations are tenant-scoped (no cross-tenant access)

---

## Stage 9 Exit Condition (Complete)

Stage 9 is complete when:

1. EKE corpus entries load into the context package based on detected scenario
2. Governed memory admission pipeline is functional end-to-end (submit → six-test → admit → persist → activate in next session)
3. At least one Carat is operational and activates correctly for eligible scenarios
4. At least one compliance cartridge is toggleable by tenant admin and appears as first gate in judgment cascade
5. Memory persists across sessions and loads at session start
6. All five context package slots are populated in a complete session: compliance constraints, Carats, scenario logic, corpus entries, operator memory
7. Full audit trail covers all new components
8. All existing tests continue to pass

**What Stage 9 does not deliver** (later stages):
- Full Carat library (only one Carat; full library is a follow-on build)
- Complete EKE corpus classification (230 entries loaded, but EKE Thinker Registry and full per-scenario mapping are follow-on specs)
- Qualitative Formula Library runtime (far future)
- Network heuristic promotion (heuristics validated across tenants; architectural future)
- IFD and Bridge (product surfaces; future stages)

---

## Files Primarily Affected

| File | Change |
|---|---|
| `src/service/eke/corpus_loader.py` | New — seed corpus loader and scenario mapping |
| `src/service/eke/scenario_corpus_map.py` | New — scenario-to-corpus associations |
| `src/service/memory/admission.py` | New — six-test admission pipeline |
| `src/service/memory/storage.py` | New — memory storage model and retrieval |
| `src/service/memory/session_init.py` | New — session-start memory loading |
| `src/service/carats/registry.py` | New — Carat registry and activation check |
| `src/service/carats/growth_mode.py` | New — first Carat instance |
| `src/service/compliance/cartridge.py` | New — compliance cartridge toggle and enforcement |
| `src/service/compliance/hipaa.py` | New — HIPAA cartridge |
| `src/service/compliance/soc2.py` | New — SOC 2 cartridge |

---

## Spec Dependencies

Stage 9 is fully specced for sub-stages 9A–9D. Sub-stage 9E is specced in principle; cross-session persistence schema needs one additional follow-on spec.

| Component | Spec Location |
|---|---|
| EKE corpus schema and strata | `docs/architecture/EXECUTIVE_KNOWLEDGE_ENGINE_CORPUS_SCHEMA.md` |
| Seed corpus | `docs/corpus/EKE_MONOLITH_SEED_CORPUS.md` |
| Scenario-to-corpus mapping (starter) | `docs/architecture/REFLEX_AND_ACTIVATION_SYSTEM.md` §Scenario-to-Corpus Mapping |
| Memory admission doctrine | `docs/architecture/PERSISTENT_MEMORY_ADMISSION_AND_CLASSIFICATION_DOCTRINE.md` |
| Six-test admission filter | `CLAUDE.md §3` |
| Memory promotion ladder | `CLAUDE.md §8` |
| Carat registry standard | `docs/architecture/CARAT_REGISTRY_STANDARD.md` |
| Compliance cartridge architecture | `docs/architecture/COMPLIANCE_CARTRIDGE_ARCHITECTURE.md` |
| Governance Gap persistence | `docs/architecture/PROACTIVE_SOLUTIONS_ARCHITECTURE.md` §Proactive Signal Persistence |

---

## The Stage 9 Completion Picture

When Stage 9 is complete, the context package assembled by Stage 4 of the Activation Pathway will look like this for a real session:

```
{
  "compliance_constraints": [HIPAA_CARTRIDGE_CONSTRAINTS],   // if toggled
  "active_carats": [GROWTH_MODE_OVERLAY],                    // if scenario eligible
  "scenario_context": { COMPETITIVE_THREAT_SCENARIO },       // from detected scenario
  "active_reflexes": [BATNA_DIAGNOSTIC, FLANKING_FRAMEWORK], // from reflex gate
  "corpus_entries": [HTL-0023, HTL-0025, HTL-0132],         // from corpus loader
  "operator_memory": [MEM-0042, MEM-0031],                  // from admitted memory
  "prime_directive_frame": { VALUE_CLARITY_LENSES },         // always present
  "session_context": { TENANT_OPERATOR_METADATA }             // always present
}
```

This is what a fully operational Execalc judgment call looks like. Every slot is populated. The LLM is not reasoning from a blank page — it is reasoning within a prepared, governed, context-rich environment that reflects the organization's accumulated institutional intelligence.

**This is the product.**
