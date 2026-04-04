# Skill Writing Guide

This guide explains how to write portable specialist skills that are easy to select, easy to maintain, and cheap to load.

## 1. Start with Selection Clarity

Every generated skill should make two things obvious at the top:

- when the skill should be used
- what inputs the skill needs to do useful work

That pair replaces vague trigger logic. If a reader cannot tell where the skill applies, the skill boundary is not ready.

### Good Pattern

```markdown
## When to Use
- use this skill for API documentation generation from an existing codebase
- use it when the request needs endpoint inventory, usage examples, and schema notes
- do not use it for product marketing copy or high-level architecture review

## Required Inputs
- repository or API source files
- desired output format
- audience and depth
```

### Weak Pattern

```markdown
This skill helps with documentation.
```

Too broad, no boundary, no input contract.

## 2. Keep the Main Skill Lean

The main `SKILL.md` should contain:

- purpose
- selection boundary
- input contract
- workflow
- output contract
- validation notes

Move bulky domain detail into `references/`. A good rule of thumb is that a fresh reader should understand the skill's decision boundary in under a minute.

## 3. Write Why-First Instructions

Explain the reason behind non-obvious rules.

### Weak

```markdown
Always compare the API shape to the UI types.
```

### Better

```markdown
Compare the API shape to the UI types because boundary mismatches often pass local checks while failing in integration. Reading both sides prevents false confidence from isolated validation.
```

Reason-first guidance survives edge cases better than flat commands.

## 4. Define an Output Contract

If the output structure matters, say so explicitly.

```markdown
## Outputs
- `docs/api/endpoints.md` with endpoint list and auth notes
- `docs/api/examples.md` with request and response examples
- `_workspace/qa_api_gaps.md` for missing information discovered during validation
```

Use deterministic names. Another person should be able to predict the artifact names without rereading the whole skill.

## 5. Use Examples Instead of Long Explanations

Examples compress meaning.

```markdown
## Example Review Statuses
- `pass`: no blocking issues; output is ready
- `fix`: targeted issues; revision is cheaper than regeneration
- `redo`: the output is directionally wrong and should be regenerated
```

Use examples where the format or decision boundary is easier to show than to describe.

## 6. Progressive Disclosure

Use `references/` when the skill needs depth without turning the main file into a wall of text.

### Pattern 1: Domain Split

```text
data-docs/
├── SKILL.md
└── references/
    ├── finance.md
    ├── sales.md
    └── product.md
```

### Pattern 2: Conditional Detail

```markdown
## Validation
For schema diffs, use the standard checks in `references/schema-validation.md`.
For migration backfills, read `references/backfill-playbook.md` before writing steps.
```

### Pattern 3: Large Reference File Structure

If a reference file grows large, add a table of contents near the top and split clearly by topic.

## 7. Bundle Scripts Only for Repeated, Deterministic Work

Add a helper script when it removes repeated setup or repeated manual validation.

Good candidates:

- a structure validator used on every iteration
- a deterministic report normalizer
- a schema comparison helper

Bad candidates:

- one-off experiments
- scripts that encode policy that belongs in the skill text
- scripts that only hide unclear workflow design

## 8. Recommended Section Order

Most specialist skills work well with this order:

```markdown
# Skill Name

## When to Use
## Required Inputs
## Workflow
## Outputs
## Validation
## References
```

Add domain-specific sections only when they prevent a predictable mistake.

## 9. Data Schema Standards

When a skill participates in evaluation, use stable schemas for test metadata and grading results.

### `eval_metadata.json`

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "User task prompt",
  "assertions": [
    "The artifact contains X",
    "A file with Y format is created"
  ]
}
```

### `grading.json`

```json
{
  "expectations": [
    {
      "text": "The artifact includes a migration table",
      "passed": true,
      "evidence": "Found in section 3"
    }
  ],
  "summary": {
    "passed": 1,
    "failed": 0,
    "total": 1,
    "pass_rate": 1.0
  }
}
```

### `timing.json`

```json
{
  "duration_ms": 23332,
  "total_duration_seconds": 23.3,
  "notes": "Optional timing capture for comparison runs"
}
```

## 10. What Not to Include

Remove content that does not change decisions:

- generic background knowledge the model already knows
- exhaustive prose that can be replaced by a short example
- platform-specific assumptions that do not belong to the repository
- duplicate instructions already enforced by `AGENTS.md` or the orchestrator spec
