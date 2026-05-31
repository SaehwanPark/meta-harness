# Deletion And PR Sequence
## Scope

Role: `deletion_and_pr_sequence`.

Harness project: `/home/palantirkc/meta-harness`.

Reviewed source authority: `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini`.

Owned output: `/home/palantirkc/meta-harness/_workspace/palantir-mini-codex-review-2026-05-31/10_subagents/07_deletion_and_pr_sequence.md`.

This review followed the explicit opt-out contract. I did not use palantir-mini MCP tools, palantir-mini skills, palantir-mini routing, workflow gates, or plugin validation tools. Evidence is local file reads, local diffs, and sibling meta-harness review artifacts.

Goal: propose a staged PR sequence for deleting, merging, or default-disabling unnecessary MCPs, skills, agents, hooks, and runtime policy surfaces while preserving protected-mutation safety and making rollback cheap.

## Files And Sources Read

- `/home/palantirkc/meta-harness/.agents/skills/harness/SKILL.md`
- `/home/palantirkc/meta-harness/docs/harness/README.md`
- `/home/palantirkc/meta-harness/_workspace/palantir-mini-codex-review-2026-05-31/00_input/palantir-mini-opt-out-protocol.md`
- `/home/palantirkc/meta-harness/_workspace/palantir-mini-codex-review-2026-05-31/00_input/palantir-mini-opt-out.env`
- `/home/palantirkc/meta-harness/_workspace/palantir-mini-codex-review-2026-05-31/10_subagents/02_runtime_hooks_bottleneck_audit.md`
- `/home/palantirkc/meta-harness/_workspace/palantir-mini-codex-review-2026-05-31/10_subagents/03_mcp_tool_surface_audit.md`
- `/home/palantirkc/meta-harness/_workspace/palantir-mini-codex-review-2026-05-31/10_subagents/04_skills_agents_surface_audit.md`
- `/home/palantirkc/meta-harness/_workspace/palantir-mini-codex-review-2026-05-31/10_subagents/05_governance_rbac_safety_audit.md`
- `/home/palantirkc/meta-harness/_workspace/palantir-mini-codex-review-2026-05-31/10_subagents/06_one_dev_local_architecture.md`
- `/home/palantirkc/meta-harness/_workspace/palantir-mini-codex-review-2026-05-31/10_subagents/08_runtime_separation_audit.md`
- `/home/palantirkc/palantir-mini-marketplace/README.md`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/.codex-plugin/plugin.json`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/.mcp.json`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/package.json`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/README.md`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/PRIVATE_INSTALL.md`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/docs/CODEX_HOOK_ADAPTER.md`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/docs/RELOAD_PER_RUNTIME.md`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/managed-settings.d/50-palantir-mini.json`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/bridge/mcp-server.ts`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/hooks/codex-hooks.json`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/hooks/hooks.json`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/codex-skills/README.md`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/tests/runtime-boundary/codex-plugin-hooks.test.ts`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/schemas/pm-pre-mutation-governance.input.schema.json`
- Read-only git evidence from `/home/palantirkc/palantir-mini-marketplace`: `status --short plugins/palantir-mini`, `diff --stat -- plugins/palantir-mini`, and targeted diffs for docs/tests/schema/MCP files. One targeted `git diff` against `hooks/codex-hooks.json` was blocked by active hook policy; the same hotfix state was verified from file contents and tests/docs diffs.

## Proposed PR Slices

### PR 0: land the Lead hotfix as the emergency unlock

Status: already made in source, not by this reviewer.

Keep this as a small, separate PR or first commit in the cleanup train. The source now removes Codex `PreToolUse` from `hooks/codex-hooks.json`, updates `docs/CODEX_HOOK_ADAPTER.md`, updates `docs/RELOAD_PER_RUNTIME.md`, and updates `tests/runtime-boundary/codex-plugin-hooks.test.ts` so the checked-in Codex registry intentionally mounts `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `SubagentStart`, `SubagentStop`, and `Stop`, but not `PreToolUse`, `SessionStart`, or `UserPromptSubmit`.

Rationale: explicit opt-out review writes were repeatedly blocked by broad pre-tool governance. Removing `PreToolUse` from Codex is the right emergency stopgap until prompt opt-out capture, read-only command classification, and review-artifact write classification are reliable.

Do not bundle physical deletion of hooks, MCPs, skills, or agents into this PR. The only intended behavior change is the Codex mount surface.

Validation:

```bash
cd /home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini
bun test tests/runtime-boundary/codex-plugin-hooks.test.ts
bun test tests/lib/codex/codex-hook-adapter.test.ts
bunx tsc --noEmit
```

Runtime reload: reinstall the Codex plugin payload and restart Codex. Hook mount changes are not hot-reloaded.

Rollback: restore the prior `PreToolUse` registration only if protected mutations are observed bypassing `PermissionRequest` or explicit user approvals. If rollback is needed, keep opt-out review work paused until review-artifact and read-only allow paths are added.

### PR 1: add explicit surface-status metadata before deleting anything

Add or generate a single inventory source for MCP tools, skills, agents, and hook policy groups with statuses such as `public-core`, `protected-default-off`, `dev-only`, `docs-only`, `internal`, `deprecated-candidate`, and `archived`.

Target surfaces:

- MCP tools in `bridge/mcp-server.ts`.
- Codex wrapper skills in `codex-skills/`.
- Canonical skills in `skills/`.
- Agent markdown files in `agents/`.
- Hook policy groups in `hooks/hooks.json` and Codex mount groups in `hooks/codex-hooks.json`.
- Managed-settings allow/ask/deny fragments.

Rationale: the live source already has classification hints, but all MCP tools become public through `tool.audience = "public"` and managed settings broadly allow the full tool set. Deletion should wait until there is a machine-checkable intent field and a test that proves default exposure follows it.

Validation:

```bash
cd /home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini
bun test tests/bridge/mcp-server-schema.test.ts
bun test tests/integration/codex-skill-surface.test.ts
bun test tests/lib/agents/deprecation.test.ts
bun test tests/bridge/handlers/pm-plugin-self-check.test.ts
bun run skill:check
bunx tsc --noEmit
```

Rollback: remove the metadata reader or generated manifest, leaving current public behavior unchanged. This PR should not remove runtime availability.

### PR 2: introduce MCP profiles and make non-core tools default-off

Add a default Codex MCP profile, for example `studio-core`, plus an explicit maintainer profile such as `dev-full`. The default profile should expose only the one-developer local Studio core:

- `pm_semantic_intent_gate`
- `pm_ontology_engineering_workflow`
- `pm_intent_router`
- `ontology_context_query`
- `pm_pre_mutation_governance`
- `compute_edits_dry_run`
- `ontology_schema_get`

Default-off or maintainer-only:

- Protected mutation and state-changing tools: `apply_edit_function`, `commit_edits`, `negotiate_sprint_contract`, `research_library_refresh`, `emit_event`, `events_log_rotate`.
- Raw context reads that should merge behind projections: `get_ontology`, `impact_query`, `pre_edit_impact`, `pm_substrate_query`, `pm_lead_brief`, `research_context_select`.
- Audit/release/maintenance tools: `pm_health_audit`, `pm_plugin_self_check`, `pm_surface_contract_audit`, `pm_aip_source_authority_validate`, `pm_runtime_decision_parity`, `pm_rule_query`, `pm_rule_audit`, `validate_managed_settings_fragments`, `grade_outcome_with_rubric`, `pm_grader_dispatch`, `pm_workflow_response_validate`.

Dependency requirement: before hiding `get_ontology`, `impact_query`, or `pre_edit_impact`, make `ontology_context_query` and/or `pm_pre_mutation_governance` emit equivalent MCP-first evidence where hooks currently require it. Otherwise the cleanup will break the existing pre-edit safety model.

Validation:

```bash
cd /home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini
bun test tests/bridge/mcp-server-schema.test.ts
bun test tests/bridge/mcp-server-mcp-first-evidence.test.ts
bun test tests/bridge/handlers/pm-plugin-self-check.test.ts
bun test tests/bridge/handlers/validate-managed-settings-fragments.test.ts
bun test tests/lib/capability-registry/loader.test.ts
bun test tests/lib/capability-registry/cache.test.ts
bunx tsc --noEmit
```

Runtime reload: MCP server changes require plugin reinstall and Codex process restart.

Rollback: switch the default profile back to `dev-full` or reinstall the previous plugin payload. Do not delete hidden tools in this PR.

### PR 3: narrow hooks by effect, opt-out, and runtime event support

Build on PR 0. Keep Codex `PreToolUse`, `SessionStart`, and `UserPromptSubmit` unmounted until the runtime can prove prompt capture and opt-out visibility before tool interception. Narrow `PermissionRequest` so it does not replay every shared `PreToolUse` policy for every permission event.

Merge or disable:

- Merge the commit-edits branch of `commit-edits-precondition.ts` into `commit-edits-governance.ts`, then retire that branch.
- Disable or narrow the raw edit branch of `commit-edits-precondition.ts`; a repository merely having `.palantir-mini` should not make unrelated opted-out review artifacts require a bound harness contract.
- Narrow `ontology-engineering-workflow-enforcement-gate.ts` so read-only commands and explicit review-artifact writes do not require FDE/SIC/DTC provenance.
- Keep `pre-edit-impact-mcp-first.ts` for protected non-small edits, but let explicit opt-out review artifacts bypass it.
- Add read-only shell classification for `jq` and similar JSON/file inspection commands when no write, network, redirect, or mutation flag is present.
- Add an adapter-level total budget and a match report: lifecycle event, tool, candidate names, matched policy refs, sync/async split, summed sync timeout, block-capable hooks.

Validation:

```bash
cd /home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini
bun test tests/lib/codex/codex-hook-adapter.test.ts
bun test tests/hooks/hooks-json-conditional-if.test.ts
bun test tests/lib/hooks/timeout-policy.test.ts
bun test tests/lib/hooks/tool-classifier.test.ts
bun test tests/hooks/commit-edits-governance.test.ts
bun test tests/hooks/commit-edits-precondition.test.ts
bun test tests/hooks/ontology-engineering-workflow-enforcement-gate.test.ts
bun test tests/hooks/pre-edit-impact-mcp-first.test.ts
bun test tests/hooks/pre-edit-impact-mcp-first.blocking.test.ts
bunx tsc --noEmit
```

Runtime reload: hook JSON, hook scripts, and adapter changes require plugin reinstall and Codex restart. If the fallback shim is still used locally, run `bun scripts/sync-codex-adapter.ts --dry-run`, then regenerate only after source validation.

Rollback: re-enable the previous hook group or previous adapter behavior if protected mutations can proceed without governance, if `commit_edits` no longer fails closed, or if opt-out/read-only classification accidentally allows source mutation.

### PR 4: shrink Codex default skills and keep canonical skills out of default injection

Keep the thin `codex-skills/` wrapper pattern, but shrink defaults to the small front-door and continuity set:

- Keep default: `pm-semantic-intent-gate`, `pm-orchestrate`, `pm-ontology-engineering-lead` if explicitly needed, `pm-verify`, `pm-recap`, `pm-mcp-reload`.
- Keep explicit release-only: `pm-review`, `pm-ship`.
- Merge or docs-only behind the front door: `pm-intent-to-ontology`, `pm-dtc-fill`.
- Dev-only or one audit entrypoint: `pm-rule-audit`, `pm-memory-map`, `pm-value-audit`, `pm-replay`, `pm-events-rotate`, `pm-dirty-classify`.

Add a test that Codex plugin discovery uses `.codex-plugin/plugin.json#skills` and does not inject the full canonical `skills/` tree. The source currently keeps 16 Codex wrappers and a much larger canonical skill library; runtime discovery must not treat both as default surfaces.

Validation:

```bash
cd /home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini
bun test tests/integration/codex-skill-surface.test.ts
bun test tests/lib/skills/skill-ontology-contract.test.ts
bun test tests/skills/tmpl-regen-idempotent.test.ts
bun run skill:check
bunx tsc --noEmit
```

Runtime reload: skill surface changes require plugin reinstall and Codex restart.

Rollback: restore the previous `codex-skills/` wrapper set. Canonical `skills/` should remain untouched in this PR except for docs/status metadata.

### PR 5: archive deprecated agents and convert Claude-shaped agents to docs-only for Codex

Delete from active discovery only after an archive/tombstone policy exists:

- `agents/pm-implementer.md`
- `agents/mc-implementer.md`
- `agents/kosmos-implementer.md`
- `agents/home-implementer.md`

`project-implementer` is the replacement for project-specific implementers, but `home-implementer` needs its inconsistent replacement text normalized before archive.

Convert these to docs-only or dev-only for Codex until native evidence exists:

- `lead-orchestrator`
- harness planner/generator/evaluator/analyzer agents
- grader agents: `code-grader`, `model-grader`, `eval-judge`
- `docs-researcher`, `scrapling-fetcher`, and researcher variants where they assume Claude tools or write research state
- maintainer roles: `hook-builder`, `plugin-maintainer`, `ontology-steward`, `protocol-designer`, `agent-author`

Rationale: `.codex-plugin/plugin.json` exports skills and MCP servers, not agents. Active `agents/*.md` files are useful recipes, but many contain Claude model pins, Claude memory assumptions, Claude-style tools, and MCP name variants. Do not make file presence equal public Codex agent availability.

Validation:

```bash
cd /home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini
bun test tests/lib/agents/deprecation.test.ts
bun test tests/agents/contract-propagation.test.ts
bun test tests/bridge/handlers/pm-plugin-self-check.test.ts
bunx tsc --noEmit
```

Runtime reload: if any runtime consumes agent files, reinstall/restart that runtime. Codex currently has no declared agent export surface in the plugin manifest.

Rollback: move archived files back into `agents/` and restore prior discovery status. Do not delete tombstones until all references are migrated.

### PR 6: split runtime-specific policy from neutral semantics

Separate runtime-neutral concepts from runtime-specific adapter artifacts:

- Neutral core: protected mutation, generated-file denial, DTC/SIC/FDE concepts, semantic conversation state, action approval, event envelope contracts.
- Codex adapter: `.codex-plugin/plugin.json`, `.mcp.json`, `hooks/codex-hooks.json`, Codex hook adapter, Codex reload docs.
- Claude adapter: `managed-settings.d/50-palantir-mini.json`, Claude hooks/settings/memory assumptions, Claude CLI model grader behavior.
- Gemini adapter: explicit gap docs until installed.

Fix runtime identity defaults that silently fall back to Claude. Unknown runtime should become `unknown`, `needs_runtime_selection`, or `runtime_gap`, not `claude-code`.

Validation:

```bash
cd /home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini
bun test tests/runtime-boundary/runtime-boundary.test.ts
bun test tests/runtime-boundary/runtime-parity-claims.test.ts
bun test tests/docs/runtime-neutral-docs-sentinel.test.ts
bun test tests/lib/runtime/capability-matrix.test.ts
bun test tests/cross-runtime/surface-decision-parity.test.ts
bun test tests/bridge/handlers/pm-runtime-decision-parity.test.ts
bunx tsc --noEmit
```

Runtime reload: source-only neutral contract changes do not necessarily reload a running session, but any adapter manifest, hook, MCP, skill, or lib used by hooks/handlers still requires reinstall and restart.

Rollback: restore previous adapter files and identity resolver behavior if runtime adapters cannot select their own identity or if event lineage loses explicit runtime identity.

### PR 7: physical deletion after two green releases or explicit no-reference proof

Only delete files after PRs 1-6 prove replacements, tests are green, and no active references remain.

Deletion candidates:

- `ontology_context_query_legacy` handler mapping and handler file, after internal callers migrate to `ontology_context_query`.
- Legacy `pre-mutation-governance.ts`, after v2 is the only decision path.
- Retired commit-edits branch in `commit-edits-precondition.ts`, after `commit-edits-governance.ts` owns the boundary.
- Deprecated implementer agents after archive/tombstone references are validated.
- Legacy prompt/startup helper hooks that are documented as direct compatibility helpers and are not mounted for Codex, if no Claude/Gemini adapter still needs them.
- Unregistered handlers such as `pm_semantic_consistency_gate` and `pm_semantic_workbench_state` only after deciding whether they become public core or are intentionally retired.

Validation:

```bash
cd /home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini
rg 'ontology_context_query_legacy|pre-mutation-governance|commit-edits-precondition|pm_semantic_consistency_gate|pm_semantic_workbench_state' .
bun test
bun run skill:check
bunx tsc --noEmit
```

Rollback: revert the deletion commit and reinstall/restart any affected runtime. Keep `_deprecation-map.ts` entries for removed public tools so clients receive a clear replacement path.

## Deletion / Merge / Default-Off Order

1. Freeze the hotfix: Codex `PreToolUse` stays removed from `hooks/codex-hooks.json` until opt-out, read-only classification, and review-artifact writes are proven.

2. Mark status before behavior change: add machine-checkable status metadata for MCP tools, skills, agents, and hooks.

3. Default-off before delete: hide maintainer, mutation, audit, refresh, and raw substrate tools behind explicit profiles before removing any files.

4. Merge raw context tools behind projections: move default usage of `get_ontology`, `impact_query`, `pre_edit_impact`, `pm_substrate_query`, `pm_lead_brief`, and `research_context_select` into `ontology_context_query`, `pm_pre_mutation_governance`, or router outputs. Preserve MCP-first evidence first.

5. Merge duplicate governance boundaries: make `commit-edits-governance.ts` the blocking `commit_edits` authority; retire overlapping `commit-edits-precondition.ts` behavior only after tests prove equivalence.

6. Narrow hooks by operation effect: read-only inspection, review-artifact writes, protected source mutation, generated-file mutation, commit/PR/release mutation, and external egress must be separate policy classes.

7. Shrink Codex skills: keep thin wrappers only for front-door, orchestrate, verify, recap, reload, and explicit release commands; push diagnostics and maintenance to dev-only.

8. Archive agents: remove deprecated implementers from active discovery first; convert Claude-shaped agents to docs-only for Codex before any runtime claims native parity.

9. Split runtime adapters: separate Claude managed settings and Claude CLI grader behavior from Codex plugin/hook/MCP behavior and from neutral core semantics.

10. Delete dead files last: only after no-reference proof, deprecation-map updates, green tests, and one successful reinstall/restart smoke pass.

## Validation And Rollback Criteria

Baseline validation for every PR:

```bash
cd /home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini
bunx tsc --noEmit
bun test
bun run skill:check
```

Focused validation by surface:

- Hook changes: `bun test tests/runtime-boundary/codex-plugin-hooks.test.ts tests/lib/codex/codex-hook-adapter.test.ts tests/hooks/hooks-json-conditional-if.test.ts tests/lib/hooks/timeout-policy.test.ts tests/lib/hooks/tool-classifier.test.ts`.
- MCP changes: `bun test tests/bridge/mcp-server-schema.test.ts tests/bridge/mcp-server-mcp-first-evidence.test.ts tests/bridge/handlers/pm-plugin-self-check.test.ts`.
- Governance changes: `bun test tests/governance/pre-mutation-governance-v2.test.ts tests/hooks/commit-edits-governance.test.ts tests/hooks/pre-edit-impact-mcp-first.blocking.test.ts tests/bridge/handlers/pm-pre-mutation-governance.test.ts`.
- Skill changes: `bun test tests/integration/codex-skill-surface.test.ts tests/lib/skills/skill-ontology-contract.test.ts tests/skills/tmpl-regen-idempotent.test.ts`.
- Agent changes: `bun test tests/lib/agents/deprecation.test.ts tests/agents/contract-propagation.test.ts`.
- Runtime separation changes: `bun test tests/runtime-boundary/runtime-boundary.test.ts tests/runtime-boundary/runtime-parity-claims.test.ts tests/docs/runtime-neutral-docs-sentinel.test.ts tests/lib/runtime/capability-matrix.test.ts tests/cross-runtime/surface-decision-parity.test.ts`.

Reload/reinstall requirements:

```bash
# Local development source registration
codex plugin marketplace add /home/palantirkc/palantir-mini-marketplace
codex plugin add palantir-mini@palantir-mini-marketplace

# Post-merge install from GitHub
codex plugin marketplace add park-kyungchan/palantir-mini-marketplace --ref main
codex plugin add palantir-mini@palantir-mini-marketplace
```

After reinstall, restart the Codex CLI process. Codex has no in-session hot reload for plugin manifests, MCP servers, hooks, skills, or agent surfaces. Docs-only and test-only changes do not require runtime reload by themselves.

Rollback criteria:

- Explicit opt-out review artifacts are blocked again by palantir-mini workflow policy.
- Read-only local inspection commands are classified as protected mutation.
- `commit_edits`, external egress, generated-file mutation, release/deploy, or source mutation can proceed without the intended governance decision.
- MCP profile filtering hides a raw tool before its replacement emits required MCP-first evidence.
- `tools/list`, managed settings, and capability metadata disagree about which tools are public/default-off/dev-only.
- Codex default skill discovery includes both thin wrappers and the full canonical `skills/` tree.
- Runtime identity falls back to Claude, Codex, or Gemini when no runtime evidence exists.
- Any PR requires editing runtime cache payloads under `~/.codex/plugins/cache/**` as semantic authority.

Rollback method:

- Revert the specific PR slice rather than the whole cleanup train.
- Reinstall the previous plugin payload and restart Codex for runtime-surface changes.
- Prefer profile fallback or status reclassification before restoring deleted files.
- If a physical deletion must be rolled back, restore the file and keep the deprecation metadata until a replacement has shipped again.

## Runtime Separation Milestones

1. Codex hotfix milestone: `PreToolUse`, `SessionStart`, and `UserPromptSubmit` remain absent from Codex hook registration; docs and tests say so.

2. Codex default profile milestone: default MCP and skill surfaces are small, user-facing, and Studio-oriented; maintainer and mutation tools are opt-in.

3. Claude artifact milestone: `managed-settings.d/50-palantir-mini.json` is labeled and validated as Claude managed-settings authority, not runtime-neutral RBAC for Codex or Gemini.

4. Neutral core milestone: semantic contracts, DTC/SIC/FDE policy, action approval, response-claim validation, and event schemas do not import runtime-native hook, MCP, settings, cache, or provider APIs.

5. Adapter milestone: Codex, Claude, and future Gemini each have separate mount/config/reload evidence. Missing support becomes `runtime_gap`, not implicit parity.

6. Event lineage milestone: shared event logs remain allowed only as neutral substrate with explicit runtime identity, session id, adapter provenance, and source-authority refs.

7. Deletion milestone: files are physically removed only after profile default-off, reference migration, tests, deprecation-map coverage, reinstall/restart smoke proof, and rollback path are all present.

## Proposal Implications

- The cleanup should be framed as exposure reduction first, deletion second. The riskiest current behavior is over-broad default availability and over-broad hook attachment, not file existence alone.
- The Lead hotfix is a necessary safety valve for Codex review usability, but it is not a complete safety model. Protected mutation must remain governed at `PermissionRequest`, MCP protected-action tools, commit/release boundaries, and explicit runtime adapters.
- MCP tools need profiles because the one-developer Studio core is much smaller than the maintainer control plane.
- Hook policy needs effect-based classification before reintroducing any broad pre-tool enforcement.
- Codex skills should remain thin pointers; canonical skills are source docs, not per-turn default context.
- Agent files should be treated as role recipes until a runtime explicitly exports and validates them.
- Managed settings should stop serving as a mixed Claude/Codex/Gemini authority. Split it into runtime-native policy artifacts and a smaller neutral semantic policy.
- Deletion PRs should be late and reversible: no behavior surprise, no cache edits, no generated-file direct edits, and a clear rollback commit.

## Open Questions

- Should default MCP profiles be selected by environment variable, separate `.mcp.json` entries, or generated plugin manifests?
- Should `PermissionRequest` keep mapping to shared `PreToolUse`, or should it get its own smaller permission-only policy family?
- What exact read-only shell grammar should classify `jq`, `node -e`, and `git diff` inspection as safe without allowing shell writes?
- Should `pm_semantic_workbench_state` become the public Studio state projection, or should its output merge into `ontology_context_query` and `pm_semantic_intent_gate`?
- Is `pm_semantic_consistency_gate` intentionally unregistered, or should it become part of the semantic front door before tool-surface deletion?
- How many green releases or smoke runs are enough before deleting deprecated agents and legacy handlers?
- Should Claude managed-settings continue shipping inside the Codex plugin payload, or move to a Claude-specific adapter/package lane?

## Confidence And Gaps

Confidence is high for the ordering principle: hotfix first, metadata/profile narrowing second, hook and governance narrowing third, skill/agent default reduction fourth, runtime separation before physical deletion.

Confidence is high that Codex `PreToolUse` has already been removed from the source hook registry and docs/tests were updated to match. The source file, docs/test diffs, and runtime-boundary test all align on that point.

Confidence is medium for exact keep/merge/default-off placement because final policy depends on product choice: one-developer Studio default versus maintainer full control plane.

Gaps:

- No palantir-mini MCP tools, skills, routing, or workflow gates were used.
- No tests were executed; commands above are proposed validation commands.
- Installed Codex cache was not inspected; source/cache drift remains possible.
- Active hooks blocked some read-only inventory commands, so some counts rely on source file reads and sibling review artifacts rather than fresh JSON summaries.
- This report does not authorize mutation of palantir-mini source, Codex cache payloads, generated files, or `.palantir-mini/session` state.
