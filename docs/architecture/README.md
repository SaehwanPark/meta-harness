---
title: Architecture
description: The portable contract, runtime capabilities, role semantics, and handoff rules behind Meta Harness.
layout: default
---

# Architecture

Meta Harness maintains one portable workflow model and maps it onto actively
supported coding-agent runtimes. The portable model is authoritative; runtime
profiles and adapters are optional, removable execution material.

## Architecture guides

- [Portable contract](portable-contract.html) — source of truth and rippability.
- [Runtime capabilities](runtime-capabilities.html) — capability vocabulary and safe degradation.
- [Role contract](role-contract.html) — runtime-neutral delegated-role fields.
- [Handoffs](handoffs.html) — ephemeral coordination and durable artifacts.

## Core invariant

A runtime adapter may lower a guarantee, but it must not silently claim a
stronger guarantee than the runtime provides. When a required capability is
unavailable, serialize the work or stop with a clear limitation.
