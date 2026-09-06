---
title: Compatibility Matrix
description: Choose the portable or first-class runtime path for Meta Harness.
layout: default
---

# Compatibility Matrix

Meta Harness has one portable skill source and four actively supported runtime
targets. First-class means that the target has an owned adapter guide,
capability mapping, and validation responsibility; it does not mean every
feature is identical in every configuration.

## Support levels

| Runtime | Status | Skill path | Native execution material | Typical capabilities |
| --- | --- | --- | --- | --- |
| [Pi](pi.html) | **First-class** | `.agents/skills/harness/` | Optional Pi extension; no required mirror | Skills; model/provider routing; workers and rich coordination with `pi-safe-agent-team` |
| [Codex](codex.html) | **First-class** | `.agents/skills/harness/` or `~/.agents/skills/harness/` | Optional `.codex/agents/` | Skills; custom agents; runtime-dependent isolation, messaging, and persistence |
| [Antigravity](antigravity.html) | **First-class** | `.agents/skills/harness/` | Optional runtime-native agent profiles | Skills; subagents and model/tool controls where enabled by the runtime |
| [Cursor CLI / Agent](cursor.html) | **First-class** | `.agents/skills/harness/` | Optional `.cursor/agents/` | Skills; native profiles; runtime-dependent background execution and isolation |
| [Generic](generic.html) | **Best effort** | Client-defined Agent Skills path, commonly `.agents/skills/` | None guaranteed | Portable instructions only; no assumed workers, isolation, messaging, or model routing |

The portable source remains `.agents/skills/harness/` in a project and
`~/.agents/skills/harness/` for a user-level install. Native profiles are
adapters or generated artifacts, never a second source of truth.

## Capability and degradation policy

Adapters report capabilities as **supported**, **supported with extension**,
**advisory**, or **unsupported**. If a runtime cannot enforce exclusive writes,
use an isolated workspace, explicit non-overlapping ownership, or serialize the
work. If native communication is unavailable, use a parent summary or a
`_workspace/` handoff. Never silently claim a stronger guarantee.

## Rippability

You can remove `.codex/agents/`, `.cursor/agents/`, or other native profiles
without removing `.agents/skills/`, `docs/harness/`, or `_workspace/`. Runtime
settings, retries, and model choices belong in removable adapters.

## Legacy clients

ForgeCode, Droid, OpenHands, and Aider are retained as **unverified and
deprecated** migration notes only. They are not first-class support targets.
Use the [generic guide](generic.html) unless you have independently verified
the client's Agent Skills behavior.

## Related architecture

- [Portable contract](../architecture/portable-contract.html)
- [Runtime capabilities](../architecture/runtime-capabilities.html)
- [Role contract](../architecture/role-contract.html)
- [Handoffs](../architecture/handoffs.html)

See the [installation guide](../installation.html) for the currently shipped
installer surface. Runtime-native generation remains optional and must not
replace the portable contract.
