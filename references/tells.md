# Detection catalog

Every tell, organized by the scoring categories in SKILL.md. Sourced from Wikipedia's *Signs of AI writing* (WikiProject AI Cleanup), which catalogued these across thousands of flagged submissions.

**Contents**
- [How to weigh a tell](#how-to-weigh-a-tell)
- [R. Residue](#r-residue)
- [A. Puffery and inflated significance](#a-puffery-and-inflated-significance)
- [B. Sentence-shape formulas](#b-sentence-shape-formulas)
- [C. Vocabulary and copula avoidance](#c-vocabulary-and-copula-avoidance)
- [D. Formatting and structure](#d-formatting-and-structure)
- [E. Vagueness and weasel attribution](#e-vagueness-and-weasel-attribution)
- [F. Missing human texture](#f-missing-human-texture)
- [Model fingerprints](#model-fingerprints)
- [Weak signals: do not score these alone](#weak-signals-do-not-score-these-alone)

---

## How to weigh a tell

No single sign proves anything. Every pattern here is more common in human writing than in AI writing in absolute terms, because models learned them from humans. What separates machine text is *density and co-occurrence*: many tells, many times, in one short passage.

Take vocabulary literally. A word being overused by models does not make its synonyms suspect. "Underscore" is a tell in the figurative sense, not when it means a literal underline or incidental music. Swapping a flagged word for a fancier synonym makes the text worse, not more human.

---

## R. Residue

Leftover machinery. Near-proof, and it caps the score at 20.

**Markup artifacts**

| Source | Signature |
|---|---|
| ChatGPT | `:contentReference[oaicite:0]{index=0}`, `oai_citation`, `Example+1`, `citeturn0search0` (in Private Use Area Unicode), `turn0image0`, `citeturn0news0`, `({"attribution":{"attributableIndex":"X-Y"}})` |
| Gemini | `[cite: 1]`, `[cite: 3, 12, 13]`, `[span_1](start_span)`, `[span_1](end_span)` |
| Grok | `grok_card` XML tags, `grok_render_citation_card_json` |
| DeepSeek | Lenticular brackets with dagger: `【85†L261-269】` |
| Perplexity | `[attached_file:1]`, `[web:1]`, S3 URLs containing `ppl-ai-file-upload` |
| Unclassified | `:::writing{variant="document" id="12345"}` |

**Tracking parameters appended to source URLs**

`utm_source=openai`, `utm_source=chatgpt.com`, `utm_source=copilot.com`, `referrer=grok.com`. These prove a tool touched the text but not that it wrote the prose, since some writers use models only to find sources.

**Conversational leftovers**

"I hope this helps", "Of course!", "Certainly!", "You're absolutely right!", "Would you like me to", "Is there anything else", "Let me know if", "Here is a", "a more detailed breakdown". Also subject lines pasted above body text, and the model explicitly narrating what the text is for.

**Knowledge-cutoff and gap speculation**

"As of my last knowledge update", "Up to my last training update", "While specific details are limited", "not widely documented", "in the provided sources", "based on available information". The modern RAG version claims information is unavailable, then speculates what it "likely" is. Both the speculation and the claim of unavailability are invented. For people, this surfaces as "maintains a low profile" or "keeps personal details private".

**Placeholders**

Unfilled Mad Libs brackets, `2025-xx-xx` dates, `INSERT_SOURCE_URL`, `SOURCE_PUBLISHER`, "Add [thing] if available with citation".

---

## A. Puffery and inflated significance

The root tell. Models regress to the statistical mean, so specific facts get smoothed into generic praise. The subject ends up simultaneously less specific and more exaggerated: "inventor of the first train-coupling device" becomes "a revolutionary titan of industry".

**Words to watch:** stands as, serves as, is a testament to, is a reminder of, a crucial/pivotal/vital/significant/key role, a crucial/pivotal moment, underscores its importance, highlights its significance, reflects broader, symbolizing its ongoing/enduring/lasting, contributing to the, setting the stage for, marking the, shaping the, represents a shift, marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted, rich heritage, lasting impact, watershed moment.

**Variants**
- Situating the subject inside broader "debates", "discussions", or "conversations"
- Applying grand significance to trivia (etymology, population figures, a product's release date)
- Hedged preambles that concede the subject is minor, then argue its importance anyway
- Promotional and travel-brochure tone: *boasts a, vibrant, rich, profound, enhancing, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking, renowned, featuring, diverse array, state-of-the-art, seamless*
- Press-release register for people and companies

**Superficial analysis via participle tails.** A present participle clause welded to the end of a sentence to add commentary the source never made. Watch for: *highlighting, underscoring, emphasizing, ensuring, reflecting, symbolizing, contributing to, cultivating, fostering, encompassing, enhancing, valuable insights, aligning with, resonating with*.

> As of the 2008 census the population stood at approximately 56,998 inhabitants, **creating a lively community within its borders**.

Cut the comma and everything after it. Nothing is lost, because nothing was there.

**Canned notability.** Listing which outlets covered something as if coverage were the point: *independent coverage, regional media outlets, trade publications, profiled in, written by a leading expert*. Also "maintains an active social media presence", which was rare in human writing before 2024.

---

## B. Sentence-shape formulas

Structural, so they survive vocabulary edits. Rewrite the sentence rather than swapping words.

**Negative parallelism**, in three forms:
1. *Not just X, but also Y* — "Not only a product launch but a statement of intent"
2. *Not X, it's Y* — "It's not about the features, it's about the philosophy". Also the stacked form: "no fluff, no filler, just results"
3. *X rather than Y* — the reversed version, unusually common in Grok output

This is the tell readers consciously notice. It became engagement-bait house style on LinkedIn and X, which makes it worse there, not better.

**Rule of three.** Three parallel adjectives, or three parallel short phrases. Used to make thin analysis look comprehensive. Fix by going to two or four, or by making the three wildly uneven in length so the rhythm breaks.

**False ranges.** "From X to Y" where nothing meaningful sits between the endpoints. "Our services range from strategic planning to implementation support" describes no scale at all.

**Elegant variation.** Repetition-penalty behavior makes models rotate synonyms for the same referent: the protagonist, the key player, the eponymous character, all in one paragraph. Note the confounder: many non-native English speakers were taught to avoid repeating words. Italian schools teach this explicitly.

**Section summaries.** "In summary", "In conclusion", "Overall", plus closing paragraphs that restate what was just said. Mostly a pre-2025 tell but still frequent in long output.

**Didactic asides.** "It's important to note", "It's worth mentioning", "It's crucial to remember", "No discussion would be complete without". Sometimes mandated by RLHF contractors as disclaimer text, so it is baked in rather than incidental.

---

## C. Vocabulary and copula avoidance

**AI vocabulary by era.** Which words co-occur tells you roughly when the text was generated.

- **2023 to mid-2024 (GPT-4):** additionally, boasts, bolstered, crucial, delve, emphasizing, enduring, garner, intricate, intricacies, interplay, key, landscape, meticulous, pivotal, underscore, tapestry, testament, valuable, vibrant
- **Mid-2024 to mid-2025 (GPT-4o):** align with, bolstered, crucial, emphasizing, enhance, enduring, fostering, highlighting, pivotal, showcasing, underscore, vibrant
- **Mid-2025 onward (GPT-5):** emphasizing, enhance, highlighting, showcasing, plus the notability and media-coverage vocabulary in section A
- **Grok, throughout:** causal, empirical, correlate, and still underscore as of 2026

One or two of these means nothing. A short passage carrying eight of them is among the strongest single tells available.

**Copula avoidance.** Models systematically dodge "is" and "are". One study measured a 10%+ drop in both across academic writing in 2023, with no prior trend, and found GPT-3.5 removed them when asked merely to "revise the following sentence".

| Machine | Human |
|---|---|
| serves as, stands as, functions as, operates as, represents, marks | is, was |
| boasts, features, maintains, offers | has |
| refers to (opening a definition) | is |
| ventured into politics as a candidate | was a candidate |
| began his career as | was |

**Stiff synonym preference.** authored (wrote), relocated (moved), utilized (used), attempted (tried), passed away (died), acquired (bought), facilitated (helped), embarked upon (started), possesses (has), demonstrates (shows), leverage (use), garner (get).

---

## D. Formatting and structure

- **Inline-header bold lists.** `- **Scalability**: The system scales easily across use cases.` Marker, bold header, colon, description. This format is close to exclusively machine-generated in prose contexts. Frequently the bold phrase is just restated in the sentence after it, which is a second, independent tell.
- **Title Case In Headings.** Sentence case is the human default outside American journalism.
- **Mechanical boldface.** Every instance of a chosen term bolded, key-takeaways style. Inherited from readmes, listicles, slide decks, and sales pages.
- **Em dashes.** Used more than in nonprofessional human writing of the same genre, in formulaic punched-up ways, and usually spaced, which is against the typographic convention most habitual em dash users follow. Weak alone, and OpenAI has actively suppressed them since GPT-5.1, so absence proves nothing either.
- **Curly quotes and apostrophes.** ChatGPT and DeepSeek default to them, Gemini and Claude typically do not. Heavily confounded by Word smart quotes, macOS and iOS defaults, Chicago style, and citation tools.
- **Emoji as headers or bullet decoration.** Mostly a 2025 tell, rarer now.
- **Skipped heading levels**, starting at H3 rather than H2.
- **Thematic breaks (`---`) before every heading.** A Markdown habit.
- **Unnecessary small tables** for content that reads better as a sentence.
- **The rigid outline.** Overview, then body sections, then "Challenges", then "Future Prospects", then "Conclusion". The Challenges section opens with "Despite its [positive adjective], [subject] faces challenges" and closes with vague optimism. The tell is the formula, not the mention of challenges.
- **Openers.** "In today's [industry]", "Have you ever wondered", "Are you struggling with", "What if I told you". Rhetorical-question stacking generally.

---

## E. Vagueness and weasel attribution

**Words to watch:** industry reports, industry experts, observers have cited, observers have noted, experts argue, some critics argue, studies show, research suggests, several sources, several publications, many believe, it is widely regarded.

**Overgeneralized sourcing.** One or two sources presented as a consensus. "Reviewers" or "scholars" in the plural while citing one person. Lists implied to be non-exhaustive when the source gives no such indication.

**Hallucinated citations.** Real-looking references that do not resolve: invalid ISBN checksums, unresolvable DOIs, DOIs that resolve to unrelated papers, and book citations with no page number or URL. A subtler version has a real book and a real page number, but the cited page does not contain the claim. The flag there is a general or heavily cited book plus no link.

**Fabricated attribution to real people.** Retrieval-enabled models attach analysis to named sources regardless of whether the source said anything close: "Roger Ebert highlighted the lasting influence". Verify any quote or attributed opinion before letting it stand.

---

## F. Missing human texture

Scored on absence. A passage can be free of every tell above and still read as machine-written because it has none of the positive markers. Wikipedia measured these across 25 years of human editing as more common in human text than AI text:

- Simple copulas: "there is a", "it has a"
- Plain verbs where a stiff synonym exists
- Superlatives and definite claims: "one of the best", "is the only", "was the first"
- Hedges and intensifiers: very, perhaps, tends to, mostly, roughly, I think
- Mild wordiness: "as a result of", "in order to", "all of the", "a part of", "the fact that"

That last one is the counterintuitive one. Every style guide tells you to cut those phrases. Cutting all of them is precisely what a model does.

Add to that: uneven sentence length, uneven paragraph length, concrete proper nouns and numbers, digressions, parenthetical asides, opinions, and the occasional slightly odd word choice. Uniform polish is itself the giveaway.

---

## Model fingerprints

Each model has an idiolect. ChatGPT and Grok situate subjects in broader context far more than Gemini and Claude do. Gemini and Claude run more concise; Grokipedia articles are notoriously long. Knowing which model produced a draft helps you predict which era's vocabulary to expect.

---

## Weak signals: do not score these alone

Scoring these produces false positives, which is worse than missing a tell.

- **Perfect grammar.** Plenty of people write well.
- **Mixed casual and formal register.** Indicates technical background, youth, playfulness, neurodivergence, or several authors.
- **"Bland" or "robotic" prose.** Modern models skew effusive and verbose, not sparse. Flat writing is usually just flat writing.
- **Fancy or academic vocabulary.** The correlation is with *specific* overused words, not with formality. Unusual low-frequency words are actually less likely in model output.
- **Transition words in isolation.** Common in essayistic human writing and endorsed by most style guides.
- **Em dashes in isolation.** The most cited tell and one of the weakest. Habitual em dash users are common among strong writers.
- **Markdown alone.** Native to developers, technical writers, and anyone using Obsidian, GitHub, Reddit, Discord, or Slack.
- **The absence of any tell.** Someone who read this list can strip all of it. Absence of tells is not evidence of human authorship.
