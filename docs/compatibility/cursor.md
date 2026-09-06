---
title: Cursor CLI and Agent Compatibility
description: Use Meta Harness with Cursor CLI or Cursor Agent through shared skills and optional native profiles.
layout: default
---

# Cursor CLI / Agent Compatibility

Cursor CLI and Cursor Agent are first-class Meta Harness targets. This status
covers those agent surfaces, not every feature of the broader Cursor IDE
extension ecosystem.

## Paths

- Portable project skill: `.agents/skills/harness/`
- Portable user skill: `~/.agents/skills/harness/`
- Optional native profiles: `.cursor/agents/`
- Durable portable artifacts: `docs/harness/` and `_workspace/`

Keep role semantics and domain instructions in `.agents/skills/` and generate
`.cursor/agents/` files only for Cursor-specific execution settings.

## Capability profile

Cursor can consume Agent Skills and native agent profiles. Model selection,
subagent invocation, foreground/background execution, context isolation, and
worktree or copy behavior depend on the selected Cursor surface and project
configuration. Treat native communication and write enforcement as
runtime-dependent until verified.

A portable role can request `workspace: isolated`, `writes: tests/**`, and
`model_policy: balanced`; the Cursor adapter may lower that to a native profile
while leaving test methodology in the shared skill tree.

## Degradation

If a worktree or isolated copy is unavailable, use explicit non-overlapping
ownership or serialize writes. If subagents or messaging are unavailable, run
the role in the current agent and persist a deterministic `_workspace/`
summary. Never claim a background worker provides isolation by itself.

## Rippability

Removing `.cursor/agents/` leaves the shared skills and portable contracts
usable. See the [portable contract](../architecture/portable-contract.html),
[runtime capabilities](../architecture/runtime-capabilities.html), and
[compatibility matrix](README.html).
