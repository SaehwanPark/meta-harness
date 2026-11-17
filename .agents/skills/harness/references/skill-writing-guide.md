# Skill Writing Guide

Capture behavior people will reuse. First check whether an existing skill or tool already covers it. Keep rules that apply across the repository in `AGENTS.md`, and coordination between roles in the team spec.

## Write for selection and execution

- Use a kebab-case directory name and matching YAML `name`. Make `description` short and specific to the request that should trigger the skill. Try a similar request that should route elsewhere.
- Put the outcome and essential constraints up front. Include prerequisite inputs, output shapes, checks, and examples where they prevent a real mistake. Explain non-obvious rules briefly so the model can adapt to edge cases.
- Let the model choose its process within those boundaries. Prescribe order when a dependency, irreversible action, or quality gate requires it. Favor repo-specific conventions and evidence over generic planning, retry, or reporting scripts written in prose.
- Keep one canonical copy of each instruction. Link conditional guidance directly from the decision it informs. Keep references self-contained where possible, and use headings to make long references easy to scan.
- Bundle a script when deterministic work repeats and the script is cheaper and more reliable than reconstructing it. State its prerequisites, invocation, and success signal. Use the repository's existing tools first.
- Give durable outputs stable names only when people or tools depend on them. Use existing repository formats and tests when they fit.

## Example

```markdown
---
name: openapi-sync
description: Update the published API schema after a public endpoint changes.
---

# OpenAPI Sync

Use the route definitions and request/response types as the source of truth.
Run `make openapi` and review the resulting `docs/api/openapi.yaml` diff.
Check changed paths, required fields, and error responses against the route tests.
For breaking changes, follow the API migration policy in `references/migrations.md`.
```

Keep only the content the target repository actually needs. The example command and migration reference stand for project-specific resources that must exist before shipping.
