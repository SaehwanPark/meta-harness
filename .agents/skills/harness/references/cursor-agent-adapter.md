# Cursor CLI / Agent Adapter

Use this adapter for Cursor CLI or Cursor Agent execution. This scope intentionally does not promise compatibility with every Cursor IDE extension or third-party integration. Portable skills and role contracts remain authoritative; `.cursor/agents/` profiles are optional, removable execution material.

Read [`runtime-capabilities.md`](runtime-capabilities.md) before lowering a role. Features can vary by CLI/Agent release, account, invocation mode, and workspace configuration.

## Capability mapping

- **Skills — `supported`** when discovery is enabled; otherwise **`advisory`**. Keep reusable skills in `.agents/skills/` and apply the relevant project instruction files. Do not fork a Cursor-specific skill mirror.
- **Roles and subagents — `supported_with_extension`** when native profiles/subagents are enabled; otherwise **`advisory`**. A stable role may use a `.cursor/agents/<role>.md` profile, while one-off work remains in the root Agent session.
- **Write isolation — `advisory`** unless an isolated worktree or copy is configured. Foreground/background execution and context isolation do not fence writes in one checkout; without isolation, use explicit non-overlap and serialize conflicts.
- **Communication — `advisory`** unless a native channel is verified and retained. For absent peer messaging, durable task state, clarification, or escalation, use a parent-mediated summary and deterministic `_workspace/` handoff.
- **Model policy — `supported` or `inherit`** where model selection is exposed: map `inherit`, `fast`, `economy`, `balanced`, and `strong` to available choices or tiers. Exact model names are optional overrides and must not be required by the portable workflow.

## Role lowering

For example, this portable role:

```yaml
role: test-investigator
reads: [src/**, tests/**]
writes: [tests/repro/**]
workspace:
  preference: isolated
skills: [test-analysis]
model_policy: balanced
communication:
  parent: required
completion:
  artifact: _workspace/test-investigator_result.md
```

may lower to a `.cursor/agents/test-investigator.md` profile that:

- references `.agents/skills/test-analysis/`;
- preserves `tests/repro/**` as the only write boundary;
- selects an isolated worktree/copy when the invocation supports one;
- returns evidence and the durable artifact to the named parent;
- does not delegate again unless the portable team specification explicitly allows it.

Keep hierarchy shallow (`root → worker` by default). A coordinator layer is exceptional and must have a stable synthesis output; runtime support for nested subagents is not itself justification for deeper trees.

## Fallback and failure behavior

If Cursor native agents, background execution, isolation, messaging, or model selection are unavailable:

1. execute the portable skill in the root session when the task is small or coupled;
2. keep independent read-heavy work separate only with an explicit synthesis owner;
3. isolate writes or assign non-overlapping files and serialize conflicts;
4. exchange durable outputs through `_workspace/` artifacts;
5. disclose unavailable capabilities and missing worker branches.

A failed launch, denied tool, workspace setup failure, communication loss, or crashed worker is a visible partial failure. Retry only under the declared workflow policy; never claim a required output exists when its branch failed.

## Adapter acceptance checklist

- **Skill discovery:** canonical `.agents/skills/` plus applicable project instructions; `.cursor/agents/` contains optional profiles, not canonical skills.
- **Role instantiation:** root Agent execution for simple work, or `.cursor/agents/` custom profiles/subagents when enabled.
- **Writes/isolation:** isolated worktree/copy preferred; otherwise explicit path ownership and serialization, since subagents alone do not fence a shared checkout.
- **Communication/handoffs:** use verified native channels for ephemeral coordination; parent summaries and `_workspace/` artifacts cover absent peer or durable messaging.
- **Model selection:** map semantic model policies to the available Cursor choices and inherit by default.
- **Unavailable capabilities:** classify and report the gap, then lower to isolation, explicit ownership, or serialization without silently weakening safety.
