# Autonomous Experimentation Workflow

Harness can support autonomous experimentation when the user explicitly wants an iterative loop that runs on computers they control. This workflow is inspired by the operational shape of [karpathy/autoresearch](https://github.com/karpathy/autoresearch), generalized into a reusable repo-local contract.

## When To Use

- the task is an explicit experiment loop, not a one-shot implementation request
- the mutable surface is narrow enough to edit and review repeatedly
- the evaluation surface can stay immutable during the run
- success can be measured with a declared metric, score, or pass/fail comparison rule
- the experiments run on user-controlled compute, whether local or another explicitly trusted execution surface

## When Not To Use

- the evaluation surface is still changing during the same loop
- the mutable surface is so broad that reverting failed ideas becomes unclear
- there is no declared metric or comparison rule
- a crash, timeout, or partial failure would have production-side effects
- the execution environment is remote or shared in a way the user cannot audit

## Core Contract

Every autonomous experiment harness should define these items up front:

- mutable surface: the files, parameters, prompts, or scripts each candidate may change
- immutable evaluation surface: the code, data, rubric, or benchmark that stays read-only for the run
- baseline run: one measured run before any mutation
- comparison rule: fixed budget, fixed dataset, fixed prompt set, or another explicit comparison contract
- experiment ledger: `_workspace/experiments/{run}/results.tsv`
- keep/discard policy: the rule for advancing a change, reverting it, or retrying it
- failure policy: bounded retry count, timeout rule, and crash handling

Treat the immutable evaluation surface as read-only for the duration of the run. If the evaluation surface must change, start a new run with a new baseline.

## Minimum Artifact Set

```text
_workspace/
└── experiments/
    └── {run}/
        ├── request-summary.md
        ├── baseline.md
        ├── results.tsv
        ├── candidate-{id}.md
        ├── eval-{id}.md
        └── final-summary.md
```

Use the smallest artifact set that still makes the loop auditable. If the domain needs extra per-run files, keep them under the same `{run}` directory.

## Default `results.tsv` Shape

If the domain does not already define a stronger schema, use:

```text
candidate_id	metric_value	runtime_seconds	status	summary
```

Status values should stay deterministic:

- `keep`: the candidate improved or met the declared advancement rule
- `discard`: the candidate ran but did not justify advancing
- `crash`: the candidate failed before producing a valid result
- `timeout`: the candidate exceeded the declared budget

Log the baseline as the first row before any mutated candidate rows.

## Recommended Loop

1. Snapshot the request, constraints, mutable surface, immutable evaluation surface, and metric in `request-summary.md`.
2. Run the baseline with no mutations and record it in `baseline.md` and `results.tsv`.
3. Propose one bounded candidate change at a time.
4. Run the candidate under the declared budget or comparison rule.
5. Record the result in `results.tsv` immediately after the run.
6. Keep or discard the candidate according to the declared policy.
7. Write `final-summary.md` with the best retained candidate, key failures, and open follow-ups.

## Failure Policy

- Retry only when the failure is clearly mechanical and the candidate intent is still sound.
- Cap retries at a small number, usually one or two attempts per candidate.
- Treat timeouts as first-class results, not silent noise.
- Record crashes and timeouts in `results.tsv` instead of dropping them from history.

## Pattern Pairings

Autonomous experimentation is not a seventh architecture pattern.

- Pair it with Pipeline when the loop is baseline -> mutate -> evaluate -> decide.
- Pair it with Supervisor when there is a changing backlog of candidate ideas or branching experiment queues.
- Pair it with Producer-Reviewer when a reviewer must explicitly approve a candidate before it becomes the new baseline.
