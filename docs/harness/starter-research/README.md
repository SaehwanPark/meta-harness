# Starter Research Example

This starter example shows the smallest useful harness package for a research workflow without adding example skills to the canonical `.agents/skills/harness/` tree.

Use it as a reference when you want to generate:

- one durable team spec
- one narrow role brief
- deterministic `_workspace/` handoff files

The example maps to these generated artifacts:

| Example surface | Intended generated path |
| --- | --- |
| team topology and workflow | `docs/harness/starter-research/team-spec.md` |
| stable role brief | `docs/harness/starter-research/roles/research-lead.md` |
| reusable orchestrator, if promoted into a skill | `.agents/skills/research-orchestrator/SKILL.md` |
| specialist skill, if promoted into a skill | `.agents/skills/source-research/SKILL.md` |
| intermediate handoffs | `_workspace/00_input/request-summary.md`, `_workspace/01_source_findings.md`, `_workspace/final/report.md` |

This repository keeps the starter package docs-first on purpose. Treat the files here as a concrete artifact contract, then generate repo-local skills only when the target repository actually needs them.
