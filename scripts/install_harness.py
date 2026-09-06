#!/usr/bin/env python3
"""Install, audit, compile, and validate Meta Harness artifacts.

The command accepts the modern subcommand form as well as the pre-v0.7
``--scope ... --layout ...`` form.  Both forms build an ``InstallRequest`` and
render an inspectable ``InstallPlan`` before any filesystem mutation.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Sequence

try:
  from audit_harness import audit_target, render_report
  from installer_core import (
    ACTIVE_AGENTS,
    LEGACY_LAYOUTS,
    MODES,
    MODEL_POLICIES,
    SCOPES,
    Action,
    InstallPlan,
    InstallRequest,
    InstallerError,
    apply_install_plan,
    build_install_plan,
    normalize_agents,
    resolve_root,
    user_home,
  )
except ModuleNotFoundError:  # pragma: no cover - supports direct package imports
  from scripts.audit_harness import audit_target, render_report
  from scripts.installer_core import (
    ACTIVE_AGENTS,
    LEGACY_LAYOUTS,
    MODES,
    MODEL_POLICIES,
    SCOPES,
    Action,
    InstallPlan,
    InstallRequest,
    InstallerError,
    apply_install_plan,
    build_install_plan,
    normalize_agents,
    resolve_root,
    user_home,
  )


VERSION = "0.8.1"
COMMANDS = ("install", "audit", "doctor", "compile", "validate")
# Kept as a read-only compatibility alias for callers that imported the old
# script constants before the planner refactor.
LAYOUTS = LEGACY_LAYOUTS


def destination_specs(scope: str, layout: str) -> list[tuple[str, str]]:
  """Return the legacy relative destinations used by the pre-v0.7 API."""
  if scope not in SCOPES:
    raise InstallerError(f"Unknown install scope: {scope}")
  if layout not in LEGACY_LAYOUTS:
    raise InstallerError(f"Unknown legacy layout: {layout}")
  specs = [("shared", ".agents/skills/harness")]
  if layout == "forgecode":
    specs.append(("forgecode", ".forge/skills/harness" if scope == "project" else "forge/skills/harness"))
  elif layout == "droid":
    specs.append(("droid", ".factory/skills/harness"))
  elif layout == "codex":
    specs.append(("codex", ".codex/skills/harness"))
  return specs


def fail(message: str) -> int:
  print(f"ERROR: {message}", file=sys.stderr)
  return 1


def _add_install_arguments(parser: argparse.ArgumentParser) -> None:
  parser.add_argument("--scope", choices=SCOPES, help="Installation scope")
  parser.add_argument("--target", help="Project root for project scope")
  parser.add_argument(
    "--agent",
    action="append",
    choices=ACTIVE_AGENTS,
    help="Runtime target; repeat for multiple targets",
  )
  parser.add_argument(
    "--layout",
    choices=LEGACY_LAYOUTS,
    help="Deprecated pre-v0.7 layout alias",
  )
  parser.add_argument("--mode", choices=MODES, default="copy")
  parser.add_argument(
    "--native-profiles",
    action="store_true",
    help="Generate optional runtime-native execution profiles",
  )
  parser.add_argument(
    "--pi-safe-agent-team",
    choices=("auto", "on", "off"),
    default="auto",
    help="Declare optional Pi team integration preference",
  )
  parser.add_argument(
    "--model-policy",
    choices=MODEL_POLICIES,
    default="inherit",
    help="Semantic model policy for generated runtime profiles",
  )
  parser.add_argument(
    "--role",
    action="append",
    help="Role brief path for native profile generation; repeat for multiple roles",
  )
  parser.add_argument(
    "--dry-run",
    action="store_true",
    help="Print the install plan without modifying any destination",
  )
  parser.add_argument(
    "--force",
    action="store_true",
    help="Replace stale managed Harness artifacts (never arbitrary user paths)",
  )
  parser.add_argument(
    "--remove-legacy",
    action="store_true",
    help="Explicitly remove recognized deprecated Harness mirrors",
  )
  parser.add_argument(
    "--interactive",
    action="store_true",
    help="Use the keyboard-friendly installer frontend (requires a TTY)",
  )
  parser.add_argument(
    "--non-interactive",
    action="store_true",
    help="Require explicit scope/target/agent values and never render a TUI",
  )


def build_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(
    prog="meta-harness",
    description=(
      "Design and install the portable Meta Harness skill with capability-aware "
      "runtime adapters."
    ),
  )
  parser.add_argument("--version", action="version", version=VERSION)
  subparsers = parser.add_subparsers(dest="command")

  install = subparsers.add_parser("install", help="Plan and install Harness artifacts")
  _add_install_arguments(install)

  audit = subparsers.add_parser("audit", help="Inventory an existing repository without mutation")
  audit.add_argument("--target", default=".")
  audit.add_argument("--format", choices=("yaml", "json"), default="yaml")
  audit.add_argument(
    "--action",
    choices=("keep", "migrate", "remove", "ignore"),
    help="Record a legacy-artifact decision without applying it",
  )

  doctor = subparsers.add_parser("doctor", help="Check source, target, and capability prerequisites")
  doctor.add_argument("--scope", choices=SCOPES, default="project")
  doctor.add_argument("--target", default=".")
  doctor.add_argument("--agent", action="append", choices=ACTIVE_AGENTS)
  doctor.add_argument("--mode", choices=MODES, default="copy")

  compile_parser = subparsers.add_parser(
    "compile", help="Compile selected runtime-native profiles from the portable contract"
  )
  compile_parser.add_argument("--scope", choices=SCOPES, default="project")
  compile_parser.add_argument("--target", help="Project root for project scope")
  compile_parser.add_argument(
    "--agent", action="append", choices=ACTIVE_AGENTS, required=True
  )
  compile_parser.add_argument("--dry-run", action="store_true")
  compile_parser.add_argument("--force", action="store_true")
  compile_parser.add_argument("--mode", choices=MODES, default="copy")
  compile_parser.add_argument("--role", action="append", help="Role brief path; repeat for multiple roles")
  compile_parser.add_argument(
    "--model-policy", choices=MODEL_POLICIES, default="inherit"
  )
  compile_parser.add_argument(
    "--pi-safe-agent-team", choices=("auto", "on", "off"), default="auto"
  )

  validate = subparsers.add_parser("validate", help="Validate portable skills and adapter fixtures")
  validate.add_argument("--target", default=None)
  validate.add_argument("--portable-only", action="store_true")

  return parser


def _normalize_legacy_argv(argv: Sequence[str]) -> list[str]:
  if not argv:
    return ["install"]
  first = argv[0]
  if first in COMMANDS or first in ("-h", "--help", "--version"):
    return list(argv)
  if first.startswith("-"):
    return ["install", *argv]
  return list(argv)


def _legacy_agent(layout: str | None) -> tuple[str, ...] | None:
  if layout is None:
    return None
  if layout == "codex":
    return ("codex",)
  return ("generic",)


def _request_from_install_args(args: argparse.Namespace) -> InstallRequest:
  if args.scope is None:
    raise InstallerError(
      "--scope is required for non-interactive install; use --interactive on a TTY for the installer UI"
    )
  if args.layout and args.agent:
    raise InstallerError("--layout is a deprecated alias and cannot be combined with --agent")
  agents = args.agent or _legacy_agent(args.layout) or ("generic",)
  if args.scope == "project" and not args.target:
    raise InstallerError("--target is required when --scope project")
  if args.scope == "user" and args.target:
    raise InstallerError("--target is only valid when --scope project")
  return InstallRequest(
    scope=args.scope,
    target=Path(args.target) if args.target else None,
    agents=tuple(agents),
    mode=args.mode,
    native_profiles=args.native_profiles,
    pi_safe_agent_team=args.pi_safe_agent_team,
    force=args.force,
    dry_run=args.dry_run,
    legacy_layout=args.layout,
    remove_legacy=args.remove_legacy,
    roles=tuple(Path(role) for role in (args.role or ())),
    model_policy=args.model_policy,
  )


def _print_install_result(plan: InstallPlan, args: argparse.Namespace) -> None:
  if args.layout:
    print(f"Installed Harness using {args.mode} mode with {args.layout} layout.")
  else:
    labels = ", ".join(plan.request.agents)
    print(f"Installed Harness using {args.mode} mode for agents: {labels}.")
  for operation in plan.operations:
    if operation.action in (Action.CREATE, Action.UPDATE):
      print(f"- {operation.action.value}: {operation.destination}")
  for note in plan.post_install_notes:
    print(note)


def _run_tui(args: argparse.Namespace) -> int:
  if not (sys.stdin.isatty() and sys.stdout.isatty()):
    return fail("interactive mode requires a TTY; pass --non-interactive with explicit values")
  try:
    try:
      from installer_tui import run_tui
    except ModuleNotFoundError:
      from scripts.installer_tui import run_tui
    return run_tui()
  except (KeyboardInterrupt, EOFError):
    print("Cancelled.")
    return 0


def run_install(args: argparse.Namespace) -> int:
  interactive_requested = args.interactive or (
    not args.non_interactive
    and args.scope is None
    and not args.agent
    and not args.layout
    and sys.stdin.isatty()
    and sys.stdout.isatty()
  )
  if interactive_requested:
    return _run_tui(args)
  if args.interactive and args.non_interactive:
    return fail("--interactive and --non-interactive cannot be combined")
  try:
    request = _request_from_install_args(args)
    plan = build_install_plan(request)
  except (InstallerError, OSError) as error:
    return fail(str(error))

  print(plan.render())
  if plan.has_conflicts:
    return fail("installation blocked by conflicts; inspect the plan and choose a safe target or --force for managed artifacts")
  if request.dry_run:
    print("Dry run only; no changes made.")
    return 0
  try:
    apply_install_plan(plan)
  except (InstallerError, OSError, shutil.Error) as error:
    return fail(str(error))
  _print_install_result(plan, args)
  return 0


def run_audit(args: argparse.Namespace) -> int:
  try:
    report = audit_target(args.target)
  except (ValueError, OSError) as error:
    return fail(str(error))
  output = render_report(report, args.format)
  if args.action:
    output += f"\nselected_action: {args.action}\nmutation: none (audit is read-only)"
  print(output)
  return 0


def run_doctor(args: argparse.Namespace) -> int:
  checks: list[tuple[str, bool, str]] = []
  source = Path(__file__).resolve().parents[1] / ".agents" / "skills" / "harness"
  checks.append(("canonical source", source.is_dir(), str(source)))
  if args.scope == "project":
    target = Path(args.target).expanduser().resolve()
    checks.append(("project target", target.is_dir(), str(target)))
  else:
    target = None
    checks.append(("user home", True, str(user_home())))
  try:
    agents = tuple(normalize_agents(args.agent or ("generic",)))
    checks.append(("runtime selection", True, ", ".join(agents)))
  except InstallerError as error:
    checks.append(("runtime selection", False, str(error)))
  checks.append(("mode", args.mode in MODES, args.mode))
  for label, ok, detail in checks:
    print(f"{'OK' if ok else 'FAIL'} {label}: {detail}")
  return 0 if all(ok for _, ok, _ in checks) else 1


def run_compile(args: argparse.Namespace) -> int:
  try:
    request = InstallRequest(
      scope=args.scope,
      target=Path(args.target) if args.target else None,
      agents=tuple(args.agent),
      mode=args.mode,
      native_profiles=True,
      pi_safe_agent_team=args.pi_safe_agent_team,
      force=args.force,
      dry_run=args.dry_run,
      roles=tuple(Path(role) for role in (args.role or ())),
      model_policy=args.model_policy,
    )
    full_plan = build_install_plan(request)
    profile_operations = tuple(
      operation for operation in full_plan.operations if operation.generated_content is not None
    )
    plan = InstallPlan(
      request=request,
      root=full_plan.root,
      operations=profile_operations,
      warnings=full_plan.warnings,
      post_install_notes=full_plan.post_install_notes,
    )
  except (InstallerError, OSError) as error:
    return fail(str(error))
  print(plan.render())
  if plan.has_conflicts:
    return fail("profile compilation blocked by conflicts")
  if args.dry_run:
    print("Dry run only; no changes made.")
    return 0
  try:
    apply_install_plan(plan)
  except (InstallerError, OSError) as error:
    return fail(str(error))
  print("Compiled runtime-native profiles.")
  return 0


def run_validate(args: argparse.Namespace) -> int:
  root = Path(args.target).expanduser().resolve() if args.target else Path(__file__).resolve().parents[1]
  validator_root = Path(__file__).resolve().parents[1]
  # An installed target contains the skill tree but not this repository's
  # validator scripts; run the canonical validators against that target.
  commands = [
    [sys.executable, str(validator_root / "scripts" / "validate_skills.py"), "--root", str(root)]
  ]
  if not args.portable_only and (root / "tests" / "fixtures").is_dir():
    commands.append(
      [sys.executable, str(validator_root / "scripts" / "validate_adapters.py"), "--root", str(root)]
    )
  for command in commands:
    result = subprocess.run(command, cwd=root, text=True, check=False)
    if result.returncode != 0:
      return result.returncode
  return 0


def main(argv: Sequence[str] | None = None) -> int:
  raw = list(sys.argv[1:] if argv is None else argv)
  parser = build_parser()
  try:
    args = parser.parse_args(_normalize_legacy_argv(raw))
  except SystemExit as error:
    return int(error.code)
  if args.command in (None, "install"):
    return run_install(args)
  if args.command == "audit":
    return run_audit(args)
  if args.command == "doctor":
    return run_doctor(args)
  if args.command == "compile":
    return run_compile(args)
  if args.command == "validate":
    return run_validate(args)
  return fail(f"Unknown command: {args.command}")


if __name__ == "__main__":
  raise SystemExit(main())
