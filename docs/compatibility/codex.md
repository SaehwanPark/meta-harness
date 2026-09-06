---
title: Codex Compatibility
description: Use the canonical skill with Codex and optionally generate native execution profiles.
layout: default
---

# Codex Compatibility

Codex is a first-class Meta Harness target. The portable skill remains the
source of truth; generated native profiles are optional execution material.

## Paths and install commands

- Shared project skill: `.agents/skills/harness/`
- Shared user skill: `~/.agents/skills/harness/`
- Optional native profiles: `.codex/agents/` or the user-level Codex agents directory
- Deprecated project mirror: `.codex/skills/harness/`
- Deprecated user mirror: `~/.codex/skills/harness/`

Use the modern runtime selection command:

```shell
meta-harness install \
  --scope project --target /path/to/repo \
  --agent codex --non-interactive
meta-harness install \
  --scope user \
  --agent codex --non-interactive
```

The modern `--agent codex` path installs the canonical shared skill and can
also generate optional `.codex/agents/` profiles. It does not create the
deprecated `.codex/skills/harness/` mirror. Do not put reusable domain
behavior in `.codex/agents/`; keep those files as runtime profiles that can be
regenerated or removed.

## Capability profile

Codex can discover Agent Skills and can use native/custom agent definitions.
Worker spawning, write isolation, communication, permission handling, model
and reasoning routing, and persistence vary with the Codex surface and project
configuration. Treat ownership as advisory unless the selected execution
profile provides isolation or enforcement.

Use the portable role contract and request semantic model policies (`inherit`,
`balanced`, or `strong`) rather than requiring a model ID. Keep delegation
shallow and assign non-overlapping files to parallel workers.

## Degradation

If a requested native capability is unavailable, lower it explicitly: use an
isolated workspace, state non-overlapping ownership, or serialize conflicting
work. If messaging or durable state is unavailable, use parent-mediated
summaries and `_workspace/` artifacts. Never assume a native profile makes a
portable guarantee enforceable.

## Rippability

Removing `.codex/agents/` or `.codex/skills/harness/` leaves the shared
`.agents/skills/harness/` source and portable `docs/harness/` contracts intact.
See the [portable contract](../architecture/portable-contract.html) and
[compatibility matrix](README.html). The optional [codex-agent-adapter.md](https://github.com/SaehwanPark/meta-harness/blob/main/.agents/skills/harness/references/codex-agent-adapter.md)
and `codex-agent.toml` template describe removable native execution material.
Generated skill files must use YAML frontmatter with `name` and `description`.
