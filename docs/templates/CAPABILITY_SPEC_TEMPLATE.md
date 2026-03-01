# Capability Specification Template

## 1. Capability Name
Clear, concise name.

---

## 2. One-Sentence Definition
What does this capability do?

---

## 3. Strategic Purpose
Why does this exist?
What executive problem does it solve?

---

## 4. Object Model
What is the unit of work?

Examples:
- Deal
- CommentCluster
- ClaimSignal
- ExecutiveThread
- ScenarioTrigger

Define:
- Required fields
- Optional fields
- Identity binding (tenant_id, operator_id, role, etc.)

---

## 5. Ingress Sources
Where does data come from?

- Public sources?
- Internal email?
- CRM?
- Document ingestion?
- API feeds?

Must specify:
- Envelope schema
- Validation rules
- Role-weighting requirements (if applicable)

---

## 6. Output Contract
What does Execalc produce?

Must define:
- Structured format
- Required metadata
- Confidence scoring
- Traceability requirements
- Scenario mapping (if applicable)

---

## 7. Governance & Risk Analysis

### Irreversible Actions
List any actions that cannot be undone.

### Proof Requirements
What constitutes proof before execution?

### Failure Modes
- False positives
- False negatives
- Political risk
- Legal risk
- Model risk

---

## 8. Tenant Isolation Requirements
Confirm:
- No cross-tenant leakage
- Namespaced storage
- Tenant-scoped credentials

---

## 9. Delegation Model
Does this require:
- Draft-only behavior?
- Execute behavior?

Where are approval gates?

---

## 10. Memory Impact
Does this capability:
- Create active memory?
- Create dormant memory?
- Promote heuristics?

Define metadata schema.

---

## 11. Required Spine Primitives
List the primitives required from Stages 2–4.

Examples:
- Envelope validation
- Role-weighted scoring
- Proof-gated transitions
- Connector sandboxing
- Kill-switch support

---

## 12. Minimal Viable Experiment
What is the smallest test to prove value?

### Success Metrics
- Accuracy
- Confidence calibration
- Adoption rate
- Time-to-decision improvement

### Falsification Criteria
What result would invalidate the hypothesis?

---

## 13. Status
- Exploration
- Approved
- Dormant
- Rejected

Must be versioned and committed before implementation.
