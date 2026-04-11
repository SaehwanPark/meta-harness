#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SKILL_DIR = ROOT / ".agents" / "skills" / "harness"
LAYOUTS = ("standard", "forgecode", "droid", "openhands", "aider", "codex")
MODES = ("copy", "symlink")
SCOPES = ("project", "user")


def build_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(
    description=(
      "Install the canonical Harness skill into a project or user-level "
      "skills directory without mutating target repo docs."
    )
  )
  parser.add_argument("--scope", choices=SCOPES, required=True)
  parser.add_argument("--target", help="Project root for --scope project")
  parser.add_argument("--layout", choices=LAYOUTS, default="standard")
  parser.add_argument("--mode", choices=MODES, default="copy")
  parser.add_argument(
    "--dry-run",
    action="store_true",
    help="Print the resolved install plan without modifying any destination paths.",
  )
  parser.add_argument(
    "--force",
    action="store_true",
    help="Replace an existing Harness install at the destination paths.",
  )
  return parser


def fail(message: str) -> int:
  print(f"ERROR: {message}", file=sys.stderr)
  return 1


def ensure_source_exists() -> None:
  if not SOURCE_SKILL_DIR.exists():
    raise SystemExit(fail(f"Missing canonical source: {SOURCE_SKILL_DIR}"))


def resolve_root(scope: str, target: str | None) -> Path:
  if scope == "project":
    if not target:
      raise SystemExit(fail("--target is required when --scope project"))
    root = Path(target).expanduser().resolve()
    if not root.exists():
      raise SystemExit(fail(f"Project target does not exist: {root}"))
    if not root.is_dir():
      raise SystemExit(fail(f"Project target is not a directory: {root}"))
    return root

  if target:
    raise SystemExit(fail("--target is only valid when --scope project"))
  return Path.home().resolve()


def destination_specs(scope: str, layout: str) -> list[tuple[str, str]]:
  specs: list[tuple[str, str]] = [("shared", ".agents/skills/harness")]

  if layout == "forgecode":
    native = ".forge/skills/harness" if scope == "project" else "forge/skills/harness"
    specs.append(("forgecode", native))
  elif layout == "droid":
    specs.append(("droid", ".factory/skills/harness"))
  elif layout == "codex":
    native = ".codex/skills/harness" if scope == "project" else ".codex/skills/harness"
    specs.append(("codex", native))

  return specs


def remove_path(path: Path) -> None:
  if path.is_symlink() or path.is_file():
    path.unlink()
  elif path.exists():
    shutil.rmtree(path)


def install_destination(source: Path, destination: Path, mode: str) -> None:
  destination.parent.mkdir(parents=True, exist_ok=True)
  if mode == "copy":
    shutil.copytree(
      source,
      destination,
      ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    return

  destination.symlink_to(source, target_is_directory=True)


def aider_followup(root: Path) -> str:
  config_path = root / ".aider.conf.yml"
  return "\n".join(
    [
      "Aider follow-up:",
      f"- Harness was installed into {root / '.agents/skills/harness'}",
      f"- Add this to {config_path}:",
      "read:",
      "  - AGENTS.md",
    ]
  )


def post_install_notes(scope: str, layout: str, root: Path) -> list[str]:
  notes: list[str] = []
  if layout == "openhands":
    notes.append(
      "OpenHands uses the shared .agents/skills/ location; keep repo-specific setup in .openhands/ only when needed."
    )
  if layout == "forgecode":
    notes.append(
      "ForgeCode can use the shared install and the native .forge/skills mirror. Reserve .forge/agents for agent definitions, not reusable shared skills."
    )
  if layout == "droid":
    notes.append(
      "Droid can use the shared install and the native .factory/skills mirror. Reserve .factory/droids for subagents with their own tool/model policy."
    )
  if layout == "codex":
    notes.append(
      "Codex can use the shared install and the native .codex/skills mirror. Keep reusable Harness workflow logic in the shared tree and use the Codex mirror for native discovery."
    )
  if layout == "aider":
    notes.append(aider_followup(root))
  return notes


def print_dry_run_summary(
  mode: str,
  layout: str,
  destinations: list[tuple[str, Path]],
  existing: list[Path],
  notes: list[str],
  force: bool,
) -> None:
  print(f"Dry run: Harness install using {mode} mode with {layout} layout.")
  for label, destination in destinations:
    state = "exists" if destination in existing else "missing"
    print(f"- {label}: {destination} [{state}]")
  if existing and not force:
    joined = ", ".join(str(path) for path in existing)
    print(f"- install status: would fail without --force because destination exists: {joined}")
  elif existing and force:
    joined = ", ".join(str(path) for path in existing)
    print(f"- install status: would replace existing destination paths: {joined}")
  else:
    print("- install status: would create all destination paths")

  for note in notes:
    print(note)
  print("Dry run only; no changes made.")


def main() -> int:
  ensure_source_exists()
  parser = build_parser()
  args = parser.parse_args()
  root = resolve_root(args.scope, args.target)

  destinations: list[tuple[str, Path]] = []
  for label, relative in destination_specs(args.scope, args.layout):
    destinations.append((label, root / relative))

  notes = post_install_notes(args.scope, args.layout, root)
  existing = [
    destination
    for _, destination in destinations
    if destination.exists() or destination.is_symlink()
  ]
  if args.dry_run:
    print_dry_run_summary(
      args.mode,
      args.layout,
      destinations,
      existing,
      notes,
      args.force,
    )
    return 0

  if existing and not args.force:
    joined = ", ".join(str(path) for path in existing)
    return fail(f"Destination already exists; rerun with --force to replace: {joined}")

  if args.force:
    for destination in existing:
      remove_path(destination)

  for _, destination in destinations:
    install_destination(SOURCE_SKILL_DIR, destination, args.mode)

  print(f"Installed Harness using {args.mode} mode with {args.layout} layout.")
  for label, destination in destinations:
    print(f"- {label}: {destination}")

  for note in notes:
    print(note)

  return 0


if __name__ == "__main__":
  raise SystemExit(main())
