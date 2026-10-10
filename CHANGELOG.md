# Changelog

All notable changes to Humanizer Extended are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.23.0] - 2026-10-11

### Added

- A blind full-vs-slim comparison on 16 texts in `eval/results/2026-10-11-full-vs-slim/`, with inputs, outputs, the A/B key, judge notes, and a scoring script. Slim was preferred 10 times, the full skill 3 times, with 3 ties.
- Six English corpus pairs with a `provenance` field: Claude Haiku 5.5 inputs from recorded fact-list prompts, and skill outputs that a blind review found to add and lose nothing.
- Tests for modal synonyms, rhetorical frames, kept contrasts, Russian name cases, and the informational booster check.

### Changed

- Pattern 9 in both skills keeps a contrast when the reader would naturally assume the negative half (weekly releases suggest speed), written short and inside one sentence: "for predictability, not speed".
- Both skills forbid adding a causal link (`so`, `because`, `поэтому`, `так что`) between facts the input only places side by side.
- Slim's sales-language list now includes `for those who value…`, `для тех, кто ценит…`, and `идеальное решение для`.
- The fact-lock audit compares modality by class (`следует` and `стоит` match; `may` and nothing does not), ignores negations and modals inside staged contrasts and rhetorical frames when checking for losses, still allows a contrast kept in plain words, treats `wasn't` and `was not` as the same negation, and matches Russian names across cases.
- The booster check is informational. It still counts confidence markers but no longer fails a rewrite that adds none.
- The README before/after images use slim's outputs after these fixes.

### Fixed

- Replaced the 2.21 reference rewrite for `ru-landing-meals`, which commented on its source in almost every sentence and used an `а не` contrast, with landing copy that keeps every fact.

## [2.22.0] - 2026-10-10

### Added

- `humanizer-slim`, a one-file companion skill (~1,650 words) in `skills/humanizer-slim/` for strong current models. It keeps the hard limits and the Russian rules, orders tells by strength, and returns only the final text by default. The plugin manifest now lists both skills.
- An account of why AI text sounds the way it does and three strength tiers: act on one sighting, act on a cluster, weak alone.
- Pattern #74 (re-explaining what the reader knows) and #75 (arguing with no one), with English and Russian forms, from upstream humanizer 3.1.
- A `9-RU` section in `references/patterns-ru.md` for `не просто X, а Y`, `Это не про X. Это про Y.`, `Дело не в X`, and related frames, plus vague Russian attributions (`эксперты считают`).
- Russian corporate calques (`культура команды`, `смена культуры`, `адресовать проблему`, `это имеет смысл`, `экспертиза`, `вызов`) in both skills. A calque copied from the source into the rewrite counts as a miss.
- A `contrast_frames` compliance metric that counts staged not-X-but-Y forms in English and Russian.
- File and embedded output modes.
- A v2.22 evidence register (R16–R23): current English and Russian Wikipedia guidance, reporting on negative parallelism, certainty distortion in LM rewriting, voice normalization, non-native false positives, and AI-edited text.
- Before/after images for English and Russian in the README, generated with `humanizer-slim`, and the same pairs as corpus entries.

### Changed

- Promoted not-X-but-Y (#9) from LEGACY to the strongest tell: act on one sighting, including split, reversed (`Y rather than X`), clipped, and Russian forms. Swapping in another contrast formula no longer counts as a fix.
- Folded upstream 3.1 additions into existing numbers: "That distinction matters.", echo closers, and example restatement into #49 and #34; self-answered questions and stock openers into #28; headings written for effect into #17; method narration and layout description into #39, now "Writing about the document instead of its subject".
- Kept #14 (dashes) as LEGACY and noted that Wikipedia moved em-dash overuse to historical indicators in October 2026. A rewrite should no longer turn every dash into a comma.
- Strengthened #56 hedge stripping and added a voice-drift audit item based on LM-rewriting research.
- Moved the skill version to `metadata.version`, as the Agent Skills spec expects, and taught the version check to read both skills.

### Deprecated

- Retired #11 (elegant variation) and #12 (false ranges) as standalone signals. Wikipedia lists the first as historical and no longer lists the second. The numbers stay reserved.

### Fixed

- `patterns-ru.md` no longer recommends replacing `Это не про X, это про Y` with `дело не столько в X, сколько в Y`, which kept the same tell.

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

[Unreleased]: https://github.com/Dex719/humanizer-extended/compare/v2.23.0...HEAD
[2.23.0]: https://github.com/Dex719/humanizer-extended/compare/v2.22.0...v2.23.0
[2.22.0]: https://github.com/Dex719/humanizer-extended/compare/v2.21.0...v2.22.0
[2.21.0]: https://github.com/Dex719/humanizer-extended/compare/v2.20.0...v2.21.0
[2.20.0]: https://github.com/Dex719/humanizer-extended/compare/v2.19.0...v2.20.0
