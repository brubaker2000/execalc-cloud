# GAQP Claim Relationship Graph

**Status:** Canonized | **Version:** 1.0 | **Authority:** Execalc GAQP Standards Body

---

## I. Purpose

The GAQP corpus is not a flat collection of independent claims. Claims relate to each other. Some support each other. Some contradict each other. Some depend on each other as premises. Some are refinements or specializations of more general claims.

The Claim Relationship Graph formalizes these relationships. It defines the edge types, their semantics, and the rules governing how relationships are created, maintained, and traversed.

---

## II. Existing Relationship Fields

The GAQP metadata schema already carries two relationship fields:

- `counterclaim_links` — claims that dispute or qualify this claim
- `supporting_claim_links` — claims that corroborate or extend this claim

These are the minimum viable graph. The full relationship vocabulary defined here extends them.

---

## III. Relationship Type Taxonomy

Each edge in the claim graph has a typed relationship. The type governs how the relationship is used during retrieval, reconstruction, and contradiction surfacing.

| Relationship | Direction | Meaning |
|---|---|---|
| `supports` | A → B | A provides evidence or logical grounding for B |
| `contradicts` | A ↔ B | A and B are in active logical conflict |
| `qualifies` | A → B | A adds a condition or scope limit to B — B remains valid within the constraint A specifies |
| `extends` | A → B | A adds scope or depth to B without contradiction |
| `depends_on` | A → B | A requires B to be true as a premise; if B is retracted, A must be reviewed |
| `supersedes` | A → B | A replaces B — B is archived, not deleted |
| `instantiates` | A → B | A is a specific case of the general claim B |
| `generalizes` | A → B | A is the general form; B is a specific instance |
| `corroborates` | A → B | A is an independent source that confirms B — used for confidence scoring |

---

## IV. Directed vs. Symmetric Relationships

**Symmetric:** `contradicts` — if A contradicts B, B contradicts A.

**Directed:** All others. The direction matters:
- `A supports B` does not mean `B supports A`
- `A depends_on B` does not mean `B depends_on A`
- `A supersedes B` is a one-way replacement

---

## V. Relationship Creation Rules

1. **Contradiction must be surfaced, not suppressed.** When a new claim is admitted that contradicts an existing corpus claim, the contradiction must be linked within the same ingestion event. See `GAQP_RUNTIME_ARCHITECTURE.md` for the contradiction surfacing engine.

2. **A claim may not contradict itself.** Two claims with the same fingerprint are duplicates, not contradictions.

3. **`supersedes` requires human authorization.** A machine may flag a potential supersession. Only an operator may commit the `supersedes` link and archive the prior claim.

4. **`depends_on` links create fragility obligations.** When a foundational claim (the dependency) is retracted or downgraded in confidence, all claims that `depends_on` it are automatically flagged for review.

5. **`corroborates` links drive confidence promotion.** The corroboration engine uses `corroborates` links to compute the `independent_sources` count and advance the confidence ladder.

---

## VI. Graph Traversal in Retrieval

When a claim is retrieved for a reasoning context, the graph is traversed to surface related claims. The traversal depth and relationship types included are governed by the retrieval mode:

| Retrieval mode | Traversal |
|---|---|
| `point` — single claim lookup | No traversal |
| `context` — claim in reasoning context | Depth 1: `supports`, `qualifies`, `contradicts` |
| `full` — deep retrieval for reconstruction | Depth 2: all relationship types |
| `dependency_check` | Depth unlimited: `depends_on` chains only |

---

## VII. Contradiction Resolution

A `contradicts` edge is not resolved by deletion. It is resolved by one of three operator-authorized outcomes:

| Resolution | Effect |
|---|---|
| **A is correct; B is retracted** | B is archived; `contradicts` link updated to `supersedes` |
| **B is correct; A is retracted** | A is archived; `contradicts` link updated to `supersedes` |
| **Both are valid in different contexts** | A `qualifies` link is added specifying the contextual scope; `contradicts` is removed |
| **Unresolved** | `contradicts` link remains; both claims carry a `struct:disputed` tag |

An unresolved contradiction is not a corpus error. It is an accurately represented state of knowledge.

---

## VIII. Graph Storage

In the V1 implementation, graph relationships are stored as JSONB arrays on the claim record:
- `counterclaim_links` — array of claim_ids with `contradicts` relationship
- `supporting_claim_links` — array of claim_ids with `supports` or `corroborates` relationship

The full typed graph (with all relationship types) is deferred to V2 where a dedicated `gaqp_claim_relationships` link table will store typed, directed edges with timestamps and actor provenance.

---

## IX. Governing Rule

> A corpus with no relationship graph is a collection of isolated assertions. A corpus with a governed relationship graph is a knowledge structure. The distinction is the difference between retrieval and reasoning.
