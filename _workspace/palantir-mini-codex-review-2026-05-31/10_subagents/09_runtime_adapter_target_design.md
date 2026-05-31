# Runtime Adapter Target Design
## Scope

Role: `runtime_adapter_target_design`.

Project root: `/home/palantirkc/meta-harness`.

Reviewed source authority: `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini`.

Owned output path: `/home/palantirkc/meta-harness/_workspace/palantir-mini-codex-review-2026-05-31/10_subagents/09_runtime_adapter_target_design.md`.

This is a design-only review artifact for a target architecture where Claude, Codex, and Gemini are fully separated active runtimes over one runtime-neutral core. I did not use palantir-mini MCP tools, palantir-mini skills, palantir-mini routing, prompt/DTC gates, or response-template enforcement. Evidence is local file inspection only, plus this single assigned report write.

The design incorporates the Lead hotfix already present in source: Codex `PreToolUse` is intentionally absent from `hooks/codex-hooks.json` until opt-out capture and read-only/review-artifact classification are reliable. The target design treats that as a release guardrail, not as target-state parity.

## Files And Sources Read

Meta-harness and opt-out contract:

- `/home/palantirkc/meta-harness/AGENTS.md`
- `/home/palantirkc/meta-harness/.agents/skills/harness/SKILL.md`
- `/home/palantirkc/meta-harness/README.md`
- `/home/palantirkc/meta-harness/docs/harness/README.md`
- `/home/palantirkc/meta-harness/_workspace/palantir-mini-codex-review-2026-05-31/00_input/palantir-mini-opt-out-protocol.md`
- Existing local review artifacts: `02_runtime_hooks_bottleneck_audit.md`, `03_mcp_tool_surface_audit.md`, `04_skills_agents_surface_audit.md`, `06_one_dev_local_architecture.md`, `08_runtime_separation_audit.md`

Reviewed source authority:

- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/.codex-plugin/plugin.json`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/.mcp.json`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/.ssot-authority.json`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/SSOT-AUTHORITY.md`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/hooks/codex-hooks.json`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/hooks/hooks.json`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/codex/codex-hook-adapter.ts`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/runtime/capability-matrix.ts`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/runtime/identity.ts`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/runtime/surface-decision-parity.ts`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/prompt-front-door/envelope.ts`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/prompt-front-door/store.ts`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/bridge/mcp-server.ts`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/hooks/tool-classifier.ts`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/capability-registry/mcp-tool-capability.ts`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/bridge/handlers/grade-outcome/model.ts`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/managed-settings.d/50-palantir-mini.json`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/contracts/layer-boundary.contract.json`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/contracts/runtime-evidence/codex.json`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/docs/CODEX_HOOK_ADAPTER.md`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/docs/RELOAD_PER_RUNTIME.md`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/docs/RUNTIME_LAYER_BOUNDARY.md`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/scripts/sync-codex-adapter.ts`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/tests/runtime-boundary/codex-plugin-hooks.test.ts`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/tests/lib/codex/codex-hook-adapter.test.ts`

## Target Architecture

The target shape is one source-owned neutral core and three runtime-owned adapter packages:

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
      adapter.manifest.json
      hooks.manifest.json
      mcp-tools.manifest.json
      managed-settings.generated.json
      agent-wrappers/
      model-grader.ts
      reload.md
    codex/
      adapter.manifest.json
      codex-plugin.generated.json
      codex-hooks.generated.json
      mcp.generated.json
      hook-adapter.ts
      skill-wrappers/
      reload.md
    gemini/
      adapter.manifest.json
      extension.generated.json
      hooks.manifest.json
      tools.manifest.json
      model-grader.ts
      reload.md
  hooks/
    hook-intent.registry.json
  bridge/
    mcp-server.ts
```

`core/runtime/*` owns runtime-neutral contracts, not executable runtime behavior. It may define semantic lifecycle events, tool capability metadata, governance decision schemas, prompt-front-door schemas, cache/source authority rules, and parity comparison rules. It must not import Claude CLI behavior, Codex hook response shapes, Gemini extension APIs, managed-settings fragments, runtime-home paths, or provider SDKs.

`runtime-adapters/*` owns native protocol details for one runtime. An adapter may translate native events, tool names, settings, manifests, model-grader calls, reload procedures, and cache/install facts into the neutral contracts. It cannot change the meaning of a SemanticIntentContract, DigitalTwinChangeContract, runtime-neutral tool capability, governance decision, eval verdict, or ontology primitive.

Active runtime selection must be explicit and single-valued per adapter process. The selected runtime should come from a required adapter manifest plus runtime-owned launch configuration, for example `PALANTIR_MINI_HOST_RUNTIME=codex` in Codex `.mcp.json`, a Claude managed-settings/env fragment, or a Gemini extension config. Missing or unrecognized runtime identity must resolve to `unknown` or `needs_runtime_selection`, never to Claude, Codex, or Gemini by fallback.

Runtime selection output should be a `RuntimeSessionContext`:

```ts
interface RuntimeSessionContext {
  runtime: "claude" | "codex" | "gemini" | "unknown";
  adapterId: string;
  adapterVersion: string;
  sessionId?: string;
  projectRoot: string;
  sourceAuthority: string;
  runtimeHome?: string;
  cacheRoot?: string;
  selectedAt: string;
}
```

Hook compilation should be two-stage:

1. Neutral `hook-intent.registry.json` declares semantic events such as `prompt.capture`, `before.protected-mutation`, `permission.request`, `after.tool`, `compact.before`, `compact.after`, `subagent.start`, `subagent.stop`, and `session.stop`.
2. Each adapter compiler maps supported semantic events to native lifecycle events and emits only that runtime's manifest syntax.

For Codex, the current compiled manifest must continue to omit `PreToolUse`. `PermissionRequest` may remain mounted only as a narrow bridge for explicit permission decisions over protected tool calls. `UserPromptSubmit` and `SessionStart` are also currently absent from the checked-in Codex registry; the first possible reintroduction should be a tiny capture-only `UserPromptSubmit` path with a small timeout and tests proving opt-out persistence before any broad pre-tool enforcement is remounted.

MCP/tool exposure should be generated from neutral capability metadata into per-runtime profiles. The target profiles are:

- `studio-core`: semantic gate, workflow/context projection, pre-mutation governance, dry-run, schema read.
- `dev-full`: maintainer audits, research refresh, rule/query surfaces, release validation.
- `protected-actions`: edit proposal and commit tools, disabled by default and enabled only behind approval evidence.
- `internal-telemetry`: event append, MCP-first evidence, log rotation, and diagnostics, callable by runtime internals but not default LLM-facing palettes.

The current source exposes a Codex MCP server through `.codex-plugin/plugin.json -> .mcp.json -> bridge/mcp-server.ts` and marks all live tools public inside the server. The target architecture should keep `bridge/mcp-server.ts` as implementation source, but make served tools profile-aware and runtime-aware before `tools/list`.

Source/cache authority remains strict:

- Source SSoT: `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini`.
- Marketplace root: `/home/palantirkc/palantir-mini-marketplace`.
- Runtime caches: `~/.codex/plugins/cache/**`, future Claude plugin cache paths, and future Gemini extension cache paths.
- Runtime homes: `~/.codex/**`, `~/.claude/**`, and future Gemini runtime home paths.

Runtime caches are installed payloads and may be inspected as consumer evidence only. Durable semantics, manifests, tests, contracts, and adapter source must be edited in the source checkout, then installed/refreshed into the runtime.

Unsupported capability handling should be explicit data, not prose-only caveats. Every adapter should return an `UnsupportedCapabilityRecord` when native lifecycle, model grading, MCP exposure, subagent lifecycle, memory, approval UI, or reload behavior is absent:

```ts
interface UnsupportedCapabilityRecord {
  runtime: "claude" | "codex" | "gemini";
  capabilityId: string;
  attemptedSurface: "hook" | "tool" | "skill" | "agent" | "model-grader" | "memory" | "reload";
  status: "unsupported" | "schema-only" | "manual" | "needs-human-review";
  fallback: string;
  evidenceRefs: string[];
  parityClaimAllowed: false;
}
```

## Runtime Adapter Contracts

`RuntimeAdapterManifest` should be the root contract for every active adapter:

| Field | Meaning |
| --- | --- |
| `schemaVersion` | Versioned adapter manifest schema. |
| `runtime` | Exactly one of `claude`, `codex`, `gemini`. |
| `adapterId` | Stable id, for example `runtime-adapter:codex`. |
| `sourceAuthority` | Must point to the plugin source root, not a cache. |
| `manifestOutputs` | Native files generated for that runtime. |
| `nativeLifecycleEvents` | Events the runtime actually fires with smoke evidence. |
| `semanticEventMap` | Neutral event to native event mapping. |
| `toolProfiles` | Runtime-visible tool profiles and default profile. |
| `settingsSurfaces` | Native settings, managed settings, extension config, or plugin config. |
| `cacheSurfaces` | Runtime cache/install roots, read-only from source perspective. |
| `unsupportedCapabilities` | Structured gap records. |
| `reloadProcedureRef` | Runtime-specific reload doc. |
| `smokeEvidenceRefs` | Tests proving actual runtime behavior. |

`HookCompilationContract` should require that generated hook manifests contain native event names only. Shared hook policy may be read live by an adapter, but generated manifests must not duplicate policy bodies or import another runtime's event vocabulary as native truth.

For Claude, the adapter contract should own Claude hook manifests, managed settings, Claude agent wrappers, Claude memory/research compatibility, and the Claude CLI model-grader path. Claude managed settings should not be validated as if they constrain Codex or Gemini.

For Codex, the adapter contract should own `.codex-plugin/plugin.json`, `hooks/codex-hooks.json`, `.mcp.json`, Codex skill wrapper exposure, the Codex hook adapter, and Codex reload requirements. The current hotfix is part of the contract: `PreToolUse` remains unmounted until opt-out capture and read-only/review-artifact classification tests pass.

For Gemini, the adapter contract should be created before behavior is claimed. It should include a native event map, extension/tool manifest, install/cache path, reload path, model-grader status, and explicit gaps. Until that exists, Gemini support is `manual` or `unsupported`, not active parity.

`ToolExposureContract` should be generated from `MCP_TOOL_CAPABILITIES` plus profile policy. It must include audience, lifecycle, effect, mutation kind, DTC requirement, sprint-contract requirement, external egress, release/deploy implication, and runtime tool aliases. `tools/list` should not hide these distinctions from adapter compilers.

`PromptStateIsolationContract` should namespace prompt-front-door envelopes and current pointers by project root, runtime, session id, and prompt id. An adapter may read another runtime's prompt state only through an explicit neutral handoff artifact that names source runtime, target runtime, prompt id, prompt hash, and approval refs.

`RuntimeDecisionParityContract` should compare neutral, Claude, Codex, and Gemini decisions. Runtime-specific fields such as native event name, manifest syntax, reload steps, UI presentation, and unsupported surface refs may differ; semantic fields such as required contracts, allowed/forbidden tools, blocking gates, advisory gates, eval requirements, lineage requirements, and final decision must match the neutral decision.

## Forbidden Cross-Runtime Couplings

- Neutral code must not default missing runtime identity to `claude-code`. Current `resolveHostRuntimeIdentity` and model-grader host runtime behavior should be changed in implementation to return `unknown` unless an adapter selected the runtime.
- Prompt-front-door state lookup must not scan across all runtimes by default. Cross-runtime prompt lookup requires an explicit handoff artifact.
- Claude managed settings must not define Codex or Gemini MCP policy. Codex plugin manifests and Gemini extension manifests must be generated separately.
- Codex MCP tool aliases must not be treated as Claude managed-settings names, and Claude `mcp__palantir-mini__*` names must not be treated as Codex-native names without adapter mapping.
- Runtime cache paths must not host source edits, source tests, or semantic manifests. They are reinstall outputs only.
- Provider identity must not authorize protected mutation, approve contracts, promote advisory cards, or change tool mutation classification.
- Shared `events.jsonl` may remain a neutral ledger only if events carry explicit runtime, adapter id, session id, and source authority. Runtime-local prompt pointers, memory, settings, and approval UI state must stay runtime-local.
- Agent files with Claude model pins, Claude memory settings, or Claude tool names must not become neutral agent contracts. Split neutral role contracts from runtime wrappers.
- Model grading must not import Claude CLI behavior from neutral code. Claude may own a Claude CLI grader; Codex and Gemini need native graders or explicit `needs_human_review`.
- `hooks/hooks.json` must not remain both neutral intent and install-support status. Codex-only, Claude-only, and Gemini-only mount facts belong in adapter manifests.
- Codex `PreToolUse` must not be reintroduced just because adapter tests can call `runCodexHookAdapter("PreToolUse", ...)`. Runtime mounting requires opt-out/read-only/review-artifact evidence against the generated Codex manifest.
- `PermissionRequest` must not silently become a full duplicate of all shared `PreToolUse` policy. It should be limited to permission-specific protected-action checks unless a later design intentionally expands it and tests latency, opt-out, and classification behavior.
- Runtime parity tests must not compare only neutral/Claude/Codex if the proposal claims active Gemini support.

## Test And Validation Plan

Static contract tests:

- Validate every `runtime-adapters/*/adapter.manifest.json` against a shared `RuntimeAdapterManifest` schema.
- Fail if neutral core files import `~/.claude`, `~/.codex`, Gemini runtime paths, Claude CLI modules, Codex hook response types, Gemini extension APIs, or provider SDKs.
- Fail if runtime identity resolvers default missing runtime to Claude, Codex, or Gemini.
- Fail if prompt-front-door runtime ids differ across prompt envelope, adapter manifest, capability matrix, approval refs, event identity, and parity comparison.

Hook compilation tests:

- Compile neutral hook intent into Claude, Codex, and Gemini manifests and snapshot each manifest.
- Assert the current Codex manifest excludes `PreToolUse`, `SessionStart`, and `UserPromptSubmit` until the hotfix exit criteria are met.
- Assert Codex `PermissionRequest` maps only to the allowed protected-action policy subset and returns Codex permission response shape.
- Assert each generated manifest uses only native events for that runtime and does not include another runtime's event names as native claims.
- Assert unsupported events produce `UnsupportedCapabilityRecord` and never execute hooks.

Codex hotfix exit tests:

- Prove direct opt-out prompt capture before any later tool hook can run.
- Prove stored opt-out suppresses all palantir-mini policy fan-out for later lifecycle events in the same prompt envelope.
- Prove a later explicit opt-in prompt no longer inherits the old opt-out pointer.
- Prove read-only/review-artifact commands used by meta-harness audits are classified read-only, including `sed`, `rg`, `find`, `test`, `wc`, `jq` summaries, `node -e` JSON summaries, and sourced opt-out shell prefixes.
- Prove writing only an assigned `_workspace/.../10_subagents/<role>.md` review artifact is not classified as protected palantir-mini source mutation.
- Prove aggregate pre-tool latency stays below the runtime budget before `PreToolUse` is remounted.

Prompt state isolation tests:

- Save Claude, Codex, and Gemini prompt envelopes with the same session id and prove each adapter reads only its own runtime pointer.
- Add a neutral handoff artifact and prove only then can a target runtime read source-runtime prompt refs.
- Fail if a runtime adapter searches project/cwd/home candidates broadly without a project-root-bound context.

MCP/tool exposure tests:

- Generate per-runtime `studio-core`, `dev-full`, `protected-actions`, and `internal-telemetry` tool manifests from `MCP_TOOL_CAPABILITIES`.
- Assert default public palettes exclude protected mutation and maintainer-only tools.
- Assert `tools/list` for each profile includes capability metadata or a profile manifest that clients can inspect.
- Assert managed-settings allowlists, Codex MCP names, and Gemini tool names are generated from the same neutral capability records but retain runtime-native naming.
- Assert source has no "all tools public" override in the served default profile.

Source/cache boundary tests:

- Fail if source tests, manifests, docs, or adapter compilers read or write `~/.codex/plugins/cache/**` as source authority.
- Fail if runtime-home paths are used as canonical source roots.
- Verify source changes that affect manifests, hooks, MCP tools, skills, or agents require runtime-specific reinstall/reload docs.

Runtime gap and parity tests:

- Expand `compareRuntimeDecisionParity` to include Gemini.
- Assert unsupported lifecycle hooks, model grading, subagent events, and memory features return structured gaps.
- Assert non-Claude model grading does not spawn `claude -p` and does not default to Claude when runtime env is missing.
- Assert runtime-specific fields may differ while semantic decision fields match the neutral decision.

Suggested validation commands for an implementation PR:

```bash
bun test tests/runtime-boundary/codex-plugin-hooks.test.ts
bun test tests/lib/codex/codex-hook-adapter.test.ts
bun test tests/runtime-boundary/runtime-adapter-manifest.test.ts
bun test tests/runtime-boundary/runtime-hook-compilation.test.ts
bun test tests/runtime-boundary/runtime-tool-profiles.test.ts
bun test tests/runtime-boundary/prompt-state-isolation.test.ts
bun run scripts/verify-layer-boundary.ts
```

## Proposal Implications

The proposal should be framed as "neutral core plus active runtime adapters", not "make every runtime behave like Codex" or "make every runtime behave like Claude." Runtime-native files are protocol authorities for their runtime only.

The first implementation milestone should be contract extraction, not behavior expansion:

- Create the neutral runtime id, adapter manifest, unsupported capability, tool profile, hook intent, cache authority, and parity contracts.
- Move current Codex manifest facts under a Codex adapter contract without changing runtime behavior.
- Add a Claude adapter contract that owns existing Claude-shaped managed settings and agent wrappers.
- Add a Gemini adapter contract with explicit gap records before claiming active support.

The second milestone should fix existing bleed before adding new mounts:

- Remove default-to-Claude runtime identity behavior.
- Stop prompt-front-door cross-runtime pointer scanning by default.
- Split neutral hook intent from adapter mount manifests.
- Generate MCP/tool exposure profiles from capability metadata.
- Expand runtime decision parity to include Gemini.

The Codex hotfix must stay in force during these milestones. Codex `PreToolUse` should remain unmounted until tests prove opt-out capture, read-only classification, review-artifact classification, and latency behavior. The existing `02_runtime_hooks_bottleneck_audit.md` contains stale evidence that describes `PreToolUse` as mounted; the reviewed source now supersedes that for this target design.

The current source/cache discipline is strong and should be extended, not weakened. Add Claude and Gemini cache/install sections beside Codex; do not create runtime-home source forks.

MCP surface reduction and runtime separation are connected. If all tools stay public in one MCP server, adapters cannot prove distinct runtime profiles. Tool profile generation should become part of adapter compilation.

Model grading is a good pilot for adapter separation: neutral rubric logic stays core, Claude CLI grading moves to the Claude adapter, and Codex/Gemini return native grader results or structured `needs_human_review`.

## Open Questions

- Should Codex remount `UserPromptSubmit` as capture-only before `PreToolUse`, or should opt-out state come from a runtime-level opt-out environment/config channel instead?
- Should `PermissionRequest` run only protected-action permission checks, or should it continue to bridge selected shared pre-tool policy?
- Is Claude intended to become an active local install target again, or only a source-owned adapter package for users who install it later?
- What is the intended Gemini host surface: Gemini CLI extension, IDE extension, MCP server bridge, or another native protocol?
- Should Cursor remain in prompt-front-door runtime types, or move to a future-runtime/gap enum until a Cursor adapter exists?
- Should the shared event ledger stay physically shared across runtimes, or should each adapter write runtime-local logs that fold into a neutral projection?
- Which tools belong in the default `studio-core` profile, and should raw `get_ontology`, `impact_query`, and `pre_edit_impact` remain public or be internal evidence emitters?
- What is the minimum smoke proof for "active runtime": manifest generated, installed locally, lifecycle hook fired, MCP/tool list verified, model grader status verified, and reload documented?
- Should adapter manifests be committed JSON files, generated files, or both committed source manifests plus generated runtime payloads?

## Confidence And Gaps

Confidence is high for current Codex source facts: `.codex-plugin/plugin.json` points to `hooks/codex-hooks.json` and `.mcp.json`; `hooks/codex-hooks.json` currently omits `PreToolUse`, `SessionStart`, and `UserPromptSubmit`; the Codex adapter live-reads shared hook intent for mounted events; `PermissionRequest` maps to shared `PreToolUse` policy while returning Codex response shape; source/cache boundary docs demote runtime caches.

Confidence is medium-high for the separation risks: local source directly shows default-to-Claude identity behavior, cross-runtime prompt runtime vocabulary mismatch, Claude-managed settings in plugin source, all-public MCP tool exposure, and parity comparison that does not include Gemini.

Confidence is medium for the Gemini target adapter because no active Gemini package/install surface exists in the reviewed source. The report therefore specifies contract requirements and gap handling rather than claiming implementation details.

Gaps:

- No palantir-mini MCP tools, skills, routing, or validation commands were used.
- No tests were executed; this report is based on read-only source evidence.
- Installed Codex cache state was not inspected.
- Official external docs were not needed for terminology, so no web or official-doc refresh was performed.
- The target file layout is a proposed architecture, not proof that the current repository already has those directories.
