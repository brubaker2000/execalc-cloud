# Execalc Cloud v1

Execalc is an executive-grade cognition platform designed to sit above large language models and govern their use through structured judgment, principled constraints, and auditable decision logic.

This repository is the canonical Cloud v1 trunk.

## Purpose
- Establish a governed, production-grade cloud foundation
- Enforce decision quality through explicit principles (value creation, asymmetry, risk discipline)
- Treat LLMs as substrates, not authorities
- Enable secure, multi-tenant executive cognition at enterprise scale

## Status
Cloud Version 1 — initial scaffold.
Architecture, protocols, and governance are locked prior to implementation.

## Non-Goals
- This is not an agent playground
- This is not prompt engineering
- This is not an experimentation sandbox

All additions to this repository must respect:
- Governance before capability
- Determinism before scale
- Auditability before speed

---
Execalc: industrial-grade organizational cognition.

## Gcloud crash recovery in Cloud Shell

### Symptom
`gcloud` crashes with:
`TypeError: string indices must be integers, not 'str'`

This can show up on commands like:
- `gcloud run deploy ...`
- `gcloud builds submit ...`
- `gcloud auth print-access-token ...`

### Likely cause
A corrupted or inconsistent local gcloud config/state in the active `CLOUDSDK_CONFIG` directory.

### Fast fix (isolate to a clean config directory)
1. Create a clean config directory and point gcloud at it:
   - `mkdir -p "$HOME/.config/gcloud-execalc-clean"`
   - `export CLOUDSDK_CONFIG="$HOME/.config/gcloud-execalc-clean"`

2. Authenticate (Cloud Shell is usually already authenticated, but this forces a usable local state):
   - `gcloud auth login j.brubaker@playerscapital.net --brief`

3. Set the project explicitly:
   - `gcloud config set project execalc-core`

4. Verify gcloud is healthy:
   - `gcloud auth print-access-token >/dev/null && echo token_ok`

5. Deploy again:
   - `gcloud run deploy execalc-api --source . --region us-east1 --project execalc-core --quiet`

### Make it persistent for future shells (optional)
Add to `~/.bashrc`:
- `export CLOUDSDK_CONFIG=$HOME/.config/gcloud-execalc-clean`

If you previously set `CLOUDSDK_CONFIG` to a temporary directory (like `/tmp/...`), remove that old export and replace it with the persistent path above.
