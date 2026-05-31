# MCP Tool Surface Audit

## Scope

Role: `mcp_tool_surface_audit`.

Harness project: `/home/palantirkc/meta-harness`.

Reviewed source authority: `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini`.

Owned output: `/home/palantirkc/meta-harness/_workspace/palantir-mini-codex-review-2026-05-31/10_subagents/03_mcp_tool_surface_audit.md`.

This audit stayed inside the opt-out contract: no palantir-mini MCP tools, no palantir-mini skills, no palantir-mini workflow routing, no prompt contract gates, and no response-template enforcement. Evidence was local file reads plus this single report write.

The classification target is a one-developer local AIP Chatbot Studio implementation: a small LLM-callable surface for semantic conversation, context projection, deterministic governance decisions, and explicit human-approved protected actions, with release/audit/maintenance tools kept out of the default public tool palette.

## Files And Sources Read

- `/home/palantirkc/meta-harness/.agents/skills/harness/SKILL.md lines 1-73: harness artifact and repo-local handoff rules.`
- `/home/palantirkc/meta-harness/docs/harness/README.md lines 1-23: `_workspace/` output contract.`
- `/home/palantirkc/meta-harness/_workspace/palantir-mini-codex-review-2026-05-31/00_input/palantir-mini-opt-out-protocol.md lines 1-55: opt-out and authority boundary.`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/bridge/mcp-server.ts lines 1-16, 48-62, 781-887, 897-1100: live MCP source of truth, categories, handler dispatch, all-public assignment, MCP-first evidence side effect.`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/.mcp.json lines 1-15: Codex MCP server command and runtime env.`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/.codex-plugin/plugin.json lines 1-43: plugin manifest linking `mcpServers` to `.mcp.json`.`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/managed-settings.d/50-palantir-mini.json lines 1-107: managed settings MCP allowlist and ask/deny rules.`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/capability-registry/mcp-tool-capability.ts lines 1-90 and 120-480: typed MCP tool capability metadata.`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/hooks/tool-classifier.ts lines 35-75, 95-170, 210-255: runtime classifier read-only and protected-action behavior.`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/hooks/pre-edit-impact-mcp-first.ts lines 1-45: MCP-first hook dependency on `get_ontology`, `impact_query`, and `pre_edit_impact`.`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/bridge/handlers/pm-plugin-self-check/check-mcp-registration.ts lines 1-150: handler inventory versus public MCP registration policy.`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/bridge/handlers/_deprecation-map.ts lines 1-118: removed MCP tool map.`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/bridge/handlers/pm-semantic-workbench-state.ts lines 1-65: internal, unregistered workbench-state exporter.`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/bridge/handlers/pm-semantic-consistency-gate.ts lines 1-73: implemented but unregistered semantic consistency gate.`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/chatbot-studio/semantic-conversation-state.ts lines 13-120 and `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/chatbot-studio/workbench-state.ts` lines 31-90: Chatbot Studio state shapes.`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/docs/RELOAD_PER_RUNTIME.md lines 1-82 and `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/docs/RUNTIME_LAYER_BOUNDARY.md` lines 40-82: source/runtime separation and reload implications.`

## Confirmed Tool Inventory

`bridge/mcp-server.ts` declares 31 live public MCP tools in `TOOLS`; `tools/list` returns those tools; `HANDLER_MODULES` maps each live tool to a handler. One extra handler mapping, `ontology_context_query_legacy`, is explicitly internal or skill-only and not included in `TOOLS` or `tools/list`.

Live tools by server category:

- Ontology engineering: `emit_event`, `get_ontology`, `ontology_schema_get`, `impact_query`, `pre_edit_impact`, `apply_edit_function`, `compute_edits_dry_run`, `pm_ontology_engineering_workflow`, `commit_edits`.
- Harness engineering: `grade_semantic_intent_contract`, `negotiate_sprint_contract`, `grade_outcome_with_rubric`, `pm_grader_dispatch`.
- Lead routing: `pm_semantic_intent_gate`, `pm_intent_router`, `pm_lead_brief`, `pm_health_audit`, `pm_substrate_query`, `research_context_select`, `ontology_context_query`.
- Validation and health: `events_log_rotate`, `research_library_refresh`, `pm_plugin_self_check`, `pm_workflow_response_validate`, `pm_surface_contract_audit`, `pm_aip_source_authority_validate`, `pm_runtime_decision_parity`, `pm_rule_query`, `pm_rule_audit`.
- Hook validation: `pm_pre_mutation_governance`, `validate_managed_settings_fragments`.

Managed settings allow the same 31 `mcp__palantir-mini__*` tool names. Capability registry also has 31 MCP capability records.

Not live MCP tools but relevant to this audit:

- `pm_semantic_workbench_state` exists as an internal handler and explicitly says it is not registered while `SemanticWorkbenchState` remains unstable.
- `pm_semantic_consistency_gate` exists as a handler but is not present in `TOOLS`, `HANDLER_MODULES`, managed settings, or the MCP capability registry.
- Deprecated removed tools are recorded in `_deprecation-map.ts`, including propagation audits, doc drift, schema pin, codegen headers, planner/classification graders, Playwright scenario tools, value metrics, and hook validation helpers.

## Bottleneck Evidence

- All 31 live tools are forced to `audience = "public"` and default `lifecycle = "public"` in `bridge/mcp-server.ts` lines 881-886. `publicToolSpec` returns only name, description, and input schema, so category, audience, lifecycle, owner module, and stable-since metadata are hidden from clients.
- Managed settings allow every live MCP tool in one broad allowlist, lines 38-68. The `ask` section gates only `commit_edits` for ship-merge and `get_ontology` for security reads, leaving `apply_edit_function`, `research_library_refresh`, `negotiate_sprint_contract`, `emit_event`, and `events_log_rotate` directly allowed by that fragment.
- The capability registry already knows distinctions hidden by the public surface: effect, mutation kind, DTC approval, sprint contract requirement, data action, release deploy, external egress, and classifier projection.
- The hook classifier has a narrower read-only set than the public surface. `negotiate_sprint_contract` and `ontology_context_query` can become protected actions depending on input.
- MCP-first enforcement depends on direct calls to `get_ontology`, `impact_query`, or `pre_edit_impact`, which pressures the project to keep raw read tools public even when Studio would prefer one context projection.
- There are 76 top-level handler files under `bridge/handlers` versus 31 live public tools. The self-check treats inventory-only handlers as advisory rather than registration drift.
- The likely Studio state surface is not live: `pm_semantic_workbench_state` is intentionally internal while `SemanticWorkbenchState` remains unstable.

## Keep / Merge / Disable / Delete Table

| Tool | Classification | Reason / action |
|---|---|---|
| `pm_semantic_intent_gate` | Public core | Core semantic conversation and SIC/DTC boundary gate; keep public as a guided Studio action. |
| `pm_ontology_engineering_workflow` | Public core | Core workflow state machine; keep, but do not treat event append as authorization. |
| `pm_intent_router` | Public core | Useful after approved refs exist; keep with explicit preconditions and no hidden auto-approval in Studio mode. |
| `ontology_context_query` | Public core | Best single read-path/context projection candidate; absorb lower-level context reads. |
| `pm_pre_mutation_governance` | Public core | Compute-only governance decision before protected mutation; make it mandatory preflight. |
| `compute_edits_dry_run` | Public core | Safe preview/evaluation path before commit. |
| `ontology_schema_get` | Public core | Read-only schema retrieval needed for local authoring and validation. |
| `get_ontology` | Merge | Raw ontology snapshot read; fold behind ontology_context_query, keep temporarily for MCP-first/security-domain compatibility. |
| `impact_query` | Merge | Raw impact read; fold into ontology_context_query and pm_pre_mutation_governance, keep temporarily for MCP-first compatibility. |
| `pre_edit_impact` | Merge | Pre-edit projection overlaps with context/governance; keep temporarily for hooks. |
| `pm_substrate_query` | Merge | Lineage/workflow/retro/learn reads overlap with context and health projections. |
| `pm_lead_brief` | Merge | Session opener overlaps with router/context responses. |
| `research_context_select` | Merge | Retrieval pack selection should be an axis of the context projection. |
| `grade_semantic_intent_contract` | Merge | Deterministic SIC grading should run inside the semantic gate; keep standalone for tests/debug. |
| `pm_grader_dispatch` | Merge | Single-criterion grader overlaps with grade_outcome_with_rubric; keep internal if possible. |
| `pm_workflow_response_validate` | Merge | Response-template validation belongs in release/self-check or internal enforcement, not Studio UX. |
| `pm_rule_query` | Dev-only | Maintainer/governance debug surface, not default Studio core. |
| `pm_rule_audit` | Dev-only | Maintainer health check. |
| `pm_health_audit` | Dev-only | Broad audit multiplexer for maintainers. |
| `pm_plugin_self_check` | Dev-only | Release/plugin health aggregator. |
| `pm_surface_contract_audit` | Dev-only | Surface-contract audit for maintainers. |
| `pm_aip_source_authority_validate` | Dev-only | Source-authority audit for maintainers. |
| `pm_runtime_decision_parity` | Dev-only | Runtime parity audit for maintainers. |
| `validate_managed_settings_fragments` | Dev-only | RBAC drift audit for managed settings. |
| `grade_outcome_with_rubric` | Dev-only | Evaluation harness tool for developer tests/evals. |
| `emit_event` | Dev-only | Append-only lineage primitive should be internal telemetry. |
| `events_log_rotate` | Dev-only | Retention maintenance. |
| `negotiate_sprint_contract` | Disable-by-default | Contract negotiation writes state and can be classifier-sensitive; not default one-developer Studio flow. |
| `apply_edit_function` | Disable-by-default | Protected mutation proposal; enable only behind approved UI and governance preflight. |
| `commit_edits` | Disable-by-default | Protected mutation commit; require dry-run, approval, and governance decision. |
| `research_library_refresh` | Disable-by-default | Refreshes local research state and capability metadata marks external egress. |

Delete candidates: no live public MCP tool should be deleted solely from this read-only audit. The strongest delete candidate is not a live MCP tool: `ontology_context_query_legacy`, after existing internal callers are migrated. Removed public tools should stay in `_deprecation-map.ts` as compatibility evidence.

## Runtime Separation Implications

- `.codex-plugin/plugin.json` points Codex to `.mcp.json`; `.mcp.json` launches the server with `PALANTIR_MINI_HOST_RUNTIME=codex`. That is the Codex runtime MCP registration surface.
- `managed-settings.d/50-palantir-mini.json` says it is loaded by Claude Code into effective permission policy. It is evidence of intended RBAC, but it does not by itself constrain Codex MCP exposure.
- Current public `tools/list` cannot express runtime profiles. A Codex client sees the 31 public tools unless the plugin/server adds filtering or installs a narrower MCP server profile.
- Source/runtime separation docs require editing the source checkout and reinstalling/restarting Codex after MCP changes. A tool-surface change is not active until Codex reloads the plugin/MCP server.
- Because MCP-first evidence is emitted only at server dispatch, hiding raw context tools without replacing the evidence mechanism would break hooks that expect `get_ontology`, `impact_query`, or `pre_edit_impact` evidence in project events.
- Claude managed-settings names use `mcp__palantir-mini__*`, while Codex-exposed tool names in this runtime can appear under `mcp__palantir_mini__*`. Policy generation should not assume one runtime naming convention is universal.

## Proposal Implications

- Define an explicit MCP profile for one-developer local AIP Chatbot Studio: public core should be about 7 tools (`pm_semantic_intent_gate`, `pm_ontology_engineering_workflow`, `pm_intent_router`, `ontology_context_query`, `pm_pre_mutation_governance`, `compute_edits_dry_run`, `ontology_schema_get`) plus optional gated protected-action tools.
- Promote capability metadata into the served MCP surface or a generated manifest: audience, lifecycle, effect, mutation kind, external egress, DTC requirement, and replacement should not live only in a TypeScript registry invisible to `tools/list` consumers.
- Generate managed-settings MCP allowlists from the same capability registry rather than hand-maintaining a broad allowlist. At minimum, split public-core, dev-only, and disable-by-default fragments.
- Add a stable Studio projection tool or fold `pm_semantic_workbench_state` into `ontology_context_query`/`pm_semantic_intent_gate` output. The current public palette exposes lower-level governance primitives but not the end-user workbench state shape.
- Register or intentionally retire `pm_semantic_consistency_gate`. It exists as a handler, and semantic consistency state exists in `SemanticConversationState`, but the live MCP surface has no explicit semantic-consistency gate tool.
- Preserve raw MCP-first compatibility while reducing surface area by letting `ontology_context_query` and/or `pm_pre_mutation_governance` emit the same MCP-first evidence currently tied to `get_ontology`, `impact_query`, and `pre_edit_impact`.
- Keep release, rule, runtime parity, source authority, surface contract, and managed-settings audits dev-only. They are valuable for plugin maintainers but create noise and accidental authority for a local Studio user.
- Keep `apply_edit_function`, `commit_edits`, `negotiate_sprint_contract`, and `research_library_refresh` disable-by-default. They change project, contract, event, or local research state and should require explicit user action in any Studio UI.

## Open Questions

- Should the default Codex MCP server support profiles, for example `PALANTIR_MINI_MCP_PROFILE=studio-core|dev-full`, or should profiles be separate `.mcp.json` entries?
- Is `pm_semantic_workbench_state` intended to become the public Chatbot Studio state tool once stable, or should its projection be embedded into existing gate/context responses?
- Is `pm_semantic_consistency_gate` intentionally unregistered, or is it a missed public core addition for semantic promotion readiness?
- Should `get_ontology`, `impact_query`, and `pre_edit_impact` remain public only because of MCP-first hook evidence, or can that evidence be emitted by a smaller context/governance tool set?
- Should managed settings ask/deny rules cover `apply_edit_function`, `research_library_refresh`, `events_log_rotate`, and contract negotiation, not only `commit_edits` ship-merge and `get_ontology` security reads?
- Which tools are intended to be LLM-callable versus runtime-internal telemetry or maintainer commands in a one-developer local Studio?

## Confidence And Gaps

Confidence: medium-high for live inventory and classification direction. The live MCP server, managed settings allowlist, and capability registry all confirm 31 current live tools; handler inventory confirms substantially more internal/legacy handlers.

Gaps:

- I did not invoke MCP tools or import the MCP server module, so counts are based on file reads and text extraction rather than runtime `tools/list`.
- I did not run tests or self-checks because the contract was read-only evidence plus the assigned report.
- Classification is proposal-oriented for the one-developer local AIP Chatbot Studio target, not a usage telemetry analysis.
- I did not inspect Codex cache payloads or active runtime config because the source authority and opt-out contract made those consumer evidence only.
