# Installation

Meta Harness ships with a repo-local bootstrap installer so you can install the canonical Harness skill into a project or into a user-level shared skills directory.

## Project Install

Install the shared Harness skill into an existing repository:

```shell
python3 scripts/install_harness.py --scope project --target /path/to/repo --layout standard
```

The installer creates `.agents/skills/harness/` inside the target repository and does not create or update the target repo's `AGENTS.md`, `README.md`, or docs.

## User-Level Install

Install Harness as a shared skill for agents that scan user-level `.agents/skills/` directories:

```shell
python3 scripts/install_harness.py --scope user --layout standard
```

The installed skill tree includes the AGENTS authoring guide, but repo-level context files remain repo-owned and should be written intentionally.

## Layout Options

- `standard`: installs the shared `.agents/skills/harness/` tree only
- `forgecode`: also mirrors Harness into `.forge/skills/harness/` or `~/forge/skills/harness/`
- `droid`: also mirrors Harness into `.factory/skills/harness/`
- `openhands`: uses the shared `.agents/skills/harness/` tree
- `codex`: also mirrors Harness into `.codex/skills/harness/`
- `aider`: uses the shared tree and prints the `.aider.conf.yml` follow-up snippet for `AGENTS.md`

## Local Development

1. Read [AGENTS.md](../AGENTS.md) for repo-wide rules.
2. Read [.agents/skills/harness/SKILL.md](../.agents/skills/harness/SKILL.md) for the main workflow.
3. Run `python3 scripts/test_install_harness.py` to smoke test the installer.
4. Run `python3 scripts/validate_codex_port.py` for structural validation.

## Notes

- The canonical source remains in `.agents/skills/harness/` in this repository.
- Use `.agents/skills/harness/references/agents-md-guide.md` when a target repo needs a short, deliberate `AGENTS.md`.
- See [Compatibility Guides](compatibility/README.md) for agent-specific path and config details.
- Use `--mode symlink` if you want the installed skill to point back to this repository during local iteration.
