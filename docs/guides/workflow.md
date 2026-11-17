---
title: Designing a Portable Workflow
description: Choose the smallest reusable agent workflow and verify it against the work it needs to support.
layout: default
---

# Designing a Portable Workflow

## Understand the work

Start with the desired outcome, acceptance criteria, constraints, and existing
repository guidance. Inspect nearby skills and contracts for overlap. A broad
inventory is useful during a migration or a drift audit. For a small skill
change, inspect the affected paths and callers.

## Choose the smallest reusable design

Handle one-off work directly. For recurring work, start with one skill that
records project-specific commands, decisions, or checks. Add a team spec when
the work has stable coordination requirements, and add role briefs only for
responsibilities that need a separate contract. Keep root `AGENTS.md` limited
to repo-wide rules.

Delegate authorized work when independent slices benefit from specialization,
parallelism, or context isolation. Assign bounded inputs, outputs, and write
ownership. Give final synthesis to one owner. Isolate shared mutable state or
run conflicting work in sequence. See the [pattern guide](patterns.html).

Keep in-run results in native messages. Use a deterministic handoff when a
later consumer must inspect or resume the work, and reuse the deliverable if
it already serves that purpose. Describe material failure modes and preserve
partial evidence. See the [output specifications](../harness/README.html).

## Validate and simplify

Check discovery, paths, and producer/consumer agreement. Try a representative
request and any failure scenario that could affect correctness. When changing
delegation, exercise unavailable capabilities and missing branches. When
reducing instructions, compare against the previous version where practical
and check what the model reads and produces. Keep runtime mappings removable
and inherit model settings by default.
