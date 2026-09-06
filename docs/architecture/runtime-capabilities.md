---
title: Runtime Capabilities
description: Semantic capabilities, support statuses, and safe degradation rules for runtime adapters.
layout: default
---

# Runtime Capabilities

Compatibility is about guarantees, not just directory names. Adapters map a
portable role onto the capabilities a runtime actually exposes.

## Capability vocabulary

A runtime may expose any combination of:

- **skills** — Agent Skills discovery and progressive disclosure;
- **spawn** — creating a delegated worker;
- **isolation** — isolated worktree, copy, or read-only workspace;
- **ownership** — enforceable exclusive read/write boundaries;
- **communication** — parent, peer, clarification, and escalation channels;
- **durability** — task state, mailbox, journal, or resumable handoff;
- **model routing** — inherited or per-role provider/model/reasoning choices;
- **permissions** — tool, shell, network, and repository-write restrictions;
- **lifecycle** — status, cancellation, timeout, and recovery observability.

Use semantic requirements in portable roles. Do not bake a product API or an
exact model identifier into the portable workflow.

## Status vocabulary

| Status | Meaning |
| --- | --- |
| Supported | The runtime provides and the adapter documents the capability. |
| Supported with extension | An optional, removable integration provides it. |
| Advisory | The contract is communicated but enforcement is left to the runtime/user. |
| Unsupported | Do not rely on it; lower the workflow or stop. |

Capability status can differ by runtime configuration. A first-class runtime
can therefore still have unsupported individual features.

## Safe degradation

Lower requirements in this order:

```text
mechanical ownership
  -> isolated worktree or workspace copy
  -> explicit non-overlapping file ownership
  -> serialized execution
```

For communication:

```text
durable typed channel
  -> native parent/peer messaging
  -> parent-mediated summary
  -> _workspace handoff artifact
```

Never run conflicting mutable work concurrently merely because the runtime can
spawn workers. If a required guarantee cannot be preserved, explain the
limitation and serialize or stop.

## Capability profiles

See the [compatibility matrix](../compatibility/README.html) and the
[Pi](../compatibility/pi.html), [Codex](../compatibility/codex.html),
[Antigravity](../compatibility/antigravity.html), [Cursor](../compatibility/cursor.html),
and [generic](../compatibility/generic.html) guides for runtime-specific
lowering notes.
