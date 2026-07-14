# Changelog

All notable changes to Humanizer Extended are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.21.0] - 2026-07-14

### Added

- Twenty-two patterns (#52–73) covering humanizer damage, 2025+ sourcing and rhetoric, genre-gated English grammar fingerprints, and additional Russian grammar and framing problems.
- Neurodivergent, translation, genre, short-text, convergence, post-paraphrase, and no-model-attribution guards, plus explicit anti-humanization prohibitions.
- Specific-author voice anchoring using at least three authentic samples and a residue-first, fact-lock-first seven-step process.
- Standard-library diagnostics for immutable-token integrity, human-marker floors, punctuation entropy, windowed type-token ratio, content/function ratio, digit density, participial stacks, `That`-clause subjects, and dangling Russian adverbial participles.
- A verified v2.21 evidence register, evaluation methodology notes, length-mismatch warnings, and one English plus one Russian corpus pair.

### Changed

- Demoted negative parallelism (#9) and em/en-dash frequency (#14) to LEGACY corroboration-only signals; absence is no longer evidence of human authorship, and English dash counts no longer receive a pass/fail metric target.
- Made vocabulary rule #7 era-stratified and expanded Russian rule #44 with action nominalizations, long genitive chains, weak `является`, avoidable passive, and genre-specific thresholds.
- Integrated all v2.21 diagnostics into profile, compare, and aggregate output while preserving additive schema version 1 compatibility.
- Capped the aggregate structural regression target at the v2.20 rate of `0.50` so heuristic optimization does not become a writing objective.

### Fixed

- Reworked new teaching and corpus pairs so they preserve names, numbers, modality, person, and source coverage instead of inventing specifics.
- Replaced the non-canonical CoAT identifier with the publisher's canonical DOI and removed unsupported detector and contraction claims from the evidence notes.

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

[Unreleased]: https://github.com/Dex719/humanizer-extended/compare/v2.21.0...HEAD
[2.21.0]: https://github.com/Dex719/humanizer-extended/compare/v2.20.0...v2.21.0
[2.20.0]: https://github.com/Dex719/humanizer-extended/compare/v2.19.0...v2.20.0
