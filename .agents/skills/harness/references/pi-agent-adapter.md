# Pi Agent Adapter

| Capability | Base Pi | With optional `pi-safe-agent-team` |
| --- | --- | --- |
| Skills | `supported` via project `.agents/skills/` and applicable `AGENTS.md`, subject to trust and configuration | Same portable skills |
| Roles | Root execution. Worker spawning needs an optional integration | Verify worker and lifecycle tools enabled in the selected configuration |
| Write isolation | Shared-workspace ownership is `advisory`; use isolated worktrees or separate resources | Use verified broker ownership and write fencing for the resources it covers |
| Communication | Parent summaries or deterministic workspace handoffs | Use public messaging, durable task state, or mailbox features where verified |
| Model | Inherit unless a role needs Pi's provider, model, or thinking controls | Map the same semantic intent through available per-worker controls |

Keep the portable role independent of the extension's internal protocol. When worker features or enforcement are unavailable, run directly or serialize conflicts as the fallback. Report any missing required result.
