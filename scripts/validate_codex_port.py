#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    ROOT / "AGENTS.md",
    ROOT / ".agents/skills/harness/SKILL.md",
    ROOT / ".agents/skills/harness/references/agent-design-patterns.md",
    ROOT / ".agents/skills/harness/references/autonomous-experimentation.md",
    ROOT / ".agents/skills/harness/references/orchestrator-template.md",
    ROOT / ".agents/skills/harness/references/team-examples.md",
    ROOT / ".agents/skills/harness/references/skill-writing-guide.md",
    ROOT / ".agents/skills/harness/references/skill-testing-guide.md",
    ROOT / ".agents/skills/harness/references/qa-agent-guide.md",
    ROOT / "docs/compatibility/README.md",
    ROOT / "docs/compatibility/forgecode.md",
    ROOT / "docs/compatibility/droid.md",
    ROOT / "docs/compatibility/openhands.md",
    ROOT / "docs/compatibility/aider.md",
    ROOT / "docs/harness/README.md",
    ROOT / "scripts/install_harness.py",
    ROOT / "scripts/test_install_harness.py",
    ROOT / "scripts/validate_codex_port.py",
]

MAIN_SKILL_HEADINGS = [
    "## when to use",
    "## required inputs",
    "## generated artifacts",
    "## portable defaults",
    "## 6-phase workflow",
    "## architecture selection",
    "## validation expectations",
    "## reference pointers",
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


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(path: Path, text: str, failures: list[str]) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        fail(f"Main skill is missing YAML frontmatter: {path.relative_to(ROOT)}", failures)
        return {}, text

    closing = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            closing = index
            break

    if closing is None:
        fail(f"Main skill frontmatter is not closed: {path.relative_to(ROOT)}", failures)
        return {}, text

    data: dict[str, str] = {}
    for line in lines[1:closing]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            fail(f"Main skill frontmatter contains an invalid line: {line}", failures)
            continue
        key, value = stripped.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")

    return data, "\n".join(lines[closing + 1 :])


def check_required_files(failures: list[str]) -> None:
    for path in REQUIRED_FILES:
        if not path.exists():
            fail(f"Missing required file: {path.relative_to(ROOT)}", failures)


def is_local_link(target: str) -> bool:
    return not (
        target.startswith("#")
        or "://" in target
        or target.startswith("mailto:")
    )


def check_readme_links(failures: list[str]) -> None:
    readme = read_text(ROOT / "README.md")
    for match in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)|\[[^\]]+\]\(([^)]+)\)", readme):
        target = match.group(1) or match.group(2)
        if not target:
            continue
        target = target.strip()
        if not is_local_link(target):
            continue
        path_part = target.split("#", 1)[0]
        if not path_part:
            continue
        if not (ROOT / path_part).exists():
            fail(f"README link target does not exist: {target}", failures)
    if ".claude/" in readme:
        fail("README.md still presents a .claude/ path in repository documentation", failures)
    if ".claude-plugin/" in readme:
        fail("README.md still references removed legacy path: .claude-plugin/", failures)
    if "README_KO.md" in readme:
        fail("README.md still references removed legacy path: README_KO.md", failures)
    if "docs/migration/" in readme:
        fail("README.md still references removed legacy path: docs/migration/", failures)
    if re.search(r"(?<!\.agents/)skills/harness/", readme):
        fail("README.md still references removed legacy path: skills/harness/", failures)


def check_main_skill(failures: list[str]) -> None:
    path = ROOT / ".agents/skills/harness/SKILL.md"
    text = read_text(path)
    frontmatter, body = parse_frontmatter(path, text, failures)
    for required_field in ("name", "description"):
        if not frontmatter.get(required_field):
            fail(f"Main skill frontmatter is missing '{required_field}'", failures)

    lowered = body.casefold()

    for heading in MAIN_SKILL_HEADINGS:
        if heading not in lowered:
            fail(f"Main skill is missing heading: {heading}", failures)

    for phase in range(1, 7):
        if f"phase {phase}:" not in lowered:
            fail(f"Main skill is missing explicit Phase {phase}", failures)

    for ref in re.findall(r"references/[a-z0-9-]+\.md", text):
        if not (path.parent / ref).exists():
            fail(f"Main skill references missing file: {ref}", failures)


def check_pattern_reference(failures: list[str]) -> None:
    path = ROOT / ".agents/skills/harness/references/agent-design-patterns.md"
    text = read_text(path).casefold()

    for pattern in PATTERN_NAMES:
        if pattern not in text:
            fail(f"Pattern reference is missing pattern name: {pattern}", failures)

    required_subsections = [
        "### when it fits",
        "### when it does not fit",
        "### minimum generated artifacts",
        "### recommended portable implementation style",
    ]
    for subsection in required_subsections:
        count = text.count(subsection)
        if count < 6:
            fail(
                f"Pattern reference should contain at least 6 occurrences of '{subsection}' but found {count}",
                failures,
            )


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


def main() -> int:
    failures: list[str] = []
    check_required_files(failures)
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    check_readme_links(failures)
    check_main_skill(failures)
    check_pattern_reference(failures)
    check_autonomous_reference(failures)
    check_for_banned_tokens(failures)

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("OK: Harness repository structure and canonical docs passed validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
