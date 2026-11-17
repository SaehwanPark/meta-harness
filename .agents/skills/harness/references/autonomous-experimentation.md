# Autonomous Experimentation

Use this when the user requests an iterative experiment on authorized, user-controlled compute with a bounded mutable surface, an immutable evaluation surface, and a repeatable metric. Agree on the resource budget, stopping rule, and keep/discard criteria before editing. If the evaluator must change, start a new comparison with a new baseline.

1. Measure the original baseline before changing anything. Record the evaluator revision or inputs and comparison settings.
2. Change one bounded candidate at a time. Evaluate it under the same declared conditions, then keep it or restore the last accepted state.
3. Record each attempt in `_workspace/experiments/{run}/results.tsv`, with the baseline first. Preserve valid prior rows if execution stops partway.
4. Return the best retained state, outcome, and any limitations. Persist run setup or final summary separately when the ledger and repository history cannot carry them.

Default ledger columns, when the project has no established schema:

```text
candidate_id	metric_value	runtime_seconds	status	summary
```

Use `keep`, `discard`, `crash`, or `timeout` for candidate outcomes. Record crashes and timeouts even when there is no metric value. Retry only a recoverable mechanical failure within the declared budget. Prevent failed runs from mutating the evaluator or leaving unaccepted candidate changes in the retained state.
