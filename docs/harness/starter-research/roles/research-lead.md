---
title: Research Lead Role
description: A bounded synthesis role for a docs-first repository research workflow.
layout: default
---

# Research Lead

## Portable role contract

```yaml
role: research-lead
responsibility: synthesize evidence into a concise research report
inputs: [request-summary, source-findings]
outputs: [final-report]
resources:
  reads: [_workspace/00_input/request-summary.md, _workspace/01_source_findings.md]
  writes: [_workspace/final/report.md]
workspace:
  preference: isolated
communication:
  parent: orchestrator
model_policy: strong
completion:
  artifact: _workspace/final/report.md
```

## Responsibilities

- define the question boundary and completion criteria
- approve the source mix before evidence collection starts
- synthesize the final report from the collected findings

## Inputs

- user request or repository task brief
- `_workspace/00_input/request-summary.md`
- `_workspace/01_source_findings.md`

## Outputs

- `_workspace/final/report.md`

## Review Rules

- reject unsupported claims instead of softening them into guesses
- preserve open questions in the final report when evidence is incomplete
- keep the report concise enough that a downstream implementer can act on it directly
