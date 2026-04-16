# RECURSIVE_ANALYSIS_MODEL.md

## Status
Draft v0.2 — Supersedes RECURSIVE_REINTEGRATION_MODEL.md (v0.1)

## Owner
Architecture / Core 7

## Position in Core 7
Framework 7 — The final framework. Operates both on each individual output before delivery and across sessions over time. It is last because it requires all preceding frameworks to have run — it cannot audit outputs that have not been produced.

---

## Canonical Definition

Recursive Analysis is Execalc's governed self-correction framework. It preserves decision lineage, detects drift, revalidates assumptions against current reality, audits heuristic performance over time, and injects corrective reflexes so judgment compounds instead of decays.

It is the only Core 7 framework that applies the governing logic to the system's own output rather than to external input. That self-referential structure is what makes it recursive.

---

## Why This Exists

Most systems either answer once and move on, or store history without auditing the reasoning that produced it. Both patterns lead to the same failure mode: silent decay. Heuristics go stale. Assumptions embedded in prior decisions stop being valid. Conclusions made under one set of conditions persist as if those conditions still hold.

Recursive Analysis exists to prevent that. Not by adding more analysis — but by applying the same analytical frameworks to the system's own outputs and stored logic, checking for drift, inconsistency, and degradation before they harden into bad doctrine.

Without Recursive Analysis, Execalc can reason well in a session but cannot compound judgment across sessions. With it, each session builds on validated prior work rather than merely appending to it.

> A system without Recursive Analysis can only be wrong silently. A system with Recursive Analysis is wrong visibly — and therefore correctable.

---

## The Two Operational Modes

Recursive Analysis operates in two distinct modes that address different time horizons:

**Mode 1 — Real-Time Reintegration**
Per output. After each judgment call completes and before the output is delivered to the operator, the output is evaluated against the governing frameworks that were active during that call. Catches output-level inconsistencies before delivery.

**Mode 2 — Longitudinal Drift Detection**
Across sessions. Periodically and trigger-based, the system evaluates whether prior judgments, encoded heuristics, and admitted memory remain valid against current conditions. Catches system-level degradation before it compounds.

These are not variations of the same operation. Mode 1 governs output fidelity. Mode 2 governs system integrity over time. Both are required.

---

## Mode 1: Real-Time Reintegration

### What It Does

After the Stage 5 Judgment Call produces its output, and before that output reaches the operator, Reintegration runs five checks against the complete output:

---

### Check 1: Prime Directive Alignment

All three Prime Directive lenses must be present and evaluated. If the output makes a recommendation that implicitly evaluates one lens but omits others, reintegration flags the omission.

- **Pass:** All three lenses appear; each is evaluated; the recommendation follows from their combined assessment
- **Flag:** One or more lenses were loaded but do not appear in the output reasoning
- **Block:** Recommendation contradicts an evaluated lens without acknowledging the contradiction

---

### Check 2: Polymorphia Consistency

If Polymorphia identified multiple valid dimensions, the output must acknowledge the dominant dimension and not silently suppress secondary dimensions.

- **Pass:** Dominant dimension reflected in output; secondary dimensions acknowledged or explicitly set aside with stated reasoning
- **Flag:** Secondary dimensions identified by Polymorphia do not appear anywhere in the output
- **Block:** Output makes claims inconsistent with the dominant dimension without explanation

---

### Check 3: Memory Consistency

Active admitted memory units may carry governed claims that constrain what the output can validly assert. The output must not contradict active memory without acknowledging the contradiction.

- **Pass:** Output is consistent with all active admitted memory
- **Flag:** Output tensions an admitted memory unit without acknowledging the tension
- **Block:** Output directly contradicts a Canonical-tier memory unit

---

### Check 4: Corpus Anchor Integrity

If the output cites a corpus entry, that citation must be accurate. If the output draws a conclusion that conflicts with a loaded corpus entry without explaining why that framework was set aside, reintegration flags it.

- **Pass:** All corpus citations accurate; no unexplained conflicts with loaded entries
- **Flag:** Conclusion conflicts with a loaded corpus entry without explanation
- **Block:** Output falsely attributes a claim to a corpus entry

---

### Check 5: Compliance Constraint Adherence

If compliance cartridges were active, every recommendation must pass their constraints.

- **Pass:** All recommendations consistent with active compliance cartridges
- **Block:** Any recommendation that would violate an active compliance constraint

---

### Reintegration Output Schema

```json
{
  "mode": "real_time_reintegration",
  "verdict": "pass | flag | block",
  "checks": {
    "prime_directive": { "result": "pass | flag | block", "notes": null },
    "polymorphia": { "result": "flag", "notes": "Secondary dimension D2 not addressed in output" },
    "memory_consistency": { "result": "pass", "notes": null },
    "corpus_integrity": { "result": "pass", "notes": null },
    "compliance": { "result": "pass", "notes": null }
  },
  "required_revision": "Address or explicitly set aside secondary dimension D2 before delivery.",
  "operator_disclosure": true
}
```

**Verdict definitions:**
- **Pass** — output proceeds to operator as-is
- **Flag** — output proceeds with a reintegration note disclosed to the operator
- **Block** — output does not proceed; system surfaces the blocking issue and requests a revised judgment call

---

### Operator Disclosure (Mode 1)

When `operator_disclosure: true`, the operator sees:

```
[REINTEGRATION NOTE]
This output was reviewed against governing logic. One item was flagged:
Secondary dimension (Market Maturation Reading, 61% confidence) was identified
but not addressed in the recommendation.

The recommendation stands. You may wish to consider whether this alternative
framing changes your read.
```

This is governance transparency — the operator sees what the system found when it reviewed its own output.

---

### What Mode 1 Is Not

Mode 1 is not a second opinion on the substance of the recommendation. It does not evaluate whether the recommendation is correct in the world. It evaluates whether the recommendation is consistent with the governing logic that was applied.

**Mode 1 governs process fidelity, not outcome accuracy.**

A recommendation can be factually incorrect and pass Mode 1. A recommendation can be factually correct and fail Mode 1. These are independent questions.

---

## Mode 2: Longitudinal Drift Detection

### What It Does

Mode 2 operates across sessions. It asks whether the assumptions, heuristics, and logic encoded in the system are still valid against current reality — and whether decisions made in prior sessions would still be made the same way today.

This is the recursive act in the deepest sense: the governing frameworks are applied not to external input but to the system's own accumulated logic. The question is not "is this output consistent?" but "is the machine itself still calibrated correctly?"

---

### Trigger Conditions

Mode 2 activates under four conditions:

| Trigger | Description |
|---|---|
| **Session start with active heuristics** | When a session begins, heuristics that have been active beyond their freshness window are flagged for revalidation |
| **Decision Outcome admission** | When a Decision Outcome artifact is admitted, it is evaluated against the heuristics that governed the original decision |
| **State change detection** | When new evidence conflicts with assumptions embedded in prior admitted decisions |
| **Scheduled audit** | Tenant-configurable periodic review of the heuristic library and high-confidence memory units |

---

### The Four Audit Targets

**1. Logic Lineage**
How a prior conclusion was reached. Every admitted decision carries its reasoning chain — the corpus entries that were loaded, the Polymorphia dimensions that were active, the PD lens evaluations that were performed. Mode 2 checks whether that reasoning chain remains intact and valid.

*What it catches:* A conclusion that was correctly reached under one set of corpus entries but which would be reached differently if evaluated today with updated or revised corpus entries.

---

**2. State Validity**
Whether the assumptions embedded in a prior decision still hold. Every governed decision implicitly assumes something about the state of the world. When those assumptions become outdated, the decision may no longer be sound even if it was sound when made.

*What it catches:* The Series B pattern — a capital raise was approved on a 2.5x growth assumption; six months later actual growth is 1.6x. Before the board meeting, Mode 2 flags that the original growth assumption should be revalidated before the decision is cited as precedent.

*Detection method:* Compare the activation tags of the assumptions embedded in the original decision against current evidence in admitted memory and recent observations. A material gap between assumed state and observed state triggers a revalidation flag.

---

**3. Heuristic Performance**
Whether encoded heuristics are producing the outcomes they predicted. The heuristic library is only as good as its track record. Mode 2 audits each heuristic against the Decision Outcomes that reference it.

*What it catches:* A heuristic that was valid under 2022 market conditions producing bad guidance in 2025 conditions. Or a heuristic whose confidence was set at Medium that has been validated by multiple Decision Outcomes and should be promoted to High. Or the reverse — a High-confidence heuristic whose associated Decision Outcomes show consistent underperformance.

*Lifecycle implications:* Mode 2 drives heuristic lifecycle management. A heuristic that repeatedly fails its associated Decision Outcomes is a liability, not an asset. It must be revalidated, re-weighted, or retired.

---

**4. System Drift**
Whether the system's outputs have silently shifted away from governing doctrine. This is the most subtle target. Drift does not announce itself. A system can produce fluent, confident, PD-aligned outputs that have gradually shifted in emphasis, framing, or analytical posture without any individual output being flagged.

*What it catches:* Pattern-level divergence that is invisible in any single output but visible across a sequence of outputs. For example: over twelve sessions, the system has consistently weighted supply/demand over risk/reward when the doctrine specifies equal evaluation. No single output was blocked. But the pattern is a drift.

*Detection method:* Audit trail analysis across sessions. Statistical review of PD lens activation patterns and check results. Operator-level reports on whether flagged patterns are consistent with governing doctrine.

---

### Corrective Reflex Injection

Mode 2 does not merely flag drift. It injects corrective reflexes into the system's active reasoning when drift is confirmed.

Corrective reflex types:

| Reflex Type | Trigger | Action |
|---|---|---|
| **Heuristic revalidation request** | Heuristic performance degradation detected | Flag heuristic as pending revalidation; reduce activation weight until reviewed |
| **Assumption staleness warning** | State validity gap detected | Surface warning at session start when relevant scenario is detected |
| **Logic lineage alert** | Prior decision referenced in new session under changed conditions | Disclose that prior decision was made under assumptions that may no longer hold |
| **Drift correction signal** | System-level pattern drift detected | Escalate to tenant admin for governance review |

---

### The Heuristic Lifecycle

Mode 2 is the quality-control layer for the heuristic library. Heuristics are not permanent. They have a lifecycle:

```
Encoded → Active → Audited → Validated / Flagged → Re-weighted or Retired
```

**Encoded:** A new heuristic enters the corpus. Confidence level set at initial value.

**Active:** The heuristic activates in sessions when its activation tags match. Decision Outcomes that reference it are linked back.

**Audited:** Mode 2 reviews the heuristic's track record against linked Decision Outcomes. Is the confidence level accurate? Is the heuristic still applicable in its tagged scenarios?

**Validated:** Decision Outcomes confirm the heuristic is performing as expected. Confidence may be promoted.

**Flagged:** Decision Outcomes show degradation. The heuristic is flagged for review. Activation weight is reduced pending re-evaluation.

**Re-weighted or Retired:** After review, the heuristic is either re-weighted with updated confidence and scope tags, or retired (moved to dormant status). Retired heuristics are not deleted — they become historical record. A retired heuristic may be reinstated if conditions change.

---

## Relationship to Decision Outcome Artifacts

Decision Outcomes are the primary empirical feed for Mode 2 drift detection.

Every governed decision is a prediction. The Prime Directive evaluation at decision time predicts "this will deliver value." The Decision Outcome records whether that prediction was accurate. Mode 2 reads those records.

This means the three-way compound is:
- Decision Artifacts record what was decided and why
- Decision Outcomes record what actually happened
- Recursive Analysis Mode 2 reads the gap between them and updates the system accordingly

Without Recursive Analysis, Decision Outcomes are institutional memory. With it, they are the feedback mechanism that makes the system calibrate.

---

## Relationship to Persistent Memory

Persistent Memory preserves what has been admitted. Recursive Analysis determines whether preserved logic is still worthy of trust.

Memory without recursive review becomes accumulation. Recursive Analysis is what keeps memory from becoming a graveyard of stale conclusions masquerading as current wisdom.

---

## Relationship to Proactive Solutions Architecture

PSA and Recursive Analysis are explicitly paired in the Core 7:

- **PSA generates motion** — it converts governed judgment into execution pathways and proactively surfaces implications
- **Recursive Analysis audits motion** — it checks whether the generated pathways and prior judgments remain valid over time

A PSA-generated execution pathway (including any cartridge it produces) is subscribed to Recursive Analysis. If the conditions that justified the pathway change, Mode 2 detects it and injects a corrective reflex.

PSA without Recursive Analysis produces momentum. With it, it produces calibrated momentum — motion that self-corrects rather than persists blindly.

---

## Distinction from Runtime Validation Protocols

| Component | Where | What |
|---|---|---|
| Runtime Validation Protocols (Support Stack) | At each intermediate reasoning step | Does each step follow from the previous step within constraints? |
| Recursive Analysis Mode 1 | On the complete output | Does the final output follow from the full governing framework as a whole? |
| Recursive Analysis Mode 2 | Across sessions over time | Is the governing logic itself still valid against current reality? |

These are complementary, not redundant. Step-level validation (Support Stack) catches reasoning errors during the judgment call. Output-level reintegration (Mode 1) catches framework inconsistencies in the completed output. Longitudinal drift detection (Mode 2) catches system-level degradation that neither of the above can see.

---

## Audit Requirements

Every Mode 1 activation must produce an audit record:
- Session and judgment call reference
- All five check results with notes
- Overall verdict
- Whether operator disclosure was triggered
- Whether a block caused a revised judgment call and the result

Every Mode 2 activation must produce an audit record:
- Trigger condition that initiated the audit
- Audit targets evaluated and findings
- Heuristics flagged for revalidation with reason
- Corrective reflexes injected
- Operator or admin notifications generated

---

## Design Principle

> Recursive Analysis is the moment the system holds itself accountable — not just to the operator, and not just for this output, but to the integrity of its own accumulated judgment over time.

Every other Core 7 framework operates on external input. Recursive Analysis operates on the system's own output and stored logic. It is the mechanism through which the system does not merely accumulate knowledge, but audits whether that knowledge remains worthy of trust.

A system with only the first six frameworks is a governed judgment engine. A system with all seven — including Recursive Analysis operating in both modes — is a governed learning architecture.
