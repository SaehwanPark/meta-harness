---
title: Antigravity Compatibility
description: Use Meta Harness with Antigravity through the shared Agent Skills contract and optional native profiles.
layout: default
---

# Antigravity Compatibility

Antigravity is a first-class Meta Harness target. The shared Agent Skills tree
is canonical; native profiles are optional and remain runtime-specific.

## Paths

- Portable project skill: `.agents/skills/harness/`
- Portable user skill: `~/.agents/skills/harness/`
- Native profiles: Antigravity’s configured custom-agent location (generated,
  not assumed by the portable contract)
- Durable portable artifacts: `docs/harness/` and `_workspace/`

Keep native profile files out of the portable skill. If your Antigravity setup
uses a different discovery location, configure that location in the runtime
rather than forking `.agents/skills/harness/`.

## Capability profile

Antigravity can consume skills and may provide custom agents, subagents,
background execution, tool restrictions, model selection, and workspace
isolation. Exact availability depends on the installed Antigravity surface and
project policy. Confirm a capability before making it a correctness
requirement; supported recursion is not a reason to build deep hierarchies.

## Degradation

Map portable roles to the strongest verified capabilities. When isolation or
exclusive ownership is unavailable, assign explicit non-overlapping paths or
serialize mutable work. When parent/peer messaging or retained context is
unavailable, use parent summaries and `_workspace/` handoffs. Report the
lowered capability rather than silently weakening the workflow.

## Rippability

Delete Antigravity-native profiles or configuration without deleting the
canonical skills, team contracts, or durable handoffs. See the [portable
contract](../architecture/portable-contract.html), [runtime capabilities](../architecture/runtime-capabilities.html),
and [compatibility matrix](README.html).
