#!/usr/bin/env python3
"""Inventory an existing repository without mutating it.

The audit is deliberately independent of installer execution.  Its output is a
small, deterministic contract that can be consumed by a CLI, TUI, or another
agent before an installation plan is built.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable


ACTIVE_RUNTIMES = ("pi", "codex", "antigravity", "cursor")
LEGACY_ARTIFACTS = {
  "codex": (".codex/skills/harness",),
  "forgecode": (".forge", ".forge/skills/harness", ".forge/agents"),
  "droid": (".factory", ".factory/skills/harness", ".factory/droids"),
  "openhands": (".openhands",),
  "aider": (".aider.conf.yml",),
}
RUNTIME_EVIDENCE = {
  "pi": (".pi",),
  "codex": (".codex", ".codex/skills", ".codex/agents"),
  "antigravity": (".antigravity", ".antigravity/agents"),
  "cursor": (".cursor", ".cursor/agents"),
}


@dataclass(frozen=True)
class RuntimeEvidence:
  name: str
  status: str
  evidence: tuple[str, ...]


@dataclass(frozen=True)
class AuditReport:
  existing_skills: tuple[str, ...] = ()
  existing_roles: tuple[str, ...] = ()
  detected_runtimes: tuple[RuntimeEvidence, ...] = ()
  stale_artifacts: tuple[str, ...] = ()
  duplicate_roles: tuple[str, ...] = ()
  duplicate_skills: tuple[str, ...] = ()
  compatibility_risks: tuple[str, ...] = ()
  operation_classification: str = "new harness"
  recommended_action: tuple[str, ...] = ()

  def to_dict(self) -> dict[str, object]:
    value = asdict(self)
    value["detected_runtimes"] = [asdict(item) for item in self.detected_runtimes]
    return value


def _relative_paths(root: Path, paths: Iterable[Path]) -> tuple[str, ...]:
  return tuple(sorted(path.relative_to(root).as_posix() for path in paths))


def _skill_paths(root: Path) -> tuple[str, ...]:
  skills_root = root / ".agents" / "skills"
  if not skills_root.is_dir():
    return ()
  return _relative_paths(root, (path.parent for path in skills_root.rglob("SKILL.md")))


def _role_paths(root: Path) -> tuple[str, ...]:
  role_root = root / "docs" / "harness"
  if not role_root.is_dir():
    return ()
  return _relative_paths(root, role_root.rglob("roles/*.md"))


def _duplicate_names(paths: Iterable[str]) -> tuple[str, ...]:
  by_name: dict[str, list[str]] = {}
  for path in paths:
    name = Path(path).name
    by_name.setdefault(name, []).append(path)
  return tuple(
    f"{name}: {', '.join(sorted(locations))}"
    for name, locations in sorted(by_name.items())
    if len(locations) > 1
  )


def _detect_runtimes(root: Path) -> tuple[RuntimeEvidence, ...]:
  result: list[RuntimeEvidence] = []
  for runtime in ACTIVE_RUNTIMES:
    evidence = tuple(
      path
      for path in RUNTIME_EVIDENCE[runtime]
      if (root / path).exists()
    )
    if evidence:
      result.append(RuntimeEvidence(runtime, "supported", evidence))
  if (root / ".agents" / "skills").is_dir():
    result.append(RuntimeEvidence("generic", "portable", (".agents/skills",)))
  return tuple(result)


def _stale_artifacts(root: Path) -> tuple[str, ...]:
  found: list[str] = []
  for paths in LEGACY_ARTIFACTS.values():
    for relative in paths:
      if (root / relative).exists():
        found.append(relative)
  return tuple(sorted(set(found)))


def _classify(
  skills: tuple[str, ...],
  roles: tuple[str, ...],
  runtimes: tuple[RuntimeEvidence, ...],
  stale: tuple[str, ...],
  duplicate_roles: tuple[str, ...],
  duplicate_skills: tuple[str, ...],
) -> str:
  if not skills and not roles and not runtimes and not stale:
    return "new harness"
  if stale or duplicate_roles or duplicate_skills:
    return "drift repair"
  if any(item.name != "generic" for item in runtimes) and not skills:
    return "runtime adapter update"
  if skills or roles:
    return "existing harness extension"
  return "maintenance/audit"


def audit_target(target: str | Path) -> AuditReport:
  root = Path(target).expanduser().resolve()
  if not root.exists() or not root.is_dir():
    raise ValueError(f"Audit target must be an existing directory: {root}")

  skills = _skill_paths(root)
  roles = _role_paths(root)
  runtimes = _detect_runtimes(root)
  stale = _stale_artifacts(root)
  duplicate_roles = _duplicate_names(roles)
  duplicate_skills = _duplicate_names(skills)
  risks: list[str] = []
  recommendations: list[str] = []

  if stale:
    risks.append("deprecated runtime artifacts require an explicit keep, migrate, remove, or ignore decision")
    recommendations.append("inspect legacy artifacts before changing them; never remove unknown files")
  if duplicate_skills:
    risks.append("duplicate skill names can create ambiguous discovery")
    recommendations.append("choose one canonical skill source before refreshing mirrors")
  if duplicate_roles:
    risks.append("duplicate role names can create conflicting ownership")
    recommendations.append("reconcile duplicate roles before compiling native profiles")
  if not skills:
    recommendations.append("install the canonical portable skill before adding runtime profiles")
  elif not recommendations:
    recommendations.append("keep the portable skill canonical and refresh only selected adapters")

  return AuditReport(
    existing_skills=skills,
    existing_roles=roles,
    detected_runtimes=runtimes,
    stale_artifacts=stale,
    duplicate_roles=duplicate_roles,
    duplicate_skills=duplicate_skills,
    compatibility_risks=tuple(risks),
    operation_classification=_classify(
      skills, roles, runtimes, stale, duplicate_roles, duplicate_skills
    ),
    recommended_action=tuple(recommendations),
  )


def _yaml_scalar(value: object) -> str:
  if isinstance(value, bool):
    return "true" if value else "false"
  if value is None:
    return "null"
  return str(value)


def _render_yaml(value: object, indent: int = 0) -> list[str]:
  prefix = " " * indent
  lines: list[str] = []
  if isinstance(value, dict):
    for key, item in value.items():
      if isinstance(item, (dict, list, tuple)):
        lines.append(f"{prefix}{key}:")
        lines.extend(_render_yaml(item, indent + 2))
      else:
        lines.append(f"{prefix}{key}: {_yaml_scalar(item)}")
  elif isinstance(value, (list, tuple)):
    if not value:
      lines.append(f"{prefix}[]")
    for item in value:
      if isinstance(item, dict):
        entries = list(item.items())
        if not entries:
          lines.append(f"{prefix}- {{}}")
          continue
        first_key, first_value = entries[0]
        if isinstance(first_value, (dict, list, tuple)):
          lines.append(f"{prefix}- {first_key}:")
          lines.extend(_render_yaml(first_value, indent + 4))
        else:
          lines.append(f"{prefix}- {first_key}: {_yaml_scalar(first_value)}")
        for key, nested in entries[1:]:
          if isinstance(nested, (dict, list, tuple)):
            lines.append(f"{' ' * (indent + 2)}{key}:")
            lines.extend(_render_yaml(nested, indent + 4))
          else:
            lines.append(f"{' ' * (indent + 2)}{key}: {_yaml_scalar(nested)}")
      elif isinstance(item, (list, tuple)):
        lines.append(f"{prefix}-")
        lines.extend(_render_yaml(item, indent + 2))
      else:
        lines.append(f"{prefix}- {_yaml_scalar(item)}")
  else:
    lines.append(f"{prefix}{_yaml_scalar(value)}")
  return lines


def render_report(report: AuditReport, output_format: str = "yaml") -> str:
  data = report.to_dict()
  if output_format == "json":
    return json.dumps(data, indent=2, sort_keys=True)
  return "\n".join(_render_yaml(data))


def build_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(
    description="Inspect an existing Harness installation without mutating it."
  )
  parser.add_argument("--target", default=".", help="Repository to inspect")
  parser.add_argument("--format", choices=("yaml", "json"), default="yaml")
  parser.add_argument(
    "--action",
    choices=("keep", "migrate", "remove", "ignore"),
    help="Record an intended legacy-artifact decision without applying it",
  )
  return parser


def main(argv: list[str] | None = None) -> int:
  args = build_parser().parse_args(argv)
  try:
    report = audit_target(args.target)
  except ValueError as error:
    print(f"ERROR: {error}", file=sys.stderr)
    return 1
  rendered = render_report(report, args.format)
  if args.action:
    rendered += f"\nselected_action: {args.action}\n"
    rendered += "mutation: none (audit is read-only; apply changes through an explicit install plan)"
  print(rendered)
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
