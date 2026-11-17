# Codex Agent Adapter

| Capability | Mapping in the selected Codex environment |
| --- | --- |
| Skills | `supported` through `.agents/skills/` and applicable `AGENTS.md`. Keep any selected compatibility mirror derived from the canonical skill. |
| Roles and subagents | Use available built-in workers for bounded tasks. Optional custom role profiles live under `.codex/agents/` and require native agent support. |
| Write isolation | Shared-checkout ownership is `advisory`. Isolate worktrees or stateful tests where required. |
| Communication | Use verified native messaging for in-run results. Parent summaries or durable artifacts cover unavailable channels or state. |
| Model | Inherit the parent settings unless the role needs an available override. |

For a stable role, use the [inactive TOML template](../templates/codex-agent.toml) where a custom profile helps. Preserve the role's access and output contract and reference the portable skill. The fallback for unavailable workers or unsafe shared mutations is direct or serialized execution where it preserves acceptance. Surface any gaps in required results.
