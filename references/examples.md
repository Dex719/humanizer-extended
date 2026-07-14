# Expanded pattern guidance and examples

Read this file when a compact registry entry in `SKILL.md` is not enough, when a phrase may be a false positive, or when a before/after example would help. For Russian patterns 44–46, read `patterns-ru.md` instead.

## Contents

- [Voice and personality](#voice-and-personality-genre-gated)
- [Content patterns (1–6)](#content-patterns)
- [Language and grammar patterns (7–13)](#language-and-grammar-patterns)
- [Style patterns (14–19)](#style-patterns)
- [Communication patterns (20–22)](#communication-patterns)
- [Filler and hedging (23–29)](#filler-and-hedging)
- [Sourcing, artifact, and advanced rhetorical tells (30–39)](#sourcing-artifact-and-advanced-rhetorical-tells)
- [Structural and statistical tells (40–43)](#structural-and-statistical-tells)
- [Current-model and contextual tells (47–48)](#current-model-and-contextual-tells-2024-to-2026)
- [New upstream-synchronized patterns (49–51)](#new-upstream-synchronized-patterns)
- [Full Example](#full-example)

The examples illustrate transformations; they are not permission to import their details into user text. Apply every rewrite under the fact-preservation rules in `SKILL.md`.

## Voice and personality (genre-gated)

Apply these techniques only when the content and the author's voice call for them: personal blogs, essays, opinion, reviews, and similar voice-led work. Neutral reference, encyclopedic, technical, legal, and methodology prose can be plain without being soulless.

**Signs of an unnecessarily flat voice:** every sentence shares one shape; the prose avoids uncertainty or mixed feelings already present in the source; a suitable first-person perspective has been stripped; genuine humor, edge, asides, or verbal habits from the author's sample have disappeared.

**How to restore voice without fabrication:**

- Preserve opinions and reactions already present in the input or voice sample; do not invent a new attitude.
- Vary rhythm naturally rather than alternating sentence lengths by formula.
- Keep genuine complexity and unresolved tension instead of manufacturing a clean take.
- Use `I` only when the authorial context supports it.
- Preserve real tangents, asides, and self-corrections when they fit the genre.
- Replace generic affect with the specific feeling the author actually supplied. If none was supplied, do not add one.

**Before (flat but factually complete):**
> The experiment produced interesting results. The agents generated 3 million lines of code. Some developers were impressed while others were skeptical. The implications remain unclear.

**After (voice-led only if the author's sample supports this stance):**
> The agents generated 3 million lines of code. The result is interesting, and developers did not agree on what to make of it: some were impressed, while others were skeptical. Its implications are still unclear.

The rewrite changes rhythm and keeps the tension, but adds no sleeping humans, community reaction, personal feeling, or other scene absent from the input.

## CONTENT PATTERNS

### 1. Undue Emphasis on Significance, Legacy, and Broader Trends

**Words to watch:** stands/serves as, is a testament/reminder, a vital/significant/crucial/pivotal/key role/moment, underscores/highlights its importance/significance, reflects broader, symbolizing its ongoing/enduring/lasting, contributing to the, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted

**Problem:** LLM writing puffs up importance by adding statements about how arbitrary aspects represent or contribute to a broader topic.

**Before:**
> The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain. This initiative was part of a broader movement across Spain to decentralize administrative functions and enhance regional governance.

**After:**
> The Statistical Institute of Catalonia was established in 1989. The text links its establishment to decentralization and regional governance in Spain, but gives no details that support the broader claim.


### 2. Undue Emphasis on Notability and Media Coverage

**Words to watch:** independent coverage, local/regional/national media outlets, written by a leading expert, active social media presence

**Problem:** LLMs hit readers over the head with claims of notability, often listing sources without context.

**Before:**
> Her views have been cited in The New York Times, BBC, Financial Times, and The Hindu. She maintains an active social media presence with over 500,000 followers.

**After:**
> Her views have been cited by The New York Times, BBC, Financial Times, and The Hindu, and she has over 500,000 social-media followers. The input does not say which views were cited or what either list establishes.


### 3. Superficial Analyses with -ing Endings

**Words to watch:** highlighting/underscoring/emphasizing..., ensuring..., reflecting/symbolizing..., contributing to..., cultivating/fostering..., encompassing..., showcasing...

**Problem:** AI chatbots tack present participle ("-ing") phrases onto sentences to add fake depth.

**Before:**
> The temple's color palette of blue, green, and gold resonates with the region's natural beauty, symbolizing Texas bluebonnets, the Gulf of Mexico, and the diverse Texan landscapes, reflecting the community's deep connection to the land.

**After:**
> The temple uses blue, green, and gold. The text associates the colors with Texas bluebonnets, the Gulf of Mexico, and other Texan landscapes, and says they reflect the community's connection to the land.


### 4. Promotional and Advertisement-like Language

**Words to watch:** boasts a, vibrant, rich (figurative), profound, enhancing its, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking (figurative), renowned, breathtaking, must-visit, stunning

**Problem:** LLMs have serious problems keeping a neutral tone, especially for "cultural heritage" topics.

**Before:**
> Nestled within the breathtaking region of Gonder in Ethiopia, Alamata Raya Kobo stands as a vibrant town with a rich cultural heritage and stunning natural beauty.

**After:**
> Alamata Raya Kobo is a town in the Gonder region of Ethiopia. The description calls its cultural heritage rich and its natural setting beautiful, but gives no supporting detail.


### 5. Vague Attributions and Weasel Words

**Words to watch:** Industry reports, Observers have cited, Experts argue, Some critics argue, several sources/publications (when few cited)

**Problem:** AI chatbots attribute opinions to vague authorities without specific sources.

**Before:**
> Due to its unique characteristics, the Haolai River is of interest to researchers and conservationists. Experts believe it plays a crucial role in the regional ecosystem.

**After:**
> The Haolai River is of interest to researchers and conservationists. Its role in the regional ecosystem has not been well documented.

**Do not invent sources.** If the user supplied an actual verified reference, preserve its attribution verbatim. Otherwise drop the claim, hedge it honestly, or mark it `[citation needed]`. Do not create a sample institution, study, or year merely to illustrate specificity. Promoting a weasel word into a fake citation is worse than leaving “experts believe.” See pattern 31.


### 6. Outline-like "Challenges and Future Prospects" Sections

**Words to watch:** Despite its... faces several challenges..., Despite these challenges, Challenges and Legacy, Future Outlook

**Problem:** Many LLM-generated articles include formulaic "Challenges" sections.

**Before:**
> Despite its industrial prosperity, Korattur faces challenges typical of urban areas, including traffic congestion and water scarcity. Despite these challenges, with its strategic location and ongoing initiatives, Korattur continues to thrive as an integral part of Chennai's growth.

**After:**
> Korattur has traffic congestion and water scarcity. The input also claims that its location and unspecified initiatives support continued growth, but gives no details.


## LANGUAGE AND GRAMMAR PATTERNS

### 7. Overused "AI Vocabulary" Words

**High-frequency AI words (tier 1, the dead giveaways):** Actually, additionally, align with, alignment, commendable, crucial, delve, delving, elevate, emphasizing, empower, enduring, enhance, fostering, garner, garnered, highlight (verb), holistic, interplay, intricate/intricacies, key (adjective), landscape (abstract noun), leverage, meticulous/meticulously, navigate (figurative), nuanced, paramount, pivotal, realm, resonate, robust, seamless, showcase, showcases, showcasing, straightforward, surpass, swiftly, tapestry (abstract noun), testament, underscore, underscores, underscoring, unwavering, valuable, vibrant

**Tier 2, common but weaker on their own:** beacon, bolster, bolstering, comprehensive, delineate, discerning, dynamic, elucidate, exemplify, foster, groundbreaking, harness, imperative, noteworthy, notable, notably, odyssey, paradigm, profound, profoundly, quintessential, revolutionize, stalwart, synergy, transformative, unparalleled, whilst

**Problem:** These words become useful tells when they cluster: roughly three or more tier-1 words in one paragraph, or a tier-1 plus tier-2 pair repeated across paragraphs. A single occurrence proves nothing, and static blacklists age quickly. Fix the cluster without creating a dialect that conspicuously avoids normal English. Read `research.md` for the PubMed ratios and vocabulary-era findings.

**Before:**
> Additionally, a distinctive feature of Somali cuisine is the incorporation of camel meat. An enduring testament to Italian colonial influence is the widespread adoption of pasta in the local culinary landscape, showcasing how these dishes have integrated into the traditional diet.

**After:**
> Somali cuisine includes camel meat and pasta. The text describes pasta's adoption as an Italian colonial influence and says both foods have become part of the traditional diet.


### 8. Avoidance of "is"/"are" (Copula Avoidance)

**Words to watch:** serves as/stands as/marks/represents [a], boasts/features/offers [a]

**Problem:** LLMs substitute elaborate constructions for simple copulas.

**Before:**
> Gallery 825 serves as LAAA's exhibition space for contemporary art. The gallery features four separate spaces and boasts over 3,000 square feet.

**After:**
> Gallery 825 is LAAA's exhibition space for contemporary art. It has four spaces totaling over 3,000 square feet.


### 9. Negative Parallelisms and Tailing Negations

**Problem:** Constructions like "Not only...but..." or "It's not just about..., it's..." are overused. So are clipped tailing-negation fragments such as "no guessing" or "no wasted motion" tacked onto the end of a sentence instead of written as a real clause.

**Before:**
> It's not just about the beat riding under the vocals; it's part of the aggression and atmosphere. It's not merely a song, it's a statement.

**After:**
> The heavy beat adds to the aggressive tone.

**Before (tailing negation):**
> The options come from the selected item, no guessing.

**After:**
> The options come from the selected item without forcing the user to guess.


### 10. Rule of Three Overuse

**Problem:** LLMs force ideas into groups of three to appear comprehensive.

**Before:**
> The event features keynote sessions, panel discussions, and networking opportunities. Attendees can expect innovation, inspiration, and industry insights.

**After:**
> The event includes talks and panels. There's also time for informal networking between sessions.


### 11. Elegant Variation (Synonym Cycling)

**Problem:** AI has repetition-penalty code causing excessive synonym substitution.

**Before:**
> The protagonist faces many challenges. The main character must overcome obstacles. The central figure eventually triumphs. The hero returns home.

**After:**
> The protagonist faces many challenges but eventually triumphs and returns home.


### 12. False Ranges

**Problem:** LLMs use "from X to Y" constructions where X and Y aren't on a meaningful scale.

**Before:**
> Our journey through the universe has taken us from the singularity of the Big Bang to the grand cosmic web, from the birth and death of stars to the enigmatic dance of dark matter.

**After:**
> The passage covers the Big Bang, the cosmic web, the birth and death of stars, and dark matter.


### 13. Passive Voice and Subjectless Fragments

**Problem:** LLMs often hide the actor or drop the subject entirely with lines like "No configuration file needed" or "The results are preserved automatically." Rewrite these when active voice makes the sentence clearer and more direct.

**Caveat (genre and language):** This rule cuts the other way in academic and technical writing, where agentless passive can be the human norm. Forcing active voice into a methods section (`we fitted the model` instead of `the model was fitted`) can itself be a tell. Russian also makes natural use of impersonal and passive constructions. Convert passive only where it improves clarity in the applicable genre; read `research.md` for the corpus evidence.

**Before:**
> No configuration file needed. The results are preserved automatically.

**After:**
> You do not need a configuration file. The system preserves the results automatically.


## STYLE PATTERNS

### 14. Em Dashes (and En Dashes): Cut Them Unless Voice Calibration Overrides

**Rule:** For English output without a user writing sample, the final rewrite contains no em dashes (`—`) or en dashes (`–`). Replace each with a period, comma, colon, parentheses, or a recast sentence. Also catch spaced dashes and double hyphens used as dashes.

Voice calibration has priority over this generic rule. If the supplied sample systematically uses em or en dashes, preserve that habit at a comparable frequency instead of applying a zero-dash cut. The hard cut applies only when there is no sample. For Russian, read `patterns-ru.md`: grammatical тире remain valid and the target is never zero.

**Before (English, no sample):**
> The term is primarily promoted by Dutch institutions—not by the people themselves. You don't say "Netherlands, Europe" as an address—yet this mislabeling continues—even in official documents.

**After:**
> The term is primarily promoted by Dutch institutions, not by the people themselves. You don't say "Netherlands, Europe" as an address, yet this mislabeling continues in official documents.

**Before (spaced dash and double hyphen):**
> The new policy — announced without warning — affects thousands of workers. The changes -- long overdue according to critics -- will take effect immediately.

**After:**
> The new policy, announced without warning, affects thousands of workers. The changes, long overdue according to critics, will take effect immediately.

Before returning English output with no sample, scan for `—` and `–`. With a sample, compare punctuation against the sample rather than forcing zero.

### 15. Overuse of Boldface

**Problem:** AI chatbots emphasize phrases in boldface mechanically.

**Before:**
> It blends **OKRs (Objectives and Key Results)**, **KPIs (Key Performance Indicators)**, and visual strategy tools such as the **Business Model Canvas (BMC)** and **Balanced Scorecard (BSC)**.

**After:**
> It blends OKRs, KPIs, and visual strategy tools like the Business Model Canvas and Balanced Scorecard.


### 16. Inline-Header Vertical Lists

**Problem:** AI outputs lists where items start with bolded headers followed by colons.

**Before:**
> - **User Experience:** The user experience has been significantly improved with a new interface.
> - **Performance:** Performance has been enhanced through optimized algorithms.
> - **Security:** Security has been strengthened with end-to-end encryption.

**After:**
> The update improves the interface, speeds up load times through optimized algorithms, and adds end-to-end encryption.


### 17. Title Case in Headings

**Problem:** AI chatbots capitalize all main words in headings.

**Before:**
> ## Strategic Negotiations And Global Partnerships

**After:**
> ## Strategic negotiations and global partnerships


### 18. Emojis

**Problem:** AI chatbots often decorate headings or bullet points with emojis.

**Before:**
> 🚀 **Launch Phase:** The product launches in Q3
> 💡 **Key Insight:** Users prefer simplicity
> ✅ **Next Steps:** Schedule follow-up meeting

**After:**
> The product launches in Q3. User research showed a preference for simplicity. Next step: schedule a follow-up meeting.


### 19. Curly Quotation Marks

**Problem:** ChatGPT uses curly quotes (“...”) instead of straight quotes ("...").

**Before:**
> He said “the project is on track” but others disagreed.

**After:**
> He said "the project is on track" but others disagreed.


## COMMUNICATION PATTERNS

### 20. Collaborative Communication Artifacts

**Words to watch:** I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like..., Want me to...?, Want me to give examples?, Should I continue?, let me know, here is a...

**Problem:** Text meant as chatbot correspondence gets pasted as content. Offer-to-continue closers are part of the artifact even when the rest of the answer is clean.

**Before:**
> Here is an overview of the French Revolution. I hope this helps! Let me know if you'd like me to expand on any section. Want me to give examples?

**After:**
> (Remove the chatbot wrapper. This fragment contains no overview to return, so do not invent one.)

### 21. Knowledge-Cutoff Disclaimers and Speculative Gap-Filling

**Words to watch:** as of [date], Up to my last training update, While specific details are limited/scarce..., based on available information, not publicly available, maintains a low profile, keeps personal details private, prefers to stay out of the spotlight, likely [grew up/studied/began], it is believed that

**Problem:** Two related tells. (a) Older models leave hard knowledge-cutoff disclaimers in the text. (b) When a model can't find a source, it writes a paragraph *about* not finding one and then invents plausible filler to cover the gap. For a private person the guess almost always lands on the same stock phrases ("maintains a low profile," "keeps personal details private"), none of it sourced. Say what isn't known, or cut the sentence; don't dress a guess up as fact. See also patterns 31 (hallucinated citations) and the FACT PRESERVATION rules below.

**Before (cutoff disclaimer):**
> While specific details about the company's founding are not extensively documented in readily available sources, it appears to have been established sometime in the 1990s.

**After:**
> The company's founding date is not well documented in the available sources; it appears to have been established sometime in the 1990s.

**Before (speculative gap-fill):**
> Information about her early life is not publicly available, suggesting she maintains a low profile and keeps personal details private. She likely grew up in a middle-class household, which shaped her later interest in education reform.

**After:**
> Her early life is not documented in the available sources. (Or omit the section.)


### 22. Sycophantic/Servile Tone

**Problem:** Overly positive, people-pleasing language.

**Before:**
> Great question! You're absolutely right that this is a complex topic. That's an excellent point about the economic factors.

**After:**
> The economic factors you mentioned are relevant here.


## FILLER AND HEDGING

### 23. Filler Phrases

**Before → After:**
- "In order to achieve this goal" → "To achieve this"
- "Due to the fact that it was raining" → "Because it was raining"
- "At this point in time" → "Now"
- "In the event that you need help" → "If you need help"
- "The system has the ability to process" → "The system can process"
- "It is important to note that the data shows" → "The data shows"


### 24. Excessive Hedging and Genre-Gated Booster Absence

**Problem:** LLMs can over-use hedges (`could`, `might`, `potentially`, `possibly`, `perhaps`, `it could be argued that`, `this may suggest`) and under-use confident declaratives or boosters. The cumulative tell is a paragraph that stacks evidence and then refuses to say what it supports. The empirical rationale and measured ratios are collected in `research.md`.

**Before:**
> It could potentially possibly be argued that the policy might have some effect on outcomes.

**After:**
> The policy may affect outcomes.

**Before (hedging after supplied evidence):**
> Three independent replications recovered the same coefficient. The result might suggest that the effect is real, though it could potentially be explained by other factors that may not have been controlled for.

**After (voice-led analytical prose):**
> Three independent replications recovered the same coefficient. The effect is real. Whether the proposed mechanism explains it is a separate question. The controls are not tight enough to rule out a confound.

**Rule:** Cut hedge stacks and vary or remove a repeated `may`. Add a booster such as `clearly`, `definitely`, `in fact`, or a flat unhedged declarative only where the supplied evidence earns confidence **and** the genre permits authorial stance. This is a recommendation, not a quota. Do not force boosters into neutral reference, encyclopedic text, methodology, or a piece that is genuinely uncertain throughout. In those genres, zero boosters is normal. Never manufacture evidence to justify confidence.

### 25. Generic Positive Conclusions

**Problem:** Vague upbeat endings.

**Before:**
> The future looks bright for the company. Exciting times lie ahead as they continue their journey toward excellence. This represents a major step in the right direction.

**After:**
> (This fragment supplies no concrete future event. End on the last supported fact from the preceding text instead of inventing a positive forecast.)


### 26. Hyphenated Word Pair Overuse

**Words to watch:** third-party, cross-functional, client-facing, data-driven, decision-making, well-known, high-quality, real-time, long-term, end-to-end

**Problem:** Machine writing may hyphenate optional pairs with perfect consistency, including predicate uses. Hyphenation alone is a weak signal, and standard compound modifiers before a noun must remain grammatical.

**Before:**
> The cross-functional team delivered a high-quality, data-driven report. The team is cross-functional, the report is high-quality, and the methodology is data-driven.

**After:**
> The cross-functional team delivered a high-quality, data-driven report. The team is cross functional, the report is high quality, and the methodology is data driven.

**Rule:** Keep required or conventional attributive hyphens (`a high-quality report`, `a data-driven method`). Normally drop the hyphen when the compound follows the noun (`the report is high quality`) unless the dictionary, domain style, or author's sample requires it. Vary only genuinely optional forms; never dehyphenate every attributive compound to simulate inconsistency. Down-weight this pattern under reliability guidance.

### 27. Persuasive Authority Tropes

**Phrases to watch:** The real question is, at its core, in reality, what really matters, fundamentally, the deeper issue, the heart of the matter

**Problem:** LLMs use these phrases to pretend they are cutting through noise to some deeper truth, when the sentence that follows usually just restates an ordinary point with extra ceremony.

**Before:**
> The real question is whether teams can adapt. At its core, what really matters is organizational readiness.

**After:**
> The question is whether teams can adapt. That mostly depends on whether the organization is ready to change its habits.


### 28. Signposting and Announcements

**Phrases to watch:** Let's dive in, let's explore, let's break this down, here's what you need to know, now let's look at, without further ado

**Problem:** LLMs announce what they are about to do instead of doing it. This meta-commentary slows the writing down and gives it a tutorial-script feel.

**Before:**
> Let's dive into how caching works in Next.js. Here's what you need to know.

**After:**
> (Delete the announcement and begin with the user's supplied explanation of Next.js caching. This fragment contains no explanation to rewrite.)


### 29. Fragmented Headers

**Signs to watch:** A heading followed by a one-line paragraph that simply restates the heading before the real content begins.

**Problem:** LLMs often add a generic sentence after a heading as a rhetorical warm-up. It usually adds nothing and makes the prose feel padded.

**Before:**
> ## Performance
>
> Speed matters.
>
> When users hit a slow page, they leave.

**After:**
> ## Performance
>
> When users hit a slow page, they leave.


## SOURCING, ARTIFACT, AND ADVANCED RHETORICAL TELLS

### 30. Model-Tool Markup Artifacts

**Signs to watch:** `:contentReference[oaicite:N]{index=N}`, `oai_citation`, `contentReference`, `+1` as a trailing citation marker (all ChatGPT); `[attached_file:N]`, `[web:N]` (Perplexity); `<grok-card data-id="...">` (Grok); JSON tails such as `({"attribution":{"attributableIndex":"X-Y"}})`; `turn0search0`-style tags; URLs ending in `?utm_source=chatgpt.com`.

**Problem:** Chatbot UIs wrap reference and tool-use information in hidden markup that some models occasionally emit into the response body. Users then paste the response verbatim and the artifacts ship with it. They are never intentional and always unambiguous tells.

**Before:**
> Philip Morris' reputation management later became controversial, with effects still debated in contemporary regulatory discussions.[attached_file:1] The 2008 settlement[oaicite:3]{index=3} further limited advertising:contentReference[oaicite:4]{index=4}.

**After:**
> Philip Morris' reputation management later became controversial, and effects are still debated in contemporary regulatory discussions. The 2008 settlement further limited advertising.

**Rule:** Delete the artifact, including any surrounding brackets, backslashes, or whitespace it leaves behind. Strip `?utm_source=chatgpt.com` from URLs. If the artifact was standing in for a real citation, either supply the actual source or remove the claim. Never keep the tag.


### 31. Hallucinated Citations

**Signs to watch:** DOIs that look valid but resolve to unrelated articles or 404; book citations missing page numbers, publishers, or ISBNs; clusters of references where every entry is from a high-prestige journal (Nature, Science, Cell) when the topic would not plausibly draw from only those venues; "According to a [year] study by [institution/department]" with no author or title; round years with no month/issue for publications that normally carry them; non-existent URLs not present in the Internet Archive.

**Problem:** LLMs generate citations that look correct but do not exist. A fabricated reference is more dangerous than a vague one, because it looks verifiable until someone actually clicks it. Humanizing "experts believe X" by promoting it into "according to a 2019 survey by the Chinese Academy of Sciences" is the exact failure mode that earns LLM-edited articles deletion on Wikipedia. Fix *down*, not *up*.

**Before:**
> Recent research has shown that the mineral exhibits unusual magnetic properties.

**After (no verified source):**
> The mineral may exhibit unusual magnetic properties. `[citation needed]`

**After (a verified source was supplied by the user):**
> Keep the user's verified citation verbatim. Do not synthesize a sample author, journal, year, or page range.

**Rule:**
- Never invent authors, institutions, journal names, DOIs, ISBNs, page numbers, or dates to make a claim sound sourced.
- If the input already contains citations, treat them as suspect: check that the author, journal, and year form a coherent real reference before letting them through.
- When in doubt, hedge the claim or drop it. Flag with `[citation needed]` rather than fabricate.
- Removing AI-isms is the job; adding false precision is not.


### 32. Placeholder and Template Leakage

**Signs to watch:** `[Your Name]`, `[Recipient]`, `[INSERT URL]`, `[Replace with X]`, `[TODO: …]`, `[PLACEHOLDER]`, `<ADD SECTION HERE>`, `{{variable}}`, `2025-XX-XX`, `$[amount]`, `[Link to source]`, bracketed instructions to the reader such as `[Describe the specific section and provide clear reasons …]`, and HTML-comment fillers like `<!-- add paragraph here -->`. Also: code-block placeholders (`example.com`, `user@example.com`, `YOUR_API_KEY`) that escaped into prose.

**Problem:** When asked for generic outputs (emails, pitches, bios, cover letters, Wikipedia edit requests), LLMs emit fill-in-the-blank templates. The user is expected to fill in the blanks; many paste the template verbatim instead. A placeholder shipping alongside real prose is an unmistakable tell.

**Before:**
> Hi [Recipient],
>
> I hope this message finds you well. I am writing to request an edit for the Wikipedia entry on [Topic]. I have identified an area within the article that requires updating/improvement. [Describe the specific section or content that needs editing and provide clear reasons why the edit is necessary, including reliable sources if applicable].
>
> Best regards,
> [Your Name]

**After:**
> (The skill cannot invent the sender's identity, the article, or the edit rationale. Stop and flag back to the user:)
>
> This draft still contains unfilled placeholders: `[Recipient]`, `[Topic]`, `[Describe the specific section…]`, `[Your Name]`. Please fill them in before sending. I will not invent defaults.

**Rule:** Never silently fill in a placeholder with a plausible-sounding guess ("John Smith", "artificial intelligence", "example.com"). Placeholder text means the user owes the text context the skill does not have. Flag the placeholders back; refuse to ship the document until they are filled in or explicitly dropped. Treat lingering `XXXX`/`TBD`/`YYYY-MM-DD`-style fillers the same way.


### 33. Document-Internal Style Shift

**Signs to watch:** Sudden register change mid-document (academic → casual or vice versa); tense shift; British ↔ American spelling within the same section (`organisation` next to `color`); point-of-view change (`we` → `you` → `one`); citation-style switch halfway; mixed date formats (`Sept. 15` alongside `September 15th`); abrupt change in paragraph length or list density; one section heavy on tier-1 AI vocabulary while the next uses plain language.

**Problem:** When an LLM regenerates or splices sections, it does not always carry style consistently. A single author writing one document tends to stay in one voice. A hard style shift mid-document is one of the strongest structural tells, especially when the preceding paragraph was AI-typical and the new one is not (or vice versa). It also makes the document obviously stitched.

**Before:**
> The Second Punic War transformed Roman military doctrine, reshaping tactics and infrastructure across the republic. Several historians have delved into its enduring legacy in the later expansion.
>
> So basically, after Cannae, Rome just kept drafting guys until Hannibal ran out of steam. Pretty nuts honestly.

**After:**
> The Second Punic War reshaped Roman military doctrine, tactics, and infrastructure. Historians have traced its effect on the later expansion of the republic.
>
> After Cannae, Rome continued conscripting soldiers until Hannibal could no longer sustain the campaign.

**Rule:** Pick one register, tense, spelling convention, and point of view and enforce it across the whole document. If two halves of the input are clearly in different styles, ask the user which one to match rather than silently averaging them. Do not fix one paragraph to the new voice and leave the other in the old voice.


### 34. Aphoristic Closer

**Signs to watch:** Final sentence reads like a tweet-ready mantra, promises "the beginning of something bigger", or compresses the thesis into a rhyming/antithetical epigram. Two flavours, both the same trick:

*Formal/elevated epigrams.* "In the end, it's not X — it's Y.", "And that — that is the real story.", "This isn't just X. It's Y.", "The future belongs to [group].", "And that changes everything.", "X is the new Y.", "X is more than Y. It's Z."

*Folksy analogy closers.* The same compression done as a "down-to-earth" comparison instead of a high-style maxim. "Worrying about X is basically like worrying about Y.", "It's like trying to Z with one hand tied.", "X is just Y wearing a hat.", "Бояться X примерно как бояться Y", "Это как пытаться Z." A street-level register doesn't make the move different; the function, closing on a quotable comparison instead of a fact, is identical.

**Problem:** LLMs habitually end essays with a punchline that sounds conclusive but carries no information. It imitates the aesthetic *shape* of a strong ending (short, quotable, paradoxical) without doing the work. The folksy variant is more dangerous than the formal one because it disguises itself as "voice": a chatty analogy reads as human texture, but the structural beat (and its emptiness) is the same. Readers who can feel the essay ending recognize it either way.

**Before (formal):**
> Developers who pair with these tools ship faster, learn more, and collaborate better. And in the end — that's what great software has always been about: not the code, but the craft.

**After (formal):**
> Developers who pair with these tools are said to ship faster, learn more, and collaborate better. The input provides no evidence for those claims.

**Before (folksy):**
> Fat is not a cosmetic defect or a health threat. It's working material the body uses to build membranes, hormones and nerve tissue. Worrying about dietary fat is basically like worrying about bricks on a construction site.

**After (folksy):**
> Fat is working material the body uses to build membranes, hormones, and nerve tissue. Treating all dietary fat as a cosmetic defect or a health threat ignores that stated function.

**Rule:** Cut closing sentences whose content reduces to "X is actually Y", "this changes everything", "the future belongs to Z", *or* "X is basically like Y / X is like Y-ing Z." Register doesn't matter: formal maxim and folksy analogy are the same shape. Either let the final paragraph end on a concrete fact or a specific call, or stop one sentence earlier. An epigram is not an ending; it is decoration over the absence of one.


### 35. Prestige-Metaphor Nouns Used as Frames

**Signs to watch:** `tapestry`, `mosaic`, `symphony`, `orchestra`, `labyrinth`, `beacon`, `odyssey`, `quilt`, `kaleidoscope`, `crucible`, `constellation`, `fabric`, `thread`, `journey` (figurative), `landscape` (non-geographic), but only when they appear as the *organizing frame* of a sentence or paragraph, not as a single decorative word.

**Problem:** Pattern 7 lists most of these nouns as AI vocabulary. Pattern 35 is about the *structural* abuse: "the tapestry of X", "the mosaic of Y", "a symphony of Z" used to organize a sentence rather than decorate one, often several stacked in the same passage. A human who reaches for one of these metaphors usually commits to it and extends it. LLMs reach for several, mix them (weaving a tapestry while sailing an odyssey), and never develop any.

**Before:**
> AI coding tools have woven themselves into the tapestry of modern software development, creating a symphony of productivity where each developer becomes part of an intricate orchestra of creation.

**After:**
> AI coding tools are used in modern software development and can improve developer productivity.

**Rule:** Delete mixed metaphors outright. Keep at most one elevated metaphor per piece, and only if it is earned and extended. Never use two of these nouns to describe the same thing. If the content can be stated without metaphor, prefer that.


### 36. False Balance / Artificial Both-Sides

**Signs to watch:** Symmetrical "on the one hand X, on the other hand Y" framing when one side is clearly dominant or correct; "while some believe…, others argue…" that surveys views without taking one; pro/con lists on questions that are not actually contested; closers such as "the truth likely lies somewhere in between" or "both perspectives have merit."

**Problem:** LLMs default to a middle-of-the-road neutrality that sounds responsible but misleads when the evidence is lopsided. Human writers with opinions usually say which side is right and why. Artificial balance is how AI writing avoids making a claim while appearing thoughtful. It also dilutes stakes.

**Before:**
> On the one hand, proponents of regular tire rotation argue it extends tire life. On the other hand, skeptics contend the benefits are overstated. The truth likely lies somewhere in between, and consumers should make their own informed decisions based on their particular circumstances.

**After:**
> Regular tire rotation may extend tire life. Nothing in the input supports giving an unspecified skeptical view equal weight or claiming that the truth lies between the two positions.

**Rule:** Do not manufacture two-sidedness where the evidence is lopsided. If the piece must remain neutral, do not sneak in an opinion, but also do not invent a fake controversy. Cut the "both sides have merit" closer outright.


### 37. Generic Stock Examples

**Signs to watch:** Examples using interchangeable placeholder names (`John`, `Jane`, `Sarah`, `Alice and Bob`, `Company A` vs `Company B`, `Acme Corp`, `WidgetCo`, `Foo` and `Bar`); hypothetical scenarios that carry no specific detail ("imagine a small business owner who…"); examples that would fit any industry interchangeably; the same character archetype recycled across multiple examples in the same piece.

**Problem:** LLM examples sound real but are interchangeable. A human writer either uses a real example with named specifics (case study, company, dated event) or invents a deliberate fiction that is distinct enough to be obviously fiction. "Sarah, a small business owner" is the tell; "the one-person bakery on Pearl Street that closed in 2021" is not. The generic version teaches nothing and has no purpose except filling the example slot.

**Before:**
> For example, imagine Sarah, a small business owner who uses the tool daily. She finds it saves her hours each week, allowing her to focus on what truly matters: her customers.

**After:**
> (No real example was supplied. Cut the paragraph or ask the user for one; do not invent a named case study, date, or statistic.)

**Rule:** Delete placeholder names and generic archetypes. Replace them with a real named example or cut the example. If a hypothetical is genuinely necessary, make it specific enough to be obviously hypothetical, not a placeholder wearing a first name. Do not invent fake case studies or fake statistics to replace "Sarah the small business owner"; see also pattern 31.


### 38. Nominalization Overuse

**Signs to watch:** Sentences front-load abstract nouns derived from verbs, such as "the implementation of", "the realization of", "the consideration of", "the optimization of", "the integration of", "the evaluation of", "the establishment of", "the utilization of", "the determination of", "the development of". Long noun phrases ("a comprehensive examination of the underlying mechanisms") chained with weak linking verbs (`is`, `provides`, `enables`, `facilitates`). Whole paragraphs in which most main verbs are versions of *to be* or *to provide*, while the actual actions sit inside `-tion` / `-ment` / `-ance` / `-sis` nouns.

**Problem:** LLM prose can hide actors and actions inside abstract nouns. In `the implementation of automated testing was conducted by the team`, the action moved into `implementation` and a placeholder verb was added back. This compounds with pattern 13 because the agent can disappear into both a passive construction and a noun. Read `research.md` for the measured corpus differences.

**Before:**
> The optimization of database queries through the implementation of indexing strategies has been demonstrated to result in significant improvements to overall system performance.

**After:**
> Indexing strategies improved database-query performance and the performance of the system overall.

**Before:**
> A thorough evaluation of the proposed framework was conducted, and the determination was made that further refinement of certain components would be beneficial.

**After:**
> The evaluation found that some components of the proposed framework need further refinement.

**Rule:** When a sentence's main verb is `is` / `provides` / `enables` / `facilitates` / `was conducted` / `has been demonstrated`, find the abstract noun that holds the real action and turn it back into a verb. *The implementation of indexing* → *we indexed*. *Conducted an evaluation* → *evaluated*. *The realization of improvements* → *improved*. Then ask whether the agent ("we", "the team", a named person) belongs back in. Two or three nominalisations in a paragraph is normal; six is a tell. Do not chase every `-tion`; the signal, like §7, is *clustering*.


### 39. Diff-Anchored Writing

**Signs to watch:** Prose that narrates a *change* rather than describing the thing as it is: "this function was added to replace…", "we updated X to handle Y", "the new approach improves on the old one", "previously this used Z, now it uses W". Common in documentation, code comments, and README prose that was written by a model summarizing a commit.

**Problem:** Documentation or comments written as if narrating a change rather than describing the thing as it is. Unless the document is inherently version-scoped (changelogs, release notes, migration guides), it should read coherently without knowing what changed in the last commit. A reader six months later has no memory of the "previous approach"; the diff framing is noise to them.

**Before:**
> This function was added to replace the previous approach of iterating through all items, which caused O(n²) performance.

**After:**
> This function avoids the O(n²) performance caused by iterating through all items.

**Rule:** Describe what the thing *does*, not what changed to produce it. Keep diff framing only where the document is explicitly about a transition (changelog, release notes, migration guide, PR description). Everywhere else, strip "added", "updated", "previously", "now", "new" when they only exist to contrast with an unstated prior state.


## STRUCTURAL AND STATISTICAL TELLS

Word lists cannot catch structural tells. Handle patterns 40–43 with a self-audit rather than find-and-replace, and read `research.md` when the quantitative evidence or thresholds matter.

### 40. Sentence-Length Uniformity (Low Burstiness)

**Signs to watch:** Every sentence lands in the same band of roughly 14 to 20 words. No very short sentences, no long winding ones. Read aloud, the rhythm is metronomic.

**Problem:** A long run of similarly sized sentences sounds metronomic. Natural prose often lets one qualified point run long and another land briefly. Diagnose the run without turning variation into a formula; the burstiness measurements are in `research.md`.

**Before:**
> The system processes requests efficiently and returns results quickly. It handles multiple connections at once without significant slowdown. The architecture scales well under load and remains stable during traffic spikes.

**After:**
> The system is fast. Even when many requests arrive at once, it keeps returning results without a significant slowdown and remains stable during traffic spikes.

**Rule:** Vary sentence length when a passage is genuinely metronomic. As a rough diagnostic in longer English prose, look for some sentences outside the twelve-to-twenty-word band, including an occasional sentence of five words or fewer or twenty-five words or more. Do not enforce a quota in every five-sentence block: that creates the manufactured staccato in pattern 49. Russian rhythm follows `patterns-ru.md`.

### 41. Paragraph and Document Symmetry

**Signs to watch:** Every paragraph is about the same length. Every section has the same number of bullets. Lists default to three or five items regardless of content. The whole document is suspiciously balanced.

**Problem:** Near-equal paragraphs and sections can make a document look padded into a template. Human documents are often lopsided because the important point needs more room than the throat-clearing. Read `research.md` for the paragraph-variance and topic-sentence measurements.

**Before:**
> The first option offers strong performance and reasonable cost. The second option offers moderate performance and lower cost. The third option offers weak performance and the lowest cost.

**After:**
> The first option has the strongest performance at a reasonable cost. The second trades some performance for a lower cost; the third has the weakest performance and the lowest cost. Choose according to the performance and cost the task requires.

**Rule:** Let the important part run long and the minor part stay short. Do not pad a thin point to match a fat one. Break the three-bullet and five-bullet reflex; use the number of items the content actually has. The research reference records a words-per-paragraph standard deviation of 25 as a corpus threshold, not a target to manufacture in every document.

### 42. Hyperconnectivity (Over-Even Transitions)

**Signs to watch:** Almost every sentence opens with an explicit connector: furthermore, moreover, additionally, in addition, consequently, as a result, however, that said. The logic is spelled out at every joint.

**Problem:** A formal connector on nearly every sentence reads like a debate transcript. Human prose often lets juxtaposition carry clear logic or uses plain `so` and `because`. Russian shows a related clustering habit, with different syntax; see `patterns-ru.md`. The transition-density measurements are in `research.md`.

**Before:**
> The migration was risky. However, the team prepared thoroughly. Moreover, they ran a full rehearsal. Consequently, the cutover went smoothly. In addition, no data was lost.

**After:**
> The migration was risky, so the team ran a full rehearsal first. The cutover went smoothly and no data was lost.

**Rule:** Drop about half the explicit connectors and let the sentences sit next to each other. Keep one only where the logical turn would genuinely be unclear without it. Aim for at most about one explicit connector per paragraph; one on every sentence is a tell.

### 43. Sentiment and Stance Flatness

**Signs to watch:** Relentless mild positivity. No strong negative emotion, no irritation, no real enthusiasm, no doubt. Every topic gets the same even, agreeable, slightly upbeat treatment.

**Problem:** Relentless mild approval can flatten a real stance. Preserve negative or uncertain affect that the author actually supplied, but do not inject it into neutral genres. Read `research.md` for the sentiment and trust-language measurements.

**Before:**
> The new framework offers many interesting features and a thoughtful design. It provides a smooth developer experience and integrates well with existing tools. Overall it is a solid choice for modern teams.

**After:**
> The framework offers several features and integrates with existing tools. The description calls its design thoughtful and its developer experience smooth, but gives no examples to support either judgment. There is not enough detail here to call it a solid choice for modern teams.

**Rule:** Do not sand every sentiment down to mild approval. If the input or authorial context supplies real irritation, boredom, excitement, or uncertainty and the genre permits stance, let it show. Otherwise question unsupported praise without manufacturing a personal reaction. Flat positivity is a structural lead, not permission to invent feelings or facts; see pattern 36 and the PERSONALITY gate.

## CURRENT-MODEL AND CONTEXTUAL TELLS (2024 to 2026)

The vocabulary and structure tells above are largely model-agnostic. These two are newer and more specific, and their evidence ranges from peer-reviewed work to community observation. Treat them as leads, not proof; read `research.md` for the evidence hierarchy.

### 47. Superficial Guideline Echoing

**Signs to watch:** The text proves it deserves to exist by echoing the rules of the platform it was written for, in the platform's own words: "maintains an active social media presence", "has received independent coverage", "meets notability criteria", or a corporate bio that recites the brief back at you.

**Problem:** Older models hallucinated loud superlatives ("the greatest company in the world"). Newer instruction-tuned models (GPT-4o, Claude 3.5) know the platform wants neutrality and notability, so instead of just writing, they assert that the subject satisfies those criteria, using the rulebook's own vocabulary. It is the model trying to satisfy a latent instruction in front of the reader. This overlaps with pattern 2 (notability name-dropping); 47 is the phrase-level, rule-echoing version.

**Before:**
> The mall maintains an active social media presence, sharing updates that have garnered independent coverage.

**After:**
> The mall posts updates on social media and has received independent coverage. The input does not say what the coverage established.

**Rule:** Strip sentences whose only job is to argue that the subject qualifies. State what the subject actually does, with a concrete fact, and let notability speak for itself.

### 48. Model-Specific Signatures

**Signs to watch:** Tells tied to a particular model family. *Claude (3.5, 4.x):* an affinity for slightly archaic verbs, most notably "belies" / "bely" ("the simplicity belies the complexity"), and occasional over-concise, choppy phrasing. *GPT-4o, GPT-5, Llama:* participial overload and forced active voice in technical genres (see patterns 3, 13, 38). *Gemini (1.5, 2.x):* heavy reliance on bullet lists over flowing prose, and repetitive sentence structure when summarizing long context. *DeepSeek (R1):* detached cinematic interjections in narrative ("Somewhere in the distance, a dog howls"), heavy bolding, and dramatic escalation.

**Problem:** Proprietary fine-tuning leaves family-specific fingerprints. None is proof on its own, but combined with the structural tells they point to a source and to spots worth rewriting. Most of these are community-documented, so weight them low.

**Before (Claude):**
> The clean interface belies a sophisticated engine underneath.

**After:**
> The interface looks simple, but the engine underneath is not.

**Rule:** Watch for the family fingerprint that matches your generator. Replace "belies" and similar archaic leaks with plain verbs, turn Gemini bullet dumps into prose where prose reads better, and cut DeepSeek's stage-direction interjections. Do not treat any single one as conclusive.

## New upstream-synchronized patterns

### 49. Manufactured Punchlines and Staccato Drama

**Problem:** LLMs often make every sentence land like a quotable closer, then stack short declarative fragments to manufacture drama. One short sentence for emphasis is fine; a run of them sounds engineered.

**Before:**
> Then AlphaEvolve arrived. It had no preference for symmetry. No aesthetic prior. No nostalgia for human taste. The old rules were gone.

**After:**
> AlphaEvolve changed the search because it did not favor symmetry or human-looking designs. That made some of the older assumptions less useful.

**Rule:** Join a run of dramatic fragments into ordinary connected prose. Preserve one short sentence when the surrounding rhythm and content earn it. Do not “fix” sentence uniformity by manufacturing a new short-long-short template.

### 50. Aphorism Formulas

**Words to watch:** X is the Y of Z, X becomes a trap, X is not a tool but a mirror, the language of, the currency of, the architecture of

**Problem:** LLMs turn ordinary mid-text claims into reusable aphorisms that sound profound without adding precision. This extends pattern 34, which covers the same move when it is used as a closer.

**Before:**
> Symmetry is the language of trust. Efficiency becomes a trap when teams forget the human layer.

**After:**
> Symmetric layouts often feel more predictable to users. Teams can over-optimize workflows and miss how people actually use them.

**Rule:** Replace the formula with the concrete claim it gestures at. Do not flag a literal, developed metaphor or protected quotation solely because it matches the shape.

### 51. Conversational Rhetorical Openers

**Phrases to watch:** Honestly?, Look, Here's the thing, The thing is, Let's be honest, Real talk, when used as standalone hooks or fake-candid pauses before an ordinary point.

**Problem:** The opener manufactures intimacy through a theatrical pause-and-reveal. The tell is the staging, not the individual word.

**Before:**
> Is it worth the price? Honestly? It depends on how often you'll use it.

**After:**
> Whether it's worth the price depends on how often you'll use it.

**Rule:** State the point directly. Keep ordinary mid-sentence `honestly` or `look`, a genuine conversational voice from the user's sample, and secondhand text.

## Full Example

Every assertion in both rewrites below comes from the `Before` text or is an explicit observation that the input does not support one of its own claims. No person, experience, number, study, quotation, or source has been added.

**Before (AI-sounding input):**
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

**Draft rewrite:**
> AI-assisted coding tools can generate documentation, tests, and refactors. The input frames them as evidence of the transformative potential of large language models, places them between research and practice, and describes them as changing how engineers ideate, iterate, and deliver software. It also calls their role in modern workflows vital. The claimed value extends beyond autocomplete to streamlined work, better collaboration and alignment, more creativity, greater agility, and better user experiences. Those broad claims are not well documented here.
>
> Adoption is said to have expanded from hobbyist experiments to enterprise rollouts and from solo developers to cross-functional teams. No source is supplied for that trend. The text names The New York Times, Wired, and The Verge, but does not say what their coverage established.
>
> The stated benefits are faster code generation with less friction and more developer empowerment, better output and higher standards after improved training, and growing use as part of a broader trend. The input provides no measures for those claims. It says automation can contribute to better outcomes alongside human judgment, although the descriptions of a catalyst, partner, and foundation for innovation add emphasis rather than evidence.
>
> The named challenges are hallucinations, bias, and accountability. The text still says the ecosystem is thriving and recommends best practices, but it does not define those practices or support the claim about the ecosystem. Its optimistic forecast is also unsupported.

**What makes the below so obviously AI generated?**
- The draft repeats `the input` and `the text` so often that the qualification becomes mechanical.
- The paragraphs still march through the source in evenly labeled blocks.
- The final sentence announces a verdict instead of letting the documented limits carry it.

**Now make it not obviously AI generated:**
> AI-assisted coding tools can generate documentation, tests, and refactors. The text treats them as evidence of the transformative potential of large language models, places them between research and practice, and describes them as changing how engineers ideate, iterate, and deliver software. It calls their role in modern workflows vital. The claimed value also extends beyond autocomplete: streamlined work, better collaboration and alignment, more creativity, greater agility, and better user experiences. None of those broader claims is supported with evidence in the input, so they should remain claims rather than conclusions.
>
> The same caution applies to adoption. It is said to have moved from hobbyist experiments to enterprise rollouts and from solo developers to cross-functional teams, but that trend is not well documented here. The New York Times, Wired, and The Verge are named without any explanation of what their coverage showed.
>
> Speed, quality, and usage are all described as improving. Faster code generation is said to reduce friction and empower developers; improved training is said to raise output quality and standards; growing use is presented as part of a broader trend. No measures are provided. The tools are also called a catalyst, partner, and foundation for innovation, but those labels do not establish the claimed gains. What the material does support is narrower: they can produce documentation, tests, and refactors, and the text explicitly links better outcomes to an interplay between automation and human judgment.
>
> Hallucinations, bias, and accountability are the stated challenges. The claims that the ecosystem is thriving, that teams should follow best practices, and that the future is bright remain too vague to assess because the text supplies neither definitions nor evidence.

**Changes made:**
- Removed chatbot framing, offer-to-continue closers, promotional language, inflated significance, decorative formatting, and formulaic rhetoric.
- Preserved every substantive claim, named outlet, capability, benefit, adoption statement, challenge, and recommendation from the input.
- Marked unsupported claims as unsupported instead of replacing them with fabricated studies, people, experiences, numbers, or quotations.
- Kept the final version substantively aligned with the draft while improving rhythm and reducing repetitive meta-language.
