# One-Developer Local Architecture
## Scope
This report designs a minimal, local, one-developer architecture for representing Palantir AIP Chatbot Studio semantics inside `palantir-mini` without binding the semantics to Claude, Codex, Gemini, OpenAI, Anthropic, or any other provider.

The target is a runtime-neutral local control-plane core that can model:

- chatbot declarations and published-function shape;
- conversation/session state;
- application variables and deterministic application-state updates;
- retrieval context over ontology, document, and function-backed sources;
- tool bindings for actions, object queries, functions, application-variable updates, commands, and request-clarification;
- action/writeback approval boundaries;
- eval/observability/test contracts;
- runtime adapter projections that explain what each runtime can and cannot do.

This is a design-only review artifact. It does not authorize edits to `palantir-mini`, Codex caches, generated files, or `.palantir-mini/session` state.

## Files And Sources Read
- Harness and opt-out contract:
  - `/home/palantirkc/meta-harness/.agents/skills/harness/SKILL.md`
  - `/home/palantirkc/meta-harness/docs/harness/README.md`
  - `/home/palantirkc/meta-harness/_workspace/palantir-mini-codex-review-2026-05-31/00_input/palantir-mini-opt-out-protocol.md`
  - `/home/palantirkc/meta-harness/_workspace/palantir-mini-codex-review-2026-05-31/00_input/palantir-mini-opt-out.env`

- Reviewed source authority:
  - `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/docs/RUNTIME_LAYER_BOUNDARY.md`
  - `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/core/contracts/aip-fde-local-surface.ts`
  - `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/core/contracts/workflow-family-enforcement.ts`
  - `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/chatbot-studio/semantic-conversation-state.ts`
  - `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/chatbot-studio/application-state.ts`
  - `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/chatbot-studio/retrieval-context.ts`
  - `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/chatbot-studio/workbench-state.ts`
  - `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/capability/capability-contract.ts`
  - `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/capability/capability-router.ts`
  - `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/capability-registry/mcp-tool-capability.ts`
  - `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/runtime-overlay/schemas-snapshot/ontology/primitives/aip-agent.ts`
  - `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/runtime-overlay/schemas-snapshot/ontology/primitives/document-corpus.ts`
  - `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/runtime-overlay/schemas-snapshot/ontology/primitives/fde-ontology-build-session.ts`
  - `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/fde-build/readiness-evaluator.ts`
  - `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/fde-build/session-composer.ts`
  - `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/fde-build/gap-report-builder.ts`
  - `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/eval-suites/fde-turn-quality-semantic.json`
  - `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/eval-suites/semantic-consistency-regression.json`
  - `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/eval-suites/prompt-to-dtc-regression.json`
  - `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/tests/lib/chatbot-studio/semantic-conversation-state.test.ts`
  - `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/tests/lib/chatbot-studio/semantic-workbench-state.test.ts`
  - `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/tests/surface/palantir-source-authority.test.ts`

- Local official Palantir documentation mirrors:
  - `/home/palantirkc/.claude/research/palantir-developers/build-with-aip.md`
  - `/home/palantirkc/.claude/research/palantir-foundry/aip/BROWSE.md`
  - `/home/palantirkc/.claude/research/palantir-official/foundry/aip.md`
  - `/home/palantirkc/.claude/research/palantir-official/foundry/architecture-center/aip-architecture.md`
  - `/home/palantirkc/.claude/research/palantir-official/foundry/chatbot-studio/overview.md`
  - `/home/palantirkc/.claude/research/palantir-official/foundry/chatbot-studio/core-concepts.md`
  - `/home/palantirkc/.claude/research/palantir-official/foundry/chatbot-studio/application-state.md`
  - `/home/palantirkc/.claude/research/palantir-official/foundry/chatbot-studio/retrieval-context.md`
  - `/home/palantirkc/.claude/research/palantir-official/foundry/chatbot-studio/tools.md`
  - `/home/palantirkc/.claude/research/palantir-official/foundry/chatbot-studio/chatbots-as-functions.md`
  - `/home/palantirkc/.claude/research/palantir-official/foundry/chatbot-studio/foundry-apis.md`
  - `/home/palantirkc/.claude/research/palantir-official/foundry/chatbot-studio/commands-as-tools.md`
  - `/home/palantirkc/.claude/research/palantir-official/foundry/aip-evals.md`

Key evidence:

- Official Chatbot Studio docs define chatbots as interactive assistants powered by LLMs, the Ontology, documents, and custom tools, deployable internally and externally through SDK/API surfaces.
- Official core concepts name application state, retrieval context, tools, context window, and chatbots-as-functions as first-class concepts.
- Official application-state docs distinguish visible values, deterministic updates, deterministic tool inputs pinned at reasoning-loop start, and LLM-driven application-variable updates.
- Official retrieval docs define ontology, document, and function-backed retrieval context, with function-backed context returning a `retrievedPrompt`.
- Official tools docs enumerate action, object query, function, update application variable, command, request clarification, and legacy ontology semantic search.
- Existing `palantir-mini` code already contains semantic conversation state, application-state projection, retrieval-context projection, workbench projection, capability routing, tool-surface contracts, AIP surface enums, `AIPAgentDeclaration`, document corpus, eval suites, and FDE read-only chatbot/eval review structures.

## Proposed Minimal Architecture
Keep the first implementation slice local and additive inside the existing `lib/chatbot-studio/` family. Do not create a separate runtime stack, do not introduce a provider SDK, and do not replace current `SemanticConversationState`.

Minimal file layout:

```text
plugins/palantir-mini/
  lib/chatbot-studio/
    index.ts
    declaration.ts
    session-state.ts
    tool-surface.ts
    action-surface.ts
    eval-surface.ts
    validators.ts
    application-state.ts
    retrieval-context.ts
    semantic-conversation-state.ts
    workbench-state.ts
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
    semantic-conversation-state.test.ts
    semantic-workbench-state.test.ts
  eval-suites/
    chatbot-studio-local-regression.json
```

The new files should be pure TypeScript data contracts and deterministic builders:

- `declaration.ts`: defines a `ChatbotStudioDeclaration` that specializes existing `AIPAgentDeclaration` semantics for the current product name. It should include `legacyNames` to preserve Agent Studio naming drift, but prose-facing output should prefer AIP Chatbot Studio.
- `session-state.ts`: defines local session and exchange contracts. It should model `sessionRid`, `chatbotId`, message/exchange ids, application-state snapshots, retrieval runs, planned tool invocations, tool results, citations, trace refs, and eval refs.
- `tool-surface.ts`: maps official tool types to local contracts. It should reuse or mirror the existing `ToolSurfaceContract` shape from `workflow-family-enforcement.ts`, not invent a second tool taxonomy.
- `action-surface.ts`: represents action/writeback intent, confirmation policy, submission criteria refs, dry-run/simulation refs, and required approval refs. It must not execute ontology edits.
- `eval-surface.ts`: maps chatbot-as-function and local-function test targets to eval-suite/run artifacts. It should support variance checks, test cases, metrics, and session-trace evidence.
- `validators.ts`: validates additive local contracts and returns stable issue ids. It must not read files, call providers, or mutate project state.

Existing files should be extended, not bypassed:

- `semantic-conversation-state.ts` remains the semantic root for prompt/session meaning, lifecycle, contract refs, ontology activation, selected skills/capabilities, and read-only LLM control.
- `application-state.ts` remains the deterministic application-variable projection layer and already has the correct pinned-loop concept.
- `retrieval-context.ts` remains the local retrieved-prompt projection layer and should gain structured `retrievalRuns` only if the current `retrievedPrompt/sourceRefs` shape is insufficient.
- `workbench-state.ts` remains the human-review projection and should consume the new declaration/session summaries as optional additions.

The one-developer sequence should be:

1. Add data-only declarations and JSON schemas.
2. Add deterministic builders from `SemanticConversationState` to `ChatbotStudioDeclaration`, `ChatbotStudioSessionState`, and `ChatbotStudioEvalSurface`.
3. Add validators and focused tests.
4. Add one local regression eval suite that covers application state, retrieval context, tool planning, action approval, and eval traceability.
5. Only after the pure core is stable, wire adapter-specific surfaces in separate files.

## Data Model And Artifact Contracts
Use schema-versioned JSON-compatible contracts. Avoid model objects, SDK clients, live tool runners, provider messages, or runtime hook payloads in the core data model.

| Artifact | Minimal fields | Authority and behavior |
| --- | --- | --- |
| `ChatbotStudioDeclaration` | `schemaVersion`, `chatbotId`, `apiName`, `displayName`, `legacyNames`, `instructionsRef`, `descriptionRef`, `ontologyScope`, `applicationVariableIds`, `retrievalContextIds`, `toolBindingIds`, `evalSuiteIds`, `deploymentStage`, `sourceAuthorityRefs`, `runtimeProjection` | Local declaration of the chatbot surface. It may reference `AIPAgentDeclaration` but should prefer current Chatbot Studio naming. |
| `ChatbotStudioSessionState` | `sessionRid`, `externalSessionRid?`, `chatbotId`, `status`, `createdAt`, `updatedAt`, `runtime?`, `applicationSnapshotRefs`, `exchangeIds`, `traceRefs`, `approvalRefs`, `evalRunRefs` | Local session ledger. `externalSessionRid` can preserve the Foundry-style `ri.aip-agents..session.{uuid}` without making it the local id authority. |
| `ChatbotStudioExchange` | `exchangeId`, `sessionRid`, `userInput`, `retrievalRunRefs`, `toolPlanRefs`, `toolResultRefs`, `applicationUpdates`, `markdownResponse?`, `citationRefs`, `sessionTraceRef?` | One user turn. Response text is optional because the runtime adapter, not the core, performs model inference. |
| `ChatbotStudioApplicationVariable` | `variableId`, `valueType`, `description`, `visibility`, `sourceStateKind`, `sourceStateId`, `updateAuthority`, `updatePolicy`, `visibleToModel`, `writableByModel`, `currentValue?` | Extends the current local variable model. Default `writableByModel` remains false unless an explicit update-application-variable tool emits a proposal/update event. |
| `ReasoningLoopSnapshot` | `loopId`, `pinnedAt`, `variables`, `sourceExchangeId` | Captures deterministic tool-input pinning. Updates in the same query do not alter pinned inputs. |
| `RetrievalContextBinding` | `retrievalContextId`, `kind`, `inputVariableIds`, `sourceRefs`, `outputVariableIds`, `citationPolicy`, `freshnessPolicy`, `failureBehavior` | Models ontology, document, function-backed, local-research, or session-lineage retrieval. |
| `RetrievalRun` | `retrievalRunId`, `bindingId`, `conversationStateId`, `retrievedPrompt`, `ontologyRefs`, `documentRefs`, `functionRefs`, `sourceRefs`, `citationRefs`, `warnings` | Runtime-neutral retrieved context. For function-backed context, `retrievedPrompt` is the core output. |
| `ToolBinding` | `toolBindingId`, `toolType`, `mode`, `inputSources`, `mutationClass`, `approvalPolicy`, `ontologyRefs`, `actionTypeRid?`, `functionRid?`, `commandRef?`, `applicationVariableIds` | Maps directly to official tool types and existing `ToolSurfaceContract`. `mode` may be `prompted`, `native`, or `adapter-declared`, but selection cannot change semantics. |
| `ToolInvocationPlan` | `toolPlanId`, `toolBindingId`, `exchangeId`, `plannedInputs`, `deterministicInputRefs`, `requiresUserApproval`, `blockedReason?` | Planning-only. Core creates plans; adapters may execute only when their own runtime plus governance allows it. |
| `ActionSurface` | `actionSurfaceId`, `actionTypeRid`, `operationIntent`, `submissionCriteriaRefs`, `confirmationPolicy`, `requiresDtcApproval`, `dryRunRequired`, `auditEvidenceRefs` | Mutating action semantics. No commit/apply token is produced here. |
| `EvalSurface` | `evalSurfaceId`, `suiteId`, `targetKind`, `targetRef`, `testCaseRefs`, `criteriaRefs`, `metrics`, `varianceChecks`, `traceRefs` | Local analogue of AIP Evals. It can target chatbot-as-function or local pure builders. |
| `RuntimeProjection` | `runtime`, `support`, `adapterRefs`, `fallbackObligations`, `unsupportedSurfaceRefs`, `smokeEvidenceRefs` | Explains runtime support without making runtime identity semantic authority. |

Artifact rules:

- Every artifact gets a schema version and stable id prefix.
- Every optional field must be absent-safe.
- The core can produce warnings and plans, but not approvals, commits, provider calls, or UI side effects.
- Tool/action/eval bindings should cite `sourceAuthorityRefs` when they claim Palantir semantics.
- Local official docs are source evidence, not a corpus to republish.

## Runtime-Neutral Core Boundary
The core boundary should be:

```text
local source evidence
  -> runtime-neutral Chatbot Studio contracts
  -> deterministic builders and validators
  -> runtime adapter projections
  -> optional runtime-specific execution outside the core
```

Rules:

- `lib/chatbot-studio/*.ts` core files should not import Codex, Claude, Gemini, MCP server handlers, hook payloads, provider SDKs, Playwright, browser APIs, or filesystem helpers.
- The core accepts structured inputs such as `SemanticConversationState`, `CapabilityContract`, `AIPAgentDeclaration`, `DocumentCorpus`, and eval-suite JSON.
- The core returns structured outputs such as declarations, session state, retrieval runs, tool plans, action surfaces, eval surfaces, and validation issues.
- Runtime adapters may translate Codex, Claude, Gemini, API, or app events into the core input shape. They cannot alter the meaning of `SemanticIntentContract`, `DigitalTwinChangeContract`, application variable authority, retrieval context, or action approval.
- Provider identity is metadata. It may affect tool-call mechanics or stream shape, but it must not affect whether a tool is mutating, whether a variable is writable, whether an approval is required, or whether an eval passes.
- Native tool calling and prompted tool calling are execution modes, not separate semantic taxonomies.
- Command tools should be represented as contracts first. Real app pairing, browser state, and Workshop/AIP Assist embedding should stay adapter/platform work.
- Action tools are always gated by local governance contracts. A chatbot declaration can say an action is available; it cannot authorize the action.

The existing runtime boundary doc already states that provider identity must not affect the meaning of semantic contracts, DTCs, resolver output, release gates, or ontology primitives. This proposal applies that same rule to Chatbot Studio declarations, sessions, tool plans, retrieval runs, and eval surfaces.

## Must-Have / Later / Non-Goal Table
| Area | Must-have | Later | Non-goal |
| --- | --- | --- | --- |
| Naming | Use `AIP Chatbot Studio` and retain `legacyNames` for Agent Studio/AIP Agents. | Automated naming drift audit in release gates. | Rewriting all historical file names that intentionally preserve legacy slugs. |
| Declaration | `ChatbotStudioDeclaration` or a strict wrapper around `AIPAgentDeclaration`. | Migration helper from existing declarations. | A second unrelated agent registry. |
| Session | Local session/exchange state with optional external RID. | Import/export from Foundry session APIs. | Live Foundry session creation in the core. |
| Application state | Visible/hidden variables, deterministic update policy, pinned loop snapshots. | More variable types after evidence. | Default LLM write authority over readiness or approvals. |
| Retrieval | Ontology, document, function-backed, local-research/session-lineage bindings. | Real vector index adapters. | Live embedding service or provider-specific RAG implementation. |
| Tools | Official tool taxonomy mapped to local `ToolSurfaceContract`. | Native tool-call adapter optimizations. | Treating native tool calling as semantic authority. |
| Actions | Action/writeback contracts with confirmation and DTC requirements. | Dry-run simulation summaries per ActionType. | Auto-committing ontology edits from chatbot output. |
| Commands | Declaration-only command tool contracts with approval policy. | Workshop/AIP Assist/app-pairing adapter. | Browser UI automation in the core. |
| Evals | Local eval surface with suite, target, criteria, metrics, variance, trace refs. | Dashboard/report rendering. | Claiming production-quality model performance without repeated eval runs. |
| Observability | Session trace refs, tool-plan refs, eval-run refs. | Full trace viewer. | Provider trace formats inside core data contracts. |
| Runtime support | RuntimeProjection per runtime. | More adapters after core tests pass. | Provider-coupled core imports. |
| Source authority | Local official-doc refs plus exact source paths. | Live official-doc refresh before implementation. | Using runtime cache or generated payloads as semantic authority. |

## Proposal Implications
- The implementation should be small because much of the semantic substrate already exists. `SemanticConversationState`, application state, retrieval context, workbench state, workflow-family AIP surface enums, capability contracts, `AIPAgentDeclaration`, document corpus, and eval suites are already present.
- The missing local abstraction is not "a chatbot UI." It is a compact set of contracts that tie chatbot declaration, session, retrieval, tools, action boundaries, and evals together in one runtime-neutral shape.
- `AIPAgentDeclaration` already models governed ontology-connected agents with ontology scope, tool bindings, eval suites, deployment stage, and observability. The minimal path is to wrap or extend it as a Chatbot Studio declaration rather than introducing a parallel source of truth.
- Existing `application-state.ts` already matches the official deterministic-input rule: pinned loop snapshots are not changed by later updates in the same reasoning loop. The new architecture should lean into that instead of rewriting it.
- Existing `retrieval-context.ts` already produces `retrievedPrompt`, ontology refs, skill refs, source refs, semantic refs, and document refs. The minimal addition is structured run metadata, not a new retriever.
- Existing workflow-family contracts already enumerate `application-state-variables`, `retrieval-context`, `tools-action`, `tools-object-query`, `tools-function`, `tools-update-application-variable`, `tools-command`, `tools-request-clarification`, `chatbots-as-functions`, `evals-observability`, `security-governance`, and `runtime-projection`. Use those enums as the canonical surface list.
- The current FDE readiness evaluator asks a next-step question that names a specific `mcp__palantir-mini__pm_semantic_intent_gate` path. For provider-neutral Chatbot Studio semantics, user-facing readiness questions should describe the semantic approval requirement and leave runtime-specific invocation details to adapters or docs.
- Commands-as-tools should be included as a contract type but not implemented as runtime app pairing in the first slice. The official docs make commands application-context dependent; local core should only declare the command and approval policy.
- Evals are not optional for chatbot semantics. Official docs connect chatbots-as-functions to AIP Evals, and existing local eval suites already model nondeterminism, human review for mutation, deterministic semantic mapping, and prompt-to-DTC regressions.

## Open Questions
- Should the first implementation expose `ChatbotStudioDeclaration` as a new top-level primitive, or as a strict `AIPAgentDeclaration` subtype with `surface: "aip-chatbot-studio"`?
- Should local session ids be deterministic ids for reproducible tests, random ids for API resemblance, or deterministic ids with optional external Foundry-style session RIDs?
- Should `Update application variable` be represented as a state-update tool that can write only named application variables, or as a proposal event that a deterministic post-processor applies?
- What is the smallest acceptable action simulation for the first slice: declared `ActionTypeRid` plus approval refs only, or a dry-run result envelope with submission-criteria diagnostics?
- Should document context use only `.palantir-mini/document-corpus.json` initially, or also accept local research refs from source-authority contracts?
- Which eval suite should become the required smoke gate: a new `chatbot-studio-local-regression.json`, or extensions to `fde-turn-quality-semantic.json` and `semantic-consistency-regression.json`?
- Should command tools be held at declaration-only until a separate app-pairing adapter exists?

## Confidence And Gaps
Confidence: medium-high.

The design is well supported by local source evidence and local official Palantir documentation mirrors. The main confidence anchors are the existing `lib/chatbot-studio` projections, `workflow-family-enforcement` AIP surface contracts, `AIPAgentDeclaration`, FDE chatbot/eval review structures, and official docs for application state, retrieval context, tools, chatbots-as-functions, Foundry APIs, and AIP Evals.

Gaps:

- I did not use palantir-mini tools, skills, routing, or MCP.
- I did not live-refresh Palantir docs from the web. The official docs used here are local mirrors fetched on 2026-05-12.
- I did not run tests because this was a report-only architecture task.
- I did not inspect every source file under `palantir-mini`; evidence was targeted to Chatbot Studio, AIP/FDE contracts, runtime boundaries, capability routing, and eval surfaces.
- The report assumes the first implementation remains additive and source-only. Any later implementation should re-check current branch state, generated-file rules, and validation commands before editing.
