# Droid Compatibility

## Install Paths

- Shared project install: `.agents/skills/harness/`
- Shared user install: `~/.agents/skills/harness/`
- Droid project mirror: `.factory/skills/harness/`
- Droid user mirror: `~/.factory/skills/harness/`

## Install Commands

Project install with Droid mirror:

```shell
python3 scripts/install_harness.py --scope project --target /path/to/repo --layout droid
```

User-level install with Droid mirror:

```shell
python3 scripts/install_harness.py --scope user --layout droid
```

## When To Use Shared Skills Vs Native Droids

- Use `.agents/skills/harness/` for the reusable Harness workflow and shared references.
- Use `.factory/skills/harness/` when you want Droid's native skill discovery path in the same install.
- Use `.factory/droids/` or `~/.factory/droids/` only for Droid subagents that need their own tools, model preference, or delegation policy. Keep general Harness guidance in the shared skill tree.
