---
title: Harness Output Specifications
description: Durable contracts for generated team specs, role briefs, and handoff artifacts.
layout: default
---

# Harness Output Specifications

This reference defines the durable artifacts that a generated Harness may
produce. These are contracts, not mandatory ceremony for every small task.

## Portable layers

Keep the reusable **skill** (how domain work is performed), the runtime-neutral
**role** (what a worker owns and must accomplish), and the removable runtime
**execution profile** (how that role gets tools, model, workspace, permissions,
and recovery settings) separate. Skills and role specs are canonical;
execution profiles are generated mappings and must not become a second source
of truth.

## Phase 0: Inventory & Drift Audit

Before the six design phases, inspect existing `.agents/skills/`, `AGENTS.md`,
`docs/harness/`, native agent definitions, adapters, install layouts, and
runtime capabilities. Detect stale or duplicated skills, roles, profiles, and
paths; classify the operation (new harness, extension, adapter update, drift
repair, skill-only update, refactor, or maintenance). Record an auditable
summary in `_workspace/00_contract_inventory.md` when needed:

~~~yaml
existing_skills: []
existing_roles: []
existing_profiles: []
detected_runtimes: []
stale_artifacts: []
stale_profiles: []
compatibility_risks: []
recommended_action: ...
handoff:
  producer: phase-0-auditor
  consumer: phase-1-domain-analyst
  path: _workspace/00_contract_inventory.md
  schema: phase-0 inventory contract
  completion: audit-complete
~~~

Resolve source-of-truth conflicts before proceeding; do not silently overwrite
existing contracts.

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

## Role contract

A durable role brief or team spec should declare the fields relevant to the
role: responsibility, inputs, outputs, required skills, quality bar, resource
reads/writes/external mutation, ownership requirement and enforcement,
workspace preference, parent/peer communication, clarification and escalation
targets, permissions, semantic model policy, removable `runtime_overrides`,
and completion artifact plus acceptance/blocked states. Use semantic model
intent (`inherit`, `fast`, `economy`, `balanced`, or `strong`) and capability
requirements rather than model IDs. Concrete provider/model/thinking settings
belong only in an adapter override.

Ownership is a requirement, not an implied guarantee: adapters must label it
mechanically enforced, workspace-enforced, advisory, serialized, or
unsupported.

## Three handoff classes

1. **Ephemeral coordination** — status, short clarification, quick discovery,
   and bounded peer communication; prefer a native channel.
2. **Durable coordination record** — assignment, decision request, blocker,
   acceptance state, or resumable orchestration; use a typed runtime record or
   `_workspace/` fallback.
3. **Durable artifact** — plans, evidence, ledgers, reports, and cross-session
   outputs; use deterministic files with an owning producer.

Persist only when auditability, resumability, debugging, or cross-agent
consumption justifies it. Durable handoffs name producer, consumer, path,
expected sections/schema, and completion state.

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

## Portable delegation and failure contract

Portable team specs must name:

- which tasks are eligible for delegation;
- the paths or resources each writer owns and the enforcement level;
- workspace, communication, permissions, escalation, model intent, and completion criteria;
- who owns synthesis and final acceptance;
- how partial-worker failures and missing synthesis branches are reported;
- how conflicting results are resolved.

Declare behavior for worker spawn failure, unavailable model/tool, resource
conflict, communication failure, permission denial, workspace setup failure,
and missing runtime capabilities. Never silently weaken a correctness
requirement: lower mechanical ownership to isolated workspaces, then explicit
non-overlap, then serialized execution. Preserve partial results and mark the
run blocked/incomplete rather than inventing coverage.

When supported, observability should expose active workers, topology, task,
workspace, ownership, blocked state, clarifications, and partial failures;
portable artifacts must remain understandable without it. Keep hierarchy
shallow (`root -> worker`, or exceptionally `root -> coordinator -> worker`).

Native mappings belong in removable adapters. Source-of-truth precedence is
portable skill semantics, portable team/role spec, capability definition,
adapter mapping, then generated native profile. Removing a native profile must
leave skills, docs, and `_workspace/` contracts usable. See the [Codex adapter
in the source tree](https://github.com/SaehwanPark/meta-harness/blob/main/.agents/skills/harness/references/codex-agent-adapter.md)
when a client-specific execution profile is useful.

## Starter example

The [starter research example](starter-research/README.html) shows one team
spec, one role brief, and deterministic handoff paths without adding example
skills to the canonical tree.

Return to the [workflow guide](../guides/workflow.html) for the phase sequence,
or inspect the [orchestrator template in the source tree](https://github.com/SaehwanPark/meta-harness/blob/main/.agents/skills/harness/references/orchestrator-template.md).
