# UI Surface Architecture and Tab Governance

## Status
Draft v0.1

## Owner
Product Layer

---

## 1. Purpose

This section defines the formal UI/UX structure for Execalc's primary working environment.

Execalc will not present itself as a conventional dashboard. Its primary interface will be a desktop-first, browser-like executive workspace shell built around configurable tabs. The shell is intended to function as the operator's daily command environment, allowing the user to move across governed work surfaces without leaving the system.

The design goal is simple:

> Make Execalc feel as familiar as Chrome, while making it far more governed, purposeful, and strategically useful.

---

## 2. Canonical Shell Definition

**Execalc Shell:**
A browser-like workspace composed of horizontally arranged tabs representing governed work surfaces. Each tab is either:
- a native Execalc surface
- an integrated external system, or
- a published institutional reference surface

The shell must support:
- fixed default tab order
- role-based tab visibility
- optional tab enablement
- pinned tabs
- read-only versus editable distinctions
- tenant-specific configuration
- desktop-first usability
- persistent session state

The shell is the product's primary interaction surface.

---

## 3. Core Tabs

These tabs define the default operating spine of the system. They appear in a stable left-to-right order unless a tenant administrator explicitly changes the configuration.

### 3.1 Admin Tab

- **Default position:** far left
- **Surface class:** native Execalc
- **Primary users:** administrators, operators with governance authority
- **Purpose:** system control and workspace governance

**Core functions:**
- user and role management
- tab enablement and visibility control
- integration configuration
- tenant settings
- guidance publishing controls
- cartridge and policy controls
- workspace preferences
- audit and governance state visibility

**Edit posture:** Editable by authorized administrators only.

**Notes:** This is the control room, not a casual-use tab. It exists to govern the shell itself.

---

### 3.2 Chat Tab

- **Default position:** second
- **Surface class:** native Execalc
- **Primary users:** all authorized users
- **Purpose:** primary deliberation and command surface

**Core functions:**
- question and answer interaction
- scenario analysis
- decision support
- synthesis
- memory recall
- judgment workflows
- operator guidance
- strategic recommendation output

**Edit posture:** Fully interactive.

**Notes:** This is the central intelligence surface, but it is not the whole product. Chat is the command console, not the entire application.

---

### 3.3 Email Tab

- **Default position:** third
- **Surface class:** integrated external surface
- **Primary users:** operators, executives, associates with communications access
- **Purpose:** correspondence management inside the shell

**Core functions:**
- inbox and thread visibility
- drafting and reply workflows
- priority thread surfacing
- flagged conversation monitoring
- contextual email support from Execalc
- communication-linked opportunity detection

**Edit posture:** Editable where permissions and provider capabilities allow.

**Notes:** In v1, this begins as a connected Gmail surface. Outlook follows where enterprise demand requires it.

---

### 3.4 Team Communications Tab

- **Default position:** fourth
- **Surface class:** integrated external surface
- **Primary users:** operators, executives, teams with approved channel access
- **Purpose:** internal organizational communications and live signal monitoring

**Core functions:**
- Slack or Teams channel visibility
- monitored communication streams
- escalation awareness
- friction and alignment detection
- rapid context switching between communication and judgment

**Edit posture:** Depends on connector scope and tenant policy. Some users may have read-only channel visibility; others may have full messaging access.

**Notes:** This tab is not merely for convenience. It is an organizational signal surface.

---

### 3.5 Calendar Tab

- **Default position:** fifth
- **Surface class:** integrated external surface
- **Primary users:** all calendar-enabled users
- **Purpose:** timing, scheduling, and meeting-context surface

**Core functions:**
- calendar visibility
- meeting preparation
- schedule-linked memory loading
- upcoming interaction review
- conflict visibility
- meeting support workflows

**Edit posture:** Editable where provider permissions allow.

**Notes:** Calendar is not just a planner. It is a timing and context engine.

---

### 3.6 Published Guidance Tabs

- **Default position:** after the core operational tabs
- **Surface class:** published reference surfaces
- **Primary users:** all authorized roles, subject to visibility rules
- **Purpose:** stable institutional guidance one tab away from live work

**Typical contents:**
- tip sheets
- internal guidance memos
- playbooks
- published Google Docs
- published Google Sheets
- training guides
- informational reference materials
- approved policy summaries

**Edit posture:** Read-only inside Execalc.

**Notes:** These tabs should not expose raw editing. Their value is stability, consistency, and governed access to institutional knowledge.

---

## 4. Optional Tabs

Optional tabs are role-specific or scenario-specific surfaces enabled by tenant policy, operator preference, or situational relevance.

### 4.1 CRM Tab
Examples: Salesforce, HubSpot
Purpose: lead tracking, deal management, contact intelligence, pipeline visibility

### 4.2 Deal Room Tab
Purpose: transaction workflows, diligence review, capital raises, strategic opportunity tracking

### 4.3 Signals Tab
Purpose: alerts, anomalies, flagged activity, opportunity signals, monitored pattern surfaces

### 4.4 Planning Tab
Purpose: structured planning, priorities, timelines, initiative tracking

### 4.5 Diagnostics Tab
Purpose: system checks, strategic health views, scenario breakdowns, governance diagnostics

### 4.6 Dashboard Tab
Purpose: KPI, executive summaries, operating metrics, summary-level business views

### 4.7 Board Pack Tab
Purpose: board-facing materials, governance summaries, locked reports, executive review packages

### 4.8 Forms / Intake Tab
Purpose: controlled intake workflows, structured data collection, requests, submission pipelines

### 4.9 Project Workspace Tab
Purpose: focused initiative workspace for specific teams, campaigns, clients, or engagements

### 4.10 Scenario-Specific Tabs
Examples:
- Draft Day Console
- Investor Workflow
- Sales Briefing
- Executive Alignment Console

These are situational instruments and should not be forced into every user's daily shell.

---

## 5. Surface Permission Model

Every tab must be governed by a permission model, not merely displayed or hidden ad hoc.

### 5.1 Roles

**System Admin**
Full control over shell configuration, integrations, user access, guidance publishing, and governance settings.

**Executive Operator**
Full use of strategic and working surfaces relevant to their role. Limited or no authority over tenant-wide settings unless explicitly granted.

**Associate / Staff User**
Operational access to approved surfaces, with narrower permissions and limited administrative power.

**Read-Only / Advisor User**
View access to selected tabs and materials, without mutation rights except where explicitly granted.

### 5.2 Permission Types

Each tab carries explicit settings for:

| Permission | Meaning |
|---|---|
| Visible | User can see the tab |
| Accessible | User can open and use the tab |
| Editable | User can make changes |
| Configurable | User can alter tab settings or properties |
| Publish-capable | User can publish institutional guidance to the shell |
| Admin-governed | Only admins can modify visibility or behavior |

---

## 6. Surface-by-Surface Permission Guidance

### 6.1 Admin
- System Admin: full access
- Executive Operator: optional, usually limited
- Associate: generally hidden
- Read-Only / Advisor: hidden

### 6.2 Chat
- System Admin: full access
- Executive Operator: full access
- Associate: full or scoped access
- Read-Only / Advisor: optional restricted access

### 6.3 Email
- Access tied to provider connection and tenant policy
- Some users may have personal mailbox access only
- Shared mailbox access must be explicitly permissioned

### 6.4 Team Communications
- Channel visibility must reflect actual team permissions
- Read-only monitoring may be allowed even when posting is not

### 6.5 Calendar
- Visibility can be personal, delegated, or team-specific
- Editing rights depend on provider and tenant policy

### 6.6 Published Guidance
- Broad view access is appropriate
- Edit rights do not exist inside the tab itself
- Publishing and replacement rights belong to admins or designated content owners

### 6.7 CRM / Deal Tabs
- Access should be role-based and often narrower than general shell access
- Sensitive revenue, pipeline, or diligence data must follow tenant policy and role scope

---

## 7. Read-Only Versus Editable Doctrine

The shell must clearly distinguish between surfaces intended for action and surfaces intended for guidance.

### 7.1 Read-Only Surfaces
- published guidance tabs
- approved policy docs
- locked playbooks
- formal tip sheets
- institutional reference materials
- certain board or diligence packages

### 7.2 Editable Surfaces
- chat
- email drafts
- notes
- forms
- planning surfaces
- selected CRM records
- selected operational workflows

This doctrine matters because Execalc is a governed environment. Not every piece of information should be mutable in place.

---

## 8. Governed Versus Embedded Doctrine

Not every connected tool deserves the same product meaning.

### 8.1 Embedded Surface
A third-party tool or view presented inside the shell for convenience.

Examples:
- calendar view
- Slack pane
- Gmail pane
- published doc tab

### 8.2 Governed Surface
Execalc adds strategic value through interpretation, prioritization, contextualization, or signal extraction.

Examples:
- email threads flagged as stalled or leverage-bearing
- team messages surfaced as friction, urgency, or drift
- calendar events enriched with meeting context
- guidance tabs linked to an active scenario or role need

**Embedded is visible. Governed is useful.**

The shell should progressively move important surfaces from merely embedded to genuinely governed.

---

## 9. V1 Implementation Guidance

V1 should be disciplined and not overbuilt.

### 9.1 V1 Interaction Model
- desktop-first browser-based shell
- stable tab bar
- authenticated workspace
- chat as primary command surface
- integrated operational tabs
- read-only guidance tabs
- basic role-aware tab visibility

### 9.2 V1 Core Tabs
1. Admin
2. Chat
3. Email
4. Team Communications
5. Calendar
6. Published Guidance

### 9.3 V1 Integration Priority

First wave:
- Gmail
- Google Calendar
- Slack
- Published Google Docs / Sheets surfaces

These fit the current vision best and keep the shell tightly aligned with daily executive work.

### 9.4 V1 UI Behavior
- pinned default tabs
- admin-controlled enablement
- no uncontrolled tab sprawl
- read-only published knowledge surfaces
- consistent left-to-right order
- desktop layout first

### 9.5 V1 Restraints

V1 should avoid:
- excessive personalization complexity
- unrestricted user-generated tab proliferation
- full document editing inside the shell
- trying to replicate every function of every external tool
- mobile-first design as the primary assumption

---

## 10. Later-Phase Implementation Guidance

### 10.1 Phase 2
- CRM tab
- signals tab
- diagnostics tab
- planning tab
- richer role-based tab sets
- deeper cross-surface context awareness

### 10.2 Phase 3
- deal room workflows
- board pack tab
- scenario-triggered temporary tabs
- operator-specific workspace profiles
- advanced governance and audit views
- mobile companion refinement

### 10.3 Longer-Term Extensions
- voice as secondary input surface
- API-driven external module injection
- deeper governed actions across integrated tools
- more dynamic surface orchestration based on scenario and role

---

## 11. Canonical Product Language

**Primary interface statement:**
Execalc's primary interface is a desktop-first, browser-like executive workspace shell composed of governed tabs for administration, deliberation, communication, scheduling, and institutional guidance.

**Operational meaning statement:**
Execalc is not merely a chatbot or dashboard. It is a tab-governed executive operating environment that brings judgment, communication, timing, and guidance into one controlled workspace.

**UX doctrine statement:**
The shell should feel as familiar as Chrome, while remaining more governed, more role-aware, and more strategically useful than a conventional browser or SaaS dashboard.

---

## 12. Canonical Lock Line

> Execalc's UI is a desktop-first, browser-like workspace shell in which core executive functions are organized into governed tabs, allowing operators to move across chat, communication, scheduling, and institutional guidance inside one controlled operating environment.

---

## 13. Next Build Artifacts Required

1. Wireframe-level tab map
2. Permissions matrix table (roles × tabs × permission types)
3. V1 component inventory
4. Shell state model
5. Integration connector spec for Gmail, Google Calendar, Slack, Google Docs/Sheets
