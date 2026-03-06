# Execalc Build Doctrine

## Core Build Principle

Execalc must not trade off plumbing against cognition.

Every new cognitive feature must sit on top of hardened operational rails.
Every new plumbing feature must unlock a visible intelligence behavior.

The system should not become:
- clever but fragile, or
- robust but strategically empty.

Build sequencing must preserve both:
- institutional-grade reliability
- meaningful decision intelligence expansion

## 1. Stabilize the Kernel with One Operator (PCG Tenant)
Ensure kernel stability with one operator in the PCG tenant. The focus is on deterministic decision-making, stable envelope generation, and governed output behavior.

## 2. Add Minimal Multi-User Inside PCG Tenant
Introduce a minimal multi-user test within the PCG tenant to verify role-based visibility, tenant isolation, and correct audit behavior across actors.

## 3. Build Integration Plumbing
Create the integration architecture first with harness connectors, ensuring data flows correctly before connecting to real external systems.

## 4. Test One Production Integration
Implement one external integration, testing full authorization, data ingestion, governance enforcement, and failure handling.

## 5. Onboard Additional Tenants (Pilot Phase)
Onboard a pilot tenant, ensuring proper isolation, scalability, and full functionality.

## 6. Operationalizing the System
Expand integrations and onboard additional tenants. This stage includes persistence hardening, operational defaults, and the transition from isolated reasoning to reusable decision infrastructure.

## 7. Comparative Decision Memory
After the persistence layer is stable, expand the system into comparative decision infrastructure.

Suggested sequence:
- 7A: Journal hardening in real use
- 7B: `/decision/compare`
- 7C: Multi-objective comparison logic

This stage is the bridge between robust plumbing and visible executive cognition.

## Future Layer Awareness
The Intelligent Front Door is now recognized as a future architectural layer, but it is not current build scope.
It should be developed only after the decision journal and comparative reasoning layer are sufficiently stable.

### Key Decision Rule
Every surface area added to the system must:
- test a failure mode that cannot be tested otherwise
- increase learning per unit of risk
- strengthen either operational reliability or visible intelligence
- ideally strengthen both
