---
name: harness
description: Design portable, repo-local agent harnesses with reusable skills, team specs, and deterministic handoff artifacts.
---

# Harness

Harness is a meta-skill for designing portable, repo-local agent workflows. Use it to analyze a project, decide which guidance belongs in `AGENTS.md`, choose a collaboration pattern, generate reusable specialist skills, and define how those skills hand work off through markdown specs and deterministic files.

## When to Use

Use Harness when you need to:

- design a new domain-specific skill stack for a repository
- adapt an existing workflow into repo-local shared skills
- define reusable specialist roles, orchestration rules, and validation steps
- standardize artifact naming, handoff files, and review loops for complex work

Do not use Harness for one-off tasks that can be handled directly by a single existing skill without adding reusable structure.

## Required Inputs

Provide or discover the following before generating artifacts:

- domain or project goal
- primary workflow and expected final deliverables
- constraints, quality bars, and failure tolerance
- current repository context, if a codebase already exists
- any existing skills, role docs, or templates worth preserving

If information is missing, inspect the repository first and make the narrowest reasonable repo-local assumption.

## Generated Artifacts

Harness generates only the artifacts needed to make the workflow reusable:

- `AGENTS.md` for repo-wide coordination rules only when the target repository needs durable always-loaded guidance
- `.agents/skills/{domain}-orchestrator/SKILL.md` for reusable top-level orchestration
- `.agents/skills/{specialist}/SKILL.md` for reusable specialist behavior
- `.agents/skills/{specialist}/references/*` for progressive-disclosure details
- `.agents/skills/{specialist}/templates/*` for optional runtime templates that should ship with a skill but remain inactive until copied or adapted intentionally
- `docs/harness/{domain}/team-spec.md` for role topology, handoffs, and failure policy
- `docs/harness/{domain}/roles/{role}.md` only when a role needs a durable brief but not a full skill
- `_workspace/{phase}_{role}_{artifact}.md` for durable intermediate artifacts and review evidence when a handoff must be inspectable, resumable, or shared across agents
- `_workspace/experiments/{run}/results.tsv` when the harness includes an autonomous experiment loop

Default to the smallest reusable surface: often one skill, sometimes a skill plus a team spec. Add extra role briefs, runtime adapters, or handoff files only when they solve a durable coordination need.

## AGENTS.md Guidance

`AGENTS.md` is the highest-leverage repo guide because it is loaded into every session. Only create or revise it when the target repository needs durable repo-wide guidance.

- Keep it short, human-written, and limited to repo-wide `WHAT / WHY / HOW`.
- Include project purpose, canonical paths or boundaries, and exact build/test/verify commands when they are non-obvious.
- Use pointers to deeper repo-local docs instead of copying long directory listings or task-specific playbooks into the root file.
- Do not auto-generate large codebase overviews, style guides already enforced by tooling, or one-off instructions.
- Read `references/agents-md-guide.md` before writing or revising a repo `AGENTS.md`.

## Harness Design Rules

- Treat prompt engineering as one layer inside harness engineering, not a replacement for clear artifacts and role contracts.
- Prefer rippable seams. Keep model-specific retries, heuristics, and recovery rules isolated in removable sections or reference docs.
- Keep coordination shallow. If the harness only works through deep routing or clever runtime recovery, simplify the design before adding more logic.

## Portable Defaults

- Prefer repo-local skills first.
- Keep direct or single-agent work when one context can complete the task without losing important information.
- Delegate only when work units are independent, specialization or context isolation has clear value, and one owner can synthesize the results.
- Prefer delegated workers for read-heavy exploration, review, isolated tests, and summarization. For parallel writes or tests with shared mutable resources, require non-overlapping ownership or isolated environments.
- Keep delegation shallow. Recursive fan-out is exceptional and must have an explicit depth, concurrency, and synthesis policy.
- Use file-based handoffs when work must be inspectable, resumable, audited, or consumed across agent boundaries. Allow concise in-thread summaries for ephemeral, low-risk coordination.
- Do not require model pins, SDK runtimes, or MCP orchestration unless the repository already depends on them.
- Keep model-specific retries and recovery logic easy to rip out as models improve.
- Require YAML frontmatter in every generated `SKILL.md`. Include at least `name` and `description` before the markdown body so native skill discovery can reliably find repo-specific generated skills.
- Keep names deterministic and repository-friendly.

## 6-Phase Workflow

### Phase 1: Domain Analysis

1. Inspect the repository, request, and existing docs.
2. Identify the domain, core task types, expected outputs, and quality bar.
3. Note reusable existing materials, current runtime assumptions, and any existing repo-wide guidance that already belongs in `AGENTS.md`.
4. Detect whether the workflow is best expressed as direct work, one reusable skill, role briefs, an orchestrator, delegated workers, or an autonomous experiment loop on user-controlled compute.
5. If the request is an autonomous experiment workflow, define the mutable surface, immutable evaluation surface, baseline requirement, and metric before generating artifacts.
6. Capture the result in a concise domain summary before generating new artifacts.

Output:

- domain summary
- task inventory
- reuse notes for any existing material

### Phase 2: Team Architecture Design

1. Choose the smallest architecture that can cover the workflow.
2. Apply the delegation decision gate: identify independent work units, context pressure, specialization value, overlapping files or mutable resources, permission needs, and the final synthesis owner.
3. Select one of the six patterns from `references/agent-design-patterns.md`.
4. For autonomous experiment loops, choose the matching workflow profile from `references/autonomous-experimentation.md` and decide whether it composes with Pipeline, Supervisor, or Producer-Reviewer.
5. Define how information moves between phases through final outputs, concise summaries, or `_workspace/` files. Persist only handoffs that need inspection, resumability, auditability, or cross-agent consumption.
6. Decide which recovery or model-specific logic must stay removable as the harness evolves.

Output:

- chosen architecture pattern
- role list
- handoff plan
- artifact naming convention

### Phase 3: Role and Artifact Definition Generation

1. Define each stable role as one of:
   - reusable specialist skill
   - reusable orchestrator skill
   - role-spec markdown under `docs/harness/{domain}/roles/`
2. Write explicit responsibilities, inputs, outputs, review edges, and failure policy.
3. Keep role boundaries aligned with specialization, parallelism, context pressure, and reuse.
4. Avoid creating separate files for roles that are too narrow or single-use.
5. Keep portable specialist behavior in skills, narrow durable responsibility in role briefs, reusable coordination in orchestrators, and runtime-specific execution settings in removable adapters.

Output:

- role inventory
- file layout for skills and team specs
- per-role input and output contract

### Phase 4: Skill Generation

1. Generate each reusable skill under `.agents/skills/`.
2. Start every generated `SKILL.md` with YAML frontmatter containing at least `name` and `description`, then the markdown heading and body.
3. Keep the main `SKILL.md` lean and move bulky detail or evolving heuristics into `references/`.
4. Include `When to use`, `Required inputs`, workflow steps, expected outputs, and validation notes.
5. Bundle deterministic helper scripts only when they remove repeated manual setup or repeated validation work.

Output:

- specialist skills
- optional orchestrator skill
- progressive-disclosure references

### Phase 5: Integration and Orchestration

1. Define the reusable end-to-end workflow in an orchestrator skill or team spec.
2. Specify phase order, handoff files, ownership, fallback rules, and which recovery logic is stable versus removable.
3. Reserve worker delegation for clearly parallel slices such as broad research, multi-surface review, isolated tests, log analysis, or independent generation branches.
4. For parallel writes or stateful tests, assign non-overlapping files and resources or use isolated environments; never rely on later synthesis to repair uncontrolled interference.
5. For autonomous experiment loops, preserve the run ledger, baseline artifact, and keep/discard policy under `_workspace/experiments/{run}/`.
6. Preserve intermediate artifacts in `_workspace/` when they provide debugging, handoff, or audit value; otherwise return a bounded summary to the coordinator.

Output:

- orchestrator skill or team spec
- `_workspace/` contract
- failure and retry policy

### Phase 6: Validation and Testing

1. Verify structure, paths, and internal references.
2. Run scenario tests for normal flow and at least one failure flow.
3. For autonomous experiment loops, validate the baseline run, immutable evaluation surface, results ledger, and crash/timeout reporting path.
4. Compare a specialized-skill run against a no-specialized-skill or manual baseline when useful.
5. Refine instructions when tests show ambiguity, overfitting, unnecessary weight, or stale heuristics that should be ripped out.

Output:

- validation checklist
- test scenarios
- follow-up fixes or simplifications

## Architecture Selection

Use the smallest pattern that preserves quality and clarity.

| Pattern | Best for | Default portable style |
| --- | --- | --- |
| Pipeline | sequential dependent work | sequential orchestrator skill plus `_workspace/` handoffs |
| Fan-out/Fan-in | parallel independent work with later synthesis | orchestrator skill plus bounded parallel workers and a final synthesis step |
| Expert Pool | selective routing to a subset of specialists | routing section in team spec plus reusable specialist skills |
| Producer-Reviewer | generation followed by explicit quality review | specialist producer skill, reviewer skill, and bounded revision loop |
| Supervisor | dynamic allocation across changing work units | top-level orchestrator or supervisor skill with explicit reassignment rules |
| Hierarchical Delegation | naturally layered decomposition | shallow hierarchy with a top-level orchestrator and one downstream coordination layer |

Short summaries:

- Pipeline: each phase depends on the previous artifact.
- Fan-out/Fan-in: several specialists work independently before synthesis.
- Expert Pool: only the relevant specialists are invoked for a given request.
- Producer-Reviewer: output quality is enforced by a paired review step.
- Supervisor: one coordinator manages a changing backlog and redistributes work.
- Hierarchical Delegation: a top-level goal breaks into sub-goals that may themselves be coordinated.

Read `references/agent-design-patterns.md` before finalizing the pattern.

## Workflow Profiles

Harness also supports reusable workflow profiles that compose with the six architecture patterns.

### Autonomous Experimentation

- This is not a seventh architecture pattern.
- Use it when the request explicitly calls for iterative experiments on user-controlled compute with a narrow mutable surface and a fixed evaluation surface.
- Pair it with Pipeline for a simple baseline -> mutate -> evaluate -> decide loop.
- Pair it with Supervisor when the experiment backlog changes during execution.
- Read `references/autonomous-experimentation.md` before finalizing the loop contract.

## Validation Expectations

Every generated harness should meet these checks:

- paths are real and internally consistent
- specialist skills and team specs agree on artifact names
- each phase has at least one named output
- reviewer or QA steps are explicit when quality risk is high
- `When to use` and `Required inputs` sections are concrete enough to prevent overlap
- generated skills start with YAML frontmatter that includes at least `name` and `description`
- `_workspace/` handoffs are deterministic and preserved for inspection
- any repo `AGENTS.md` stays short, repo-wide, and pointer-heavy
- model-specific recovery logic is isolated enough to remove without rewriting the whole harness
- no platform-specific runtime assumptions are required unless the repository already depends on them
- delegated work names its ownership boundary, synthesis owner, and partial-failure behavior
- parallel write and stateful-test workflows use non-overlapping ownership or isolated environments

## Reference Pointers

- `references/agents-md-guide.md` for writing short, durable repo-level `AGENTS.md` files
- `references/agent-design-patterns.md` for pattern choice and coordination styles
- `references/autonomous-experimentation.md` for iterative experiment loops on user-controlled compute
- `references/orchestrator-template.md` for a reusable orchestrator-spec template
- `references/team-examples.md` for example artifact trees and handoff patterns
- `references/skill-writing-guide.md` for authoring specialist skills
- `references/skill-testing-guide.md` for validation and iteration loops
- `references/qa-agent-guide.md` for cross-boundary QA methodology
- `references/codex-agent-adapter.md` for an optional, removable mapping to current Codex subagents and custom agents
