# Skills And Agents Surface Audit

## Scope

Audit target: source codex-skills/ and agents/ under /home/palantirkc/palantir-mini-marketplace/plugins/palantir-mini.
Harness project: /home/palantirkc/meta-harness. Boundary: read-only evidence plus this assigned report only.
No plugin tools, plugin skills, routing, source edits, cache edits, staging, commits, pushes, or PRs were used.

## Files And Sources Read

- meta-harness/.agents/skills/harness/SKILL.md
- 00_input/palantir-mini-opt-out-protocol.md, subagent-prompt-prefix.md, palantir-mini-opt-out.env
- Source: .codex-plugin/plugin.json, codex-skills/README.md, all 16 codex-skills/*/SKILL.md files
- Source: all 24 active agents/*.md files and archived doc-writer.md
- Targeted grep/list evidence from source skills/ for deprecation, merge, and category markers
- Runtime evidence: narrow read-only checks of ~/.codex/config.toml and the installed cache for version 6.79.0

## Confirmed Inventory

- .codex-plugin/plugin.json points Codex skills at ./codex-skills/ and does not declare an agent export surface.
- codex-skills/ has 16 wrapper skills, 16 lines each, 256 total lines. The README says wrappers are thin pointers and must not contain workflow truth.
- Canonical skills/ has 78 SKILL.md files and about 11,966 total lines; that surface is too large for default injection.
- agents/ has 24 active markdown files, about 3,927 total lines, plus one archived doc-writer.md.
- Active deprecated agents: home-implementer, pm-implementer, mc-implementer, kosmos-implementer.
- project-implementer replaces pm-implementer, mc-implementer, and kosmos-implementer. home-implementer has inconsistent replacement text.
- docs-researcher already absorbs the old doc-writer role; doc-writer is archived.
- The installed cache contains 16 codex wrappers, 78 canonical skills, and 24 active agents while the plugin is enabled in Codex config.

## Bottleneck Evidence

- Context pressure: source intent is 16 thin Codex wrappers, but the installed cache also contains the full 78 canonical skills. If runtime discovery scans every cached SKILL.md, the visible surface becomes 94 skill docs.
- Wrapper duplication: each Codex wrapper has the same name as a canonical skill and says to read the canonical skill before use. Good pointer pattern, risky if both paths are injected.
- Default wrapper sprawl: audit, retention, replay, memory, value, dirty-state, review, ship, verify, and reload all compete with the front-door skills.
- Runtime assumptions: active agents contain Claude-style model pins, Agent/Task* tools, SubagentStop validation, claude-in-chrome tools, MCP tool names, and ~/.claude paths.
- Runtime-gap evidence is already present in lead-orchestrator, hook-builder, plugin-maintainer, and ontology-steward; several mark Codex support as manual or adapter-native.
- Overlap: lead-orchestrator duplicates pm-orchestrate; harness agents duplicate pm-harness workflows; grader agents overlap with grade dispatcher behavior; researcher/docs-researcher/scrapling-fetcher overlap.
- Retired implementer risk: four deprecated implementers remain discoverable in active agents/.
- Tool naming is not normalized: wrappers use mcp__palantir-mini__... while many agents use mcp__plugin_palantir-mini_palantir-mini__....

## Keep / Merge / Disable / Delete Table
| Surface | Recommendation | Rationale |
| --- | --- | --- |
| pm-semantic-intent-gate | Keep public | Best front-door boundary for intent and contract checks. |
| pm-orchestrate | Keep public | Single multi-step workflow entrypoint; do not also expose a public lead-orchestrator by default. |
| pm-ontology-engineering-lead | Keep public or bundle under pm-orchestrate | Valuable for explicit session-first ontology work, but overlaps with the main orchestrator. |
| pm-verify, pm-recap, pm-mcp-reload | Keep public | Validation, continuity, and reload boundaries are durable Codex defaults. |
| pm-review, pm-ship | Keep public only as explicit release commands | High value when directly invoked; should not auto-trigger. |
| pm-intent-to-ontology, pm-dtc-fill | Merge or make docs-only behind pm-semantic-intent-gate | They overlap with the front-door gate; pm-dtc-fill is better as contract-fill guidance than a default wrapper. |
| pm-rule-audit, pm-memory-map, pm-value-audit, pm-replay, pm-events-rotate, pm-dirty-classify | Dev-only or merged into one audit wrapper | Diagnostics and maintenance should stay reachable without all being default-loaded. |
| codex-skills wrapper pattern | Keep | The pattern is healthy if wrappers stay thin and runtime discovery ignores canonical skills by default. |
| researcher, verifier-correctness, verifier-adversarial | Keep public only where native agent support exists; otherwise docs-only | Read-only and useful, but still contain runtime/event assumptions. |
| implementer | Keep public with explicit scope contract | Generic one-task executor; needs file boundary and verification briefing. |
| project-implementer | Keep public only for governed project-bound work; otherwise dev-only | Correct replacement for project-specific implementers, but depends on project-scope files and contract authority. |
| pm-implementer, mc-implementer, kosmos-implementer | Delete from active surface or move to archive | Deprecated, superseded by project-implementer, and retired at sprint 77. |
| home-implementer | Delete from active surface or move to archive | Retired and has inconsistent replacement text; normalize then archive. |
| docs-researcher | Keep dev-only | It writes research files and already merged doc-writer duties. |
| scrapling-fetcher | Merge into researcher/docs-researcher guidance or keep dev-only | Too narrow for public discovery; useful as a cost helper. |
| code-grader, model-grader, eval-judge | Merge behind grader dispatcher or keep dev-only | These are eval substrate implementation details, not public agents. |
| harness-planner, harness-generator, harness-evaluator, harness-analyzer | Dev-only or docs-only recipes | They assume harness paths, grading MCPs, and SubagentStop semantics. |
| lead-orchestrator | Docs-only for Codex until native parity is proven | Declares manual Codex support and unsupported subagent lifecycle parity. |
| hook-builder, plugin-maintainer, ontology-steward, protocol-designer, agent-author | Dev-only | Mutation-capable maintainer roles with source/runtime/schema authority. |

## Runtime Separation Implications

- Codex should treat .codex-plugin/plugin.json#skills as the Codex skill export authority; canonical skills in cache should not become defaults.
- agents/ should not be treated as native public Codex agents merely because files exist; the manifest does not declare an agent export surface.
- Agent model pins are recipe metadata. Codex full-history forks must not pass role/model/reasoning/service-tier overrides in the same call.
- Any Codex projection needs an adapter contract for tools, output contracts, lifecycle gaps, and fallback behavior.
- Normalize MCP tool naming before public exposure; current wrappers and agents use different naming shapes.
- Mutation-capable agents need explicit project root, writable scope, contract refs, and runtime support evidence.

## Proposal Implications

- Add surfaceStatus metadata: public, dev-only, docs-only, archived; add runtime status when needed.
- Shrink public Codex defaults to the front-door/orchestrate/verify/recap/reload set, with review and ship as explicit release commands.
- Collapse audit and maintenance wrappers behind one audit entrypoint or keep them canonical-only/dev-only.
- Add a validation test that fails if canonical skills/* are injected when plugin.json points to codex-skills/.
- Move deprecated implementers out of active agents/ or exclude deprecated agents from discovery.
- Keep project-implementer as the only project-specific implementer pattern; put project variation in project-scope files.
- Convert lead-orchestrator and harness agents to Codex docs-only recipes until subagent lifecycle parity has smoke evidence.

## Open Questions

- Does public mean default-loaded every turn or available by explicit named invocation?
- Does current Codex discovery scan only plugin.json#skills, or every cached SKILL.md? File evidence shows both wrapper and canonical trees are present.
- Should agents stay public in Claude while docs-only in Codex, or should one shared surfaceStatus govern all runtimes?
- Is .archived/ enough for retired implementer tombstones, or must active tombstone files remain in agents/?
- Should home-implementer be superseded by implementer or project-implementer? The file says both.
- Should pm-dtc-fill remain a public wrapper or be absorbed by pm-semantic-intent-gate?

## Confidence And Gaps

Confidence is high for inventory counts, deprecated implementer findings, the doc-writer merge evidence, and source/cache surface mismatch evidence.

Confidence is medium for exact public/dev/docs-only placement because final policy depends on what public means for Codex and Claude separately.

Gaps:

- No plugin tools, routes, skills, or MCP validation were used.
- No runtime smoke test was run to prove actual Codex injection behavior.
- Canonical skills were not audited one by one beyond inventory, counts, and targeted deprecation/category evidence.
- This report proposes surface policy only; it does not edit source, cache, manifests, agents, skills, or generated files.
