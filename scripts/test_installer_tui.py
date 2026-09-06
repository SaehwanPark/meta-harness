#!/usr/bin/env python3

from __future__ import annotations

import io
import tempfile
from pathlib import Path

from installer_tui import TuiState, render_main_screen, run_tui


class TtyBuffer(io.StringIO):
  def isatty(self) -> bool:
    return True


def assert_true(condition: bool, message: str) -> None:
  if not condition:
    raise AssertionError(message)


def main() -> int:
  state = TuiState(scope="project", target=".", agents=("cursor", "pi"))
  request = state.to_request()
  assert_true(request.agents == ("pi", "cursor"), "TUI request should use core normalization")
  assert_true("[x] pi" in render_main_screen(state), "TUI should render checked runtime")
  assert_true("[ ] generic" in render_main_screen(state), "TUI should render unchecked runtime")
  assert_true(state.toggle_agent("generic").agents == ("pi", "cursor", "generic"), "toggle should be deterministic")

  with tempfile.TemporaryDirectory(prefix="meta-harness-tui-") as tmp:
    target = Path(tmp) / "project"
    target.mkdir()
    input_stream = TtyBuffer(
      "project\n"
      f"{target}\n"
      "1,4\n"
      "auto\n"
      "y\n"
      "inherit\n"
      "copy\n"
      "d\n"
    )
    output_stream = TtyBuffer()
    status = run_tui(input_stream=input_stream, output_stream=output_stream)
    assert_true(status == 0, "TUI dry-run should succeed")
    assert_true("Installation plan preview" in output_stream.getvalue(), "TUI should preview before action")
    assert_true("Dry run only; no changes made." in output_stream.getvalue(), "TUI dry-run confirmation missing")
    assert_true(not (target / ".agents").exists(), "TUI dry-run must not mutate target")

  print("OK: Installer TUI state and smoke tests passed.")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
