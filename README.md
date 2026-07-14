# Humanizer Extended

A portable agent skill that removes signs of AI-generated writing from English and Russian text, making it sound more natural while preserving the original facts and meaning.

> **Fork.** `humanizer-extended` is a fork of [blader/humanizer](https://github.com/blader/humanizer) (original by Siqi Chen, MIT). It diverged after upstream 2.5.1 and adds patterns #30–38 (model-tool markup, hallucinated citations, placeholder leakage, document-internal style shift, aphoristic closer, prestige-metaphor frames, false balance, generic stock examples, nominalization) plus a FACT PRESERVATION section. Version 2.20.0 synchronizes upstream 2.8.x patterns as #49–51 and moves conditional detail into `references/`. Version 2.21.0 adds anti-humanization damage, current-era, grammar, and Russian patterns #52–73; it also demotes the old hard em-dash and negative-parallelism signals to LEGACY. Pattern numbers in this fork do **not** match upstream's.

## Installation

### Skills CLI

Install with the cross-agent [skills CLI](https://skills.sh/docs/cli):

```bash
npx skills add Dex719/humanizer-extended
```

Update an existing install:

```bash
npx skills update humanizer-extended
```

To install into every supported agent harness:

```bash
npx skills add Dex719/humanizer-extended --agent '*'
```

To target one configured harness, pass its agent name:

```bash
npx skills add Dex719/humanizer-extended --agent <agent-name>
```

### Claude Code plugin marketplace

Claude Code users can also install Humanizer Extended as a plugin:

```text
/plugin marketplace add Dex719/humanizer-extended
/plugin install humanizer-extended@humanizer-extended
```

The plugin exposes the skill as `/humanizer-extended:humanizer-extended`.

### Manual installation

Clone the repository into the skills directory used by your harness. For Claude Code:

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/Dex719/humanizer-extended.git ~/.claude/skills/humanizer-extended
```

For OpenCode:

```bash
mkdir -p ~/.config/opencode/skills
git clone https://github.com/Dex719/humanizer-extended.git ~/.config/opencode/skills/humanizer-extended
```

If the repository is already cloned, copy the complete skill directory rather than only `SKILL.md`; current releases load supporting files under `references/` on demand. The `eval/` directory is for development and is not needed at runtime.

> **Note:** OpenCode also scans `~/.claude/skills/` for compatibility, so a single clone into `~/.claude/skills/humanizer-extended/` works for both tools.

## Usage

### Claude Code

```
/humanizer-extended

[paste your text here]
```

### OpenCode

```
/humanizer-extended

[paste your text here]
```

Or ask the model to humanize text directly in either tool:

```
Please humanize this text: [your text]
```

### Voice Calibration

As of 2.17.0 the skill offers this automatically at the start of a run (it asks whether you want to provide a sample). If the current harness does not support `AskUserQuestion`, the skill continues with its default voice without stopping or reporting an error. You can also provide a sample up front to match your personal writing style:

```
/humanizer-extended

Here's a sample of my writing for voice matching:
[paste 2-3 paragraphs of your own writing]

Now humanize this text:
[paste AI text to humanize]
```

The skill will analyze your sentence rhythm, word choices, and quirks, then apply them to the rewrite instead of producing generic "clean" output.

## Overview

Based on [Wikipedia's "Signs of AI writing"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) guide, maintained by WikiProject AI Cleanup. This comprehensive guide comes from observations of thousands of instances of AI-generated text.

The skill also includes a final "obviously AI generated" audit pass and a second rewrite, to catch lingering AI-isms in the first draft.

### Key Insight from Wikipedia

> "LLMs use statistical algorithms to guess what should come next. The result tends toward the most statistically likely result that applies to the widest variety of cases."

## 51 Patterns Detected (with Before/After Examples)

### Content Patterns

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 1 | **Significance inflation** | "marking a pivotal moment in the evolution of..." | "was established in 1989 to collect regional statistics" |
| 2 | **Notability name-dropping** | "cited in NYT, BBC, FT, and The Hindu" | "In a 2024 NYT interview, she argued..." |
| 3 | **Superficial -ing analyses** | "symbolizing... reflecting... showcasing..." | Remove or expand with actual sources |
| 4 | **Promotional language** | "nestled within the breathtaking region" | "is a town in the Gonder region" |
| 5 | **Vague attributions** | "Experts believe it plays a crucial role" | "according to a 2019 survey by..." |
| 6 | **Formulaic challenges** | "Despite challenges... continues to thrive" | Specific facts about actual challenges |

### Language Patterns

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 7 | **AI vocabulary** | "Actually... additionally... testament... landscape... showcasing" | "also... remain common" |
| 8 | **Copula avoidance** | "serves as... features... boasts" | "is... has" |
| 9 | **Negative parallelisms / tailing negations (LEGACY)** | Repeated "not just X, but Y" and clipped negation tails | Reduce mechanical clusters; absence is not evidence of human authorship |
| 10 | **Rule of three** | "innovation, inspiration, and insights" | Use natural number of items |
| 11 | **Synonym cycling** | "protagonist... main character... central figure... hero" | "protagonist" (repeat when clearest) |
| 12 | **False ranges** | "from the Big Bang to dark matter" | List topics directly |
| 13 | **Passive voice / subjectless fragments** | "No configuration file needed" | Name the actor when it helps clarity |
| 38 | **Nominalization overuse** | "the implementation of indexing resulted in optimization of queries" | Turn the abstract noun back into a verb: "indexing made queries faster" |

### Style Patterns

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 14 | **Em/en dashes (LEGACY)** | Mechanical dash clusters in English with no matching voice habit | Recast only the mechanical uses; frequency is corroboration, not a pass/fail signal |
| 15 | **Boldface overuse** | "**OKRs**, **KPIs**, **BMC**" | "OKRs, KPIs, BMC" |
| 16 | **Inline-header lists** | "**Performance:** Performance improved" | Convert to prose |
| 17 | **Title Case Headings** | "Strategic Negotiations And Partnerships" | "Strategic negotiations and partnerships" |
| 18 | **Emojis** | "🚀 Launch Phase: 💡 Key Insight:" | Remove emojis |
| 19 | **Curly quotes** | `said “the project”` | `said "the project"` |
| 26 | **Hyphenated word-pair clusters** | "cross-functional, data-driven, client-facing" repeated throughout | Keep required compounds; vary only conspicuous clusters of optional forms |
| 27 | **Persuasive authority tropes** | "At its core, what matters is..." | State the point directly |
| 28 | **Signposting announcements** | "Let's dive in", "Here's what you need to know" | Start with the content |
| 29 | **Fragmented headers** | "## Performance" + "Speed matters." | Let the heading do the work |
| 33 | **Document-internal style shift** | Formal academic paragraph followed by "pretty nuts honestly" paragraph | Pick one register and enforce it; ask if the input mixes two |
| 34 | **Aphoristic closer** | "And in the end — that's what great software has always been about: not the code, but the craft." | Cut the epigram or end on a specific fact |
| 35 | **Prestige-metaphor nouns as frames** | "the tapestry of modern software, a symphony of productivity, an orchestra of creation" | Delete mixed metaphors; keep at most one earned one |
| 39 | **Diff-anchored writing** | "This function was added to replace the previous approach..." | Describe what it does, not what changed |

### Communication Patterns

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 20 | **Chatbot and offer-to-continue artifacts** | "I hope this helps! Want me to continue?" | Remove entirely |
| 21 | **Cutoff disclaimers + gap-filling** | "While details are limited...", "maintains a low profile", "likely grew up..." | Find sources, say what's unknown, or remove; never guess |
| 22 | **Sycophantic tone** | "Great question! You're absolutely right!" | Respond directly |
| 30 | **Model-tool markup artifacts** | `settlement:contentReference[oaicite:4]{index=4}`, `[attached_file:1]`, `?utm_source=chatgpt.com` | Delete the artifact and the markup around it |
| 31 | **Hallucinated citations** | "According to a 2019 survey by the Chinese Academy of Sciences…" (invented to replace "experts say") | Keep the claim hedged; never fabricate a source |
| 32 | **Placeholder leakage** | "Hi [Recipient], … Best regards, [Your Name]" | Flag placeholders back to the user; never fill them in with guesses |
| 36 | **False balance** | "On the one hand X, on the other hand Y. The truth likely lies in between." | Drop the fake symmetry; state what the evidence shows |
| 37 | **Generic stock examples** | "Imagine Sarah, a small business owner…" | Use a real named example or cut the illustration |

### Filler and Hedging

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 23 | **Filler phrases** | "In order to", "Due to the fact that" | "To", "Because" |
| 24 | **Excessive hedging + booster absence** | "this might suggest that the effect may possibly be real" (after three replications) | Cut hedge stacks; use earned confidence only when the genre permits it |
| 25 | **Generic conclusions** | "The future looks bright" | Specific plans or facts |

### Structural and Statistical Patterns

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 40 | **Sentence-length uniformity (low burstiness)** | Every sentence 14–20 words, metronomic rhythm | Mix in a 5-word sentence and a 25-word one |
| 41 | **Paragraph / document symmetry** | Equal paragraphs; default 3- or 5-item lists | Let the important part run long; use the real item count |
| 42 | **Hyperconnectivity** | "However… Moreover… Consequently…" on every sentence | Drop half the connectors; let juxtaposition carry the logic |
| 43 | **Sentiment / stance flatness** | Uniform mild positivity, no negative emotion | Allow real irritation, doubt, enthusiasm |

### Russian-Language Patterns (RU)

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 44 | **Russian AI vocabulary / frame phrases** | «В современном мире… играет ключевую роль» | State the fact directly |
| 45 | **Russian syntactic calques from English** | «клиентоориентированно-сервисного результата», forced commas, calqued «однако» | Plain phrasing a person would actually speak |
| 46 | **Russian punctuation tells** | Capital after colon; тире on every sentence; "curly" quotes | Lowercase after colon; «ёлочки»; reduce тире (do not hard-cut as in #14) |

> **Russian inversions:** for Russian text, several English rules flip. Do **not** cut тире (#14 is off), **do** add agentless/impersonal passive (#13 inverts), and do **not** fragment long sentences (#40 softens). See [`references/patterns-ru.md`](references/patterns-ru.md).

### Current-Model and Contextual Patterns

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 47 | **Superficial guideline echoing** | "maintains an active social media presence, garnering independent coverage" | State what the subject actually does, with a concrete fact |
| 48 | **Model-specific signatures** | Claude "belies"; DeepSeek "somewhere a dog howls"; Gemini bullet dumps | Replace the family fingerprint; treat as a lead, not proof |

### Upstream-Synchronized Patterns

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 49 | **Manufactured punchlines / staccato drama** | "It had no preference. No prior. No nostalgia." | Connect the routine claim as ordinary prose; preserve only earned emphasis |
| 50 | **Aphorism formulas** | "Symmetry is the language of trust." | State the precise claim instead of dressing it as a maxim |
| 51 | **Conversational rhetorical openers** | "Honestly? It depends on how often you'll use it." | "Whether it's worth the price depends on how often you'll use it." |

### v2.21 Pattern Families

| # | Family | What it covers |
|---|--------|----------------|
| 52–57 | **Humanizer damage** | Thesaurus damage, clause atomization, persona injection, fake errors, hedge stripping, and residue cleanup |
| 58–67 | **Current-era and sourcing tells** | Formulaic closers, notability packing, specificity loss, Markdown skeletons, unsupported debate, misattribution, and source-count exaggeration |
| 68–69 | **Genre-gated grammar fingerprints** | Present-participial stacks and sentence-subject `That` clauses, with news and formal-register exceptions |
| 70–73 | **Additional Russian patterns** | Dangling adverbial participles, didactic disclaimers, formulaic openings, and recap-only conclusions |

The **Reliability and false positives** section now includes neurodivergent, translation, genre, short-text, post-paraphrase, and no-model-attribution guards. Aggressive rewriting requires convergence across independent pattern families. Em dashes and negative parallelism remain LEGACY corroboration only; their absence never proves human authorship.

## Full Example

The complete draft-audit-final example lives in [`references/examples.md`](references/examples.md#full-example). Its rewrite keeps every substantive input claim, labels unsupported assertions instead of replacing them with plausible inventions, and adds no person, experience, number, study, quotation, or source.

## References

- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) - Primary source
- [WikiProject AI Cleanup](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup) - Maintaining organization
- [Reinhart et al., *Do LLMs write like humans? Variation in grammatical and rhetorical styles*, PNAS 2025](https://www.pnas.org/doi/10.1073/pnas.2422455122) - structural differences (participle clauses, nominalizations); backs #3, #38, #40–43
- [Kobak et al., *Delving into LLM-assisted writing in biomedical publications through excess vocabulary*, Science Advances 2025](https://www.science.org/doi/10.1126/sciadv.adt3813) - excess-vocabulary frequency ratios (backs #7: delves r=28.0, underscores r=13.8, showcasing r=10.7)
- [Muñoz-Ortiz, Gómez-Rodríguez & Vilares, *Contrasting Linguistic Patterns in Human and LLM-Generated News Text*, Artificial Intelligence Review 2024](https://link.springer.com/article/10.1007/s10462-024-10903-2) - human/LLM syntactic contrast
- [Desaire et al., *Distinguishing academic science writing from humans or ChatGPT...*, Cell Reports Physical Science 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10704924/) - paragraph-length variance (AUC 0.98); backs #41
- [Liang et al., *GPT detectors are biased against non-native English writers*, Patterns 2023](https://arxiv.org/abs/2304.02819) - detector false positives; backs the Reliability section
- Shalevska 2024, *Hedges and Boosters in AI and Human Writing* - resolved hedge/booster frequencies; backs #24
- Geng & Trotta 2025 ([arXiv 2502.09606](https://arxiv.org/abs/2502.09606)) - AI vocabulary timeline and the April 2024 "delve" collapse; backs #7
- Russian-language tells: community write-ups on [Habr](https://habr.com/ru/articles/1022906/) and vc.ru (heuristic, not peer-reviewed) - backs #44–46
- [v2.21 evidence register](references/research.md#v221-evidence-register) - verified primary links and bounded claims for patterns #52–73, reliability guards, and evaluation methodology

## Version History

- **2.21.0** - Added patterns #52–73, evidence-backed reliability guards, specific-author voice anchoring, residue-first fact locking, nine stdlib diagnostics, two corpus pairs, and length/integrity reporting. Demoted #9 and #14 to LEGACY and expanded Russian канцелярит and grammar checks. See [CHANGELOG.md](CHANGELOG.md) for the full release notes.
- **2.20.0** - Added three upstream 2.8.x writing-pattern guards, fail-safe voice calibration, genre-aware booster guidance, and stronger fact preservation. Split the large skill into a compact core plus conditional references. Added Russian-aware structural/compliance metrics, a six-genre Russian eval corpus, aggregate baselines, tests, cross-agent skills CLI and Claude Code marketplace packaging, repository hygiene, and CI checks. See [CHANGELOG.md](CHANGELOG.md) for the full release notes.
- **2.19.0** - Eval-driven fix. Built a deterministic structural-metrics harness (kept local, not shipped) and ran it on a 12-genre before/after corpus. Result: applied to real text, the skill reliably strips em dashes (100%), participial overload (0%→83% pass), nominalizations, and the *may*-heavy hedging, and it *improves* sentence-length variance (17%→83% pass) rather than regressing as one hand-written example had implied. The one systematic gap was boosters: across all 12 rewrites the skill added *zero* boosters, even though booster-absence is the single most reliable AI tell (pattern 24). Hardened pattern 24, the structural self-audit, and the Process so that adding at least one booster (where the evidence earns it) is a mandatory step, not an optional check. No new patterns.
- **2.18.0** - Folded in three Gemini deep-research reports. Upgraded the structural patterns (#40–43) with measured thresholds: burstiness coefficient ~0.15–0.45 for humans vs ~0 for AI; words-per-paragraph standard deviation >25 separated human from AI at AUC 0.98 (Desaire et al. 2023); transition density ~1.8× the human rate; positive-sentiment inflation 37–54% (Abdulhai et al. 2026). Rewrote #24's hedge claim with resolved numbers (Shalevska 2024: AI hedges ~1.39×, ~84% of them the single word *may*, and *zero* boosters; the booster gap and the *may* monopoly are the real signals, not "twice as many hedges"). Made #7 era-aware (the loud first-wave words like *delve* collapsed in frequency around April 2024 once publicized; second-wave words *significant/potential/findings/crucial* now carry more signal). Added a genre/language caveat to #13 (the agentless passive is the human norm in technical writing and in Russian, and AI under-produces it). Added pattern **#47** (superficial guideline echoing) and **#48** (model-specific signatures: Claude "belies", DeepSeek environmental framing, Gemini bullet reliance). Greatly expanded the Russian section: the «Однако,» calque (highest-confidence RU marker), «Это не про X. Это про Y», «за которым последовало», typographic sterility, and an explicit "Russian inversions" block (for Russian: do not cut тире, do add passive/impersonal forms, do not fragment long sentences). Added a RELIABILITY AND FALSE POSITIVES section (Liang et al. 2023: ~61% false positives on non-native English; structural signals are robust, while em dashes, "not X but Y", rule of three, and curly quotes are weak, over-fired folk theories to down-weight as evidence). Total now 48 patterns plus the structural self-audit and reliability sections.
- **2.17.0** - Voice calibration is now offered proactively. When the skill is invoked it asks once (via AskUserQuestion) whether you want to paste a short sample of your own writing for style matching, instead of only using a sample if you happened to provide one. If you skip or have no sample, it falls back to the default voice. (Skills are stateless across sessions, so in practice this is offered at the start of each session/run, not literally only the first time ever.) No pattern changes.
- **2.16.0** - Added two new sections and fixed several self-compliance issues. (1) **STRUCTURAL AND STATISTICAL TELLS (#40–43):** sentence-length uniformity / low burstiness, paragraph and document symmetry, hyperconnectivity (a connector on every sentence), and sentiment/stance flatness, plus a structural self-audit checklist with operational targets (e.g. at least one ≤5-word and one ≥25-word sentence per ~5; cut half the connectors). This covers the structural signal a word/phrase blocklist misses. Backed by Reinhart et al. *PNAS* 2025 (present-participle clauses ~2–5× and nominalizations ~1.5–2× the human rate) and an iScience 2026 corpus study (length uniformity, positive-sentiment/certainty skew); detector-evasion research confirms structure survives word-swapping. (2) **RUSSIAN-LANGUAGE TELLS (#44–46):** a Russian vocabulary/frame-phrase list parallel to #7 («важно отметить», «в современном мире», «играет ключевую роль»), a Russian syntactic-calque detector (the highest-value RU-only tell, since it does not depend on vocabulary), and Russian punctuation tells (capital-after-colon, тире reduce-not-cut, «ёлочки»), with a note that the structural patterns (8–13, 24, 28, 33, 36, 38, 40–43) apply to Russian unchanged. Also: softened #14's rationale (the em dash is now a model-dependent, frequently over-fired tell, and Claude/Gemini barely use it) while keeping the hard cut for English output; fixed two dogfooding bugs (em dashes inside the #24 and #34 "After" examples, and in several Rule/Problem prose lines, all of which violated #14); corrected the frontmatter description ("em dash overuse" → "em and en dash removal"); named **Shalevska 2024** as the source for #24's hedge/booster claim instead of the vague "Hedges and Boosters comparative study" (and softened the unverified "twice as many hedges" magnitude); and gave the previously unheadered patterns #30–39 a real section header. Total now 46 patterns.
- **2.15.0** - Merge pass: brought back three rules from the upstream blader/humanizer 2.7.0 line that this fork had diverged from. (1) Added pattern #39 (diff-anchored writing: prose that narrates a change instead of describing the thing as it is). (2) Hardened pattern #14 from "em dash overuse / prefer commas" to a hard cut — the final rewrite must contain zero em or en dashes, with a scan step before returning. (3) Expanded pattern #21 from bare cutoff disclaimers to also cover speculative gap-filling ("maintains a low profile", "likely grew up..."), cross-referencing the fact-preservation rules. Also fixed the stale "29 patterns" header (this fork has documented 38+ since 2.14.0). Total now 39 patterns. Note: this fork's pattern numbers #30-38 differ from upstream's; #39 is upstream's #30 renumbered to avoid collision.
- **2.14.1** - Refined pattern #24 (excessive hedging) to cover the *booster-absence* half of the same asymmetry: AI text over-uses hedges (could, might, potentially, possibly, may suggest) *and* under-uses boosters (clearly, definitely, obviously, in fact, indeed). The fix is not just removing hedges; it is letting the paragraph commit when the evidence has already done the work. Added a second before/after showing booster absence after stacked evidence. Backed by Almulla 2025 and Shalevska 2024 (*Hedges and Boosters in AI and Human Writing*), both reporting that AI essays badly under-use boosters and lean harder on hedges than comparable human writing (exact magnitudes vary across studies).
- **2.14.0** - Added pattern #38: nominalization overuse — abstract noun phrases ("the implementation of", "the realization of", "the consideration of") chained with weak linking verbs ("is", "provides", "was conducted"). Asks the rewrite to find the action hidden in the `-tion`/`-ment`/`-ance` noun and turn it back into a verb. Backed by Munoz-Ortiz et al. 2024 and Almulla 2025 corpus studies showing AI text uses more nominalisations than human text. Total now 38 patterns.
- **2.13.1** - Refined pattern #34 (aphoristic closer): split "Signs to watch" into formal/elevated epigrams *and* folksy analogy closers ("X is basically like Y", "It's like trying to Z", "Бояться X примерно как бояться Y"). Same structural beat in a chatty register; added a note that register doesn't change the move. Updated rule and added a folksy before/after.
- **2.13.0** - Added a FACT PRESERVATION AND OUTPUT COMPLETENESS section with three rules (never invent facts, never truncate, never over-clean) and a step-10 fact/completeness check in the Process. No new patterns; this guardrail binds the existing ones so pattern removal cannot justify fabrication or content loss.
- **2.12.0** - Added pattern #36 (false balance / artificial both-sides: "some say X, others say Y, the truth lies in between") and pattern #37 (generic stock examples: Sarah the small business owner, Alice and Bob, Acme Corp). Total now 37 patterns.
- **2.11.0** - Added pattern #35: prestige-metaphor nouns used as sentence frames (tapestry, mosaic, symphony, orchestra, labyrinth, odyssey, etc.), catching structural overuse that pattern 7's word-list alone does not. Total now 35 patterns.
- **2.10.0** - Added pattern #33 (document-internal style shift: mid-document register, tense, spelling, or POV change) and pattern #34 (aphoristic closer: tweetable mantras masquerading as conclusions). Total now 34 patterns.
- **2.9.0** - Expanded pattern #7 (AI vocabulary words) with the post-LLM corpus words from Kobak et al. 2025: meticulous/meticulously, commendable, resonate, realm, holistic, leverage, robust, seamless, straightforward, nuanced, paramount, unwavering, surpass, elevate, empower, swiftly, navigate (figurative), alignment, and a tier-2 set. Added a note that the signal is clustering, not any single word.
- **2.8.0** - Added pattern #32: placeholder and template leakage (`[Your Name]`, `[INSERT URL]`, bracketed "describe the specific section" instructions, `2025-XX-XX` dates, `YOUR_API_KEY`, etc.). Total now 32 patterns.
- **2.7.0** - Added pattern #31: hallucinated citations. Added an explicit "do not invent sources" rule to pattern #5 (vague attributions) and fixed the pattern #5 example so it no longer teaches fabrication. Total now 31 patterns.
- **2.6.0** - Added pattern #30: model-tool markup artifacts (ChatGPT `contentReference`/`oaicite`/`oai_citation`, Perplexity `[attached_file]`/`[web]`, Grok `<grok-card>`, `?utm_source=chatgpt.com` URLs), raising the total to 30 patterns
- **2.5.1** - Added a passive-voice / subjectless-fragment rule, raising the total to 29 patterns
- **2.5.0** - Added patterns for persuasive framing, signposting, and fragmented headers; expanded negative parallelisms to cover tailing negations; tightened wording around em dash overuse; fixed frontmatter wording to use "filler phrases"
- **2.4.0** - Added voice calibration: match the user's personal writing style from samples
- **2.3.0** - Added pattern #25: hyphenated word pair overuse
- **2.2.0** - Added a final "obviously AI generated" audit + second-pass rewrite prompts
- **2.1.1** - Fixed pattern #18 example (curly quotes vs straight quotes)
- **2.1.0** - Added before/after examples for all 24 patterns
- **2.0.0** - Complete rewrite based on raw Wikipedia article content
- **1.0.0** - Initial release

## License

MIT
