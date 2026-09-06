---
title: Interactive Installer
description: Use the keyboard-friendly Meta Harness installer while sharing the CLI planner.
layout: default
---

# Interactive Installer

On a real terminal, `meta-harness install` opens the interactive frontend. It
is a frontend over the same `InstallRequest` and `InstallPlan` used by the
CLI; it does not contain a second filesystem mutation engine.

## Selection flow

1. Choose **Project** or **User** scope with the scope radio controls.
2. Enter an existing project target when project scope is selected.
3. Toggle first-class runtime checkboxes: Pi, Codex, Antigravity, and Cursor
   CLI/Agent; select Generic Agent Skills separately for best-effort mode.
4. Choose the optional Pi safe-agent-team integration, native profile
   generation, semantic model policy, and Copy/Symlink mode.
5. Review the plan preview before applying it.

The dependency-free frontend accepts all selections from the keyboard: enter
scope, target, comma-separated runtime numbers, toggles, and single-letter
actions. The compact line-mode fallback uses numbered choices when the
terminal is too small for the full view.

## Preview and conflicts

The preview shows every `CREATE`, `UPDATE`, `KEEP`, `SKIP`, `REMOVE`, and
`CONFLICT` operation. The installer does not mutate anything while the preview
is open. A conflict screen offers **Inspect**, **Repair**, or **Cancel**;
repair retries only managed Harness artifacts with an explicit force choice,
never overwriting an unknown user path. Inspect leaves the plan unchanged;
cancel is the default.

A dry-run action renders the same plan and exits without writing. The final
confirmation applies only after all destinations pass preflight, so one
user-owned conflict cannot leave a partial multi-runtime installation.

## Non-TTY behavior

Piped, CI, and redirected sessions never attempt to render the TUI. Pass
`--non-interactive` with explicit `--scope`, `--target` when needed, and one or
more `--agent` values. If required values are missing, the CLI fails with an
actionable message rather than guessing or silently opening a terminal UI.

See the [CLI guide](cli.html), [main installation guide](../installation.html),
and [compatibility matrix](../compatibility/README.html) for deterministic
commands and runtime capability fallbacks.
