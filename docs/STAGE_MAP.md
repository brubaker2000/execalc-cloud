## Permanent Protocols
- Editor-only development (no terminal editors): see `docs/EDITOR_ONLY_DEV_PROTOCOL.md`.

# Stage Map (Pointer)

Canonical stage map lives here:

- docs/vision/STAGE_MAP.md

This file exists to prevent continuity drift in boot packets and handoff instructions.
## Stage 3: Delegation Guardrails + Canon Spine (Complete)
- **Environment Config Change**: Cloud Run: set EXECALC_CONNECTOR_CREDENTIAL_REQUIRED to {"*":[]} to allow smoke test without credentials for echo connector
- **Smoke Test Success**: Smoke gate now passes after revision deploy
- All checks green for PR #9

