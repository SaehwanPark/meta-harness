#!/usr/bin/env python3

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from audit_harness import audit_target, render_report


def assert_true(condition: bool, message: str) -> None:
  if not condition:
    raise AssertionError(message)


def main() -> int:
  with tempfile.TemporaryDirectory(prefix="meta-harness-audit-") as tmp:
    root = Path(tmp)
    (root / ".agents" / "skills" / "harness").mkdir(parents=True)
    (root / ".agents" / "skills" / "harness" / "SKILL.md").write_text(
      "---\nname: harness\ndescription: test\n---\n", encoding="utf-8"
    )
    (root / ".cursor" / "agents").mkdir(parents=True)
    (root / ".cursor" / "agents" / "reviewer.md").write_text("role", encoding="utf-8")
    (root / ".forge" / "skills" / "harness").mkdir(parents=True)
    report = audit_target(root)
    assert_true(".agents/skills/harness" in report.existing_skills, "skill inventory missing")
    assert_true(any(item.name == "cursor" for item in report.detected_runtimes), "runtime missing")
    assert_true(".forge" in report.stale_artifacts, "legacy artifact missing")
    assert_true(report.operation_classification == "drift repair", "classification missing")
    assert_true("selected_action" not in render_report(report), "audit unexpectedly mutated")
    parsed = json.loads(render_report(report, "json"))
    assert_true(parsed["existing_roles"] == [], "unexpected role inventory")
  print("OK: Harness audit smoke tests passed.")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
