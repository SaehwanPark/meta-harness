---
title: Meta Harness Documentation
description: Design portable agent workflows, specialist skills, and deterministic handoffs.
layout: default
---

<div class="hero-panel">
  <div class="eyebrow">Portable agent workflow design</div>
  <h1>Design workflows that stay <span>portable</span>.</h1>
  <p>
    Meta Harness turns a project goal into a domain-specific workflow, the
    specialist skills that support it, and the handoff artifacts that keep the
    work inspectable.
  </p>
  <div class="hero-actions">
    <a class="button button-primary" href="{{ '/installation.html' | relative_url }}">Install Harness</a>
    <a class="button button-secondary" href="{{ '/guides/workflow.html' | relative_url }}">Read the workflow</a>
  </div>
  <div class="hero-meta">
    Current release: <strong>v{{ site.version }}</strong> · Runtime-neutral by
    default · <a href="https://github.com/SaehwanPark/meta-harness" target="_blank" rel="noopener">Open source on GitHub</a>
  </div>
</div>

## Start with the shortest useful path

Install the shared skill into a project, then ask for the smallest reusable
workflow that meets your need:

~~~shell
python3 scripts/install_harness.py \
  --scope project \
  --target /path/to/repo \
  --layout standard
~~~

The installer creates `.agents/skills/harness/` and leaves the target
repository's `AGENTS.md`, `README.md`, and documentation under the target
project's ownership.

<div class="card-grid">
  <article class="card">
    <h3>1. Describe the goal</h3>
    <p>State the domain, the final deliverable, and the quality bar before choosing a team shape.</p>
    <a class="card-link" href="{{ '/sample-prompts.html' | relative_url }}">Browse prompt patterns →</a>
  </article>
  <article class="card">
    <h3>2. Choose the shape</h3>
    <p>Use one of six coordination patterns only when specialization, ordering, or review provides real value.</p>
    <a class="card-link" href="{{ '/guides/patterns.html' | relative_url }}">Compare patterns →</a>
  </article>
  <article class="card">
    <h3>3. Preserve the handoff</h3>
    <p>Keep durable specs, role briefs, and intermediate artifacts in predictable repository paths.</p>
    <a class="card-link" href="{{ '/harness/README.html' | relative_url }}">See output specs →</a>
  </article>
</div>

## What Harness gives you

<div class="stat-grid">
  <div class="stat">
    <div class="stat-value">6</div>
    <div class="stat-label">phases from analysis to validation</div>
  </div>
  <div class="stat">
    <div class="stat-value">6</div>
    <div class="stat-label">coordination patterns</div>
  </div>
  <div class="stat">
    <div class="stat-value">1</div>
    <div class="stat-label">portable canonical skill tree</div>
  </div>
  <div class="stat">
    <div class="stat-value">0</div>
    <div class="stat-label">required runtime-specific agents</div>
  </div>
</div>

The core design is intentionally small:

- domain analysis makes the task boundary and quality bar explicit;
- architecture selection matches coordination to actual dependencies;
- generated skills keep reusable knowledge separate from runtime settings;
- deterministic handoffs make work inspectable, resumable, and easy to review;
- validation checks structure, behavior, and failure paths before the workflow
  is treated as reusable.

## The six-phase path

<ol class="phase-list">
  <li>
    <div><strong>Domain analysis</strong><span>Inspect the project, task types, constraints, and existing guidance.</span></div>
  </li>
  <li>
    <div><strong>Team architecture design</strong><span>Select the smallest coordination pattern that preserves quality.</span></div>
  </li>
  <li>
    <div><strong>Role and artifact definition</strong><span>Name responsibilities, write ownership, inputs, outputs, and failure policy.</span></div>
  </li>
  <li>
    <div><strong>Skill generation</strong><span>Write portable skills with clear selection boundaries and progressive disclosure.</span></div>
  </li>
  <li>
    <div><strong>Integration and orchestration</strong><span>Connect phases through concise summaries or durable `_workspace/` handoffs.</span></div>
  </li>
  <li>
    <div><strong>Validation and testing</strong><span>Run normal and failure scenarios, then simplify anything that does not earn its weight.</span></div>
  </li>
</ol>

Read the detailed [six-phase workflow guide](guides/workflow.html) for phase
outputs and stop conditions.

## Choose the coordination shape

| Pattern | Best when | Start here |
| --- | --- | --- |
| Pipeline | each phase depends on the previous artifact | [Pipeline](guides/patterns.html#pipeline) |
| Fan-out/Fan-in | independent read-heavy work benefits from parallel coverage | [Fan-out/Fan-in](guides/patterns.html#fan-outfan-in) |
| Expert Pool | a router should select a specialist for each request | [Expert Pool](guides/patterns.html#expert-pool) |
| Producer-Reviewer | an output needs an explicit critique and bounded revision | [Producer-Reviewer](guides/patterns.html#producer-reviewer) |
| Supervisor | a changing backlog needs central prioritization and reassignment | [Supervisor](guides/patterns.html#supervisor) |
| Hierarchical Delegation | a large goal naturally separates into shallow sub-goals | [Hierarchical Delegation](guides/patterns.html#hierarchical-delegation) |

> [!TIP]
> Keep tightly coupled work in one context. Add delegation only when the
> boundary, ownership, and synthesis responsibility can be stated clearly.

## Keep the portable source visible

The public portal explains the workflow. The repository remains the authority
for the reusable skill and its contracts:

| Surface | Purpose |
| --- | --- |
| `.agents/skills/harness/SKILL.md` | canonical six-phase workflow and portable defaults |
| `docs/harness/` | durable team-spec and role-artifact contracts |
| `_workspace/` | deterministic intermediate handoffs when inspection or resumption matters |
| `scripts/` | installer and repository validation |

For implementation details, read the [canonical Harness skill on GitHub](https://github.com/SaehwanPark/meta-harness/blob/main/.agents/skills/harness/SKILL.md).

## Continue

<div class="card-grid two-up">
  <article class="card">
    <h3>For builders</h3>
    <p>Install the skill, choose a target scope, and use a goal-shaped prompt.</p>
    <a class="card-link" href="{{ '/installation.html' | relative_url }}">Installation guide →</a>
  </article>
  <article class="card">
    <h3>For maintainers</h3>
    <p>Review the artifact contract, starter example, and repository validation commands.</p>
    <a class="card-link" href="{{ '/harness/README.html' | relative_url }}">Maintainer reference →</a>
  </article>
</div>
