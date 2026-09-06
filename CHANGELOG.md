# Changelog

This repository uses checkpoint-based versioning for the meta-harness project history.

## 0.8.4

- Extended release validation to enforce all runtime adapters, capability statuses, active-support claims, generic boundaries, and legacy deprecation boundaries.
- Documented the runtime capability rippability boundary.

## 0.8.3

- Aligned the Phase 0 inventory output with the durable handoff contract by naming its producer, consumer, path, schema, and completion state.

## 0.8.2

- Hardened the audit classification contract for migrations, skill-only updates, and stale native profiles.
- Clarified generic best-effort selection and fail-closed TUI behavior, and required an installed portable skill before standalone profile compilation.

## 0.8.1

- Hardened audit evidence, generated profile serialization, role overrides, and fail-closed TUI actions after the v0.8.0 release.
- Added explicit role selection to modern `install --native-profiles` invocations.

## 0.8.0

- Scope: complete the shared installer frontend and portable-role lowering path.
- Added: keyboard-friendly TUI selection/preview/conflict flow over the same planner, semantic model-policy selection, and generated role profiles for Codex, Antigravity, and Cursor CLI/Agent.
- Added: profile compilation tests, role-contract fixtures, rollback coverage, and release-gate validation for portable skills, adapters, TUI state, and rippability.

## 0.7.0

- Scope: replaced layout-centric installation with an inspectable, idempotent planner and modern runtime selection CLI.
- Added: `InstallRequest`, `InstallPlan`, explicit operation states, multi-runtime `--agent`, audit/doctor/compile/validate commands, conflict protection, and legacy deprecation warnings.
- Added: dependency-free portable skill and adapter validators, runtime fixtures, migration guidance, and planner scenario coverage.
- Changed: managed installations can be safely re-run; unknown user-owned destinations remain conflicts even with `--force`.

## 0.6.0

- Scope: clarified product positioning around one portable workflow model with four actively supported runtime adapters.
- Added: first-class compatibility guidance for Pi, Codex, Antigravity, and Cursor CLI/Agent, plus a generic best-effort path.
- Added: public architecture guides for the portable contract, runtime capabilities, role semantics, and handoffs.
- Changed: capability-aware degradation and rippability rules are now explicit; native profiles are removable and non-canonical.
- Deprecated: ForgeCode, Droid, OpenHands, and Aider compatibility claims are unverified migration notes rather than supported targets.

## 0.5.0

- Scope: refined user-facing documentation and a GitHub Pages documentation portal
- Added: Jekyll layout, responsive navigation, public workflow and pattern guides, and Pages deployment automation
- Added: dependency-free Pages source and rendered-link validation in repository CI
- Validation: installer smoke tests and Codex-port checks remain part of the release gate

## 0.4

- Checkpoint: `b2a4b3a` (`Merge pull request #8 from SaehwanPark/feat/harness-modernization`)
- Scope: modernized harness authoring and delegation guidance, including required generated-skill frontmatter, capability-aware worker selection, explicit write isolation and synthesis ownership, and proportional handoff persistence
- Added: an optional, removable Codex agent adapter and inactive custom-agent template
- Validation: expanded installer smoke coverage and documentation checks for the new skill contract and deployable adapter payload

## 0.3

- Checkpoint: `b24fc51` (`Merge pull request #4 from SaehwanPark/codex/v0.3-agents-harness-upgrade`)
- Scope: post-PR #4 release after the AGENTS authoring and rippable-harness updates were merged into `main`
- Added: concise repo-wide `AGENTS.md` guidance, progressive-disclosure authoring guidance, a Codex global skill mirror, broader drift validation, and CI-backed installer checks

## 0.2

- Checkpoint: `e962657` (`Merge pull request #1 from SaehwanPark/improve-portability-n-autonomousity`)
- Scope: post-PR #1 release after the portability and autonomous experimentation updates were merged into `main`
- Added: portable repository layouts, cross-agent compatibility guidance, bootstrap installation, and the autonomous experimentation workflow profile

## 0.1

- Checkpoint: `7fef0d0ef799d2ca33933c46f8c042149813d371`
- Scope: initial project version for the post-bootstrap repository state
- Established: the Codex-native Harness skill surface, Apache 2.0 licensing, and the streamlined repository baseline after legacy package removal
