# Codex Agent Adapter

Use this optional adapter to lower a portable Harness role onto current OpenAI Codex. The portable skill and runtime-neutral role contract remain authoritative; Codex-native profiles are generated execution material, not a second source of workflow semantics. This adapter may be removed without removing `.agents/skills/` or `_workspace/` artifacts.

Read [`runtime-capabilities.md`](runtime-capabilities.md) before selecting a profile. Codex behavior varies with the installed release, invocation mode, and enabled native-agent features; do not claim a capability that the selected environment has not exposed.

## Capability mapping

- **Skills — `supported`**: keep reusable skills in `.agents/skills/`. A native Codex mirror may be generated for discovery when requested, but it must not become the canonical copy. Applicable `AGENTS.md` instructions remain part of the execution context.
- **Roles and subagents — `supported` when enabled**: use built-in general-purpose/exploration agents for one-off work. Use a custom agent only when a stable role needs distinct instructions, tools, permissions, or model policy. Native definitions belong in the target repository's `.codex/agents/`; the inactive template at [`../templates/codex-agent.toml`](../templates/codex-agent.toml) is a starting point, not an installed agent.
- **Write isolation — configuration-dependent**: native subagents do not make shared-checkout writes safe by themselves. Prefer separate worktrees/checkouts for independent mutable branches, then integrate through one owner. If isolation cannot be established, assign non-overlapping files or serialize the work.
- **Communication — configuration-dependent/advisory**: use only messaging, task state, or background facilities actually provided by the selected Codex mode. Otherwise use parent-mediated summaries and deterministic `_workspace/` artifacts. Do not infer peer messaging or durable recovery from the existence of subagents.
- **Model policy — `supported`/inherited**: map semantic policies (`inherit`, `fast`, `economy`, `balanced`, `strong`) to Codex's available model/reasoning controls. Leave model and reasoning settings inherited by default; pin them only for a measured repository need and keep the pin in the runtime profile.

## Selection and lowering

Keep work in the main agent when it is small, tightly coupled, or cannot be safely isolated. Delegate only when specialization, context isolation, or parallel read-heavy work has a concrete benefit. Give each worker one independent question, a shared input snapshot, and an explicit output contract. Name one synthesis owner before spawning.

A portable role may declare:

```yaml
role: implementation-worker
reads: [src/**]
writes: [src/parser/**]
workspace: isolated
model_policy: balanced
communication:
  parent: required
permissions:
  spawn: false
```

A generated Codex profile should preserve those semantic fields in its instructions while adding only runtime settings:

```toml
name = "implementation-worker"
description = "Implement the parser slice within the declared boundary."
developer_instructions = """
Use the portable implementation skill.
Own only src/parser/**; report evidence and blockers to the parent.
Do not delegate again.
"""
# Add model, reasoning, tools, and permissions only when justified.
```

Do not hand-edit a generated profile and then treat that change as canonical. Promote intentional behavior back to the portable role contract first.

## Isolation, depth, and partial failure

- Assign non-overlapping files/components before parallel edits begin.
- Isolate tests and commands that share databases, snapshots, generated state, ports, services, or devices.
- Keep one downstream delegation layer by default. A deeper tree needs explicit domain justification, stable outputs at each layer, and a declared synthesis policy.
- Define which worker failures are skippable before execution. A missing required branch, conflict, permission denial, or setup failure must remain visible in the final synthesis.
- A blocked worker returns the failed action and remaining uncertainty; it is not silently marked complete.

## Adapter acceptance checklist

- **Skill discovery:** canonical `.agents/skills/` plus applicable `AGENTS.md`; an optional `.codex/skills/` mirror is generated only when selected.
- **Role instantiation:** built-in subagents are preferred for one-off work; `.codex/agents/` custom profiles are optional generated material for stable roles.
- **Writes/isolation:** use separate worktrees/checkouts where possible; otherwise explicit non-overlap and serialization. Native subagents alone are not enforcement.
- **Communication/handoffs:** use native Codex messaging/background/task facilities only when present and verified; otherwise parent summaries and `_workspace/` durable records.
- **Model selection:** translate semantic policy to available Codex model/reasoning controls; inherit by default.
- **Unavailable capabilities:** mark the status, lower to an isolated or serialized plan, and disclose partial failure or unresolved coordination.
