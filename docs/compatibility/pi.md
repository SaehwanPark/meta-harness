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

Keep Pi extension configuration outside the canonical skill so it remains
removable. The installer previews detected subagent extensions using the
project's `.pi` directory and the user agent directory
(`PI_CODING_AGENT_DIR` or `~/.pi/agent`). It looks for recognizable package
names and local extension names. Verify in Pi which tools load in the
target session, including project trust and extension settings.

Reuse an available subagent extension. If none is available and you want
delegation, install the preferred package with `pi install npm:pi-subagents`.

## Capability profile

| Capability | Base Pi | Pi with a subagent extension |
| --- | --- | --- |
| Agent Skills and progressive disclosure | Supported | Supported |
| Spawned workers | Run work in the root session | Verify spawning and lifecycle tools |
| Messaging and task state | Use portable handoffs as needed | Use the features exposed by the selected extension |
| Ownership and write isolation | Isolate work or serialize conflicts | Verify enforcement before relying on it |
| Model/provider/thinking routing | Supported by Pi configuration | Available per worker where the extension supports it |

## Lowering and fallback

When delegation is unavailable, use the portable skill in the root Pi
session. Serialize conflicting writes and persist cross-session results
under `_workspace/` when another session needs them.

## Rippability

Removing Pi extensions or team configuration leaves `.agents/skills/`,
`docs/harness/`, and `_workspace/` usable. Keep model/provider choices and
recovery heuristics in the optional runtime layer.

See [runtime capabilities](../architecture/runtime-capabilities.html) and the
[compatibility matrix](README.html) for shared policy.
