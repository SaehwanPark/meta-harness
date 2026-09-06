---
title: CLI Installation
description: Use the deterministic Meta Harness planner from scripts and CI.
layout: default
---

# CLI Installation

The CLI parses requests into an inspectable `InstallPlan`. The interactive
frontend renders the same plan; filesystem mutation happens only
when the plan has no conflicts and dry-run is not selected.

## Install one or more runtimes

```shell
python3 scripts/install_harness.py install \
  --scope project --target /path/to/repo \
  --agent pi --agent codex --non-interactive
```

Use `--agent generic` for portable Agent Skills only. Repeat `--agent` instead
of using a comma-separated value. `--native-profiles` adds optional generated
runtime profiles for runtimes that expose a profile format. Compile selected
role briefs explicitly when a repository has durable role contracts:

```shell
python3 scripts/install_harness.py compile \
  --scope project --target /path/to/repo \
  --agent codex --agent cursor \
  --role docs/harness/example/roles/worker.md \
  --model-policy balanced
```

## Inspect before writing

```shell
python3 scripts/install_harness.py install \
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
