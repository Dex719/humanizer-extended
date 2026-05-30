# Humanizer Extended

A skill for Claude Code and OpenCode that removes signs of AI-generated writing from text, making it sound more natural and human.

> **Fork.** `humanizer-extended` is a fork of [blader/humanizer](https://github.com/blader/humanizer) (original by Siqi Chen, MIT). It diverged after upstream 2.5.1 and adds patterns #30–38 (model-tool markup, hallucinated citations, placeholder leakage, document-internal style shift, aphoristic closer, prestige-metaphor frames, false balance, generic stock examples, nominalization) plus a FACT PRESERVATION section. As of 2.15.0 it also re-incorporates three rules from upstream 2.7.0 (#39 diff-anchored writing, the hard em/en dash cut in #14, and speculative gap-filling in #21). Pattern numbers in this fork do **not** match upstream's.

## Installation

### Claude Code

Clone directly into Claude Code's skills directory:

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/Dex719/humanizer-extended.git ~/.claude/skills/humanizer-extended
```

Or copy the skill file manually if you already have this repo cloned:

```bash
mkdir -p ~/.claude/skills/humanizer-extended
cp SKILL.md ~/.claude/skills/humanizer-extended/
```

### OpenCode

Clone directly into OpenCode's skills directory:

```bash
mkdir -p ~/.config/opencode/skills
git clone https://github.com/Dex719/humanizer-extended.git ~/.config/opencode/skills/humanizer-extended
```

Or copy the skill file manually if you already have this repo cloned:

```bash
mkdir -p ~/.config/opencode/skills/humanizer-extended
cp SKILL.md ~/.config/opencode/skills/humanizer-extended/
```

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

To match your personal writing style, provide a sample of your own writing:

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

## 39 Patterns Detected (with Before/After Examples)

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
| 9 | **Negative parallelisms / tailing negations** | "It's not just X, it's Y", "..., no guessing" | State the point directly |
| 10 | **Rule of three** | "innovation, inspiration, and insights" | Use natural number of items |
| 11 | **Synonym cycling** | "protagonist... main character... central figure... hero" | "protagonist" (repeat when clearest) |
| 12 | **False ranges** | "from the Big Bang to dark matter" | List topics directly |
| 13 | **Passive voice / subjectless fragments** | "No configuration file needed" | Name the actor when it helps clarity |
| 38 | **Nominalization overuse** | "the implementation of indexing resulted in optimization of queries" | Turn the abstract noun back into a verb: "indexing made queries faster" |

### Style Patterns

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 14 | **Em/en dashes** | "institutions—not the people—yet this continues—" | Cut them entirely: periods, commas, colons, or parentheses (hard constraint) |
| 15 | **Boldface overuse** | "**OKRs**, **KPIs**, **BMC**" | "OKRs, KPIs, BMC" |
| 16 | **Inline-header lists** | "**Performance:** Performance improved" | Convert to prose |
| 17 | **Title Case Headings** | "Strategic Negotiations And Partnerships" | "Strategic negotiations and partnerships" |
| 18 | **Emojis** | "🚀 Launch Phase: 💡 Key Insight:" | Remove emojis |
| 19 | **Curly quotes** | `said “the project”` | `said “the project”` |
| 26 | **Hyphenated word pairs** | “cross-functional, data-driven, client-facing” | Drop hyphens on common word pairs |
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
| 20 | **Chatbot artifacts** | "I hope this helps! Let me know if..." | Remove entirely |
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
| 24 | **Excessive hedging + booster absence** | "this might suggest that the effect may possibly be real" (after three replications) | Cut hedge stacks; if a paragraph stacked evidence, let it commit ("the effect is real") |
| 25 | **Generic conclusions** | "The future looks bright" | Specific plans or facts |

## Full Example

**Before (AI-sounding):**
> Great question! Here is an essay on this topic. I hope this helps!
>
> AI-assisted coding serves as an enduring testament to the transformative potential of large language models, marking a pivotal moment in the evolution of software development. In today's rapidly evolving technological landscape, these groundbreaking tools—nestled at the intersection of research and practice—are reshaping how engineers ideate, iterate, and deliver, underscoring their vital role in modern workflows.
>
> At its core, the value proposition is clear: streamlining processes, enhancing collaboration, and fostering alignment. It's not just about autocomplete; it's about unlocking creativity at scale, ensuring that organizations can remain agile while delivering seamless, intuitive, and powerful experiences to users. The tool serves as a catalyst. The assistant functions as a partner. The system stands as a foundation for innovation.
>
> Industry observers have noted that adoption has accelerated from hobbyist experiments to enterprise-wide rollouts, from solo developers to cross-functional teams. The technology has been featured in The New York Times, Wired, and The Verge. Additionally, the ability to generate documentation, tests, and refactors showcases how AI can contribute to better outcomes, highlighting the intricate interplay between automation and human judgment.
>
> - 💡 **Speed:** Code generation is significantly faster, reducing friction and empowering developers.
> - 🚀 **Quality:** Output quality has been enhanced through improved training, contributing to higher standards.
> - ✅ **Adoption:** Usage continues to grow, reflecting broader industry trends.
>
> While specific details are limited based on available information, it could potentially be argued that these tools might have some positive effect. Despite challenges typical of emerging technologies—including hallucinations, bias, and accountability—the ecosystem continues to thrive. In order to fully realize this potential, teams must align with best practices.
>
> In conclusion, the future looks bright. Exciting times lie ahead as we continue this journey toward excellence. Let me know if you’d like me to expand on any section!

**After (Humanized):**
> AI coding assistants can speed up the boring parts of the job. They're great at boilerplate: config files and the little glue code you don't want to write. They can also help you sketch a test, but you still have to read it.
>
> The dangerous part is how confident the suggestions look. I've accepted code that compiled and passed lint, then discovered later it missed the point because I stopped paying attention.
>
> If you treat it like autocomplete and review every line, it's useful. If you use it to avoid thinking, it will help you ship bugs faster.
>
> The only real backstop is tests. Without them, you're mostly judging vibes.

## References

- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) - Primary source
- [WikiProject AI Cleanup](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup) - Maintaining organization

## Version History

- **2.15.0** - Merge pass: brought back three rules from the upstream blader/humanizer 2.7.0 line that this fork had diverged from. (1) Added pattern #39 (diff-anchored writing: prose that narrates a change instead of describing the thing as it is). (2) Hardened pattern #14 from "em dash overuse / prefer commas" to a hard cut — the final rewrite must contain zero em or en dashes, with a scan step before returning. (3) Expanded pattern #21 from bare cutoff disclaimers to also cover speculative gap-filling ("maintains a low profile", "likely grew up..."), cross-referencing the fact-preservation rules. Also fixed the stale "29 patterns" header (this fork has documented 38+ since 2.14.0). Total now 39 patterns. Note: this fork's pattern numbers #30-38 differ from upstream's; #39 is upstream's #30 renumbered to avoid collision.
- **2.14.1** - Refined pattern #24 (excessive hedging) to cover the *booster-absence* half of the same asymmetry: AI text over-uses hedges (could, might, potentially, possibly, may suggest) *and* under-uses boosters (clearly, definitely, obviously, in fact, indeed). The fix is not just removing hedges; it is letting the paragraph commit when the evidence has already done the work. Added a second before/after showing booster absence after stacked evidence. Backed by Almulla 2025 and the Hedges-and-Boosters 2024 comparative study, both reporting roughly 2× hedge density and a fraction of the booster density in AI essays.
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
