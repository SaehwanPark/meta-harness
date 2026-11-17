---
name: harness
description: Design, review, or simplify a repository's reusable agent skills, team workflows, and handoffs.
---

# Harness

Start with the outcome, intended users, constraints, and acceptance checks. Inspect existing guidance, skills, and workflow contracts where the change could affect them. Reuse their canonical paths and preserve existing consumers. Make reasonable, reversible assumptions and resolve conflicting instructions where possible. Ask when a material decision remains.

## Choose what to build

Keep ordinary one-off work direct. For recurring work, start with one skill that captures repository-specific decisions, tools, or checks. Add the following only when the workflow needs them:

| Need | Artifact |
| --- | --- |
| Guidance that applies across the repository | Short `AGENTS.md` |
| Independently useful behavior or a reusable entry point | `.agents/skills/{name}/SKILL.md` |
| Stable responsibilities, ordering, or coordination | `docs/harness/{domain}/team-spec.md` |
| A durable role that needs its own brief | `docs/harness/{domain}/roles/{role}.md` |
| Evidence or state needed for audit, resumption, or later consumption | A deterministic path under `_workspace/` |
| Client-specific execution settings | A removable adapter or profile |

Keep each rule in one canonical place. Skills teach reusable behavior, role briefs define responsibility, and adapters map those contracts to runtime capabilities. Add role or profile settings only where they change how the work is executed.

## Write the workflow

- Start each generated skill with YAML `name` and a short, specific `description` for discovery. In the body, state the outcome and include the inputs, constraints, outputs, or checks the model cannot reliably infer. Use steps when order matters. Link to specific references from the decision that needs them.
- Prefer a single agent for work that shares context or changes the same resources. Delegate when authorized and independent work has a concrete benefit from specialization, latency, or context isolation. Give each worker a bounded task, inputs, output and acceptance criteria, required access, and a parent who owns synthesis.
- For parallel writes or stateful tests, establish effective isolation or non-overlapping ownership. Serialize conflicts. When a capability or worker fails, preserve partial evidence, identify missing coverage, and use a safe fallback or report the blocker.
- Use short native messages for in-run coordination. When a durable handoff is needed, give it an owner, consumer, stable path or record key, expected contents, and completion state. Reuse the deliverable as the handoff when it already contains that information.
- Let the runtime inherit its model and settings by default. Put justified overrides and recovery behavior in removable adapters. Keep portable behavior usable with the adapter removed.

Check paths and producer/consumer agreement, then exercise a representative workflow and any failure path that could affect correctness. When prompt overhead motivated a change, compare quality and cost against the previous or direct workflow where practical. Summarize the changes and remaining gaps.

## Read when needed

- [Skill writing](references/skill-writing-guide.md) or [repo-wide guidance](references/agents-md-guide.md) when authoring those artifacts.
- [Coordination patterns](references/agent-design-patterns.md), [orchestrator template](references/orchestrator-template.md), or [examples](references/team-examples.md) when designing a reusable team.
- [Skill testing](references/skill-testing-guide.md) for behavior changes or [QA guide](references/qa-agent-guide.md) for cross-boundary review.
- [Autonomous experiments](references/autonomous-experimentation.md) for explicitly requested, bounded experiments on authorized compute.
- [Runtime capabilities](references/runtime-capabilities.md) and the selected adapter when translating a portable role to [Codex](references/codex-agent-adapter.md), [Pi](references/pi-agent-adapter.md), [Antigravity](references/antigravity-agent-adapter.md), [Cursor](references/cursor-agent-adapter.md), or a [generic runtime](references/generic-agent-adapter.md). Verify guarantees in the actual deployment.
