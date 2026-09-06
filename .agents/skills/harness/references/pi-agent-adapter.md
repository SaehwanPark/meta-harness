# Pi Agent Adapter

Use this adapter when lowering a portable Harness role onto Pi. The canonical source remains `.agents/skills/`; do not fork a Pi-specific copy of a skill. This adapter is removable: deleting Pi-specific configuration must leave the portable skill, role contract, and `_workspace/` handoffs usable.

Read [`runtime-capabilities.md`](runtime-capabilities.md) first. Pi capability status depends materially on whether the optional `pi-safe-agent-team` integration is installed.

## Capability boundary

### Base Pi

- **Skills — `supported`**: discover the project `.agents/skills/` tree and applicable `AGENTS.md` instructions. A user-level shared skills location may be used when the installation policy selects it. Project trust and local instruction scope still apply.
- **Roles and subagents — `supported_with_extension`**: a root Pi session can execute a portable role directly. Worker spawning and native role profiles require the relevant Pi extension/configuration; bare Pi must not be treated as a team runtime.
- **Write isolation — `advisory`**: ordinary prompts and shared checkout conventions do not mechanically fence writes. Use isolated worktrees/copies, explicit non-overlapping ownership, or serialization. Never run concurrent conflicting writes merely because several workers were requested.
- **Communication — `advisory`**: without a broker, use parent-mediated summaries and deterministic `_workspace/` artifacts. Do not assume peer messaging, durable mailboxes, or resumable task state.
- **Model policy — `supported`**: map `inherit`, `fast`, `economy`, `balanced`, and `strong` to the provider/model/thinking controls available in the current Pi session. Exact IDs belong in an optional runtime override, not in the portable role.

### Pi with `pi-safe-agent-team`

Treat this as an optional first-party-quality enhancement, not a portable dependency. Through its public tools, it can provide the stronger semantics represented by:

- child and (when enabled) recursive worker spawning;
- parent/peer messages, clarification, and escalation;
- durable mailbox and task-board state;
- hierarchical resource ownership, mutable borrowing, and write fencing;
- shared or isolated workspace modes;
- explicit provider/model/thinking routing and capability restrictions;
- lifecycle status, cancellation, journal, and recovery information.

The adapter must still keep the default hierarchy shallow (`root → worker`, with `root → coordinator → worker` only when justified). Technical recursive spawning is not a reason to create deep orchestration.

Meta Harness depends only on the public semantic boundary. It must not import or reproduce the broker's internal protocol. If the extension is absent, lower each requirement using the fallback rules below.

## Role lowering

A portable role can declare, for example:

```yaml
role: reviewer
writes: []
workspace: shared-readonly
model_policy: strong
communication:
  parent: required
  peers: optional
permissions:
  spawn: false
```

A Pi materialization may select the corresponding runtime settings:

```text
worker role: reviewer
workspace: shared (read-only by contract; enforce with broker or isolate)
may_write_repo: false
may_spawn: false
provider/model/thinking: derived from model_policy
```

Keep responsibility, inputs, outputs, skills, quality bar, and acceptance criteria in the portable role. Keep Pi provider, model, thinking, tool restrictions, and extension-specific settings in the removable adapter/profile.

## Safe fallback when the extension is unavailable

1. Run the portable skill in the root session when no independent worker is needed.
2. For independent read-heavy work, use separate Pi contexts only if their inputs and outputs are isolated and the synthesis owner is explicit.
3. For mutable work, select isolated worktrees/copies or explicit non-overlapping file ownership.
4. Serialize any work whose writes, generated state, database, service, or other mutable resource could conflict.
5. Use `_workspace/` for durable results, blockers, and missing branches. State which guarantees are advisory.

A worker spawn failure, permission denial, unavailable model, or lost communication is a partial failure. Return the failed branch and remaining uncertainty to the parent; do not silently treat it as completed.

## Adapter acceptance checklist

- **Skill discovery:** `.agents/skills/` is canonical; `AGENTS.md` and project trust/instruction scope remain in force.
- **Role instantiation:** direct root execution works on base Pi; worker/native profiles and team behavior require optional extension support.
- **Writes/isolation:** broker-enforced resource borrowing or isolated workspaces are preferred; otherwise use ownership declarations and serialization.
- **Communication/handoffs:** use public parent/peer messaging and durable task/mailbox facilities only when the safe-agent integration is active; otherwise parent summaries and `_workspace/` artifacts.
- **Model selection:** semantic model policies map to Pi provider/model/thinking controls; omit exact overrides unless justified.
- **Unavailable capabilities:** report the status, lower to the next safe mechanism, and serialize when safety cannot be enforced.
