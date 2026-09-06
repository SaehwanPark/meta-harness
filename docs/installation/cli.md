---
title: CLI Installation
description: Use the deterministic Meta Harness planner from the installed CLI.
layout: default
---

# CLI Installation

The preferred command is the installed `meta-harness` CLI. It parses requests
into an inspectable `InstallPlan`. The interactive frontend renders the same
plan; filesystem mutation happens only when the plan has no conflicts and
dry-run is not selected.

When running directly from a source checkout without the CLI on `PATH`, replace
`meta-harness` with `python scripts/install_harness.py`. Both forms use the same
modern planner; the deprecated direct `--layout` form is for migration only.

## Install one or more runtimes

```shell
meta-harness install \
  --scope project --target /path/to/repo \
  --agent pi --agent codex --non-interactive
```

Use `--agent generic` for portable Agent Skills only. Repeat `--agent` instead
of using a comma-separated value. `--native-profiles` adds optional generated runtime profiles for runtimes that
expose a profile format. On `install`, pass repeatable `--role` paths to lower
specific portable role briefs. Compile selected role briefs explicitly when a
repository has durable role contracts:

```shell
meta-harness compile \
  --scope project --target /path/to/repo \
  --agent codex --agent cursor \
  --role docs/harness/example/roles/worker.md \
  --model-policy balanced
```

## Inspect before writing

```shell
meta-harness install \
  --scope project --target /path/to/repo \
  --agent cursor --native-profiles --dry-run --non-interactive
```

Plans use these operation states:

- `CREATE`: destination is absent;
- `UPDATE`: a managed artifact is stale or mode changed;
- `KEEP`: managed artifact is current;
- `SKIP`: operation is intentionally disabled;
- `REMOVE`: an explicitly selected known legacy artifact; and
- `CONFLICT`: an unknown or unsafe destination that must not be overwritten.

`--force` is limited to managed Harness artifacts. It is not a permission to
overwrite arbitrary user files.

## Commands

| Command | Purpose | Mutates by default? |
| --- | --- | --- |
| `install` | plan and apply portable skill/profile destinations | yes, after preflight |
| `audit` | inventory skills, roles, runtimes, drift, and legacy artifacts | no |
| `doctor` | report source, target, mode, and selection prerequisites | no |
| `compile` | lower portable role briefs into selected native profiles | yes, after preflight |
| `validate` | run portable skill and adapter structure checks | no |

Use `--dry-run` for an install or compile preview. Use `--non-interactive` in
CI, scripts, and piped sessions. A non-TTY invocation never attempts to render
the TUI and reports missing required values instead.

See the [main installation guide](../installation.html) and
[migration guide](migration.html) for legacy layouts and safe removal.
