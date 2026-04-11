# Harness Output Specs

Generated harness-specific team specs and role briefs belong under `docs/harness/{domain}/`.

Repo-level version history for the meta-harness project lives in [CHANGELOG.md](../../CHANGELOG.md).

Start from the [orchestrator template](../../.agents/skills/harness/references/orchestrator-template.md) when you need a durable phase-and-handoff spec. Use the [AGENTS Authoring Guide](../../.agents/skills/harness/references/agents-md-guide.md) when the target repository needs short always-loaded repo guidance. See the [starter research example](starter-research/README.md) for a minimal concrete package that includes a team spec, one role brief, and `_workspace/` artifact mapping.

Typical generated files include:

- `docs/harness/{domain}/team-spec.md`
- `docs/harness/{domain}/roles/{role}.md`
- `_workspace/{phase}_{role}_{artifact}.md`

Autonomous experiment workflows may additionally preserve deterministic run logs such as:

- `_workspace/experiments/{run}/results.tsv`
- `_workspace/experiments/{run}/baseline.md`
- `_workspace/experiments/{run}/final-summary.md`

Keep model-specific retries, shortcuts, and recovery heuristics in removable, rippable sections of the team spec or linked references instead of hard-wiring them into the core artifact contract.

This repository keeps `docs/harness/` as the canonical destination and now includes one docs-first starter example for reference without shipping example skills in the canonical source tree.
