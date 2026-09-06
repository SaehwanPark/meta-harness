---
title: Aider Compatibility (Deprecated)
description: Unverified and deprecated migration guidance for legacy Aider setups.
layout: default
---

# Aider Compatibility (Deprecated)

Aider is not a first-class Meta Harness target and is no longer actively
verified. Existing `.aider.conf.yml` settings remain user-owned; Meta Harness
does not promise native agent or subagent behavior for Aider.

For best-effort use, install the portable skill at `.agents/skills/harness/`
and follow the [generic guide](generic.html). If Aider supports an explicit
read list in your setup, add `AGENTS.md` there and verify all other behavior
manually.

Historical (deprecated) paths and commands were `.agents/skills/harness/`,
`~/.agents/skills/harness/`, `.aider.conf.yml`, `~/.aider.conf.yml`,
`python3 scripts/install_harness.py --scope project --target /path/to/repo --layout aider`,
and `python3 scripts/install_harness.py --scope user --layout aider`.
The historical read-list shape was:

```yaml
read:
  - AGENTS.md
```

These references support migration only.
