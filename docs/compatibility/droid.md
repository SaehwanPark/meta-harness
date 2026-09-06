---
title: Droid Compatibility (Deprecated)
description: Unverified and deprecated migration guidance for legacy Droid layouts.
layout: default
---

# Droid Compatibility (Deprecated)

Droid/Factory is not a first-class Meta Harness target and is no longer
actively verified. Existing `.factory/skills/` or `.factory/droids/` files may
remain, but their capabilities and discovery behavior are unverified.

For best-effort use, install the portable skill at `.agents/skills/harness/`
and follow the [generic guide](generic.html). Keep any native files removable
and do not move portable workflow semantics into them.

Historical (deprecated) paths were `.agents/skills/harness/`,
`~/.agents/skills/harness/`, `.factory/skills/harness/`, and
`~/.factory/skills/harness/`. The old commands
`python3 scripts/install_harness.py --scope project --target /path/to/repo --layout droid`
and `python3 scripts/install_harness.py --scope user --layout droid`
are migration references only.
