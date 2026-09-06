#!/usr/bin/env python3
"""Pure install planning and filesystem execution for Meta Harness.

The planner has no side effects.  CLI and TUI callers build the same
``InstallRequest`` and consume the same ``InstallPlan`` before choosing whether
to apply it.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
import tempfile
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SKILL_DIR = ROOT / ".agents" / "skills" / "harness"
ACTIVE_AGENTS = ("pi", "codex", "antigravity", "cursor", "generic")
LEGACY_LAYOUTS = ("standard", "forgecode", "droid", "openhands", "aider", "codex")
MODES = ("copy", "symlink")
SCOPES = ("project", "user")
MODEL_POLICIES = ("inherit", "fast", "economy", "balanced", "strong")


class Action(str, Enum):
  CREATE = "CREATE"
  UPDATE = "UPDATE"
  KEEP = "KEEP"
  SKIP = "SKIP"
  REMOVE = "REMOVE"
  CONFLICT = "CONFLICT"


class InstallerError(ValueError):
  """A user-correctable request or preflight error."""


@dataclass(frozen=True)
class RuntimeSpec:
  name: str
  label: str
  native_profile_dir: str | None
  capabilities: tuple[str, ...]
  notes: tuple[str, ...] = ()


RUNTIME_SPECS: Mapping[str, RuntimeSpec] = {
  "pi": RuntimeSpec(
    "pi",
    "Pi",
    None,
    ("skills", "model-routing", "optional-team-extension"),
    ("pi-safe-agent-team is optional and has no portable filesystem dependency",),
  ),
  "codex": RuntimeSpec(
    "codex",
    "Codex",
    ".codex/agents",
    ("skills", "custom-agents", "model-routing"),
  ),
  "antigravity": RuntimeSpec(
    "antigravity",
    "Antigravity",
    ".antigravity/agents",
    ("skills", "custom-agents", "model-routing"),
  ),
  "cursor": RuntimeSpec(
    "cursor",
    "Cursor CLI / Agent",
    ".cursor/agents",
    ("skills", "custom-agents", "model-routing"),
  ),
  "generic": RuntimeSpec(
    "generic",
    "Generic Agent Skills",
    None,
    ("portable-skills",),
    ("no runtime-specific orchestration guarantee",),
  ),
}

AGENT_ALIASES = {
  "cursor-cli": "cursor",
  "cursor-agent": "cursor",
  "agent-skills": "generic",
  "generic-agent-skills": "generic",
  "portable": "generic",
}

# These paths are retained only for the deprecated --layout compatibility path.
LEGACY_MIRRORS: Mapping[str, tuple[str, str]] = {
  "codex": (".codex/skills/harness", ".codex/skills/harness"),
  "forgecode": (".forge/skills/harness", "forge/skills/harness"),
  "droid": (".factory/skills/harness", ".factory/skills/harness"),
}
LEGACY_NOTES = {
  "openhands": "OpenHands is unverified/deprecated; use the shared skill and keep optional setup in .openhands/ user-owned.",
  "aider": "Aider is unverified/deprecated; use the shared skill and configure AGENTS.md in the client's read list.",
}

MARKER_NAME = ".meta-harness-install.json"
MARKER_VERSION = 1


@dataclass(frozen=True)
class InstallRequest:
  scope: str
  target: Path | None = None
  agents: tuple[str, ...] = ("generic",)
  mode: str = "copy"
  native_profiles: bool = False
  pi_safe_agent_team: str = "auto"
  force: bool = False
  dry_run: bool = False
  legacy_layout: str | None = None
  remove_legacy: bool = False
  source: Path = SOURCE_SKILL_DIR

  def __post_init__(self) -> None:
    if self.scope not in SCOPES:
      raise InstallerError(f"Unknown install scope: {self.scope}")
    if self.mode not in MODES:
      raise InstallerError(f"Unknown install mode: {self.mode}")
    if self.pi_safe_agent_team not in ("auto", "on", "off"):
      raise InstallerError("pi_safe_agent_team must be auto, on, or off")
    if self.legacy_layout is not None and self.legacy_layout not in LEGACY_LAYOUTS:
      raise InstallerError(f"Unknown legacy layout: {self.legacy_layout}")
    normalized_agents = tuple(normalize_agents(self.agents))
    if not normalized_agents:
      raise InstallerError("at least one runtime agent must be selected")
    object.__setattr__(self, "agents", normalized_agents)
    object.__setattr__(self, "source", Path(self.source).expanduser().resolve())
    if self.target is not None:
      object.__setattr__(self, "target", Path(self.target).expanduser().resolve())


@dataclass(frozen=True)
class InstallOperation:
  action: Action
  destination: Path
  source: Path | None = None
  owner: str = "installer"
  reason: str = ""
  generated_content: str | None = None
  metadata: Mapping[str, object] = field(default_factory=dict)

  def to_dict(self) -> dict[str, object]:
    return {
      "action": self.action.value,
      "source": self.source.as_posix() if self.source else None,
      "destination": self.destination.as_posix(),
      "owner": self.owner,
      "reason": self.reason,
      "metadata": dict(self.metadata),
    }


@dataclass(frozen=True)
class InstallPlan:
  request: InstallRequest
  root: Path
  operations: tuple[InstallOperation, ...]
  warnings: tuple[str, ...] = ()
  post_install_notes: tuple[str, ...] = ()

  @property
  def conflicts(self) -> tuple[InstallOperation, ...]:
    return tuple(op for op in self.operations if op.action == Action.CONFLICT)

  @property
  def changes(self) -> tuple[InstallOperation, ...]:
    return tuple(
      op
      for op in self.operations
      if op.action in (Action.CREATE, Action.UPDATE, Action.REMOVE)
    )

  @property
  def has_conflicts(self) -> bool:
    return bool(self.conflicts)

  def to_dict(self) -> dict[str, object]:
    return {
      "root": self.root.as_posix(),
      "request": {
        "scope": self.request.scope,
        "target": self.request.target.as_posix() if self.request.target else None,
        "agents": list(self.request.agents),
        "mode": self.request.mode,
        "native_profiles": self.request.native_profiles,
        "pi_safe_agent_team": self.request.pi_safe_agent_team,
        "force": self.request.force,
        "dry_run": self.request.dry_run,
        "legacy_layout": self.request.legacy_layout,
      },
      "operations": [op.to_dict() for op in self.operations],
      "warnings": list(self.warnings),
      "post_install_notes": list(self.post_install_notes),
    }

  def render(self) -> str:
    lines = ["Installation plan", ""]
    if not self.operations:
      lines.append("(no operations)")
    for operation in self.operations:
      path = _display_path(operation.destination, self.root)
      suffix = f" - {operation.reason}" if operation.reason else ""
      lines.append(f"{operation.action.value:<8} {path}{suffix}")
    if self.warnings:
      lines.extend(("", "Warnings:"))
      lines.extend(f"- {warning}" for warning in self.warnings)
    if self.post_install_notes:
      lines.extend(("", "Notes:"))
      lines.extend(f"- {note}" for note in self.post_install_notes)
    return "\n".join(lines)


def normalize_agents(agents: Iterable[str]) -> list[str]:
  selected: set[str] = set()
  for raw in agents:
    value = str(raw).strip().casefold()
    value = AGENT_ALIASES.get(value, value)
    if value not in ACTIVE_AGENTS:
      raise InstallerError(
        f"Unknown agent '{raw}'. Choose one of: {', '.join(ACTIVE_AGENTS)}"
      )
    selected.add(value)
  # Stable ordering makes CLI/TUI plans comparable and easy to review.
  return [agent for agent in ACTIVE_AGENTS if agent in selected]


def user_home() -> Path:
  """Resolve home deterministically, including injected test homes on Windows."""
  for variable in ("META_HARNESS_HOME", "HOME", "USERPROFILE"):
    value = os.environ.get(variable)
    if value:
      return Path(value).expanduser().resolve()
  return Path.home().resolve()


def resolve_root(request: InstallRequest) -> Path:
  if request.scope == "project":
    if request.target is None:
      raise InstallerError("--target is required when --scope project")
    root = request.target
    if not root.exists():
      raise InstallerError(f"Project target does not exist: {root}")
    if not root.is_dir():
      raise InstallerError(f"Project target is not a directory: {root}")
    return root
  if request.target is not None:
    raise InstallerError("--target is only valid when --scope project")
  return user_home()


def _display_path(path: Path, root: Path) -> str:
  try:
    return path.relative_to(root).as_posix() or "."
  except ValueError:
    return path.as_posix()


def _path_exists(path: Path) -> bool:
  return path.exists() or path.is_symlink()


def _path_has_symlink_parent(path: Path, root: Path) -> bool:
  current = path.parent
  root = root.resolve()
  while current != root and root in current.parents:
    if current.is_symlink():
      return True
    current = current.parent
  return False


def _safe_relative(path: Path, root: Path) -> bool:
  try:
    path.resolve(strict=False).relative_to(root.resolve())
    return True
  except ValueError:
    return False


def _iter_payload_files(source: Path) -> Iterable[Path]:
  for path in sorted(source.rglob("*")):
    if not path.is_file():
      continue
    if "__pycache__" in path.parts or path.suffix in (".pyc", ".pyo"):
      continue
    yield path


def payload_digest(source: Path) -> str:
  digest = hashlib.sha256()
  for path in _iter_payload_files(source):
    digest.update(path.relative_to(source).as_posix().encode("utf-8"))
    digest.update(b"\0")
    digest.update(path.read_bytes())
    digest.update(b"\0")
  return digest.hexdigest()


def _read_marker(destination: Path) -> dict[str, object] | None:
  marker = destination / MARKER_NAME
  if not marker.is_file():
    return None
  try:
    value = json.loads(marker.read_text(encoding="utf-8"))
  except (OSError, ValueError, TypeError):
    return None
  return value if isinstance(value, dict) else None


def _is_managed_skill(destination: Path, source: Path) -> bool:
  if destination.is_symlink():
    try:
      return destination.resolve() == source.resolve()
    except OSError:
      return False
  if not destination.is_dir():
    return False
  marker = _read_marker(destination)
  if marker and marker.get("managed_by") == "meta-harness":
    return True
  # Recognize pre-manifest installs conservatively by the canonical entrypoint.
  skill = destination / "SKILL.md"
  try:
    return skill.is_file() and skill.read_bytes() == (source / "SKILL.md").read_bytes()
  except OSError:
    return False


def _skill_operation(
  destination: Path, source: Path, request: InstallRequest, root: Path, reason: str
) -> InstallOperation:
  # A missing destination can still be routed outside the target by a symlinked
  # parent, so check parent components before planning CREATE.
  if _path_has_symlink_parent(destination, root):
    return InstallOperation(
      Action.CONFLICT,
      destination,
      source,
      reason="destination escapes the target through a symlink",
    )
  if not _path_exists(destination):
    return InstallOperation(Action.CREATE, destination, source, reason=reason)
  managed = _is_managed_skill(destination, source)
  if not managed:
    return InstallOperation(
      Action.CONFLICT,
      destination,
      source,
      owner="user",
      reason="existing path is not a Meta Harness installation",
    )
  if request.force:
    return InstallOperation(Action.UPDATE, destination, source, reason="force requested")
  if request.mode == "symlink":
    if destination.is_symlink():
      try:
        if destination.resolve() == source.resolve():
          return InstallOperation(Action.KEEP, destination, source, reason="symlink is current")
      except OSError:
        pass
    return InstallOperation(Action.UPDATE, destination, source, reason="switch to symlink mode")
  marker = _read_marker(destination)
  if (
    marker
    and marker.get("payload_sha256") == payload_digest(source)
    and marker.get("mode") == "copy"
  ):
    return InstallOperation(Action.KEEP, destination, source, reason="managed copy is current")
  return InstallOperation(Action.UPDATE, destination, source, reason="managed copy is stale")


def _profile_content(agent: str, source: Path, model_policy: str = "inherit") -> str:
  skill_path = ".agents/skills/harness/SKILL.md"
  if agent == "codex":
    return (
      '# Generated by Meta Harness; edit the portable role contract instead.\n'
      'name = "meta-harness"\n'
      'description = "Run the portable Meta Harness workflow with explicit handoffs and safe ownership."\n'
      'developer_instructions = """\n'
      f"Read {skill_path} and keep it authoritative.\n"
      "Preserve declared role ownership, use isolated workspaces or serialization for conflicting writes, "
      "and report missing capabilities or partial failures.\n"
      f"Model policy: {model_policy}. Inherit runtime defaults unless an explicit override is justified.\n"
      '"""\n'
    )
  label = RUNTIME_SPECS[agent].label
  return (
    "<!-- Generated by Meta Harness; edit the portable role contract instead. -->\n"
    "---\n"
    "name: meta-harness\n"
    f"description: Run the portable Meta Harness workflow in {label}.\n"
    "---\n\n"
    f"# {label} execution profile\n\n"
    f"Read `{skill_path}` as the source of truth. Preserve declared ownership, "
    "isolate or serialize conflicting writes, and report unavailable capabilities.\n"
    f"Model policy: `{model_policy}`; inherit runtime defaults unless overridden intentionally.\n"
  )


def _profile_operation(
  agent: str, destination: Path, content: str, root: Path, force: bool
) -> InstallOperation:
  if not _path_exists(destination):
    return InstallOperation(
      Action.CREATE, destination, generated_content=content, reason=f"enable {agent} profile"
    )
  if _path_has_symlink_parent(destination, root) or destination.is_symlink():
    return InstallOperation(Action.CONFLICT, destination, reason="profile path or parent is a symlink")
  if destination.is_file():
    try:
      existing = destination.read_text(encoding="utf-8")
    except OSError:
      existing = ""
    if existing == content:
      return InstallOperation(Action.KEEP, destination, generated_content=content, reason="profile is current")
    if existing.startswith("# Generated by Meta Harness") or existing.startswith(
      "<!-- Generated by Meta Harness"
    ):
      return InstallOperation(Action.UPDATE, destination, generated_content=content, reason="generated profile is stale")
  return InstallOperation(
    Action.CONFLICT,
    destination,
    owner="user",
    reason="existing profile is not generated by Meta Harness; --force cannot overwrite user-owned files",
  )


def _legacy_destinations(request: InstallRequest, root: Path) -> list[tuple[str, Path]]:
  if not request.legacy_layout or request.legacy_layout not in LEGACY_MIRRORS:
    return []
  project_relative, user_relative = LEGACY_MIRRORS[request.legacy_layout]
  relative = project_relative if request.scope == "project" else user_relative
  return [(request.legacy_layout, root / relative)]


def destination_specs(request: InstallRequest) -> list[tuple[str, Path]]:
  root = resolve_root(request)
  destinations = [("shared", root / ".agents" / "skills" / "harness")]
  destinations.extend(_legacy_destinations(request, root))
  return destinations


def _legacy_warnings(layout: str | None) -> list[str]:
  if not layout or layout == "standard":
    return []
  return [
    f"WARNING: --layout {layout} is deprecated and unverified; use --agent with the active runtime or generic mode.",
  ]


def post_install_notes(request: InstallRequest, root: Path) -> list[str]:
  notes = [
    "AGENTS.md stays repo-owned. Create or revise it intentionally only when the target repository needs durable repo-wide guidance.",
    "README.md and repository documentation remain user-owned; the installer mutates only destinations shown in the plan.",
  ]
  if "generic" in request.agents:
    notes.append(
      "Generic mode installs portable Agent Skills only; runtime discovery, orchestration, permissions, and model routing remain unvalidated."
    )
  if "pi" in request.agents:
    notes.append(
      "Pi uses the shared skill. pi-safe-agent-team is optional; without it, serialize conflicting writes or use isolated workspaces."
    )
  if "codex" in request.agents:
    notes.append(
      "Codex uses the shared skill; native profiles are generated only with --native-profiles and remain removable."
    )
  if "antigravity" in request.agents:
    notes.append(
      "Antigravity uses the shared skill; native profiles are generated only with --native-profiles and remain removable."
    )
  if "cursor" in request.agents:
    notes.append(
      "Cursor CLI/Agent uses the shared skill; native profiles are generated only with --native-profiles and remain removable."
    )
  layout = request.legacy_layout
  if layout == "forgecode":
    notes.append(
      "ForgeCode is unverified/deprecated; the legacy mirror is retained only for migration and should not become a second source of truth."
    )
  elif layout == "droid":
    notes.append(
      "Droid is unverified/deprecated; the legacy mirror is retained only for migration and should not become a second source of truth."
    )
  elif layout == "codex":
    notes.append(
      "Codex can use the shared install and the native .codex/skills mirror. The legacy mirror is deprecated, and reusable workflow logic remains canonical in the shared tree."
    )
  elif layout == "openhands":
    notes.append(
      "OpenHands uses the shared .agents/skills/ location; it is unverified/deprecated, and optional setup in .openhands/ remains user-owned."
    )
  elif layout == "aider":
    notes.extend(
      [
        LEGACY_NOTES["aider"],
        "Aider follow-up:",
        f"- Harness was installed into {root / '.agents/skills/harness'}",
        f"- Add this to {root / '.aider.conf.yml'}:",
        "read:",
        "  - AGENTS.md",
      ]
    )
  return notes


def build_install_plan(request: InstallRequest) -> InstallPlan:
  root = resolve_root(request)
  source = request.source
  if not source.exists() or not source.is_dir():
    raise InstallerError(f"Missing canonical source: {source}")
  operations: list[InstallOperation] = []
  warnings = _legacy_warnings(request.legacy_layout)

  for label, destination in destination_specs(request):
    if source == destination or source in destination.parents or destination in source.parents:
      operations.append(
        InstallOperation(
          Action.CONFLICT,
          destination,
          source,
          reason="source and destination overlap; choose a different target",
        )
      )
      continue
    operations.append(
      _skill_operation(destination, source, request, root, f"install {label} portable skill")
    )

  if request.native_profiles:
    for agent in request.agents:
      spec = RUNTIME_SPECS[agent]
      if spec.native_profile_dir is None:
        if agent == "pi" and request.pi_safe_agent_team == "on":
          warnings.append("Pi safe-agent-team is an external optional integration; no native profile was written.")
        continue
      profile_path = root / spec.native_profile_dir / (
        "meta-harness.toml" if agent == "codex" else "meta-harness.md"
      )
      operations.append(
        _profile_operation(agent, profile_path, _profile_content(agent, source), root, request.force)
      )

  if request.remove_legacy:
    for layout, (project_relative, user_relative) in LEGACY_MIRRORS.items():
      relative = project_relative if request.scope == "project" else user_relative
      legacy = root / relative
      if not _path_exists(legacy):
        continue
      if _is_managed_skill(legacy, source):
        operations.append(
          InstallOperation(Action.REMOVE, legacy, source, reason=f"explicitly remove deprecated {layout} mirror")
        )
      else:
        operations.append(
          InstallOperation(
            Action.CONFLICT,
            legacy,
            source,
            owner="user",
            reason=f"refusing to remove unknown {layout} path",
          )
        )

  return InstallPlan(
    request=request,
    root=root,
    operations=tuple(operations),
    warnings=tuple(dict.fromkeys(warnings)),
    post_install_notes=tuple(post_install_notes(request, root)),
  )


def _remove_path(path: Path) -> None:
  if path.is_symlink() or path.is_file():
    path.unlink()
  elif path.exists():
    shutil.rmtree(path)


def _write_marker(destination: Path, source: Path, mode: str) -> None:
  marker = {
    "managed_by": "meta-harness",
    "schema_version": MARKER_VERSION,
    "kind": "portable-skill",
    "payload_sha256": payload_digest(source),
    "mode": mode,
  }
  (destination / MARKER_NAME).write_text(
    json.dumps(marker, indent=2, sort_keys=True) + "\n", encoding="utf-8"
  )


def _snapshot_path(path: Path) -> tuple[str, Path | str] | None:
  """Copy one managed path into a temporary location for transaction rollback."""
  if not _path_exists(path):
    return None
  backup_root = Path(tempfile.mkdtemp(prefix="meta-harness-backup-"))
  if path.is_symlink():
    link_target = backup_root / "symlink-target"
    link_target.write_text(os.readlink(path), encoding="utf-8")
    return ("symlink", link_target)
  backup = backup_root / "payload"
  if path.is_dir():
    shutil.copytree(path, backup)
    return ("directory", backup)
  shutil.copy2(path, backup)
  return ("file", backup)


def _restore_snapshot(path: Path, snapshot: tuple[str, Path | str]) -> None:
  kind, value = snapshot
  _remove_path(path)
  path.parent.mkdir(parents=True, exist_ok=True)
  if kind == "symlink":
    target = Path(value).read_text(encoding="utf-8")
    path.symlink_to(target, target_is_directory=os.path.isdir(target))
  elif kind == "directory":
    shutil.copytree(Path(value), path)
  else:
    shutil.copy2(Path(value), path)


def apply_install_plan(plan: InstallPlan) -> tuple[InstallOperation, ...]:
  """Apply a preflighted plan and return operations that were executed.

  All conflicts are checked before the first mutation. Existing managed paths
  are snapshotted so a copy/profile failure can restore the prior state rather
  than leaving a partially applied multi-runtime installation.
  """
  if plan.has_conflicts:
    joined = "; ".join(
      f"{_display_path(op.destination, plan.root)} ({op.reason})" for op in plan.conflicts
    )
    raise InstallerError(f"Install plan has conflicts: {joined}")
  applied: list[InstallOperation] = []
  snapshots: list[tuple[Path, tuple[str, Path | str]]] = []
  try:
    for operation in plan.operations:
      if operation.action in (Action.KEEP, Action.SKIP):
        continue
      if operation.action in (Action.REMOVE, Action.UPDATE):
        snapshot = _snapshot_path(operation.destination)
        if snapshot is not None:
          snapshots.append((operation.destination, snapshot))
      if operation.action == Action.REMOVE:
        _remove_path(operation.destination)
        applied.append(operation)
        continue
      if operation.generated_content is not None:
        operation.destination.parent.mkdir(parents=True, exist_ok=True)
        operation.destination.write_text(operation.generated_content, encoding="utf-8")
        applied.append(operation)
        continue
      if operation.source is None:
        raise InstallerError(f"Missing source for {operation.destination}")
      if operation.action == Action.UPDATE and _path_exists(operation.destination):
        _remove_path(operation.destination)
      operation.destination.parent.mkdir(parents=True, exist_ok=True)
      if plan.request.mode == "copy":
        shutil.copytree(
          operation.source,
          operation.destination,
          ignore=shutil.ignore_patterns("__pycache__", "*.pyc", MARKER_NAME),
        )
        _write_marker(operation.destination, operation.source, "copy")
      else:
        try:
          operation.destination.symlink_to(operation.source, target_is_directory=True)
        except (OSError, NotImplementedError) as error:
          raise InstallerError(
            "symlink mode is unavailable on this platform; use --mode copy or enable directory-link permissions"
          ) from error
      applied.append(operation)
  except Exception:
    # Remove every newly written path first, then restore managed snapshots in
    # reverse order. This is best-effort for unexpected filesystem failures but
    # keeps deterministic preflight conflicts fully side-effect free.
    for operation in reversed(applied):
      if operation.action in (Action.CREATE, Action.UPDATE):
        try:
          _remove_path(operation.destination)
        except OSError:
          pass
    for path, snapshot in reversed(snapshots):
      try:
        _restore_snapshot(path, snapshot)
      except OSError:
        pass
    raise
  finally:
    for _, snapshot in snapshots:
      value = snapshot[1]
      if isinstance(value, Path):
        backup_root = value.parent
        shutil.rmtree(backup_root, ignore_errors=True)
  return tuple(applied)


def runtime_selections(agents: Sequence[str]) -> tuple[RuntimeSpec, ...]:
  return tuple(RUNTIME_SPECS[name] for name in normalize_agents(agents))


def install_request_from_values(**values: object) -> InstallRequest:
  return InstallRequest(**values)  # type: ignore[arg-type]


__all__ = [
  "ACTIVE_AGENTS",
  "Action",
  "InstallOperation",
  "InstallPlan",
  "InstallRequest",
  "InstallerError",
  "LEGACY_LAYOUTS",
  "MODES",
  "RUNTIME_SPECS",
  "RuntimeSpec",
  "SCOPES",
  "SOURCE_SKILL_DIR",
  "apply_install_plan",
  "build_install_plan",
  "destination_specs",
  "install_request_from_values",
  "normalize_agents",
  "payload_digest",
  "resolve_root",
  "runtime_selections",
  "user_home",
]
