---
title: Prompt Library
description: Goal-shaped prompts for designing portable Harness workflows.
layout: default
---

# Prompt Library

The shortest useful Harness request has three parts:

1. **Goal:** what domain or project problem should the workflow solve?
2. **Output:** what skills, specs, or handoff artifacts should it produce?
3. **Constraint:** what must remain portable, deterministic, bounded, or
   explicitly out of scope?

## Start with a reusable research workflow

~~~text
Build a reusable research harness for this repository.
Use deterministic handoff files, cite each source-backed finding, and validate
one normal flow plus one weak-evidence failure flow.
~~~

## Add an explicit review path

~~~text
Design a review workflow for this repository's documentation changes.
Separate content correctness, link/path integrity, and scope review; give each
review pass a bounded output and keep the final synthesis with one owner.
~~~

## Adapt an existing workflow

~~~text
Adapt this workflow into a repo-local Harness.
Keep the canonical skill runtime-neutral, preserve the existing artifact paths,
and move only conditional detail into references.
~~~

## Design an autonomous experiment loop

~~~text
Design an autonomous experiment harness for this repository.
Declare the mutable surface, keep the evaluation surface read-only, establish
a baseline, use one fixed metric, and record every candidate in a deterministic
results.tsv ledger.
~~~

## Ask for a specific output contract

~~~text
Create a portable source-research skill.
It should state when it applies, required inputs, citation rules, output paths,
normal and failure scenarios, and the exact validation command.
Do not create native agent definitions or add a new dependency.
~~~

## Make the boundary explicit

Useful constraints answer questions such as:

- Which files may change?
- Which runtime or client paths must remain optional?
- Which facts must be sourced or reproducible?
- Which work should stay single-agent?
- What should happen when evidence, permissions, or a worker is missing?

Avoid asking for a generic “agent team” without naming the deliverable. A
specific output lets Harness choose a pattern and a handoff shape that can be
reviewed.

## Near misses

Harness is a poor fit for a one-line edit, an isolated explanation, or work
that has no reusable workflow boundary. In those cases, ask directly for the
answer or change. Add Harness when the repeated process, role contract, or
validation path is part of the value.
