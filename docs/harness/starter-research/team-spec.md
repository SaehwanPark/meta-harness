# Starter Research Team Spec

## Goal

Produce a short cited research brief for one repository-specific question using deterministic handoff files and one final synthesis owner.

## Roles

| Role | Responsibility | Writes |
| --- | --- | --- |
| `research-lead` | scopes the question, checks source quality, and owns final synthesis | `_workspace/final/report.md` |
| `source-research` | gathers evidence from approved sources and normalizes citations | `_workspace/01_source_findings.md` |

## Workflow

### Phase 1: Scope

- Capture the request and success criteria in `_workspace/00_input/request-summary.md`.
- Name the required source types and any exclusions before research starts.

### Phase 2: Evidence Collection

- Gather findings into `_workspace/01_source_findings.md`.
- Keep each finding tied to one source and one claim.

### Phase 3: Synthesis

- Read the request summary and findings artifact.
- Write `_workspace/final/report.md` with a short answer, supporting evidence, and open questions.

## Failure Policy

- If the request scope is ambiguous, stop after Phase 1 and record the missing decision in the request summary.
- If evidence quality is weak, preserve the findings artifact and mark the final report as incomplete rather than inventing coverage.

## Validation

- Every phase writes exactly one named artifact.
- The final report cites the findings artifact and states any unresolved gaps.
