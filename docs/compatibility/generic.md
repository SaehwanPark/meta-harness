---
title: Generic Agent Skills Compatibility
description: Best-effort guidance for clients without a validated Meta Harness runtime adapter.
layout: default
---

# Generic Compatibility

Generic mode is a best-effort portable Agent Skills contract, not a
first-class runtime integration. Use it when a client can load Markdown skills
but Meta Harness has no validated native adapter for that client.

## Paths

- Project skill: `.agents/skills/harness/`
- User skill: `~/.agents/skills/harness/`
- Durable contracts: `docs/harness/`
- Durable handoffs: `_workspace/`

The client may require a different Agent Skills discovery path. Copy or link
the canonical skill according to that client’s documented convention; do not
create a second source of truth.

## What is portable

The six-phase workflow, role semantics, deterministic handoffs, and validation
prompts are portable Markdown guidance. A generic client may be able to read
`AGENTS.md` and skills, but Meta Harness does not guarantee worker spawning,
recursive delegation, messaging, ownership enforcement, workspace isolation,
permission controls, model routing, lifecycle tracking, or crash recovery.

## Safe fallback

Assume one agent and inherited runtime settings. Run tightly coupled work in a
single context. For delegated work, use explicit non-overlapping ownership and
serialize conflicting writes. Use `_workspace/` for outputs that must survive
the session. State unsupported capabilities in the plan instead of silently
weakening a correctness guarantee.

## Rippability and support

Generic mode never changes the portable contract. If the client later gains a
validated adapter, native profiles may be added without changing
`.agents/skills/`, `docs/harness/`, or `_workspace/`. Legacy client pages for
ForgeCode, Droid, OpenHands, and Aider are unverified and deprecated; use this
guide for those clients unless independently verified.
