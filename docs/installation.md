---
title: Installation
description: Install the canonical Meta Harness skill into a project or user-level skills directory.
layout: default
---

# Installation

Meta Harness is distributed as a repository-owned skill tree. The bootstrap
installer copies that tree into a project or into your user-level skills
directory; it does not take ownership of the target project's documentation.

## Choose an install scope

| Scope | Destination | Use it when… |
| --- | --- | --- |
| Project | `./.agents/skills/harness/` | one repository should carry its own Harness install |
| User | `~/.agents/skills/harness/` | several repositories should share one install |

The project scope is the safer default for a reproducible repository setup.
The user scope is convenient when you maintain several projects with the same
Harness version.

## Install into a project

Run this command from the Meta Harness checkout:

~~~shell
python3 scripts/install_harness.py \
  --scope project \
  --target /path/to/repo \
  --layout standard
~~~

The target directory must already exist. The installer creates the shared
`.agents/skills/harness/` path and preserves the target's `AGENTS.md`,
`README.md`, and documentation.

## Install for your user account

~~~shell
python3 scripts/install_harness.py --scope user --layout standard
~~~

This writes to `~/.agents/skills/harness/` for the current user. Use this
scope when the client discovers shared skills from the user home directory.

## Select a layout

`standard` installs only the portable shared tree. Select a native mirror
when the client has a separate discovery convention:

| Layout | Adds | Follow-up |
| --- | --- | --- |
| `standard` | `.agents/skills/harness/` | none |
| `codex` | `.codex/skills/harness/` alongside the shared tree | keeps custom agents inactive |
| `forgecode` | `.forge/skills/harness/` alongside the shared tree | reserve `.forge/agents/` for native agents |
| `droid` | `.factory/skills/harness/` alongside the shared tree | reserve `.factory/droids/` for native droids |
| `openhands` | shared tree only | keep optional setup in `.openhands/` |
| `aider` | shared tree only | add `AGENTS.md` to Aider's read list |

See the [compatibility matrix](compatibility/README.html) for exact paths and
client-specific notes.

## Verify and repeat safely

Preview a resolved install without changing any destination:

~~~shell
python3 scripts/install_harness.py \
  --scope project \
  --target /path/to/repo \
  --layout codex \
  --dry-run
~~~

Re-running an install fails when a destination already exists. Use
`--force` only after confirming the destination is the Harness tree you intend
to replace:

~~~shell
python3 scripts/install_harness.py \
  --scope project \
  --target /path/to/repo \
  --layout standard \
  --force
~~~

During local Harness development, `--mode symlink` can point a destination at
this checkout so changes are visible immediately:

~~~shell
python3 scripts/install_harness.py \
  --scope project \
  --target /path/to/repo \
  --layout standard \
  --mode symlink
~~~

Use symlink mode only when the target intentionally depends on this working
copy. Use the default copy mode for a standalone install.

The installer does not create or update the target repo's `AGENTS.md`,
`README.md`, or docs. The [AGENTS Authoring Guide](https://github.com/SaehwanPark/meta-harness/blob/main/.agents/skills/harness/references/agents-md-guide.md)
explains how to add durable target-repository guidance intentionally.

> [!TIP]
> If you are unsure which client path to use, start with `standard`. The
> shared `.agents/skills/harness/` tree is the portable source; native mirrors
> are optional discovery conveniences.

## Validate the repository

Run the same checks used by continuous integration from the Meta Harness root:

~~~shell
python3 scripts/test_install_harness.py
python3 scripts/validate_codex_port.py
~~~

## Next step

After installation, use a prompt that names the goal, output, and constraint.
The [prompt library](sample-prompts.html) includes small starting points.
