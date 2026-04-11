# Writing a Good `AGENTS.md`

`AGENTS.md` is the highest-leverage repo guide because it is loaded into every session. Treat it as durable infrastructure, not as a place to dump everything known about the codebase.

## Core Rule

Keep it short, human-written, and limited to repo-wide guidance that matters on nearly every task.

If a detail is only useful for one workflow, move it into a repo-local skill, team spec, or docs page and point to it from `AGENTS.md`.

## What To Include

- `WHAT`: the project purpose, stack choices, canonical paths, and the major surfaces another engineer or agent must not confuse
- `WHY`: why the project exists, why key boundaries matter, and why a few persistent constraints are worth keeping in every session
- `HOW`: the exact build, test, and verification commands plus non-obvious tool choices such as `uv` over `pip` or `bun` over `npm`
- pointers to deeper repo-local docs when the detailed workflow is conditional or role-specific

## What To Leave Out

- generated directory dumps or codebase tours that another agent can discover directly
- code style rules already enforced by formatters, linters, or tests
- task-specific playbooks that only matter sometimes
- copied snippets or long prose that could be replaced by one repo-local pointer
- model-specific retries, recovery logic, or temporary heuristics that belong in removable harness docs instead

## Progressive Disclosure

- keep `AGENTS.md` as the stable entry point
- put deeper workflow detail in `.agents/skills/`, `docs/`, or other repo-local references
- prefer pointers over copies so the guidance stays cheap to load and easy to update

## Rippable Harness Note

`AGENTS.md` should describe stable repository rules, not temporary harness cleverness. Keep evolving prompt tweaks, retry heuristics, and model-specific recovery logic in orchestrator specs or linked references that can be deleted without rewriting the repo-wide contract.

## Compact Template

```markdown
# Repository Agents Guide

Keep this file short and repo-wide. Point to deeper docs when detail is conditional.

## What
- {project purpose and main surfaces}
- {canonical paths or shared contracts}
- {major tool or runtime choices only when non-obvious}

## Why
- {why the project exists}
- {why the main boundaries or constraints matter}

## How
- {exact build, test, and verify commands}
- {required doc-sync or release rules}
- {pointers to deeper docs}
```

## Quick Checks

- Would this line help on most tasks?
- Is this guidance written by someone who understands the repo and intends to keep it maintained?
- Can a linked doc hold the detail instead?
- If model behavior improves next month, will this rule still belong in `AGENTS.md`?
