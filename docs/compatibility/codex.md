# Codex Compatibility

## Install Paths

- Shared project install: `.agents/skills/harness/`
- Shared user install: `~/.agents/skills/harness/`
- Codex project mirror: `.codex/skills/harness/`
- Codex user mirror: `~/.codex/skills/harness/`

## Install Commands

Project install with Codex mirror:

```shell
python3 scripts/install_harness.py --scope project --target /path/to/repo --layout codex
```

User-level install with Codex mirror:

```shell
python3 scripts/install_harness.py --scope user --layout codex
```

## When To Use Shared Skills Vs Native Mirrors

- Use `.agents/skills/harness/` for reusable Harness guidance that should stay canonical and portable.
- Use `.codex/skills/harness/` when you want Codex's native discovery path in addition to the shared one.
- Keep Codex-specific setup in `.codex/` only when it is genuinely native behavior and not part of the reusable Harness workflow contract.
