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

## Generated Skill Discovery

- Generated `SKILL.md` files should begin with YAML frontmatter.
- Include at least `name` and `description` before the markdown heading so Codex can reliably discover repo-specific generated skills.

## Optional Native Agent Adapter

Harness remains usable without native Codex agents. When a portable workflow has independent work units and benefits from context isolation, specialization, or parallel read-heavy work, use the [optional Codex agent adapter](../../.agents/skills/harness/references/codex-agent-adapter.md) to map the workflow onto Codex subagents.

The deployable skill includes an inactive [custom-agent TOML template](../../.agents/skills/harness/templates/codex-agent.toml). Installing Harness does not copy it into `.codex/agents/` or activate an agent. Copy and adapt it intentionally only when the target repository needs a stable execution profile.

- Keep skills responsible for reusable knowledge and workflow.
- Keep custom agents responsible for optional runtime execution settings.
- Prefer bounded read-heavy delegation.
- Require non-overlapping ownership or isolated worktrees for parallel writes.
- Leave model and reasoning settings inherited unless the repository has measured reasons to pin them.
