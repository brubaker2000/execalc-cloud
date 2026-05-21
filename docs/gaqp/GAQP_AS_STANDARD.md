# GAQP as a Standard: Separation Doctrine

**Status:** Canonized | **Version:** 1.0 | **Authority:** Execalc GAQP Standards Body

---

## I. The Core Distinction

GAQP (Governed Analytical Quality Protocol) is a standard. Execalc is an implementation of that standard.

These are not the same thing. They must not be treated as the same thing.

**GAQP governs:** How qualitative claims are formed, typed, classified, scored, corroborated, stored, retrieved, and promoted to canon. These rules are independent of any platform.

**Execalc implements:** The runtime, storage, reasoning engine, and interface that operationalizes GAQP inside a governed decision environment. Execalc is GAQP-compliant. It is not GAQP itself.

---

## II. Why This Distinction Matters

If GAQP and Execalc are collapsed into one thing, three failure modes follow:

**1. Portability is destroyed.** GAQP claims must be exportable, transferable, and readable outside of Execalc. If the standard is fused with the implementation, a GAQP corpus becomes a proprietary data format rather than a standards-compliant knowledge artifact.

**2. Third-party adoption is blocked.** GAQP-the-standard can be adopted by consulting firms, investment analysts, and enterprise intelligence platforms without using Execalc. GAQP-the-Execalc-feature cannot.

**3. Credibility is undermined.** A standard that only one platform implements is not a standard. It is a product feature with a formal-sounding name. The separation preserves the legitimacy of GAQP as a governing framework.

---

## III. What GAQP Owns

The following belong to the GAQP standard, not to Execalc:

- The 24 canonical claim types and their definitions
- The admission test battery (seven tests)
- The confidence ladder (Seed → Single Source → Developing → Corroborated → Structural)
- The metadata schema (all required and optional fields)
- The corroboration rules (independence criterion, actor key definition)
- The durability class taxonomy (Enduring / Medium-term / Ephemeral)
- The activation scope taxonomy (Universal / Domain-specific / Situational / Tenant-specific)
- The evidence status taxonomy (Observed / Argued / Inferred / Corroborated / Unverified)
- The canon revision process (human approval required for structural elevation)
- The 10 Core Principles

These are published in `docs/gaqp/` and constitute the GAQP standards corpus.

---

## IV. What Execalc Owns

The following belong to Execalc, not to GAQP:

- The decision loop engine and its GAQP activation layer
- The Qualitative Capture Runtime and its five-layer pipeline
- The Executive Rail and its card types
- Persistent Executive Memory (PEM) and its admission rules
- The tenant namespace model and isolation guarantees
- The contradiction surfacing engine
- The corroboration engine implementation
- All API contracts, database schemas, and service interfaces

Execalc is GAQP-compliant. That is a relationship, not an identity.

---

## V. The Relationship Model

```
GAQP Standard
  ↓ governs
Execalc Runtime
  ↓ implements via
  - GAQP Extraction Engine
  - GAQP Corpus (gaqp_claims table)
  - GAQP Corroboration Engine
  - GAQP Contradiction Engine
  - GAQP Activation Layer
  - QCR Deconstructor (produces GAQP-compliant atomic nuggets)
  - PEM (admits GAQP-class memory objects)
```

---

## VI. Publishing Implication

GAQP documentation should be written as if addressed to a practitioner who does not use Execalc. The standard must be self-contained and implementable independently.

Execalc documentation may reference GAQP freely. GAQP documentation should reference Execalc only as an example implementation, not as the authoritative surface.

---

## VII. The Governing Statement

> GAQP is not an Execalc feature. Execalc is a GAQP-compliant platform.
> The standard is separable. The implementation is not the standard.
