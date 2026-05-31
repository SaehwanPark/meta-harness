# Official AIP Chatbot Studio Surface
## Scope

This report defines the official Palantir AIP Chatbot Studio product surface that a local one-developer proposal should emulate. It treats "AIP Chatbot Studio" as the current official product name and "AIP Agent Studio" / "AIP Agents" as legacy naming preserved for compatibility. The scope is limited to official Palantir documentation and local read-only evidence from the reviewed source authority. It does not use palantir-mini MCP tools, palantir-mini skills, pm-* tools, plugin routing, source edits, generated-file edits, cache edits, or `.palantir-mini/session` state.

The target to emulate is not "a generic agent framework." It is a builder surface for interactive, multi-turn assistants backed by LLMs, Ontology context, documents, application state, custom tools, publication/versioning, deployment surfaces, and observability.

## Files And Sources Read

Local meta-harness contract:

- `/home/palantirkc/meta-harness/.agents/skills/harness/SKILL.md`
- `/home/palantirkc/meta-harness/docs/harness/README.md`
- `/home/palantirkc/meta-harness/_workspace/palantir-mini-codex-review-2026-05-31/00_input/palantir-mini-opt-out-protocol.md`
- `/home/palantirkc/meta-harness/_workspace/palantir-mini-codex-review-2026-05-31/00_input/palantir-mini-opt-out.env`

Official Palantir documentation:

- `https://www.palantir.com/docs/foundry/chatbot-studio/overview/`
- `https://www.palantir.com/docs/foundry/chatbot-studio/getting-started/`
- `https://www.palantir.com/docs/foundry/chatbot-studio/core-concepts/`
- `https://www.palantir.com/docs/foundry/chatbot-studio/application-state/`
- `https://www.palantir.com/docs/foundry/chatbot-studio/retrieval-context/`
- `https://www.palantir.com/docs/foundry/chatbot-studio/tools/`
- `https://www.palantir.com/docs/foundry/chatbot-studio/commands-as-tools/`
- `https://www.palantir.com/docs/foundry/chatbot-studio/chatbots-as-functions/`
- `https://www.palantir.com/docs/foundry/chatbot-studio/session-logging/`
- `https://www.palantir.com/docs/foundry/chatbot-studio/marketplace/`
- `https://www.palantir.com/docs/foundry/chatbot-studio/foundry-apis/`
- `https://www.palantir.com/docs/foundry/workshop/widgets-aip-chatbot/`
- `https://www.palantir.com/docs/foundry/aip/aip-features/`
- `https://www.palantir.com/docs/foundry/announcements/2026-04/`

Local reviewed source authority, read-only:

- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/runtime-overlay/schemas-snapshot/ontology/primitives/aip-agent.ts`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/chatbot-studio/semantic-conversation-state.ts`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/chatbot-studio/application-state.ts`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/chatbot-studio/retrieval-context.ts`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/lib/chatbot-studio/lead-ontology-turn-card.ts`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/schemas/semantic-conversation-state.schema.json`
- `/home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini/core/contracts/aip-fde-local-surface.ts`

## Confirmed Product Surface

AIP Chatbot Studio is the current official name. Palantir's April 2026 announcement says AIP Agent Studio was rebranded starting the week of April 27, 2026, and that existing features and functionality remained unchanged. The same announcement says existing API naming remains available through AIP Agent endpoints for backwards compatibility.

The core product object is an AIP Chatbot: an interactive assistant equipped with enterprise-specific information and tools. Official docs describe it as deployable inside the Palantir platform and externally through the Ontology SDK and platform APIs. Chatbots are powered by LLMs, the Ontology, documents, and custom tools, and can support dynamic read/write workflows in applications.

Chatbot creation is a file/resource workflow. Official getting-started docs say AIP Chatbots are Palantir filesystem resources with granular access control, created from workspace navigation, quick search, Files, Chatbot Studio, or AIP Threads. Setup includes name, description, optional avatar, model selection, system prompt, temperature, input placeholder, suggested prompts, save/view/publish controls, and usage/feedback monitoring.

The official configuration pillars are:

| Surface | Official behavior |
| --- | --- |
| Retrieval context | Runs deterministically with every new user message and injects retrieved information into the LLM. Supported types are Ontology context, document context, and function-backed context. |
| Application state | String or object-set variables can be configured, described, selectively visible to the model, mapped to Workshop variables, used as deterministic inputs, updated by tools/context, tested in debug state, and referenced in the system prompt. |
| Tools | External capabilities/API calls that let the LLM perform actions or retrieve information. Official tool types include Action, Object query, Function, Update application variable, Command, Request clarification, and legacy Ontology semantic search. |
| Tool calling mode | Prompted tool calling is broadly supported. Native tool calling is available for a subset of models and tool types and can call multiple tools in parallel. |
| Command tools | Commands let chatbots act inside Palantir applications on behalf of the user, use current application state/screen, optionally require approval before execution, and can be tested through app pairing. |
| View reasoning | Users can inspect reasoning in edit mode, view mode, Workshop, or AIP Threads. |
| Publish/version lifecycle | Users can save versions, view as an end user, publish for production, and optionally publish the chatbot as a Function. |
| Functions | Published chatbot functions accept `userInput`, optional `sessionRid`, and application variables; they output markdown response, session RID, and variable updates. |
| APIs | Developer Console applications can embed chatbots via platform APIs, create sessions, continue sessions through blocking or streaming APIs, retrieve content/history, and retrieve session traces. |
| Workshop | The AIP Chatbot widget is the recommended Workshop integration. It selects a chatbot/version, can show reasoning, maps application variables to Workshop variables, and can use Commands for read/write cross-application workflows. |
| Observability | Session logging can export structured execution events with trace IDs, session RIDs, user requests, compiled system prompts, tool calls/results, final responses, and errors. |
| Distribution | Foundry DevOps can package AIP Chatbots into Marketplace products, with document media sets included when document context is configured. |
| Security model | Official docs state the product uses the Palantir platform security model so LLMs receive only the access needed for the task. |

## Local One-Developer Implications

The local emulation should be a product-surface mirror, not a claim of Palantir feature parity. For one developer, the practical unit is a repo-local declaration and deterministic review loop that makes an assistant's configuration, state, tools, publication stage, and evidence inspectable.

The local source already points in this direction:

- `runtime-overlay/schemas-snapshot/ontology/primitives/aip-agent.ts` models a governed `AIPAgentDeclaration`, explicitly distinct from runtime subagents. It includes surface names, legacy naming support, model refs, system prompt ref, ontology scope, tool bindings, eval suite IDs, deployment stage, and observability options.
- `lib/chatbot-studio/semantic-conversation-state.ts` models the conversation as typed state with user-facing, ontology-facing, skill/capability-facing, contract-facing, impact-facing, issue-facing, validation-facing, and lifecycle projections.
- `lib/chatbot-studio/application-state.ts` mirrors the official application-state idea with visible variables, deterministic updates, pinned reasoning-loop snapshots, and model write denial for control variables.
- `lib/chatbot-studio/retrieval-context.ts` mirrors function-backed retrieval by building a `retrievedPrompt` plus ontology, skill, source, canonical-term, conflict, and document refs from conversation state.
- `lib/chatbot-studio/lead-ontology-turn-card.ts` provides a local review card with plain summaries, choices, readiness, next actions, and an explicit `mutationAuthorizedFromCard: false` boundary.
- `core/contracts/aip-fde-local-surface.ts` requires source authority refs, runtime projections, mutation capability, validation refs, and forbids unsupported parity claims.

For a one-developer local proposal, the minimum credible surface is therefore:

- A durable agent/chatbot declaration, separate from native runtime subagents.
- A state model that separates user-visible state, application state, retrieval context, tool bindings, lifecycle, evaluation, observability, and deployment stage.
- A deterministic local simulation of official Chatbot Studio loops: retrieve context, pin application variables, choose/call tools, capture tool result, update variables, produce response, and preserve trace.
- A clear mutation boundary: an assistant may propose, request clarification, call read tools, or call approved write tools, but local authorization must not be inferred from LLM text alone.
- A local "publish" concept that means ready for developer use in the repo, not public Palantir deployment.

## Must-Have / Should-Have / Out-Of-Scope Table

| Priority | Capability | Local interpretation |
| --- | --- | --- |
| Must-have | Current/legacy naming bridge | Use AIP Chatbot Studio as current name; preserve Agent Studio / Agent endpoint naming only as compatibility metadata. |
| Must-have | Chatbot/agent declaration | Store name, description, surface, model refs, system prompt ref, ontology scope, tool bindings, deployment stage, and observability flags. |
| Must-have | Filesystem/resource semantics | Treat local declarations as durable repo artifacts with reviewable access and provenance, not ephemeral prompts. |
| Must-have | Retrieval context | Support deterministic per-message context assembly from ontology-like refs, docs/source refs, and function-backed/local computed retrieval. |
| Must-have | Application state | Support string/object-set-like variables, descriptions, visibility, deterministic inputs, pinned loop values, and deterministic updates. |
| Must-have | Tool catalog | Represent at least object query/read, action/write, function, application-variable update, command-like local operation, and request-clarification tools. |
| Must-have | Human approval for mutation | Model write/action tools with approval requirements and keep approval external to free-form LLM output. |
| Must-have | Save/view/publish lifecycle | Provide draft/dev/staging/production-like stages and a local view/test mode before publish. |
| Must-have | Session trace | Persist session ID, trace ID, user message, retrieved context, compiled prompt, tool calls/results, final response, and errors. |
| Must-have | Runtime-boundary disclosure | State which official Palantir surfaces are emulated locally and which are absent. |
| Should-have | Workshop-like application state mapping | Let local app/view state be mapped to variables so other local surfaces can consume chatbot outputs. |
| Should-have | Function publishing analogue | Provide a callable local function/CLI/API wrapper with `userInput`, optional `sessionId`, and variable inputs/outputs. |
| Should-have | Blocking and streaming response modes | Match official API shape conceptually, even if implemented as local blocking first. |
| Should-have | View reasoning/debug panel | Preserve enough structured reasoning/tool trace for developer debugging without treating it as authority. |
| Should-have | Evals linkage | Attach evaluation suite IDs or local eval packs to non-draft agents. |
| Should-have | Marketplace/package analogue | Export/share declarations and required document/source context as a portable local bundle. |
| Out-of-scope | Real Foundry deployment | Local emulation cannot claim deployment to Foundry, Workshop, AIP Assist, AIP Automate, or Marketplace. |
| Out-of-scope | Real Palantir filesystem ACLs | Local files can approximate review/provenance, but not Foundry's resource security model. |
| Out-of-scope | Real Ontology SDK / Platform API access | Unless a separate integration is configured, local code should not claim official API execution. |
| Out-of-scope | Real Palantir session logging export | Local traces can mirror the schema shape but are not Foundry streaming datasets. |
| Out-of-scope | Native tool-calling parity | Local runtimes may expose different tool semantics; parity must be described as conceptual unless verified per runtime. |
| Out-of-scope | Commands in live Palantir apps | Local command-like operations are not Workshop/App Pairing commands unless actually wired to those products. |

## Proposal Implications

The final proposal should emulate AIP Chatbot Studio as an authoring and governance surface, not just a chat UI. It should define a local artifact contract with these objects:

- `AIPChatbotDeclaration` or current-compatible `AIPAgentDeclaration`
- `SystemPromptRef`
- `RetrievalContextConfig`
- `ApplicationStateConfig`
- `ToolBinding`
- `PublishVersion`
- `SessionTrace`
- `EvaluationBinding`
- `DeploymentTarget`

The proposal should explicitly map each local object to the official surface it emulates. It should also include a "not Palantir" disclosure for every official capability that cannot be reproduced locally: Foundry ACLs, Workshop widgets, AIP Assist, Ontology SDK deployment, platform APIs, Foundry logging export, and Marketplace.

The local product should privilege deterministic state over prompt-only behavior. Official docs make retrieval context deterministic per user message, support deterministic application variable updates, and separate configured tools from free-form prompt text. A local one-developer implementation should therefore make the state machine inspectable and testable before allowing any write-like operation.

The proposal should keep runtime subagents separate from product agents. Local read-only source evidence already makes that distinction in `AIPAgentDeclaration`: runtime subagents are not the same thing as governed ontology-connected product agents. The final proposal should preserve that boundary.

The strongest local analogue is a repo-local "Chatbot Studio workbench" that can:

- create/edit a chatbot declaration;
- bind retrieval context, application state, and tools;
- run a debug/view session;
- show trace, variables, tool calls, and final response;
- require external approval for mutation-capable tools;
- publish a local version for CLI/API/app embedding;
- run evals and preserve trace evidence.

## Open Questions

- Should the local proposal use the current official name `AIPChatbotDeclaration`, keep the existing local `AIPAgentDeclaration`, or expose both with one canonical alias?
- What is the local one-developer substitute for Foundry ACLs: repository permissions, signed review files, allowlists, or a capability-token model?
- Which official tool types are required in the first local slice: object query, action, function, update variable, command, request clarification, or all of them as schema-only declarations?
- Should local "publish as function" be a CLI command, an HTTP endpoint, a TypeScript function, or all three behind the same declaration?
- What trace retention policy should local session logging use, especially for user identifiers, prompts, and tool payloads?
- Should command-like tools be allowed to touch the local browser/app environment, or remain proposal-only until a dedicated approval surface exists?
- How should eval suites gate promotion from draft/dev to production in the local lifecycle?

## Confidence And Gaps

Confidence is high for the official product surface described above because it is grounded in current official Palantir documentation, including the April 2026 rename announcement, Chatbot Studio overview, getting-started, core concepts, retrieval context, application state, tools, functions, APIs, Workshop widget, session logging, and Marketplace pages.

Confidence is medium for local implementation implications because the reviewed source was read-only and appears to contain the relevant primitives and control-state mirrors, but this report did not execute tests or inspect all downstream call sites. The local source already contains strong ingredients for a Chatbot Studio-style proposal, especially `AIPAgentDeclaration`, deterministic application state, retrieval context, semantic conversation state, review cards, and local surface contracts.

Main gaps:

- Official docs confirm the product surface, not exact internal implementation details.
- This report did not verify current Foundry API OpenAPI schemas beyond the public docs page.
- This report did not use Palantir product access, Workshop, AIP Assist, Developer Console, Ontology SDK, or AIP Automate.
- This report did not inspect every local file that may reference Chatbot Studio or Agent Studio because the task only needed the product surface and proposal implications.
- Local parity claims must remain limited to emulation unless a later implementation proves runtime behavior with tests and explicit user opt-in.
