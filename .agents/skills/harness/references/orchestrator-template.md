# Orchestrator Spec Template

Use this template when a workflow is reusable enough to deserve a top-level orchestrator skill or a durable team spec. The orchestrator should describe phase order, handoffs, and validation, not hide critical workflow rules inside ad hoc prompts.

## Authoring Rules

- Define the goal before defining the roles.
- Name every phase output and handoff file.
- Prefer markdown specs and `_workspace/` artifacts over implied coordination.
- Add worker-delegation notes only where parallelism is clearly bounded.
- Keep failure policy explicit. A reusable orchestrator should say what happens when a phase fails, stalls, or returns conflicting results.
- Keep model-specific retries, shortcuts, and recovery heuristics in a clearly removable section instead of weaving them through the whole spec.

## Template

```markdown
# {Domain} Orchestrator

## Goal
Describe the end-to-end outcome and the boundary of responsibility.

## Inputs
- required repositories, documents, or user inputs
- assumptions allowed when information is missing

## Outputs
- final deliverables
- intermediate artifacts that must be preserved

## Roles
| Role | Responsibility | Reusable skill | Writes |
| --- | --- | --- | --- |
| {role-1} | {what this role owns} | `.agents/skills/{role-1}/SKILL.md` or `n/a` | `_workspace/01_{role-1}_{artifact}.md` |
| {role-2} | {what this role owns} | `.agents/skills/{role-2}/SKILL.md` or `n/a` | `_workspace/02_{role-2}_{artifact}.md` |

## Phase Order

### Phase 1: {name}
- input sources:
- actions:
- output files:
- completion criteria:

### Phase 2: {name}
- input sources:
- actions:
- output files:
- completion criteria:

### Phase 3: {name}
- input sources:
- actions:
- output files:
- completion criteria:

## Handoff Files
| From | To | File | Purpose |
| --- | --- | --- | --- |
| {role-1} | {role-2} | `_workspace/01_{role-1}_{artifact}.md` | {why this handoff exists} |

## Failure Policy
- retry policy:
- partial completion policy:
- conflict resolution policy:
- escalation trigger:

## Removable Model-Specific Logic
- temporary retries or recovery heuristics:
- optional shortcuts or guardrails:
- deletion trigger:

## Validation Checks
- structural checks:
- content checks:
- scenario tests:
- baseline comparison, if useful:

## Optional Worker Delegation Notes
- safe parallel slices:
- forbidden overlaps:
- synthesis owner:

## Test Scenarios
### Normal flow
- request:
- expected phase outputs:
- expected final output:

### Failure flow
- failure point:
- expected fallback behavior:
- expected reporting:
```

## Recommended `_workspace/` Layout

```text
_workspace/
├── 00_input/
│   └── request-summary.md
├── 01_{role}_{artifact}.md
├── 02_{role}_{artifact}.md
├── 03_review_{artifact}.md
└── final/
    └── {deliverable}.md
```

## Minimal Orchestrator Artifact Set

For most reusable harnesses, the minimum useful set is:

- one orchestrator skill or one durable team spec
- one named artifact per phase
- one failure policy section
- one validation section
- one normal-flow and one failure-flow scenario

If the flow is too small to justify that set, it probably should remain a single specialist skill instead of an orchestrator.
