# EXECALC UI IMPLEMENTATION — SPRINT 1

## Purpose

Define the first implementation sprint for the Execalc UI shell.

Goal:
- establish a working multi-surface workspace
- prove workbench + decision surfaces
- introduce role-aware surface exposure

---

## Scope

### Build

- Workspace shell (top bar + tabs + routing)
- Execalc workbench surface
- Decisions surface
- Signals surface (placeholder, role-aware)
- Admin surface (placeholder)

---

## Non-Goals

- full email client
- full Slack client
- full diagnostics execution
- UI polish / animation layers
- deep admin tooling

---

## Surfaces

- Execalc (Workbench)
- Decisions
- Diagnostics (placeholder)
- Planning (placeholder)
- Signals
- Admin

---

## Core Components

- WorkspaceShell
- TopBar
- SurfaceTabs
- SurfaceRouter

### Execalc

- ProjectSidebar
- ConversationPane
- ComposerBar
- ResponseActionBar
- ContextDrawer

### Decisions

- DecisionListPane
- DecisionArtifactView
- ComparisonReportView

### Signals

- SignalNav
- SignalCard (stub)

### Admin

- PermissionsPanel (stub)
- PolicyPanel (stub)
- AuditPanel (stub)

---

## Acceptance Criteria

### Shell

- user can switch between all surfaces
- active surface persists

### Execalc

- chat layout renders
- composer accepts input
- response actions visible

### Decisions

- decision list renders
- artifact view renders
- comparison view renders

### Signals

- tabs:
  - My Signals
  - Team Signals
  - Organization (role-gated)

### Admin

- role-gated access works

---

## Definition of Done

- workspace shell is functional
- workbench feels usable
- decisions can be viewed
- role-based visibility exists
- UI resembles a multi-surface workspace
