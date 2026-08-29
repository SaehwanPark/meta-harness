<p align="center">
  <img src="meta_harness_banner.png" alt="Meta Harness banner" width="600">
</p>

<p align="center">
  <strong>Portable agent workflow design</strong><br>
  Turn a project goal into reusable skills and inspectable handoffs.
</p>

<p align="center">
  <a href="https://saehwanpark.github.io/meta-harness/">Documentation</a> ·
  <a href="https://github.com/SaehwanPark/meta-harness">Source</a> ·
  <a href="LICENSE">Apache 2.0</a>
</p>

# Meta Harness

Meta Harness is a runtime-neutral meta-skill for designing domain-specific
workflows, reusable specialist skills, and deterministic handoff artifacts.
It is adapted from [the original Harness project](https://github.com/revfactory/harness)
and distributed under the Apache 2.0 license.

Current project version: `0.5.0`. See the [changelog](CHANGELOG.md) for the
checkpoint-based project history.

## Start here

The [Meta Harness documentation portal](https://saehwanpark.github.io/meta-harness/)
is the recommended entry point. It covers installation, the six-phase workflow,
architecture patterns, prompt design, compatibility, and durable output specs.

For a quick project install:

~~~shell
python3 scripts/install_harness.py \
  --scope project \
  --target /path/to/repo \
  --layout standard
~~~

Then ask for a goal-shaped workflow, for example:

~~~text
Design a reusable research harness for this repository.
Keep the handoffs deterministic and validate one normal and one failure flow.
~~~

## What the repository contains

- a six-phase workflow from domain analysis through validation;
- six coordination patterns: Pipeline, Fan-out/Fan-in, Expert Pool,
  Producer-Reviewer, Supervisor, and Hierarchical Delegation;
- portable skills under `.agents/skills/`;
- durable team specs and role contracts under `docs/harness/`;
- deterministic `_workspace/` handoffs when inspection or resumption matters;
- a bootstrap installer with standard and agent-specific layouts;
- a removable Codex adapter without making Codex a canonical dependency.

## Six-phase workflow

| Phase | Question it answers |
| --- | --- |
| Domain analysis | What is this project, task, and quality bar? |
| Team architecture | What coordination shape earns its complexity? |
| Role and artifact definition | Who owns each output and handoff? |
| Skill generation | What reusable behavior belongs in a skill? |
| Integration and orchestration | How does information move between phases? |
| Validation and testing | Does the workflow work, fail clearly, and stay maintainable? |

Read the [workflow guide](docs/guides/workflow.md) and
[pattern guide](docs/guides/patterns.md) for the operational details.

## Installation

Install into a project:

~~~shell
python3 scripts/install_harness.py \
  --scope project \
  --target /path/to/repo \
  --layout standard
~~~

Install as a user-level shared skill:

~~~shell
python3 scripts/install_harness.py --scope user --layout standard
~~~

Use `--layout codex`, `--layout forgecode`, or `--layout droid` when a native
mirror is useful. `openhands` and `aider` keep the shared skill path and add
client-specific follow-up guidance. See the
[installation guide](docs/installation.md) and
[compatibility matrix](docs/compatibility/README.md).

The installer owns only the skill destinations. The target repository keeps
ownership of its `AGENTS.md`, `README.md`, and documentation.

## Repository contract

The canonical source is `.agents/skills/harness/SKILL.md`. Generated skills
must begin with YAML frontmatter containing at least `name` and `description`.
Use `docs/harness/` for durable team specs and role briefs, and `_workspace/`
for deterministic intermediate artifacts that need inspection, resumption, or
cross-agent synthesis.

Keep `AGENTS.md` short and repo-wide. Put conditional detail in skills,
references, or project documentation. Prefer direct work for small tasks and
add workers only when boundaries, ownership, synthesis, and partial-failure
behavior are explicit.

## Authoring guidance

Read the AGENTS Authoring Guide
(`.agents/skills/harness/references/agents-md-guide.md`) when a target repository
needs durable repo-wide rules. Keep temporary model-specific recovery logic in
a rippable harness layer. Every generated skill starts with YAML frontmatter
and declares its `name` and `description`.

## Validation

Run the repository checks from the project root:

~~~shell
python3 scripts/validate_pages.py
python3 scripts/test_install_harness.py
python3 scripts/validate_codex_port.py
~~~

The first check protects the rendered Pages source and internal navigation.
The installer smoke test exercises project/user scopes, layouts, dry runs,
replacement, and symlink mode. The Codex-port validator protects canonical
paths, required references, frontmatter guidance, and legacy-path exclusions.

## License

Apache 2.0. See [LICENSE](LICENSE).
