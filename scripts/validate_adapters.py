#!/usr/bin/env python3
"""Validate first-class runtime adapter guidance and structural fixtures."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADAPTERS = {
  "pi": ROOT / ".agents/skills/harness/references/pi-agent-adapter.md",
  "codex": ROOT / ".agents/skills/harness/references/codex-agent-adapter.md",
  "antigravity": ROOT / ".agents/skills/harness/references/antigravity-agent-adapter.md",
  "cursor": ROOT / ".agents/skills/harness/references/cursor-agent-adapter.md",
  "generic": ROOT / ".agents/skills/harness/references/generic-agent-adapter.md",
}
FIXTURE_NAMES = (*ADAPTERS.keys(),)
REQUIRED_TERMS = (
  "skill",
  "role",
  "write",
  "communication",
  "model",
  "unavailable",
  "fallback",
)
STATUSES = ("supported", "supported_with_extension", "advisory", "unsupported")


def validate_adapters(root: str | Path = ROOT) -> list[str]:
  base = Path(root).expanduser().resolve()
  errors: list[str] = []
  adapters_root = base / ".agents" / "skills" / "harness" / "references"
  for name in ADAPTERS:
    path = adapters_root / f"{name}-agent-adapter.md"
    if not path.is_file():
      errors.append(f"missing adapter: {path.relative_to(base)}")
      continue
    text = path.read_text(encoding="utf-8").casefold()
    for term in REQUIRED_TERMS:
      if term not in text:
        errors.append(f"{path.relative_to(base)} is missing adapter guidance: {term}")
    if not any(status in text for status in STATUSES):
      errors.append(f"{path.relative_to(base)} does not use capability status vocabulary")

  fixtures_root = base / "tests" / "fixtures"
  for name in FIXTURE_NAMES:
    fixture = fixtures_root / name
    manifest = fixture / "README.md"
    if not fixture.is_dir():
      errors.append(f"missing adapter fixture directory: {fixture.relative_to(base)}")
      continue
    if not manifest.is_file():
      errors.append(f"missing adapter fixture manifest: {manifest.relative_to(base)}")
      continue
    text = manifest.read_text(encoding="utf-8").casefold()
    for term in ("runtime:", "portable_skill:", "status:", "degradation:"):
      if term not in text:
        errors.append(f"{manifest.relative_to(base)} is missing fixture field: {term}")
    if list(fixture.rglob("SKILL.md")):
      errors.append(f"{fixture.relative_to(base)} duplicates portable SKILL.md content")
  return errors


def build_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(description="Validate runtime adapters and fixtures")
  parser.add_argument("--root", default=str(ROOT))
  return parser


def main(argv: list[str] | None = None) -> int:
  args = build_parser().parse_args(argv)
  errors = validate_adapters(args.root)
  if errors:
    for error in errors:
      print(f"FAIL: {error}", file=sys.stderr)
    return 1
  print("OK: Runtime adapter validation passed.")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
