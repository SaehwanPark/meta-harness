---
title: Architecture Patterns
description: Select a coordination pattern that matches the dependency and review shape of your work.
layout: default
---

# Architecture Patterns

Patterns are coordination tools, not required ceremony. Pick one only when it
makes ownership, sequencing, or review clearer than a direct workflow.

## Pipeline

**Best fit:** sequential work where each phase consumes a stable prior artifact.

**Shape:** scope → research → build → review → validate.

Use it when order is the main risk. Do not use it when independent branches
would be forced to wait for one another.

## Fan-out/Fan-in

**Best fit:** several independent, read-heavy slices followed by synthesis.

**Shape:** one request → bounded parallel findings → one synthesis owner.

Give each branch a non-overlapping artifact or isolated environment. Do not
use it when branches depend on shared mutable state.

## Expert Pool

**Best fit:** a router selects one or more specialists from a stable set.

**Shape:** classify request → select specialist → return bounded result.

Use explicit routing criteria and one fallback for ambiguous requests. Do not
use it when every request needs nearly every specialist.

## Producer-Reviewer

**Best fit:** generated work benefits from a separate critique and bounded
revision.

**Shape:** produce → review → fix or approve.

The reviewer reads the original request, the produced artifact, and the
acceptance criteria. Cap revision loops so “review” cannot become an
unbounded second production process.

## Supervisor

**Best fit:** the backlog changes during execution and needs reprioritization.

**Shape:** assign → inspect status → reassign or integrate.

The supervisor owns the queue and final integration. Keep worker writes
isolated and report partial failure explicitly.

## Hierarchical Delegation

**Best fit:** a large goal separates naturally into shallow sub-goals, each
with its own local workflow.

**Shape:** top-level goal → domain lead → bounded execution.

Keep the hierarchy to two coordination layers. Flatten it when routing starts
to hide rather than clarify dependencies.

## Combine patterns carefully

Common combinations include:

- **Pipeline + Fan-out/Fan-in:** ordered stages with a parallel evidence phase;
- **Fan-out/Fan-in + Producer-Reviewer:** parallel drafts followed by one review;
- **Supervisor + Expert Pool:** a changing queue routed to explicit specialists;
- **Hierarchical Delegation + Pipeline:** shallow domain splits with local order.

Document the outer pattern first and keep the inner variation local to the
phase that needs it.

## Quick selection table

| If your main problem is… | Start with… |
| --- | --- |
| order and phase dependency | [Pipeline](#pipeline) |
| independent coverage | [Fan-out/Fan-in](#fan-outfan-in) |
| selecting among specialists | [Expert Pool](#expert-pool) |
| output quality and critique | [Producer-Reviewer](#producer-reviewer) |
| a changing backlog | [Supervisor](#supervisor) |
| a naturally layered goal | [Hierarchical Delegation](#hierarchical-delegation) |

Read the [workflow guide](workflow.html) for the phase contract and the
[output specifications](../harness/README.html) for durable artifact shapes.
