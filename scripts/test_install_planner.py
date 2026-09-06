#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from installer_core import (
  Action,
  InstallRequest,
  InstallerError,
  apply_install_plan,
  build_install_plan,
  normalize_agents,
)


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install_harness.py"


def assert_true(condition: bool, message: str) -> None:
  if not condition:
    raise AssertionError(message)


def actions(plan):
  return [operation.action for operation in plan.operations]


def run_cli(*args: str, env: dict[str, str] | None = None, expect: int = 0):
  result = subprocess.run(
    [sys.executable, str(INSTALLER), *args],
    cwd=ROOT,
    env=env,
    text=True,
    capture_output=True,
    check=False,
  )
  if result.returncode != expect:
    raise AssertionError(
      f"Unexpected installer status {result.returncode} (expected {expect})\n"
      f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
  return result


def main() -> int:
  assert_true(
    normalize_agents(("cursor", "pi", "cursor", "generic"))
    == ["pi", "cursor", "generic"],
    "agent normalization should deduplicate and be deterministic",
  )

  with tempfile.TemporaryDirectory(prefix="meta-harness-planner-") as tmp:
    root = Path(tmp) / "project"
    root.mkdir()

    request = InstallRequest("project", root, ("cursor", "pi", "cursor"))
    first = build_install_plan(request)
    assert_true(actions(first) == [Action.CREATE], "first install should create one shared destination")
    assert_true(len(first.operations) == 1, "multi-runtime install should deduplicate shared skill")
    assert_true(not (root / ".agents").exists(), "planning must not mutate the target")
    apply_install_plan(first)
    assert_true((root / ".agents/skills/harness/SKILL.md").exists(), "shared skill missing")

    second = build_install_plan(request)
    assert_true(actions(second) == [Action.KEEP], "identical reinstall should be idempotent")
    apply_install_plan(second)

    marker = root / ".agents/skills/harness/.meta-harness-install.json"
    marker_data = json.loads(marker.read_text(encoding="utf-8"))
    marker_data["payload_sha256"] = "stale"
    marker.write_text(json.dumps(marker_data), encoding="utf-8")
    stale = build_install_plan(request)
    assert_true(actions(stale) == [Action.UPDATE], "stale managed install should update")
    apply_install_plan(stale)

    unknown_root = Path(tmp) / "unknown"
    unknown_root.mkdir()
    unknown_destination = unknown_root / ".agents/skills/harness"
    unknown_destination.mkdir(parents=True)
    (unknown_destination / "README.md").write_text("user-owned", encoding="utf-8")
    conflict = build_install_plan(InstallRequest("project", unknown_root, ("generic",)))
    assert_true(conflict.has_conflicts, "unknown destination should be a conflict")
    try:
      apply_install_plan(conflict)
    except InstallerError:
      pass
    else:
      raise AssertionError("conflicting plan should not apply")
    assert_true(
      (unknown_destination / "README.md").read_text(encoding="utf-8") == "user-owned",
      "conflict application must not mutate user-owned files",
    )
    forced_conflict = build_install_plan(
      InstallRequest("project", unknown_root, ("generic",), force=True)
    )
    assert_true(forced_conflict.has_conflicts, "--force must not overwrite unknown paths")

    profile_root = Path(tmp) / "profiles"
    profile_root.mkdir()
    profiles = build_install_plan(
      InstallRequest(
        "project",
        profile_root,
        ("pi", "codex", "antigravity", "cursor"),
        native_profiles=True,
      )
    )
    profile_paths = {operation.destination.relative_to(profile_root).as_posix() for operation in profiles.operations}
    assert_true(".agents/skills/harness" in profile_paths, "profile plan must retain shared skill")
    assert_true(".codex/agents/meta-harness.toml" in profile_paths, "Codex profile missing")
    assert_true(".antigravity/agents/meta-harness.md" in profile_paths, "Antigravity profile missing")
    assert_true(".cursor/agents/meta-harness.md" in profile_paths, "Cursor profile missing")
    assert_true(not any(path.startswith(".pi/") for path in profile_paths), "Pi must not invent a native profile path")
    apply_install_plan(profiles)
    assert_true((profile_root / ".agents/skills/harness/SKILL.md").exists(), "portable skill missing after profile install")
    assert_true((profile_root / ".cursor/agents/meta-harness.md").exists(), "Cursor profile not written")

    legacy_root = Path(tmp) / "legacy"
    legacy_root.mkdir()
    legacy_request = InstallRequest("project", legacy_root, ("generic",), legacy_layout="codex")
    legacy_plan = build_install_plan(legacy_request)
    assert_true(any("deprecated" in warning for warning in legacy_plan.warnings), "legacy warning missing")
    assert_true(len(legacy_plan.operations) == 2, "legacy Codex install should include shared and mirror paths")
    apply_install_plan(legacy_plan)
    removal = build_install_plan(
      InstallRequest("project", legacy_root, ("generic",), remove_legacy=True)
    )
    assert_true(
      any(operation.action == Action.REMOVE for operation in removal.operations),
      "explicit legacy removal should plan REMOVE",
    )
    apply_install_plan(removal)
    assert_true((legacy_root / ".agents/skills/harness").exists(), "portable skill must survive rippability removal")
    assert_true(not (legacy_root / ".codex/skills/harness").exists(), "legacy mirror should be removed")

    symlink_root = Path(tmp) / "symlink"
    symlink_root.mkdir()
    try:
      symlink_request = InstallRequest("project", symlink_root, ("generic",), mode="symlink")
      symlink_first = build_install_plan(symlink_request)
      apply_install_plan(symlink_first)
      symlink_again = build_install_plan(symlink_request)
      assert_true(actions(symlink_again) == [Action.KEEP], "managed source symlink should be idempotent")
    except (OSError, InstallerError) as error:
      if isinstance(error, InstallerError) and "symlink mode" not in str(error):
        raise

    parent_link_root = Path(tmp) / "parent-link"
    parent_link_root.mkdir()
    outside = Path(tmp) / "outside"
    outside.mkdir()
    try:
      (parent_link_root / ".agents").symlink_to(outside, target_is_directory=True)
    except OSError:
      pass
    else:
      parent_conflict = build_install_plan(
        InstallRequest("project", parent_link_root, ("generic",))
      )
      assert_true(parent_conflict.has_conflicts, "symlinked destination parent must be rejected")
      assert_true(not (outside / "skills").exists(), "parent symlink conflict must not mutate outside target")

    overlap = build_install_plan(InstallRequest("project", ROOT, ("generic",)))
    assert_true(overlap.has_conflicts, "source/destination overlap must be rejected")

    user_home = Path(tmp) / "home"
    user_home.mkdir()
    env = os.environ.copy()
    env["HOME"] = str(user_home)
    env["USERPROFILE"] = str(user_home)
    user = run_cli("install", "--scope", "user", "--agent", "generic", env=env)
    assert_true((user_home / ".agents/skills/harness/SKILL.md").exists(), "user install did not honor injected home")
    dry_root = Path(tmp) / "dry"
    dry_root.mkdir()
    dry = run_cli(
      "install",
      "--scope",
      "project",
      "--target",
      str(dry_root),
      "--agent",
      "codex",
      "--agent",
      "cursor",
      "--native-profiles",
      "--dry-run",
      "--non-interactive",
    )
    assert_true("CREATE" in dry.stdout and "Dry run only" in dry.stdout, "dry-run should render plan")
    assert_true(not (dry_root / ".agents").exists(), "dry-run must not mutate target")

  print("OK: Harness installer planner tests passed.")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
