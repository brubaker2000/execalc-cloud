# Algorithm Specification Template

This template is required before implementing any non-trivial reasoning or scoring logic.

---

## 1. Algorithm Name

Clear, stable name.

---

## 2. Purpose

What does this algorithm compute or decide?

Why is it necessary?

---

## 3. Inputs

List all required inputs:
- Data fields
- Object types
- Metadata
- Threshold parameters

Specify:
- Required vs optional
- Validation constraints
- Tenant binding requirements

---

## 4. Outputs

Define:
- Structured output schema
- Confidence score (if applicable)
- Traceability metadata
- Error states

---

## 5. Deterministic Steps

List the step-by-step logic.

Each step must be:
- Explicit
- Ordered
- Non-ambiguous

If probabilistic, define:
- Scoring logic
- Weighting model
- Confidence calculation method

---

## 6. Role Weighting (If Applicable)

If inputs come from multiple roles:
- Define weighting hierarchy
- Define normalization method
- Define bias mitigation rules

---

## 7. Thresholds

Define:
- Minimum activation threshold
- Heuristic promotion threshold
- Alert threshold
- Suppression threshold

Include rationale for each.

---

## 8. Failure Modes

Identify:
- False positives
- False negatives
- Sampling bias
- Model hallucination risk
- Edge case breakdowns

Define mitigation strategy.

---

## 9. Governance Constraints

Confirm:
- No cross-tenant leakage
- No unauthorized execution
- No self-escalation
- Proof requirements enforced

---

## 10. Test Cases

Provide:
- Minimum 3 valid test scenarios
- Minimum 1 failure scenario
- Expected outputs for each

These must be implemented as unit tests.

---

## 11. Versioning

- Version number
- Date created
- Author
- Change log (if updated)

No algorithm may move to production without versioning and test coverage.
