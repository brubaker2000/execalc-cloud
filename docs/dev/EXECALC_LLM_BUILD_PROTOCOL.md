# EXECALC LLM BUILD PROTOCOL

## Purpose
This document defines the operating protocol for working with a large language model during Execalc development. It exists to ensure that development chats remain governed, deterministic, and aligned with repository truth.

## Core Principle
The repository is the system of record. Chat is temporary working memory.

## Operating Rules

### 1. Repo-first truth
If a framework, invariant, runtime object, workflow rule, or enforcement expectation matters, it must exist in the repository as code, documentation, tests, or checklists.

### 2. Inspect before change
The LLM must never assume repository structure or current file contents. It must inspect the relevant file or files before recommending a modification.

### 3. Deterministic execution sequence
All code modifications must follow this sequence:

Inspect -> Modify -> Verify -> Commit -> Push

No modification is complete until verification has occurred.

### 4. Operator-safe instructions
All instructions must be executable by a non-programmer operator. Instructions should be:
- explicit
- atomic
- copy/paste ready
- shell-based when possible

The LLM must not rely on vague editor instructions or assumed technical fluency.

### 5. No architecture without enforcement
Any architectural change must reference an enforcement point in the Runtime Enforcement Matrix. A concept is not considered real merely because it is well described.

### 6. Verification is mandatory
After every meaningful change, the operator and LLM must verify the result through one or more of:
- file printout
- compile check
- unit test
- integration test
- diff inspection

### 7. Chat is not memory
No important rule should live only in chat. If it matters beyond the current exchange, it must be written into the repository.

### 8. LLM output is draft until verified
All model-generated code, architecture, and guidance should be treated as draft material until it has been inspected and validated.

### 9. Prefer branch and PR discipline
Structural changes should prefer branch + pull request workflow rather than direct modification of protected branches.

### 10. Audit on demand
When prompted, the LLM should perform architectural audits, identify under-enforced capabilities, and tie recommendations back to repo artifacts and enforcement points.

## Intended Use
This file should be loaded into every new development chat as part of the Execalc chat rehydration process.
