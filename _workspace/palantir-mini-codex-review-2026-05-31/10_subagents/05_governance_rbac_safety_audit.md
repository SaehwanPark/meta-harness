# Governance RBAC Safety Audit
## Scope

This audit reviewed governance, RBAC, and safety surfaces in the reviewed source authority, with `PM_ROOT` meaning `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini`. The harness project was `/home/palantirkc/meta-harness`.

The review used only local read-only evidence plus the meta-harness handoff contract. I did not use palantir-mini MCP tools, palantir-mini skills, palantir-mini routing, or palantir-mini workflow state. The only write was this assigned report.

## Files And Sources Read

- `/home/palantirkc/meta-harness/AGENTS.md` content provided in the prompt, including the explicit palantir-mini opt-out for this repository.
- `/home/palantirkc/meta-harness/.agents/skills/harness/SKILL.md`.
- `/home/palantirkc/meta-harness/docs/harness/README.md`.
- `/home/palantirkc/meta-harness/_workspace/palantir-mini-codex-review-2026-05-31/00_input/palantir-mini-opt-out-protocol.md`.
- `PM_ROOT/.codex-plugin/plugin.json`.
- `PM_ROOT/.mcp.json`.
- `PM_ROOT/managed-settings.d/50-palantir-mini.json`.
- `PM_ROOT/schemas/pm-pre-mutation-governance.input.schema.json`.
- `PM_ROOT/schemas/governance-decision.output.schema.json`.
- `PM_ROOT/schemas/hooks/governance-hook.output.schema.json`.
- `PM_ROOT/schemas/project-gate-policy.schema.json`.
- `PM_ROOT/contracts/project-gate-policy.contract.json`.
- `PM_ROOT/bridge/handlers/pm-pre-mutation-governance.ts`.
- `PM_ROOT/bridge/handlers/commit-edits.ts`.
- `PM_ROOT/bridge/handlers/pm-workflow-response-validate.ts`.
- `PM_ROOT/bridge/handlers/validate-managed-settings-fragments.ts`.
- `PM_ROOT/bridge/handlers/pm-plugin-self-check/check-managed-settings.ts`.
- `PM_ROOT/bridge/handlers/pm-plugin-self-check/check-workflow-response-template.ts`.
- `PM_ROOT/lib/governance/pre-mutation-governance-v2.ts`.
- `PM_ROOT/lib/governance/pre-mutation-governance.ts`.
- `PM_ROOT/lib/governance/pre-mutation-impact-gate.ts`.
- `PM_ROOT/lib/governance/dtc-surface-policy.ts`.
- `PM_ROOT/lib/governance/policy-compiler.ts`.
- `PM_ROOT/lib/governance/fde-governance-policy.ts`.
- `PM_ROOT/lib/governance/effective-gate-mode.ts`.
- `PM_ROOT/lib/ontology-engineering-response-template.ts`.
- `PM_ROOT/lib/hooks/tool-classifier.ts`.
- `PM_ROOT/lib/codex/codex-hook-adapter.ts`.
- `PM_ROOT/lib/runtime/capability-matrix.ts`.
- `PM_ROOT/lib/hooks/workflow-registry.ts`.
- `PM_ROOT/runtime-overlay/schemas-snapshot/ontology/policies/rbac.ts`.
- `PM_ROOT/lib/rbac/l2-check.ts`.
- `PM_ROOT/lib/rbac/l3-check.ts`.
- `PM_ROOT/hooks/hooks.json`.
- `PM_ROOT/hooks/codex-hooks.json`.
- `PM_ROOT/hooks/commit-edits-governance.ts`.
- `PM_ROOT/hooks/commit-edits-precondition.ts`.
- `PM_ROOT/hooks/ontology-engineering-workflow-enforcement-gate.ts`.
- `PM_ROOT/hooks/pre-edit-impact-mcp-first.ts`.
- `PM_ROOT/hooks/prompt-dtc-enforcement-gate.ts`.
- `PM_ROOT/hooks/stop-validate.ts`.
- `PM_ROOT/docs/CODEX_HOOK_ADAPTER.md`.
- `PM_ROOT/tests/governance/pre-mutation-governance-v2.test.ts`.
- `PM_ROOT/tests/hooks/commit-edits-governance.test.ts`.
- `PM_ROOT/tests/hooks/pre-edit-impact-mcp-first.blocking.test.ts`.
- `PM_ROOT/tests/bridge/handlers/validate-managed-settings-fragments.test.ts`.
- `PM_ROOT/tests/bridge/handlers/pm-workflow-response-validate.test.ts`.
- `PM_ROOT/tests/docs/ontology-engineering-response-template.test.ts`.
- `PM_ROOT/tests/lib/ontology-engineering-response-template.test.ts`.
- `PM_ROOT/tests/runtime-boundary/codex-plugin-hooks.test.ts`.
- `PM_ROOT/tests/integration/codex-prompt-to-dtc-e2e.test.ts`.

## Confirmed Findings

1. `managed-settings.d/50-palantir-mini.json` is a Claude Code managed-settings fragment, but it is packaged inside a Codex-installed plugin and validated by plugin self-checks. It grants broad read access to `~/.claude/**` and `./**`, broad write/edit permissions over Claude rules, Claude project memory, `.palantir-mini/session/**`, scenarios, harness artifacts, generated source, and many MCP tool invocations. This is too broad to be treated as runtime-neutral RBAC authority.

2. The managed settings fragment mixes distinct authorities: Claude filesystem permissions, palantir-mini MCP tool allowlists, project-local generated source edits, harness artifact edits, and shell command permissions. That makes it hard to answer the policy question that matters most: which runtime is allowed to mutate which authority layer.

3. The RBAC schema snapshot does not exactly model the packaged managed settings file. `ManagedSettingsFragment` in `runtime-overlay/schemas-snapshot/ontology/policies/rbac.ts` types `ask` as `string[]`, while the actual managed settings file uses structured ask rules with `match`, `condition`, `risk`, `requires`, and `reason`. The validator is therefore primarily a drift checker, not a full schema-level safety contract.

4. `pm-pre-mutation-governance.input.schema.json` marks only `toolName` as required, while the handler requires either `project` or `projectRoot`. The runtime validation and the published input schema are misaligned. This can make clients believe a governance call is valid while the handler rejects it.

5. `pre-mutation-governance-v2` has a good safety core: it is compute-only, deterministic, treats caller booleans and free-text authorization as audit context only, allows read-only/non-protected operations, denies generated files, denies missing approved DTC for protected mutation, denies incomplete DTC fill, and can deny semantic consistency conflicts and impact-gate failures.

6. The older `pre-mutation-governance.ts` still exists as a passive decision-record builder and is less crisp than v2. It uses wall-clock timestamps in decision IDs and has weaker boundary semantics. Keeping both names active increases policy confusion unless the older surface is clearly deprecated or isolated.

7. `pre-mutation-impact-gate` and `dtc-surface-policy` contain necessary protected-surface checks across files, MCP tools, action types, project surfaces, data actions, release/deploy, and egress. That is a real safety layer and should stay, but it must be applied only when the operation is actually protected or mutating.

8. `policy-compiler.ts` is directionally useful because it turns policy primitives into ordered decisions: read-only allowlist, generated-file denial, outside-root denial, forbidden patterns, DTC requirements, known issues, validation packs, workflow traces, fill completeness, and ontology-affecting intent checks. The risk is not the compiler itself; the risk is over-broad attachment points.

9. `fde-governance-policy.ts` correctly captures the higher bar for protected mutation: approved DTC, optional human approval reference, no open blocking decisions, required review domains closed, and no open DTC risks. That should be retained for real ontology-affecting mutation, release, external command, and commit/pull-request boundaries.

10. `commit-edits-governance.ts` is the right direction for the `commit_edits` MCP boundary. It blocks `PALANTIR_MINI_HARNESS_BYPASS=1`, requires a bound harness contract, requires DTC approval for protected mutation, runs policy/impact gates, grades quick-sprint cases advisory-only, requires dry-run and grading evidence in full mode, and fails closed on invalid input or unhandled errors.

11. `commit-edits-precondition.ts` is now overextended. Although it contains useful older checks, the active hook wiring applies it to raw `Edit`, `Write`, `MultiEdit`, and `NotebookEdit` events. In this review it blocked writing an unrelated meta-harness report because the repository has a `.palantir-mini` marker but no `.palantir-mini/harness` directory, producing a `no-harness-dir` block for a non-palantir-mini review artifact. That is bottleneck-producing overreach.

12. `ontology-engineering-workflow-enforcement-gate.ts` is also overextended when applied to every PreToolUse event. In this review, a read-only `jq` count command against already-read source evidence was blocked because the Codex adapter classifies shell as `Bash`, `jq` is not in the read-only shell allowlist, and the command text referenced protected governance surfaces. A read-only evidence command should not require SIC/DTC/FDE provenance.

13. `tool-classifier.ts` omits common read-only inspection tools such as `jq`. That causes normal JSON inspection to be treated as potentially mutating shell, which then activates heavier workflow gates. This is a small classifier gap with large workflow cost.

14. `pre-edit-impact-mcp-first.ts` encodes a valuable safety invariant: non-small edits in tracked projects should have recent impact evidence. But it is currently dependent on palantir-mini MCP evidence by default and can become a bottleneck for review-only, explicitly opted-out, or non-palantir-mini work. The tests confirm opt-out skip behavior exists, but active Codex prompt capture is not mounted, so relying on stored prompt opt-out state is brittle.

15. `codex-hooks.json` intentionally does not register `SessionStart` or `UserPromptSubmit`, and `docs/CODEX_HOOK_ADAPTER.md` says ordinary Codex sessions have no auto startup context or prompt-front-door capture. Tests confirm the active Codex registry does not auto-capture UserPromptSubmit. Therefore any policy path depending on current prompt-front-door state is not reliable in active Codex unless invoked explicitly by an exposed, supported event.

16. Runtime capability files conflict: `lib/runtime/capability-matrix.ts` lists Codex native events including `SessionStart` and `UserPromptSubmit`, while `lib/hooks/workflow-registry.ts`, `codex-hooks.json`, docs, and tests say those events are unsupported or unmounted in active Codex. RBAC and governance policy should follow the active registry, not the optimistic capability matrix.

17. Response-template enforcement is well-scoped in the explicit validator: `pm-workflow-response-validate` requires governed response fields only when forced or when the prompt text requires it, and explicit opt-out prompts are treated as not requiring the full workflow template. The template also checks runtime-gap disclosure, SSoT basis, plain-language explanation, false parity claims, and DTC approval-card quality. This is a necessary safety surface for user-visible governance claims.

18. Stop-hook response validation is best-effort because the hook can only validate response text when the runtime payload exposes it. That is the right boundary: do not pretend Stop hooks can enforce text that the runtime does not provide.

19. `l2-check.ts` checks token shape, expiry, scope, and signature presence but does not cryptographically verify signatures. This is acceptable only as a local deterministic precheck or advisory layer. It should not be represented as strong RBAC enforcement.

20. `l3-check.ts` attempts to read a TypeScript schema snapshot path as JSON and returns empty marking rules on parse failure. Its default behavior allows public access when no marking is found. That may be acceptable for demo/local use, but it is not a strong marking-based policy enforcement path.

## Safety vs Bottleneck Separation

Necessary safety:

- Keep compute-only pre-mutation governance v2 for protected mutation decisions.
- Keep generated-file direct-edit denial, outside-root denial, forbidden-pattern denial, semantic consistency conflict denial, and protected-surface DTC matching.
- Keep strict `commit_edits` governance for actual ontology edits, release/deploy, external commands, data egress, pull request, and commit boundaries.
- Keep response-template validation for governed palantir-mini workflow answers and DTC approval-card claims.
- Keep managed-settings drift checks, but scope them to the runtime they actually govern.
- Keep runtime-gap disclosure where the runtime lacks prompt text, lifecycle events, or hook payloads.

Bottleneck-producing overreach:

- Applying ontology/FDE/SIC/DTC enforcement to all PreToolUse events, including read-only evidence gathering.
- Applying `commit-edits-precondition.ts` to raw file edits in any repo that merely has a `.palantir-mini` marker, even when the task is explicitly opted out and the target is a meta-harness review artifact.
- Treating a prompt-front-door/DTC continuity check as mandatory in active Codex while UserPromptSubmit is intentionally unmounted.
- Requiring palantir-mini MCP evidence for non-palantir-mini review work or for explicitly opted-out review artifacts.
- Classifying read-only JSON inspection with `jq` as mutating shell.
- Treating the broad Claude managed-settings fragment as if it were runtime-neutral authority for Codex or Gemini.

## Keep / Merge / Disable / Delete Table

| Surface | Recommendation | Rationale |
| --- | --- | --- |
| `pre-mutation-governance-v2` | Keep | Strong compute-only governance core with deterministic decisions and correct treatment of free-text/caller booleans as non-authorizing evidence. |
| `pm-pre-mutation-governance` input schema | Merge/fix | Align required fields with handler reality by requiring `project` or `projectRoot` using schema-level conditional validation. |
| `pre-mutation-governance.ts` legacy builder | Disable or deprecate | Passive legacy shape overlaps v2 and weakens clarity unless retained only for migration compatibility. |
| `pre-mutation-impact-gate` and `dtc-surface-policy` | Keep | Correct protected-surface matching layer, but attach only to protected mutation paths. |
| `policy-compiler.ts` | Keep | Useful ordered policy compiler; the issue is where it is invoked, not the rule model itself. |
| `fde-governance-policy.ts` | Keep | Appropriate high bar for protected mutation, release, external command, and proposal execution. |
| `commit-edits-governance.ts` | Keep | Correct primary boundary for `commit_edits`; denies bypass, requires contract/DTC/dry-run/grading evidence, fails closed. |
| `commit-edits-precondition.ts` commit-edits branch | Merge into `commit-edits-governance` or delete | Duplicate/older behavior conflicts with the newer boundary and includes bypass semantics that the new hook correctly denies. |
| `commit-edits-precondition.ts` raw edit branch | Disable by default or narrow | Currently blocks unrelated opted-out review artifacts in tracked repos; should apply only to protected palantir-mini source surfaces or explicit governed sessions. |
| `ontology-engineering-workflow-enforcement-gate.ts` | Narrow | Do not run hard provenance checks for read-only commands or opted-out review artifacts. Gate only protected mutation/routing/authoring surfaces. |
| `pre-edit-impact-mcp-first.ts` | Keep but scope | Valuable for non-small protected edits; should honor explicit local opt-out and not require MCP-first evidence for non-palantir-mini review tasks. |
| `prompt-dtc-enforcement-gate.ts` | Keep advisory/scoped by default | Good continuity policy when prompt-front-door evidence exists; unsafe to make broadly blocking in active Codex without UserPromptSubmit. |
| `tool-classifier.ts` read-only shell allowlist | Merge/fix | Add read-only tools such as `jq` or classify shell by effect more accurately. |
| `managed-settings.d/50-palantir-mini.json` | Split | Separate Claude managed-settings authority from Codex plugin runtime policy and from palantir-mini MCP allowlists. |
| `validate-managed-settings-fragments` | Keep | Useful drift checker, but should validate against runtime-specific schemas. |
| RBAC schema snapshot | Merge/fix | Update to model structured ask rules or stop claiming it schemas the current managed settings file. |
| `l2-check.ts` | Keep as advisory only | Shape/expiry/scope/signature-presence check is useful but not cryptographic authorization. |
| `l3-check.ts` | Fix or disable as enforcement | Default TS-as-JSON registry path and public-on-missing behavior are too weak for strong marking enforcement. |
| Response-template validator | Keep | Strong, well-scoped check for governed user-visible claims and runtime-gap disclosure. |
| Stop response validation | Keep best-effort | Correctly avoids claiming enforcement when runtime payload lacks assistant response text. |
| Codex capability matrix event claims | Merge/fix | Must match active hook registry and tests: SessionStart/UserPromptSubmit are not mounted in active Codex. |

## Runtime Separation Implications

Claude, Codex, and Gemini should have separate RBAC and policy authority instead of sharing one broad managed-settings artifact.

Claude:

- Claude managed settings can remain the authority for Claude filesystem permissions, Claude MCP exposure, Claude hooks, and Claude-specific ask/allow/deny policy.
- Claude-local settings should not be packaged as generic palantir-mini runtime authority unless clearly labeled as Claude-only.
- Claude project memory, `.claude/rules`, `.claude/agents`, and `.claude/hooks` permissions should remain Claude runtime facts, not Codex or Gemini facts.

Codex:

- Codex authority should come from `.codex-plugin/plugin.json`, `.mcp.json`, `codex-hooks.json`, Codex hook adapter behavior, Codex config, and Codex runtime docs.
- Codex policy must reflect that SessionStart and UserPromptSubmit are not currently mounted. Prompt-front-door-dependent governance cannot be mandatory unless Codex explicitly captures the prompt through a supported event or direct user-approved workflow call.
- Codex should treat Claude managed-settings files as source evidence for Claude compatibility, not as native RBAC enforcement.
- Codex hook policy should distinguish read-only inspection, review-artifact writes, protected source mutation, generated-file mutation, commit/PR/release mutation, and external egress.

Gemini:

- Gemini install/package surfaces are absent in the reviewed source. Therefore Gemini should have no implied palantir-mini RBAC authority from Claude managed settings or Codex plugin registration.
- Any Gemini policy should be introduced as a separate runtime-native adapter/manifest with explicit unsupported-surface disclosures.

Cross-runtime:

- Provider identity must be metadata, not semantic authority.
- DTC/SIC/FDE concepts may define semantic policy, but enforcement has to bind through runtime-native surfaces that actually exist.
- A runtime that cannot capture a prompt, response text, lifecycle event, or permission request must disclose that gap and fall back to advisory or explicit user-driven validation, not pretend parity.

## Proposal Implications

- Split `managed-settings.d/50-palantir-mini.json` into runtime-specific policy artifacts: Claude managed settings, Codex plugin policy/hook exposure, and any future Gemini policy. Keep a small cross-runtime semantic policy document only for concepts such as protected mutation, DTC approval, generated-file denial, and response-claim requirements.

- Make `commit-edits-governance.ts` the single blocking authority for `commit_edits`. Move any still-needed logic from `commit-edits-precondition.ts` into the newer hook, then retire the commit-edits branch in the older file.

- Narrow raw edit governance to target protected mutation surfaces, not repository presence. A `.palantir-mini` directory alone should not make every file edit in that repository require a bound harness contract.

- Add an explicit review-artifact allow path for meta-harness `_workspace/.../10_subagents/*.md` outputs when the task is operating under the opt-out review contract. This should not grant authority to mutate source, caches, sessions, or runtime policy.

- Update the shell classifier to recognize read-only JSON and file inspection commands such as `jq` as read-only when no redirection, write flag, network call, or command substitution with mutation is present.

- Fix schema/handler mismatches for `pm-pre-mutation-governance`, especially the required project/projectRoot condition.

- Update or separate RBAC schemas so the structured `ask` rules in managed settings are schema-backed. If not, label the current schema as a simplified snapshot rather than authoritative validation.

- Reconcile Codex capability documentation: active registry, `codex-hooks.json`, docs, and tests should be the authority over unsupported lifecycle events. The capability matrix should not claim active Codex support for SessionStart/UserPromptSubmit unless those events are actually mounted.

- Keep response-template enforcement as a user-visible claim safety layer, but do not apply it to explicit opt-out prompts or ordinary non-palantir-mini responses.

## Open Questions

- Should Claude managed-settings files continue to ship inside the Codex plugin payload, or should they move to a Claude-only packaging/export path?

- What is the desired native Codex replacement for prompt-front-door continuity if UserPromptSubmit remains unmounted?

- Should review-only meta-harness artifacts receive a first-class policy category distinct from source mutation and generated artifact mutation?

- Is `l2-check.ts` intended to become cryptographic verification, or should it be renamed/documented as a shape and expiry precheck only?

- Is `l3-check.ts` supposed to load a generated JSON registry rather than a TypeScript schema snapshot path?

- Which runtime owns final approval for broad MCP allowlists: palantir-mini semantic policy, Codex plugin manifest, Claude managed settings, or per-project policy fragments?

## Confidence And Gaps

Confidence is high for the main governance conclusions because the reviewed files, hook wiring, schemas, and tests consistently show the same pattern: strong protected-mutation safety exists, but several active hooks are attached too broadly and create review/read-only/edit bottlenecks.

Gaps:

- I did not run palantir-mini MCP tools, palantir-mini skills, or palantir-mini routing by instruction.
- I did not mutate or test the reviewed source authority.
- I did not run the full test suite; this was a read-only audit plus one report write.
- I reviewed representative governance/RBAC/safety files and tests, not every file in the plugin.
- One attempted read-only `jq` count was blocked by active hook enforcement; the MCP allow count was derived manually from the already-read JSON lines.
