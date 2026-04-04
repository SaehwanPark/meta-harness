# Aider Compatibility

## Install Paths

- Shared project install: `.agents/skills/harness/`
- Shared user install: `~/.agents/skills/harness/`
- Aider config: `.aider.conf.yml` or `~/.aider.conf.yml`

## Install Commands

Project install for Aider:

```shell
python3 scripts/install_harness.py --scope project --target /path/to/repo --layout aider
```

User-level shared install for Aider:

```shell
python3 scripts/install_harness.py --scope user --layout aider
```

## Required Follow-Up

Tell Aider to read `AGENTS.md` by adding this snippet to the repo or home-level config file:

```yaml
read:
  - AGENTS.md
```

## When To Use Shared Skills Vs Native Aider Config

- Use `.agents/skills/harness/` for the reusable Harness instructions and references.
- Use `.aider.conf.yml` only for Aider configuration such as reading `AGENTS.md`.
- There is no separate Aider-native agent or subagent format to mirror Harness into, so the shared skill tree is the canonical install surface.
