---
title: Installation Migration
description: Audit and safely migrate deprecated Meta Harness runtime layouts.
layout: default
---

# Installation Migration

ForgeCode, Droid, OpenHands, and Aider layouts are unverified and deprecated.
They remain as compatibility aliases so an existing installation can be
inspected and deliberately migrated; they are not active support targets.

## Audit first

```shell
meta-harness audit --target /path/to/repo
```

Review `stale_artifacts`, `compatibility_risks`, and
`operation_classification`. Choose one explicit decision for each known legacy
artifact:

- **keep** it when another tool still owns it;
- **migrate** its reusable content to `.agents/skills/` or a portable role;
- **remove** it only when it is a recognized Meta Harness mirror; or
- **ignore** it and record why it remains.

Audit is read-only. Unknown files and runtime-owned configuration are never
removed automatically.

## Install the portable source

```shell
meta-harness install \
  --scope project --target /path/to/repo \
  --agent generic --non-interactive
```

Add first-class runtime targets explicitly when they are validated in the
repository. Native profiles are optional generated artifacts, not canonical
workflow definitions.

## Remove a known mirror explicitly

After confirming the audit result, ask the planner to remove recognized legacy
Harness mirrors while retaining the shared source:

```shell
meta-harness install \
  --scope project --target /path/to/repo \
  --agent generic --remove-legacy --non-interactive
```

The plan must show `REMOVE` for each mirror. If a destination is not recognized
as a managed Harness tree, it becomes `CONFLICT` and remains untouched.

## Rippability check

After migration, verify that removing native profile or legacy mirror
directories does not remove `.agents/skills/harness/`, `docs/harness/`, or
`_workspace/`. Keep `AGENTS.md`, `README.md`, and repository docs under their
original owner’s control.

See the [compatibility matrix](../compatibility/README.html),
[CLI guide](cli.html), and [portable contract](../architecture/portable-contract.html)
for support tiers and source-of-truth rules.
