# Orchestrator Template

Use an orchestrator skill when the workflow needs a reusable entry point, or a team spec when the workflow mainly needs a durable coordination contract. Keep the workflow authoritative in one place and link to it from the other entry point if both exist.

```markdown
# {Workflow}

State the outcome, material inputs, and acceptance criteria.

## Execution

Describe dependencies and decisions that affect the result. Name each stable
responsibility and link any reusable skill. Use one owner for synthesis and
final acceptance.

If delegating, state when it pays off, who owns writes and mutable resources,
and what access or isolation is required. Run conflicting work sequentially
when those boundaries cannot be enforced safely.

## Durable handoffs

Include this section only for results that must survive the current run or
be independently consumed. For each, give the producer, consumer, path or
record key, expected contents, and completion state.

## Failure and acceptance

State which failures permit direct or sequential fallback and what must be
reported as partial or blocked. Check that the final result meets the original
criteria and identifies any missing evidence.
```

Omit sections that have no effect on this workflow. Use the deliverable itself for a handoff when its format and location already serve the consumer. Keep runtime-specific settings in optional profiles.
