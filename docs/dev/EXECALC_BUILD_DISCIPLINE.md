# EXECALC BUILD DISCIPLINE

## Purpose
This document defines the positive operating standards for building Execalc. It converts lessons learned from prior development friction into a repeatable discipline for future work.

## Build Discipline Standard

### 1. Persist truth in the repository
All frameworks, invariants, runtime objects, workflows, and enforcement expectations must exist in repository artifacts. If something matters, it must be written down in code, documentation, tests, or checklists.

### 2. Close doctrine to runtime
Every architectural concept must map to:
- a runtime object
- an enforcement point
- an observable output
- a test

A concept is not considered complete until this chain exists.

### 3. Inspect before modifying
The current state of the relevant file, module, or artifact must be inspected before any change is proposed.

### 4. Use deterministic shell commands
All instructions should be reproducible through explicit shell commands whenever possible. Operator-safe determinism is preferred over editor-based ambiguity.

### 5. Verify after every change
After each meaningful modification, verification must occur through one or more of:
- file printout
- compile check
- test execution
- diff inspection

### 6. Prefer branch and PR for structural changes
Major or structural changes should be performed on branches and merged through pull requests rather than committed directly to protected branches.

### 7. Perform architecture audits regularly
Periodic audits should review whether canonical frameworks are fully represented in docs, runtime objects, enforcement points, audit surfaces, and tests.

### 8. Treat LLM output as draft until verified
All model-generated code, documentation, architecture language, and recommendations are draft material until inspected and validated.

### 9. Protect working behavior while strengthening architecture
Remediation work should preserve existing efficacious behavior wherever possible through inspection, verification, and testing before merge.

### 10. Improve the system, not just the file
Each change should be understood in the context of the broader system. The goal is coordinated improvement across architecture, runtime, auditability, and stability.

## Intended Use
This file should be loaded into new development chats and used as a standing standard for all repo changes.
