#!/usr/bin/env python3
"""Dependency-free, keyboard-oriented installer frontend.

This module owns presentation and selection state only.  Planning and mutation
remain in :mod:`installer_core`, so CLI and TUI requests have identical
semantics.
"""

from __future__ import annotations

import shutil
import sys
from dataclasses import dataclass, replace
from pathlib import Path
from typing import TextIO

try:
  from installer_core import (
    ACTIVE_AGENTS,
    MODES,
    MODEL_POLICIES,
    SOURCE_SKILL_DIR,
    Action,
    InstallPlan,
    InstallRequest,
    InstallerError,
    apply_install_plan,
    build_install_plan,
    normalize_agents,
  )
except ModuleNotFoundError:  # pragma: no cover
  from scripts.installer_core import (
    ACTIVE_AGENTS,
    MODES,
    MODEL_POLICIES,
    SOURCE_SKILL_DIR,
    Action,
    InstallPlan,
    InstallRequest,
    InstallerError,
    apply_install_plan,
    build_install_plan,
    normalize_agents,
  )


@dataclass(frozen=True)
class TuiState:
  scope: str = "project"
  target: str = "."
  agents: tuple[str, ...] = ("pi",)
  mode: str = "copy"
  native_profiles: bool = True
  pi_safe_agent_team: str = "auto"
  model_policy: str = "inherit"
  force: bool = False
  dry_run: bool = False

  def selected_agents(self) -> tuple[str, ...]:
    return tuple(normalize_agents(self.agents))

  def toggle_agent(self, agent: str) -> "TuiState":
    current = set(self.agents)
    if agent in current:
      current.remove(agent)
    else:
      current.add(agent)
    if not current:
      current.add("generic")
    return replace(self, agents=tuple(normalize_agents(current)))

  def to_request(self, source: Path = SOURCE_SKILL_DIR) -> InstallRequest:
    target = Path(self.target).expanduser() if self.scope == "project" else None
    return InstallRequest(
      scope=self.scope,
      target=target,
      agents=self.selected_agents(),
      mode=self.mode,
      native_profiles=self.native_profiles,
      pi_safe_agent_team=self.pi_safe_agent_team,
      model_policy=self.model_policy,
      force=self.force,
      dry_run=self.dry_run,
      source=source,
    )


def _checkbox(enabled: bool) -> str:
  return "[x]" if enabled else "[ ]"


def render_main_screen(state: TuiState, compact: bool = False) -> str:
  lines = ["Meta Harness Installer", ""]
  lines.extend(
    [
      "Installation scope",
      f"  (*) Project   {state.target if state.scope == 'project' else ''}" if state.scope == "project" else "  ( ) Project",
      "  (*) User" if state.scope == "user" else "  ( ) User",
      "",
      "Actively supported coding agents",
    ]
  )
  for agent in ACTIVE_AGENTS:
    lines.append(f"  {_checkbox(agent in state.agents)} {agent}")
  lines.extend(
    [
      "",
      f"  {_checkbox(state.pi_safe_agent_team != 'off')} Use pi-safe-agent-team when available",
      f"  {_checkbox(state.native_profiles)} Generate native execution profiles",
      f"  Model policy: {state.model_policy}",
      f"  (*) Copy    {'( ) Symlink' if state.mode == 'copy' else '(*) Symlink'}",
      "  [ Continue ]   [ Dry Run ]   [ Cancel ]",
    ]
  )
  if compact:
    return "\n".join(
      [
        "Meta Harness Installer (compact)",
        f"scope={state.scope} target={state.target or '-'}",
        f"agents={','.join(state.agents)} mode={state.mode} profiles={state.native_profiles} model={state.model_policy}",
        "Enter values as prompted; q cancels.",
      ]
    )
  return "\n".join(lines)


def render_preview(plan: InstallPlan) -> str:
  return plan.render()


def _ask(output: TextIO, stream: TextIO, prompt: str, default: str = "") -> str:
  output.write(prompt)
  output.flush()
  value = stream.readline()
  if value == "":
    raise EOFError
  value = value.strip()
  return value or default


def _select_agents(value: str) -> tuple[str, ...]:
  selected: list[str] = []
  values = [part.strip().casefold() for part in value.replace(" ", "").split(",") if part.strip()]
  for item in values:
    if item.isdigit():
      index = int(item) - 1
      if 0 <= index < len(ACTIVE_AGENTS):
        selected.append(ACTIVE_AGENTS[index])
    elif item in ACTIVE_AGENTS:
      selected.append(item)
  if not selected:
    raise InstallerError("select at least one runtime (for example: pi,cursor)")
  return tuple(normalize_agents(selected))


def run_tui(
  source: Path = SOURCE_SKILL_DIR,
  input_stream: TextIO | None = None,
  output_stream: TextIO | None = None,
) -> int:
  input_stream = input_stream or sys.stdin
  output_stream = output_stream or sys.stdout
  if not (input_stream.isatty() and output_stream.isatty()):
    output_stream.write("ERROR: interactive mode requires a TTY.\n")
    return 1

  columns = shutil.get_terminal_size(fallback=(80, 24)).columns
  compact = columns < 60
  state = TuiState()
  output_stream.write(render_main_screen(state, compact=compact) + "\n\n")
  try:
    scope = _ask(output_stream, input_stream, "Scope [project/user] (project): ", "project").casefold()
    if scope not in ("project", "user"):
      raise InstallerError("scope must be project or user")
    target = "."
    if scope == "project":
      target = _ask(output_stream, input_stream, "Target directory (.): ", ".")
    agent_value = _ask(
      output_stream,
      input_stream,
      "Agents (numbers 1=pi 2=codex 3=antigravity 4=cursor 5=generic): ",
      "1",
    )
    agents = _select_agents(agent_value)
    team = _ask(output_stream, input_stream, "Pi team integration [auto/on/off] (auto): ", "auto").casefold()
    if team not in ("auto", "on", "off"):
      raise InstallerError("Pi team integration must be auto, on, or off")
    profiles = _ask(output_stream, input_stream, "Generate native profiles [Y/n]: ", "y").casefold() not in (
      "n",
      "no",
    )
    model_policy = _ask(
      output_stream,
      input_stream,
      "Model policy [inherit/fast/economy/balanced/strong] (inherit): ",
      "inherit",
    ).casefold()
    if model_policy not in MODEL_POLICIES:
      raise InstallerError("model policy must be inherit, fast, economy, balanced, or strong")
    mode = _ask(output_stream, input_stream, "Mode [copy/symlink] (copy): ", "copy").casefold()
    if mode not in MODES:
      raise InstallerError("mode must be copy or symlink")
    state = TuiState(
      scope=scope,
      target=target,
      agents=agents,
      mode=mode,
      native_profiles=profiles,
      pi_safe_agent_team=team,
      model_policy=model_policy,
    )
    request = state.to_request(source)
    plan = build_install_plan(request)
    output_stream.write("\nInstallation plan preview\n\n" + render_preview(plan) + "\n")
    if plan.has_conflicts:
      choice = _ask(
        output_stream,
        input_stream,
        "Conflict: [i]nspect, [r]epair managed files, or [c]ancel (c): ",
        "c",
      ).casefold()
      if choice == "r":
        repaired = replace(state, force=True)
        plan = build_install_plan(repaired.to_request(source))
        output_stream.write("\nRepair plan\n\n" + render_preview(plan) + "\n")
      if plan.has_conflicts:
        output_stream.write("No safe plan is available; nothing was changed.\n")
        return 1
    action = _ask(
      output_stream,
      input_stream,
      "[i] Install, [d] Dry Run, or [c] Cancel (c): ",
      "c",
    ).casefold()
    if action in ("c", "cancel"):
      output_stream.write("Cancelled.\n")
      return 0
    if action in ("d", "dry", "dry-run"):
      output_stream.write("Dry run only; no changes made.\n")
      return 0
    if action not in ("i", "install"):
      output_stream.write("No valid action selected; nothing was changed.\n")
      return 1
    apply_install_plan(plan)
    output_stream.write("Installed selected Meta Harness artifacts.\n")
    return 0
  except (EOFError, KeyboardInterrupt):
    output_stream.write("Cancelled.\n")
    return 0
  except (InstallerError, OSError) as error:
    output_stream.write(f"ERROR: {error}\n")
    return 1


__all__ = ["TuiState", "render_main_screen", "render_preview", "run_tui"]
