---
title: Compatibility Matrix
description: Choose the shared or native skill path for each supported agent client.
layout: default
---

# Compatibility Matrix

Meta Harness keeps one portable source tree and adds native mirrors only when
a client benefits from a separate discovery path. The shared tree is always
the source of truth.

| Agent | Shared skill path | Native path | Native files for agent-specific behavior |
| --- | --- | --- | --- |
| ForgeCode | `.agents/skills/harness/` or `~/.agents/skills/harness/` | `.forge/skills/harness/` or `~/forge/skills/harness/` | `.forge/agents/` or `~/forge/agents/` |
| Codex | `.agents/skills/harness/` or `~/.agents/skills/harness/` | `.codex/skills/harness/` or `~/.codex/skills/harness/` | optional `.codex/agents/` or `~/.codex/agents/` |
| Droid | `.agents/skills/harness/` or `~/.agents/skills/harness/` | `.factory/skills/harness/` or `~/.factory/skills/harness/` | `.factory/droids/` or `~/.factory/droids/` |
| OpenHands | `.agents/skills/harness/` or `~/.agents/skills/harness/` | none | optional `.openhands/` setup files |
| Aider | `.agents/skills/harness/` or `~/.agents/skills/harness/` | none | `.aider.conf.yml` read configuration |

Use the shared path when several clients should consume the same reusable
workflow. Add a native mirror only for client-specific discovery or execution
behavior. Keep model settings and native agent definitions out of the
portable skill contract.

## Choose a client guide

- [ForgeCode](forgecode.html) — shared and native ForgeCode paths.
- [Codex](codex.html) — optional project/user mirror and native adapter.
- [Droid](droid.html) — shared tree plus optional Factory mirror.
- [OpenHands](openhands.html) — shared tree with repository setup only when needed.
- [Aider](aider.html) — shared tree plus the required AGENTS read-list follow-up.

## Shared versus native

The shared path is the right default when:

- portability across clients matters;
- a workflow should be installed without activating custom agents;
- the target repository owns its own AGENTS.md, README.md, and docs;
- model and runtime configuration should remain inherited.

The native path is useful only when a client does not discover the shared
directory on its own. The installation command can create both paths for
Codex, ForgeCode, and Droid.

> [!IMPORTANT]
> Keep reusable Harness behavior in the shared skill tree. Use native
> directories for native behavior, not as a second source of truth.

Return to the [installation guide](../installation.html) for the command
options, or read the [Codex guide](codex.html) for the most complete native
mirror example.
