#!/usr/bin/env python3
"""Fail when release versions in user-facing metadata drift apart."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEMVER = r"[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?"


def require_match(path: Path, pattern: str, label: str, *, flags: int = 0) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(pattern, text, flags)
    if match is None:
        raise ValueError(f"could not find {label} in {path.relative_to(ROOT)}")
    return match.group("version")


def skill_version(relative: str = "SKILL.md") -> str:
    """Read ``metadata.version`` from a skill's YAML frontmatter.

    The Agent Skills spec has no top-level ``version`` field, so the version
    lives under ``metadata`` and a top-level one is rejected.
    """

    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{relative} must begin with YAML frontmatter")
    try:
        frontmatter = text.split("---\n", 2)[1]
    except IndexError as exc:
        raise ValueError(f"{relative} has unterminated YAML frontmatter") from exc
    if re.search(r"^version:", frontmatter, re.MULTILINE):
        raise ValueError(f"{relative}: move the top-level version under metadata.version")
    match = re.search(
        rf"^metadata:\s*\n(?:[ \t]+.*\n)*?[ \t]+version:\s*[\"']?(?P<version>{SEMVER})[\"']?\s*$",
        frontmatter,
        re.MULTILINE,
    )
    if match is None:
        raise ValueError(f"could not find metadata.version in {relative} frontmatter")
    return match.group("version")


def readme_version() -> str:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    section = re.search(
        r"^## Version History\s*$\n(?P<body>.*?)(?=^##\s|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if section is None:
        raise ValueError("could not find the Version History section in README.md")
    match = re.search(
        rf"^-\s+\*\*(?P<version>{SEMVER})\*\*\s+-",
        section.group("body"),
        re.MULTILINE,
    )
    if match is None:
        raise ValueError("could not find the latest README.md Version History entry")
    return match.group("version")


def changelog_version() -> str:
    return require_match(
        ROOT / "CHANGELOG.md",
        rf"^##\s+\[(?P<version>{SEMVER})\](?:\s+-\s+\d{{4}}-\d{{2}}-\d{{2}})?\s*$",
        "latest released changelog version",
        flags=re.MULTILINE,
    )


def plugin_version() -> str:
    path = ROOT / ".claude-plugin" / "plugin.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc
    version = data.get("version")
    if not isinstance(version, str) or re.fullmatch(SEMVER, version) is None:
        raise ValueError(".claude-plugin/plugin.json must contain a semantic version")
    return version


def marketplace_version() -> str:
    path = ROOT / ".claude-plugin" / "marketplace.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc
    version = data.get("version")
    if not isinstance(version, str) or re.fullmatch(SEMVER, version) is None:
        raise ValueError(".claude-plugin/marketplace.json must contain a semantic version")
    return version


def main() -> int:
    readers = {
        "SKILL.md frontmatter": skill_version,
        "skills/humanizer-slim/SKILL.md frontmatter": lambda: skill_version(
            "skills/humanizer-slim/SKILL.md"
        ),
        "README.md Version History": readme_version,
        "CHANGELOG.md latest release": changelog_version,
        ".claude-plugin/plugin.json": plugin_version,
        ".claude-plugin/marketplace.json": marketplace_version,
    }
    versions: dict[str, str] = {}
    try:
        for label, reader in readers.items():
            versions[label] = reader()
    except (OSError, ValueError) as exc:
        print(f"version-sync: {exc}", file=sys.stderr)
        return 1

    width = max(len(label) for label in versions)
    for label, version in versions.items():
        print(f"{label:<{width}}  {version}")

    unique = set(versions.values())
    if len(unique) != 1:
        print("version-sync: release versions do not match", file=sys.stderr)
        return 1

    print(f"version-sync: OK ({unique.pop()})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
