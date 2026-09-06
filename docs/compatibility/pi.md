---
title: Pi Compatibility
description: Use the canonical Agent Skills tree with Pi, with optional team capabilities.
layout: default
---

# Pi Compatibility

Pi is a first-class Meta Harness target. Pi can consume the canonical Agent
Skills tree directly; no Pi-specific copy of the skill is required.

## Paths

- Project skill: `.agents/skills/harness/`
- User skill: `~/.agents/skills/harness/`
- Optional extensions: Pi's configured extension/package location
- Durable portable artifacts: `docs/harness/` and `_workspace/`

The installer’s `standard` layout is the portable starting point. Keep any Pi
extension configuration outside the canonical skill so it remains removable.

## Capability profile

| Capability | Base Pi | Pi with `pi-safe-agent-team` |
| --- | --- | --- |
| Agent Skills and progressive disclosure | Supported | Supported |
| Spawned workers | Extension/runtime dependent | Supported |
| Parent/peer messaging and clarification | Extension dependent | Supported |
| Task state, ownership, and write fencing | Not assumed | Supported by the integration when configured |
| Model/provider/thinking routing | Supported by Pi configuration | Supported per worker where configured |
| Isolated workspaces and lifecycle recovery | Configuration dependent | Supported where the integration exposes it |

`pi-safe-agent-team` is optional and is not a portable dependency. The guide
describes the semantic boundary; it does not couple Meta Harness to an
internal broker protocol.

## Lowering and fallback

If the optional team integration is unavailable, use the portable skill in the
root Pi session. Do not pretend advisory ownership is mechanical: serialize
conflicting writes and persist cross-session results under `_workspace/`.
Single-agent execution is the correct default for tightly coupled work.

## Rippability

Removing Pi extensions or team configuration leaves `.agents/skills/`,
`docs/harness/`, and `_workspace/` usable. Keep model/provider choices and
recovery heuristics in the optional runtime layer.

See [runtime capabilities](../architecture/runtime-capabilities.html) and the
[compatibility matrix](README.html) for shared policy.
