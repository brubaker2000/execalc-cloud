# GAQP Tagging System

**Status:** Canonized | **Version:** 1.0 | **Authority:** Execalc GAQP Standards Body

---

## I. Purpose

Tags are the retrieval and cross-reference layer of the GAQP corpus. A claim without tags is findable only by its claim_type and domain. A claim with correct tags is findable by scenario, by counterparty, by sector, by regulatory framework, by decision context, and by any combination thereof.

The tagging system is what makes GAQP a searchable standard rather than a labeled filing cabinet.

---

## II. Tag Namespaces

Tags are organized into namespaces. Each tag carries its namespace prefix to avoid collision.

| Namespace | Prefix | Purpose |
|---|---|---|
| Scenario | `scenario:` | Decision scenarios that invoke this claim |
| Sector | `sector:` | Industry or sector classification |
| Counterparty | `cp:` | Named counterparty types or specific entities |
| Regulatory | `reg:` | Regulatory framework or jurisdiction |
| Temporal | `time:` | Temporal relevance marker |
| Structural | `struct:` | Structural role this claim plays in reasoning |
| Operator | `op:` | Operator-assigned free tags |

---

## III. Scenario Tags

Scenario tags identify the decision contexts in which a claim activates. They are the primary mechanism for context-aware retrieval.

**Canonical scenario tags:**

| Tag | Activates when |
|---|---|
| `scenario:draft_trade` | Player acquisition or trade decisions |
| `scenario:contract_negotiation` | Contract structuring decisions |
| `scenario:capital_allocation` | Investment and spending decisions |
| `scenario:feasibility` | Viability assessment decisions |
| `scenario:risk_review` | Risk identification and mitigation decisions |
| `scenario:competitive_positioning` | Market and competitive analysis |
| `scenario:vendor_selection` | Procurement and partner decisions |
| `scenario:org_design` | Organizational structure decisions |
| `scenario:fundraising` | Investor and financing decisions |
| `scenario:m_and_a` | Merger, acquisition, or partnership decisions |

A claim may carry multiple scenario tags.

---

## IV. Sector Tags

Sector tags enable cross-tenant corpus filtering and industry-calibrated retrieval. They use standard classification systems to remain interoperable.

**Primary classification systems supported:**

| System | Usage | Example |
|---|---|---|
| NAICS | North American industry classification | `sector:naics:711211` (sports teams) |
| GICS | Global Industry Classification Standard | `sector:gics:253010` (hotels, restaurants, leisure) |
| SIC | Standard Industrial Classification (legacy) | `sector:sic:7941` (professional sports clubs) |
| Custom | Tenant-defined sector labels | `sector:custom:nfl_franchise` |

For most claims, a single GICS code at the sub-industry level is sufficient.

---

## V. Structural Tags

Structural tags describe the logical role a claim plays in reasoning — independent of its claim_type. A `doctrine` claim and a `causal_claim` may both serve as foundational premises; a structural tag captures that role.

| Tag | Meaning |
|---|---|
| `struct:foundation` | This claim is a premise other conclusions rest on |
| `struct:constraint` | This claim limits the solution space |
| `struct:lever` | This claim identifies a controllable variable |
| `struct:signal` | This claim is an early indicator of a larger condition |
| `struct:decision_gate` | This claim must be resolved before a decision can proceed |
| `struct:canon_candidate` | This claim is nominated for elevation to governing doctrine |
| `struct:disputed` | This claim is in active contradiction with another |

---

## VI. Temporal Tags

Temporal tags indicate the time-sensitivity of a claim. They complement the `freshness_class` field by adding precision.

| Tag | Meaning |
|---|---|
| `time:timeless` | No expiry — governs regardless of when retrieved |
| `time:cycle_sensitive` | Relevant only within a specific business cycle |
| `time:quarter:{Q}:{YYYY}` | Relevant to a specific quarter |
| `time:expires:{YYYY-MM-DD}` | Hard expiry date |
| `time:event_bound:{event_slug}` | Relevant only until a named event resolves |

---

## VII. Tag Application Rules

1. **Every claim must carry at least one scenario tag.** A claim with no scenario context is not activation-ready.
2. **Sector tags are required for claims with `activation_scope: universal`.** Universal claims must declare their sector relevance.
3. **Structural tags are optional but recommended** for claims that serve as foundations or gates in a reasoning chain.
4. **Operator tags (`op:`) may be any string** and are not validated against a controlled vocabulary. They are for human navigation, not machine retrieval.
5. **Tags do not replace fields.** `claim_type`, `domain`, and `confidence_level` are authoritative. Tags extend retrieval — they do not substitute for proper classification.

---

## VIII. Tag Inheritance

When a rail artifact is deconstructed into second-order nuggets, the parent artifact's scenario and sector tags are inherited by each child nugget. The child may add tags but not remove inherited ones.

This ensures that second-order intelligence remains findable within the same retrieval context as the conversation that produced it.

---

## IX. Governing Rule

> A GAQP claim without scenario tags is incomplete. Tags are not metadata decoration — they are the retrieval contract that makes the claim usable. An untagged corpus is a corpus that cannot be governed.
