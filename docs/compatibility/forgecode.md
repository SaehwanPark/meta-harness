# ForgeCode Compatibility

## Install Paths

- Shared project install: `.agents/skills/harness/`
- Shared user install: `~/.agents/skills/harness/`
- ForgeCode project mirror: `.forge/skills/harness/`
- ForgeCode user mirror: `~/forge/skills/harness/`

## Install Commands

Project install with ForgeCode mirror:

```shell
python3 scripts/install_harness.py --scope project --target /path/to/repo --layout forgecode
```

User-level install with ForgeCode mirror:

```shell
python3 scripts/install_harness.py --scope user --layout forgecode
```

## When To Use Shared Skills Vs Native Agents

- Use `.agents/skills/harness/` for reusable Harness guidance you want other agents to share.
- Use `.forge/skills/harness/` when you want ForgeCode's native skill discovery path in addition to the shared one.
- Use `.forge/agents/` or `~/forge/agents/` only for ForgeCode-specific agents with their own tool or model policy. Do not move shared Harness workflow logic there unless it is truly ForgeCode-only.
