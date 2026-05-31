# Repository Agents Guide
Keep this file short and repo-wide. Put conditional or bulky guidance in linked docs instead of here.
## What
- Meta Harness is a portable repository for designing repo-local agent harnesses. Canonical source: [.agents/skills/harness/](.agents/skills/harness/). Durable contracts: [docs/harness/README.md](docs/harness/README.md). `_workspace/` holds deterministic handoffs.
## Why
- Keep harness design portable, repo-local, rippable, and easy to update as models improve. Leads orchestrate by default: context, plan, work contracts, subAgent prompts, synthesis, validation, and final decision.
## How
- When work can be bounded, spawn a bounded implementer instead of writing the deliverable in the Lead; direct Lead writes require explicit authorization, emergency unblocker status, or final synthesis/handoff ownership recorded in `_workspace/`.
- Keep a compact context pack: goal, scope, source authority, constraints, subAgent ids/roles, output paths, tests, blockers, and final decision.
- For `$harness` or harness-style multi-agent requests, run approval-first planning before execution with `RequestMeaning`, `Assumptions`, `Architecture`, `FileOwnership`, `WavePlan`, `SpawnPlan`, `SpawnPrompts`, `TurnByTurnFeedback`, `ValidationPlan`, `FinalReviewCriteria`, and `ApprovalGate`.
- Do not spawn subAgents, mutate target deliverables, or start implementation for harness-style work until the user approves the final plan.
- Spawn prompts are work contracts: role, objective, source authority, read/write scope, tool permissions, forbidden overlaps, output path/template, acceptance criteria, stop conditions, and report format.
- Avoid full-history forks with explicit model overrides; if a model override is needed, use a compact handoff. Pick models by task shape and uncertainty.
- Researchers use web/search only when needed; implementers stay inside disjoint write sets; reviewers read the request, artifact, and acceptance criteria before reporting.
- Use deterministic `_workspace/` handoffs. When canonical paths, workflow guidance, or artifact contracts change, update [README.md](README.md) and [docs/harness/README.md](docs/harness/README.md) too.
- Validate with `python3 scripts/test_install_harness.py` and `python3 scripts/validate_codex_port.py`; read [.agents/skills/harness/SKILL.md](.agents/skills/harness/SKILL.md) for deeper guidance.
## Runtime Boundary
- Meta Harness has no external control-plane plugin dependency. Do not use the palantir-mini plugin, palantir-mini MCP tools, palantir-mini routing, MCP-first palantir-mini policies, generated palantir-mini session state, or plugin hooks here unless the user explicitly asks for palantir-mini by name for the current task.
- Apply the same opt-in rule to any other external control-plane plugin: do not install, enable, or rely on runtime plugin hooks, MCP-first policies, generated session state, or plugin routing unless the user explicitly asks for that plugin by name for the current task.
