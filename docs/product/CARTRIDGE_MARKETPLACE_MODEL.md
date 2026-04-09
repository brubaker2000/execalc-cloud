# Cartridge Marketplace Model

## Purpose

This document defines the cartridge marketplace as a distinct business model layer within the Execalc platform.

Cartridges are domain-specific governed logic bundles that extend the Executive Knowledge Engine corpus for a specific industry, function, scenario type, or operator context.

---

## The Core Idea

The Execalc platform sells governed cognition capability.

The cartridge marketplace sells **pre-packaged domain expertise** that activates within that governed environment.

The analogy: the "For Dummies" series did not create expertise from scratch. It packaged existing domain knowledge into an accessible, structured format that non-experts could use immediately.

Execalc cartridges do the same thing — except the knowledge activates at runtime, triggered by scenario detection, not by a human flipping to the right chapter.

---

## What a Cartridge Is

A cartridge is a versioned, governed logic bundle containing:

- domain-specific frameworks
- heuristics tested against real-world operational contexts
- scenario activation triggers
- decision cues and operating notes
- expected outputs for each applicable scenario
- conflict notes (where this cartridge's logic may clash with general frameworks)
- source provenance and confidence metadata

A cartridge is not a document. It is a callable knowledge module.

---

## Activation Model

Cartridges do not wait for the operator to invoke them manually.

The system detects a scenario signature and activates the matching cartridge automatically.

Example:
- A grief counselor opens a session with language suggesting a client in acute distress
- The grief counseling cartridge activates
- The system applies grief-specific protocols, heuristics, and carats before producing output
- The operator receives guidance pre-loaded with domain context they did not have to request

This is the heuristic-trigger model: **the cartridge fires when the situation matches, not when the user asks.**

---

## Example Cartridge Domains

Cartridges can be created for any domain where expertise follows recognizable patterns:

**Professional services:**
- Grief counseling protocols
- Legal intake and triage
- Financial advisory best practices
- Medical consultation heuristics

**Sales and revenue:**
- Auto dealership sales cadence
- Enterprise software sales playbooks
- Commercial real estate negotiation

**Coaching and performance:**
- Football game-week preparation
- Executive performance coaching
- Athletic recovery and periodization

**Organizational operations:**
- Crisis communications
- M&A due diligence
- Board preparation
- Fundraising cadence

The pattern: any domain where an expert advisor would be called frequently, where the situations are recognizable, and where best practices are learnable and encodable.

---

## The Two-Sided Marketplace Model

### Side 1 — Cartridge Creators
Domain experts, consulting firms, training organizations, and publishers can build and submit cartridges.

Requirements:
- Cartridges must conform to the EKE corpus schema
- Cartridges must pass a GAQP-governed certification review
- Activation triggers must be explicit and testable
- Source provenance must be declared

### Side 2 — Cartridge Consumers
Operators and organizations purchase cartridges from the marketplace and load them into their tenant environment.

Purchased cartridges:
- are tenant-scoped (not shared with other tenants)
- activate automatically based on their trigger definitions
- can be combined with other cartridges and the base Monolith
- can be updated by the creator when versioned revisions are released

---

## Certification as a Governed Act

Execalc certifies cartridges before they appear in the marketplace.

Certification evaluates:
- schema conformance
- trigger accuracy (does the trigger actually match the intended scenario?)
- internal consistency (do the heuristics conflict with each other?)
- provenance legitimacy (is the source credible?)
- GAQP compliance (does the cartridge meet admission standards?)

Certification is itself a GAQP-governed act — not a subjective editorial judgment.

---

## Revenue Model

| Stream | Description |
|---|---|
| Platform seat license | Dashboard access — separate from cartridge market |
| Cartridge purchase | Operator buys domain cartridge from marketplace |
| Marketplace take rate | Execalc retains a percentage of each cartridge sale |
| Certification fee | Creator pays for GAQP certification review |
| Enterprise bulk licensing | Org purchases cartridge library access for all seats |

---

## Relationship to the EKE Corpus

The EKE corpus has two layers:

**The Monolith** — the shared baseline of general executive frameworks, maintained by Execalc, available to all tenants.

**Cartridges** — tenant-specific or purchased domain bundles that extend or specialize the Monolith for a given context.

The marketplace is the distribution and governance mechanism for the cartridge layer.

---

## Strategic Implication

The cartridge marketplace creates a compounding platform dynamic:

1. More cartridge creators produce more domain coverage
2. More domain coverage makes the platform more valuable to more operator types
3. More operator types increase the platform's addressable market
4. Execalc's certification role becomes a quality moat — not all platforms can certify governed logic

This is structurally similar to the App Store model — but the "apps" are governed knowledge modules, not software features, and the certification standard is GAQP, not an arbitrary editorial policy.

---

## Thesis

The cartridge marketplace is not an add-on to Execalc. It is a second revenue layer that compounds the platform's value with every new domain covered.

The platform provides the governed environment. The marketplace provides the domain depth. Together they make Execalc useful to a far wider range of operators than any single set of general frameworks could serve.
