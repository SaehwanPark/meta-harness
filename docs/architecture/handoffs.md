---
title: Handoffs
description: Choose ephemeral coordination, durable coordination records, and durable artifacts deliberately.
layout: default
---

# Handoffs

Persist information when it provides auditability, resumability, debugging,
cross-agent consumption, or later synthesis—not merely because a runtime can
store it.

## Three classes

### Ephemeral coordination

Use native status, short clarification, and bounded parent/peer messages when
the result is only needed during the current run.

### Durable coordination record

Use a task assignment, decision request, block, acceptance state, or recovery
record when orchestration may resume later. A native task/message broker is
optional; `_workspace/` is the portable fallback.

### Durable artifact

Use deterministic files for plans, review evidence, experiment ledgers,
integration reports, and outputs consumed across sessions. Follow the
repository's `_workspace/` naming contract.

## Failure semantics

Describe failures that can change acceptance, such as a missing review
branch or unavailable access to an evidence source. Preserve partial outputs
and keep missing results visible in synthesis. Use a direct or serialized
fallback when it preserves the required permissions and guarantees.
