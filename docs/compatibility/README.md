# Compatibility Guides

Harness keeps `.agents/skills/harness/` as the shared install path and adds native mirrors only where an agent benefits from them.

| Agent | Shared skill path | Native path | Native files for agent-specific behavior |
| --- | --- | --- | --- |
| ForgeCode | `.agents/skills/harness/` or `~/.agents/skills/harness/` | `.forge/skills/harness/` or `~/forge/skills/harness/` | `.forge/agents/` or `~/forge/agents/` |
| Codex | `.agents/skills/harness/` or `~/.agents/skills/harness/` | `.codex/skills/harness/` or `~/.codex/skills/harness/` | none |
| Droid | `.agents/skills/harness/` or `~/.agents/skills/harness/` | `.factory/skills/harness/` or `~/.factory/skills/harness/` | `.factory/droids/` or `~/.factory/droids/` |
| OpenHands | `.agents/skills/harness/` or `~/.agents/skills/harness/` | none | `.openhands/` for setup scripts, hooks, and repo customization |
| Aider | `.agents/skills/harness/` or `~/.agents/skills/harness/` | none | `.aider.conf.yml` for `AGENTS.md` loading |

Use the shared path whenever you want one Harness skill tree that multiple agents can reuse. Add the native mirror only when the client has its own skill discovery path or separate subagent format.

- [ForgeCode](forgecode.md)
- [Codex](codex.md)
- [Droid](droid.md)
- [OpenHands](openhands.md)
- [Aider](aider.md)
