# Harness Output Specs

Generated harness-specific team specs and role briefs belong under `docs/harness/{domain}/`.

Repo-level version history for the meta-harness project lives in [CHANGELOG.md](../../CHANGELOG.md).

Start from the [orchestrator template](../../.agents/skills/harness/references/orchestrator-template.md) when you need a durable phase-and-handoff spec. Use the [AGENTS Authoring Guide](../../.agents/skills/harness/references/agents-md-guide.md) when the target repository needs short always-loaded repo guidance. See the [starter research example](starter-research/README.md) for a minimal concrete package that includes a team spec, one role brief, and `_workspace/` artifact mapping.

## Role and Handoff Contract

- The Lead is the orchestrator for the whole workflow. It owns the goal, context, source authority, current scope, active constraints, work contracts, subAgent prompts, output contracts, synthesis, validation, and final decision state.
- Delegated implementers should receive disjoint write sets and a bounded output contract. They should not expand scope, re-plan the workflow, or browse broadly unless the Lead explicitly asks for that work.
- The Lead should not directly edit or write implementation deliverables when a bounded implementer can be spawned; direct writes belong only to explicit user authorization, non-delegable emergency unblockers, or final synthesis and handoff artifacts owned by the Lead.
- When the Lead uses one of those exceptions, record the reason in `_workspace/` so the next turn can see why the boundary was crossed.
- Researchers may use web, search, or scrapling only when current external information or multi-source evidence is actually needed for the task.
- Reviewers and red-team roles should read the original request, the produced artifact, and the acceptance criteria, then write a deterministic report.
- Preserve the Lead thread or top-level handoff file with enough detail to prevent context loss: objective, scope, source authority, active constraints, assigned subAgent ids and roles, output paths, test results, blocked conditions, and the final decision state.
- Use `_workspace/` markdown files for each phase, and keep the content deterministic so another agent can pick up the work without guessing.

## Approval-First Harness Planning

Use this contract when the user invokes `$harness`, asks for subAgents, or asks the Lead to design a multi-agent workflow before execution.

- Start in planning mode. Do not spawn subAgents, mutate target deliverables, or start implementation until the user approves the final plan for execution.
- Treat the first response as a reviewable work contract, not as a loose proposal. The user should be able to challenge assumptions, reorder waves, add roles, narrow file ownership, or strengthen prompts turn by turn.
- Keep the Lead responsible for orchestration only unless the user explicitly authorizes direct implementation, the Lead is writing final synthesis/handoff artifacts, or an emergency unblocker is documented in `_workspace/`.
- Prefer compact handoffs over full-history forks. If a subAgent needs context, pass the exact source authority, paths, constraints, and output contract in the prompt.
- Preserve each approved plan or revision in `_workspace/` when the work will continue across sessions.

An approval-first plan should include these sections in this order. The stable labels are intentionally machine- and human-readable so later turns can revise a named section without regenerating the whole plan.

| Stable label | Purpose |
| --- | --- |
| `RequestMeaning` | Restate what the user is actually asking for, including durable intent and non-goals. |
| `SSoTSourceAuthority` | Name the read order, authoritative paths, external-source policy, and conflict rule. |
| `Assumptions` | Separate safe assumptions from questions that would change scope or risk. |
| `Architecture` | Select the smallest Harness pattern or pattern combination and explain why. |
| `FileOwnership` | Assign every writable path or artifact family to exactly one role; mark read-only surfaces. |
| `WavePlan` | Split work into sequential and parallel waves with dependencies, blockers, and synthesis points. |
| `SpawnPlan` | List every proposed subAgent, role type, fork-context choice, model rationale if any, and whether it is read-only or write-enabled. |
| `SpawnPrompts` | Provide the exact prompt drafts that will be sent after approval. |
| `TurnByTurnFeedback` | Name the checkpoints where the user can revise scope before execution continues. |
| `ValidationPlan` | Define structural checks, content checks, scenario tests, and cross-boundary QA. |
| `FinalReviewCriteria` | State the pass/fix/redo bar before any worker starts. |
| `ApprovalGate` | End with the exact condition required before spawning or mutation begins. |

## Spawn Prompt Contract

Every subAgent prompt should be specific enough that the worker can succeed without hidden context. Avoid short prompts like `analyze this` or `improve the docs` for serious harness work.

Include these fields unless a field is clearly irrelevant:

- Role identity: who the agent is acting as and what it owns.
- Objective: the exact outcome, not just an activity verb.
- Context snapshot: user intent, current phase, and why this role exists.
- Source authority: exact files, read order, official docs, or external-source constraints.
- Read scope: paths the agent may inspect and any paths it should avoid.
- Write scope: exact files or `_workspace/` artifacts the agent may change; use `read-only` when no edits are allowed.
- Coordination warning: say the agent is not alone in the codebase, must not revert others, and must stay inside the assigned scope.
- Tool permissions: whether web/search/scrapling/browser/test commands are allowed, and under what evidence rules.
- Forbidden overlaps: paths, decisions, or domains owned by another role.
- Task steps: ordered actions with expected intermediate observations.
- Output path: the exact artifact path to write or the exact final response shape when read-only.
- Output template: required headings, tables, JSON, TSV, or checklist format.
- Acceptance criteria: objective checks the Lead/reviewer will apply.
- Stop conditions: missing authority, conflicting sources, protected content, unsafe mutation, dependency on another unfinished wave, or scope drift.
- Final reporting format: changed files, commands run, unresolved blockers, confidence, and follow-up needs.

Prompt engineering rules for subAgent plans:

- Use verbs that match authority: `audit`, `map`, `draft`, `edit`, `validate`, or `review`, not vague `look at` language.
- Put source authority before tasks so workers do not optimize around convenience.
- For write-enabled workers, make the write set disjoint and include a reminder not to edit generated files directly.
- For reviewers, require comparison against the original request, produced artifacts, and acceptance criteria.
- For researchers, require citations or exact source paths and state whether current web verification is allowed.
- For future-facing architecture work, separate current implementation from extension contracts and runtime gaps.

## Turn-by-Turn Feedback Loop

Use this loop when a plan needs user refinement before execution:

1. Lead drafts the approval-first plan and labels it `Draft`.
2. User comments on assumptions, roles, prompt wording, write scopes, or final review criteria.
3. Lead replies with a revision summary: what changed, what stayed fixed, and any new risk.
4. Lead updates the proposed spawn prompts and wave plan without spawning agents.
5. Repeat until the user gives explicit final approval to execute.
6. After approval, Lead creates or updates the top-level `_workspace/` context pack, spawns only the approved agents, and tracks every agent id, role, write scope, and expected output.

During execution, Lead feedback should stay concise but state phase, active agents, completed artifacts, blockers, and next decision point. If a worker discovers a scope-changing issue, pause the affected wave and return to the user with a focused decision request.

## Context Engineering

- Keep the Lead context pack compact: only the facts needed for the current decision and next handoff.
- Prefer a compact handoff over a full-history fork when a specific model is required.
- Avoid pairing a full-history fork with explicit model overrides; that mixes too much history into a constrained execution path.
- If the task needs deeper background, add a small note in `_workspace/` and keep the thread focused on the current decision.

## Model Selection

- Use a cheap and fast model for deterministic implementation, docs, and test edits after the Lead has already decided the patch.
- Use a coding-optimized model for bounded code changes where the scope is narrow but still implementation-heavy.
- Use frontier, high, or xhigh only for broad research, multi-source synthesis, architecture ambiguity, governance or security review, or cross-runtime reasoning.
- `gpt-5.5 xhigh` belongs in the high-uncertainty bucket, not the default path.
- Do not hardcode one model for every task; choose from the task shape and the uncertainty level.

Typical generated files include:

- `docs/harness/{domain}/team-spec.md`
- `docs/harness/{domain}/roles/{role}.md`
- `_workspace/{phase}_{role}_{artifact}.md`

Generated `SKILL.md` files under `.agents/skills/` should start with YAML frontmatter containing at least `name` and `description`, followed by the markdown body.

Autonomous experiment workflows may additionally preserve deterministic run logs such as:

- `_workspace/experiments/{run}/results.tsv`
- `_workspace/experiments/{run}/baseline.md`
- `_workspace/experiments/{run}/final-summary.md`

Keep model-specific retries, shortcuts, and recovery heuristics in removable, rippable sections of the team spec or linked references instead of hard-wiring them into the core artifact contract.

This repository keeps `docs/harness/` as the canonical destination and now includes one docs-first starter example for reference without shipping example skills in the canonical source tree.
