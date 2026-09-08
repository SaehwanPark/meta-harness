#!/usr/bin/env python3
"""Tests for CLI launchers and installation scripts."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.8.4"


def assert_true(condition: bool, message: str) -> None:
  if not condition:
    raise AssertionError(message)


def test_root_unix_launcher() -> None:
  launcher = ROOT / "meta-harness"
  assert_true(launcher.exists(), "meta-harness launcher should exist in repo root")
  assert_true(os.access(launcher, os.X_OK), "meta-harness launcher should be executable")

  # Test --version
  result = subprocess.run(
    [str(launcher), "--version"],
    capture_output=True,
    text=True,
    cwd=ROOT,
    check=False,
  )
  assert_true(result.returncode == 0, f"meta-harness --version failed: {result.stderr}")
  assert_true(VERSION in result.stdout, f"Expected version {VERSION} in output, got: {result.stdout}")

  # Test --help
  result_help = subprocess.run(
    [str(launcher), "--help"],
    capture_output=True,
    text=True,
    cwd=ROOT,
    check=False,
  )
  assert_true(result_help.returncode == 0, f"meta-harness --help failed: {result_help.stderr}")
  assert_true("install" in result_help.stdout, "Expected 'install' in help output")


def test_windows_launchers_exist() -> None:
  cmd_launcher = ROOT / "meta-harness.cmd"
  ps1_launcher = ROOT / "meta-harness.ps1"
  assert_true(cmd_launcher.exists(), "meta-harness.cmd should exist in repo root")
  assert_true(ps1_launcher.exists(), "meta-harness.ps1 should exist in repo root")

  cmd_content = cmd_launcher.read_text(encoding="utf-8")
  assert_true("scripts\\install_harness.py" in cmd_content, "meta-harness.cmd should reference install_harness.py")

  ps1_content = ps1_launcher.read_text(encoding="utf-8")
  assert_true("install_harness.py" in ps1_content, "meta-harness.ps1 should reference install_harness.py")


def test_install_sh() -> None:
  install_sh = ROOT / "install.sh"
  assert_true(install_sh.exists(), "install.sh should exist in repo root")
  assert_true(os.access(install_sh, os.X_OK), "install.sh should be executable")

  with tempfile.TemporaryDirectory(prefix="meta-harness-test-bin-") as tmp:
    tmp_bin = Path(tmp).resolve() / "bin"
    result = subprocess.run(
      [str(install_sh), "--bin-dir", str(tmp_bin)],
      capture_output=True,
      text=True,
      cwd=ROOT,
      check=False,
    )
    assert_true(result.returncode == 0, f"install.sh failed: {result.stderr}")
    assert_true("installed successfully" in result.stdout, f"Expected success message, got: {result.stdout}")

    installed_launcher = tmp_bin / "meta-harness"
    assert_true(installed_launcher.exists(), "Installed launcher should exist in target bin-dir")
    assert_true(os.access(installed_launcher, os.X_OK), "Installed launcher should be executable")

    # Run the installed launcher
    version_result = subprocess.run(
      [str(installed_launcher), "--version"],
      capture_output=True,
      text=True,
      check=False,
    )
    assert_true(version_result.returncode == 0, f"Installed launcher --version failed: {version_result.stderr}")
    assert_true(VERSION in version_result.stdout, f"Installed launcher output missing version: {version_result.stdout}")


def test_install_ps1_content() -> None:
  install_ps1 = ROOT / "install.ps1"
  assert_true(install_ps1.exists(), "install.ps1 should exist in repo root")
  content = install_ps1.read_text(encoding="utf-8")
  assert_true("meta-harness.cmd" in content, "install.ps1 should create meta-harness.cmd")
  assert_true("meta-harness.ps1" in content, "install.ps1 should create meta-harness.ps1")
  assert_true("SetEnvironmentVariable" in content, "install.ps1 should configure user PATH")
  assert_true("$env:PATH" in content, "install.ps1 should update current session PATH")


def main() -> int:
  test_root_unix_launcher()
  test_windows_launchers_exist()
  test_install_sh()
  test_install_ps1_content()
  print("OK: CLI launchers and installation scripts tests passed.")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
