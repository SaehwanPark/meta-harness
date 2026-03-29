# QA Specialist Guide

Use this guide when a harness needs a reusable QA skill or worker brief. The focus is not just "does each part exist?" but "do the parts agree at their boundaries?"

## 1. Common Failure Pattern: Boundary Mismatch

The most common integration failures happen where two correct-looking components disagree at the handoff.

| Boundary | Example mismatch | Why it slips through |
| --- | --- | --- |
| API response to UI hook | API returns `{ projects: [...] }`, UI expects an array directly | each side looks valid in isolation |
| API fields to type definitions | response uses `thumbnailUrl`, consumer expects `thumbnail_url` | a cast or loose typing hides the mismatch |
| page files to links | a page exists at `/dashboard/create`, but links point to `/create` | file structure and link values were never compared directly |
| status map to runtime updates | a transition is defined on paper but never performed in code | the checklist verified the map, not the execution |
| endpoint inventory to client usage | an API exists but nothing calls it | presence was checked, linkage was not |

## 2. Integration Coherence Verification

QA should compare both sides of a boundary at the same time.

### API Response vs Consumer Types

1. inspect the actual response shape
2. inspect the consuming hook, parser, or type definition
3. compare nesting, field names, nullability, and list vs object shape

### File Paths vs Links

1. map the real route or file structure
2. collect every link or navigation target
3. confirm that each target resolves to an actual path

### State Transition Map vs Runtime Updates

1. collect the allowed transitions
2. collect the real status updates in code
3. compare for missing, dead, or unauthorized transitions

### Producer Output vs Reviewer Expectations

1. read the original request
2. read the produced artifact
3. read the review criteria
4. confirm the reviewer is checking the actual acceptance bar, not an invented one

## 3. Design Principles for a QA Skill or Brief

### Read Both Sides

A QA pass that reads only one side of a boundary is incomplete by design.

### Prefer Cross-Checks Over Presence Checks

Presence checks answer "is there a thing?" QA should answer "does this thing match the thing that consumes it?"

### Run QA Incrementally

Run QA after meaningful module completion, not only at the very end. Early integration checks are cheaper to fix.

### Keep the Report Actionable

A useful QA report includes:

- the boundary being checked
- the specific mismatch
- the likely impact
- the smallest fix path

## 4. QA Checklist Template

```markdown
## Integration Coherence Checks

### API to Consumer
- [ ] response shape matches the consuming type or parser
- [ ] wrapped responses are unwrapped consistently
- [ ] field naming is consistent across layers
- [ ] optional values are handled consistently

### Routing
- [ ] every navigation target resolves to a real path
- [ ] generated links include the required path prefix
- [ ] dynamic segments are populated correctly

### State Flow
- [ ] allowed transitions are actually exercised
- [ ] runtime updates do not invent undocumented transitions
- [ ] intermediate states can reach a terminal state

### Data Flow
- [ ] storage fields, API fields, and UI fields line up
- [ ] null and undefined handling is consistent across layers
- [ ] review artifacts cite the source artifact they evaluated
```

## 5. QA Skill Brief Template

```markdown
# QA Inspector

## When to Use
- use this skill for cross-boundary verification after implementation or during staged integration

## Required Inputs
- the original spec or request
- the producer-side files
- the consumer-side files
- any acceptance criteria or review rubric

## Responsibilities
- compare both sides of each boundary
- report concrete mismatches with likely impact
- distinguish confirmed failures from unverified areas

## Outputs
- `_workspace/qa_report.md`
- optional targeted fix list when the repair path is obvious

## Validation
- cite the exact files or artifacts compared
- separate blocking issues from follow-up improvements
```

## 6. Real-World Lessons

These patterns came from real integration failures:

- correct-looking API responses that did not match client expectations
- valid pages that were unreachable because links used the wrong prefix
- state machines that looked complete in docs but were missing a runtime transition

The fix was not "review harder." The fix was to compare both sides of the boundary on purpose.
