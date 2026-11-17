# Skill Testing and Iteration

Check the result or observable behavior the skill is intended to improve. Use existing validators for format, paths, and deterministic outputs. For judgment-heavy work, compare against concrete acceptance criteria and cite the evidence behind failures.

## Choose scenarios

Start with a realistic positive request. Add a near miss when the discovery boundary might overlap another skill, and a failure case when a shortcut could break correctness. For delegation changes, cover a direct task, independent read-heavy work, overlapping writes or shared mutable resources, and a missing or conflicting branch. Check that the workflow has one synthesis owner and preserves uncertainty when coverage is incomplete.

## Compare only when it answers a question

For a new skill, compare with direct execution. For a revision, compare with the previous version. Keep the task, inputs, runtime, permissions, model, and acceptance criteria fixed within each pair. Grade correctness first, then check reference reads, artifacts created, and coordination overhead. Report token use or timings only when the runtime exposes comparable telemetry. A word or byte count measures static prompt size.

Keep comparison runs separate from the canonical skill. Repeat unstable or consequential cases and use more than one target model when portability is the claim. For a small edit, a focused check often suffices. Add durable eval files or reviewer roles when results need to be repeated, audited, or consumed by automation. Reuse existing schemas and runners.
