# Stage 9A-0: Architecture Lock

**Status:** Canonized  
**Version:** 1.0  
**Date:** 2026-05-03  
**Authority:** Execalc Architecture / Players Capital Group  
**Purpose:** Settle all design decisions before any Stage 9 code is written.

---

## The Doctrine

Stage 9 is the moment GAQP becomes executable.

Its job is not to remember prior decisions. Its job is to convert decision artifacts into governed qualitative claims that can be admitted, scored, contradicted, corroborated, activated, and reused.

> The admission gate protects quality.  
> The fingerprint protects idempotency.  
> The visibility tier protects tenant trust.  
> The corroboration profile protects truth from repetition.  
> The contradiction model protects Polymorphia.  
> The rail integration protects operator visibility.

---

## The Canonical Flow

```
DecisionReport
    → Claim Candidate
    → GAQP Admission Test (seven tests, sequential)
    → Admitted / Rejected / Needs Review
    → Corpus (gaqp_claims)
    → Future Activation
```

Every claim that enters the corpus has passed the seven admission tests defined in `GAQP_ADMISSION_TESTS.md`. A claim that fails any test does not enter. There is no shortcut path into the corpus.

---

## Settled Decisions

### 1. What qualifies as a GAQP claim candidate

A claim candidate is any discrete, self-contained assertion extracted from a `DecisionReport` field that can be separated from its source without losing meaning.

The `DecisionReport` extraction surface for Stage 9B:

| Source field | Extraction method | Expected claim types |
|---|---|---|
| `value_assessment` | Direct — one candidate per field | Judgment, Tradeoff, Risk |
| `risk_reward_assessment` | Direct | Risk, Tradeoff |
| `supply_demand_assessment` | Direct | Market, Constraint |
| `asset_assessment` | Direct | Strength, Opportunity |
| `liability_assessment` | Direct | Weakness, Threat, Constraint |
| `incentives` | Direct — one candidate per list item | Incentive, Priority |
| `asymmetries` | Direct — one candidate per list item | Asymmetry, Leverage |
| `tradeoffs.key_tradeoffs` | Direct — one candidate per item | Tradeoff |
| `confidence_rationale` | Direct — one candidate per item | Evidence, Judgment |
| `executive_summary` | Deferred to v2 — requires LLM decomposition | Mixed |

List fields extract atomically. Paragraph fields extract as single candidates in v1. LLM decomposition of paragraph fields is explicitly deferred.

---

### 2. Admission criteria

The seven admission tests in `GAQP_ADMISSION_TESTS.md` apply unchanged. Tests are sequential. Failure at any test terminates evaluation for that candidate.

A candidate that passes all seven tests receives `admission_status: admitted`.  
A candidate that fails tests 1–4 receives `admission_status: rejected`.  
A candidate that fails only tests 5–7 receives `admission_status: needs_review` and is held for operator evaluation.

---

### 3. What confidence means

Confidence tracks corroboration state, not authorial certainty.

The GAQP ladder governs. The prior metadata schema confidence taxonomy (Established / Probable / Contextual / Provisional / Disputed) is superseded for Stage 9 purposes by the ladder:

| Level | Score | Meaning |
|---|---|---|
| Seed | 0.50 | First admission — baseline |
| Developing | 0.72 | Second independent corroboration |
| Strong | 0.91 | Third corroboration — pattern confirmed |
| Structural | 1.00 | Institutional doctrine threshold crossed |
| Disputed | — | Contradicting claims present; score paused |

All newly admitted claims enter at Seed (0.50). Score rises only through independent corroboration, never through repetition by the same source.

---

### 4. Corroboration is not repetition

Corroboration requires independence. A `corroboration_profile` field tracks the distinction:

```
corroboration_profile: {
    corroboration_count: int,       # total corroborating events
    independent_sources: int,       # distinct tenant+user combinations
    same_tenant_count: int,         # within-tenant repetitions (weak signal)
    cross_tenant_count: int,        # cross-tenant matches on structural claims
    contradictions: int,            # active contradicting claims
    last_corroborated_at: datetime
}
```

The confidence score advances only when `independent_sources` increases. Same-source repetitions increment `corroboration_count` but do not advance the score. A contradiction increments `contradictions` and sets `confidence_level` to Disputed until resolved.

---

### 5. Contradictions are stored, not erased

The corpus holds tension. Two claims that assert opposite things in different contexts can both be admitted and both be correct.

`contradiction_refs` is a list of `claim_id` values for claims that contradict or qualify this one. `support_refs` is a list of `claim_id` values for claims that corroborate or extend it.

When a new claim is admitted, the extraction pipeline checks for existing claims of the same `claim_type` and overlapping `activation_scope`. Matches are surfaced for operator review, not auto-resolved.

---

### 6. Tenant visibility: three tiers

| Tier | Label | Meaning |
|---|---|---|
| 1 | Private | Specific to one user or decision. Never shared. |
| 2 | Tenant | Reusable within one organization. Not visible cross-tenant. |
| 3 | Structural | De-identified, generalizable. Eligible for cross-tenant corroboration. |

`corpus_scope` stores one of `private`, `tenant`, `structural`.

All newly extracted claims default to `tenant`. Promotion to `structural` requires explicit operator admission (Memoralize path) or governance review. Demotion to `private` is always available.

Cross-tenant corroboration applies only to `structural` claims. The network effect compounds in the Structural tier only.

---

### 7. Fingerprinting and idempotency

Every claim has a deterministic fingerprint computed at extraction time:

```
fingerprint = sha256(
    tenant_id
    + source_envelope_id
    + claim_type
    + normalized_content       # stripped, lowercased, punctuation-removed
    + activation_scope
    + schema_version
)
```

If a claim with the same fingerprint already exists in the corpus, the extraction pipeline skips insertion. This guarantees that running the backfill against existing Postgres decision records multiple times does not duplicate corpus entries.

---

### 8. Activation contract

Activated claims surface as visible context, not as silent prompt material.

When the activation engine retrieves relevant claims for an incoming scenario, the result is a structured `ActivationBundle` passed alongside the `DecisionReport`, not injected into it:

```
ActivationBundle: {
    activated_claims: List[GAQPClaim],
    activation_rationale: List[str],   # why each claim matched
    corpus_scope: str,                 # private / tenant / structural
    confidence_floor: float            # minimum score threshold used
}
```

The decision engine may read the bundle and incorporate it. The operator sees it in the right rail. It never silently overrides the decision output. `DecisionReport` itself is not modified.

---

## Python Model: Required Fields

The Stage 9A Python dataclass must include all fields below. Fields marked `[json]` may be stored as JSON columns in Postgres v1 but belong in the model now.

```
claim_id                str          — stable UUID
claim_type              str          — one of 24 GAQP canonical types
content                 str          — self-contained claim text
domain                  str          — strategy / capital / operations / human behavior / governance
confidence_level        str          — Seed / Developing / Strong / Structural / Disputed
confidence_score        float        — 0.50 / 0.72 / 0.91 / 1.00
provenance              dict [json]  — source_kind, source_ref, actor_id, envelope_id
activation_triggers     list [json]  — conditions that cause this claim to fire
activation_scope        str          — Universal / Domain-specific / Situational / Tenant-specific
admission_status        str          — admitted / rejected / needs_review
corpus_scope            str          — private / tenant / structural
fingerprint             str          — deterministic sha256 hash
corroboration_profile   dict [json]  — see Section 4
contradiction_refs      list [json]  — claim_ids of contradicting claims
support_refs            list [json]  — claim_ids of corroborating claims
schema_version          str          — "stage9_v1"
tenant_id               str          — ownership boundary
source_envelope_id      str          — originating decision artifact
extraction_method       str          — direct_field / llm_decomposed / operator_memoralized
created_at              datetime
updated_at              datetime
```

---

## Postgres Strategy

**v1: single table.**

One `gaqp_claims` table. Complex fields (`provenance`, `activation_triggers`, `corroboration_profile`, `contradiction_refs`, `support_refs`) stored as JSONB columns.

Additional tables (`gaqp_claim_links`, `gaqp_claim_sources`, `gaqp_activation_events`) are deferred to v2 once the claim object is stable under real workload. Do not build link tables speculatively.

Indexes required at v1: `(tenant_id, claim_type)`, `(fingerprint)` unique, `(corpus_scope, confidence_score)`, `(source_envelope_id)`.

---

## Build Sequence

| Sub-stage | Deliverable | Dependency |
|---|---|---|
| 9A | `GAQPClaim` Python dataclass + `ActivationBundle` | This doc |
| 9B | Extraction pipeline: `DecisionReport → List[GAQPClaim]` | 9A |
| 9C | Postgres schema + write path + idempotency | 9A |
| 9D | Activation engine: scenario in → `ActivationBundle` out | 9B, 9C |
| 9E | Orchestration rail integration: bundle surfaced to operator | 9D |
| Backfill | Run 9B+9C against all existing `execution_records` | 9C stable |

---

## Explicitly Out of Scope for Stage 9 v1

- Semantic / embedding-based claim matching
- LLM decomposition of paragraph-level fields
- `gaqp_claim_links` relational table
- Automatic corpus-wide triangulation
- Cross-tenant corpus search UI
- Claim lifecycle automation (expiration, promotion rules)

These belong in Stage 10 or later. Stage 9 ships a clean, inspectable, deterministic loop first.
