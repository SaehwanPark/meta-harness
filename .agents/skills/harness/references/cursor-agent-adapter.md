# Cursor CLI / Agent Adapter

| Capability | Mapping in the selected Cursor CLI or Agent environment |
| --- | --- |
| Skills | `supported` when Agent Skills discovery is enabled. Keep the canonical `.agents/skills/` tree and verify which project instructions apply. |
| Roles | Optional `.cursor/agents/<role>.md` profiles depend on native subagent support. Use the root session for direct work. |
| Write isolation | Shared-checkout boundaries are `advisory`. Background execution alone provides no write fence. |
| Communication | Verify native result channels and retention before relying on them. Use a parent summary or durable workspace artifact as needed. |
| Model | Inherit unless an available model control is needed for a role. |

When native profiles, workers, or isolation are unavailable, use direct work or serialize conflicting tasks as the fallback. Keep the profile removable and surface any missing required result.
