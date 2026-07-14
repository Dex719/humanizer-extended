---
name: humanizer-extended
version: 2.20.0
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

1. Check whether the user already supplied a writing sample. If not, offer once to match a sample of two or three paragraphs or to use the default voice.
2. Use `AskUserQuestion` only when it is available in the current harness. If it is unavailable or unsupported, continue immediately with the default voice without asking, failing, or reporting an error. Do not block or ask twice in one session.
3. When a sample exists, analyze sentence length, vocabulary, paragraph openings, punctuation, recurring phrases, transitions, and register. Replace AI patterns with the writer's own patterns rather than with a generic “human” style.
4. Let the sample override generic cleanup preferences. In particular, if it systematically uses em or en dashes, preserve that habit at a comparable frequency. Pattern 14's hard cut applies only to English output with no sample. Russian punctuation follows the RU reference regardless.
5. Choose the genre before adding personality. Apply PERSONALITY AND SOUL only to genres where an authored stance belongs: personal blogs, essays, opinion, reviews, and similar voice-led prose. Do **not** inject opinions, first person, jokes, uncertainty, or feelings into neutral references, encyclopedic text, documentation, methodology, legal writing, or other genres where plain neutrality is the human voice.
6. When personality is appropriate, vary rhythm, allow genuine complexity, use first person only if the input or authorial context supports it, and keep real asides or self-corrections. Never manufacture affect to satisfy this step.

## Compact pattern registry

Use the registry to scan. Open the examples reference for complete signs, explanations, and before/after rewrites.

### Content, language, and grammar

1. **Undue emphasis on significance, legacy, and broader trends:** replace inflated claims that an ordinary fact “marks,” “underscores,” or “stands as a testament” with the concrete fact.
2. **Undue emphasis on notability and media coverage:** stop listing outlets, followers, or “independent coverage” without saying what was actually reported and why it matters.
3. **Superficial analyses with -ing endings:** cut trailing participial clauses that add fake depth; state the supported relationship as a normal clause.
4. **Promotional and advertisement-like language:** replace “vibrant,” “breathtaking,” “renowned,” and similar sales copy with neutral, specific description.
5. **Vague attributions and weasel words:** name a supplied, verifiable source or honestly hedge, flag, or remove the unsupported claim; never invent a source.
6. **Outline-like challenges and future prospects:** replace stock “Despite these challenges…” sections with documented problems, actions, and outcomes.
7. **Overused AI vocabulary:** edit clusters of tier-1/tier-2 words, not every occurrence; prefer plain wording without creating an unnatural avoidance dialect.
8. **Copula avoidance:** replace ornamental “serves as,” “stands as,” “boasts,” and “features” with `is`, `are`, or `has` where accurate.
9. **Negative parallelisms and tailing negations:** reduce clustered “not only…but,” “not X, but Y,” and clipped “no guessing” tails; keep a legitimate isolated contrast.
10. **Rule-of-three overuse:** use the number of items the content requires instead of forcing repeated tricolons.
11. **Elegant variation:** repeat the correct noun when synonym cycling makes one subject look like several.
12. **False ranges:** replace “from X to Y” when the endpoints do not share a meaningful scale.
13. **Passive voice and subjectless fragments:** name the actor when that improves ordinary prose, but preserve agentless passive in methods, technical genres, and languages where it is normal.

### Style, communication, and filler

14. **Em and en dashes:** for English with no voice sample, replace every em/en dash with punctuation or a recast sentence; with a sample, calibration wins, and for Russian load the RU override.
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
44. **Russian AI vocabulary and frame phrases:** for Russian, remove clusters of bureaucratic calques and stock frames using the RU reference.
45. **Russian syntactic calques from English:** rewrite imported English architecture into spoken, idiomatic Russian; follow the inversion rules in the RU reference.
46. **Russian punctuation tells:** lowercase ordinary text after a colon, use Russian quotation conventions, and reduce rather than eliminate legitimate тире.
47. **Superficial guideline echoing:** delete claims that merely recite platform criteria; state the supplied concrete fact and let it demonstrate relevance.
48. **Model-specific signatures:** use family fingerprints such as `belies`, bullet dumping, or cinematic interjections only as low-confidence leads, never proof.
49. **Manufactured punchlines and staccato drama:** collapse a run of quotable fragments into ordinary connected prose; preserve an isolated short sentence that genuinely earns emphasis.
50. **Aphorism formulas:** replace mid-text “X is the language/currency/architecture of Y” and “X becomes a trap” formulas with the precise claim they gesture at.
51. **Conversational rhetorical openers:** remove fake-candid hooks such as “Honestly?”, “Look,” “Here's the thing,” and “Real talk” when they stage a routine point; do not flag ordinary mid-sentence use.

## Reliability and false-positive guards

- Rank structural clusters, internal style shifts, sourcing artifacts, and repeated rhetoric above isolated vocabulary or punctuation.
- Down-weight em dashes, curly quotes, hyphenation, rules of three, negative parallelism, common transitions, and a single short sentence as evidence. Edit them only when the applicable style rule calls for it or when they form a cluster.
- Preserve secondhand text: quotations, titles, proper names, citations, source excerpts, code, and examples under discussion do not trigger a rewrite merely by containing a watched phrase.
- Respect genre and language inversions. Academic methods can prefer agentless passive; Russian allows long sentences, impersonal constructions, and grammatical тире.
- Do not equate non-native, simple, formal, bland, polished, or consistently formatted prose with AI authorship.
- Preserve hard-to-fabricate specifics, unresolved tension, era-bound references, genuine asides, and intentional choices. Consult the research reference for evidence strength and detailed guards.

## Process

0. Offer optional voice calibration once. If `AskUserQuestion` is unavailable, silently use the genre-appropriate default.
1. Determine the language and genre. For Russian, load the RU reference before applying any global rule.
2. Read the whole input and inventory its claims, caveats, structure, terminology, and supplied voice markers.
3. Scan for clusters from the registry. Protect quotations and other secondhand text before editing.
4. Write a draft that rewrites each problem while preserving facts and coverage.
5. Ask internally: **“What makes the below so obviously AI generated?”** List the remaining tells briefly.
6. Revise into the final version. Do not expose chain-of-thought; provide only the brief diagnostic bullets requested by the output format.
7. Compare final against input claim by claim. Remove every new specific and restore every dropped item.

## Structural self-audit

Check deliberately rather than chasing a detector score:

- **Rhythm:** Are sentences and paragraphs naturally varied, or uniformly mid-length and equal-sized? Do not “fix” them into repeated one-line punchlines.
- **Transitions:** If most sentences announce their logical relation, remove redundant connectors.
- **Participles and nominalizations:** If a paragraph clusters trailing `-ing` clauses or abstract `-tion/-ment/-ance` nouns, restore plain clauses and verbs.
- **Hedges and boosters:** Remove hedge stacks and diversify repeated `may`. Treat zero boosters as actionable only when the evidence supports confidence and the genre permits an authored stance. Zero is acceptable in neutral reference, encyclopedic, methodology, and genuinely uncertain text.
- **Affect:** Add no emotion. Preserve or clarify only the stance supported by the input, sample, and genre.
- **Rhetorical drama:** Check for staccato runs, aphorism formulas, and a manufactured closer after varying rhythm.
- **Dashes:** With no sample, scan English output for `—` and `–` and replace each. With a sample, match its punctuation. For Russian, follow the RU reference.
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
