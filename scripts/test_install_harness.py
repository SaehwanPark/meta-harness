#!/usr/bin/env python3

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install_harness.py"


def assert_true(condition: bool, message: str) -> None:
  if not condition:
    raise AssertionError(message)


def assert_contains(text: str, needle: str, message: str) -> None:
  if needle not in text:
    raise AssertionError(message)


def assert_agents_note(text: str) -> None:
  assert_contains(
    text,
    "AGENTS.md stays repo-owned.",
    "Expected installer output to explain that AGENTS.md remains repo-owned.",
  )


def run_install(
  *args: str, env: dict[str, str] | None = None, expect_success: bool = True
) -> subprocess.CompletedProcess[str]:
  command = [sys.executable, str(INSTALLER), *args]
  result = subprocess.run(
    command,
    cwd=ROOT,
    env=env,
    text=True,
    capture_output=True,
    check=False,
  )
  if expect_success and result.returncode != 0:
    raise AssertionError(
      f"Installer failed: {' '.join(command)}\n{result.stderr}\n{result.stdout}"
    )
  if not expect_success and result.returncode == 0:
    raise AssertionError(f"Installer unexpectedly succeeded: {' '.join(command)}")
  return result


def assert_standard_install(project_root: Path) -> None:
  shared_root = project_root / ".agents" / "skills" / "harness"
  shared_skill = project_root / ".agents" / "skills" / "harness" / "SKILL.md"
  agents_guide = shared_root / "references" / "agents-md-guide.md"
  assert_true(shared_skill.exists(), f"Missing shared install: {shared_skill}")
  assert_true(agents_guide.exists(), f"Missing AGENTS guide: {agents_guide}")
  assert_true(
    not shared_skill.is_symlink(), "Expected copy mode to create a standalone SKILL.md"
  )
  assert_true(
    not (project_root / "AGENTS.md").exists(),
    "Installer should not create AGENTS.md in the target",
  )
  assert_true(
    not (project_root / "README.md").exists(),
    "Installer should not create README.md in the target",
  )
  assert_true(
    not (project_root / "docs").exists(),
    "Installer should not create docs/ in the target",
  )


def assert_shared_install(project_root: Path, expect_symlink: bool = False) -> None:
  shared_root = project_root / ".agents" / "skills" / "harness"
  shared_skill = shared_root / "SKILL.md"
  agents_guide = shared_root / "references" / "agents-md-guide.md"
  assert_true(shared_skill.exists(), f"Missing shared install: {shared_skill}")
  assert_true(agents_guide.exists(), f"Missing AGENTS guide: {agents_guide}")
  assert_true(
    shared_root.is_symlink() == expect_symlink,
    f"Expected shared install symlink={expect_symlink}: {shared_root}",
  )


def main() -> int:
  with tempfile.TemporaryDirectory(prefix="meta-harness-install-") as tmp:
    tmp_root = Path(tmp)

    project_dry_run = tmp_root / "project-dry-run"
    project_dry_run.mkdir()
    dry_run = run_install(
      "--scope",
      "project",
      "--target",
      str(project_dry_run),
      "--layout",
      "standard",
      "--dry-run",
    )
    assert_contains(
      dry_run.stdout,
      "Dry run only; no changes made.",
      "Expected dry-run output to confirm no changes were made.",
    )
    assert_agents_note(dry_run.stdout)
    assert_true(
      not (project_dry_run / ".agents").exists(),
      "Dry run should not create the shared install path.",
    )

    project_standard = tmp_root / "project-standard"
    project_standard.mkdir()
    standard_install = run_install(
      "--scope", "project", "--target", str(project_standard), "--layout", "standard"
    )
    assert_agents_note(standard_install.stdout)
    assert_standard_install(project_standard)
    rerun = run_install(
      "--scope",
      "project",
      "--target",
      str(project_standard),
      "--layout",
      "standard",
      expect_success=False,
    )
    assert_true(
      "Destination already exists" in rerun.stderr,
      "Expected rerun without --force to fail cleanly.",
    )
    marker = project_standard / ".agents" / "skills" / "harness" / "marker.txt"
    marker.write_text("replace me", encoding="utf-8")
    run_install(
      "--scope",
      "project",
      "--target",
      str(project_standard),
      "--layout",
      "standard",
      "--force",
    )
    assert_standard_install(project_standard)
    assert_true(not marker.exists(), "Expected --force to replace the prior install tree.")

    home_root = tmp_root / "home"
    home_root.mkdir()
    home_env = os.environ.copy()
    home_env["HOME"] = str(home_root)
    user_standard = run_install("--scope", "user", "--layout", "standard", env=home_env)
    assert_agents_note(user_standard.stdout)
    shared_user_skill = home_root / ".agents" / "skills" / "harness" / "SKILL.md"
    assert_true(
      shared_user_skill.exists(), f"Missing user-level install: {shared_user_skill}"
    )
    assert_true(
      not shared_user_skill.is_symlink(), "Expected copy mode for user install"
    )
    user_dry_run = run_install(
      "--scope", "user", "--layout", "aider", "--dry-run", env=home_env
    )
    assert_contains(
      user_dry_run.stdout,
      str(home_root / ".aider.conf.yml"),
      "Expected aider dry-run output to include the user config path.",
    )

    codex_home_root = tmp_root / "home-codex"
    codex_home_root.mkdir()
    codex_env = os.environ.copy()
    codex_env["HOME"] = str(codex_home_root)
    user_codex = run_install("--scope", "user", "--layout", "codex", env=codex_env)
    assert_true(
      (codex_home_root / ".agents" / "skills" / "harness" / "SKILL.md").exists(),
      "Missing shared user-level install alongside Codex mirror.",
    )
    assert_true(
      (codex_home_root / ".codex" / "skills" / "harness" / "SKILL.md").exists(),
      "Missing user-level Codex mirror install.",
    )
    assert_contains(
      user_codex.stdout,
      "Codex can use the shared install and the native .codex/skills mirror.",
      "Expected Codex post-install guidance in output.",
    )

    project_forge = tmp_root / "project-forge"
    project_forge.mkdir()
    run_install(
      "--scope", "project", "--target", str(project_forge), "--layout", "forgecode"
    )
    assert_standard_install(project_forge)
    assert_true(
      (project_forge / ".forge" / "skills" / "harness" / "SKILL.md").exists(),
      "Missing ForgeCode mirror install.",
    )

    project_droid = tmp_root / "project-droid"
    project_droid.mkdir()
    run_install(
      "--scope", "project", "--target", str(project_droid), "--layout", "droid"
    )
    assert_standard_install(project_droid)
    assert_true(
      (project_droid / ".factory" / "skills" / "harness" / "SKILL.md").exists(),
      "Missing Droid mirror install.",
    )

    project_codex = tmp_root / "project-codex"
    project_codex.mkdir()
    run_install(
      "--scope", "project", "--target", str(project_codex), "--layout", "codex"
    )
    assert_standard_install(project_codex)
    assert_true(
      (project_codex / ".codex" / "skills" / "harness" / "SKILL.md").exists(),
      "Missing Codex mirror install.",
    )

    project_openhands = tmp_root / "project-openhands"
    project_openhands.mkdir()
    openhands = run_install(
      "--scope", "project", "--target", str(project_openhands), "--layout", "openhands"
    )
    assert_standard_install(project_openhands)
    assert_contains(
      openhands.stdout,
      "OpenHands uses the shared .agents/skills/ location",
      "Expected OpenHands guidance in post-install notes.",
    )

    project_aider = tmp_root / "project-aider"
    project_aider.mkdir()
    aider = run_install(
      "--scope", "project", "--target", str(project_aider), "--layout", "aider"
    )
    assert_standard_install(project_aider)
    assert_contains(
      aider.stdout,
      str(project_aider / ".aider.conf.yml"),
      "Expected Aider follow-up output to include the project config path.",
    )

    project_symlink = tmp_root / "project-symlink"
    project_symlink.mkdir()
    run_install(
      "--scope",
      "project",
      "--target",
      str(project_symlink),
      "--layout",
      "standard",
      "--mode",
      "symlink",
    )
    assert_shared_install(project_symlink, expect_symlink=True)

  print("OK: Harness installer smoke tests passed.")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
