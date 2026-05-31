# Proposals: Local One-Developer AIP Chatbot Studio-Style Control Plane

Review workspace: `/home/palantirkc/meta-harness/_workspace/palantir-mini-codex-review-2026-05-31`

Reviewed source authority: `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini`

This proposal is intentionally local and one-developer-scale. It proposes a repo-local AIP Chatbot Studio-style authoring, state, tool, eval, and runtime-adapter surface for `palantir-mini`. It does not claim Palantir Foundry SaaS parity, Foundry security parity, Workshop parity, official API parity, or Marketplace parity.

## Status And Boundary

- This synthesis did not use palantir-mini MCP tools, palantir-mini skills, palantir-mini routing, prompt/DTC gates, or palantir-mini workflow state.
- This review package is intended to be read together with the final red-team report and any subsequent bounded-fix reports; this turn only updates this final proposal and `20_synthesis/evidence-matrix.md` inside the meta-harness review workspace.
- The Lead hotfix is already present in source: Codex `PreToolUse` is intentionally absent from `hooks/codex-hooks.json`, and docs/tests say `PreToolUse`, `SessionStart`, and `UserPromptSubmit` are not mounted for Codex.
- That hotfix is source-complete, but not active-runtime-complete: the active Codex runtime still requires plugin reinstall/reload and Codex process restart before the active session observes hook, MCP, skill, or manifest changes.
- Source plan approval must never be treated as live Codex behavior until reinstall/restart smoke evidence proves the mounted hook manifest, MCP profile, and skill surface in the active runtime.
- Report 02's bottleneck findings remain important historical evidence: they explain why broad pre-tool hook enforcement blocked review work. Reports 07 and 09 plus current source files supersede it for the checked-in Codex hook mount state.

## Core Recommendation

Build a small local "Chatbot Studio core" inside the existing `lib/chatbot-studio/` family, then reduce palantir-mini's default runtime exposure around it.

The local analogue should be a deterministic authoring and review workbench, not a generic chatbot framework. It should let one developer declare a chatbot, bind retrieval context and application state, define tool/action surfaces, run debug sessions, inspect traces, attach evals, and publish a local version for CLI/API/app embedding. Protected actions must remain default-off and require external approval plus governance evidence. Runtime adapters for Claude, Codex, and Gemini should translate native protocol details into the neutral core without changing semantics.

The default user-facing surface should become `studio-core`: small, inspectable, and local filesystem/SQLite-friendly. Maintainer tools, mutation tools, research refresh, event-log maintenance, broad audits, and runtime parity diagnostics should be explicit opt-in profiles.

## A. Observed Code-Level Bottlenecks

1. MCP overexposure.

`bridge/mcp-server.ts` exposes 31 live public tools and forces all live tools into public/lifecycle public behavior. `managed-settings.d/50-palantir-mini.json` broadly allows those tools, while richer capability metadata in `lib/capability-registry/mcp-tool-capability.ts` is not visible in `tools/list`.

2. Hook fan-out and latency.

The Codex adapter can expand a single runtime event through `hooks/hooks.json`, broad matcher aliases, and sequential sync hook execution. Report 02 found long aggregate timeout budgets and broad failure behavior. The source hotfix removes Codex `PreToolUse`, but `PermissionRequest` still bridges to shared `PreToolUse` policy and must be narrowed.

3. Governance attached too broadly.

The strong safety pieces are valuable, especially `lib/governance/pre-mutation-governance-v2.ts`, `hooks/commit-edits-governance.ts`, and response-claim validation. The bottleneck is attachment: `hooks/commit-edits-precondition.ts` and `hooks/ontology-engineering-workflow-enforcement-gate.ts` can block read-only evidence gathering or meta-harness review artifacts when they should only gate protected mutation or governed workflow claims.

4. Runtime identity bleed.

Several shared paths default missing runtime identity to Claude or hardcode `claude-code`, including `lib/runtime/identity.ts`, model grading, prompt capture, event emitters, timing, skill suggestions, and DTC governance emission. Unknown runtime must be explicit, not silently promoted.

5. Prompt state cross-runtime lookup.

Prompt-front-door store/adapter paths can scan across runtime pointers and project/cwd/home candidates. That is useful migration behavior but unsafe as a permanent architecture. Runtime state must be namespaced by project, runtime, session, and prompt id.

6. Skill and agent surface pressure.

The Codex wrapper pattern is right, but the installed/source surface also contains the large canonical skill library. Active agent files are mostly recipes, not native Codex agents, and several are Claude-shaped or deprecated.

7. Runtime-specific policy mixed into shared files.

Claude managed settings, Codex plugin manifests, shared hook intent, runtime capability facts, and future Gemini concepts are mixed too closely. That makes it hard to prove what a specific runtime actually enforces.

## B. Deletion And Disablement Proposals

Deletion should come last. The first goal is exposure reduction.

MCP tools:

| Class | Proposal |
| --- | --- |
| Public core | Keep only `pm_semantic_intent_gate`, `pm_ontology_engineering_workflow`, `pm_intent_router`, `ontology_context_query`, `pm_pre_mutation_governance`, `compute_edits_dry_run`, and `ontology_schema_get` in `studio-core`. |
| Merge candidates | Fold `get_ontology`, `impact_query`, `pre_edit_impact`, `pm_substrate_query`, `pm_lead_brief`, and `research_context_select` behind context/governance projections after replacement MCP-first evidence exists. |
| Protected default-off | Keep `apply_edit_function`, `commit_edits`, `negotiate_sprint_contract`, and `research_library_refresh` disabled by default. Enable only behind explicit approval, dry-run/governance evidence, and an opt-in profile. |
| Dev-only | Move broad audits, rule queries, source-authority validation, runtime parity, managed-settings validation, grader dispatch, event rotation, and plugin self-check to `dev-full`. |
| Internal telemetry | Keep event append and log maintenance out of default LLM-facing palettes unless explicitly requested by a maintainer flow. |

Any change to the seven-tool `studio-core` default should preserve public-core status, read-only or compute-only effect, no external egress by default, profile metadata visible to clients, and replacement MCP-first evidence before raw context tools are hidden.

Hooks:

- Keep Codex `PreToolUse` unmounted until hotfix exit tests pass.
- Limit `PermissionRequest` to permission-specific protected-action policy instead of replaying all broad pre-tool policy.
- Add effect classes: read-only inspection, review-artifact write, protected source mutation, generated-file mutation, commit/PR/release mutation, and external egress.
- Add a match report per hook call: lifecycle event, native tool, candidate aliases, matched policies, sync/async split, summed sync timeout, block-capable hooks, and opt-out decision.
- Add read-only shell classification for `jq`, safe `node -e` summaries, `git diff` inspection, sourced opt-out prefixes, `sed`, `rg`, `find`, `test`, and `wc` when no write/network/mutation behavior is present.

Skills:

- Keep thin Codex wrappers as the export pattern.
- Shrink defaults to front-door/orchestration/continuity: `pm-semantic-intent-gate`, `pm-orchestrate`, `pm-verify`, `pm-recap`, `pm-mcp-reload`, and optionally `pm-ontology-engineering-lead`.
- Keep `pm-review` and `pm-ship` explicit release commands, not ambient defaults.
- Merge or docs-only `pm-intent-to-ontology` and `pm-dtc-fill` behind the semantic gate.
- Move audit/maintenance wrappers behind one dev-only audit entrypoint or explicit named use.
- Add a test that Codex discovery does not default-inject canonical `skills/` when `.codex-plugin/plugin.json` points to `codex-skills/`.

Agents:

- Treat `agents/*.md` as role recipes unless a runtime explicitly exports them.
- Archive or remove from active discovery: `pm-implementer`, `mc-implementer`, `kosmos-implementer`, and `home-implementer` after tombstone/reference tests.
- Keep `project-implementer` as the replacement pattern for project-scoped implementers.
- Convert Claude-shaped agents to Codex docs-only unless native Codex lifecycle/tool/output-contract smoke tests exist.

Governance/RBAC:

- Keep `pre-mutation-governance-v2`, generated-file denial, outside-root denial, protected-surface matching, semantic conflict denial, strict `commit_edits` governance, and response claim validation.
- Retire or isolate legacy `pre-mutation-governance.ts`.
- Merge needed `commit-edits-precondition.ts` logic into `commit-edits-governance.ts`, then remove the older commit branch.
- Fix `pm-pre-mutation-governance` schema/handler mismatch so `project` or `projectRoot` is schema-required.
- Split Claude managed settings from Codex plugin policy and future Gemini policy.

## C. Runtime Separation Proposal

Use one runtime-neutral core and separate active runtime adapters.

Target layout:

```text
plugins/palantir-mini/
  core/runtime/
    runtime-id.ts
    runtime-session-context.ts
    adapter-manifest.ts
    hook-intent.ts
    tool-capability.ts
    unsupported-capability.ts
    cache-authority.ts
    parity.ts
  runtime-adapters/
    claude/
    codex/
    gemini/
```

Neutral core owns semantic contracts: runtime ids, adapter manifests, hook intent, tool capability metadata, governance decision schemas, prompt-front-door schemas, cache/source authority, and parity rules. It must not import Claude CLI behavior, Codex hook response shapes, Gemini APIs, provider SDKs, runtime-home paths, or managed-settings files.

Codex adapter owns `.codex-plugin/plugin.json`, `.mcp.json`, `hooks/codex-hooks.json`, Codex hook adapter behavior, Codex skill wrappers, Codex reload docs, and Codex cache/install evidence. The current hotfix remains part of this adapter contract.

Claude adapter owns Claude managed settings, Claude hooks/settings/memory assumptions, Claude agent wrappers, and Claude CLI model grading. Claude managed settings must not define Codex or Gemini policy.

Gemini adapter must start as an explicit manifest with gap records. Until Gemini has install/config/tool/hook/model-grader evidence, Gemini support is `unsupported`, `manual`, or `needs_human_review`, not active parity.

Rules:

- Missing runtime identity returns `unknown` or `needs_runtime_selection`.
- Provider identity is metadata, not approval authority.
- Prompt state is isolated by project/runtime/session/prompt id.
- Cross-runtime prompt reads require explicit neutral handoff artifacts.
- Shared `events.jsonl` can remain neutral only if every event carries runtime id, adapter id, session id, and source authority.
- Runtime parity must compare neutral, Claude, Codex, and Gemini if active Gemini support is claimed.

## D. Target Local Chatbot Studio Architecture

Implement the first slice as data-only contracts and deterministic builders under `lib/chatbot-studio/`.

Proposed source layout:

```text
plugins/palantir-mini/
  lib/chatbot-studio/
    declaration.ts
    session-state.ts
    tool-surface.ts
    action-surface.ts
    eval-surface.ts
    validators.ts
    index.ts
  schemas/chatbot-studio/
    declaration.schema.json
    session-state.schema.json
    tool-surface.schema.json
    eval-surface.schema.json
  tests/lib/chatbot-studio/
    declaration.test.ts
    session-state.test.ts
    tool-surface.test.ts
    eval-surface.test.ts
  eval-suites/
    chatbot-studio-local-regression.json
```

Core artifacts:

| Artifact | Purpose |
| --- | --- |
| `ChatbotStudioDeclaration` | Local declaration for name, API name, legacy names, instructions refs, ontology scope, retrieval bindings, application variables, tool bindings, eval suites, deployment stage, observability, and runtime projections. |
| `ChatbotStudioSessionState` | Local session ledger with session id, optional external session RID, runtime metadata, application snapshots, exchanges, trace refs, approval refs, and eval refs. |
| `ChatbotStudioExchange` | One user turn with user input, retrieval runs, tool plans, tool results, application updates, citations, optional markdown response, and trace refs. |
| `ApplicationVariable` and `ReasoningLoopSnapshot` | Deterministic visible/hidden variables, update policy, pinned reasoning-loop inputs, and no default model write authority. |
| `RetrievalContextBinding` and `RetrievalRun` | Ontology/document/function/local-source context, retrieved prompt, citations, source refs, warnings, and freshness/failure policy. |
| `ToolBinding` and `ToolInvocationPlan` | Official tool taxonomy mapped to local contracts: action, object query, function, update application variable, command, request clarification, and legacy semantic search as compatibility metadata. |
| `ActionSurface` | Mutating action intent, confirmation policy, DTC/approval requirements, dry-run requirement, and audit evidence refs. It does not execute commits. |
| `EvalSurface` | Local eval target, suite, test cases, criteria, metrics, variance checks, and trace refs. |
| `RuntimeProjection` | Per-runtime support, adapter refs, unsupported surfaces, fallback obligations, and smoke evidence refs. |

Storage should stay simple:

- Declarations: schema-versioned JSON files in a repo-local declaration directory.
- Sessions/traces: JSONL or SQLite tables, with stable ids and append-friendly records.
- Evals: JSON suite files plus local run records.
- Workbench state: deterministic projection from declaration, session, variables, retrieval, tool plans, approval status, eval status, and runtime gaps.

Execution boundary:

- The core creates declarations, plans, traces, validation issues, and eval surfaces.
- The core does not call LLM providers, execute MCP tools, edit files, commit ontology edits, drive browsers, or write runtime caches.
- Runtime adapters may execute read tools or approved protected actions only when the selected runtime, governance decision, and user approval all permit it.

## E. Staged PR And Implementation Sequence

PR 0: Codex hook hotfix freeze.

- Keep the already-performed source hotfix separate.
- `PreToolUse`, `SessionStart`, and `UserPromptSubmit` remain absent from Codex hook registration.
- Runtime reload/reinstall and Codex restart are required before an active session observes the change.

PR 1: Surface status metadata.

- Add machine-checkable status for MCP tools, skills, agents, hooks, and managed-settings fragments.
- Include explicit keep/register/retire status for `pm_semantic_workbench_state` and `pm_semantic_consistency_gate` before any physical deletion work.
- Status values: `public-core`, `protected-default-off`, `dev-only`, `docs-only`, `internal`, `deprecated-candidate`, `archived`.
- No deletion in this PR.

PR 2: MCP profiles.

- Add `studio-core`, `dev-full`, `protected-actions`, and `internal-telemetry`.
- Generate default served tools from capability metadata.
- Preserve MCP-first evidence before hiding raw context tools.

PR 3: Hook and governance narrowing.

- Keep broad Codex `PreToolUse` absent.
- Narrow `PermissionRequest`.
- Add review-artifact allow paths and read-only shell classification.
- Add hook match reports and aggregate timeout budgets.
- Make `commit-edits-governance.ts` the single strict `commit_edits` boundary.

PR 4: Skills and agents shrink.

- Keep thin Codex wrappers.
- Shrink default skills.
- Convert deprecated/Claude-shaped agents to archived/docs-only as appropriate.
- Add tests against accidental canonical skill injection and deprecated agent discovery.

PR 5: Runtime separation contracts.

- Add neutral runtime ids, adapter manifests, unsupported capability records, hook intent contracts, tool profile contracts, cache authority contracts, and parity contracts.
- Create Codex adapter manifest from existing source facts.
- Create Claude adapter manifest owning managed settings and Claude-shaped wrappers.
- Create Gemini adapter manifest with explicit gap records.

PR 6: Chatbot Studio data core.

- Add `ChatbotStudioDeclaration`, session/exchange state, tool/action/eval surfaces, validators, and JSON schemas.
- Extend existing `semantic-conversation-state.ts`, `application-state.ts`, `retrieval-context.ts`, and `workbench-state.ts` rather than bypassing them.
- This PR depends on PR 5 runtime separation contracts for runtime projection fields unless it intentionally scopes `RuntimeProjection` to placeholder gap records only.
- Add `chatbot-studio-local-regression.json`.

PR 7: Local workbench, session ledger, and publish analogue.

- Add a local debug/view flow that compiles context, pins application variables, plans tools, records traces, shows runtime gaps, and blocks protected actions until approval evidence exists.
- Add a local callable function shape with `userInput`, optional `sessionId`, variable inputs, markdown response, session id, variable updates, and trace refs.
- Use JSONL or SQLite for session/trace ledgers.

PR 8: Physical deletion.

- Delete only after no-reference proof, deprecation-map coverage, green tests, and reinstall/restart smoke evidence for the metadata, profile, hook, and runtime replacements.
- Candidates include `pm_semantic_workbench_state`, `pm_semantic_consistency_gate`, legacy handlers, legacy governance builders, deprecated implementer agents, and unregistered handlers only after keep/register/retire decisions are complete.

## F. Validation Gates

Validation is split by what exists now, what the read-only subagent review did not execute, what the Lead separately verified for the source hotfix, and what each future PR must add before it can be considered complete.

Existing runnable commands now are the usual repo checks (`bunx tsc --noEmit`, `bun test`, and `bun run skill:check`). The runtime-separation and Chatbot Studio test paths in this proposal are future acceptance tests that must be added before those PRs are complete.

Already run by read-only subagent review: none. The specialist reports used local evidence and assigned report writes only.

Already run separately by the Lead for the source hotfix and harness package:

```bash
# palantir-mini source hotfix checks
cd /home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini
bun test tests/runtime-boundary/codex-plugin-hooks.test.ts
bun test tests/bridge/handlers/pm-plugin-self-check.test.ts

# meta-harness package checks
cd /home/palantirkc/meta-harness
python3 scripts/validate_codex_port.py
python3 scripts/test_install_harness.py
```

The key acceptance bar is simple: the source proposal can be approved without being mistaken for live Codex behavior, and the active runtime must prove the mounted hook manifest, MCP profile, and skill surface before anyone treats the source plan as operational.
