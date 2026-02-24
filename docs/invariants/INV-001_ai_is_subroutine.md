# INV-001 — AI Is a Subroutine, Not the System

## Status
Binding architectural invariant (non-negotiable)

## Purpose
Prevent “demo-ware” architecture where vectors/models replace schema, rules, and auditable control paths.
Execalc is a governed judgment layer. The LLM and embeddings are optional subroutines inside deterministic governance.

## Invariant Rules

### 1) Deterministic First. AI Second.
If a requirement can be solved with:
- Schema
- SQL filters
- Explicit joins
- Rule-based triggers
- Structured metadata

Then it MUST be solved that way.

AI is reserved for ambiguity:
- Semantic similarity
- Thematic clustering
- Conceptual recall
- Fuzzy classification

If it can be answered with `=`, `>`, `<`, `AND`, `OR`, or `JOIN`, it does not belong in the model path.

### 2) Postgres Is the System of Record
All structured data lives in Postgres.
Embeddings are attributes of structured records — not a separate universe.

Forbidden:
- Vector-only data silos
- Detached embedding stores
- Black-box retrieval paths

Every vector query MUST be joinable and constrainable by:
- `tenant_id`
- permissions / RBAC
- governance flags
- activation tags
- deterministic filters

Structured narrowing first. Semantic ranking second.

### 3) Tenant Isolation Must Never Depend on AI
Tenant scoping is enforced:
- at ingress
- at schema
- in queries
- in vector filters
- in logs

We never retrieve globally and “filter later.”
Permission and tenant boundaries are applied BEFORE similarity logic.

### 4) Embeddings Are for Meaning, Not Structure
Do NOT embed:
- IDs
- dates
- numeric ranges
- geographic coordinates
- enumerated categories

Do embed:
- free text
- descriptions
- strategic insights
- narrative content

Vectors handle meaning. SQL handles structure.

### 5) Reflex System Must Degrade Gracefully
Reflex triggers must be rule-based first.
Model classification may enhance them — but must never be the only gate.

If the model times out or returns garbage, the system still behaves deterministically.

### 6) Retrieval Must Be Explainable
Every surfaced result must be traceable:
- which rule triggered it
- which fields matched
- what similarity score was used
- which records were involved

No black-box surfacing.

## Enforcement
- Any PR that introduces vector-first retrieval, vector-only storage, or post-hoc tenant filtering violates this invariant.
- New retrieval features must include an “explain” payload: deterministic filters + scoring + rule path.

## Unifying Principle
The most robust AI systems use the least AI necessary.
We are building architecture, not demos.
