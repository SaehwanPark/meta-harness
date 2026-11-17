# Harness Examples

## One reusable skill

A repository updates its API schema from route definitions. Ship `.agents/skills/openapi-sync/SKILL.md` with the project command and compatibility check. The schema diff is the deliverable. Add a breaking-change reference when the repository has that policy.

## Read-heavy parallel review

A team repeatedly needs separate API and data-model review against the same diff. Keep routing and acceptance in `docs/harness/change-review/team-spec.md`. Each authorized reviewer returns evidence for its area to the lead, who deduplicates findings and names coverage gaps. Use existing reviewer skills if they fit. Add branch files only if an auditor or a later session needs the original evidence.

## Resumable research

When collection and synthesis may happen in separate sessions, a team spec can name one durable handoff and one final deliverable:

| Producer | Consumer | Path | Contents and state |
| --- | --- | --- | --- |
| Source researcher | Research lead | `_workspace/01_sources_findings.md` | Question, claims with sources, open gaps, and complete or partial status |
| Research lead | Requester | User-selected report path | Cited synthesis and remaining evidence gaps |

The lead can resume from the findings file. If a required source is missing, the lead records that gap and reports partial coverage or continues collection. A separate request snapshot is useful only if the findings cannot carry the necessary scope.
