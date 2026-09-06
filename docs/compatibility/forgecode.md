---
title: ForgeCode Compatibility (Deprecated)
description: Unverified and deprecated migration guidance for legacy ForgeCode layouts.
layout: default
---

# ForgeCode Compatibility (Deprecated)

ForgeCode is not a first-class Meta Harness target and is no longer actively
verified. Existing `.forge/skills/` or `.forge/agents/` files may remain in a
repository, but this project makes no runtime capability or maintenance
promise for them.

For best-effort use, install the portable skill at `.agents/skills/harness/`
and follow the [generic guide](generic.html). Do not treat a ForgeCode mirror
as a second source of truth. Remove or regenerate legacy native profiles only
after reviewing their ownership.

Historical (deprecated) paths were `.agents/skills/harness/`,
`~/.agents/skills/harness/`, `.forge/skills/harness/`, and `~/forge/skills/harness/`.
The old commands
`python3 scripts/install_harness.py --scope project --target /path/to/repo --layout forgecode`
and `python3 scripts/install_harness.py --scope user --layout forgecode`
remain documented only so existing automation can be migrated; they are not a
current support claim.
