# Harness Modernization Review

## Verdict

The modernization premise is supported with a narrow boundary: current agent capabilities justify stronger guidance for independent read-heavy exploration, review, isolated tests, and context isolation. They do not justify making multi-agent execution the default for small, tightly coupled, or overlapping-write work.

The strongest design is a portable delegation decision contract plus an optional Codex adapter. The current Codex manual documents first-class subagents, standalone custom-agent files, shallow default nesting, inherited permissions, and higher token cost for subagent workflows. It recommends read-heavy parallelism and caution for parallel writes: <https://learn.chatgpt.com/docs/agent-configuration/subagents>.

## Paired Evaluation

The baseline and proposed guidance were applied to identical read-only fixtures with the same rubric: correctness 35, coverage 20, delegation appropriateness 15, synthesis 10, write safety 10, and overhead 10. Hard gates prohibited overlapping writes, invented evidence, hidden partial failure, or missing synthesis ownership.

| Scenario | Baseline | Proposed | Result |
| --- | ---: | ---: | --- |
| small direct task | 98 | 100 | both stayed single-agent; proposed removed artifact ambiguity |
| read-heavy review | 95 | 100 | proposed made synthesis/failure policy explicit and reduced unnecessary handoffs |
| overlapping writes | 84 | 98 | proposed explicitly serialized or isolated shared mutable resources |
| partial failure and conflict | 86 | 99 | proposed required disclosure, preserved uncertainty, and prohibited invented coverage |

Both variants passed the safety gates when the baseline was interpreted carefully. The proposed guidance won all four comparisons, improved the targeted behavior in more than one case, and did not regress the should-not-delegate case.

## Implemented High-Confidence Recommendations

- Replace the absolute single-agent default with a capability-aware delegation gate while keeping small coherent tasks direct.
- Prefer bounded read-heavy delegation; require isolation for overlapping files, stateful tests, and other mutable resources.
- Keep synthesis ownership, partial failure, conflict handling, concurrency, and depth explicit.
- Distinguish skills, role briefs, orchestrators, and runtime-native custom agents.
- Require durable `_workspace/` handoffs only for auditability, resumption, conflicts, or cross-agent consumption.
- Add an inactive Codex custom-agent template and removable adapter without installing active agents or pinning models.
- Test topology changes with controlled current-versus-proposed scenarios and hard safety gates.
- Validate the new deployable payload structurally and byte-for-byte across installer layouts.

## Deferred or Rejected

- Rejected always-on or recursive delegation because coordination, context, and token costs remain material.
- Rejected active `.codex/agents/` installation, global concurrency values, and model/reasoning pins because they are target-repository policy.
- Rejected replacing skills with custom agents; they serve different portable workflow and runtime execution concerns.
- Retained `_workspace/` for durable evidence while removing it as mandatory ceremony for ephemeral coordination.
- Deferred a full repeated benchmark suite; these paired decision simulations establish design safety and clarity, not statistical performance claims.
