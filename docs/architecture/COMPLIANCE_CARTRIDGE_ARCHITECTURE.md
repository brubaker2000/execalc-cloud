# COMPLIANCE_CARTRIDGE_ARCHITECTURE.md

## Status
Draft v0.1

## Owner
Executive Knowledge Engine (EKE) / Governance Layer

## Purpose
This document defines the Compliance Cartridge class — a special-purpose runtime cartridge that encodes regulatory and compliance frameworks as governed, toggleable overlays within the Execalc judgment pipeline.

When a compliance cartridge is active, it becomes the highest-priority consideration in any deliberation. No judgment, recommendation, synthesis, or action pathway may proceed without first clearing the active compliance gate.

---

## The Core Design Principle

Compliance is not hardcoded into the Execalc system. It is a cartridge.

This means:
- Unregulated operators carry zero compliance overhead by default
- Regulated operators activate exactly the frameworks that apply to them
- The compliance layer is modular, auditable, and extensible
- New regulatory frameworks can be added without altering core system architecture

The base Execalc system is compliance-neutral. Compliance posture is a tenant-level configuration decision.

---

## Compliance Cartridge Class Definition

A Compliance Cartridge is a distinct subclass of the runtime cartridge family with the following properties that differentiate it from standard Carats and cartridges:

| Property | Standard Carat / Cartridge | Compliance Cartridge |
|---|---|---|
| Activation position in cascade | After scenario classification | **Before all other evaluation** |
| Effect on output | Influences synthesis | **Constrains synthesis** |
| Priority when active | Shares priority pool | **Overrides all other active cartridges** |
| Failure mode | Reduces confidence or changes emphasis | **Blocks or flags non-compliant output** |
| Toggle control | Operator-level | **Tenant admin-level** |
| Audit requirement | Standard | **Enhanced — every deliberation must record compliance gate result** |
| Conflict handling | Standard arbitration | **Compliance wins; conflicts between compliance cartridges require explicit resolution** |

---

## Runtime Cascade — Compliance Active

When one or more compliance cartridges are active, the judgment pipeline runs as follows:

```
Input
  → Compliance Gate (all active compliance cartridges evaluated first)
      → [BLOCK if non-compliant] or [PROCEED with compliance constraints loaded]
  → Scenario Classification
  → Carat / Cartridge Activation (standard)
  → EKE Corpus Activation
  → Prime Directive Evaluation (compliance constraints visible as inputs)
  → Synthesis
  → Output (compliance constraints surfaced in audit trail)
```

**Without active compliance cartridges:**
```
Input → Scenario Classification → Carat Activation → EKE → Prime Directive → Synthesis → Output
```

The compliance gate does not replace the Prime Directive. It precedes it. A compliant action may still fail the Prime Directive. A non-compliant action cannot pass the Prime Directive regardless of how favorable the other lenses are.

---

## Toggle Mechanism

Compliance cartridges are toggled at the tenant level by tenant administrators.

Toggle states:
- **Active** — compliance cartridge is live for all sessions in this tenant; highest priority
- **Dormant** — cartridge is configured but not enforcing; still visible in audit trail as dormant
- **Not configured** — cartridge does not exist in this tenant's configuration

Toggle events are themselves auditable. Every activation and deactivation is recorded with:
- who toggled it
- timestamp
- reason (optional but recommended)
- prior state

Toggle authorization requires tenant admin role. Operators cannot toggle compliance cartridges without admin permission.

---

## Compliance Cartridge Registry (v0.1)

The following compliance frameworks are the initial registry. Each becomes a buildable cartridge.

### Tier 1 — Priority Build

| Cartridge ID | Framework | Primary Audience | Key Constraints |
|---|---|---|---|
| COMP-HIPAA | HIPAA | Healthcare operators | PHI handling, data minimization, access controls, breach notification |
| COMP-SOC2 | SOC 2 (Type I / Type II) | SaaS / cloud operators | Security, availability, confidentiality, processing integrity, privacy |
| COMP-GDPR | GDPR | EU data subjects / EU operators | Consent, right to erasure, data portability, DPA requirements |
| COMP-CCPA | CCPA / CPRA | California operators / consumers | Right to know, right to delete, opt-out of sale |

### Tier 2 — Follow-On Build

| Cartridge ID | Framework | Primary Audience | Key Constraints |
|---|---|---|---|
| COMP-PCI | PCI-DSS | Payment processing operators | Cardholder data security, transmission controls |
| COMP-SOX | SOX | Public company operators | Financial reporting integrity, internal controls |
| COMP-FINRA | FINRA | Broker-dealer operators | Suitability, supervision, recordkeeping |
| COMP-FERPA | FERPA | Education operators | Student record privacy |
| COMP-FCA | FCA (UK) | UK financial operators | Conduct of business, consumer protection |
| COMP-ITAR | ITAR / EAR | Defense / export operators | Export controls, technology transfer |

### Tier 3 — Future

| Cartridge ID | Framework | Notes |
|---|---|---|
| COMP-ISO27001 | ISO 27001 | Information security management |
| COMP-NIST | NIST CSF | Federal / enterprise security framework |
| COMP-ADA | ADA / WCAG | Accessibility compliance |
| COMP-CUSTOM | Custom Regulatory | Tenant-defined regulatory framework |

---

## Minimum Compliance Cartridge Object

Every compliance cartridge must implement the following fields:

| Field | Description |
|---|---|
| `cartridge_id` | Stable unique identifier (e.g., COMP-HIPAA) |
| `name` | Canonical name |
| `framework_version` | Version of the regulatory framework encoded |
| `status` | draft / candidate / approved / deprecated |
| `jurisdiction` | Geographic or industry scope |
| `primary_constraints` | List of the highest-priority rules this cartridge enforces |
| `hard_blocks` | Actions that are unconditionally prohibited when this cartridge is active |
| `soft_flags` | Actions that trigger a compliance warning but are not unconditionally blocked |
| `data_handling_rules` | Specific requirements for data storage, transmission, access |
| `audit_requirements` | What must be logged when this cartridge is active |
| `conflict_rules` | How this cartridge resolves conflicts with other active compliance cartridges |
| `toggle_authority` | Minimum role required to activate / deactivate |
| `version` | Cartridge version for auditability |
| `last_reviewed` | Date of last regulatory accuracy review |

---

## Multi-Compliance Conflict Handling

Multiple compliance cartridges may be active simultaneously. When their requirements conflict (e.g., GDPR's right to erasure vs. HIPAA's retention requirements), the following rules apply:

1. **Identify the conflict explicitly** — the system must surface the conflict rather than silently choosing
2. **Apply the more restrictive requirement** — when two rules conflict, default to the stricter standard unless there is a jurisdiction-specific override
3. **Escalate unresolvable conflicts** — if no rule can satisfy both compliance frameworks simultaneously, escalate to tenant admin with an explicit description of the conflict
4. **Log the resolution** — every compliance conflict and its resolution must appear in the audit trail

Conflict resolution logic specific to each compliance cartridge pair will be encoded in `COMPLIANCE_CONFLICT_MATRIX.md` (follow-on spec).

---

## Relationship to the Prime Directive

Compliance constraints are visible to the Prime Directive evaluation as inputs.

Specifically:
- An active compliance cartridge's hard blocks become **liabilities** in the Assets/Liabilities lens — any action that would trigger a hard block is a structural liability
- Compliance risk surfaces in the **Risk/Reward** lens — non-compliant actions carry regulatory exposure as a downside factor
- Compliance constraints may affect the **Supply/Demand** lens — certain actions may be structurally unavailable due to regulatory prohibition

The Prime Directive does not override compliance. The Prime Directive evaluates within the compliance boundary.

---

## Relationship to EKE / Carats

When a compliance cartridge is active:
- No Carat may recommend an action that violates the active compliance framework
- Carats that conflict with active compliance constraints are suppressed or flagged
- The EKE corpus activation must load compliance-aware context before activating thinker or scenario logic

The compliance cartridge is the outermost boundary of the judgment system. It is not a peer of Carats — it outranks them.

---

## Audit Requirements

When any compliance cartridge is active, every session must produce an enhanced audit record containing:

- Which compliance cartridges were active
- Whether the compliance gate passed, flagged, or blocked
- What specific constraints were evaluated
- Whether any hard blocks were triggered
- Whether any multi-compliance conflicts occurred and how they were resolved
- Timestamp of compliance gate evaluation

This audit record must be immutable and tenant-isolated.

---

## Security Posture (Base System)

The base Execalc system — without any compliance cartridge active — operates under the following minimum security baseline:

- All data is tenant-isolated (no cross-tenant access)
- All API requests require authenticated identity
- All session data is scoped to the authenticated tenant
- Execution records are persisted with tenant_id and user_id attribution
- Dev harness is deny-by-default in production

This baseline is not a compliance certification. It is the floor. Compliance cartridges build above this floor.

---

## Current Limitations

The following are not yet specified:
- Formal compliance cartridge schema beyond this document
- COMP-HIPAA cartridge content (primary constraints, hard blocks, soft flags)
- COMP-SOC2 cartridge content
- COMPLIANCE_CONFLICT_MATRIX.md
- Toggle UI / admin interface
- Automated compliance testing against cartridge rules

---

## Required Follow-On Specs

1. `COMP_HIPAA_CARTRIDGE.md` — full HIPAA constraint encoding
2. `COMP_SOC2_CARTRIDGE.md` — full SOC 2 constraint encoding
3. `COMPLIANCE_CONFLICT_MATRIX.md` — conflict resolution rules for active multi-compliance configurations
4. `COMPLIANCE_AUDIT_SCHEMA.md` — formal audit record format for compliance gate events

---

## Design Principle

Compliance should feel like putting on a lens, not installing a cage.

When a compliance cartridge is active, the operator should feel that the system is protecting them — scanning every deliberation for exposure — not that the system is restricted. The cartridge adds intelligence, not friction.

The difference: a cage says "no." A compliance cartridge says "here is what this means for your exposure, and here is how to proceed within the boundary."
