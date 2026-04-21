# SECURITY_POSTURE_AND_COMPLIANCE_DESIGNATION.md

## Status
Active — compliance designation pending

## Owner
Governance / Architecture

---

## Current Posture

Execalc is built to be enterprise-grade by construction. The architecture enforces tenant isolation, auditability, governed data access, and deterministic execution boundaries as structural properties — not as features to be added later.

The system is **compliance-ready**. It is not yet **compliance-certified**.

The distinction matters:

> Compliance-ready means the architecture does not preclude any major compliance regime. Compliance-certified means the system has been audited and attested under a specific standard.

Certification is a business decision that depends on the regulatory context of the first enterprise operators. This document records the current posture and locks the designation process so it happens deliberately rather than by drift.

---

## What Is Already Enforced by Architecture

The following properties are structural — they are enforced regardless of which compliance designation is eventually pursued:

| Property | Enforcement Mechanism |
|---|---|
| Tenant isolation | Hard — no cross-tenant reads, writes, memory, or connector access |
| Deny-by-default | No operation proceeds without verified tenant + actor context |
| Audit trail | Every request produces a traceable record (request ID, tenant, actor, policy decisions) |
| Memory governance | No implicit memory writes; all persistence is explicit and attributed |
| Connector scope | Read-only by default; action-capable tools require explicit enablement |
| Runtime/reasoning separation | Deterministic gates fire before any LLM invocation |
| Refusal logging | BLOCK and ESCALATE events are auditable outcomes |

These properties satisfy the foundational requirements of most major compliance regimes. The gap between current posture and formal certification is attestation and documentation — not architecture.

---

## Compliance Cartridge Registry (Registered, Not Yet Built)

The following compliance frameworks are registered as Tier 1 build targets in `COMPLIANCE_CARTRIDGE_ARCHITECTURE.md`. Each will be implemented as a modular cartridge that tenants activate based on their regulatory context.

**Tier 1 — Priority Build (when enterprise operator context is confirmed):**

| Framework | Relevance to Execalc |
|---|---|
| **SOC 2 Type II** | Primary enterprise trust requirement. Controls: security, availability, confidentiality, processing integrity. Most enterprise buyers will require this before procurement. |
| **HIPAA** | Required if any operator operates in healthcare or handles PHI. Architecture already supports the necessary isolation; cartridge formalizes the control set. |
| **GDPR** | Required for any EU operator or EU data subject. Data residency, right to erasure, processing records. |
| **CCPA / CPRA** | Required for California operators handling consumer data. |

**Tier 2 — Follow-On:**

| Framework | Context |
|---|---|
| SOX | Financial reporting controls for public company operators |
| FINRA | Registered investment advisors, broker-dealers |
| FERPA | Education sector operators |
| FCA (UK) | UK financial services operators |
| PCI-DSS | Any operator handling payment card data |

**Tier 3 — Future:**
ISO 27001, NIST CSF, FedRAMP (government procurement), ADA/WCAG (accessibility)

---

## Data Residency

No data residency constraints are currently defined. This is a pending designation.

When the first enterprise operator is confirmed, the following must be resolved:

1. **Geography** — Does operator data need to remain within a specific country or region (EU, US, Canada, etc.)?
2. **Cloud region** — Which cloud provider regions are permitted?
3. **Cross-region replication** — Is disaster recovery replication permitted across borders?
4. **Model inference location** — Does LLM inference need to occur within the same geography as stored data?

Until these are resolved, the system must not make infrastructure commitments (database hosting region, CDN configuration, backup location) that would require expensive migration to meet a residency requirement later.

**Build Law applies:** No v1 infrastructure decision shall preclude meeting data residency requirements in v2.

---

## Government and Enterprise Procurement

No government procurement requirements are currently in scope for v1.

If government or defense procurement becomes relevant, FedRAMP (US), NCSC Cyber Essentials (UK), or equivalent certifications will be required. These have long lead times and require architecture review before the path begins. Flag immediately if this context changes.

For enterprise procurement (non-government), SOC 2 Type II is the primary gate. Most Fortune 500 security review processes will not proceed without it. This should be the first certification pursued once the build is stable enough to begin the audit process.

---

## Compliance Designation Process

When the regulatory context of the first enterprise operator is confirmed, the following sequence applies:

1. **Designate** the applicable compliance frameworks from the Tier 1 registry above
2. **Activate** the corresponding compliance cartridge(s)
3. **Map** the cartridge controls to the existing architecture (most will already be satisfied)
4. **Gap-fill** any controls not yet implemented
5. **Engage** an auditor for attestation (SOC 2) or begin documentation (GDPR/HIPAA self-certification)

This process is designed to be additive, not disruptive. The architecture was built to accommodate it.

---

## What This Document Is Not

This document is not a compliance certification. It is not a legal representation of security posture. It is a governance record that:

- States current architectural properties
- Registers the compliance frameworks the system is designed to accommodate
- Locks the designation process so it does not happen informally
- Ensures no build decision inadvertently forecloses a compliance path

When formal certification is pursued, this document becomes the starting point for the auditor briefing.
