<p align="center">
  <img src="meta_harness_banner.png" alt="Harness Banner" width="600">
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License"></a>
  <img src="https://img.shields.io/badge/Harness-Portable-black.svg" alt="Portable Harness">
</p>

# Meta Harness

Meta Harness is a portable, standards-first meta-skill for designing domain-specific workflows, reusable specialist skills, and deterministic handoff artifacts.

Current project version: `0.2`. See [Changelog](CHANGELOG.md) for checkpoint-based version history.

Adapted from [the original Harness project](https://github.com/revfactory/harness) and distributed here under the same [Apache 2.0](LICENSE) license.

## What This Adds

Compared to the original Claude Code-based Harness, this project adds:

- a standards-first repository layout built around `AGENTS.md`, `.agents/skills/`, and `docs/harness/`
- runtime-neutral artifact contracts based on skills, team specs, and deterministic `_workspace/` handoffs
- a repo-local bootstrap installer for project-level and user-level skill installs
- a tighter maintenance loop through repo-local validation and simpler, platform-independent conventions

## What It Includes

- a 6-phase workflow for analysis, architecture, generation, integration, and validation
- 6 architecture patterns: Pipeline, Fan-out/Fan-in, Expert Pool, Producer-Reviewer, Supervisor, and Hierarchical Delegation
- an autonomous experimentation workflow profile for user-controlled compute
- repo-local skills under `.agents/skills/`
- durable output specs under `docs/harness/`
- deterministic `_workspace/` handoff conventions
- a small bootstrap installer plus validation and smoke-test scripts

## Docs

- [Installation](docs/installation.md)
- [Compatibility Guides](docs/compatibility/README.md)
- [Sample Prompts](docs/sample-prompts.md)
- [Changelog](CHANGELOG.md)
- [Harness Output Specs](docs/harness/README.md)
- [Starter Research Example](docs/harness/starter-research/README.md)
- [Orchestrator Template](.agents/skills/harness/references/orchestrator-template.md)

## Repository Layout

```text
meta-harness/
├── AGENTS.md
├── .agents/skills/harness/
│   ├── SKILL.md
│   └── references/
├── docs/harness/README.md
├── docs/harness/starter-research/
├── scripts/install_harness.py
├── scripts/test_install_harness.py
├── scripts/validate_codex_port.py
└── LICENSE
```

## Install

Install into a project:

```shell
python3 scripts/install_harness.py --scope project --target /path/to/repo --layout standard
```

Install as a user-level shared skill:

```shell
python3 scripts/install_harness.py --scope user --layout standard
```

Use `--layout forgecode`, `--layout droid`, `--layout openhands`, or `--layout aider` when you want a client-specific mirror or follow-up guidance.
See [Compatibility Guides](docs/compatibility/README.md) for path mappings and agent-specific follow-up.

## Use

1. Read [AGENTS.md](AGENTS.md).
2. Read the main skill at [.agents/skills/harness/SKILL.md](.agents/skills/harness/SKILL.md).
3. Generate the smallest durable artifact set that fits the domain:
   - `.agents/skills/<domain>-orchestrator/SKILL.md`
   - `.agents/skills/<specialist>/SKILL.md`
   - `docs/harness/<domain>/team-spec.md`
   - `_workspace/{phase}_{role}_{artifact}.md`

Good requests for Harness:

```text
Build a reusable research harness for this repository.
Design a review workflow with explicit QA handoffs.
Define specialist skills and a team spec for this domain.
Design an autonomous experiment harness for this repository with a fixed metric and a deterministic results ledger.
```

## Workflow and Patterns

The main skill preserves the 6-phase workflow:

1. Domain Analysis
2. Team Architecture Design
3. Role and Artifact Definition Generation
4. Skill Generation
5. Integration and Orchestration
6. Validation and Testing

Pattern guidance lives in [.agents/skills/harness/references/agent-design-patterns.md](.agents/skills/harness/references/agent-design-patterns.md). Output-spec conventions live in [docs/harness/README.md](docs/harness/README.md).
Start from the [orchestrator template](.agents/skills/harness/references/orchestrator-template.md) when you need a durable workflow spec, or adapt the [starter research example](docs/harness/starter-research/README.md) when you want a concrete minimal package.

## Validation

```shell
python3 scripts/test_install_harness.py
python3 scripts/validate_codex_port.py
```

The smoke test checks the installer across project and user scopes. The validator checks required files, README links, main-skill headings, pattern coverage, and the absence of removed runtime-specific paths in the canonical docs.

## License

Apache 2.0
