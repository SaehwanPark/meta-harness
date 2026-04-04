# Harness Output Specs

Generated harness-specific team specs and role briefs belong under `docs/harness/{domain}/`.

Typical generated files include:

- `docs/harness/{domain}/team-spec.md`
- `docs/harness/{domain}/roles/{role}.md`
- `_workspace/{phase}_{role}_{artifact}.md`

Autonomous experiment workflows may additionally preserve deterministic run logs such as:

- `_workspace/experiments/{run}/results.tsv`
- `_workspace/experiments/{run}/baseline.md`
- `_workspace/experiments/{run}/final-summary.md`

This repository keeps the directory as the canonical destination without shipping a full example domain package.
