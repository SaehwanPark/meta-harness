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
import re
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
ROLE_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


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
  roles: tuple[Path, ...] = ()
  model_policy: str = "inherit"
  runtime_overrides: Mapping[str, str] = field(default_factory=dict)

  def __post_init__(self) -> None:
    if self.scope not in SCOPES:
      raise InstallerError(f"Unknown install scope: {self.scope}")
    if self.mode not in MODES:
      raise InstallerError(f"Unknown install mode: {self.mode}")
    if self.pi_safe_agent_team not in ("auto", "on", "off"):
      raise InstallerError("pi_safe_agent_team must be auto, on, or off")
    if self.model_policy not in MODEL_POLICIES:
      raise InstallerError(
        f"Unknown model policy '{self.model_policy}'. Choose one of: {', '.join(MODEL_POLICIES)}"
      )
    if self.legacy_layout is not None and self.legacy_layout not in LEGACY_LAYOUTS:
      raise InstallerError(f"Unknown legacy layout: {self.legacy_layout}")
    normalized_agents = tuple(normalize_agents(self.agents))
    if not normalized_agents:
      raise InstallerError("at least one runtime agent must be selected")
    unknown_overrides = set(self.runtime_overrides) - set(RUNTIME_SPECS)
    if unknown_overrides:
      raise InstallerError(
        f"Unknown runtime override(s): {', '.join(sorted(unknown_overrides))}"
      )
    object.__setattr__(self, "agents", normalized_agents)
    object.__setattr__(self, "source", Path(self.source).expanduser().resolve())
    if self.target is not None:
      object.__setattr__(self, "target", Path(self.target).expanduser().resolve())
    object.__setattr__(self, "roles", tuple(Path(role) for role in self.roles))
    object.__setattr__(self, "runtime_overrides", dict(self.runtime_overrides))


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
        "roles": [str(role) for role in self.request.roles],
        "model_policy": self.request.model_policy,
        "runtime_overrides": dict(self.request.runtime_overrides),
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


@dataclass(frozen=True)
class RoleDefinition:
  name: str
  source: Path | None = None
  responsibility: str = "Run the portable Meta Harness workflow."
  reads: tuple[str, ...] = ()
  writes: tuple[str, ...] = ()
  workspace: str = "shared"
  communication: str = "parent-mediated summary"
  model_policy: str = "inherit"
  completion_artifact: str = ""
  permissions: tuple[str, ...] = ()
  runtime_overrides: Mapping[str, str] = field(default_factory=dict)

  def __post_init__(self) -> None:
    name = _slugify_role_name(self.name)
    object.__setattr__(self, "name", name)
    if self.model_policy not in MODEL_POLICIES:
      raise InstallerError(f"Unknown role model policy: {self.model_policy}")
    object.__setattr__(self, "reads", tuple(str(value) for value in self.reads))
    object.__setattr__(self, "writes", tuple(str(value) for value in self.writes))
    object.__setattr__(self, "permissions", tuple(str(value) for value in self.permissions))
    normalized_overrides = dict(self.runtime_overrides)
    unknown_overrides = set(normalized_overrides) - set(RUNTIME_SPECS)
    if unknown_overrides:
      raise InstallerError(
        f"Unknown role runtime override(s): {', '.join(sorted(unknown_overrides))}"
      )
    object.__setattr__(self, "runtime_overrides", normalized_overrides)
    if self.source is not None:
      object.__setattr__(self, "source", Path(self.source).expanduser().resolve())


def _slugify_role_name(value: str) -> str:
  text = re.sub(r"[^a-zA-Z0-9]+", "-", str(value).strip()).strip("-").casefold()
  return text or "meta-harness"


def _parse_contract_value(value: str) -> object:
  value = value.strip()
  if not value:
    return ""
  if value.startswith("[") and value.endswith("]"):
    inner = value[1:-1].strip()
    if not inner:
      return []
    return [part.strip().strip('"').strip("'") for part in inner.split(",")]
  return value.strip('"').strip("'")


def _parse_runtime_overrides(contract: str) -> dict[str, str]:
  """Parse the optional ``runtime_overrides`` mapping without PyYAML."""
  overrides: dict[str, list[str]] = {}
  in_block = False
  current_agent: str | None = None
  for raw_line in contract.splitlines():
    if not raw_line.strip() or raw_line.lstrip().startswith("#"):
      continue
    indent = len(raw_line) - len(raw_line.lstrip(" "))
    stripped = raw_line.strip()
    if indent == 0 and stripped.startswith("runtime_overrides:"):
      in_block = True
      current_agent = None
      inline = stripped.split(":", 1)[1].strip()
      if inline and inline not in ("{}", "null"):
        parsed = _parse_contract_value(inline)
        if isinstance(parsed, str) and parsed:
          overrides["*"] = [parsed]
      continue
    if in_block and indent == 0:
      break
    if not in_block:
      continue
    if indent == 2 and stripped.endswith(":"):
      current_agent = stripped[:-1].strip().casefold()
      overrides.setdefault(current_agent, [])
      continue
    if indent >= 4 and current_agent and ":" in stripped:
      key, raw_value = stripped.split(":", 1)
      value = str(_parse_contract_value(raw_value))
      overrides[current_agent].append(f"{key.strip()}={value}")
  return {agent: ", ".join(values) for agent, values in overrides.items() if agent != "*" and values}


def parse_role_definition(path: str | Path) -> RoleDefinition:
  """Read a lightweight YAML contract block from a role brief.

  Full YAML is intentionally not required: role contracts use a small scalar
  and inline-list subset so compilation remains dependency-free. A prose-only
  role brief still compiles with its filename and heading as a safe default.
  """
  role_path = Path(path).expanduser().resolve()
  if not role_path.is_file():
    raise InstallerError(f"Role definition does not exist: {role_path}")
  text = role_path.read_text(encoding="utf-8")
  block_match = re.search(r"```(?:yaml|yml)\s*\n(.*?)```", text, re.IGNORECASE | re.DOTALL)
  values: dict[str, object] = {}
  if block_match:
    current_nested: str | None = None
    for raw_line in block_match.group(1).splitlines():
      if not raw_line.strip() or raw_line.lstrip().startswith("#"):
        continue
      stripped = raw_line.strip()
      if stripped.endswith(":") and ":" not in stripped[:-1]:
        current_nested = stripped[:-1]
        continue
      if ":" not in stripped:
        continue
      key, raw_value = stripped.split(":", 1)
      key = key.strip()
      parsed = _parse_contract_value(raw_value)
      values[key] = parsed
      if current_nested and key in ("preference", "artifact", "parent", "target"):
        values[f"{current_nested}.{key}"] = parsed
  heading = re.search(r"^#\s+(.+?)\s*$", text, re.MULTILINE)
  name = str(values.get("role") or _slugify_role_name(heading.group(1) if heading else role_path.stem))
  responsibility = str(values.get("responsibility") or "Run the portable role and return evidence.")
  reads = values.get("reads", values.get("resources.reads", ()))
  writes = values.get("writes", values.get("resources.writes", ()))
  workspace = str(values.get("workspace", values.get("workspace.preference", "shared")))
  if isinstance(values.get("workspace"), dict):
    workspace = str(values["workspace"].get("preference", "shared"))  # type: ignore[union-attr]
  communication = str(
    values.get("communication", values.get("communication.parent", "parent-mediated summary"))
  )
  model_policy = str(values.get("model_policy", "inherit"))
  completion = values.get("completion.artifact", values.get("artifact", ""))
  permissions = values.get("permissions", ())
  runtime_overrides = _parse_runtime_overrides(block_match.group(1)) if block_match else {}
  def as_tuple(value: object) -> tuple[str, ...]:
    if isinstance(value, (list, tuple)):
      return tuple(str(item) for item in value)
    return (str(value),) if value else ()
  return RoleDefinition(
    name=name,
    source=role_path,
    responsibility=responsibility,
    reads=as_tuple(reads),
    writes=as_tuple(writes),
    workspace=workspace,
    communication=communication,
    model_policy=model_policy,
    completion_artifact=str(completion),
    permissions=as_tuple(permissions),
    runtime_overrides=runtime_overrides,
  )


def discover_role_definitions(root: Path, paths: Sequence[Path] = ()) -> tuple[RoleDefinition, ...]:
  selected = tuple(paths) or tuple(sorted((root / "docs" / "harness").glob("**/roles/*.md")))
  if not selected:
    return (RoleDefinition("meta-harness"),)
  return tuple(parse_role_definition(path) for path in selected)


def normalize_roles(root: Path, roles: Iterable[Path]) -> tuple[Path, ...]:
  result: list[Path] = []
  for role in roles:
    path = Path(role).expanduser()
    if not path.is_absolute():
      target_path = root / path
      path = target_path if target_path.exists() or not Path(path).exists() else Path(path)
    path = path.resolve()
    if path not in result:
      result.append(path)
  return tuple(result)


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


def _inline_text(value: object) -> str:
  """Keep user-authored role values on one generated-profile line."""
  return " ".join(str(value).replace("\r", " ").replace("\n", " ").split())


def _toml_escape(value: object, multiline: bool = False) -> str:
  escaped: list[str] = []
  for character in str(value):
    codepoint = ord(character)
    if character == "\\":
      escaped.append("\\\\")
    elif character == '"':
      escaped.append('\\"')
    elif character == "\n":
      escaped.append("\n" if multiline else " ")
    elif character == "\r":
      escaped.append("\\r" if multiline else " ")
    elif character == "\t":
      escaped.append("\\t")
    elif character == "\b":
      escaped.append("\\b")
    elif character == "\f":
      escaped.append("\\f")
    elif codepoint < 0x20:
      escaped.append(f"\\u{codepoint:04x}")
    else:
      escaped.append(character)
  return "".join(escaped)


def _toml_string(value: str) -> str:
  return _toml_escape(value)


def _profile_content(
  agent: str,
  source: Path,
  role: RoleDefinition,
  model_policy: str = "inherit",
  runtime_override: str = "",
) -> str:
  skill_path = ".agents/skills/harness/SKILL.md"
  responsibility = _inline_text(role.responsibility)
  reads = ", ".join(_inline_text(value) for value in role.reads) or "declared portable inputs"
  writes = ", ".join(_inline_text(value) for value in role.writes) or "no repository writes unless the role contract says otherwise"
  workspace = _inline_text(role.workspace) or "shared"
  communication = _inline_text(role.communication) or "parent-mediated summary"
  completion = _inline_text(role.completion_artifact) or "the role's declared completion evidence"
  override_note = (
    f"Runtime override (removable): {_inline_text(runtime_override)}.\n" if runtime_override else ""
  )
  if agent == "codex":
    instructions = (
      f"Read {skill_path} as the source of truth.\n"
      f"Responsibility: {responsibility}\n"
      f"Read boundary: {reads}. Write boundary: {writes}.\n"
      f"Workspace: {workspace}. Communication: {communication}.\n"
      f"Completion evidence: {completion}. Preserve safe ownership and report partial failures.\n"
      f"Model policy: {model_policy}. Inherit runtime defaults unless an explicit override is justified.\n"
      + override_note
    )
    return (
      "# Generated by Meta Harness; edit the portable role contract instead.\n"
      f'name = "{_toml_string(role.name)}"\n'
      f'description = "{_toml_string(responsibility)}"\n'
      f'developer_instructions = """\n{_toml_escape(instructions, multiline=True)}"""\n'
    )
  label = RUNTIME_SPECS[agent].label
  return (
    "---\n"
    f"name: {role.name}\n"
    f'description: "{_toml_escape(responsibility)}"\n'
    "---\n"
    "<!-- Generated by Meta Harness; edit the portable role contract instead. -->\n\n"
    f"# {label} execution profile: {role.name}\n\n"
    f"Read `{skill_path}` as the source of truth.\n\n"
    f"- Responsibility: {responsibility}\n"
    f"- Reads: {reads}\n"
    f"- Writes: {writes}\n"
    f"- Workspace: {workspace}\n"
    f"- Communication: {communication}\n"
    f"- Completion evidence: {completion}\n"
    f"- Model policy: `{model_policy}`; inherit runtime defaults unless overridden intentionally.\n"
    + (
      f"- Runtime override (removable): {_inline_text(runtime_override)}\n"
      if runtime_override
      else ""
    )
    + "\nDo not silently weaken a required ownership or capability guarantee.\n"
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
    if (
      existing.startswith("# Generated by Meta Harness")
      or existing.startswith("<!-- Generated by Meta Harness")
      or "<!-- Generated by Meta Harness" in existing[:300]
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
    role_paths = normalize_roles(root, request.roles)
    roles = discover_role_definitions(root, role_paths)
    role_names = [role.name for role in roles]
    if len(role_names) != len(set(role_names)):
      raise InstallerError("role definitions must have unique slugified names")
    for agent in request.agents:
      spec = RUNTIME_SPECS[agent]
      if spec.native_profile_dir is None:
        if agent == "pi" and request.pi_safe_agent_team == "on":
          warnings.append("Pi safe-agent-team is an external optional integration; no native profile was written.")
        elif agent == "generic":
          warnings.append("Generic mode has no native profile format; portable skills remain canonical.")
        continue
      for role in roles:
        profile_name = f"{role.name}.{'toml' if agent == 'codex' else 'md'}"
        profile_path = root / spec.native_profile_dir / profile_name
        override = request.runtime_overrides.get(
          agent, role.runtime_overrides.get(agent, "")
        )
        effective_policy = (
          request.model_policy if request.model_policy != "inherit" else role.model_policy
        )
        operations.append(
          _profile_operation(
            agent,
            profile_path,
            _profile_content(agent, source, role, effective_policy, override),
            root,
            request.force,
          )
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
  touched: list[Path] = []
  snapshots: list[tuple[Path, tuple[str, Path | str]]] = []
  try:
    for operation in plan.operations:
      if operation.action in (Action.CREATE, Action.UPDATE, Action.REMOVE):
        touched.append(operation.destination)
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
    # Remove every touched path first (including a CREATE that failed halfway),
    # then restore managed snapshots in reverse order. This is best-effort for
    # unexpected filesystem failures but keeps deterministic preflight conflicts
    # fully side-effect free.
    for path in reversed(touched):
      try:
        _remove_path(path)
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
  "RoleDefinition",
  "SCOPES",
  "SOURCE_SKILL_DIR",
  "apply_install_plan",
  "build_install_plan",
  "destination_specs",
  "install_request_from_values",
  "normalize_agents",
  "parse_role_definition",
  "discover_role_definitions",
  "normalize_roles",
  "payload_digest",
  "resolve_root",
  "runtime_selections",
  "user_home",
]
