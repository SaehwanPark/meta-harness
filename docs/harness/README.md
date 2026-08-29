---
title: Harness Output Specifications
description: Durable contracts for generated team specs, role briefs, and handoff artifacts.
layout: default
---

# Harness Output Specifications

This reference defines the durable artifacts that a generated Harness may
produce. These are contracts, not mandatory ceremony for every small task.

## Canonical destinations

| Artifact | Path | Purpose |
| --- | --- | --- |
| Team spec | `docs/harness/{domain}/team-spec.md` | role topology, phase order, handoffs, and failure policy |
| Role brief | `docs/harness/{domain}/roles/{role}.md` | one stable responsibility that does not need a full skill |
| Reusable skill | `.agents/skills/{specialist}/SKILL.md` | behavior that should be selected and reused across projects |
| Intermediate handoff | `_workspace/{phase}_{role}_{artifact}.md` | inspectable, resumable, or cross-agent work product |

The repository keeps `docs/harness/` as the canonical destination for team
specs and role briefs. Keep the root `AGENTS.md` short, human-written, and
limited to rules that matter across tasks.

## When to persist a handoff

Persist an artifact when another phase or contributor must:

- inspect the work without reconstructing it from chat;
- resume after interruption;
- audit a decision or resolve conflicting results;
- consume a deterministic output during synthesis.

Use a concise summary for low-risk, ephemeral coordination. Do not create a
large handoff tree merely to document a one-step task.

## Generated skill contract

Every generated `SKILL.md` begins with YAML frontmatter containing at least
`name` and `description`. Its body should state:

- when to use the skill and when not to use it;
- the inputs required to do useful work;
- the workflow and ownership boundaries;
- the named outputs and validation checks.

Move bulky or conditional detail into `references/` so the main skill stays
cheap to load.

The [AGENTS Authoring Guide](https://github.com/SaehwanPark/meta-harness/blob/main/.agents/skills/harness/references/agents-md-guide.md)
explains how to keep repo-wide guidance short and human-written. Keep
temporary recovery logic in a rippable section that can be removed as the
workflow evolves.

## Autonomous experiment artifacts

An autonomous experiment workflow may additionally preserve:

~~~text
_workspace/experiments/{run}/request-summary.md
_workspace/experiments/{run}/baseline.md
_workspace/experiments/{run}/results.tsv
_workspace/experiments/{run}/final-summary.md
~~~

Declare the mutable surface before the first candidate. Keep the evaluation
surface read-only, measure a baseline, and record crashes and timeouts rather
than silently dropping them.

## Portable delegation contract

Portable team specs must name:

- which tasks are eligible for delegation;
- the paths or resources each writer owns;
- who owns synthesis and final acceptance;
- how partial-worker failures are reported;
- how conflicting results are resolved.

Native mappings belong in removable adapters. See the [Codex adapter in the
source tree](https://github.com/SaehwanPark/meta-harness/blob/main/.agents/skills/harness/references/codex-agent-adapter.md)
when a client-specific execution profile is useful.

## Starter example

The [starter research example](starter-research/README.html) shows one team
spec, one role brief, and deterministic handoff paths without adding example
skills to the canonical tree.

Return to the [workflow guide](../guides/workflow.html) for the phase sequence,
or inspect the [orchestrator template in the source tree](https://github.com/SaehwanPark/meta-harness/blob/main/.agents/skills/harness/references/orchestrator-template.md).
