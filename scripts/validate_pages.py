#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

REQUIRED_FILES = (
  DOCS / "_config.yml",
  DOCS / "_layouts" / "default.html",
  DOCS / "assets" / "css" / "style.css",
  DOCS / "index.md",
  ROOT / ".github" / "workflows" / "pages.yml",
  ROOT / ".github" / "workflows" / "validate.yml",
)

REQUIRED_LAYOUT_PATHS = (
  "/installation.html",
  "/guides/workflow.html",
  "/guides/patterns.html",
  "/sample-prompts.html",
  "/compatibility/README.html",
  "/compatibility/codex.html",
  "/harness/README.html",
  "/harness/starter-research/README.html",
)


def page_has_frontmatter(path: Path) -> bool:
  lines = path.read_text(encoding="utf-8").splitlines()
  if not lines or lines[0].strip() != "---":
    return False
  try:
    end = lines.index("---", 1)
  except ValueError:
    return False
  frontmatter = "\n".join(lines[1:end])
  return bool(
    re.search(r"(?m)^title:\s*\S", frontmatter)
    and re.search(r"(?m)^description:\s*\S", frontmatter)
    and re.search(r"(?m)^layout:\s*default\s*$", frontmatter)
  )


def without_fenced_code(text: str) -> str:
  return re.sub(
    r"(?ms)^(?:\x60\x60\x60|~~~).*?^(?:\x60\x60\x60|~~~)\s*$",
    "",
    text,
  )


def local_link_targets(path: Path) -> list[str]:
  text = without_fenced_code(path.read_text(encoding="utf-8"))
  markdown_targets = re.findall(r"\]\(([^)\s]+)", text)
  html_targets = re.findall(r"""href=["']([^"']+)["']""", text)
  return markdown_targets + html_targets


def resolve_source_path(page: Path, target: str) -> Path | None:
  clean_target = target.split("#", 1)[0].strip()
  if not clean_target:
    return None
  if clean_target.startswith(
    ("http://", "https://", "mailto:", "javascript:", "{{", "{%")
  ):
    return None
  candidate = (page.parent / clean_target).resolve()
  if clean_target.endswith(".html"):
    candidate = candidate.with_suffix(".md")
  return candidate


def validate() -> list[str]:
  errors: list[str] = []
  for path in REQUIRED_FILES:
    if not path.exists():
      errors.append(f"missing required Pages file: {path.relative_to(ROOT)}")
  if errors:
    return errors

  config = (DOCS / "_config.yml").read_text(encoding="utf-8")
  if 'baseurl: "/meta-harness"' not in config:
    errors.append("docs/_config.yml must set baseurl to /meta-harness")
  if 'url: "https://saehwanpark.github.io"' not in config:
    errors.append("docs/_config.yml must set the project Pages host")

  workflow = (ROOT / ".github" / "workflows" / "pages.yml").read_text(
    encoding="utf-8"
  )
  for token in (
    "actions/configure-pages@v5",
    "actions/jekyll-build-pages@v1",
    "source: ./docs",
    "actions/upload-pages-artifact@v3",
    "actions/deploy-pages@v4",
  ):
    if token not in workflow:
      errors.append(f"Pages workflow is missing: {token}")

  for page in sorted(DOCS.rglob("*.md")):
    if not page_has_frontmatter(page):
      errors.append(
        f"Markdown page needs title, description, and default layout frontmatter: "
        f"{page.relative_to(ROOT)}"
      )
    for target in local_link_targets(page):
      source_path = resolve_source_path(page, target)
      if source_path is None:
        continue
      clean_target = target.split("#", 1)[0].strip()
      if clean_target.endswith(".md") and source_path.is_relative_to(DOCS):
        errors.append(
          f"public page links to Markdown source instead of rendered HTML: "
          f"{page.relative_to(ROOT)} -> {target}"
        )
      elif clean_target.endswith(".html") and not source_path.exists():
        errors.append(
          f"rendered page link has no Markdown source: "
          f"{page.relative_to(ROOT)} -> {target}"
        )
      elif clean_target.endswith(".md") and not source_path.exists():
        errors.append(
          f"local Markdown link has no source: {page.relative_to(ROOT)} -> {target}"
        )

  layout = (DOCS / "_layouts" / "default.html").read_text(encoding="utf-8")
  for target in REQUIRED_LAYOUT_PATHS:
    if target not in layout:
      errors.append(f"layout navigation is missing: {target}")

  validate_workflow = (ROOT / ".github" / "workflows" / "validate.yml").read_text(
    encoding="utf-8"
  )
  if "python3 scripts/validate_pages.py" not in validate_workflow:
    errors.append("repository validation workflow must run scripts/validate_pages.py")

  return errors


def main() -> int:
  errors = validate()
  if errors:
    for error in errors:
      print(f"ERROR: {error}", file=sys.stderr)
    return 1
  print("OK: GitHub Pages source validation passed.")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
