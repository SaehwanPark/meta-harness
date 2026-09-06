#!/usr/bin/env python3

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

try:
  import tomllib
except ModuleNotFoundError:  # pragma: no cover
  tomllib = None

from installer_core import (
  InstallRequest,
  apply_install_plan,
  build_install_plan,
  parse_role_definition,
)


def assert_true(condition: bool, message: str) -> None:
  if not condition:
    raise AssertionError(message)


def main() -> int:
  with tempfile.TemporaryDirectory(prefix="meta-harness-profile-") as tmp:
    root = Path(tmp)
    role = root / "docs/harness/demo/roles/reviewer.md"
    role.parent.mkdir(parents=True)
    role.write_text(
      "# Reviewer\n\n```yaml\n"
      "role: reviewer\n"
      "responsibility: review generated output\n"
      "resources:\n"
      "  reads: [src/**]\n"
      "  writes: []\n"
      "workspace:\n"
      "  preference: shared-readonly\n"
      "communication:\n"
      "  parent: orchestrator\n"
      "model_policy: strong\n"
      "runtime_overrides:\n"
      "  cursor:\n"
      "    provider: role-provider\n"
      "completion:\n"
      "  artifact: _workspace/review.md\n"
      "```\n",
      encoding="utf-8",
    )
    parsed_role = parse_role_definition(role)
    assert_true(
      parsed_role.runtime_overrides.get("cursor") == "provider=role-provider",
      "role runtime override was not parsed",
    )
    plan = build_install_plan(
      InstallRequest(
        "project",
        root,
        ("codex", "antigravity", "cursor"),
        native_profiles=True,
        roles=(role,),
        runtime_overrides={"cursor": "provider=example"},
      )
    )
    apply_install_plan(plan)
    codex = root / ".codex/agents/reviewer.toml"
    cursor = root / ".cursor/agents/reviewer.md"
    antigravity = root / ".antigravity/agents/reviewer.md"
    assert_true(codex.is_file() and cursor.is_file() and antigravity.is_file(), "all profiles missing")
    if tomllib is not None:
      parsed = tomllib.loads(codex.read_text(encoding="utf-8"))
      assert_true(parsed["name"] == "reviewer", "Codex profile name missing")
      assert_true("src/**" in parsed["developer_instructions"], "Codex read boundary missing")
      assert_true("Model policy: strong" in parsed["developer_instructions"], "role model policy missing")
    cursor_text = cursor.read_text(encoding="utf-8")
    assert_true(cursor_text.startswith("---\n"), "Cursor profile must begin with frontmatter")
    assert_true("Runtime override (removable): provider=example" in cursor_text, "override missing")
    assert_true("shared-readonly" in antigravity.read_text(encoding="utf-8"), "workspace lowering missing")
    shutil.rmtree(root / ".codex/agents")
    shutil.rmtree(root / ".cursor/agents")
    shutil.rmtree(root / ".antigravity/agents")
    assert_true(
      (root / ".agents/skills/harness/SKILL.md").exists(),
      "removing native profiles must preserve the portable skill",
    )
  print("OK: Runtime profile compilation tests passed.")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
