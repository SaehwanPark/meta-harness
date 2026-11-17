#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
  import tomllib
except ModuleNotFoundError:  # Python 3.10 compatibility
  tomllib = None


from validate_skills import validate_skills


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
  ROOT / "AGENTS.md",
  ROOT / ".agents/skills/harness/SKILL.md",
  ROOT / ".agents/skills/harness/references/agents-md-guide.md",
  ROOT / ".agents/skills/harness/references/agent-design-patterns.md",
  ROOT / ".agents/skills/harness/references/autonomous-experimentation.md",
  ROOT / ".agents/skills/harness/references/codex-agent-adapter.md",
  ROOT / ".agents/skills/harness/references/pi-agent-adapter.md",
  ROOT / ".agents/skills/harness/references/antigravity-agent-adapter.md",
  ROOT / ".agents/skills/harness/references/cursor-agent-adapter.md",
  ROOT / ".agents/skills/harness/references/generic-agent-adapter.md",
  ROOT / ".agents/skills/harness/references/runtime-capabilities.md",
  ROOT / ".agents/skills/harness/references/orchestrator-template.md",
  ROOT / ".agents/skills/harness/references/team-examples.md",
  ROOT / ".agents/skills/harness/references/skill-writing-guide.md",
  ROOT / ".agents/skills/harness/references/skill-testing-guide.md",
  ROOT / ".agents/skills/harness/references/qa-agent-guide.md",
  ROOT / ".agents/skills/harness/templates/codex-agent.toml",
  ROOT / "docs/compatibility/README.md",
  ROOT / "docs/compatibility/codex.md",
  ROOT / "docs/compatibility/forgecode.md",
  ROOT / "docs/compatibility/droid.md",
  ROOT / "docs/compatibility/openhands.md",
  ROOT / "docs/compatibility/aider.md",
  ROOT / "docs/harness/README.md",
  ROOT / "docs/harness/starter-research/README.md",
  ROOT / "docs/harness/starter-research/team-spec.md",
  ROOT / "docs/harness/starter-research/roles/research-lead.md",
  ROOT / "scripts/install_harness.py",
  ROOT / "scripts/installer_core.py",
  ROOT / "scripts/installer_tui.py",
  ROOT / "scripts/test_install_harness.py",
  ROOT / "scripts/test_installer_tui.py",
  ROOT / "scripts/test_install_planner.py",
  ROOT / "scripts/test_profile_compilation.py",
  ROOT / "scripts/audit_harness.py",
  ROOT / "scripts/test_audit_harness.py",
  ROOT / "scripts/validate_skills.py",
  ROOT / "scripts/validate_adapters.py",
  ROOT / "scripts/validate_codex_port.py",
]

PATTERN_NAMES = [
  "pipeline",
  "fan-out/fan-in",
  "expert pool",
  "producer-reviewer",
  "supervisor",
  "hierarchical delegation",
]

BANNED_TOKENS = [
  ".claude/agents",
  ".claude/skills",
  "teamcreate",
  "sendmessage",
  "taskcreate",
  'model: "opus"',
  "available_skills",
  "claude -p",
]

DOC_LEGACY_PATTERNS = [
  (".claude/", "still presents a .claude/ path in repository documentation"),
  (".claude-plugin/", "still references removed legacy path: .claude-plugin/"),
  ("README_KO.md", "still references removed legacy path: README_KO.md"),
  ("docs/migration/", "still references removed legacy path: docs/migration/"),
]

INSTALL_VALIDATION_COMMANDS = [
  "python3 scripts/validate_skills.py",
  "python3 scripts/validate_adapters.py",
  "python3 scripts/test_install_harness.py",
  "python3 scripts/test_install_planner.py",
  "python3 scripts/test_installer_tui.py",
  "python3 scripts/test_profile_compilation.py",
  "python3 scripts/test_audit_harness.py",
  "python3 scripts/validate_codex_port.py",
]

AGENTS_MAX_LINES = 24

FIRST_CLASS_RUNTIME_ADAPTERS = (
  "pi",
  "codex",
  "antigravity",
  "cursor",
  "generic",
)
CAPABILITY_STATUSES = (
  "supported",
  "supported_with_extension",
  "advisory",
  "unsupported",
)

REPO_AGENTS_REQUIRED_TOKENS = [
  "keep this file short and repo-wide.",
  "meta harness is a portable repository for designing repo-local agent harnesses.",
  ".agents/skills/harness/",
  "docs/harness/readme.md",
  "python3 scripts/test_install_harness.py",
  "python3 scripts/validate_codex_port.py",
  "rippable",
]

ROOT_DOC_EXPECTATIONS = {
  "README.md": [
    "AGENTS Authoring Guide",
    "agents-md-guide.md",
    "rippable harness",
    "YAML frontmatter",
    "`name` and `description`",
    "meta-harness install",
  ],
  "docs/harness/README.md": [
    "AGENTS Authoring Guide",
    "agents-md-guide.md",
    "rippable",
    "YAML frontmatter",
    "`name` and `description`",
    "meta-harness install",
  ],
  "docs/compatibility/README.md": [
    ".codex/agents/",
  ],
}

COMPATIBILITY_EXPECTATIONS = {
  "forgecode.md": [
    ".agents/skills/harness/",
    "~/.agents/skills/harness/",
    ".forge/skills/harness/",
    "~/forge/skills/harness/",
    "python3 scripts/install_harness.py --scope project --target /path/to/repo --layout forgecode",
    "python3 scripts/install_harness.py --scope user --layout forgecode",
  ],
  "codex.md": [
    ".agents/skills/harness/",
    "~/.agents/skills/harness/",
    ".codex/skills/harness/",
    "~/.codex/skills/harness/",
    "meta-harness install",
    "--scope project --target /path/to/repo",
    "--scope user",
    "YAML frontmatter",
    "`name` and `description`",
    "codex-agent-adapter.md",
    "codex-agent.toml",
  ],
  "droid.md": [
    ".agents/skills/harness/",
    "~/.agents/skills/harness/",
    ".factory/skills/harness/",
    "~/.factory/skills/harness/",
    "python3 scripts/install_harness.py --scope project --target /path/to/repo --layout droid",
    "python3 scripts/install_harness.py --scope user --layout droid",
  ],
  "openhands.md": [
    ".agents/skills/harness/",
    "~/.agents/skills/harness/",
    ".openhands/",
    "python3 scripts/install_harness.py --scope project --target /path/to/repo --layout openhands",
    "python3 scripts/install_harness.py --scope user --layout openhands",
  ],
  "aider.md": [
    ".agents/skills/harness/",
    "~/.agents/skills/harness/",
    ".aider.conf.yml",
    "~/.aider.conf.yml",
    "python3 scripts/install_harness.py --scope project --target /path/to/repo --layout aider",
    "python3 scripts/install_harness.py --scope user --layout aider",
    "AGENTS.md",
    "read:",
  ],
}


def fail(message: str, failures: list[str]) -> None:
  failures.append(message)


def read_text(path: Path) -> str:
  return path.read_text(encoding="utf-8")


def iter_root_docs_markdown() -> list[Path]:
  markdown_paths = set(ROOT.glob("*.md"))
  markdown_paths.update(ROOT.glob("docs/**/*.md"))
  markdown_paths.update(ROOT.glob(".agents/skills/harness/**/*.md"))
  return sorted(markdown_paths)


def check_required_files(failures: list[str]) -> None:
  for path in REQUIRED_FILES:
    if not path.exists():
      fail(f"Missing required file: {path.relative_to(ROOT)}", failures)


def is_local_link(target: str) -> bool:
  return not (target.startswith("#") or "://" in target or target.startswith("mailto:"))


def iter_local_links(text: str) -> list[str]:
  links: list[str] = []
  markdown_pattern = r"!\[[^\]]*\]\(([^)]+)\)|\[[^\]]+\]\(([^)]+)\)"
  html_pattern = r"""(?:href|src)=["']([^"']+)["']"""

  for match in re.finditer(markdown_pattern, text):
    target = match.group(1) or match.group(2)
    if target:
      links.append(target.strip())

  for match in re.finditer(html_pattern, text):
    target = match.group(1)
    if target:
      links.append(target.strip())

  return links


def check_root_docs_markdown(failures: list[str]) -> None:
  for path in iter_root_docs_markdown():
    text = read_text(path)
    for target in iter_local_links(text):
      if not is_local_link(target):
        continue
      path_part = target.split("#", 1)[0]
      if not path_part or path_part.startswith(("{{", "{%")):
        continue
      resolved = (path.parent / path_part).resolve()
      rendered_source = resolved.with_suffix(".md") if path_part.endswith(".html") else resolved
      if not resolved.exists() and not rendered_source.exists():
        fail(
          f"Local link target does not exist in {path.relative_to(ROOT)}: {target}",
          failures,
        )

    for token, message in DOC_LEGACY_PATTERNS:
      if token in text:
        fail(f"{path.relative_to(ROOT)} {message}", failures)
    if re.search(r"(^|[`(\s])skills/harness/", text, re.MULTILINE):
      fail(
        f"{path.relative_to(ROOT)} still references removed legacy path: skills/harness/",
        failures,
      )


def check_pattern_reference(failures: list[str]) -> None:
  path = ROOT / ".agents/skills/harness/references/agent-design-patterns.md"
  text = read_text(path).casefold()

  for pattern in PATTERN_NAMES:
    if pattern not in text:
      fail(f"Pattern reference is missing pattern name: {pattern}", failures)


def check_autonomous_reference(failures: list[str]) -> None:
  path = ROOT / ".agents/skills/harness/references/autonomous-experimentation.md"
  text = read_text(path).casefold()
  required_tokens = [
    "mutable surface",
    "immutable evaluation surface",
    "baseline",
    "results.tsv",
    "keep",
    "discard",
    "user-controlled compute",
  ]
  for token in required_tokens:
    if token not in text:
      fail(f"Autonomous experimentation reference is missing: {token}", failures)


def check_runtime_contract(failures: list[str]) -> None:
  capabilities_path = ROOT / ".agents/skills/harness/references/runtime-capabilities.md"
  capabilities = read_text(capabilities_path).casefold()
  for status in CAPABILITY_STATUSES:
    if not re.search(rf"\b{re.escape(status)}\b", capabilities):
      fail(f"Runtime capability reference is missing status vocabulary: {status}", failures)
  for runtime in FIRST_CLASS_RUNTIME_ADAPTERS:
    path = ROOT / f".agents/skills/harness/references/{runtime}-agent-adapter.md"
    text = read_text(path).casefold()
    for term in ("skill", "role", "write", "communication", "model", "fallback"):
      if term not in text:
        fail(f"{path.relative_to(ROOT)} is missing runtime guidance: {term}", failures)
    if not any(re.search(rf"\b{re.escape(status)}\b", text) for status in CAPABILITY_STATUSES):
      fail(f"{path.relative_to(ROOT)} does not classify capability status", failures)

  matrix_path = ROOT / "docs/compatibility/README.md"
  matrix = read_text(matrix_path).casefold()
  for runtime in ("pi", "codex", "antigravity", "cursor cli / agent"):
    if runtime not in matrix:
      fail(f"Compatibility matrix is missing active runtime: {runtime}", failures)
  if "first-class" not in matrix:
    fail("Compatibility matrix is missing the first-class support claim", failures)
  if "generic" not in matrix or "best effort" not in matrix:
    fail("Compatibility matrix is missing the generic best-effort boundary", failures)
  for legacy in ("forgecode", "droid", "openhands", "aider"):
    path = ROOT / f"docs/compatibility/{legacy}.md"
    legacy_text = read_text(path).casefold()
    if legacy not in matrix or "unverified" not in legacy_text or "deprecated" not in legacy_text:
      fail(f"Compatibility docs are missing legacy boundary: {legacy}", failures)


def check_codex_agent_template(failures: list[str]) -> None:
  path = ROOT / ".agents/skills/harness/templates/codex-agent.toml"
  text = read_text(path)
  if tomllib is not None:
    try:
      data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as error:
      fail(f"Codex agent template is invalid TOML: {error}", failures)
      return
  else:
    data = {}
    for key in ("name", "description"):
      match = re.search(rf'^\s*{key}\s*=\s*"([^"]+)"\s*$', text, re.MULTILINE)
      if match:
        data[key] = match.group(1)
    instructions = re.search(
      r'^\s*developer_instructions\s*=\s*"""(.+?)"""\s*$',
      text,
      re.MULTILINE | re.DOTALL,
    )
    if instructions:
      data["developer_instructions"] = instructions.group(1)

  for key in ("name", "description", "developer_instructions"):
    if not isinstance(data.get(key), str) or not data[key].strip():
      fail(f"Codex agent template requires a non-empty string: {key}", failures)

  for key in ("model", "model_reasoning_effort"):
    if key in data or re.search(rf"^\s*{key}\s*=", text, re.MULTILINE):
      fail(f"Codex agent template must inherit optional setting: {key}", failures)


def check_for_banned_tokens(failures: list[str]) -> None:
  root = ROOT / ".agents/skills/harness"
  for path in sorted(root.rglob("*")):
    if not path.is_file():
      continue
    text = read_text(path).casefold()
    for token in BANNED_TOKENS:
      if token in text:
        fail(
          f"Found legacy runtime token '{token}' in {path.relative_to(ROOT)}",
          failures,
        )


def check_repo_agents(failures: list[str]) -> None:
  path = ROOT / "AGENTS.md"
  text = read_text(path)
  lowered = text.casefold()
  if len(text.splitlines()) > AGENTS_MAX_LINES:
    fail(
      f"AGENTS.md should stay concise ({AGENTS_MAX_LINES} lines max) but has {len(text.splitlines())}",
      failures,
    )

  for token in REPO_AGENTS_REQUIRED_TOKENS:
    if token not in lowered:
      fail(f"AGENTS.md is missing required repo guidance: {token}", failures)


def check_root_doc_expectations(failures: list[str]) -> None:
  for relative_path, required_tokens in ROOT_DOC_EXPECTATIONS.items():
    text = read_text(ROOT / relative_path)
    for token in required_tokens:
      if token not in text:
        fail(f"{relative_path} is missing required synchronized guidance: {token}", failures)


def check_installation_doc(failures: list[str]) -> None:
  installer_text = read_text(ROOT / "scripts/install_harness.py")
  core_path = ROOT / "scripts/installer_core.py"
  if core_path.exists():
    installer_text += "\n" + read_text(core_path)
  installation_text = read_text(ROOT / "docs/installation.md")

  layout_match = re.search(r'(?:LAYOUTS|LEGACY_LAYOUTS) = \(([^)]+)\)', installer_text)
  if layout_match is None:
    fail("Could not parse installer layouts from scripts/install_harness.py", failures)
    return

  layouts = re.findall(r'"([^"]+)"', layout_match.group(1))
  for layout in layouts:
    bullet = rf"-\s+{re.escape(layout)}\s*:"
    table = rf"\|[^\n]*{re.escape(layout)}[^\n]*\|"
    if not re.search(rf"(?:{bullet}|{table})", installation_text):
      fail(f"docs/installation.md is missing layout guidance for '{layout}'", failures)

  for command in INSTALL_VALIDATION_COMMANDS:
    if command not in installation_text:
      fail(
        f"docs/installation.md is missing validation command: {command}",
        failures,
      )

  for command in ("meta-harness install", "python scripts/install_harness.py install"):
    if command not in installation_text:
      fail(
        f"docs/installation.md is missing preferred/source install command: {command}",
        failures,
      )

  if "--mode symlink" not in installation_text:
    fail("docs/installation.md is missing --mode symlink guidance", failures)

  for token in (
    "does not create or update the target repo's `AGENTS.md`",
    "agents-md-guide.md",
    "AGENTS.md stays repo-owned",
  ):
    if token not in installation_text and token not in installer_text:
      fail(f"Installer contract is missing updated AGENTS guidance: {token}", failures)


def check_compatibility_docs(failures: list[str]) -> None:
  compatibility_root = ROOT / "docs/compatibility"
  for filename, required_tokens in COMPATIBILITY_EXPECTATIONS.items():
    path = compatibility_root / filename
    text = read_text(path)
    for token in required_tokens:
      if token not in text:
        fail(
          f"{path.relative_to(ROOT)} is missing required compatibility guidance: {token}",
          failures,
        )


def main() -> int:
  failures: list[str] = []
  check_required_files(failures)
  if failures:
    for failure in failures:
      print(f"FAIL: {failure}")
    return 1

  failures.extend(validate_skills(ROOT).errors)
  check_root_docs_markdown(failures)
  check_repo_agents(failures)
  check_root_doc_expectations(failures)
  check_pattern_reference(failures)
  check_autonomous_reference(failures)
  check_runtime_contract(failures)
  check_codex_agent_template(failures)
  check_for_banned_tokens(failures)
  check_installation_doc(failures)
  check_compatibility_docs(failures)

  if failures:
    for failure in failures:
      print(f"FAIL: {failure}")
    return 1

  print("OK: Harness repository structure and canonical docs passed validation.")
  return 0


if __name__ == "__main__":
  sys.exit(main())
