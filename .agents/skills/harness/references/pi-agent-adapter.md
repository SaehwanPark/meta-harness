# Pi Agent Adapter

Use the subagent extension already available in the target Pi session. If
delegation is useful and the user wants to add it, recommend
`pi install npm:pi-subagents`. Confirm which tools and guarantees the active
extension exposes before designing around it.

| Capability | Base Pi | With an optional subagent extension |
| --- | --- | --- |
| Skills | `supported` via project `.agents/skills/` and applicable `AGENTS.md`, subject to trust and configuration | Same portable skills |
| Roles | Run in the root session | Verify worker spawning and lifecycle tools |
| Write isolation | Ownership is `advisory`. Use isolated worktrees or separate resources | Verify any ownership and write enforcement before relying on it |
| Communication | Parent summaries or deterministic workspace handoffs | Use messaging and task state where available |
| Model | Inherit unless the role needs Pi's provider, model, or thinking controls | Map model intent through available per-worker controls |

Keep generated skills and role briefs portable. Put extension setup and
tool-specific instructions in the Pi adapter, and exercise the root-session
fallback when delegation is unavailable. Serialize conflicting writes or
isolate them as needed. Report any missing required result.
