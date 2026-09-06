---
title: Phase 0 Audit and Six-Phase Workflow
description: The portable Meta Harness path from repository inventory to a validated workflow.
layout: default
---

# Phase 0 Audit and Six-Phase Workflow

Harness starts with an inventory because an existing repository is not a blank
slate. The audit protects existing sources of truth, identifies drift, and
chooses the smallest safe operation before design work begins. It is followed
by six execution phases; small tasks may still remain single-agent.

## 0. Inventory and drift audit

Inspect existing `.agents/skills/`, `AGENTS.md`, `docs/harness/`, runtime
profiles, adapters, installation paths, and capability evidence. Detect stale
or duplicated skills, roles, profiles, and documentation. Classify the work as
one of:

- new harness;
- existing harness extension;
- runtime adapter update;
- drift repair;
- skill-only update;
- architecture refactor; or
- maintenance/audit.

**Output:** a concise inventory with `existing_skills`, `existing_roles`,
`detected_runtimes`, `stale_artifacts`, `compatibility_risks`, and a
`recommended_action`. Do not overwrite an existing source of truth silently.

## 1. Domain analysis

Inspect the repository, request, existing skills, and quality bar. Identify the
task classes the workflow should serve and the work that should remain outside
its boundary.

**Output:** a concise domain summary with task inventory, constraints, and reuse
notes.

## 2. Team architecture design

Choose the smallest coordination shape that preserves quality. Record whether
the value comes from ordering, specialization, parallel read-only coverage,
context isolation, or explicit review. Name the synthesis owner before
parallel work starts.

**Output:** a pattern choice, role list, ownership boundaries, and handoff plan.

## 3. Role and artifact definition

Turn the architecture into responsibilities another contributor can execute.
Name inputs, outputs, skills, resource reads/writes, ownership enforcement,
workspace preference, communication/escalation, permissions, semantic model
policy, review edges, and failure policy. Keep runtime execution settings out
of the portable role.

**Output:** a team spec or role brief for each durable responsibility.

## 4. Skill generation

Promote reusable domain behavior into `.agents/skills/`. Every generated
`SKILL.md` starts with YAML frontmatter containing `name` and `description`,
then states when it applies, what it needs, what it produces, and how it is
validated. Keep runtime-specific settings in removable adapters.

**Output:** a lean specialist or orchestrator skill with deeper detail in
`references/` only when progressive disclosure earns its keep.

## 5. Integration and orchestration

Connect phases through the smallest useful handoff. Use a short in-thread
summary for ephemeral coordination. Use a durable coordination record or
`_workspace/` artifact when another phase or contributor must inspect, resume,
audit, or synthesize the result. Lower capability requirements explicitly;
serialize conflicting writes when isolation or enforcement is unavailable.

**Output:** an end-to-end workflow with named handoffs, ownership, fallback,
partial-failure behavior, and a shallow hierarchy (`root → worker` by default).

## 6. Validation and testing

Check paths, internal references, selection boundaries, normal flow, and at
least one failure flow. Validate unavailable capabilities, conflicting writes,
worker failure, missing synthesis branches, and adapter removal when the
workflow is multi-agent. For autonomous experiments, establish a baseline,
keep evaluation read-only, record every candidate, and preserve the ledger.

**Output:** a validation checklist and a report of remaining gaps or
simplifications.

## The delegation gate

Before adding workers, answer all six questions:

1. Which work units are independent?
2. Is the benefit specialization, latency, or context isolation?
3. Which paths and test resources does each writer own?
4. Are permissions and tools sufficient?
5. Who owns synthesis and acceptance?
6. What happens if a worker fails or results conflict?

If any answer is unclear, keep the workflow single-agent or sequential. See the
[architecture pattern guide](patterns.html) and
[output specifications](../harness/README.html) for durable contracts.
