# OpenHands Compatibility

## Install Paths

- Shared project install: `.agents/skills/harness/`
- Shared user install: `~/.agents/skills/harness/`
- OpenHands repo customization: `.openhands/`

## Install Commands

Project install for OpenHands:

```shell
python3 scripts/install_harness.py --scope project --target /path/to/repo --layout openhands
```

User-level shared install:

```shell
python3 scripts/install_harness.py --scope user --layout openhands
```

## When To Use Shared Skills Vs OpenHands Repo Customization

- Use `.agents/skills/harness/` for reusable Harness instructions, references, and shared workflow contracts.
- Use `.openhands/setup.sh`, `.openhands/hooks.json`, or `.openhands/pre-commit.sh` only for repository-specific execution setup, enforcement hooks, or pre-commit behavior.
- Prefer the project-level shared install when you are working inside a cloned repository. Use the user-level shared install when your OpenHands environment exposes shared skills across repositories.
