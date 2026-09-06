---
title: OpenHands Compatibility (Deprecated)
description: Unverified and deprecated migration guidance for legacy OpenHands setups.
layout: default
---

# OpenHands Compatibility (Deprecated)

OpenHands is not a first-class Meta Harness target and is no longer actively
verified. Existing `.openhands/` setup or hook files are repository-owned and
are not generated or maintained by Meta Harness.

For best-effort use, install the portable skill at `.agents/skills/harness/`
and follow the [generic guide](generic.html). Verify skills, permissions,
workspace behavior, and handoffs in your own OpenHands setup.

Historical (deprecated) paths and commands were `.agents/skills/harness/`,
`~/.agents/skills/harness/`, `.openhands/`,
`python3 scripts/install_harness.py --scope project --target /path/to/repo --layout openhands`,
and `python3 scripts/install_harness.py --scope user --layout openhands`.
They are retained for migration, not as a support guarantee.
