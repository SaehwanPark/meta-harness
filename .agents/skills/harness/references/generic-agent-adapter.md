# Generic Agent Skills Adapter

Use this fallback when a client can consume the portable Agent Skills
convention but has no validated Meta Harness runtime adapter. The generic mode is
best effort, not a first-class execution guarantee.

## Capability boundary

- **Skills — `advisory`**: install or point the client at `.agents/skills/` (or
  its documented equivalent) and verify that it discovers `SKILL.md` files
  with YAML frontmatter. Discovery behavior is client-defined.
- **Roles and workers — `unsupported` unless independently verified**: run the
  portable role in the root session. Do not infer subagents, recursion,
  background execution, or custom profiles from skill support alone.
- **Write isolation — `unsupported`**: keep mutable work in one owner, declare
  non-overlapping paths, or serialize it. Instructions are not a mechanical
  write fence.
- **Communication and durability — `unsupported`**: use parent-mediated
  summaries and deterministic `_workspace/` artifacts for anything that must
  survive a turn or be consumed by another worker.
- **Model and permissions — `inherit`/`advisory`**: use the client defaults;
  exact model, tool, shell, or network settings are not portable requirements.

## Safe lowering

Unavailable capabilities are explicit; unsupported worker, isolation, and
communication guarantees must not be inferred from skill discovery.

1. Preserve the canonical skill and runtime-neutral role contract.
2. Keep work single-agent unless the client independently proves a stronger
   capability.
3. For independent read-heavy work, use separate contexts only with an
   explicit synthesis owner and inspectable outputs.
4. For mutable work, isolate it, declare exclusive/non-overlapping ownership,
   or serialize conflicting steps.
5. Report missing capabilities rather than silently weakening a correctness
   guarantee.

## Rippability

Generic mode creates no native runtime profile and does not duplicate the
portable skill. A client-specific integration can be added later as a
removable adapter without changing the canonical workflow.

## Acceptance checklist

Before claiming compatibility, verify skill discovery, instruction-file scope,
role execution, write behavior, handoff durability, model selection, and failure
handling in the target client. Until evidence exists, classify each capability
as advisory or unsupported and use the safe fallback above.
