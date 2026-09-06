# Runtime Capability Model

This reference is the contract between portable Harness semantics and runtime adapters. It describes **what a workflow needs**, not which product API happens to provide it. The portable skill and role contract remain authoritative; adapter files lower those requirements onto a selected runtime.

## Capability status

Adapters use one of four statuses for each capability:

- `supported`: the selected runtime provides the semantic guarantee directly in the supported configuration.
- `supported_with_extension`: the guarantee is available only after an optional, explicitly selected integration (for example a Pi extension).
- `advisory`: the runtime can express the intent, but enforcement or durability is not guaranteed. The adapter must state the risk and lower the workflow conservatively.
- `unsupported`: the runtime cannot provide the capability. Do not imply that instructions alone provide the missing guarantee.

A status is about a semantic guarantee, not merely the existence of a similarly named command. Version-, account-, or installation-dependent features should be `supported_with_extension` or `advisory` until validated.

## Portable vocabulary

The following names are intentionally runtime-neutral:

```yaml
skills:
  portable_agent_skills: true
  progressive_disclosure: true
agents:
  spawn: false
  custom_agents: false
  recursive_spawn: false
  asynchronous: false
  background_execution: false
communication:
  parent_child_message: false
  peer_message: false
  durable_message: false
  request_reply: false
  escalation: false
tasks:
  task_board: false
  durable_task_state: false
  dependencies: false
workspace:
  shared_workspace: true
  isolated_workspace: false
  worktree: false
resources:
  advisory_ownership: true
  enforced_ownership: false
  read_write_borrowing: false
  write_fencing: false
  root_write_guard: false
models:
  per_agent_model: false
  provider_selection: false
  reasoning_selection: false
  inheritance: true
permissions:
  tool_restriction: false
  shell_restriction: false
  write_restriction: false
  permission_bubbling: false
lifecycle:
  cancellation: false
  status: false
  resume: false
  crash_recovery: false
observability:
  agent_tree: false
  task_status: false
  messages: false
```

This is a vocabulary, not a requirement that every runtime expose every key. An adapter should report only evidence-backed values and should preserve `false`/`unsupported` when evidence is absent.

## Semantic model policy

Portable roles select a policy rather than an exact model identifier:

- `inherit`: use the invoking runtime's default.
- `fast`: prefer low-latency execution for bounded, low-risk work.
- `economy`: prefer the least expensive adequate option.
- `balanced`: ordinary implementation or investigation work.
- `strong`: reasoning-heavy review, synthesis, or safety-sensitive work.

Adapters may map a policy to a runtime tier or setting. An optional runtime override may name a provider, model, or reasoning mode, but removing that override must not invalidate the portable workflow.

## Capability lowering

A role declares semantic requirements (`writes`, `workspace`, `communication`, `model_policy`, and optionally `ownership`). The adapter resolves them in this order:

1. Use a runtime-enforced guarantee when available.
2. Use an isolated worktree or workspace copy when mechanical ownership is unavailable.
3. Use explicit, non-overlapping file ownership when isolation is unavailable.
4. Serialize conflicting work as the final safe fallback.

For communication, lower in this order:

1. durable typed messaging;
2. native direct messaging;
3. parent-mediated summaries;
4. a deterministic `_workspace/` handoff artifact.

If a role requires a stronger guarantee than the selected runtime can provide, report the mismatch and choose a safer lower form. Never silently run concurrent conflicting writes or claim that a prompt enforces ownership.

## Runtime profiles

The actively supported adapters use this capability vocabulary as follows. Exact values can vary by runtime version and selected integration; the adapter must call out those conditions.

| Runtime | Portable skills | Native role profiles | Isolation / ownership | Communication | Model policy |
| --- | --- | --- | --- | --- | --- |
| Pi base | `supported` | `supported_with_extension` (otherwise `advisory`) | `advisory` | `advisory` | `supported` |
| Pi + `pi-safe-agent-team` | `supported` | `supported_with_extension` | `supported` for broker-enforced resources | `supported` | `supported` |
| Codex | `supported` | `supported_with_extension` when native agents are enabled; otherwise `advisory` | `advisory` unless an isolated workspace is configured | `advisory` unless a native channel is verified | `supported` or `inherit` |
| Antigravity | `supported` when discovery is enabled; otherwise `advisory` | `supported_with_extension` when custom agents are enabled; otherwise `advisory` | `advisory` unless an isolated workspace is configured | `advisory` unless a retained channel is verified | `advisory` or `inherit` |
| Cursor CLI / Agent | `supported` | `supported_with_extension` when native profiles are enabled; otherwise `advisory` | `advisory` unless an isolated worktree/copy is configured | `advisory` unless a native channel is verified | `supported` or `inherit` |
| Generic Agent Skills consumer | `advisory` | `unsupported` | `unsupported` | `unsupported` | `inherit` |

The generic row is a portability fallback, not a first-class execution guarantee. Keep portable skills usable there, but use one root agent, explicit ownership, and serialized execution whenever a role would otherwise conflict.

## Handoff classes

- **Ephemeral coordination**: status, a short clarification, or a bounded summary. Use native messaging when available.
- **Durable coordination record**: assignments, decisions, blockers, or acceptance state needed to resume orchestration. Use a runtime broker when durable; otherwise use a deterministic `_workspace/` record.
- **Durable artifact**: plans, implementation results, review evidence, or outputs consumed by later phases. Always use a deterministic file when cross-session inspection or synthesis matters.

Do not persist every message merely because a runtime can; persist when it adds auditability, resumability, debugging, or cross-agent consumption.

## Adapter acceptance checklist

Every runtime adapter must answer, with a status and fallback where relevant:

1. How are portable skills discovered, and which instruction files are in scope?
2. How is a portable role instantiated, and are subagents/custom agents available?
3. How are writes and workspace isolation enforced, or safely serialized when they are not?
4. How do parent, peer, clarification, escalation, and durable handoffs work?
5. How is a semantic model policy selected or inherited?
6. What happens when a requested capability is unavailable?

A runtime adapter is incomplete if it answers only with a product path and omits the semantic guarantee or degradation behavior.
