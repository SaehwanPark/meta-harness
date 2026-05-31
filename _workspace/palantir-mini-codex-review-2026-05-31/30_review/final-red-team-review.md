# Final Red-Team Review

Review workspace: `/home/palantirkc/meta-harness/_workspace/palantir-mini-codex-review-2026-05-31`

Reviewed proposal: `_workspace/palantir-mini-codex-review-2026-05-31/final/palantir-mini-local-aip-chatbot-studio-proposals.md`

Boundary: this review used the meta-harness review contract and local read-only evidence only. It did not use palantir-mini MCP tools, palantir-mini skills, palantir-mini routing, prompt/DTC gates, or palantir-mini workflow state. The only review write is this report file.

## Lead/Orchestrator Boundary Check

Pass. The updated meta-harness docs clearly say that the Lead orchestrates rather than implements by default:

- `AGENTS.md:11-17` says Leads own context, plan, work contracts, prompts, synthesis, validation, and final decision; bounded work should go to bounded implementers; Lead direct writes are limited to explicit authorization, emergency unblockers, or final synthesis/handoff artifacts; compact context packs and model-by-task-shape selection are required.
- `README.md:41-48` repeats the same collaboration model and model-selection tiers.
- `docs/harness/README.md:11-33` gives the durable role/handoff contract, compact context guidance, and model-selection rules, including the warning against pairing full-history forks with explicit model overrides.

## Blockers

None.

I did not find a proposal defect that invalidates the review package outright. The proposal is directionally well supported by the subagent reports and the synthesis matrix. However, the High findings below should be fixed before asking the user to approve the implementation plan.

## High

1. Validation gates mix existing tests with future/nonexistent tests without labeling them.

   Evidence: the proposal lists immediate-looking validation commands for runtime adapter contracts and Chatbot Studio core tests at `final/palantir-mini-local-aip-chatbot-studio-proposals.md:317-331`. A local read-only file-existence check found these paths missing in the reviewed source:

   - `tests/runtime-boundary/runtime-adapter-manifest.test.ts`
   - `tests/runtime-boundary/runtime-hook-compilation.test.ts`
   - `tests/runtime-boundary/runtime-tool-profiles.test.ts`
   - `tests/runtime-boundary/prompt-state-isolation.test.ts`
   - `tests/lib/chatbot-studio/declaration.test.ts`
   - `tests/lib/chatbot-studio/session-state.test.ts`
   - `tests/lib/chatbot-studio/tool-surface.test.ts`
   - `tests/lib/chatbot-studio/eval-surface.test.ts`

   This is understandable because the proposal is specifying future PR gates. The risk is presentation: user approval could mistake those commands for currently runnable verification. The reports also consistently state that no implementation tests were executed during this read-only review (`10_subagents/07_deletion_and_pr_sequence.md:404-407`, `10_subagents/09_runtime_adapter_target_design.md:323-328`).

   Required fix: split validation into `existing runnable gates now`, `tests each PR must add`, and `runtime smoke gates after reinstall/restart`. Do not list missing future tests as baseline commands without marking them as new acceptance artifacts.

2. The PR ordering needs one explicit reconciliation between "build Studio core first" and "reduce exposure first."

   Evidence: the Core Recommendation says to build a small local Chatbot Studio core inside `lib/chatbot-studio/`, then reduce default runtime exposure around it (`final/...proposals.md:17-23`). The staged PR sequence defers Chatbot Studio data-core work until PR 6, after hotfix freeze, status metadata, MCP profiles, hook/governance narrowing, skills/agents shrink, and runtime separation contracts (`final/...proposals.md:221-265`). Report 06 recommends data-only declarations/builders/tests first and adapters only after the pure core is stable (`10_subagents/06_one_dev_local_architecture.md:124-130`). Report 07 recommends hotfix, metadata/profile narrowing, hook/governance narrowing, skill/agent reduction, runtime separation, then deletion (`10_subagents/07_deletion_and_pr_sequence.md:283-303`).

   This is not a conceptual contradiction, but the plan needs to say which dependency wins for the first implementation train. Otherwise the next implementer may reorder PRs in a way that either delays the actual local Studio value too long or exposes the new core through the old oversized surface.

   Required fix: add a short dependency note: either "PRs 0-5 are exposure-control prerequisites before building the Studio core" or "PR 1 adds the data core before runtime exposure work; later PRs narrow exposure around it." Pick one ordering and make the rationale explicit.

## Medium

1. Source-complete hotfix status is correctly disclosed, but approval should require active-runtime proof.

   Evidence: the proposal says the Codex hook hotfix is source-visible and that active Codex still needs plugin reinstall/reload plus process restart (`final/...proposals.md:13-15`, `334-341`, `365-366`). Reports also warn that installed cache/source drift was not checked or not treated as authority (`10_subagents/02_runtime_hooks_bottleneck_audit.md:81-82`, `10_subagents/07_deletion_and_pr_sequence.md:404-407`, `10_subagents/09_runtime_adapter_target_design.md:323-327`).

   Required before approval: the proposal should add an explicit approval boundary: "source plan approval does not mean active runtime behavior is fixed until reinstall/restart smoke evidence proves the mounted hook manifest, MCP profile, and skill surface."

2. The title phrase "Local One-Developer AIP Chatbot Studio Equivalent" is a little stronger than the body.

   Evidence: the body is careful: it says the proposal is local, one-developer-scale, and does not claim Foundry SaaS/security/Workshop/API/Marketplace parity (`final/...proposals.md:7`, `44`, `352-370`). Report 01 also requires local emulation rather than Palantir feature parity (`10_subagents/01_official_aip_chatbot_studio_surface.md:70-89`, `111-116`, `132-136`).

   Risk: the word `Equivalent` can be read as parity if the title is separated from the non-goal section. Prefer "Local AIP Chatbot Studio-Style Control Plane" or "Local AIP Chatbot Studio Analogue."

3. Unregistered semantic workbench/consistency handlers should be named in the deletion/default-off plan.

   Evidence: Report 03 calls out `pm_semantic_workbench_state` and `pm_semantic_consistency_gate` as relevant but not live public MCP tools (`10_subagents/03_mcp_tool_surface_audit.md:50-54`, `118-120`). Report 07 lists them as deletion candidates only after keep/register/retire decisions (`10_subagents/07_deletion_and_pr_sequence.md:264-270`). The final proposal mentions generic unregistered handlers only at PR 8 (`final/...proposals.md:273-276`).

   Required before implementation, not necessarily before conceptual approval: name those two handlers directly in the PR sequence and require a keep/register/retire decision before physical deletion.

## Low

1. The proposal's "only intended writes" sentence is local to synthesis and will be stale once this red-team report exists.

   Evidence: `final/...proposals.md:11-12` says the intended writes are the final proposal and evidence matrix. That was true for the synthesis artifact, but the complete review package now includes this assigned review report. This is harmless, but future readers may misread it.

2. The exact seven-tool `studio-core` default is well supported, but the acceptance criteria for changing it should be explicit.

   Evidence: the seven-tool default is supported by the evidence matrix (`20_synthesis/evidence-matrix.md:17-19`) and Report 03 (`10_subagents/03_mcp_tool_surface_audit.md:66-102`, `113-123`). The proposal should add a small rule for when a tool can enter or leave `studio-core`: public-core status, read-only or compute-only effect, no external egress by default, profile metadata visible to clients, and replacement MCP-first evidence where needed.

## Missing Evidence

- No tests were run in this review. The specialist reports explicitly describe read-only evidence plus assigned report writes, not executed implementation validation (`10_subagents/03_mcp_tool_surface_audit.md:133-142`, `10_subagents/07_deletion_and_pr_sequence.md:402-408`, `10_subagents/09_runtime_adapter_target_design.md:323-328`).
- No active Codex reinstall/restart smoke was performed. The proposal correctly states that hook/MCP/skill/manifest changes are not active-session-complete until reinstall/restart (`final/...proposals.md:334-341`, `365-366`).
- No runtime `tools/list` invocation was used for the 31-tool claim; Report 03 grounded the count in local source reads rather than live MCP execution (`10_subagents/03_mcp_tool_surface_audit.md:36-49`, `137-142`).
- The final red-team review did not live-refresh official Palantir documentation because the user required local read-only evidence. Report 01 cites official URLs and Report 06 used local official-doc mirrors, with a stated fetch date gap (`10_subagents/01_official_aip_chatbot_studio_surface.md:17-32`, `158-169`; `10_subagents/06_one_dev_local_architecture.md:223-228`).
- Current Claude and Gemini runtime installations were not verified. Report 08 states that reviewed source currently has Codex-only local install/package support and that Claude/Gemini install/package surfaces are absent or inactive (`10_subagents/08_runtime_separation_audit.md:122-136`, `264-270`).
- Installed Codex cache state was not used as source authority. That is correct for the source/runtime boundary, but active runtime behavior still needs separate smoke evidence before rollout approval (`20_synthesis/evidence-matrix.md:57-61`).

## Final Verdict

Verdict: Revise before user approval.

The proposal is strong enough to continue. It covers the required surfaces: code-level bottlenecks, MCP/Skill/Agent/Hook shrinkage and default-off posture, Claude/Codex/Gemini separation, local one-developer Chatbot Studio architecture, staged PRs, validation gates, non-goals, and reload/reinstall runtime gaps.

The main issue is not the direction. It is approval precision. The plan must distinguish current runnable validation from future test artifacts, reconcile the PR order, and make active-runtime smoke proof a required boundary before anyone treats source changes as live Codex behavior.

## Required Fixes Before User Approval

1. Revise the validation section into three buckets: existing runnable commands, tests to add in each PR, and reinstall/restart runtime smoke gates.
2. Resolve the PR-order ambiguity between "build Studio core first" and "exposure-control cleanup first."
3. Add an explicit user-approval boundary: source-complete does not equal active-runtime-complete until plugin reinstall/restart smoke evidence exists.
4. Soften the title from "Equivalent" to "Studio-style" or "Analogue," or move the non-parity disclosure directly under the title.
5. Name `pm_semantic_workbench_state` and `pm_semantic_consistency_gate` in the PR sequence with keep/register/retire decisions before deletion.
