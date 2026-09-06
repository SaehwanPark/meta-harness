# Antigravity Agent Adapter

Use this adapter when a project is executed by Google Antigravity. Portable skills and role contracts remain the source of truth; Antigravity custom-agent configuration is a removable lowering. Do not copy domain methodology into a runtime profile.

Read [`runtime-capabilities.md`](runtime-capabilities.md) first. Antigravity capabilities can depend on the installed product version, account, enabled tools, and workspace configuration. A capability is `supported` only when the selected environment exposes the corresponding semantic guarantee.

## Capability mapping

- **Skills — `supported`** when Agent Skills discovery is enabled; otherwise **`advisory`**. Discover the canonical `.agents/skills/` tree and applicable repository instruction files. If a deployment does not discover Agent Skills, use its documented import/configuration while preserving the portable files.
- **Roles and subagents — `supported_with_extension`** when custom-agent/subagent execution is enabled; otherwise **`advisory`**. Instantiate portable roles through the selected runtime configuration and keep responsibility, inputs, outputs, quality bar, and acceptance criteria portable.
- **Write isolation — `advisory`** unless an isolated worktree or workspace copy is configured. A subagent or asynchronous run is not evidence of write fencing; without isolation, assign non-overlapping paths and serialize conflicts.
- **Communication — `advisory`** unless a retained native channel is verified. Use parent/child, peer, clarification, escalation, or background-result channels only when exposed; otherwise return summaries or deterministic `_workspace/` artifacts.
- **Model policy — `advisory` or `inherit`**: translate `inherit`, `fast`, `economy`, `balanced`, and `strong` to available tiers/settings. Keep exact model names as optional overrides and do not make portable correctness depend on them.

## Lowering a portable role

A role can remain runtime-neutral:

```yaml
role: test-investigator
responsibility: identify the smallest reproducible failing case
reads: [src/**, tests/**]
writes: [tests/repro/**]
workspace:
  preference: isolated
communication:
  parent: required
  peers: optional
model_policy: balanced
permissions:
  shell: true
  write_repo: true
  spawn: false
completion:
  artifact: _workspace/test-investigator_result.md
```

The Antigravity profile should reference the portable skill, preserve the path boundary, select an isolated workspace when available, and name the parent as synthesis owner. Do not treat supported recursion depth as a recommendation: default to `root → worker`, with at most one additional coordination layer when dependencies justify it.

## Fallback and failure behavior

If custom agents, background execution, retained context, or messaging are unavailable:

1. Run the portable skill in the root session when delegation adds no concrete value.
2. Keep independent read-only investigations separate only when their inputs and outputs are isolated.
3. Isolate mutable work or serialize it; do not rely on instructions to prevent concurrent writes.
4. Use parent-mediated summaries and `_workspace/` artifacts for durable handoffs.
5. Report unavailable capabilities and any missing worker branch to the synthesis owner.

A model/tool denial, workspace setup failure, communication loss, or crashed worker is a visible partial failure. Retry or serialize only under the workflow's declared policy; never silently downgrade a required guarantee.

## Adapter acceptance checklist

- **Skill discovery:** canonical `.agents/skills/` and applicable repository instructions, with deployment-specific import settings documented when needed.
- **Role instantiation:** custom-agent/subagent execution when enabled; otherwise execute or serialize the portable role in the root context.
- **Writes/isolation:** use a worktree/workspace copy when available; otherwise enforce non-overlapping ownership by planning and serialize conflicts.
- **Communication/handoffs:** use verified native channels for ephemeral coordination; use parent summaries or `_workspace/` records when durability or peer messaging is absent.
- **Model selection:** map semantic policies to available Antigravity tiers/settings and inherit by default.
- **Unavailable capabilities:** classify the status, lower conservatively, and expose blockers, missing branches, and unresolved conflicts.
