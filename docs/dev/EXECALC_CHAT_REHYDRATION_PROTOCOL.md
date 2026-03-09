# EXECALC CHAT REHYDRATION PROTOCOL

## Purpose
This document defines the standard procedure for starting a new Execalc development chat. Its purpose is to restore the correct operating context, governance posture, and current build state at the beginning of each session.

## Principle
A new chat should not rely on prior chat memory. It should be rehydrated from repository truth.

## Required Artifacts to Load
Before meaningful development begins, load the following repository artifacts into the new chat:

1. `docs/dev/EXECALC_LLM_BUILD_PROTOCOL.md`
2. `docs/dev/EXECALC_BUILD_DISCIPLINE.md`
3. `docs/architecture/EXECALC_RUNTIME_ENFORCEMENT_MATRIX.md`
4. `docs/process/DEV_CHAT_REHYDRATION_PROTOCOL.md`
5. Current stage map or next-actions artifact, if present

## Standard Initialization Instruction
After loading the artifacts above, the operator should instruct the LLM with language equivalent to:

"You are now operating under the Execalc Build Protocol and Build Discipline.
Treat the repository as the system of record.
Use deterministic, operator-safe shell commands.
Inspect before changing.
Verify after every meaningful change.
Tie architectural changes back to the Runtime Enforcement Matrix."

## Required Chat Behavior
A properly rehydrated development chat should behave as follows:

- repo-first truth
- no assumptions about current file contents
- deterministic shell-based guidance when possible
- operator-safe instructions suitable for a non-programmer
- verification after every meaningful change
- preference for branch and pull request discipline on structural work
- periodic architectural audit when prompted

## Rehydration Outcome
A chat is considered successfully rehydrated when:
- the governing repo artifacts have been loaded
- the build posture is correctly reinstalled
- the current stage or next-action context is known
- the LLM is operating under deterministic development discipline

## Intended Use
This file should be used at the start of every new Execalc development chat.
