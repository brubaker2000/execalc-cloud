# GAQP Canon Revision 001
## Stakeholder Complaint Claim as the 19th Canonical Claim Type

**Status:** Canonized
**Revision ID:** GAQP-CR-001
**Date:** 2026-04-30
**Authority:** Execalc GAQP Standards Body
**Taxonomy version prior:** 1.0 (18 types)
**Taxonomy version after:** 1.1 (19 types)

---

## I. Governing Rationale

Complaint cannot be safely collapsed into Observation, Diagnostic Signal, or Event because its stakeholder provenance, failure directionality, aggregation behavior, and legal-operational implications require distinct runtime handling.

The decisive distinction is:

> A complaint is a stakeholder-originated failure assertion.

That phrase is the anchor. It separates the Stakeholder Complaint Claim from every existing type. All 18 prior types are analyst-sourced or institutionally-sourced — a reasoner making a claim about the world. A Stakeholder Complaint Claim is the affected party making the claim. That provenance difference changes routing, weighting, aggregation behavior, and legal handling in ways that metadata on an existing type cannot replicate.

---

## II. Claim Type Name

**Full name:** Stakeholder Complaint Claim
**Short name:** Complaint
**Type number:** 19

---

## III. Definition

A stakeholder-originated assertion that a product, service, policy, decision, or experience failed to meet expectation, caused harm, created dissatisfaction, or imposed an unreasonable burden. A Stakeholder Complaint Claim carries stakeholder provenance, may aggregate into pattern evidence, and may create legal, operational, reputational, or design significance depending on context.

---

## IV. Core Distinction

A Stakeholder Complaint Claim establishes two separable facts:

**1. The complaint exists.**
This is highly reliable when captured in a company system, regulator database, call log, warranty record, or legal filing. The system treats this as established upon admission.

**2. The underlying allegation is true.**
This requires validation, corroboration, trend analysis, or expert review. The system does not assert this from the complaint alone.

Execalc treats every Stakeholder Complaint Claim as stakeholder-originated evidence of claimed failure — not as confirmed truth. `verification_status` governs what reasoning the claim may participate in.

---

## V. Why Existing Types Are Insufficient

| Candidate Collapse Type | Why It Fails |
|---|---|
| **Observation** | Analyst-generated — a reasoner noticed something. A Stakeholder Complaint Claim is external — an affected party asserted something. The provenance is categorically different. |
| **Diagnostic Signal** | Defined as weak by construction. A complaint is a direct assertion of failure. One complaint may be weak; ten thousand complaints about brake failure are not a diagnostic signal — they are pattern evidence of a different order. |
| **Event** | Captures a time-bound occurrence with strategic significance. A regulatory investigation triggered by complaints is an Event. The individual complaints that produced it are governed material, not Events. |
| **Tendency** | A confirmed recurring pattern. A complaint is the atomic input from which Tendencies may be derived — it is not itself a Tendency. |

---

## VI. Required Metadata

In addition to standard GAQP metadata fields, every Stakeholder Complaint Claim requires:

| Field | Type | Purpose |
|---|---|---|
| complainant_type | enum | customer / employee / regulator / counterparty / public |
| affected_party_status | string | Individual, class, regulator, advocacy body, etc. |
| complaint_channel | enum | warranty / call log / regulator filing / legal / social / dealer / survey |
| alleged_failure_type | string | Safety / quality / performance / policy / service / experience |
| harm_type | enum | physical / financial / reputational / operational / regulatory / experiential |
| severity_level | enum | Critical / High / Medium / Low / Unclassified |
| regulatory_status | enum | Formal / Informal / Under investigation / Closed |
| resolution_status | enum | Open / Resolved / Escalated / Disputed / Withdrawn |
| verification_status | enum | Unverified / Corroborated / Validated / Disputed |
| duplicate_or_cluster_id | string | Links individual complaint to its cluster object |
| source_system | string | NHTSA / CRM / warranty DB / legal / social monitor / etc. |
| received_at | datetime | When the complaint entered the system of record |

---

## VII. Aggregation Rule

Volume does not belong on the individual complaint. Volume belongs on the Complaint Cluster.

One atomic complaint remains one atomic nugget. The system does not inflate an individual claim with aggregate weight. Once multiple complaints cluster together, the cluster object carries volume, scope, and pattern data. The cluster then produces higher-order governed claims through the standard GAQP promotion path.

---

## VIII. Three-Tier Architecture

```
Individual Complaint (Stakeholder Complaint Claim)
  └── Single stakeholder-originated failure assertion
      Atomic. One nugget. Carries full metadata.

Complaint Cluster
  └── Multiple similar complaints grouped by:
      product / issue / geography / channel /
      time period / severity / affected class
      Volume count belongs here.

Derived Pattern Claim (existing GAQP types)
  └── Complaint Cluster promotes to one or more of:
      · Tendency               (confirmed recurring pattern)
      · Threshold Condition    (volume or severity tipping point)
      · Institutional Precedent (resolved cluster with forward-governing force)
      · Causal Claim           (cluster establishes X drives Y failure)
      · Observation            (early cluster, pattern not yet confirmed)
```

Note: "Legal Exposure Signal" and "Design Failure Signal" are not new claim types. A complaint cluster that creates legal or design exposure routes to a **Threshold Condition** with `harm_type` and `regulatory_status` metadata carrying the legal and design context. This preserves taxonomy discipline.

---

## IX. Activation and Routing Implications

- Complaints with `severity_level = Critical` and `harm_type = physical` activate escalation regardless of volume.
- Complaint Clusters crossing a defined volume threshold are candidates for automatic promotion to Threshold Condition.
- Complaints with `regulatory_status = Formal` carry elevated authority and route to compliance-aware reasoning paths.
- `verification_status = Unverified` constrains composability — unverified complaints may not compose directly into Causal Claims without corroboration.

---

## X. Market Significance — Complaint Intelligence

The Stakeholder Complaint Claim type establishes **Complaint Intelligence** as a named Execalc vertical.

Every regulated industry generates complaint data at scale. Most of it is trapped as noisy text, ticket logs, call notes, warranty codes, and legal residue. GAQP governance turns that corpus into structured, classified, traceable signal.

**Target verticals:**
- Automotive (warranty claims, NHTSA filings, dealer feedback)
- Pharmaceutical (adverse event reports, FDA submissions, patient complaints)
- Financial services (CFPB filings, customer disputes, arbitration records)
- Healthcare (patient complaints, incident reports, CMS data)
- Aviation (FAA reports, passenger complaints, maintenance logs)
- Medical devices (MDR filings, post-market surveillance)
- Consumer products (CPSC complaints, return data, social signal)
- Utilities and government agencies

**Canonical use case:** An automotive manufacturer synthesizes warranty claims, regulator filings, dealer feedback, and customer service logs into governed Stakeholder Complaint Claims — enabling legal and design teams to detect Threshold Conditions before they become Institutional Precedents or litigation events.

---

## XI. Canon Revision Process Record

1. Concept originated in ideation session — 2026-04-30
2. Exclusion analysis conducted against all 18 existing types
3. Governing rationale formalized
4. Definition, metadata schema, three-tier architecture developed and reviewed
5. External review confirmed: "This is not a side issue. It opens a major application layer."
6. Caution applied: no secondary new types invented in derived paths
7. Canonized and committed to repo

Per the GAQP Founding Charter: the taxonomy is locked except through explicit canon revision with documented rationale. This document constitutes that rationale. The taxonomy is updated to version 1.1.
