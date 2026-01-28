# Build Cockpit Checklist

This checklist is the non-negotiable operating procedure for the Execalc build.
Goal: prevent regressions, preserve invariants, and maintain an audit-grade trail.

## Session Start Snapshot
Run:
- pwd
- git status
- git branch --show-current
- git log -5 --oneline

Expected:
- Correct repo directory
- On intended branch (typically main)
- Clean working tree

## Baseline Health Gate
Run:
- python3 -m unittest -q

Expected:
- All tests pass before changes begin

## Core Invariants (Multi-Tenant)
These must remain true after every change:
1) No database drift:
   - No accidental repo-root SQLite databases.
   - Tenant DB paths are explicit and deterministic.
2) Tenant isolation:
   - Tenant context is required for tenant operations.
   - Tenant context must not change mid-request.
3) Authorization:
   - RBAC enforced at service entrypoints.
   - Unauthorized access fails explicitly.
4) Repo hygiene:
   - Runtime artifacts (DB files, __pycache__, *.pyc) are ignored and never committed.

Practical checks:
- find . -name "*.db" -o -name "__pycache__" -o -name "*.pyc" | head
- git check-ignore -v src/service/tenant/tenants.db

## Change Discipline Loop (Repeat Per Change)
1) Ensure clean baseline:
   - git status --porcelain
   - python3 -m unittest -q
2) Make one coherent change (single intent).
3) Inspect the diff:
   - git diff
4) Run tests relevant to the change:
   - minimum: python3 -m unittest -q
5) Commit only when proven:
   - git add <files>
   - git commit -m "<message that matches intent>"

## Pre-Push Gate
Run:
- git status
- git log -3 --oneline
- python3 -m unittest -q

Expected:
- Clean working tree
- Recent commits are coherent and scoped
- Tests are green

## Post-Push Gate
Run:
- git status

Expected:
- Clean working tree
- CI green (when applicable)
