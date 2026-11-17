---
title: Starter Research Team Spec
description: A resumable research workflow with one evidence handoff and one synthesis owner.
layout: default
---

# Starter Research Team Spec

Answer a repository-specific question with a short cited report. The collector
scopes the question and gathers evidence. The [research lead](roles/research-lead.html)
owns synthesis and acceptance. One agent can perform both responsibilities when
collection and synthesis fit in a single session.

| Producer | Consumer | Path | Contents |
| --- | --- | --- | --- |
| Collector | Research lead | `_workspace/01_source_findings.md` | Question, source-backed claims, unresolved gaps, and ready, partial, or blocked state |
| Research lead | Requester | `_workspace/final/report.md` | Answer, supporting citations, and limits of coverage |

Use the findings file to resume across sessions. If a required source is
missing, record the attempted lookup and the conclusion it affects. The lead
can synthesize supported conclusions and flag incomplete coverage. Check
reported claims against the findings and their original sources.
