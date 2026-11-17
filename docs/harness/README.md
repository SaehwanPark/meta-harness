---
title: Harness Output Specifications
description: Durable contracts for generated team specs, role briefs, and handoff artifacts.
layout: default
---

# Harness Output Specifications

Use the smallest set of artifacts that supports the target workflow. A single
skill often suffices. Add a team contract or durable handoff when another
worker, session, or tool depends on it.

## Canonical destinations

| Artifact | Path | Purpose |
| --- | --- | --- |
| Reusable skill | `.agents/skills/{name}/SKILL.md` | Behavior that should be discovered and reused |
| Team spec | `docs/harness/{domain}/team-spec.md` | Stable responsibilities, dependencies, and acceptance |
| Role brief | `docs/harness/{domain}/roles/{role}.md` | A durable responsibility that needs a separate contract |
| Intermediate handoff | `_workspace/{phase}_{role}_{artifact}.md` | A default naming pattern for inspectable or resumable work |

Keep established paths and schemas when existing consumers rely on them. If a
migration needs an inventory, `_workspace/00_contract_inventory.md` is an
available path for its findings. Root `AGENTS.md` holds repo-wide guidance.
The [AGENTS Authoring Guide](https://github.com/SaehwanPark/meta-harness/blob/main/.agents/skills/harness/references/agents-md-guide.md)
shows what belongs there.

## Generated skills

Begin each `SKILL.md` with YAML frontmatter containing `name` and `description`.
Use a short, specific description for discovery. In the body, state the goal
and include the inputs, constraints, outputs, and checks that need to be
explicit. Keep conditional details in linked references. Add steps when their
order matters.

## Team and role contracts

A team spec names responsibilities, dependencies, and the owner of synthesis
and acceptance. For a delegated role, state its inputs, expected result,
acceptance criteria, and access boundaries. Add workspace, communication,
permissions, escalation, and fallback details where the workflow depends on
them. Explicit write ownership can be advisory. Use enforcement or isolation
where necessary, and serialize conflicting work when those guarantees are
unavailable. Preserve partial output and report missing required results.

Skills contain reusable behavior, role contracts define responsibility, and
runtime profiles map that work to the selected client. Keep native profiles
rippable. Let settings inherit unless the role needs an override. Portable
model intent may use `inherit`, `fast`, `economy`, `balanced`, or `strong`.
See [role contracts](../architecture/role-contract.html) for compilation.

## Handoffs

Use short native messages for ephemeral coordination. For audit, resumption,
or later consumption, use a durable runtime record or a file with a stable
path. Include its producer, consumer, expected contents, and completion state.
Use an existing deliverable if it already meets that contract.

For explicitly requested experiments, preserve a baseline and log every
candidate, including crashes and timeouts, in
`_workspace/experiments/{run}/results.tsv`. Keep the evaluator fixed. Persist
setup and summary separately when the ledger and repository history cannot
carry the required evidence.

## Getting started

Run `meta-harness install --scope project --target /path/to/repo --agent generic`
to install the skill. A source checkout can use `python scripts/install_harness.py`
with the same subcommand and options. See the [installation guide](../installation.html)
and the [starter research example](starter-research/README.html).
