Below is a handoff-ready implementation plan that treats this as a coherent next-generation `meta-harness` architecture rather than a set of compatibility patches.

# Meta Harness: Multi-Runtime Architecture and Installer Modernization Plan

## 1. Purpose

Evolve `meta-harness` into a portable, capability-aware harness designer for modern coding agents while preserving its strongest existing design principle:

> Define reusable workflow semantics once, then adapt them to the capabilities of each supported runtime.

The project should actively support four coding-agent environments:

1. **Pi**
2. **OpenAI Codex**
3. **Google Antigravity**
4. **Cursor CLI / Agent**

Other coding agents should remain usable through the portable Agent Skills layer on a best-effort basis, but should not receive the same compatibility guarantees unless they become actively tested targets.

The installer should support both:

* deterministic CLI operation;
* an interactive checkbox/radio-based TUI.

Both interfaces must drive the same internal planning and execution engine.

---

# 2. Product Positioning

## 2.1 Canonical project statement

Recommended positioning:

> Meta Harness designs portable coding-agent workflows using Agent Skills, runtime-neutral role contracts, deterministic handoffs, and capability-aware execution adapters.
>
> Pi, Codex, Antigravity, and Cursor CLI/Agent are actively supported and tested execution targets. Other compatible coding agents may consume the portable skill layer on a best-effort basis.

Avoid broad claims such as:

* "supports all coding agents";
* "works with Aider/OpenHands/Droid/etc.";
* "universal compatibility".

Portability and validated support should be treated as separate concepts.

## 2.2 Compatibility policy

Adopt three explicit tiers.

### Tier 1: First-class / actively supported

* Pi
* Codex
* Antigravity
* Cursor CLI / Agent

Requirements:

* explicit installer target;
* runtime adapter documentation;
* automated validation where practical;
* release-gate smoke tests;
* manually exercised workflows periodically;
* regressions considered project bugs.

### Tier 2: Portable / best effort

Any implementation compatible with the Agent Skills conventions or able to consume `.agents/skills/`.

Guarantees:

* canonical skill is structurally portable;
* no runtime-specific orchestration guarantee;
* no assumption about subagents, messaging, worktrees, permissions, model routing, or context behavior;
* no release-blocking compatibility promise.

### Tier 3: Community / unverified

Named third-party runtimes may be documented when useful, but:

* clearly marked unverified;
* no dedicated installer target unless actively maintained;
* community PRs welcome;
* compatibility claims must be evidence-backed.

## 2.3 Guiding maxim

> Support is earned by validation, not inferred from theoretical compatibility.

---

# 3. Core Architecture

## 3.1 Target architecture

```text
                         meta-harness
                              │
             ┌────────────────┴────────────────┐
             │                                 │
       Portable semantics               Portable Agent Skills
             │                            .agents/skills/
             │
   ┌─────────┼───────────┬──────────────────┐
   │         │           │                  │
workflow   roles      coordination       validation
           contracts     contracts          rules
   │         │           │                  │
   └─────────┴───────────┴─────────┬────────┘
                                   │
                         capability lowering
                                   │
            ┌──────────┬───────────┼───────────┐
            │          │           │           │
           Pi        Codex    Antigravity    Cursor
            │          │           │           │
      runtime adapter / execution profile materialization
```

## 3.2 Important separation of concerns

Formalize three concepts that are currently partially implicit.

### Skill

Defines **how domain work is performed**.

Examples:

* security review methodology;
* benchmarking procedure;
* literature review workflow;
* QA methodology.

Canonical location:

```text
.agents/skills/<skill-name>/SKILL.md
```

Skills should remain runtime-portable.

### Role

Defines **what a worker owns and must accomplish**.

Examples:

* security-reviewer;
* implementation-worker;
* integration-owner;
* experiment-auditor.

A role includes:

* responsibility;
* expected inputs;
* expected outputs;
* quality bar;
* owned resources;
* allowed communication;
* escalation;
* required skills.

Role semantics are runtime-neutral.

### Runtime execution profile

Defines **how a role is instantiated on a specific coding agent**.

Examples:

* Codex custom agent;
* Antigravity custom agent;
* Cursor `.cursor/agents/*.md`;
* Pi `agent_spawn(...)` configuration.

Runtime profiles may include:

* tool permissions;
* model selection;
* reasoning/thinking settings;
* workspace mode;
* subagent permissions;
* runtime-specific recovery behavior.

These profiles must remain removable and regenerable.

---

# 4. Runtime Capability Model

## 4.1 Motivation

Current compatibility is too path-oriented.

Future harness generation should reason about actual capabilities such as:

* can this runtime spawn workers?
* can workers communicate?
* can writes be isolated?
* are permissions enforceable?
* can models be selected per worker?
* can task state survive asynchronous execution?

Introduce a formal runtime capability abstraction.

## 4.2 Proposed capability vocabulary

Create:

```text
.agents/skills/harness/references/runtime-capabilities.md
```

Possible capability fields:

```yaml
skills:
  portable_agent_skills: true
  progressive_disclosure: true

agents:
  spawn: true
  custom_agents: true
  recursive_spawn: false
  asynchronous: true
  background_execution: true

communication:
  parent_child_message: true
  peer_message: false
  durable_message: false
  request_reply: false
  escalation: false

tasks:
  task_board: false
  durable_task_state: false
  dependencies: false

workspace:
  shared_workspace: true
  isolated_workspace: true
  worktree: true

resources:
  advisory_ownership: true
  enforced_ownership: false
  read_write_borrowing: false
  write_fencing: false

models:
  per_agent_model: true
  provider_selection: false
  reasoning_selection: true
  inheritance: true

permissions:
  tool_restriction: true
  shell_restriction: true
  write_restriction: true
  permission_bubbling: false

lifecycle:
  cancellation: true
  status: true
  resume: false
  crash_recovery: false

observability:
  agent_tree: true
  task_status: false
  messages: false
```

Exact schema can evolve, but capability names should be semantic rather than tied to product APIs.

## 4.3 Graceful degradation hierarchy

Harness designs should define semantic requirements and allow adapters to lower them.

Example: parallel mutable work.

Preferred lowering:

```text
mechanical resource enforcement
        ↓ unavailable
isolated worktrees / workspace copies
        ↓ unavailable
non-overlapping explicit file ownership
        ↓ unavailable
serialized execution
```

Example: worker collaboration.

```text
durable typed peer messaging
        ↓
native direct messaging
        ↓
parent-mediated summaries
        ↓
_workspace handoff artifact
```

The harness must never silently assume that a weaker runtime provides a stronger guarantee.

## 4.4 Capability status

Adapters should distinguish:

* `supported`
* `supported_with_extension`
* `advisory`
* `unsupported`

This is especially useful for Pi:

```text
Pi base
  spawn: extension-dependent

Pi + pi-safe-agent-team
  spawn: supported
  peer messaging: supported
  task board: supported
  mechanical ownership: supported
```

---

# 5. Runtime Adapters

Create a dedicated adapter for each actively supported runtime.

Recommended files:

```text
.agents/skills/harness/references/
  runtime-capabilities.md
  pi-agent-adapter.md
  codex-agent-adapter.md
  antigravity-agent-adapter.md
  cursor-agent-adapter.md
```

The existing Codex adapter can be refactored rather than rewritten from zero.

---

# 6. Pi Support

## 6.1 Canonical skill placement

Do not create an unnecessary Pi-specific skill mirror.

Pi can consume:

```text
.agents/skills/
```

Therefore:

* canonical skill remains source of truth;
* Pi-specific behavior belongs in the adapter;
* global user-level installation may use whichever shared Agent Skills path is appropriate.

## 6.2 Base Pi support

Document:

* Agent Skills discovery;
* `AGENTS.md` behavior;
* project trust implications;
* extensions;
* context/compaction behavior;
* model/provider flexibility;
* limitations of bare Pi regarding agent teams.

## 6.3 Enhanced Pi backend

Treat `pi-safe-agent-team` as an optional first-party-quality integration, not as part of the portable contract.

Capability mapping should include:

* recursive child agents;
* parent/peer communication;
* clarification;
* escalation;
* durable mailbox;
* task board;
* hierarchical resource ownership;
* shared/mutable borrowing;
* write fencing;
* root write guard;
* isolated/shared workspace modes;
* explicit model/provider/thinking routing;
* capability restrictions;
* lifecycle tracking;
* durable journal and recovery.

## 6.4 Pi role lowering

Portable role:

```yaml
role: reviewer
writes: []
may_spawn: false
may_message:
  - parent
  - implementer
workspace: shared-readonly
model_policy: strong
```

Possible Pi lowering:

```text
agent_spawn(
  role="reviewer",
  mayWriteRepo=false,
  maySpawn=false,
  mayMessagePeers=true,
  workspace="shared",
  provider=...,
  model=...,
  thinking=...
)
```

## 6.5 Pi-specific fallback

If `pi-safe-agent-team` is unavailable:

* use portable skill in root session;
* avoid pretending mechanical ownership exists;
* serialize conflicting tasks;
* use `_workspace/` handoffs where necessary.

---

# 7. Codex Support

## 7.1 Preserve existing adapter philosophy

Keep:

* canonical portable skill;
* optional native agent definitions;
* inherited model defaults unless pinning is justified;
* shallow delegation;
* isolated write ownership.

## 7.2 Refactor Codex adapter around capability model

Instead of describing Codex as an isolated special case, map Codex onto the same runtime capabilities as the other three.

Document:

* custom-agent capabilities;
* built-in subagents;
* tool/permission handling;
* model and reasoning routing;
* workspace/write behavior;
* limitations around communication and persistence;
* partial failure handling.

## 7.3 Native profile generation

Optional:

```text
.codex/agents/
```

should be treated as generated runtime material, not canonical domain behavior.

---

# 8. Antigravity Support

## 8.1 First-class adapter

Add:

```text
antigravity-agent-adapter.md
```

## 8.2 Map relevant capabilities

Document and test, where feasible:

* `.agents/skills/`;
* custom agents;
* model selection;
* tool restrictions;
* subagent invocation;
* asynchronous/background execution;
* nested delegation;
* worktree or isolated workspace behavior;
* parent/child/peer messaging;
* permission bubbling;
* retained subagent context.

## 8.3 Guardrail

Do not equate supported recursion depth with recommended harness depth.

Meta Harness should retain:

* one downstream delegation layer by default;
* two coordination layers as an exceptional practical ceiling;
* flattening when coordination begins obscuring dependencies.

---

# 9. Cursor CLI / Agent Support

## 9.1 Scope

Explicitly support:

* Cursor CLI;
* Cursor Agent.

Do not frame this as support for the broader Cursor IDE-extension ecosystem.

## 9.2 Adapter

Add:

```text
cursor-agent-adapter.md
```

Document:

* Agent Skills;
* `.cursor/agents/`;
* subagents;
* background/foreground execution;
* model selection;
* context isolation;
* worktree or isolated copy behavior;
* applicable instruction files;
* custom agent configuration.

## 9.3 Role lowering

Portable role:

```yaml
role: test-investigator
writes:
  - tests/**
workspace: isolated
model_policy: balanced
skills:
  - test-analysis
```

Cursor lowering may produce:

```text
.cursor/agents/test-investigator.md
```

while leaving the actual test methodology in:

```text
.agents/skills/test-analysis/
```

---

# 10. Semantic Model Policy

## 10.1 Problem

Runtime model controls differ:

* Pi can select provider/model/thinking;
* Codex exposes its own model/reasoning settings;
* Antigravity may use runtime-specific model tiers;
* Cursor has its own model choices.

Portable roles should not depend primarily on exact model IDs.

## 10.2 Add semantic policies

Initial portable vocabulary:

```text
inherit
fast
economy
balanced
strong
```

Optional additional requirements:

```yaml
model_policy: strong

requirements:
  reasoning: high
  tool_use: required
  context: large
```

Adapters translate these semantics as well as possible.

## 10.3 Explicit override

Allow adapter-specific overrides only when justified:

```yaml
runtime_overrides:
  pi:
    provider: openai
    model: ...
    thinking: high
```

Portable harness logic must still function when these overrides are removed.

---

# 11. Richer Role Contract

## 11.1 Proposed role fields

Every meaningful delegated role should be able to specify:

```yaml
role: implementation-worker

responsibility:
  ...

inputs:
  ...

outputs:
  ...

skills:
  - implementation-guidelines

quality_bar:
  ...

resources:
  reads:
    - src/**
  writes:
    - src/parser/**
  external_mutable:
    - test-db

workspace:
  preference: isolated

communication:
  parent: orchestrator
  peers:
    - reviewer
  clarification_target: orchestrator
  escalation_target: orchestrator

permissions:
  shell: true
  write_repo: true
  spawn: false

model_policy:
  balanced

completion:
  artifact: _workspace/03_implementation-worker_result.md
  acceptance:
    - tests pass
```

Not every generated role must use every field.

## 11.2 Mechanical versus advisory semantics

The role contract should distinguish:

```yaml
ownership:
  requirement: exclusive
  enforcement: runtime
```

Possible adapter outcomes:

```text
Pi + safe-agent-team:
  broker-enforced

Cursor isolated worktree:
  workspace-enforced

basic runtime:
  advisory + serialized
```

---

# 12. Coordination and Handoff Semantics

## 12.1 Introduce three handoff classes

### Ephemeral coordination

For:

* status;
* short clarification;
* quick discovery;
* bounded peer communication.

Preferred runtime transport if available.

### Durable coordination record

For:

* task assignment;
* decision requests;
* blocking conditions;
* acceptance state;
* resumable orchestration.

May map to:

* Pi task/message broker;
* runtime-native agent state;
* `_workspace/` fallback.

### Durable artifact

For:

* implementation plans;
* review evidence;
* experiment ledgers;
* integration reports;
* outputs needed across sessions.

Use deterministic files.

## 12.2 Principle

> Do not persist everything merely because persistence is available.

Use durable storage when it provides:

* auditability;
* resumability;
* debugging;
* cross-agent consumption;
* later synthesis.

---

# 13. Restore Phase 0: Inventory and Drift Audit

## 13.1 Why

The current six-phase workflow should gain a preceding audit step for existing projects.

New structure:

```text
Phase 0: Inventory & Drift Audit
Phase 1: Domain Analysis
Phase 2: Team Architecture
Phase 3: Role & Artifact Definition
Phase 4: Skill Generation
Phase 5: Integration & Orchestration
Phase 6: Validation & Testing
```

## 13.2 Phase 0 responsibilities

Inspect:

* existing `.agents/skills/`;
* existing `AGENTS.md`;
* runtime-specific agent definitions;
* existing harness documentation;
* stale adapters;
* duplicated skills;
* duplicated roles;
* outdated runtime configuration;
* deprecated install layouts;
* current runtime capabilities.

Classify operation:

```text
new harness
existing harness extension
runtime adapter update
drift repair
skill-only update
architecture refactor
maintenance/audit
```

## 13.3 Required output

Produce concise inventory:

```yaml
existing_skills:
  ...

existing_roles:
  ...

detected_runtimes:
  ...

stale_artifacts:
  ...

compatibility_risks:
  ...

recommended_action:
  ...
```

---

# 14. Installer Redesign

## 14.1 One program, two interaction modes

Support:

### CLI

For:

* scripts;
* CI;
* automated agents;
* reproducible setups;
* advanced users.

### TUI

For:

* discovery;
* checkbox selection;
* interactive installation;
* repair/audit;
* users who dislike dense CLI flags.

Both must produce the same internal `InstallRequest`.

---

# 15. CLI Design

## 15.1 Replace layout-centric UX

Move away from:

```text
--layout codex
--layout forgecode
--layout droid
...
```

toward:

```bash
meta-harness install --agent pi
meta-harness install --agent codex
meta-harness install --agent antigravity
meta-harness install --agent cursor
meta-harness install --agent generic
```

## 15.2 Multi-runtime selection

Allow multiple:

```bash
meta-harness install \
  --agent pi \
  --agent cursor \
  --agent codex
```

Repeatable `--agent` is preferable to a single comma-separated flag.

## 15.3 Suggested commands

```bash
meta-harness install
meta-harness audit
meta-harness doctor
meta-harness compile
meta-harness validate
```

Potential meanings:

### `install`

Install portable skill and selected adapters.

### `audit`

Inspect existing harness and runtime integration.

### `doctor`

Detect broken/missing dependencies, stale paths, capability mismatches.

### `compile`

Materialize runtime-specific execution profiles from portable role definitions.

### `validate`

Run portable and adapter-specific structural validation.

Do not implement all commands immediately if they create unnecessary scope.

---

# 16. Interactive Behavior

## 16.1 Default behavior

```bash
meta-harness install
```

If attached to a TTY:

* launch interactive installer.

If noninteractive:

* fail clearly if required values are missing.

Do not silently launch TUI in CI or piped shell environments.

## 16.2 Explicit mode controls

Possible:

```bash
meta-harness install --interactive
meta-harness install --non-interactive ...
```

---

# 17. TUI Design

## 17.1 Main screen

Example:

```text
Meta Harness Installer

Installation scope
  (•) Project
  ( ) User

Actively supported coding agents
  [x] Pi
  [ ] Codex
  [ ] Antigravity
  [x] Cursor CLI / Agent

Portable compatibility
  [ ] Generic Agent Skills only

Pi integration
  [x] Use pi-safe-agent-team when available

Native execution profiles
  [x] Generate runtime-native agent definitions

Install mode
  (•) Copy
  ( ) Symlink

Target
  /home/user/project

[ Continue ]   [ Dry Run ]   [ Cancel ]
```

## 17.2 Preview screen

Before mutation:

```text
Installation plan

CREATE  .agents/skills/harness/
CREATE  .cursor/agents/
KEEP    AGENTS.md
KEEP    README.md

Pi
  portable skill: enabled
  safe-agent integration: enabled

Cursor
  portable skill: enabled
  native profiles: enabled

No repository-owned documentation will be overwritten.

[ Install ]  [ Back ]  [ Cancel ]
```

## 17.3 Existing installation mode

If an installation already exists:

```text
Detected

✓ Meta Harness skill
✓ Pi
✓ Cursor
! Codex adapter outdated
! legacy ForgeCode mirror present

Recommended actions

[x] Refresh Codex adapter
[x] Remove deprecated ForgeCode mirror
[ ] Regenerate Cursor profiles

[ Apply ] [ Inspect ] [ Cancel ]
```

---

# 18. Installer Internal Architecture

## 18.1 Core principle

Do not implement CLI and TUI separately.

Target flow:

```text
CLI parser ──────────────┐
                        │
TUI selections ─────────┼──> InstallRequest
                        │
config file ────────────┘
                              │
                              v
                    capability resolver
                              │
                              v
                         InstallPlan
                              │
               ┌──────────────┼───────────────┐
               │              │               │
           CLI renderer   TUI renderer      executor
```

## 18.2 Suggested domain objects

Conceptually:

```python
InstallRequest
  scope
  target
  agents[]
  mode
  native_profiles
  optional_integrations
  force
  dry_run

RuntimeSelection
  name
  features[]

InstallOperation
  action
  source
  destination
  owner
  reason

InstallPlan
  operations[]
  warnings[]
  detected_conflicts[]
  post_install_notes[]
```

The language may change later, but the separation should remain.

## 18.3 Idempotency

Installer must be safe to rerun.

Operations should distinguish:

```text
CREATE
UPDATE
KEEP
SKIP
REMOVE
CONFLICT
```

Avoid deleting repository-owned files implicitly.

---

# 19. Runtime Detection

Where safe and deterministic, detect evidence such as:

```text
.agents/
.codex/
.cursor/
.pi/
AGENTS.md
runtime-specific config
installed Pi extension/package metadata
```

Detection must not automatically imply mutation.

Example:

```text
Detected Cursor configuration.

Would you like to enable the Cursor adapter?
```

Do not silently install adapters based solely on directory presence.

---

# 20. Legacy Compatibility

## 20.1 Current named layouts

Existing options such as:

* ForgeCode
* Droid
* OpenHands
* Aider

should be toned down.

Recommended transition:

### Short term

Keep old flags operational but mark deprecated.

Example:

```text
WARNING:
--layout forgecode is deprecated.
ForgeCode is no longer an actively tested target.
Using generic Agent Skills compatibility.
```

### Later

Remove from primary CLI help and README.

Possibly retain hidden compatibility aliases for another release.

## 20.2 Migration

`meta-harness audit` should detect legacy installation artifacts and offer:

```text
keep
migrate
remove
ignore
```

Never remove unknown user-managed runtime files automatically.

---

# 21. Skill Validation

## 21.1 Add portable validator

Create:

```text
scripts/validate_skills.py
```

Validate at least:

* valid YAML frontmatter;
* `name`;
* `description`;
* portable naming rules;
* expected directory/name relationship;
* description length;
* internal relative links;
* referenced files exist;
* referenced templates exist;
* no accidental runtime-specific assumptions in portable core;
* no broken reference paths.

## 21.2 Strict portable intersection

When runtimes differ in validation behavior, target the stricter portable subset where reasonable.

Goal:

> A generated Meta Harness skill should be structurally valid before any runtime sees it.

---

# 22. Runtime Adapter Validation

Add fixtures or tests for:

```text
tests/fixtures/pi/
tests/fixtures/codex/
tests/fixtures/antigravity/
tests/fixtures/cursor/
tests/fixtures/generic/
```

Validate:

* destination paths;
* generated profile structure;
* no portable/runtime source duplication;
* adapter links;
* expected capability mappings;
* degraded behavior when a capability is absent.

---

# 23. Release Gate

A release should not ship if one of the actively supported targets has a known structural regression.

Suggested CI stages:

```text
portable skill validation
installer tests
CLI parsing tests
TUI state/model tests
Pi adapter validation
Codex adapter validation
Antigravity adapter validation
Cursor adapter validation
documentation validation
Pages validation
legacy migration tests
```

Where live runtime execution is impractical in CI, use structural fixtures plus periodic manual verification.

---

# 24. Runtime Compatibility Documentation

Replace the current compatibility matrix with something closer to:

| Runtime            | Status      | Agent Skills             | Native agents  | Isolation                    | Communication                  | Model routing |
| ------------------ | ----------- | ------------------------ | -------------- | ---------------------------- | ------------------------------ | ------------- |
| Pi                 | First-class | Yes                      | Via extensions | Yes with appropriate backend | Rich with `pi-safe-agent-team` | Rich          |
| Codex              | First-class | Yes                      | Yes            | Runtime-dependent            | Runtime-dependent              | Yes           |
| Antigravity        | First-class | Yes                      | Yes            | Yes                          | Yes                            | Yes           |
| Cursor CLI / Agent | First-class | Yes                      | Yes            | Yes                          | Runtime-dependent              | Yes           |
| Generic            | Portable    | Implementation-dependent | No guarantee   | No guarantee                 | No guarantee                   | No guarantee  |

Avoid pretending all capabilities are equivalent.

---

# 25. Documentation Structure

Recommended:

```text
docs/
  architecture/
    portable-contract.md
    runtime-capabilities.md
    role-contract.md
    handoffs.md

  compatibility/
    README.md
    pi.md
    codex.md
    antigravity.md
    cursor.md
    generic.md

  installation/
    README.md
    cli.md
    tui.md
    migration.md

  guides/
    workflow.md
    patterns.md
    runtime-selection.md

  harness/
    ...
```

The skill's `references/` directory should contain only material needed by the agent at runtime.

Public/product documentation can be more expansive.

---

# 26. AGENTS.md Policy

Preserve the existing strong policy:

* short;
* repository-wide;
* pointer-heavy;
* human-readable;
* no generated encyclopedia;
* no runtime-specific clutter unless truly repo-wide.

Runtime adapters should not dump large instructions into root `AGENTS.md`.

---

# 27. Harness Generation Workflow

## Phase 0 — Inventory & Drift Audit

Determine:

* existing harness state;
* installed skills;
* existing runtime profiles;
* supported runtimes;
* stale compatibility artifacts;
* conflicts and duplication.

Output:

```text
inventory
drift report
operation classification
```

## Phase 1 — Domain Analysis

Determine:

* project purpose;
* workflows;
* constraints;
* quality bars;
* failure tolerance;
* existing reusable material.

## Phase 2 — Architecture Selection

Choose:

* direct work;
* one skill;
* sequential orchestration;
* fan-out/fan-in;
* producer-reviewer;
* expert pool;
* supervisor;
* shallow hierarchy.

Then determine required runtime capabilities.

## Phase 3 — Role & Artifact Contracts

Define:

* roles;
* responsibilities;
* input/output;
* ownership;
* communication;
* escalation;
* workspace requirements;
* model policy;
* handoff durability.

## Phase 4 — Skill Generation

Generate only reusable domain behavior.

Keep runtime details out.

## Phase 5 — Runtime Lowering & Orchestration

Map portable roles onto:

* Pi;
* Codex;
* Antigravity;
* Cursor;
* generic fallback.

Generate native profiles only when selected.

## Phase 6 — Validation

Test:

* portable structure;
* runtime compatibility;
* normal scenario;
* partial failure;
* conflicting writes;
* unavailable capability;
* worker failure;
* adapter removal.

---

# 28. Rippable Runtime Layer

Retain and strengthen the existing "rippable harness" principle.

A user should be able to delete:

```text
.cursor/agents/
.codex/agents/
runtime-specific adapter output
```

without destroying:

```text
.agents/skills/
docs/harness/
portable role semantics
_workspace contract
```

Runtime profiles are compiled artifacts or optional adapters, not the authoritative workflow.

---

# 29. Source-of-Truth Rules

Recommended precedence:

```text
1. Portable skill semantics
2. Portable team/role specification
3. Runtime capability definition
4. Runtime adapter mapping
5. Generated native profile
```

Never edit generated native profiles and then treat those edits as canonical unless intentionally promoted back into the portable role contract.

---

# 30. Configuration Design

A future optional repo-level configuration could look like:

```yaml
version: 1

runtimes:
  - pi
  - cursor

features:
  native_profiles: true

pi:
  safe_agent_team: auto

model_policy:
  default: inherit

handoffs:
  durable_directory: _workspace

validation:
  failure_scenario: true
```

Avoid introducing this file until configuration actually reduces duplication.

Do not create configuration merely for architectural elegance.

---

# 31. `pi-safe-agent-team` Integration Boundary

Meta Harness should not directly depend on its internal broker protocol.

Instead:

```text
Meta Harness semantic capability
        ↓
Pi adapter
        ↓
pi-safe-agent-team public tools
```

Examples:

```text
exclusive write ownership
  → agent_resource borrow mutable

durable clarification
  → agent_send clarification

task completion
  → agent_task complete

isolated worker
  → agent_spawn workspace=worktree
```

This prevents `meta-harness` from coupling itself to broker implementation details.

---

# 32. Failure Semantics

Every generated multi-agent harness should specify:

* worker spawn failure;
* unavailable model;
* unavailable tool;
* resource conflict;
* partial worker failure;
* synthesis with missing branches;
* communication failure;
* permission denial;
* workspace setup failure;
* runtime lacking requested capability.

Portable rule:

> Never silently weaken a correctness guarantee.

Example:

If exclusive write safety was required but unavailable:

```text
serialize workers
```

rather than:

```text
run them concurrently and hope instructions are followed
```

---

# 33. Observability

Where runtimes support it, expose:

* active workers;
* parent/child topology;
* current task;
* workspace;
* ownership;
* blocked state;
* outstanding clarifications;
* partial failures.

Portable harness outputs should still remain understandable without runtime-specific observability.

---

# 34. Context Management

Do not assume subagents are always beneficial.

Continue applying the delegation gate:

Delegate when there is concrete value from:

* specialization;
* context isolation;
* parallel latency;
* independent exploration.

Stay single-agent when:

* work is tightly coupled;
* write ownership cannot be isolated;
* communication overhead exceeds benefit;
* one context is sufficient.

Runtime richness must not become a justification for unnecessary team complexity.

---

# 35. Hierarchy Policy

Default:

```text
root
  └─ worker
```

Acceptable when justified:

```text
root
  └─ coordinator
      └─ worker
```

Avoid deeper structures even if the runtime technically permits them.

Require explicit justification for recursive delegation.

---

# 36. TUI Technology Decision

## Near term

Keep installer logic in Python.

Advantages:

* smallest migration risk;
* current script can evolve incrementally;
* focus first on architecture.

Possible lightweight TUI/dialog choices should be evaluated.

Avoid creating a heavy dependency merely for visual polish.

## Later

Consider Rust if the installer becomes a real product surface requiring:

* standalone binaries;
* fast startup;
* no Python dependency;
* richer TUI;
* cross-platform distribution;
* long-term maintainability.

Potential stack:

```text
clap
ratatui
crossterm
serde
```

Do not rewrite solely for novelty.

---

# 37. Implementation Phases

## Phase A — Compatibility Contract

* [ ] Define actively supported runtimes: Pi, Codex, Antigravity, Cursor.
* [ ] Define generic portable target.
* [ ] Tone down unsupported runtime claims.
* [ ] Rewrite compatibility policy.
* [ ] Add `runtime-capabilities.md`.
* [ ] Define capability status vocabulary.
* [ ] Define degradation hierarchy.

### Acceptance criteria

* Documentation clearly separates portability from active support.
* No unsupported runtime is presented equivalently to first-class targets.
* Capability vocabulary is runtime-neutral.

---

## Phase B — Runtime Adapters

* [ ] Refactor Codex adapter.
* [ ] Add Pi adapter.
* [ ] Document base Pi capabilities.
* [ ] Document optional `pi-safe-agent-team` capability enhancement.
* [ ] Add Antigravity adapter.
* [ ] Add Cursor CLI/Agent adapter.
* [ ] Add generic fallback adapter.
* [ ] Document capability differences.

### Acceptance criteria

Each adapter answers:

* how skills are discovered;
* how roles are instantiated;
* whether subagents exist;
* how writes are isolated;
* how communication works;
* how model selection works;
* how unsupported semantics degrade.

---

## Phase C — Portable Role Contract

* [ ] Formalize skill vs role vs runtime profile.
* [ ] Extend team-spec guidance.
* [ ] Add resource ownership declarations.
* [ ] Add workspace requirements.
* [ ] Add communication declarations.
* [ ] Add escalation rules.
* [ ] Add semantic model policy.
* [ ] Add runtime override escape hatch.
* [ ] Add durable/ephemeral handoff classification.

### Acceptance criteria

A role can be lowered onto all four first-class runtimes without embedding one runtime's terminology in the canonical role.

---

## Phase D — Phase 0 Audit

* [ ] Add Inventory & Drift Audit.
* [ ] Detect existing skills.
* [ ] Detect native runtime profiles.
* [ ] Detect stale adapters.
* [ ] Detect duplicate roles/skills.
* [ ] Classify new build vs extension vs migration vs repair.
* [ ] Define audit output contract.

### Acceptance criteria

Running Harness against an existing repo no longer assumes a blank slate.

---

## Phase E — Installer Core Refactor

* [ ] Separate argument parsing from filesystem mutation.
* [ ] Implement `InstallRequest`.
* [ ] Implement `InstallPlan`.
* [ ] Implement operations: CREATE/UPDATE/KEEP/SKIP/REMOVE/CONFLICT.
* [ ] Add repeatable `--agent`.
* [ ] Add `generic`.
* [ ] Add multi-runtime installs.
* [ ] Preserve `--dry-run`.
* [ ] Preserve copy/symlink support where appropriate.
* [ ] Make reruns idempotent.
* [ ] Keep repo-owned documentation untouched.

### Acceptance criteria

CLI and future TUI can operate through the same planner without duplicating install logic.

---

## Phase F — CLI Modernization

* [ ] Add `meta-harness install`.
* [ ] Support `--agent pi`.
* [ ] Support `--agent codex`.
* [ ] Support `--agent antigravity`.
* [ ] Support `--agent cursor`.
* [ ] Support `--agent generic`.
* [ ] Support repeated `--agent`.
* [ ] Define TTY/non-TTY behavior.
* [ ] Add deprecated compatibility path for legacy layouts.
* [ ] Improve errors and plan summaries.

### Acceptance criteria

Example:

```bash
meta-harness install \
  --scope project \
  --target . \
  --agent pi \
  --agent cursor
```

runs deterministically without interaction.

---

## Phase G — TUI

* [ ] Implement interactive frontend.
* [ ] Add scope radio selection.
* [ ] Add first-class runtime checkboxes.
* [ ] Add generic compatibility option.
* [ ] Add Pi safe-agent integration option.
* [ ] Add native profile option.
* [ ] Add copy/symlink selection if still exposed.
* [ ] Add target input.
* [ ] Add plan preview.
* [ ] Add dry-run path.
* [ ] Add conflict screen.
* [ ] Add repair/update mode.
* [ ] Ensure keyboard-only operation.
* [ ] Handle small terminals gracefully.
* [ ] Ensure non-TTY never attempts to render TUI.

### Acceptance criteria

The TUI and equivalent CLI invocation produce identical `InstallPlan` semantics.

---

## Phase H — Validation

* [ ] Add portable skill validator.
* [ ] Validate frontmatter.
* [ ] Validate names/descriptions.
* [ ] Validate bundled references.
* [ ] Validate internal links.
* [ ] Add Pi fixture tests.
* [ ] Add Codex fixture tests.
* [ ] Add Antigravity fixture tests.
* [ ] Add Cursor fixture tests.
* [ ] Add generic fixture.
* [ ] Add legacy migration tests.
* [ ] Add multi-runtime install tests.
* [ ] Add dry-run equality tests.
* [ ] Add idempotent reinstall tests.
* [ ] Add conflict tests.
* [ ] Add removal/rippability tests.

---

## Phase I — Documentation

* [ ] Rewrite README positioning.
* [ ] Replace broad compatibility matrix.
* [ ] Add four runtime guides.
* [ ] Add generic compatibility guide.
* [ ] Add CLI installation guide.
* [ ] Add TUI installation guide.
* [ ] Add architecture documentation.
* [ ] Document role contract.
* [ ] Document capability lowering.
* [ ] Document migration from legacy layouts.
* [ ] Document support policy.
* [ ] Update GitHub Pages.

---

# 38. Suggested Versioning

A reasonable sequence:

## v0.6 — Runtime model

Focus:

* four officially supported targets;
* capability contract;
* Pi/Codex/Antigravity/Cursor adapters;
* generic portability;
* Phase 0 audit;
* compatibility claim cleanup.

## v0.7 — Installer architecture

Focus:

* repeatable `--agent`;
* shared install planner;
* multi-runtime install;
* migration support;
* improved validation;
* legacy layout deprecation.

## v0.8 — TUI and native compilation

Focus:

* interactive installer;
* preview/repair;
* runtime-native profile generation;
* role → runtime lowering;
* semantic model policy.

Version boundaries may change depending on implementation size.

---

# 39. Explicit Non-Goals

Do not:

* support every coding agent;
* maintain runtime adapters not actively exercised;
* fork portable skills by runtime;
* turn runtime profiles into canonical workflow definitions;
* create deep recursive agent hierarchies;
* require multi-agent execution for simple tasks;
* require `pi-safe-agent-team` for Pi usage;
* make exact model IDs part of portable role semantics by default;
* silently weaken write-safety guarantees;
* overwrite repository-owned `AGENTS.md`;
* require users to understand native directory layouts to perform normal installs;
* build separate CLI and TUI install engines;
* rewrite the installer in Rust before the architecture warrants it.

---

# 40. Important Design Invariants

The implementation should preserve these invariants.

### Invariant 1

```text
.agents/skills/
```

remains the canonical reusable skill source.

### Invariant 2

Portable workflow semantics do not depend on one agent runtime.

### Invariant 3

Runtime-native files are adapters or generated artifacts.

### Invariant 4

No runtime receives a first-class support label without validation.

### Invariant 5

Multi-agent execution must earn its complexity.

### Invariant 6

Conflicting writes require:

```text
mechanical enforcement
OR isolation
OR explicit non-overlap
OR serialization
```

### Invariant 7

Model-specific heuristics remain removable.

### Invariant 8

CLI and TUI share one install planner.

### Invariant 9

Installer plans are inspectable before mutation.

### Invariant 10

Repository-owned documentation remains repository-owned.

---

# 41. Representative End-State UX

## New interactive user

```bash
meta-harness install
```

TUI opens.

User selects:

```text
[x] Pi
[x] Cursor
```

Installer previews:

```text
CREATE .agents/skills/harness/
ENABLE Pi adapter
ENABLE Cursor adapter
OPTIONAL .cursor/agents profiles

KEEP AGENTS.md
```

User confirms.

---

## Automation / coding agent

```bash
meta-harness install \
  --scope project \
  --target . \
  --agent pi \
  --agent codex \
  --non-interactive
```

Deterministic result.

---

## Generic client

```bash
meta-harness install \
  --agent generic
```

Output explains:

```text
Installed portable Agent Skills representation.

Runtime-specific discovery, orchestration, subagents,
permissions, and model routing have not been validated
for this client.
```

---

## Existing repository

```bash
meta-harness audit
```

Result:

```text
Portable skill: current

Detected runtimes:
  Pi       supported
  Cursor   supported

Legacy:
  ForgeCode mirror found
  OpenHands guidance found

Drift:
  Cursor native profile missing

Recommended:
  add Cursor adapter
  remove or retain legacy mirror explicitly
```

---

# 42. Definition of Done

This modernization is complete when:

1. Meta Harness clearly identifies Pi, Codex, Antigravity, and Cursor CLI/Agent as its only actively supported runtime targets.
2. Other clients are represented through an explicit generic/best-effort compatibility mode.
3. Portable skills remain canonical under `.agents/skills/`.
4. Skill, role, and runtime execution profile are formally separated.
5. Runtime capabilities are modeled semantically.
6. Harness designs degrade safely when a runtime lacks a capability.
7. Pi can optionally take advantage of `pi-safe-agent-team` without making it a portable dependency.
8. All four first-class runtimes have dedicated adapters.
9. Existing harnesses are audited before modification.
10. Multi-runtime installation is supported.
11. CLI and TUI share one planner.
12. TUI provides checkbox-based runtime selection and pre-install preview.
13. Legacy unsupported layouts are toned down or deprecated.
14. Portable skill validation runs in CI.
15. Adapter fixture validation covers all four supported runtimes.
16. Documentation accurately distinguishes active support from theoretical portability.
17. Runtime-specific artifacts can be deleted without destroying the portable harness.
18. No first-class compatibility claim exists without corresponding validation responsibility.

---

# 43. Core Implementation Principle

The most important architectural statement for contributors should be:

> **Meta Harness does not maintain four separate harnesses. It maintains one portable workflow model and four actively validated runtime adapters.**

Pi, Codex, Antigravity, and Cursor should become execution targets of the same semantics rather than sources of four competing design languages.

That should remain the governing rule as both coding agents and `meta-harness` evolve.

I’d use this as the canonical handoff document, then let the implementation agent derive a concrete `ROADMAP.md` and issue/PR breakdown from its phases rather than mixing low-level task tracking into the architecture document.
