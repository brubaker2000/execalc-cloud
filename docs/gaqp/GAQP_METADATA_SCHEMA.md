# GAQP Governance Metadata Schema
**Status:** Canonized | **Version:** 1.0 | **Authority:** Execalc GAQP Standards Body

## Required Fields

| Field | Type | Purpose |
|---|---|---|
| claim_id | string | Unique identifier for retrieval and cross-referencing |
| claim_text | string | The statement itself — self-contained, standalone meaning |
| claim_type | enum | One of the 18 canonical types |
| domain | string | strategy / capital / operations / human behavior / governance |
| subdomain | string | More specific classification within domain |
| confidence_level | enum | Established / Probable / Contextual / Provisional / Disputed |
| provenance_source | string | Document, conversation, or institution of origin |
| provenance_author | string | Individual or body that produced the claim |
| activation_scope | enum | Universal / Domain-specific / Situational / Tenant-specific |
| activation_triggers | list | Conditions or signals that cause this nugget to fire |
| polarity | enum | Positive / Cautionary / Negative / Neutral / Mixed |
| durability_class | enum | Enduring / Medium-term / Ephemeral |
| evidence_status | enum | Observed / Argued / Inferred / Corroborated / Unverified |
| freshness_class | enum | Timeless / Date-sensitive / Event-bound / Expiring |
| composability_score | int | 0-100 — degree to which this claim combines cleanly with others |
| origin | enum | Internal / External / Mixed — whether the claim arises from inside or outside the organization; required for Strength, Weakness, Threat, and Opportunity; optional for other types |

## Optional Fields

| Field | Type | Purpose |
|---|---|---|
| counterclaim_links | list | Links to nuggets that dispute or qualify this claim |
| supporting_claim_links | list | Links to nuggets that corroborate or extend this claim |
| scenario_tags | list | Named scenarios that invoke this claim |
| tenant_scope | string | Universal or specific to a tenant namespace |
| rail_candidate | bool | Flag for elevation to the organizational knowledge rail |

## The Confidence Ladder

| Stage | Score | Meaning |
|---|---|---|
| Seed | 0.50 | First occurrence — baseline confidence |
| Developing | 0.72 | Second independent corroboration |
| Strong | 0.91 | Third corroboration — pattern confirmed |
| Structural | 1.00 | Threshold crossed — treated as established doctrine |

Three recurrences in independent sessions triggers structural threshold automatically.
