# Harness Architecture Patterns

Use direct execution or one reusable skill when the work fits in one context. A coordination pattern earns its place when it handles a real dependency, concurrency opportunity, or acceptance gate.

| Pattern | Use when | Capture in the workflow |
| --- | --- | --- |
| Pipeline | Later steps need earlier results | Order and the information each dependent step uses |
| Fan-out/Fan-in | Independent slices benefit from parallel work or context isolation | Common input, branch boundaries, and one synthesis owner |
| Expert Pool | Different requests need different specialists | Selection criteria and a fallback for ambiguous requests |
| Producer-Reviewer | An independent check changes acceptance | Review criteria, actionable findings, and a stopping condition |
| Supervisor | New tasks or blockers change routing during execution | Queue ownership and reassignment only where needed |
| Hierarchical Delegation | A large subdomain needs its own coordinator | Bounded subgoals and synthesis ownership at each level |

Combine patterns only where each one solves a distinct problem. Keep one downstream delegation layer by default. Use native messages for short results and stable artifacts for handoffs that need independent inspection or resumption. See [examples](team-examples.md) for the difference in file layout.
