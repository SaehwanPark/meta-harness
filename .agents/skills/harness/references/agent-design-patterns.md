# Harness Architecture Patterns

Harness supports six reusable architecture patterns. Choose the smallest pattern that preserves quality, keeps handoffs understandable, and produces durable artifacts that another engineer or agent can reuse later.

## Portable Coordination Styles

Before choosing a pattern, choose the coordination style that fits the work:

| Coordination style | Use when | Typical artifacts |
| --- | --- | --- |
| Single-agent workflow | one person or one skill can complete the job without durable specialist boundaries | one `SKILL.md`, one output contract |
| Sequential orchestration skill | work has clear phase dependencies | orchestrator `SKILL.md`, `_workspace/` handoffs |
| Parallel worker fan-out | several bounded slices can run independently and then be merged | orchestrator spec, specialist skills, synthesis step |
| Supervisor-led delegation | the backlog changes during execution and needs reassignment | team spec with routing and reassignment rules |
| Hierarchical delegation | the problem decomposes cleanly into a shallow tree of sub-goals | top-level orchestrator plus one subordinate coordination layer |

Decision guide:

- Start with single-agent unless role boundaries are clearly reusable.
- Upgrade to sequential orchestration when outputs from one phase become required inputs to the next.
- Upgrade to parallel worker fan-out only when the branches are genuinely independent.
- Upgrade to supervisor-led delegation when tasks cannot be fully assigned up front.
- Keep hierarchical delegation shallow. If the tree grows deeper than two coordination layers, flatten it.

## Rippable Harness Rule

- Keep the core workflow in durable artifacts and push model-specific retries or recovery heuristics into clearly removable sections or reference docs.
- Prefer shallow coordination. If a pattern needs many special cases or more than two coordination layers, simplify it before adding more harness logic.
- Explicit handoffs beat hidden runtime magic. Another engineer should be able to delete a recovery rule without losing the main workflow contract.

## 1. Pipeline

Sequential dependent work where each phase consumes the prior phase's artifact.

### When It Fits

- requirements, design, implementation, and validation happen in order
- downstream steps need a stable artifact from upstream steps
- the main risk is skipping or compressing a necessary phase

### When It Does Not Fit

- several phases can proceed independently
- late synthesis is more important than ordered handoffs
- one phase is acting as an overloaded dispatcher for unrelated tasks

### Minimum Generated Artifacts

- `.agents/skills/{domain}-orchestrator/SKILL.md` or `docs/harness/{domain}/team-spec.md`
- `_workspace/01_*`, `_workspace/02_*`, and later phase artifacts with deterministic names
- specialist skills only for phases that are reusable outside the current flow

### Recommended Portable Implementation Style

- use a sequential orchestrator skill
- define a file handoff for every phase boundary
- keep each phase artifact narrow enough that the next phase can read it quickly
- add a reviewer or QA phase only where a real quality gate exists

## 2. Fan-out/Fan-in

Parallel independent work followed by a synthesis step.

### When It Fits

- multiple specialists can work from the same input without stepping on each other
- cross-angle coverage matters more than ordered transformation
- the final output benefits from synthesis across several perspectives

### When It Does Not Fit

- branches depend on each other's intermediate findings
- the synthesis step would be forced to rebuild missing context from scratch
- branch ownership is too fuzzy to define deterministic outputs

### Minimum Generated Artifacts

- orchestrator skill or team spec with branch ownership
- one `_workspace/{phase}_{role}_{artifact}.md` per parallel branch
- one synthesis artifact or final report that cites the branch outputs

### Recommended Portable Implementation Style

- use bounded parallel workers only for clearly independent branches
- keep every branch on the same input snapshot
- define the synthesis criteria before work starts
- preserve all branch artifacts so disagreements can be traced later

## 3. Expert Pool

Selective routing to one or more relevant specialists from a larger set.

### When It Fits

- only a subset of specialists should run for any given request
- request classification is simpler than running every specialist every time
- the repository already has reusable specialist skills with distinct scopes

### When It Does Not Fit

- every request needs nearly every specialist
- routing criteria are vague enough that specialists will overlap heavily
- specialists are so narrow that the router becomes harder to maintain than the work itself

### Minimum Generated Artifacts

- routing rules in `docs/harness/{domain}/team-spec.md`
- reusable specialist skills under `.agents/skills/`
- optional decision table or request-to-skill matrix in `references/`

### Recommended Portable Implementation Style

- keep routing rules explicit and deterministic
- document which requests trigger which specialists
- add one fallback path for ambiguous requests instead of many partial routes
- review overlap regularly so the pool does not drift into duplicated skills

## 4. Producer-Reviewer

A generation phase followed by explicit quality review and bounded revision.

### When It Fits

- output quality matters enough to justify a separate review step
- review criteria can be stated clearly
- the review can either approve, request fixes, or request a limited redo

### When It Does Not Fit

- review criteria are so vague that the reviewer becomes a second producer
- the work is too small for a dedicated review loop
- the loop would run indefinitely because no acceptance threshold exists

### Minimum Generated Artifacts

- producer skill
- reviewer skill or QA brief
- review artifact in `_workspace/`
- bounded revision policy in the team spec

### Recommended Portable Implementation Style

- keep the review output structured: pass, fix, or redo
- cap revision loops at a small number of retries
- make the reviewer read both the produced artifact and the original request
- store review notes as durable artifacts, not transient comments

## 5. Supervisor

A coordinator manages a changing backlog and reallocates work as conditions change.

### When It Fits

- tasks appear dynamically during the workflow
- work units vary in size or complexity
- reassignment and prioritization are part of the design, not an exception

### When It Does Not Fit

- all tasks can be assigned cleanly up front
- the supervisor would only repeat a fixed checklist
- there is no durable backlog or task inventory to manage

### Minimum Generated Artifacts

- supervisor-oriented team spec
- task inventory or work queue artifact
- reassignment and escalation policy
- final integration or audit report

### Recommended Portable Implementation Style

- keep the supervisor logic in a top-level orchestrator or team spec
- define the task queue format in markdown or JSON
- assign work in chunks large enough to reduce churn
- require explicit status updates when tasks are reassigned or blocked

## 6. Hierarchical Delegation

A top-level goal breaks into sub-goals that may each need their own coordination.

### When It Fits

- the problem naturally separates into domains with their own local workflows
- one coordination layer is not enough to keep the work understandable
- each lower layer can produce a stable artifact for the layer above

### When It Does Not Fit

- the hierarchy would become deeper than two coordination layers
- lower layers are so small that they should be specialist skills instead
- the same information would be copied across too many levels

### Minimum Generated Artifacts

- top-level orchestrator skill or team spec
- subordinate coordination notes or role briefs
- clear parent-to-child and child-to-parent handoff artifacts

### Recommended Portable Implementation Style

- keep the hierarchy shallow
- let the top level own global goals and acceptance criteria
- let each subordinate layer own a bounded sub-domain
- flatten the design if reporting lines start to hide rather than clarify dependencies

## Combined Patterns

Real harnesses often blend patterns:

- Pipeline + Fan-out/Fan-in: sequential stages with a parallel middle phase
- Fan-out/Fan-in + Producer-Reviewer: parallel generation followed by review and synthesis
- Supervisor + Expert Pool: a coordinator selects specialists as new work arrives
- Hierarchical Delegation + Pipeline: a top-level split into domains, each with its own ordered workflow

When combining patterns, document the outermost pattern first, then note the local variation inside the relevant phase.

## Workflow Profile: Autonomous Experimentation

Autonomous experimentation is not a seventh architecture pattern. It is a workflow profile for requests that iterate on a narrow mutable surface against an immutable evaluation surface and declared metric.

Use it when:

- the user explicitly wants an iterative experiment loop
- the evaluation harness can stay read-only for the run
- every candidate can be logged and either kept or discarded

Recommended pairings:

- Pipeline for baseline -> mutate -> evaluate -> decide loops
- Supervisor for changing experiment backlogs or branching candidate queues
- Producer-Reviewer when a reviewer must explicitly approve advancing the best candidate

Minimum extra artifacts:

- `_workspace/experiments/{run}/request-summary.md`
- `_workspace/experiments/{run}/baseline.md`
- `_workspace/experiments/{run}/results.tsv`
- `_workspace/experiments/{run}/final-summary.md`

Core rules:

- declare the mutable surface before the first candidate
- keep the evaluation surface read-only for the run
- establish a measured baseline before mutation
- record every candidate outcome, including crashes and timeouts
- run on user-controlled compute unless the repository defines another trusted execution surface

## Artifact Shape Rules

Use these defaults when converting a pattern into files:

- reusable coordination logic becomes `.agents/skills/{domain}-orchestrator/SKILL.md`
- durable role topology becomes `docs/harness/{domain}/team-spec.md`
- reusable specialist behavior becomes `.agents/skills/{specialist}/SKILL.md`
- bulky domain detail moves into `.agents/skills/{specialist}/references/`
- model-specific recovery notes belong in linked references or clearly named removable sections
- intermediate work products live in `_workspace/` and keep deterministic names
- autonomous experiment ledgers live under `_workspace/experiments/{run}/`
