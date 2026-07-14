---
name: humanizer-extended
version: 2.21.0
description: |
  Remove signs of AI-generated writing while preserving facts, coverage, register,
  and the author's voice. Use when rewriting or reviewing English or Russian prose
  for formulaic AI vocabulary, rhetoric, formatting, sourcing artifacts, structural
  uniformity, synthetic personality, or translation calques. Supports optional voice
  matching and genre-aware editing for articles, documentation, essays, marketing,
  biographies, reviews, reference text, and technical or academic writing.
license: MIT
compatibility: claude-code opencode
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Humanizer: remove AI writing patterns

Edit prose so it reads like a person wrote it. Remove specific tells rather than laundering the text toward a detector score.

## Load references on demand

Keep this file as the operating core. Load only the reference needed for the current text:

- **Russian text:** read [`references/patterns-ru.md`](references/patterns-ru.md) before editing. Its rules override conflicting English rules.
- **Expanded pattern guidance and examples:** read [`references/examples.md`](references/examples.md) when a registry entry is unclear, when a watched phrase may be legitimate, or when a concrete before/after model would help. Read its Full Example before using the full draft-audit-final workflow for the first time.
- **Research and reliability:** read [`references/research.md`](references/research.md) when weighing false positives, applying quantitative heuristics, explaining why a tell matters, or comparing signal strength. Do not load it for a routine rewrite.

## Non-negotiable constraints

### Preserve facts

- Do not add statistics, dates, names, companies, institutions, studies, quotations, citations, identifiers, or URLs absent from the input or user-supplied context.
- Do not turn “experts believe” into a plausible specific citation. If a claim lacks support, hedge it honestly, mark `[citation needed]`, say it is not well documented, or remove the unsupported claim.
- Do not silently fill placeholders such as `[Your Name]`, `[Insert URL]`, or `YYYY-MM-DD`; flag them for the user.
- Do not invent a personal experience, feeling, interview, case study, or “realistic” example to add soul.
- Treat citations already present in the input as claims to preserve, not as verified truth. Verify them only when the task and available tools permit it; otherwise retain with an appropriate caveat or flag.

### Preserve coverage

- Cover every claim, caveat, heading, list item, and data point in the input. Rewrite problematic content; do not use deletion as a shortcut.
- A shorter sentence is fine. A rewrite that loses content is not.
- If the input cannot fit in one pass, ask how to split it instead of returning a truncated document.

### Preserve legitimate voice and secondhand text

- Match the requested genre, register, dialect, spelling convention, point of view, and terminology.
- Do not flag or rewrite watched phrases merely because they occur inside quotations, titles, proper names, citations, code, or examples that discuss the phrase rather than use it. Preserve secondhand text unless the user asks to edit it too.
- Look for clusters and structural patterns, not isolated words. Perfect grammar, formal vocabulary, one transition, one short sentence, one em dash, or one rule of three proves nothing.
- Do not over-clean. Keep vivid language, genuine asymmetry, specific odd details, mixed feelings, and defensible stylistic choices.

## Voice calibration and genre gate

1. Calibrate on at least three authentic samples from the same author: compare sentence-length distribution, lexical register, paragraph structure, punctuation, openings, transitions, and recurring phrases. Do not smooth away distinctive habits.
2. If the user has not supplied three samples, offer voice matching once. Use `AskUserQuestion` only when available; otherwise continue with a genre-appropriate default, without blocking, and avoid aggressive voice normalization.
3. Anchor edits to that specific author, never to an abstract “human” voice. Generic humanizing remains distinguishable as sample size grows (arXiv:2505.14608); post-editing toward a specific writer's style is more effective (arXiv:2604.24444).
4. Let authentic samples override generic cleanup preferences. If they systematically use em or en dashes, preserve that habit at a comparable rate. Pattern 14's default applies only to English output without samples; Russian punctuation follows the RU reference.
5. Treat a human-edited AI draft as an editing task, not an attribution task. Preserve the author's own wording even when it is statistically AI-like.
6. Choose the genre before adding personality. Add no opinions, first person, jokes, uncertainty, or feelings to neutral reference, technical, legal, or methodology prose. In voice-led prose, preserve supported stance, asymmetry, asides, and self-corrections without manufacturing affect.

## Compact pattern registry

Use the registry to scan. Open the examples reference for complete signs, explanations, and before/after rewrites.

### Content, language, and grammar

1. **Undue emphasis on significance, legacy, and broader trends:** replace inflated claims that an ordinary fact “marks,” “underscores,” or “stands as a testament” with the concrete fact.
2. **Undue emphasis on notability and media coverage:** stop listing outlets, followers, or “independent coverage” without saying what was actually reported and why it matters.
3. **Superficial analyses with -ing endings:** cut trailing participial clauses that add fake depth; state the supported relationship as a normal clause.
4. **Promotional and advertisement-like language:** replace “vibrant,” “breathtaking,” “renowned,” and similar sales copy with neutral, specific description.
5. **Vague attributions and weasel words:** name a supplied, verifiable source or honestly hedge, flag, or remove the unsupported claim; never invent a source. In RAG-era prose, generic `-ing` tails can attach to real names, so apply pattern 66 before trusting the attribution.
6. **Outline-like challenges and future prospects:** replace stock “Despite these challenges…” sections with documented problems, actions, and outcomes.
7. **Overused AI vocabulary (era-stratified):** treat 2023–24 words (`delve`, `tapestry`, `testament`) as deprecated solo signals, 2024–25 vocabulary as transitional, and 2025+ clusters (`emphasizing`, `enhance`, `highlighting`, `showcasing`, notability language) as current leads. Watch the shift from superlatives to evaluatives such as `notable`, `considerable`, `meaningful`, `robust`, and `nuanced`. Vocabulary from any era requires corroboration from another pattern family.
8. **Copula avoidance:** replace ornamental “serves as,” “stands as,” “boasts,” and “features” with `is`, `are`, or `has` where accurate.
9. **Negative parallelisms and tailing negations (LEGACY):** use clustered “not only…but,” “not X, but Y,” and clipped “no guessing” tails only as corroboration; humanizers actively remove them, so absence is not evidence of human authorship. Keep a legitimate isolated contrast.
10. **Rule-of-three overuse:** use the number of items the content requires instead of forcing repeated tricolons.
11. **Elegant variation:** repeat the correct noun when synonym cycling makes one subject look like several.
12. **False ranges:** replace “from X to Y” when the endpoints do not share a meaningful scale.
13. **Passive voice and subjectless fragments:** name the actor when that improves ordinary prose, but preserve agentless passive in methods, technical genres, and languages where it is normal.

### Style, communication, and filler

14. **Em and en dashes (LEGACY):** when editing English without a voice sample, replace mechanical em/en dashes with punctuation or recast sentences; with samples, calibration wins, and Russian uses its RU override. Humanizers actively remove dashes, so their absence is not evidence of human authorship.
15. **Overuse of boldface:** remove mechanical emphasis and keep bold only where the document's format needs it.
16. **Inline-header vertical lists:** turn repeated bold-label bullets into prose or a genuinely useful list.
17. **Title Case in headings:** use the heading convention of the language, style guide, or author instead of automatic English Title Case.
18. **Emojis:** remove decorative emoji unless the user's genre and voice clearly use them.
19. **Curly quotation marks:** for English with no contrary style requirement, normalize mechanical curly quotes; treat typography alone as weak evidence and use Russian «ёлочки» where appropriate.
20. **Collaborative communication artifacts:** delete pasted chatbot framing and offer-to-continue closers such as “I hope this helps,” “Want me to…?”, “Should I continue?”, and “Let me know if…”.
21. **Knowledge-cutoff disclaimers and speculative gap-filling:** state only what is known; do not turn missing information into guesses about dates, biographies, or privacy.
22. **Sycophantic or servile tone:** replace praise and automatic agreement with a direct response to the substantive point.
23. **Filler phrases:** compress “in order to,” “due to the fact that,” and similar padding into direct language.
24. **Excessive hedging and booster absence:** remove hedge stacks and the `may` monopoly; add a booster only when evidence earns it **and** the genre permits authorial confidence. Never force boosters into neutral reference, encyclopedic, or methodology text.
25. **Generic positive conclusions:** end on a concrete fact, decision, consequence, or specific call rather than “the future looks bright.”
26. **Hyphenated word-pair overuse:** keep grammatically required attributive compounds such as “a high-quality report”; vary only optional forms and normally drop the hyphen in predicate position. Treat this as a weak, down-weighted signal.
27. **Persuasive authority tropes:** cut “the real question,” “at its core,” and similar ceremony that pretends an ordinary claim is a revelation.
28. **Signposting and announcements:** do the work instead of saying “let's dive in” or “here's what you need to know.”
29. **Fragmented headers:** remove a warm-up line that merely restates its heading.

### Sourcing, rhetoric, structure, and context

30. **Model-tool markup artifacts:** remove leaked citation/tool tags and tracking suffixes; restore a real citation if supplied or remove the unsupported claim.
31. **Hallucinated citations:** never add bibliographic precision; verify when possible, otherwise preserve cautiously, flag `[citation needed]`, hedge, or drop the claim.
32. **Placeholder and template leakage:** flag unfilled template tokens and wait for user context rather than guessing defaults.
33. **Document-internal style shift:** enforce one chosen register, tense, spelling system, point of view, citation style, and date format across the document.
34. **Aphoristic closer:** replace tweet-ready “X is really Y” endings and folksy analogy closers with a concrete last point or stop earlier.
35. **Prestige-metaphor frames:** delete mixed “tapestry/symphony/journey/landscape” frames; keep at most one earned, developed metaphor.
36. **False balance or artificial both-sides:** do not invent a controversy or midpoint when the supplied evidence is lopsided; remain neutral without manufacturing symmetry.
37. **Generic stock examples:** use a user-supplied real example, make a hypothetical explicitly hypothetical, or cut it; never fabricate a named case or statistic.
38. **Nominalization overuse:** turn clusters of abstract action nouns and weak verbs back into concrete verbs, restoring the actor when the genre calls for one.
39. **Diff-anchored writing:** describe what a thing does, not what changed, except in changelogs, release notes, migrations, PRs, and other version-scoped documents.
40. **Sentence-length uniformity:** break a metronomic run of mid-length sentences with natural variation; do not manufacture a quota-driven staccato rhythm.
41. **Paragraph and document symmetry:** let important material run longer and stop padding sections or lists to matching sizes.
42. **Hyperconnectivity:** remove redundant sentence-opening connectors and let clear adjacent sentences carry their own logic.
43. **Sentiment and stance flatness:** where the genre and source voice permit, preserve real irritation, doubt, excitement, or mixed feelings; never invent them.
44. **Russian AI vocabulary, frame phrases, and канцелярит:** use the RU reference to check stock frames plus action nominalizations, genitive chains longer than three, `является` as a weak copula, and avoidable passive. Flag at least 2 features per 500 words; official/legal prose is neutral, and scientific prose requires more than 3 per 500.
45. **Russian syntactic calques from English:** rewrite imported English architecture into spoken, idiomatic Russian; follow the inversion rules in the RU reference.
46. **Russian punctuation tells:** lowercase ordinary text after a colon, use Russian quotation conventions, and reduce rather than eliminate legitimate тире.
47. **Superficial guideline echoing:** delete claims that merely recite platform criteria; state the supplied concrete fact and let it demonstrate relevance.
48. **Model-specific signatures:** use family fingerprints such as `belies`, bullet dumping, or cinematic interjections only as low-confidence leads, never proof.
49. **Manufactured punchlines and staccato drama:** collapse a run of quotable fragments into ordinary connected prose; preserve an isolated short sentence that genuinely earns emphasis.
50. **Aphorism formulas:** replace mid-text “X is the language/currency/architecture of Y” and “X becomes a trap” formulas with the precise claim they gesture at.
51. **Conversational rhetorical openers:** remove fake-candid hooks such as “Honestly?”, “Look,” “Here's the thing,” and “Real talk” when they stage a routine point; do not flag ordinary mid-sentence use.

### Humanizer damage (anti-humanization)

52. **Thesaurus damage:** restore a common word when a rare synonym breaks collocation or register; check authentic voice samples first. See [`references/examples.md`](references/examples.md#52-thesaurus-damage).
53. **Clause atomization:** when at least four consecutive single-clause sentences have lost meaningful subordination, reconnect them non-uniformly; never split them further. See [`references/examples.md`](references/examples.md#53-clause-atomization).
54. **Persona injection:** restore the source's grammatical person after an unsupported shift to `we`, `I`, or `you`; do not flag a person used in authentic voice samples. See [`references/examples.md`](references/examples.md#54-persona-injection).
55. **Fake typos or forced slang:** never inject typos, slang, or fake informality. Treat found instances as damage and repair them. See [`references/examples.md`](references/examples.md#55-fake-typos--forced-slang--hard-ban).
56. **Hedge stripping:** restore deleted epistemic modality that turned a hypothesis into a fact; treat this as a fact-preservation violation. See [`references/examples.md`](references/examples.md#56-hedge-stripping).
57. **Humanizer residue:** clean garbage tokens, dangling citations, and escaped Markdown before any style work. See [`references/examples.md`](references/examples.md#57-humanizer-residue-triage-first).

### Wikipedia-era and 2025+ tells

58. **Despite-challenges closer:** replace a vague concede-then-optimism document closer with supported specifics; standard report limitations sections are neutral. See [`references/examples.md`](references/examples.md#58-despite-challenges-closer).
59. **Notability packing:** replace meta-claims about leading outlets, attention, or social presence with verifiable specifics; treat them as genre-normal in marketing copy. See [`references/examples.md`](references/examples.md#59-notability-packing).
60. **Hedged inflation:** when a hedge and inflated historical-importance claim occur together, state the supported impact or cut it; grant proposals are genre-gated. See [`references/examples.md`](references/examples.md#60-hedged-inflation).
61. **Specificity erosion:** restore a rare, concrete source fact replaced by generic praise; this is a fact-preservation violation. See [`references/examples.md`](references/examples.md#61-specificity-erosion).
62. **Inanimate rhetorical agent:** replace “the fact underscores” or `сам факт подчёркивает` with an animate agent or plain supported verb; preserve deliberate literary personification. See [`references/examples.md`](references/examples.md#62-inanimate-rhetorical-agent-enru).
63. **Markdown skeleton:** fix repeated separators, heading-level jumps, micro-tables, escaped Markdown, and placeholder dates independently. See [`references/examples.md`](references/examples.md#63-markdown-skeleton).
64. **“Refers to” lead:** open with what the subject is or does instead of treating a descriptive title as a proper name; dictionary definitions are neutral. See [`references/examples.md`](references/examples.md#64-refers-to-lead).
65. **Manufactured broader debate:** name supplied participants and positions or remove an unsupported claim that something “generated debate.” See [`references/examples.md`](references/examples.md#65-manufactured-broader-debate).
66. **Named-source misattribution:** verify generic `-ing` tails attached to real names; remove an unverifiable attribution rather than inventing a quote. See [`references/examples.md`](references/examples.md#66-named-source-misattribution-rag-era-upgrades-pattern-5).
67. **Source-quantity exaggeration:** make `several`, `multiple`, or `ряд исследователей` match the actual cited source count. See [`references/examples.md`](references/examples.md#67-source-quantity-exaggeration).

### Grammar fingerprints (genre-gated)

68. **Present-participial stacking:** flag at least 2 V-ing clauses per sentence in academic, blog, or creative prose and at least 3 in technical documentation; treat news and journalism as neutral because the direction reverses there. Require two other pattern families before aggressive rewriting. See [`references/examples.md`](references/examples.md#68-present-participial-stacking-genre-gated).
69. **That-clause subjects:** flag more than 1 sentence-subject `That [clause] is/was` per 500 words, or more than 2 in academic prose; formal argumentative use is neutral. See [`references/examples.md`](references/examples.md#69-that-clause-subjects-genre-gated).

### Additional Russian patterns

70. **Висячий деепричастный оборот:** перестроить фразу, если субъект деепричастия не совпадает с субъектом главной части; это грамматическая ошибка во всех жанрах. См. [`references/patterns-ru.md`](references/patterns-ru.md#70-висячий-деепричастный-оборот).
71. **Дидактические дисклеймеры:** убрать кластер из двух и более оборотов вроде `важно отметить` или `стоит учесть` на 500 слов; учебный и справочный тексты нейтральны. См. [`references/patterns-ru.md`](references/patterns-ru.md#71-дидактические-дисклеймеры).
72. **Формульные зачины:** переписать `В данной работе…` и аналоги в первых двух предложениях; стандартные аннотации и подтверждённая авторская привычка нейтральны. См. [`references/patterns-ru.md`](references/patterns-ru.md#72-формульные-зачины).
73. **Формульное «Заключение»:** заменить заключение, состоящее только из пересказа, на подтверждённый входом синтез следствий или удалить повтор; сам раздел `Заключение` нейтрален. См. [`references/patterns-ru.md`](references/patterns-ru.md#73-формульное-заключение).

## Reliability and false-positive guards

Rank structural clusters, internal style shifts, sourcing artifacts, and repeated rhetoric above isolated vocabulary or punctuation. Preserve quotations, titles, proper names, citations, code, and examples under discussion. Preserve hard-to-fabricate specifics and intentional choices.

### Neurodivergent writing guard

Do not “repair” directness without hedges, terminology repetition, low pronoun density, structural regularity, or hyper-precise factual language as AI tells. Require at least two non-stylistic signals, such as sourcing artifacts, chatbot framing, or fabricated citations, before aggressive rewriting (Chambers & Kelley, AIED 2025).

### Translation guard

Machine translation is a major false-positive class (Weber-Wulff et al., 2023). When calques or foreign word order indicate translation, disable lexical and uniformity patterns and edit only for natural target-language usage.

### Genre calibration

Demote these signals to neutral: vocabulary pattern 7, dash pattern 14, and participial pattern 68 in résumés and cover letters; patterns 9 and 44 in legal prose; patterns 58 and 59 in press releases; pattern 72 in standard abstracts. False-positive rates vary sharply by genre (Jabarian & Imas, BFI 2025).

### Short-text abstention

For texts under 100 words, abstain from AI-authorship or pattern-based verdicts. Still repair clear grammar or residue and perform specific user-requested edits under the preservation constraints; do not perform an aggressive detector-driven rewrite.

### Convergence requirement

Require at least three independent pattern families (lexical, structural, grammatical, sourcing) before aggressive rewriting. A single family drifts as LLM language enters human usage.

### Post-paraphrase abstention

If pattern 57 suggests a prior humanizer or paraphraser, absence of AI tells does not prove human authorship (Nature, 2026). Switch from detection to edit quality and fact checking; never conclude `likely human` from that absence.

### No model attribution

Do not conclude that prose “sounds like Claude” or “sounds like GPT.” Statistical model fingerprints exist (Sun et al., ICML 2025), but pattern 48 remains a low-confidence editing lead, not an attribution method.

### Anti-humanization prohibitions

Never insert typos, slang, fake informality, a new grammatical person, reduced epistemic modality, or sentence splits designed to game uniformity metrics. Repair such damage under patterns 52–57.

## Process

1. **Residue cleanup:** repair patterns 57 and 63 before any stylistic work.
2. **Fact lock:** inventory claims and lock numbers, dates, URLs, names, negations, and modality. After editing, run `immutable_token_audit` when available and target zero violations; otherwise compare them manually.
3. **Genre gate:** determine language and genre, load the RU reference for Russian, and apply every relevant guard.
4. **Voice anchor:** calibrate on at least three authentic samples or avoid aggressive voice rewriting.
5. **Pattern pass:** protect secondhand text, scan patterns 1–73 under their gates and convergence requirement, write a fact-preserving draft, ask internally **“What makes the below so obviously AI generated?”**, and revise. Do not expose chain-of-thought.
6. **Anti-humanization check:** confirm that the edit introduced none of patterns 52–56.
7. **Structural and integrity audit:** apply the v2.21 metrics and abstention conditions when available, then compare the final version against the input claim by claim. Remove every new specific and restore every dropped item.

## Structural self-audit

Check deliberately rather than chasing a detector score:

- **Rhythm:** Are sentences and paragraphs naturally varied, or uniformly mid-length and equal-sized? Do not “fix” them into repeated one-line punchlines.
- **Transitions:** If most sentences announce their logical relation, remove redundant connectors.
- **Participles and nominalizations:** If a paragraph clusters trailing `-ing` clauses or abstract `-tion/-ment/-ance` nouns, restore plain clauses and verbs.
- **Hedges and boosters:** Remove hedge stacks and diversify repeated `may`. Treat zero boosters as actionable only when the evidence supports confidence and the genre permits an authored stance. Zero is acceptable in neutral reference, encyclopedic, methodology, and genuinely uncertain text.
- **Affect:** Add no emotion. Preserve or clarify only the stance supported by the input, sample, and genre.
- **Rhetorical drama:** Check for staccato runs, aphorism formulas, and a manufactured closer after varying rhythm.
- **Dashes:** Treat English dash frequency as weak, legacy corroboration rather than a pass/fail signal. Rewrite only mechanical clusters unless a supplied style guide says otherwise; with voice samples, match their punctuation. For Russian, follow the RU reference.
- **Integrity:** Confirm that no fact, citation, name, number, quotation, placeholder value, or personal experience was invented and no input content was lost.

## Output format

Provide:

1. **Draft rewrite**
2. **“What makes the below so obviously AI generated?”** with brief bullets about remaining tells
3. **Final rewrite** revised after the audit
4. A short summary of changes only when useful

For the complete, fact-preserving Full Example, read [`references/examples.md`](references/examples.md#full-example).

## Reference basis

This skill derives its pattern taxonomy from [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup, and extends it with structural, sourcing, current-model, and Russian-language guidance. See [`references/research.md`](references/research.md) for the evidence notes and limits.
