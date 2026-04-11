# Repository Agents Guide

Keep this file short and repo-wide. Put conditional or bulky guidance in linked docs instead of here.

## What

- Meta Harness is a portable repository for designing repo-local agent harnesses.
- The canonical Harness source lives in [.agents/skills/harness/](.agents/skills/harness/).
- Durable artifact contracts live in [docs/harness/README.md](docs/harness/README.md); `_workspace/` is for deterministic intermediate handoffs.

## Why

- This repo exists to keep harness design portable, repo-local, and easy to update as models improve.
- Prefer simple, rippable coordination over runtime-specific orchestration or sticky recovery logic.

## How

- When changing canonical paths, workflow guidance, or generated artifact contracts, update [README.md](README.md) and [docs/harness/README.md](docs/harness/README.md) in the same change.
- Validate with `python3 scripts/test_install_harness.py` and `python3 scripts/validate_codex_port.py`.
- For deeper authoring guidance, read [.agents/skills/harness/SKILL.md](.agents/skills/harness/SKILL.md) and [.agents/skills/harness/references/agents-md-guide.md](.agents/skills/harness/references/agents-md-guide.md).
