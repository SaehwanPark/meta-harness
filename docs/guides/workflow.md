---
title: Six-Phase Workflow
description: The portable Meta Harness path from a project goal to a validated workflow.
layout: default
---

# Six-Phase Workflow

Harness uses a six-phase path because reusable coordination fails when the
project boundary, artifact contract, or review path is left implicit. Each
phase has one job and a concrete output.

## 1. Domain analysis

Inspect the repository, the request, existing skills, and the quality bar.
Identify the task classes the workflow should serve and the work that should
remain outside its boundary.

**Output:** a concise domain summary with task inventory, constraints, and
reuse notes.

## 2. Team architecture design

Choose the smallest coordination shape that preserves quality. Record whether
the value comes from ordering, specialization, parallel read-only coverage,
context isolation, or explicit review.

**Output:** a pattern choice, role list, ownership boundaries, and handoff plan.

## 3. Role and artifact definition

Turn the architecture into responsibilities another contributor can execute.
Name inputs, outputs, review edges, failure policy, and deterministic artifact
paths. Keep the final synthesis owner unambiguous.

**Output:** a team spec or role brief for each durable responsibility.

## 4. Skill generation

Promote reusable behavior into `.agents/skills/`. Every generated `SKILL.md`
starts with YAML frontmatter containing `name` and `description`, then states
when it applies, what it needs, what it produces, and how it is validated.

**Output:** a lean specialist or orchestrator skill with deeper detail in
`references/` only when progressive disclosure earns its keep.

## 5. Integration and orchestration

Connect the phases through the smallest useful handoff. Use a short in-thread
summary for ephemeral work. Use `_workspace/` when another phase or
contributor must inspect, resume, audit, or synthesize the result.

**Output:** an end-to-end workflow with named handoffs, ownership, fallback,
and partial-failure behavior.

## 6. Validation and testing

Check paths, internal references, selection boundaries, normal flow, and at
least one failure flow. For autonomous experiments, establish a baseline,
keep evaluation read-only, record every candidate, and preserve the ledger.

**Output:** a validation checklist and a report of remaining gaps or
simplifications.

## A portable package shape

~~~text
AGENTS.md                         # short, repo-wide rules when needed
.agents/skills/<specialist>/      # reusable behavior
docs/harness/<domain>/team-spec.md
_workspace/<phase>_<artifact>.md  # only when a durable handoff matters
~~~

The package is intentionally runtime-neutral. Native agent adapters, model
settings, and temporary recovery heuristics belong in removable integration
layers rather than the canonical workflow.

## Delegation gate

Before adding workers, answer all six questions:

1. Which work units are independent?
2. Is the benefit specialization, latency, or context isolation?
3. Which paths and test resources does each writer own?
4. Are permissions and tools sufficient?
5. Who owns synthesis and acceptance?
6. What happens if a worker fails or results conflict?

If any answer is unclear, keep the workflow single-agent or sequential.

Continue with the [architecture pattern guide](patterns.html), or start from
the [prompt library](../sample-prompts.html).
