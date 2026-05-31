# Runtime Separation Audit

## Scope

Role: `runtime_separation_audit`.

Reviewed source authority: `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini`.

Review contract: use the meta-harness review process plus local read-only evidence only. I did not use palantir-mini MCP tools, palantir-mini skills, palantir-mini routing, or palantir-mini workflow tools. The only write is this assigned report path.

User requirement under audit: Claude, Codex, and Gemini should become completely separated active runtimes under an LLM-agnostic runtime-neutral core. Provider identity must remain metadata, not semantic authority. Runtime-native hooks, settings, memory, tool names, model graders, and caches must not bleed into the neutral core or into other runtime adapters.

This is a static source audit. It identifies coupling risks and separation rules; it does not mutate the reviewed palantir-mini source.

## Files And Sources Read

Meta-harness contract inputs:

- `/home/palantirkc/meta-harness/.agents/skills/harness/SKILL.md`
- `/home/palantirkc/meta-harness/_workspace/palantir-mini-codex-review-2026-05-31/00_input/palantir-mini-opt-out-protocol.md`

Runtime identity and capability surfaces:

- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/runtime/capability-matrix.ts` lines 1-122
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/runtime/identity.ts` lines 1-27
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/runtime/surface-decision-parity.ts` lines 22-58
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/bridge/handlers/pm-runtime-decision-parity.ts` lines 7-11
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/bridge/mcp-server.ts` lines 662-675

Hook, adapter, and prompt-front-door surfaces:

- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/hooks/hooks.json` lines 1-708
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/hooks/codex-hooks.json` lines 1-104
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/hooks/workflow-registry.ts` lines 1-177
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/hooks/policy-registry.ts` lines 105-189 and 617-623
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/codex/codex-hook-adapter.ts` lines 141-199, 241-372, 401-470, 621-656, 810-815, 873-979
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/tests/runtime-boundary/codex-plugin-hooks.test.ts` lines 37-101
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/prompt-front-door/envelope.ts` lines 7-132
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/prompt-front-door/store.ts` lines 118-224
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/prompt-front-door/validators.ts` lines 30-32
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/prompt-front-door/approval-ref.ts` lines 7-23 and 105-106
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/hooks/prompt-front-door-capture.ts` lines 1-6, 33-51, 181-221, 283-332
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/hooks/user-prompt-submit.ts` lines 1-2 and 100-119
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/hooks/prompt-dtc-enforcement-gate.ts` lines 135-141, 377-399, 478-485, 647-720, 768-914
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/hooks/pre-edit-impact-mcp-first.ts` lines 20-40, 131-249, 410-489

Model grading, agents, and runtime-owned configs:

- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/bridge/handlers/pm-grader-dispatch.ts` lines 1-7, 36-63, 204-347
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/bridge/handlers/grade-outcome/model.ts` lines 1-7, 25-57, 60-80, 108-145
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/agents/model-grader.md` lines 1-17 and 99-116
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/agents/lead-orchestrator.md` frontmatter and runtime projection sections
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/agents/protocol-designer.md` frontmatter
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/agents/docs-researcher.md` frontmatter
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/agents/ontology-steward.md` frontmatter
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/managed-settings.d/50-palantir-mini.json` lines 1-98
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/bridge/handlers/pm-plugin-self-check/check-managed-settings.ts` lines 11-64
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/.codex-plugin/plugin.json` lines 2-40
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/.mcp.json` lines 3-12

Source/cache authority, research, docs, and event identity:

- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/contracts/layer-boundary.contract.json` lines 4-199
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/contracts/runtime-evidence/codex.json` lines 1-19
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/.ssot-authority.json` lines 5-20
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/SSOT-AUTHORITY.md` lines 3-77
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/README.md` lines 3-23, 35-45, 71-166, 192
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/docs/RUNTIME_LAYER_BOUNDARY.md` lines 3-67
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/docs/CODEX_HOOK_ADAPTER.md` lines 17-91 and 150-164
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/docs/RELOAD_PER_RUNTIME.md` lines 1-61
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/PRIVATE_INSTALL.md` lines 3-19
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/runtime-overlay/rules/27-cross-runtime-substrate.md` lines 15-29
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/runtime-overlay/research-core-select.ts` lines 6-14 and 231-339
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/scripts/refresh-runtime-overlay.ts` lines 30-45
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/ontology-workflow/emit.ts` lines 78-238
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/event-log/timing.ts` lines 122-155
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/skill-suggestion-emit.ts` lines 43-58
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/plan-root/resolve-plan-root.ts` lines 4-68

## Confirmed Cross-Runtime Couplings

1. The runtime capability model mixes provider-specific facts in one shared table.

   `lib/runtime/capability-matrix.ts` defines `RuntimeId = "claude" | "codex" | "gemini"` and then stores Claude, Codex, and Gemini hook/event facts in the same module. Codex gaps are phrased as missing "Claude ${event}" lifecycle events, and Gemini gaps are phrased as missing "Codex ${event}" events. That is useful as compatibility documentation, but it makes one runtime's vocabulary the explanatory frame for another runtime. It also excludes `cursor`, while prompt-front-door accepts `cursor` as a runtime.

2. Runtime identity defaults can silently promote an unknown host to Claude.

   `lib/runtime/identity.ts` defaults `resolveHostRuntimeIdentity` to `"claude-code"` when no runtime is found. `bridge/handlers/grade-outcome/model.ts` similarly defaults `resolveModelGraderHostRuntime` to `"claude-code"`. `hooks/prompt-front-door-capture.ts` defaults `detectRuntime` to `"claude"` if no env/tool-input signal is found. Under the user's requirement, missing runtime identity must become `unknown` or an explicit runtime gap, never Claude by fallback.

3. Prompt-front-door runtime vocabulary is broader than the runtime core.

   `lib/prompt-front-door/envelope.ts` accepts `["claude", "codex", "cursor", "gemini", "unknown"]`, while `capability-matrix.ts` only models Claude, Codex, and Gemini. `approval-ref.ts` accepts any `PromptRuntime`, including `cursor` and `unknown`, for structured approval refs. This creates a mismatch: prompt state can record runtimes that the runtime capability and parity layers cannot evaluate.

4. Prompt-front-door state lookup can scan across runtime pointers.

   `lib/codex/codex-hook-adapter.ts` and `hooks/prompt-dtc-enforcement-gate.ts` read current prompt-front-door envelopes by trying the preferred runtime and then looping across all prompt runtimes. The Codex adapter also searches project/cwd/home candidates. This is convenient during migration, but it risks cross-runtime or cross-project state bleed. A Codex adapter should not discover a Claude or Gemini current pointer unless an explicit neutral handoff contract authorizes it.

5. Shared hook intent, policy support, and runtime mounts are not fully separated.

   `hooks/hooks.json` is described as a runtime-neutral hook workflow intent registry, while also saying current local install support is Codex-only and that Claude/Gemini hook registries are absent. `hooks/codex-hooks.json` then live-reads that shared registry through the Codex adapter. `lib/hooks/workflow-registry.ts` includes Claude, Codex, and Gemini support logic, but `lib/hooks/policy-registry.ts` only gives detailed support claims for Claude/Codex and has incomplete Gemini gating. This collapses three layers that should be distinct: neutral hook semantics, per-runtime mount manifests, and runtime policy evidence.

6. Codex hook support facts are inconsistent across files.

   `hooks/codex-hooks.json` intentionally omits `SessionStart` and `UserPromptSubmit`, but registers `SubagentStart` and `SubagentStop`. `workflow-registry.ts` marks Codex unsupported hook events as only `SessionStart` and `UserPromptSubmit`. Capability docs describe missing Claude task/subagent lifecycle parity, while Codex native events include `SubagentStart` and `SubagentStop`. This is not necessarily wrong, but the naming makes "Claude task/subagent parity" and "Codex subagent hook support" easy to conflate.

7. Some shared emitters hardcode `claude-code` identity.

   `lib/ontology-workflow/emit.ts` emits `workflow_trace_opened`, `workflow_trace_transitioned`, `workflow_trace_closed`, and `dtc_fill_turn_advanced` with `identity: "claude-code"`. `lib/event-log/timing.ts` uses `CLAUDE_SESSION_ID ?? "local"` and `identity: "claude-code"`. `lib/skill-suggestion-emit.ts` emits skill suggestions with `identity: "claude-code"`. `hooks/prompt-dtc-enforcement-gate.ts` emits `pre_mutation_governance_decided` with `identity: "claude-code"`. These are hard couplings inside code paths that otherwise appear runtime-neutral or monitor-like.

8. Model grading is effectively a Claude adapter with non-Claude gaps.

   The model grader documentation and code are honest that Claude hosts use Claude CLI while Codex/Gemini return `needs_human_review`. That is a valid current gap. The coupling risk is that the handler imports Claude Code effort mapping and the lower-level resolver defaults to Claude when env is absent. The neutral grader surface should dispatch through a runtime adapter interface; the Claude CLI invocation should live only in the Claude adapter package.

9. Managed settings are Claude-local but packaged beside runtime-neutral source.

   `managed-settings.d/50-palantir-mini.json` is explicitly loaded by Claude Code and grants broad read/write/bash/MCP access under `~/.claude/**`. `check-managed-settings.ts` validates public MCP tool coverage against those fragments. There is no equivalent Codex/Gemini managed-settings contract in the same validation path. Keeping Claude RBAC in the plugin is fine as a Claude adapter artifact, but it must not be treated as cross-runtime policy.

10. Agent definitions are mostly Claude-shaped runtime wrappers.

    Several active agent files use Claude-native concepts such as `model: opus/sonnet/haiku`, `memory: project`, `TaskCreate`, `TaskUpdate`, `Agent`, Claude-style MCP tool names, and `~/.claude` research/schema paths. `agents/model-grader.md` is the clearest example: it describes Claude CLI grading and non-Claude gaps, but still includes Claude-style frontmatter and Claude MCP/event guidance. These files should be split into runtime-neutral role contracts plus runtime-specific wrappers.

11. Source/cache authority is mostly clear, but active runtime coverage is Codex-only.

    `contracts/layer-boundary.contract.json`, `.ssot-authority.json`, `SSOT-AUTHORITY.md`, `docs/RUNTIME_LAYER_BOUNDARY.md`, `PRIVATE_INSTALL.md`, and `.codex-plugin/plugin.json` correctly distinguish source authority from Codex cache/installed payload. However, they also state that current local install support is Codex-only and that Claude/Gemini package/install paths are inactive or absent. That is accurate for the current source, but it is not the target state of "separated active runtimes."

12. Research/schema provenance still depends on `~/.claude` naming.

    `README.md`, `SSOT-AUTHORITY.md`, `research-core-select.ts`, and `scripts/refresh-runtime-overlay.ts` use plugin-vendored snapshots as the package source, but still treat `~/.claude/research` and `~/.claude/schemas` as external provenance or refresh inputs. This is acceptable as a legacy refresh source only if it is clearly isolated from runtime-neutral semantics. The neutral core should consume vendored or shared-core snapshots, not live Claude runtime homes.

13. Shared event substrate is intentionally cross-runtime.

    `runtime-overlay/rules/27-cross-runtime-substrate.md` says Claude and Codex may append to the same `events.jsonl`, and future Gemini/Cursor should follow the same substrate contract. A shared append-only substrate can remain neutral, but runtime-specific session state, identity, hook state, and prompt-front-door pointers must be isolated. Shared event storage must not imply shared runtime memory or shared runtime authority.

14. Runtime decision parity is only neutral/Claude/Codex.

    `surface-decision-parity.ts`, `pm-runtime-decision-parity.ts`, and the MCP schema compare neutral, Claude, and Codex decisions only. Gemini and Cursor are not first-class participants. This is a gap if the proposal claims separated active Claude/Codex/Gemini runtimes.

15. Legacy Claude plan paths remain accepted.

    `lib/plan-root/resolve-plan-root.ts` keeps canonical plans under `.palantir-mini/plan` but still treats `~/.claude/plans` as a legacy plan artifact root. Legacy support is understandable, but it should be explicitly migration-only and unavailable as a source of current runtime-neutral authority unless a compatibility mode opts in.

## Required Runtime Separation Rules

1. Runtime identity must be explicit.

   No neutral or shared code should default unknown runtime identity to Claude, Codex, Gemini, or Cursor. Unknown runtime should produce `unknown`, `needs_runtime_selection`, or `runtime_gap`.

2. Runtime vocabulary must be unified and typed.

   The set of runtime IDs used by prompt-front-door, capability matrix, hook registry, adapter dispatch, approval refs, and event identity must come from one neutral type. If Cursor is not an active runtime, it should be a future/runtime-gap value, not an approval-capable runtime.

3. Neutral core must not import runtime-native APIs.

   Runtime-neutral code may define contracts, event schemas, ontology semantics, validation rules, and adapter interfaces. It must not import Claude CLI effort mapping, Codex hook wire shapes, Claude managed settings, Gemini extension names, or runtime-home paths.

4. Each active runtime needs its own adapter package.

   Suggested separation:

   - `runtime-core`: neutral contracts, schemas, event envelope types, ontology semantics, prompt contract types, adapter interfaces.
   - `runtime-adapters/claude`: Claude hooks, Claude managed settings, Claude CLI model grader, Claude memory/research compatibility.
   - `runtime-adapters/codex`: Codex plugin manifest, Codex hook adapter, Codex MCP/config install facts, Codex cache refresh docs.
   - `runtime-adapters/gemini`: Gemini extension/event adapter, Gemini install/config docs, Gemini gap evidence until implemented.

5. Prompt-front-door state must be isolated per runtime.

   Prompt envelopes, current pointers, opt-out state, approval refs, and DTC gate state must be namespaced by project, runtime, session, and prompt ID. A runtime adapter may read another runtime's prompt state only through an explicit neutral handoff artifact.

6. Hook semantics, hook mount manifests, and policy evidence must be separate artifacts.

   Neutral hook semantics can say "before mutation" or "after prompt capture." Runtime manifests must say how Claude/Codex/Gemini mount that semantic event. Policy evidence must say which mount is actually active and tested.

7. Runtime-specific settings must never become neutral policy.

   Claude managed settings, Codex plugin manifests, Codex MCP config, and Gemini extension config should each live as runtime-specific adapter artifacts. Neutral validation can check that each runtime adapter provides required capability evidence, but it should not validate all runtimes through one runtime's settings file.

8. Model grading must dispatch through a neutral adapter interface.

   Claude CLI grader behavior belongs in the Claude adapter. Codex and Gemini should provide native graders or explicit `needs_human_review`/`runtime_gap` responses. Neutral code should not map to Claude Code effort levels unless it has selected the Claude adapter.

9. Research and schema snapshots must be portable.

   `~/.claude/research` and `~/.claude/schemas` may remain legacy/dev refresh sources, but runtime-neutral code should consume vendored snapshots or `~/ontology/shared-core` abstractions. Runtime homes should not be live semantic dependencies.

10. Shared event substrate is allowed only as neutral substrate.

    Shared `events.jsonl` can remain a neutral append-only ledger if every event carries explicit runtime identity, session ID, adapter provenance, and source authority. Runtime-local memory, hooks, approval state, and cache state must remain separated.

## Keep / Split / Remove / Runtime-Specific Table

| Surface | Keep | Split | Remove | Runtime-Specific Target |
| --- | --- | --- | --- | --- |
| Layer/source/cache authority contracts | Keep source vs cache distinction and Codex cache demotion | Add Claude/Gemini active adapter authority sections | Remove any implication that Codex install is the only future active runtime | Neutral core plus per-runtime adapter authority |
| Runtime capability matrix | Keep evidence-backed capability facts | Split neutral capability schema from runtime-specific capability data | Remove cross-runtime phrasing like "Gemini lacks Codex event name" as normative language | `runtime-adapters/*/capabilities` |
| Runtime identity resolver | Keep alias normalization | Split host detection by runtime adapter | Remove fallback to `claude-code` | Neutral `unknown` plus adapter-selected identity |
| Hook workflow registry | Keep neutral hook semantic names | Split semantics, mount manifests, and policy evidence | Remove incomplete shared Gemini policy inference | Neutral hooks plus Claude/Codex/Gemini manifests |
| `hooks/hooks.json` | Keep as neutral intent only if stripped of install assumptions | Split active runtime hook registries | Remove Codex-only install statements from neutral file | Runtime-specific hook registries |
| Codex hook adapter | Keep as Codex runtime adapter | Split any neutral prompt/DTC logic into core interfaces | Remove cross-runtime current-pointer scanning by default | `runtime-adapters/codex` |
| Prompt-front-door envelope/store | Keep prompt envelope and approval concepts | Split runtime state namespaces and handoff artifacts | Remove approval-capable `unknown`; restrict `cursor` until adapter exists | Neutral schema plus runtime stores |
| DTC/pre-edit governance gates | Keep neutral governance decisions | Split runtime input parsing and runtime identity emission | Remove hardcoded `claude-code` identities | Neutral gate plus adapter event emitters |
| Model grader | Keep explicit non-Claude gap behavior | Split adapter dispatch from Claude CLI implementation | Remove default Claude host fallback | Claude adapter; Codex/Gemini adapters or gap stubs |
| Managed settings | Keep Claude RBAC fragment as Claude artifact | Split Codex/Gemini settings validation | Remove use as cross-runtime MCP policy baseline | `runtime-adapters/claude/managed-settings` |
| Agent definitions | Keep role semantics | Split role contract from runtime prompt/frontmatter | Remove Claude-native tools from neutral agent definitions | Neutral roles plus runtime wrappers |
| Research/schema refresh | Keep vendored portable snapshots | Split external refresh provenance by source/runtime | Remove live `~/.claude` as neutral source authority | Neutral snapshots; Claude dev refresh input |
| Event ledger | Keep append-only neutral event substrate | Split runtime session and pointer state | Remove hardcoded `claude-code` in shared emitters | Neutral emitter requiring runtime identity |
| Docs | Keep runtime boundary docs | Split by neutral core and each runtime adapter | Remove "per-runtime" titles that only document Codex | `docs/runtime/{core,claude,codex,gemini}` |

## Proposal Implications

The proposed architecture should not try to make Codex, Claude, and Gemini share one operational runtime. It should define a small neutral core and make each runtime adapter prove its own mount points, config, memory assumptions, model grader behavior, and cache/source refresh path.

Near-term proposal implications:

1. Start with a runtime identity correction pass.

   Replace `claude-code` defaults in identity detection, model grading, prompt-front-door capture, event emitters, DTC governance, timing telemetry, and skill suggestion emitters. Unknown runtime should be explicit and non-authorizing.

2. Create a neutral runtime adapter interface before moving code.

   The interface should cover hook event normalization, prompt-front-door capture, governance decision emission, model grading, settings/capability evidence, and reload instructions. The existing Codex adapter can become the first implementation.

3. Promote hook separation before adding Gemini.

   If Gemini is added while `hooks/hooks.json`, `workflow-registry.ts`, and `policy-registry.ts` still mix neutral semantics and mount evidence, the Gemini adapter will inherit ambiguous policy. Split these first.

4. Treat current Codex-only packaging as current-state evidence, not target architecture.

   The current docs correctly describe a Codex plugin package. The proposal needs new active-runtime docs for Claude and Gemini rather than editing Codex docs until they appear runtime-neutral.

5. Move Claude-managed settings and Claude agent frontmatter into a Claude adapter.

   The neutral core should expose role contracts and capability requirements. Claude wrapper files can keep `model`, `memory`, `TaskCreate`, Claude MCP names, and `~/.claude` compatibility.

6. Keep source/cache authority discipline.

   The existing source vs Codex cache separation is a strong part of the design. Extend it to Claude and Gemini by naming each runtime's install/cache/config surfaces instead of weakening the source SSoT.

7. Make shared event ledger semantics stricter.

   If one `events.jsonl` remains shared, the event schema must require runtime ID, host adapter, source authority, and session provenance. Runtime-local prompt pointers and approval state should not be shared through that ledger without explicit handoff events.

## Open Questions

1. Should Cursor be a first-class active runtime in this proposal, or should it be removed from approval-capable prompt-front-door types until a Cursor adapter exists?

2. Should Claude remain a local active runtime for palantir-mini now, or is Claude support only a future adapter target while Codex remains the only installed runtime?

3. What is the intended Gemini native surface: a Gemini CLI extension, an MCP-like adapter, a browser/workspace extension, or only a future capability matrix entry?

4. Should the shared `events.jsonl` remain physically shared across runtimes, or should each runtime have a local event log that is later folded into a neutral lineage projection?

5. Which source should replace `~/.claude/research` and `~/.claude/schemas` as the neutral refresh input: vendored plugin snapshots, `~/ontology/shared-core`, a new `~/.ontology` home, or project-local research packs?

6. How much legacy compatibility should remain for `~/.claude/plans` and Claude agent frontmatter after runtime separation?

7. Should non-Claude model grading remain `needs_human_review`, or should Codex and Gemini receive native model graders in the first separation milestone?

8. What is the minimum acceptance test for "completely separated active runtime": separate install paths, separate hook manifests, separate prompt-front-door stores, separate managed settings, separate model graders, or all of the above?

## Confidence And Gaps

Confidence: high for the listed static source findings. The same coupling patterns appeared across independent surfaces: runtime identity defaults, prompt-front-door storage, hook registries, model grading, managed settings, docs, and shared event emitters.

Gaps:

- I did not run palantir-mini MCP tools, palantir-mini skills, routing, validation, or workflow commands by contract.
- I did not inspect generated Codex cache payloads as authority.
- I did not run dynamic hook simulations or runtime reload tests.
- I did not verify current Claude or Gemini runtime installations, because the reviewed source states those install/package surfaces are absent or inactive.
- I did not browse external docs; this audit is grounded in local source evidence only.

Bottom line: palantir-mini already has a useful source/cache boundary and a candid Codex-only current-state story, but it is not yet separated into active Claude/Codex/Gemini runtimes under a neutral core. The largest required changes are explicit runtime identity, per-runtime adapter packages, per-runtime hook/settings/prompt state, and removal of Claude defaults from shared code.
