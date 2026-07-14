# Changelog

All notable changes to Humanizer Extended are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.20.0] - 2026-07-14

### Added

- Three current-upstream patterns: manufactured punchlines and staccato drama, mid-text aphorism formulas, and conversational rhetorical openers.
- Progressive-disclosure references for Russian rules, research notes, and full examples.
- Russian-aware structural metrics, a six-genre Russian evaluation corpus, aggregate baselines, and pytest coverage.
- Installation through the cross-agent skills CLI and the Claude Code plugin marketplace.
- GitHub Actions checks for pytest, aggregate-metric regressions, and release-version synchronization.

### Changed

- Split metric reporting into structural-quality and skill-compliance blocks, with language-specific targets.
- Made evidence boosters genre-gated instead of universally mandatory.
- Clarified that an explicit voice sample may override house-style rules when the user asks for faithful voice matching.
- Relaxed the hyphenated-word rule to target repeated, conspicuous clusters rather than normal compounds.
- Reduced the core `SKILL.md` payload by moving conditional detail to `references/`.

### Fixed

- Reworked the full example so the rewrite preserves facts and does not invent sources.
- Added a safe default when `AskUserQuestion` is unavailable.
- Added secondhand-text false-positive protection and offer-to-continue closer coverage from upstream.
- Fixed corpus path resolution, sentence splitting around common abbreviations, and the false positive for the month "May".
- Ignored Python caches and local Claude settings, and enforced LF line endings.

[Unreleased]: https://github.com/Dex719/humanizer-extended/compare/v2.20.0...HEAD
[2.20.0]: https://github.com/Dex719/humanizer-extended/compare/v2.19.0...v2.20.0
