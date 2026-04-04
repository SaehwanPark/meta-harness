# Skill Testing and Iteration Guide

Harness treats skill quality as an iterative engineering problem. Test the skill, compare it to a simpler baseline, keep the assertions honest, and simplify the skill when the extra structure is not buying you anything.

## 1. Testing Model

Use both qualitative and quantitative evaluation.

| Evaluation type | Method | Best for |
| --- | --- | --- |
| Qualitative | human review of usefulness, clarity, and structure | creative work, writing, design, strategic planning |
| Quantitative | assertion-based checks | file generation, extraction, transformation, deterministic reporting |

Core loop:

1. write or revise the skill
2. run scenario tests
3. evaluate results
4. generalize the lessons
5. rerun the same scenarios

## 2. Test Prompt Design

Write prompts that sound like real requests.

### Weak Prompts

```text
process this document
analyze the code
generate a report
```

### Better Prompts

```text
Audit this repository for API route documentation gaps. I need a markdown report
grouped by feature area, plus one example request and response for each route.
```

```text
Review the migration docs in this repo and tell me whether the new skill layout
still leaves any platform-specific runtime assumptions behind.
```

Cover at least:

- one core use case
- one edge case
- one request that is similar but should not need the skill

## 3. Specialized Skill vs Baseline

When useful, compare:

- a run that follows the specialized skill or orchestrator
- a baseline run that uses no specialized skill or uses a lighter manual approach

The point is not to prove that the skill always wins. The point is to learn whether the added structure improves quality, consistency, or speed enough to justify itself.

### Workspace Layout

```text
_workspace/
└── iteration-1/
    └── eval-0/
        ├── with_skill/
        │   └── outputs/
        └── baseline/
            └── outputs/
```

### Baseline Choices

| Situation | Baseline |
| --- | --- |
| new skill | solve the same task without the specialized skill |
| skill revision | solve the same task with the previous version |
| orchestrator revision | compare old workflow vs new workflow on the same cases |

## 4. Assertion-Based Evaluation

Good assertions:

- are objectively true or false
- test the skill's actual value
- reveal differences between approaches

Weak assertions:

- pass regardless of quality
- only test that some output exists
- depend on taste without a scoring rubric

### Example `grading.json`

```json
{
  "expectations": [
    {
      "text": "The report lists all six architecture patterns",
      "passed": true,
      "evidence": "Found all six pattern headings in the document"
    },
    {
      "text": "The README avoids canonical output paths under the legacy generated path",
      "passed": true,
      "evidence": "No canonical tree uses the legacy path"
    }
  ],
  "summary": {
    "passed": 2,
    "failed": 0,
    "total": 2,
    "pass_rate": 1.0
  }
}
```

## 5. Specialist Roles for Evaluation

Reusable review roles can improve evaluation quality.

### Grader

- checks assertions
- cites evidence
- flags weak or non-discriminating assertions

### Comparator

- compares outputs blindly when you want a less biased A/B judgment
- is most useful when two solutions are both plausible but structurally different

### Analyzer

- finds unstable cases, repeated failures, and high-cost low-value instructions
- helps decide whether the skill should be simplified or split

These roles can be implemented as specialist skills or lightweight worker briefs depending on how often they are reused.

## 6. Iteration Loop

Use this order:

1. revise the skill
2. rerun the same scenario set in a new iteration directory
3. compare quality, clarity, and cost
4. generalize the fix rather than patching for one example
5. stop when additional instructions no longer improve outcomes meaningfully

## 7. Selection-Boundary Validation

Portable skills should still be tested for boundary clarity.

Write two small query sets:

- should-use cases: requests where the skill clearly helps
- should-not-use cases: near misses that should stay with another skill or a direct workflow

Good near misses are adjacent requests, not unrelated ones. The goal is to make the skill boundary sharper.

## 8. Failure-Flow Testing

Every orchestrator should have at least one failure scenario:

- a missing input
- a partial branch failure
- conflicting findings during synthesis
- a reviewer asking for fixes that exceed the retry budget

Test that the harness degrades predictably and reports what was skipped or left uncertain.

## 9. When to Bundle Validation Scripts

Bundle a validation helper when:

- the same structure checks run on every iteration
- the output format is deterministic enough for automation
- the script reduces manual noise without hiding important judgment calls

Keep the script small. It should enforce invariants, not replace human review.
