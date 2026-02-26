# Editor-Only Dev Protocol (Permanent)

## Rule (Non-Negotiable)
All file edits happen in Cloud Workstations VS Code only.
- No nano, vim, or terminal-based editors.
- Terminal is for commands only (tests/build/git/gcloud), not editing.

## Standard Dev Loop (Repeatable)
1) Edit (VS Code)
2) Compile (terminal)
3) Test (terminal)
4) Commit (VS Code Source Control or terminal)
5) Push (VS Code or terminal)
6) Verify CI (GitHub Actions) and smoke gates (when applicable)

## Required Verification Commands (Terminal Only)

### Compile
python -m compileall -q src/service && echo compile_ok

### Unit tests (tenant kernel)
python -m unittest discover -s src/service/tenant -p "test_*.py" -v

### Quick repo status
git status

## Workflow Discipline
- One purpose per commit.
- Every PR description must reference what it closes in `docs/NEXT_ACTIONS.md`.
- If conversational guidance conflicts with repo docs, repo docs win.

## Enforcement
- Any instructions in dev chats must assume VS Code UI edits only.
- If a step would normally use nano/vim, it must be rewritten into VS Code steps.