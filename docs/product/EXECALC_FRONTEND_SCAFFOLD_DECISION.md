# EXECALC FRONTEND SCAFFOLD DECISION

## Decision

The first frontend scaffold for Execalc will live in:

`web/`

at the repo root.

## Why

This keeps the frontend cleanly separated from the Python backend in `src/`, while preserving a single monorepo-style product structure.

It also aligns with the Execalc UI shell doctrine:

- backend service logic remains in `src/service`
- product UI shell and workspace surfaces live in `web/`
- docs remain in `docs/`

## Intended frontend stack

Initial frontend stack:

- Next.js
- React
- TypeScript
- Tailwind CSS
- shadcn/ui
- Zustand
- TanStack Query

## Initial goal

The first frontend goal is not full product polish.

It is to establish the UI shell defined in:

- `docs/product/EXECALC_UI_SHELL_V1.md`
- `docs/product/EXECALC_UI_IMPLEMENTATION_SPRINT_1.md`

## Initial surface scope

V1 frontend scaffold should support:

- Workspace shell
- Execalc workbench surface
- Decisions surface
- Signals surface (minimal, role-aware)
- Admin surface (minimal)

## Constraint

The frontend scaffold must not outrun backend discipline.
UI actions should map to explicit backend execution paths.
