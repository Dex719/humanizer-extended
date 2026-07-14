# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## What this repo is
This repository is a portable agent skill with a small Python evaluation harness.

The runtime entry point is `SKILL.md`: compatible agents read its YAML frontmatter and the prompt/instructions that follow. Conditional detail lives under `references/` and is part of the installed skill.

`README.md` is for humans: installation, usage, and a compact overview of the patterns.

## Key files (and how they relate)
- `SKILL.md`
  - The actual skill definition.
  - Starts with YAML frontmatter (`---` … `---`) containing `name`, `version`, `description`, and `allowed-tools`.
  - After the frontmatter is the editor prompt: the canonical, detailed pattern list with examples.
- `README.md`
  - Installation and usage instructions.
  - Contains a summarized pattern table and a short version history.
- `references/`
  - Detailed rules, examples, and research that `SKILL.md` loads only when needed.
- `eval/`
  - Structural and compliance metrics, the bilingual before/after corpus, tests, and the committed aggregate baseline.
- `.claude-plugin/`
  - Claude Code plugin and marketplace manifests.
- `scripts/check_version_sync.py`
  - Keeps release versions synchronized across the skill, README, changelog, and plugin manifest.

When changing behavior/content, treat `SKILL.md` as the source of truth, and update `README.md` to stay consistent.

## Common commands
### Install with the cross-agent skills CLI
```bash
npx skills add Dex719/humanizer-extended
npx skills update humanizer-extended
```

### Run repository checks
```bash
python -m pytest -q
python eval/metrics.py aggregate --corpus eval/corpus --check-baseline eval/baseline.json --json
python scripts/check_version_sync.py
```

## How to “run” it (Claude Code)
Invoke the skill:
- `/humanizer-extended` then paste text

## Making changes safely
### Versioning (keep in sync)
- `SKILL.md` has a `version:` field in its YAML frontmatter.
- `README.md` has a “Version History” section.
- `CHANGELOG.md` has the latest released version.
- `.claude-plugin/plugin.json` has the plugin version.

If you bump the version, update all four. CI enforces this with `scripts/check_version_sync.py`.

### Editing `SKILL.md`
- Preserve valid YAML frontmatter formatting and indentation.
- Keep the pattern numbering stable unless you’re intentionally re-numbering (since the README table and examples reference the same numbering).

### Documenting non-obvious fixes
If you change the prompt to handle a tricky failure mode (e.g., a repeated mis-edit or an unexpected tone shift), add a short note to `README.md`’s version history describing what was fixed and why.
