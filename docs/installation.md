---
title: Installation
description: Plan and install the canonical Meta Harness skill for one or more runtime targets.
layout: default
---

# Installation

The installer has one planning engine for CLI, TUI, audit, and profile
compilation. It previews operations before mutation and never takes ownership of
the target repository's `AGENTS.md`, `README.md`, or documentation.

## Modern CLI

Use the explicit `install` command for deterministic automation:

```shell
python3 scripts/install_harness.py install \
  --scope project \
  --target /path/to/repo \
  --agent pi \
  --agent cursor \
  --non-interactive
```

`--agent` is repeatable. The actively supported targets are `pi`, `codex`,
`antigravity`, `cursor`, and `generic`. All selections retain the shared
`.agents/skills/harness/` source of truth. `generic` installs portable Agent
Skills without promising runtime-specific workers, isolation, permissions, or
model routing.

Preview first:

```shell
python3 scripts/install_harness.py install \
  --scope project --target /path/to/repo \
  --agent codex --agent cursor \
  --native-profiles --dry-run --non-interactive
```

The plan reports `CREATE`, `UPDATE`, `KEEP`, `SKIP`, `REMOVE`, and `CONFLICT`
operations. A conflict is never silently overwritten. `--force` can replace a
known managed Harness tree or generated profile, but it cannot overwrite an
arbitrary user-owned path.

## Scopes

| Scope | Destination | Use it when… |
| --- | --- | --- |
| Project | `./.agents/skills/harness/` | one repository should carry its own Harness install |
| User | `~/.agents/skills/harness/` | several repositories should share one install |

For project scope, `--target` must name an existing directory. User scope uses
the current home directory and rejects `--target`. Test homes can be injected
with `META_HARNESS_HOME` (or `HOME`/`USERPROFILE`) without touching a real user
installation.

## Native profiles and compilation

Native execution profiles are optional generated artifacts. Enable them during
installation:

```shell
python3 scripts/install_harness.py install \
  --scope project --target /path/to/repo \
  --agent codex --agent antigravity --agent cursor \
  --native-profiles --non-interactive
```

Or compile profiles separately:

```shell
python3 scripts/install_harness.py compile \
  --scope project --target /path/to/repo \
  --agent codex --agent cursor
```

Profiles remain removable adapters. Deleting native profile directories leaves
the shared skill, portable role contracts, and `_workspace/` handoffs intact.
Pi's optional `pi-safe-agent-team` integration is selected with
`--pi-safe-agent-team on` but does not cause an invented native profile path.

## Audit and diagnostics

Inspect an existing repository without mutation:

```shell
python3 scripts/install_harness.py audit --target /path/to/repo
```

The audit reports `existing_skills`, `existing_roles`, `detected_runtimes`,
`stale_artifacts`, `compatibility_risks`, `operation_classification`, and a
`recommended_action`. Legacy artifacts receive an explicit keep/migrate/remove/
ignore decision; audit itself is read-only.

Check prerequisites:

```shell
python3 scripts/install_harness.py doctor --scope project --target /path/to/repo
```

## Interactive mode

On a real TTY, `meta-harness install` (or `--interactive`) opens the keyboard-
friendly checkbox/radio installer. It selects scope, runtimes, optional Pi
integration, native profiles, mode, and target, then previews the same
`InstallPlan` used by the CLI. Use `--non-interactive` in CI or piped commands;
non-TTY execution never attempts to render a TUI and instead requires explicit
values.

The [TUI guide](installation/tui.html) describes preview, conflict, repair, and
small-terminal behavior.

## Copy and symlink modes

Copy mode is the default and produces a standalone installation. During local
Harness development, symlink mode can point a destination at this checkout:

```shell
python3 scripts/install_harness.py install \
  --scope project --target /path/to/repo \
  --agent generic --mode symlink --non-interactive
```

Use symlink mode only when the target intentionally depends on this working
copy. If directory links are unavailable, the installer fails clearly and does
not silently fall back to copy mode.

## Deprecated compatibility aliases

The old direct invocation and `--layout` names remain temporarily operational
for migration. They are unverified/deprecated and do not grant first-class
support:

| Layout | Destination or behavior | Status |
| --- | --- | --- |
| `standard` | shared `.agents/skills/harness/` | portable compatibility alias |
| `codex` | shared tree plus `.codex/skills/harness/` | deprecated compatibility alias |
| `forgecode` | shared tree plus `.forge/skills/harness/` (or `~/forge/skills/harness/`) | unverified/deprecated |
| `droid` | shared tree plus `.factory/skills/harness/` | unverified/deprecated |
| `openhands` | shared tree; optional `.openhands/` setup remains user-owned | unverified/deprecated |
| `aider` | shared tree; follow up with `.aider.conf.yml` `read: AGENTS.md` | unverified/deprecated |

For example, this old form remains accepted but emits a deprecation warning:

```shell
python3 scripts/install_harness.py \
  --scope project --target /path/to/repo --layout codex
```

Do not remove unknown legacy files automatically. Use the audit report and an
explicit install plan with `--remove-legacy` only for recognized Harness
mirrors. See the [migration guide](installation/migration.html).

## Repository ownership and validation

The installer does not create or update the target repo's `AGENTS.md`,
`README.md`, or docs. `AGENTS.md` stays repo-owned; use the
[AGENTS Authoring Guide](https://github.com/SaehwanPark/meta-harness/blob/main/.agents/skills/harness/references/agents-md-guide.md)
for intentional durable guidance.

Run the checks from the Meta Harness root:

```shell
python3 scripts/validate_pages.py
python3 scripts/validate_skills.py
python3 scripts/validate_adapters.py
python3 scripts/test_install_harness.py
python3 scripts/test_install_planner.py
python3 scripts/test_audit_harness.py
python3 scripts/validate_codex_port.py
```
