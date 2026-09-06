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

Current project version: `0.8.4`. Meta Harness actively supports Pi, Codex,
Antigravity, and Cursor CLI/Agent through one portable workflow model and
runtime adapters. Generic Agent Skills use is best effort; legacy client
layouts are unverified and deprecated. See the [changelog](CHANGELOG.md) for
the checkpoint-based project history.

## Start here

The [Meta Harness documentation portal](https://saehwanpark.github.io/meta-harness/)
is the recommended entry point. It covers installation, the Phase 0 inventory
and drift audit, the six execution phases, architecture patterns, prompt design,
compatibility, and durable output specs.

For a quick project install:

~~~shell
python3 scripts/install_harness.py install \
  --scope project \
  --target /path/to/repo \
  --agent generic \
  --non-interactive
~~~

Then ask for a goal-shaped workflow, for example:

~~~text
Design a reusable research harness for this repository.
Keep the handoffs deterministic and validate one normal and one failure flow.
~~~

## What the repository contains

- a Phase 0 inventory and drift audit followed by six execution phases from domain analysis through validation;
- six coordination patterns: Pipeline, Fan-out/Fan-in, Expert Pool,
  Producer-Reviewer, Supervisor, and Hierarchical Delegation;
- portable skills under `.agents/skills/`;
- durable team specs and role contracts under `docs/harness/`;
- deterministic `_workspace/` handoffs when inspection or resumption matters;
- a shared CLI/TUI installer planner with portable layout and optional native profiles;
- audit, doctor, compile, and validation commands over inspectable plans;
- removable runtime adapters for Pi, Codex, Antigravity, and Cursor CLI/Agent
  without forking the canonical skill;
- explicit capability degradation and rippability rules for runtime profiles.

## Phase 0 audit plus six-phase workflow

| Phase | Question it answers |
| --- | --- |
| Inventory and drift audit | What already exists, what is stale, and what operation is safe? |
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
python3 scripts/install_harness.py install \
  --scope project \
  --target /path/to/repo \
  --agent pi \
  --agent cursor \
  --non-interactive
~~~

Install as a user-level shared skill:

~~~shell
python3 scripts/install_harness.py install \
  --scope user \
  --agent generic \
  --non-interactive
~~~

`--agent` is repeatable. Runtime-specific installation and capability guidance
for the actively supported Pi, Codex, Antigravity, and Cursor CLI/Agent targets
is in the [compatibility matrix](docs/compatibility/README.md). Generic clients
are best-effort only; ForgeCode, Droid, OpenHands, and Aider are retained as
unverified, deprecated migration notes. Use `audit`, `doctor`, `compile`, and
`validate` for inspectable lifecycle operations.

The installer owns only explicitly planned skill/profile destinations. The
target repository keeps ownership of its `AGENTS.md`, `README.md`, and
documentation. Legacy `--layout` flags remain compatibility aliases and are
unverified/deprecated; use `--agent` for new automation.

## Runtime support and architecture

The portable contract is authoritative: `.agents/skills/` contains reusable
behavior, `docs/harness/` contains role and team contracts, and `_workspace/`
contains durable handoffs. Runtime-native profiles are removable adapters, not
sources of truth. Read the [architecture guide](docs/architecture/README.md)
and [compatibility matrix](docs/compatibility/README.md) before adding a
runtime-specific integration.

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
python3 scripts/validate_skills.py
python3 scripts/validate_adapters.py
python3 scripts/test_install_harness.py
python3 scripts/test_install_planner.py
python3 scripts/test_installer_tui.py
python3 scripts/test_profile_compilation.py
python3 scripts/test_audit_harness.py
python3 scripts/validate_codex_port.py
~~~

The Pages check protects rendered source and navigation. Portable-skill and
adapter validators protect frontmatter, links, capability guidance, and
fixtures. The installer tests cover project/user scopes, multi-runtime plans,
legacy aliases, dry runs, idempotent updates, conflicts, profiles, and symlink
mode. The Codex-port validator protects canonical paths, synchronized docs,
and legacy-path exclusions.

## License

Apache 2.0. See [LICENSE](LICENSE).
