#!/usr/bin/env python3
"""Validate portable Agent Skills structure without third-party dependencies."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RUNTIME_PATHS = (".codex/", ".cursor/", ".antigravity/", ".pi/", ".forge/", ".factory/")
OPERATIONAL_TERMS = re.compile(
  r"\b(must|required|canonical|install(?:ed)?|discover(?:y)?|source of truth|only)\b",
  re.IGNORECASE,
)


@dataclass(frozen=True)
class ValidationResult:
  errors: tuple[str, ...] = ()
  warnings: tuple[str, ...] = ()

  @property
  def ok(self) -> bool:
    return not self.errors


def _read(path: Path) -> str:
  return path.read_text(encoding="utf-8")


def _parse_frontmatter(path: Path, text: str) -> tuple[dict[str, str], str, list[str]]:
  errors: list[str] = []
  lines = text.splitlines()
  label = str(path)
  if not lines or lines[0].strip() != "---":
    return {}, text, [f"{label}: SKILL.md must start with YAML frontmatter"]
  try:
    end = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
  except StopIteration:
    return {}, text, [f"{label}: YAML frontmatter is not closed"]
  values: dict[str, str] = {}
  for line in lines[1:end]:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
      continue
    if ":" not in stripped:
      errors.append(f"{label}: invalid frontmatter line: {line}")
      continue
    key, value = stripped.split(":", 1)
    values[key.strip()] = value.strip().strip('"').strip("'")
  return values, "\n".join(lines[end + 1 :]), errors


def _is_local_link(target: str) -> bool:
  return not target.startswith(("#", "mailto:", "http://", "https://", "{{", "{%"))


def _link_targets(text: str) -> Iterable[str]:
  markdown = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")
  html = re.compile(r"(?:href|src)=[\"']([^\"']+)[\"']")
  for match in markdown.finditer(text):
    yield match.group(1).strip().split()[0]
  yield from (match.group(1).strip() for match in html.finditer(text))


def _check_links(path: Path, body: str, errors: list[str]) -> None:
  for target in _link_targets(body):
    if not _is_local_link(target):
      continue
    clean = target.split("#", 1)[0].split("?", 1)[0]
    if not clean:
      continue
    candidate = (path.parent / clean).resolve()
    source_candidate = candidate.with_suffix(".md") if clean.endswith(".html") else candidate
    if not candidate.exists() and not source_candidate.exists():
      errors.append(f"{path}: local link target does not exist: {target}")


def _check_references(path: Path, text: str, errors: list[str]) -> None:
  for reference in re.findall(r"(?:references|templates)/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*", text):
    candidate = (path.parent / reference).resolve()
    if not candidate.exists():
      errors.append(f"{path}: referenced bundled file does not exist: {reference}")


def _check_portable_boundary(path: Path, body: str, errors: list[str]) -> None:
  lines = body.splitlines()
  for line_number, line in enumerate(lines, start=1):
    if not any(token in line.casefold() for token in RUNTIME_PATHS):
      continue
    context = "\n".join(lines[max(0, line_number - 3) : line_number + 1])
    if OPERATIONAL_TERMS.search(line) and not re.search(
      r"\b(remov|delet|rippab|optional)\w*\b", context, re.IGNORECASE
    ):
      errors.append(
        f"{path}:{line_number}: portable skill operationally requires a runtime-specific path"
      )


def discover_skills(root: Path) -> tuple[Path, ...]:
  skills_root = root / ".agents" / "skills"
  if not skills_root.is_dir():
    return ()
  return tuple(sorted(skills_root.rglob("SKILL.md")))


def validate_skills(root: str | Path = ROOT) -> ValidationResult:
  base = Path(root).expanduser().resolve()
  errors: list[str] = []
  warnings: list[str] = []
  skills = discover_skills(base)
  if not skills:
    errors.append(f"{base}: no .agents/skills/**/SKILL.md files found")
    return ValidationResult(tuple(errors), tuple(warnings))

  for path in skills:
    try:
      relative_parent = path.parent.relative_to(base / ".agents" / "skills")
    except ValueError:
      relative_parent = path.parent
    if len(relative_parent.parts) != 1:
      errors.append(f"{path}: skill directory must be one level below .agents/skills/")
      continue
    directory_name = relative_parent.name
    if not SKILL_NAME_RE.fullmatch(directory_name):
      errors.append(f"{path}: skill directory is not portable kebab-case: {directory_name}")
    text = _read(path)
    frontmatter, body, frontmatter_errors = _parse_frontmatter(path, text)
    errors.extend(frontmatter_errors)
    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    if not name:
      errors.append(f"{path}: frontmatter requires name")
    elif name != directory_name:
      errors.append(f"{path}: frontmatter name '{name}' must match directory '{directory_name}'")
    if not description:
      errors.append(f"{path}: frontmatter requires description")
    elif len(description) > 1024:
      errors.append(f"{path}: description must be at most 1024 characters")
    _check_links(path, body, errors)
    _check_references(path, text, errors)
    _check_portable_boundary(path, body, errors)

  canonical = base / ".agents" / "skills" / "harness" / "SKILL.md"
  if canonical not in skills:
    warnings.append("canonical harness skill is not present under .agents/skills/harness/")
  return ValidationResult(tuple(errors), tuple(warnings))


def build_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(description="Validate portable Agent Skills")
  parser.add_argument("--root", default=str(ROOT), help="Repository root to validate")
  return parser


def main(argv: list[str] | None = None) -> int:
  args = build_parser().parse_args(argv)
  result = validate_skills(args.root)
  for warning in result.warnings:
    print(f"WARNING: {warning}", file=sys.stderr)
  if not result.ok:
    for error in result.errors:
      print(f"FAIL: {error}", file=sys.stderr)
    return 1
  print("OK: Portable skill validation passed.")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
