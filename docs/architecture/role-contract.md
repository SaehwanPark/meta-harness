---
title: Role Contract
description: Define delegated roles independently from runtime-specific execution profiles.
layout: default
---

# Role Contract

A role describes what must be done. An adapter describes how a selected runtime
executes it. Keeping these separate makes a workflow portable and rippable.

## Portable role fields

A role may declare:

```yaml
role: implementation-worker
responsibility: implement and test the parser change
inputs: ["_workspace/plan.md"]
outputs: ["_workspace/implementation-result.md"]
skills: ["parser-guidance"]
reads: ["src/**"]
writes: ["src/parser/**"]
workspace: isolated
communication: parent-summary
model_policy: balanced
```

Use the smallest contract that makes ownership and acceptance unambiguous.
Meaningful roles should state responsibility, inputs, outputs, quality bar,
reads/writes, workspace preference, communication/escalation, permissions,
and completion evidence when those constraints matter.

## Semantic model policy

Portable roles may request `inherit`, `fast`, `economy`, `balanced`, or
`strong`. Adapters translate that request to their available model and
reasoning controls. Exact model IDs are optional runtime overrides, never a
portable requirement.

## Lowering rules

- Preserve required write safety with enforcement, isolation, explicit
  non-overlap, or serialization.
- Preserve acceptance evidence as a deterministic file when native state is
  not durable.
- Treat native agent definitions as generated profiles; do not move domain
  behavior into them.
- Keep delegation shallow: root → worker by default, with a second layer only
  when dependencies justify it.

See [runtime capabilities](runtime-capabilities.html) for status and fallback
semantics.
