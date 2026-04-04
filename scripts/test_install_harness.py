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
  shared_skill = project_root / ".agents" / "skills" / "harness" / "SKILL.md"
  assert_true(shared_skill.exists(), f"Missing shared install: {shared_skill}")
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


def main() -> int:
  with tempfile.TemporaryDirectory(prefix="meta-harness-install-") as tmp:
    tmp_root = Path(tmp)

    project_standard = tmp_root / "project-standard"
    project_standard.mkdir()
    run_install(
      "--scope", "project", "--target", str(project_standard), "--layout", "standard"
    )
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

    home_root = tmp_root / "home"
    home_root.mkdir()
    home_env = os.environ.copy()
    home_env["HOME"] = str(home_root)
    run_install("--scope", "user", "--layout", "standard", env=home_env)
    shared_user_skill = home_root / ".agents" / "skills" / "harness" / "SKILL.md"
    assert_true(
      shared_user_skill.exists(), f"Missing user-level install: {shared_user_skill}"
    )
    assert_true(
      not shared_user_skill.is_symlink(), "Expected copy mode for user install"
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

  print("OK: Harness installer smoke tests passed.")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
