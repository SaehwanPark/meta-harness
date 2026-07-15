# Optional Codex Agent Adapter

Use this reference only when the target repository runs current Codex and native subagents materially improve the chosen portable Harness pattern. The portable workflow contract remains authoritative; this adapter maps that contract onto Codex execution without making Codex a dependency.

## Selection

Keep work in the main agent when the task is small, tightly coupled, or write ownership cannot be separated. Delegate when work units are independent and at least one of these benefits is concrete:

- noisy exploration, tests, logs, or source material can stay out of the main context
- several read-heavy angles can run independently
- a narrow specialist instruction or tool policy improves a bounded result
- isolated implementation branches can be reconciled by one integration owner

Use Codex's built-in general-purpose or exploration agents before creating a custom agent. Create a custom agent only when a stable, reusable execution profile needs distinct instructions, tools, permissions, or model policy. A reusable skill still owns domain knowledge and workflow; a custom agent owns runtime execution settings and may use that skill.

## Read-Heavy Delegation

- Give each worker one independent question, the same input snapshot, and an explicit output contract.
- Ask for distilled evidence and conclusions instead of raw logs.
- Name one parent or orchestrator as the synthesis owner.
- Preserve branch artifacts only when later inspection, audit, resumption, or conflict resolution needs them.

## Write Isolation and Ownership

- Assign non-overlapping files or components before parallel edits begin.
- Use separate worktrees or checkouts when changes could touch the same paths or shared generated state.
- Serialize writes when ownership cannot be separated safely.
- Keep final integration, conflict resolution, and acceptance checks with one owner.

Native subagents do not make concurrent writes to a shared checkout safe by themselves.

Apply the same rule to tests and commands that share databases, snapshots, generated state, ports, services, devices, or other mutable resources. Parallelize them only when those resources are isolated or known to be concurrency-safe.

## Concurrency and Depth

- Choose concurrency from the number of genuinely independent work units and available runtime capacity; do not pin a repository-wide value in a portable harness.
- Keep one downstream delegation layer by default.
- Allow deeper delegation only when the domain naturally decomposes, every layer has a stable output, and the team spec declares the depth and synthesis policy.

## Permissions

Subagents normally inherit the parent task's effective permissions and available tools. Set the parent permission boundary before delegation. Use a narrower custom-agent sandbox only when the worker's job benefits from it, such as a read-only reviewer.

Do not design a reusable workflow around approvals that cannot be surfaced in its intended interactive or non-interactive runtime. A blocked worker should return the failed action and remaining uncertainty to the parent.

## Synthesis and Partial Failure

Before spawning workers, define:

- the synthesis owner and acceptance criteria
- how duplicate or conflicting results are reconciled
- whether partial results are useful
- which worker failures may be skipped
- which failures require retry, serialization, or user escalation

The final response must disclose missing branches and unresolved conflicts. Do not let a successful synthesis hide incomplete worker coverage.

## Custom Agent Template

Start from [`../templates/codex-agent.toml`](../templates/codex-agent.toml) when a stable custom execution profile is justified. The template is intentionally inactive inside the Harness package. Copy and adapt it into a target repository's native Codex agent directory only after the repository chooses to depend on that behavior.

Leave model and reasoning settings unspecified unless the target repository has measured reasons to pin them. Inherited runtime defaults keep the adapter easier to update as Codex improves.
