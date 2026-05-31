# Runtime Hooks Bottleneck Audit

## Scope

Audited the Codex hook/runtime surface for `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini` from `/home/palantirkc/meta-harness`, under the opt-out review contract. This report is the only file written.

Covered hidden fan-out, timeout accumulation, matcher expansion, fail-closed/advisory behavior, prompt opt-out gaps, and lifecycle mismatch. No plugin tools, routing, source edits, cache edits, generated-file edits, or session edits were used.

## Files And Sources Read

- `/home/palantirkc/meta-harness/.agents/skills/harness/SKILL.md`
- `/home/palantirkc/meta-harness/_workspace/palantir-mini-codex-review-2026-05-31/00_input/palantir-mini-opt-out-protocol.md`
- `/home/palantirkc/meta-harness/_workspace/palantir-mini-codex-review-2026-05-31/00_input/palantir-mini-opt-out.env`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/hooks/codex-hooks.json`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/hooks/hooks.json`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/codex/codex-hook-adapter.ts`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/runtime/capability-matrix.ts`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/hooks/tool-classifier.ts`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/docs/CODEX_HOOK_ADAPTER.md`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/tests/runtime-boundary/codex-plugin-hooks.test.ts`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/tests/lib/codex/codex-hook-adapter.test.ts`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/tests/hooks/hook-contracts.test.ts`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/tests/hooks/hooks-json-conditional-if.test.ts`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/tests/lib/hooks/timeout-policy.test.ts`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/tests/bridge/handlers/pm-plugin-self-check.test.ts`

## Confirmed Findings

1. Codex hook registration looks small, but actual execution fans out through the adapter. `codex-hooks.json` registers one adapter command per mounted lifecycle event, usually with broad matchers and a 225 second outer timeout. The adapter then live-reads `hooks.json` and expands a single Codex event into every matching shared command. The timeout-policy test expects the current shared registry to contain 69 command hooks.

2. Matcher expansion is broad. The adapter maps `apply_patch` to `Edit`, `Write`, `MultiEdit`, and `NotebookEdit`; maps `functions.exec_command` and `functions.write_stdin` to `Bash`; maps Codex agent spawn to `Agent`; adds palantir-mini MCP aliases; and adds paths plus command text as candidates. One Codex tool call can therefore match more groups than the native tool name suggests.

3. Timeout accumulation can exceed the outer adapter timeout. Async hooks are started and ignored for the returned decision, while sync hooks are awaited sequentially. Several common edit-path sync hooks carry 25-50 second budgets, while compact and stop lifecycle hooks include 75-100 second budgets. The summed sync budget can approach or exceed the 225 second Codex wrapper timeout.

4. `PermissionRequest` replays shared `PreToolUse` policy. Docs and tests confirm that the adapter maps this wire event to the shared pre-tool policy while returning Codex permission response shape. This is useful for protected decisions, but it can duplicate or extend pre-tool latency.

5. Blocking behavior is mixed. The adapter blocks on explicit deny/block responses, exit code `2`, selected schema mismatches, `failureMode: "fail-closed"`, and `permissionDecision: "deny"`. Async hooks are advisory for the response path but can still consume resources and produce side effects.

6. Prompt opt-out is not consistently available to later lifecycle events. The adapter supports direct prompt opt-out and stored prompt-front-door state, but checked-in Codex registration intentionally omits `UserPromptSubmit` and `SessionStart`. Docs and tests assert that omission. Later pre-tool calls may therefore lack the stored opt-out state they need.

7. The gap was observed during this review. Read-only summary command shapes using `jq`, `node -e`, and `nl -ba ... hooks.json` were blocked by the installed PreToolUse gate despite the explicit opt-out sentence. Sourcing the provided opt-out env inside the shell command did not help for those cases because the hook runs before the shell command executes. Plain `sed`, `find`, and selected `rg` reads were allowed.

8. Source capability and mounted runtime behavior are not the same thing. The capability matrix and adapter tests include events that the checked-in Codex registry does not mount. Proposal language should separate adapter support, source registry mounting, and current installed runtime behavior.

## Bottleneck Evidence

- `codex-hooks.json` mounts adapter commands for `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `SubagentStart`, `SubagentStop`, and `Stop`, all with `timeout: 225`.
- `codex-hooks.json` uses broad matchers for high-frequency lifecycle events.
- `hooks.json` contains a broad first PreToolUse workflow gate and multiple edit-governance commands.
- `hooks.json` PreCompact includes two synchronous blocking commands with 100 and 75 second budgets plus async advisories.
- `hooks.json` Stop includes five commands with 40, 75, 100, 40, and 75 second budgets.
- `tests/lib/hooks/timeout-policy.test.ts` verifies 69 command hooks and no forbidden heavy broad audit commands.
- `tests/bridge/handlers/pm-plugin-self-check.test.ts` verifies hook policy shape but not user-visible latency.
- `tests/lib/codex/codex-hook-adapter.test.ts` covers opt-out behavior, fail-closed denial, matcher aliasing, PermissionRequest bridging, and Stop blocking behavior.

## Keep / Merge / Disable / Delete Table

| Surface | Action | Rationale |
| --- | --- | --- |
| `codex-hooks.json` delegation registry | Keep | It preserves runtime-specific entrypoints without forking shared policy. |
| Adapter live-read of `hooks.json` | Keep | Source authority stays centralized; the issue is lack of budget and visibility controls. |
| Matcher alias bridge | Keep with guardrails | Compatibility is useful, but expanded candidates need diagnostics and fan-out limits. |
| Prompt opt-out path | Merge fix | Downstream events need a pre-tool-visible opt-out source, not only prompt capture from an unmounted event. |
| `UserPromptSubmit` mounting policy | Merge decision | Either mount a tiny capture-only entrypoint or remove claims that prompt capture protects later hooks. |
| Broad PreToolUse workflow gate | Disable or narrow for opted-out review tasks | It blocked local read-only audit commands under explicit opt-out. |
| `PermissionRequest` bridge | Narrow | Use it for protected permission decisions, not as a full duplicate of all pre-tool checks. |
| Total timeout policy | Merge fix | Add a per-event total budget below 225 seconds and return structured partial results before runtime kill. |
| Async advisories | Merge fix | Cap count/time and skip under explicit opt-out. |
| Existing hook files | Delete none | The safer change is registry narrowing and tests, not direct deletion. |

## Runtime Separation Implications

There are three different facts that must not be collapsed:

- Adapter capability: what `codex-hook-adapter.ts` can handle when invoked.
- Source registry mounting: what `codex-hooks.json` asks Codex to invoke.
- Current installed runtime behavior: what actually fires before commands and edits.

The current review showed that installed hooks can still affect an explicitly opted-out meta-harness task. Prompt-level opt-out is only reliable if the hook process can see it before matcher expansion and before the shell command starts.

The installed Codex cache was not inspected, so source/cache drift remains possible.

## Proposal Implications

- Treat hook runtime behavior as a bottleneck surface, not just a policy list.
- Require a deterministic match report for hook changes: event, tool, candidates, matched commands, sync/async split, summed sync timeout, and block-capable hooks.
- Put opt-out handling before shared-registry fan-out.
- Add an adapter-level total budget below the outer Codex timeout.
- Keep review-only meta-harness work out of plugin workflow enforcement unless the user opts back in.
- Do not claim prompt opt-out persistence unless mounted hooks and a runtime smoke test prove it.

## Open Questions

- Should Codex remount `UserPromptSubmit` as capture-only with a tiny timeout?
- Should review opt-out be visible as runtime env before PreToolUse, rather than shell-sourced env?
- Which pre-tool groups must remain synchronous and fail-closed outside the plugin source repo?
- Should `PermissionRequest` run all pre-tool policy or only permission-specific policy?
- What maximum latency is acceptable for PreToolUse, PostToolUse, Stop, and compact events?
- Should read-only classification include `jq`, `node -e` JSON summaries, and sourced-env prefixes for audit work?
- Does the installed Codex cache exactly match the reviewed source after the recent opt-out PR?

## Confidence And Gaps

Confidence is high for source-level findings about fan-out, matcher expansion, timeout accumulation, and blocking behavior because they are directly supported by source, docs, and tests.

Confidence is medium-high for the prompt opt-out lifecycle gap because the source registry omits the prompt event, tests assert that omission, and this review observed pre-tool blocks despite explicit opt-out.

Gaps:

- No plugin MCP tools, skills, routing, source edits, cache edits, generated-file edits, or session edits were used.
- No tests were executed; evidence is read-only inspection plus observed hook blocks.
- Installed cache/source drift was not checked.
- Exact aggregate counts by event were not computed because JSON summary commands were blocked by the active PreToolUse gate.
