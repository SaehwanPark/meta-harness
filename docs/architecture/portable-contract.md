---
title: Portable Contract
description: The source-of-truth and rippability rules for Meta Harness workflows.
layout: default
---

# Portable Contract

Meta Harness does not maintain four separate harnesses. It maintains one
portable workflow model and actively validates runtime adapters for Pi, Codex,
Antigravity, and Cursor CLI/Agent.

## Source-of-truth order

1. Portable skill semantics in `.agents/skills/`.
2. Portable team and role specifications in `docs/harness/`.
3. The runtime capability definition.
4. A runtime adapter and its lowering rules.
5. Generated native profiles.

A generated native profile is not canonical. Promote intentional changes back
to the portable contract instead of editing generated output as the source of
truth.

## Canonical paths

| Artifact | Canonical location | Purpose |
| --- | --- | --- |
| Reusable skills | `.agents/skills/` | Runtime-neutral behavior and references |
| Team and role contracts | `docs/harness/` | Responsibilities, outputs, ownership, and failure policy |
| Durable handoffs | `_workspace/` | Inspectable and resumable work products |
| Runtime adapters | Public compatibility and architecture guides | Removable lowering guidance |

## Rippability

Deleting `.codex/agents/`, `.cursor/agents/`, or other runtime-generated
profiles must not delete `.agents/skills/`, `docs/harness/`, or the
`_workspace/` contract. Runtime settings, model choices, retries, and native
syntax belong in the removable adapter layer.

## Support boundary

First-class means a runtime has an owned guide, capability mapping, and a
validation responsibility. It does not mean every runtime feature is
identical. Generic Agent Skills consumption is best effort; unknown clients
must not be presented as equivalent to first-class targets. ForgeCode, Droid,
OpenHands, and Aider pages are retained only as deprecated, unverified
migration notes.
