# Research, thresholds, and reliability

Read this file when a rewrite needs evidence weighting, a quantitative self-audit, or an explanation of why a pattern matters. Do not treat the measurements below as authorship proof or as quotas that every passage must satisfy.

## Contents

- [How to use the evidence](#how-to-use-the-evidence)
- [Vocabulary drift](#vocabulary-drift)
- [Passive voice, participles, and nominalization](#passive-voice-participles-and-nominalization)
- [Hedges and boosters](#hedges-and-boosters)
- [Sentence and paragraph variation](#sentence-and-paragraph-variation)
- [Transitions](#transitions)
- [Sentiment and stance](#sentiment-and-stance)
- [Non-native English and detector bias](#non-native-english-and-detector-bias)
- [Current-model signatures](#current-model-signatures)
- [Signal ranking](#signal-ranking)
- [Detailed false-positive guards](#detailed-false-positive-guards)
- [Human signals worth preserving](#human-signals-worth-preserving)
- [Reference basis](#reference-basis)

## How to use the evidence

The research notes in the extended fork support editing heuristics, not a binary detector. Use them to prioritize where to read closely:

1. Prefer repeated structural evidence over isolated words or punctuation.
2. Adjust every heuristic for language, genre, length, and a supplied author sample.
3. Use thresholds as prompts for inspection. Do not manufacture a short sentence, long paragraph, booster, or negative emotion merely to hit a number.
4. Never sacrifice fact preservation, completeness, grammar, or authorial voice for a more “human” metric profile.
5. Treat community-observed, model-specific signatures as lower confidence than corpus findings.

## Vocabulary drift

### Kobak et al. (2025)

The fork cites Kobak et al., *Science Advances* (2025), based on 15 million PubMed abstracts, for post-2023 shifts in vocabulary. Reported ratios over the pre-LLM baseline include:

- `delves`: `r = 28.0`
- `underscores`: `r = 13.8`
- `showcasing`: `r = 10.7`

The practical signal is clustering, not mere presence. The operating heuristic in the original extended skill was three or more tier-1 words in one paragraph, or a repeated tier-1 plus tier-2 pair across paragraphs. Every listed word also appears in human prose, so a lone hit should survive unless the sentence improves for another reason.

### Geng and Trotta (2025)

The fork cites Geng and Trotta (2025) for an era effect: conspicuous first-wave words such as `delve`, `tapestry`, `testament`, and `intricate` reportedly fell sharply around April 2024 after public attention made them easy to scrub. Quieter second-wave terms, including `significant`, `potential`, `findings`, and `crucial`, may carry more relative signal in 2025–2026. This makes a static blacklist unreliable; weight contemporary clusters and structure above a single famous word.

## Passive voice, participles, and nominalization

### Reinhart et al. (2025)

The fork cites Reinhart et al., *PNAS* (2025), arXiv `2410.16107`, for structural differences that persist across prompts and registers:

- instruction-tuned models use present-participle clauses at roughly 2–5 times the human rate;
- they use nominalizations at roughly 1.5–2 times the human rate;
- GPT-4o and Llama under-use agentless passive at roughly half the human rate in genres where passive is natural.

The editing implication is not “always use active voice.” In academic and technical methods, forced active voice can itself be a model tell. Russian academic, technical, and business prose likewise makes natural use of passive and impersonal forms. Convert passive only where naming an actor improves ordinary prose.

The original structural self-audit used fewer than about one trailing participial clause per 250 words as a rough inspection point. Treat that as a prompt to reread a dense paragraph, not a universal target.

### Nominalization studies

Pattern 38 also cites:

- Munoz-Ortiz et al. (2024), contrasting news corpora;
- Almulla (2025), measuring engagement markers;
- Reinhart (2024), a corpus study.

Together they motivate checking clusters of abstract action nouns and weak linking verbs. Two or three nominalizations in a paragraph can be normal. A dense run in which the actions disappear into `-tion`, `-ment`, `-ance`, or `-sis` nouns is the operative signal.

## Hedges and boosters

The fork cites Shalevska (2024), using 100 essays per side, and Almulla (2025) for an asymmetric hedge/booster profile:

- AI text used hedges at about `1.39×` the human rate, not the often repeated “twice as many” claim;
- roughly `84%` of AI hedges in the cited corpus were the word *may*;
- *may* occurred at about `4.5` instances per 1,000 tokens;
- the measured AI sample produced zero instances of the tracked boosters `clearly`, `definitely`, `certainly`, and `obviously`, while human writers used them steadily.

The stronger practical tells are concentration and a `may` monopoly. Remove stacked hedges and let well-supported claims become declarative.

Do **not** convert the zero-booster observation into a mandatory booster quota. Add a booster only when the evidence earns confidence and the genre accepts authorial stance. Neutral reference, encyclopedic, methodology, and genuinely uncertain prose can correctly contain zero boosters. A flat declarative can also express justified confidence without a lexical booster.

## Sentence and paragraph variation

### Sentence-length burstiness

The extended skill records a typical human-prose burstiness coefficient, sentence-length standard deviation divided by the mean, of about `0.15–0.45`, while default model output can collapse toward zero. It also notes classifier ablations in which removing sentence-length standard deviation reduced accuracy.

The former operating check asked for one sentence of five words or fewer and one of twenty-five words or more across about five sentences. Use that only to diagnose a long metronomic passage. Applying it as a fixed recipe creates pattern 49: manufactured punchlines and staccato drama. Russian literary and academic prose also tolerates longer multi-clause sentences, so inspect variation without imposing English cutoffs.

### Desaire et al. (2023)

The fork cites Desaire et al., *Cell Reports Physical Science* (2023), for paragraph-level variation:

- paragraph-length variance alone reportedly separated human from ChatGPT text with `AUC = 0.98`;
- a words-per-paragraph standard deviation above `25` read as human in that study, while below `25` read as machine;
- the topic sentence appeared first in more than `94%` of AI paragraphs versus about `73%` of human paragraphs.

These are corpus measurements, not formatting requirements. The editing lesson is to stop padding a minor point to match a major one and to avoid placing every paragraph into the same template.

### Broader structural findings

The fork also cites an iScience corpus study (2026) for tighter clustering around an average length in AI text and unnamed detector-evasion research from 2025 for the conclusion that lexical substitution alone does not erase structural signal.

## Transitions

The Reuters Institute analysis (2024) cited by the fork reports that AI prose uses explicit transitions at about `1.8×` the human baseline, with paragraph-initial `furthermore` and `moreover` at `2–4×` the human rate.

Use this to inspect a connector on nearly every sentence, not to ban ordinary transitions. A rough operational check is at most about one explicit connector per paragraph when juxtaposition already makes the logic clear. Russian shows a similar clustering tendency with `кроме того`, `таким образом`, `следовательно`, `в связи с этим`, and sentence-opening `однако`, but its punctuation and syntax require the RU reference.

## Sentiment and stance

The fork cites an iScience corpus study (2026) for more positive-emotion language, less negative emotion, and higher certainty in AI text. It also cites Abdulhai et al. (2026) for measured shifts when models revise human drafts:

- positive sentiment increased by roughly `37–54%`;
- trust language increased by roughly `17–53%`;
- models produced more fully neutral answers on contested topics.

This supports preserving genuine annoyance, fear, boredom, enthusiasm, mixed feelings, and unresolved tension. It does not justify inventing feelings or forcing negativity into neutral documentation. Genre, input, and a supplied voice sample remain the gate.

## Non-native English and detector bias

Liang et al., *Patterns* (2023), a Stanford study cited by the fork, found severe false positives against TOEFL essays by non-native English writers:

- mainstream GPT detectors flagged about `61%` as AI;
- `97.8%` were flagged by at least one detector.

Low lexical variety, formal grammar, or simple syntax can reflect language background rather than generation. A clean detector score proves nothing, and “make it pass a detector” is the wrong editing target.

## Current-model signatures

The model-specific section combines peer-reviewed work, including Reinhart et al., with community observation from sources such as Reddit and Hacker News. Confidence therefore varies.

- Claude 3.5/4.x: occasional archaic leakage such as `belies`/`bely` and sometimes over-concise phrasing.
- GPT-4o, GPT-5, and Llama: participial overload and forced active voice in technical genres.
- Gemini 1.5/2.x: bullet-list preference and repetitive sentence structure in long-context summaries.
- DeepSeek R1: detached cinematic interjections, heavy bolding, and dramatic escalation.

Use these only as leads after a stronger cluster appears. A single family-associated word or format is not evidence of authorship.

## Signal ranking

### Stronger editing leads

- repeated structural uniformity across sentences and paragraphs;
- dense participial or nominalized constructions;
- over-even connectors;
- abrupt document-internal register, spelling, point-of-view, or formatting shifts;
- leaked model/tool markup;
- placeholder leakage and incoherent citations;
- clustered rhetorical formulas rather than one isolated phrase.

### Weaker, down-weighted signals

- **Em and en dashes:** humans use them often, while some assistants, including Claude and Gemini in the fork's notes, use them sparingly. Apply the English no-sample style rule when required, but do not treat the character as proof.
- **Negative parallelism:** `not X but Y` is established human rhetoric. Edit clusters, not every contrast.
- **Rule of three:** the tricolon predates LLMs and remains ordinary human rhetoric.
- **Curly quotation marks:** Word, Pages, Google Docs, CMS software, and operating systems commonly create them automatically.
- **Hyphenated word pairs:** standard attributive compounds are grammatical. Keep `a high-quality report`; only optional, machine-uniform treatment deserves attention.
- **One common transition or short emphatic sentence:** both are normal. Patterns 42 and 49 require repetition or staging.

## Detailed false-positive guards

Do not flag these on their own:

- perfect grammar or consistent professional editing;
- a mix of casual and formal registers, which can reflect field, age, culture, or neurodivergent prose habits;
- bland or dry prose without specific AI tells;
- formal or academic vocabulary outside the listed clusters;
- a letter-style salutation or sign-off in genuine correspondence;
- one `additionally`, `moreover`, `consequently`, or `however`;
- curly quotes or an em dash supplied by an editor or platform;
- one short sentence used for real emphasis;
- ordinary mid-sentence `honestly` or `look`;
- an unsourced claim by itself;
- clean, complex formatting produced by a template or visual editor;
- watched wording inside secondhand text.

**Secondhand-text guard:** do not rewrite a watched phrase when it appears inside a quotation, title, proper name, citation, source excerpt, code sample, or example where the phrase is being discussed rather than asserted. First determine whether the user's task includes editing the quoted material. This guard applies to all 51 patterns.

When uncertain, inspect clusters. An em dash plus a repeated rule of three, prestige metaphors, promotional language, and a formulaic conclusion is meaningful in a way that one dash is not.

## Human signals worth preserving

- Specific, unusual, hard-to-fabricate details: real addresses, odd quotations, and relationships too particular to be stock.
- Mixed feelings and unresolved tension that do not collapse into a neat take.
- Dated slang, memes, and in-jokes tied to an era or subculture.
- First-person editorial choices the author can defend.
- Natural variation in sentence and paragraph length.
- Genuine asides, parentheticals, and self-corrections.
- Text demonstrably written or edited before ChatGPT's public launch on November 30, 2022, except for rare later interpolation.

## Reference basis

The taxonomy originates with [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup. The extended fork summarizes additional corpus and community findings named above. Its core statistical insight is that an LLM predicts likely continuations, so unsupported generic language and overly even structures can emerge more often than the idiosyncratic choices of a particular writer.
