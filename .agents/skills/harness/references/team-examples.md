# Team Examples

These examples show portable artifact trees and handoff patterns. They are intentionally compact: the goal is to demonstrate how a harness should be laid out in a repository, not to prescribe one exact runtime.

## Example 1: Deep Research Team

### Pattern

- Fan-out/Fan-in
- bounded parallel workers

### Good Fit

- one request needs several independent research angles
- the final deliverable is a synthesized report

### Generated Artifacts

```text
AGENTS.md
.agents/skills/research-orchestrator/SKILL.md
.agents/skills/official-research/SKILL.md
.agents/skills/media-research/SKILL.md
.agents/skills/community-research/SKILL.md
.agents/skills/background-research/SKILL.md
docs/harness/deep-research/team-spec.md
_workspace/
├── 00_input/request-summary.md
├── 01_official_findings.md
├── 01_media_findings.md
├── 01_community_findings.md
├── 01_background_findings.md
└── final/report.md
```

### Handoff Pattern

- the orchestrator snapshots the request in `_workspace/00_input/request-summary.md`
- each specialist writes one findings file with cited evidence
- the synthesis phase reads all branch outputs and writes one merged report

### Notes

- use parallel workers only for the four independent research branches
- keep synthesis in one owner to avoid conflicting merged reports

## Example 2: Full-Stack Product Build

### Pattern

- Supervisor
- shallow Hierarchical Delegation

### Good Fit

- the backlog changes during implementation
- frontend and backend each have their own local workflows

### Generated Artifacts

```text
AGENTS.md
.agents/skills/product-build-orchestrator/SKILL.md
.agents/skills/frontend-builder/SKILL.md
.agents/skills/backend-builder/SKILL.md
.agents/skills/qa-review/SKILL.md
docs/harness/product-build/team-spec.md
docs/harness/product-build/roles/frontend-lead.md
docs/harness/product-build/roles/backend-lead.md
_workspace/
├── 00_input/spec-summary.md
├── task-queue.md
├── 01_frontend_plan.md
├── 01_backend_plan.md
├── 02_frontend_status.md
├── 02_backend_status.md
├── 03_qa_report.md
└── final/release-summary.md
```

### Handoff Pattern

- the supervisor owns `task-queue.md`
- frontend and backend leads write bounded plans and status artifacts
- QA reads both implementation surfaces and writes one integration report

### Notes

- keep the hierarchy at two levels: supervisor plus domain leads
- flatten further if sub-domain briefs become too thin to justify separate files

## Example 3: Comprehensive Code Review

### Pattern

- Fan-out/Fan-in
- Producer-Reviewer for final synthesis

### Good Fit

- architecture, security, performance, and testing can be reviewed independently
- a final reviewer should normalize and prioritize findings

### Generated Artifacts

```text
AGENTS.md
.agents/skills/review-orchestrator/SKILL.md
.agents/skills/security-review/SKILL.md
.agents/skills/performance-review/SKILL.md
.agents/skills/architecture-review/SKILL.md
.agents/skills/test-review/SKILL.md
.agents/skills/findings-editor/SKILL.md
docs/harness/code-review/team-spec.md
_workspace/
├── 00_input/review-scope.md
├── 01_security_findings.md
├── 01_performance_findings.md
├── 01_architecture_findings.md
├── 01_test_findings.md
├── 02_synthesized_findings.md
└── final/review-report.md
```

### Handoff Pattern

- each reviewer owns one findings file
- the findings editor merges duplicates, adds severity ordering, and flags open questions
- the final report cites the contributing findings files for traceability

### Notes

- keep individual reviewers read-focused unless the review plan explicitly includes fixes
- make the synthesis artifact distinct from the final report so prioritization logic stays inspectable

## Example 4: Editorial Production Pipeline

### Pattern

- Pipeline
- Producer-Reviewer

### Good Fit

- concept, outline, draft, review, and revision happen in sequence
- quality improves when editorial review is explicit and bounded

### Generated Artifacts

```text
AGENTS.md
.agents/skills/editorial-orchestrator/SKILL.md
.agents/skills/story-concept/SKILL.md
.agents/skills/outline-writer/SKILL.md
.agents/skills/draft-writer/SKILL.md
.agents/skills/editorial-review/SKILL.md
docs/harness/editorial/team-spec.md
_workspace/
├── 00_input/brief.md
├── 01_concept.md
├── 02_outline.md
├── 03_draft.md
├── 04_review.md
└── final/final-draft.md
```

### Handoff Pattern

- each phase reads the previous artifact and writes exactly one next-step artifact
- the reviewer writes pass, fix, or redo guidance
- revision is capped at a small number of loops

## Artifact Pattern Summary

Use these defaults when translating a design into files:

- reusable domain logic becomes a specialist skill under `.agents/skills/`
- reusable coordination becomes an orchestrator skill or a team spec
- temporary but inspectable artifacts live in `_workspace/`
- durable role rules that are too narrow for a skill live under `docs/harness/{domain}/roles/`

## Example 5: Autonomous Experiment Loop

### Pattern

- Pipeline
- Supervisor only when the experiment backlog changes during the run

### Good Fit

- the user explicitly wants autonomous iterative experiments on local or otherwise user-controlled compute
- one narrow mutable surface is evaluated against a stable, read-only benchmark or rubric

### Generated Artifacts

```text
AGENTS.md
.agents/skills/experiment-orchestrator/SKILL.md
.agents/skills/candidate-editor/SKILL.md
.agents/skills/evaluator/SKILL.md
docs/harness/autonomous-experiment/team-spec.md
_workspace/
├── 00_input/request-summary.md
└── experiments/
    └── {run}/
        ├── baseline.md
        ├── results.tsv
        ├── candidate-01.md
        ├── eval-01.md
        └── final-summary.md
```

### Handoff Pattern

- the orchestrator defines the mutable surface, immutable evaluation surface, metric, and timeout policy before the first run
- the baseline is recorded before any candidate edit is attempted
- each candidate writes one proposal artifact and one evaluation artifact
- the ledger in `results.tsv` records `keep`, `discard`, `crash`, and `timeout` outcomes

### Notes

- keep the mutable surface narrow enough that a discard can cleanly revert to the previous best state
- do not let the evaluation harness drift during the run
- keep the loop on user-controlled compute unless the repository defines another trusted execution surface
