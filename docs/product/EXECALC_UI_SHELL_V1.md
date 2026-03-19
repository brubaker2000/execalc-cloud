# EXECALC UI SHELL V1

## Purpose

This document defines the first executable version of the Execalc user interface shell.

It translates the strategic operating system model and UI architecture into:

- a concrete screen layout
- a minimal surface structure
- a component model
- initial user flows
- role-aware cognition exposure

The goal is not visual polish.

The goal is to establish a stable, extensible workspace structure that can support governed executive cognition.

---

# 1. Core Principle

Execalc is a multi-surface executive workspace, not a single chat interface.

The UI shell must:

- preserve a central workbench for thinking
- expose structured reasoning outputs
- surface relevant signals
- maintain continuity across work
- enforce governance boundaries
- remain simple enough for immediate use

---

# 2. Shell Layout (V1)

## 2.1 Global Structure

Top Bar  
Surface Tabs  
Active Surface (varies)

---

## 2.2 Top Bar

Contents:

- Workspace / tenant selector
- Global search (future)
- Notifications (future)
- Profile / settings

### Requirement

The workspace selector must clearly indicate which tenant environment is active.

---

## 2.3 Surface Tabs

V1 surfaces:

1. Execalc (Workbench)
2. Decisions
3. Diagnostics
4. Planning
5. Signals
6. Admin

These tabs represent cognitive surfaces, not external tools.

---

## 2.4 Default Surface

Default landing surface:

Execalc (Workbench)

This preserves familiarity and reduces onboarding friction.

---

# 3. Surface Definitions (V1)

## 3.1 Execalc — Workbench Surface

### Role

Primary thinking and interaction surface.

### Layout

Left Sidebar | Conversation Pane | Context Drawer

### Components

- ProjectSidebar
- ConversationPane
  - MessageList
  - MessageCard
  - ResponseActionBar
- ComposerBar
- ContextDrawer

### Capabilities

- natural language input
- structured responses
- continuity across threads
- inline transformation actions:
  - Refine
  - Summarize
  - Formalize
  - Pressure Test
  - Convert to Decision

### Constraint

Must not absorb all system functionality.

---

## 3.2 Decisions Surface

### Role

Inspection and comparison of structured decision artifacts.

### Components

- DecisionListPane
- DecisionArtifactView
- ComparisonReportView

### Capabilities

- browse decisions
- inspect reasoning
- compare artifacts
- revisit prior outcomes

---

## 3.3 Diagnostics Surface

### Role

Access to structured analytical procedures.

### Components

- DiagnosticCatalog
- DiagnosticRunner
- DiagnosticResultView

### Capabilities

- select diagnostics
- execute procedures
- review structured outputs

---

## 3.4 Planning Surface

### Role

Translate decisions into executable sequences.

### Components

- PlanListPane
- PlanView
- ChecklistView

### Capabilities

- generate plans from decisions
- structure next steps
- preserve linkage to source reasoning

---

## 3.5 Signals Surface (Monitoring Mode)

### Role

Surface meaningful organizational signals derived from:

- chat
- email
- Slack
- calendar
- documents

### Core Principle

Signals must reflect action relevance, not raw activity.

### 3.5.1 Organizational Signal Board

Primary view for Signals surface.

### Displays

- Active themes
- Sentiment shifts
- Emerging opportunities
- Friction / misalignment
- Signal clusters

### Constraint

Signals should appear only if they could change rational decision-making.

### 3.5.2 Signal → Cognition Flow

Every signal must allow:

- Discuss in Execalc
- Create Decision
- Run Diagnostic
- Create Plan

This ensures:

signals → reasoning → decisions → plans

---

## 3.6 Admin Surface (Control Tower)

### Role

Govern system behavior.

### Components

- PermissionsPanel
- PolicyPanel
- RegistryPanel
- AuditPanel

### Capabilities

- manage roles and access
- inspect system behavior
- control governance layers

---

# 4. Role-Based Cognitive Visibility

## 4.1 Purpose

Execalc synthesizes organization-wide cognition.

This cognition must be selectively visible based on role.

## 4.2 Cognitive Layers

1. Raw Signals (scoped)
2. Synthesized Organizational Cognition
3. Role-Based Projection

## 4.3 Visibility Levels

### Operator

- personal signals
- local context
- no organization-wide synthesis

### Manager / Director

- team-level synthesis
- limited cross-functional visibility

### Executive (C-Suite)

- full organizational signal synthesis
- cross-team alignment and tension
- strategic risks and opportunities

### Board / Super Admin

- full cognition
- governance and audit visibility

## 4.4 Enforcement Requirement

Visibility must be enforced at:

- data access layer
- computation layer

NOT only at UI level.

## 4.5 UI Implication

Signals surface adapts by role:

Signals  
[My Signals] [Team Signals] [Organization] ← gated by role

---

# 5. Component Architecture (V1)

## 5.1 Top-Level

App  
└── WorkspaceShell  
  ├── TopBar  
  ├── SurfaceTabs  
  └── SurfaceRouter

## 5.2 Surface Router

SurfaceRouter  
├── ExecalcWorkbenchSurface  
├── DecisionsSurface  
├── DiagnosticsSurface  
├── PlanningSurface  
├── SignalsSurface  
└── AdminSurface

## 5.3 Shared Components

- ArtifactCard
- SignalCard
- SectionHeader
- FilterBar
- SplitPaneLayout
- CollapsibleDrawer

---

# 6. Core User Flows (V1)

## 6.1 Discussion → Refinement

User inputs idea → uses transformation actions → improves clarity.

## 6.2 Discussion → Decision

Conversation → Convert to Decision → structured artifact.

## 6.3 Decision → Comparison

Select artifacts → compare → structured comparison report.

## 6.4 Signal → Scenario

Signal appears → user explores → converts into reasoning or decision.

## 6.5 Decision → Plan

Decision → Create Plan → structured sequence.

---

# 7. Implementation Scope (V1)

## Build Now

- Workspace shell
- Execalc workbench
- Decisions surface
- Basic Signals surface
- Admin (minimal)

## Defer

- full email client
- full Slack client
- advanced monitoring feeds
- complex admin tooling
- UI polish and animation layers

---

# 8. Strategic Intent

This UI shell is designed to:

- feel familiar at entry
- expand into a full executive workspace
- preserve governed cognition
- enable accumulation of insight over time

The system should evolve from:

chat interaction

into:

persistent organizational cognition environment
