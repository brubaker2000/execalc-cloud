# Execalc Canon

This folder contains the system's durable, versioned operating canon.
Anything "locked" must land here (or be referenced here) and be enforced by tests where possible.

## Canonical map
- INVARIANTS.md — non-negotiable system truths (must not drift)
- DECISIONS.md — architectural decisions and rationale (ADR-lite)
- SECURITY.md — security posture, threat model highlights, and hard rules
- RUNBOOKS/ — operator and deployment runbooks
- db/schema.sql — canonical persistence schema
- cloud-run/ — deployment snapshots

## Rule
If it matters tomorrow, it must be written here today.
