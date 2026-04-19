# INTELLIGENT_FRONT_DOOR_CONCEPT.md

## Status
Draft v0.1 — concept phase; runtime spec pending

## Owner
Product / Architecture

## Purpose
This document defines the Intelligent Front Door (IFD) — the information intake layer that sits at the boundary between the outside world and the Execalc operating environment.

The IFD is not a form. It is not a contact page. It is a governed signal detection system that evaluates everything that arrives at the organizational boundary and routes only what has strategic value.

---

## The Concept

Imagine an organization as a building.

At the entrance is the Intelligent Front Door. Anyone can leave information there — employees, partners, customers, competitors, or outside observers. There is no expectation that any signal will be acknowledged.

The system's mandate is simple: **detect value.**

If a signal contains something strategically relevant, it is immediately routed into the organization, bypassing the classic bottlenecks of email chains and meeting queues. If a signal contains nothing of strategic value, it is not routed — regardless of the source's credentials, pedigree, or presentation.

---

## The Great Equalizer

This is the most significant social consequence of what the IFD does:

> If a 19-year-old at an internet café in Ghana submits a stellar pitch deck, it is routed immediately to someone with decision authority.
> If someone from an elite American university submits something inferior, it is ignored completely.

Execalc becomes the great equalizer.

Traditional organizational intake is credential-filtered. Who you know, where you went to school, how you got introduced, what your email domain is — these are the actual routing mechanisms in most enterprises. A brilliant idea from an unknown source dies in an inbox. A mediocre idea from a connected source gets a meeting.

The IFD routes on signal quality, not signal pedigree. This changes who gets heard inside organizations that deploy it — and by extension, changes what those organizations can see.

---

## How the IFD Works

### Stage 1: Signal Intake
Anything can arrive at the IFD. The system places no upfront constraints on source, format, or channel. The intake boundary is deliberately wide.

### Stage 2: Value Detection
The system evaluates incoming signals against the organization's governing objectives, active scenarios, and strategic context. Signal evaluation is not keyword matching — it is governed assessment against what the organization is actually trying to accomplish.

Questions the IFD answers for each incoming signal:
- Does this contain material information relative to active strategic priorities?
- Does this align with any of the 25 active scenario classifications?
- Is this a candidate for memory admission?
- Does this require immediate routing or can it be queued?
- Who has decision authority over this type of signal?

### Stage 3: Triage
High-value signals are routed immediately to the person with decision authority. Routine matters are handled automatically or queued. Low-value signals are not routed — they are held or discarded according to tenant policy.

### Stage 4: Routing
Routed signals enter the Execalc operating environment through the standard judgment pipeline. They are classified by scenario, processed through the reflex and activation system, and surfaced to the right person with the right context already loaded.

---

## Why This Matters Architecturally

The IFD solves a problem that no current enterprise software addresses: **the boundary between the outside world and organizational intelligence is currently unmanaged.**

Email inboxes are not governed. They route on sender, subject line, and whether the right person happened to see it at the right moment. Most high-value signals that arrive at organizational boundaries die before they reach decision authority — not because they lacked value, but because the routing mechanism was credential-based and human-speed.

The IFD replaces that with:
- Signal-quality-based routing
- Governed evaluation against organizational priorities
- Speed that matches the signal's urgency
- Audit trail showing what arrived, what was routed, and why

---

## Relationship to Organizational Chat Synthesis

The IFD operates at the external boundary. Organizational Chat Synthesis (see `docs/architecture/ORGANIZATIONAL_CHAT_SYNTHESIS.md`) operates at the internal boundary — synthesizing signals from within the organization.

Together they close both ends of the information gap:
- External signals in: IFD
- Internal signals synthesized: Organizational Chat Synthesis
- Both converge on: the Execalc judgment pipeline

---

## Product Stage

The IFD is a future build item — it is not part of the current v1 scope. Current build priority is the governed judgment pipeline (Stage 8) and the core shell experience.

The IFD becomes the product's public face once the internal judgment infrastructure is stable. It is the "spear tip" product surface — the first thing the world sees — and must be backed by a functioning governed system before it can be deployed responsibly.

**Build sequence:** Internal judgment pipeline → Memory runtime → EKE activation → IFD

---

## Required Follow-On Specs

1. `IFD_INTAKE_SCHEMA.md` — what formats and channels are accepted at the boundary
2. `IFD_VALUE_DETECTION_MODEL.md` — how signal quality is assessed
3. `IFD_ROUTING_RULES.md` — who receives what, under what conditions
4. `IFD_TENANT_POLICY_CONTROLS.md` — how tenants configure their IFD boundary behavior

---

## Relationship to the Bridge

The IFD governs entry. The Bridge governs inter-organizational engagement after entry is accepted.

When a signal arrives at the IFD and is deemed high-value enough to route, it enters the Execalc judgment pipeline. If that signal represents a cross-organizational collaboration opportunity — a partnership, a deal, a joint initiative — the Bridge protocol governs how that engagement proceeds between organizational namespaces. IFD is the gate; Bridge is the governed workspace on the other side of the gate.

See `docs/architecture/EXECALC_BRIDGE_PROTOCOL_CONCEPT.md`.

---

## Founding Thesis

> Organizations do not only lose value because they make bad decisions. They also lose value because good opportunities never arrive cleanly enough to be recognized.

The IFD addresses the second failure mode. Most enterprise software is built to help organizations process what has already been admitted. The IFD determines what gets admitted in the first place — before the judgment pipeline ever fires.

The boundary between the outside world and organizational intelligence is currently unmanaged. The IFD is the first governed solution to that problem.

---

## Canonical Statement

> The Intelligent Front Door routes on signal quality, not signal pedigree. It is the mechanism through which Execalc becomes the great equalizer — giving a 19-year-old with a brilliant idea the same access to organizational decision authority as an insider with a mediocre one, while filtering out the noise that currently consumes organizational attention.

> IFD governs entry. Bridge governs inter-organizational engagement after entry is accepted.
