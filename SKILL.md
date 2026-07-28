---
name: anti-ai
description: Score, audit, and aggressively rewrite text so it reads as human-written rather than model-generated. Catches puffery, negative parallelisms ("not just X, it's Y"), rule-of-three lists, present-participle significance tails, AI vocabulary, weasel attribution, inline-header bold lists, title-case headings, and em dash overuse, then rewrites to restore human sentence rhythm and concrete detail. Use this whenever the user asks to humanize, de-AI, or de-slop text; asks whether something "sounds like ChatGPT" or "reads like AI"; asks for a final polish, edit, or review of a draft before publishing; or is preparing a blog post, SEO article, newsletter, pitch deck, investor update, landing page, email, or LinkedIn/X post. Also use it proactively when writing any of those from scratch, so the first draft does not need cleaning.
---

# Anti-AI

Text that reads as model-generated loses the reader's trust before the argument lands. This skill removes the patterns that cause that and puts human texture back.

## The one principle that matters

**Subtracting AI texture is only half the job. You must add human texture back.**

If you only delete, you get flat, hedged, generic prose. That reads *more* artificial, not less, because uniformity is the underlying tell. The signals that read as human are mostly things standard writing advice tells you to cut: plain "is/has" phrasing, hedges like "perhaps" and "tends to", flat superlatives like "the only" and "the first", mild wordiness like "in order to", and wildly uneven sentence lengths.

So every pass runs in two directions. Cut the formula, then put a person back in.

## Workflow

Run all three stages unless the user asks for only one.

0. **Run the scanner** on the text. It catches every mechanical tell deterministically, which is faster and more consistent than reading for them, and it gives you the rhythm numbers you cannot eyeball.

   Call it with the script's own path, not a relative one, since your working directory is usually not the skill folder:

```bash
python3 /path/to/anti-ai/scripts/scan.py draft.md
cat draft.md | python3 /path/to/anti-ai/scripts/scan.py -   # stdin
python3 /path/to/anti-ai/scripts/scan.py draft.md --json    # machine-readable
python3 /path/to/anti-ai/scripts/scan.py draft.md --quiet    # score line only
```

   By default the scanner ignores code blocks, inline code, markdown blockquotes, and short quoted spans, so text that *quotes* a tell as an example is not scored as committing it. Pass `--score-everything` to turn that off.

   If the text is pasted into chat rather than saved as a file, write it to a temp file first, then scan that. Under about 40 words the scanner reports `n/a` instead of a score, because the statistics are noise at that length. Score those by hand from the rubric.

   The scanner cannot judge tone, so it will miss puffery, vague attribution, and hollow structure. Those are yours to catch in step 1.
1. **Read the whole text once** before editing anything. Note what it is actually trying to say. If the piece has no argument underneath the polish, say so directly. Rewriting hollow text just hides the hollowness, and the reader still feels it.
2. **Score it 0-100** using the rubric below. Show the deductions.
3. **Audit**: list every tell you found, quoting the exact phrase. Group by category. Do not paraphrase the offending text, quote it, so the user can see it in their own draft.
4. **Rewrite aggressively** using the protocol below.
5. **Re-score the rewrite** so the user can see the delta.

## Scoring rubric

Start at 100. Deduct per instance, capped per category. Normalize counts to a 500-word window so short and long pieces score comparably.

| Category | Per instance | Cap |
|---|---|---|
| **A. Puffery and inflated significance** | -4 | -20 |
| **B. Sentence-shape formulas** | -4 | -20 |
| **C. Vocabulary and copula avoidance** | -3 | -15 |
| **D. Formatting and structure** | -5 | -15 |
| **E. Vagueness and weasel attribution** | -3 | -15 |
| **F. Missing human texture** | -5 | -15 |

Category F is scored on absence, not presence. Deduct if the passage has: no sentence under 8 words, no sentence over 25 words, no concrete number/name/date/place, no hedge or qualifier, no opinion or first-person moment where the format allows one, or paragraphs that are all the same length.

**Category R: residue. One hit caps the total score at 20, regardless of everything else.**

Residue is not a style problem. It is leftover machinery proving the text was pasted without being read, so no amount of good prose elsewhere redeems it. Scan for: `contentReference`, `oaicite`, `oai_citation`, `turn0search`, `turn0image`, `citeturn`, `[cite: 1]`, `[span_1](start_span)`, `grok_card`, `grok_render_citation_card_json`, `【85†L261-269】`, `[attached_file:1]`, `[web:1]`, `ppl-ai-file-upload`, `:::writing{variant=...}`, `utm_source=chatgpt.com`, `utm_source=openai`, `utm_source=copilot.com`, `referrer=grok.com`, unfilled `[BRACKETED_PLACEHOLDER]` slots, `2025-xx-xx` dates, and conversational leftovers like "I hope this helps", "Certainly!", "Would you like me to", "Let me know if", "As of my last knowledge update", "As an AI language model".

Report residue first and separately. The user needs to know their draft is leaking machinery before they care about sentence rhythm.

**Bands**

- **90-100** Reads human. Ship it.
- **75-89** Mostly clean, a few tells left.
- **60-74** Recognizably AI-assisted.
- **40-59** Model output with light editing on top.
- **0-39** Raw model output.

Full detection catalog with words-to-watch lists: `references/tells.md`. Read it before scoring anything longer than a few paragraphs.

## The rewrite protocol

Aggressive by default. Work in this order, because subtraction first makes the additions easier to place.

### Pass 1: Cut

Delete rather than rephrase. Most AI tells are sentences carrying no information, and rewording them just produces a better-disguised empty sentence.

- Cut every clause that asserts importance instead of demonstrating it: "plays a crucial role in", "serves as a testament to", "marking a pivotal moment", "underscoring its significance".
- Cut trailing present participles that add commentary: "..., highlighting the growing demand", "..., reflecting broader industry trends". These are the single most recognizable tell. Cut the comma and everything after it.
- Cut editorial throat-clearing: "It's important to note", "It's worth mentioning", "No discussion would be complete without".
- Cut section-summary sentences that restate what the section just said.
- Cut "Challenges", "Future Prospects", "Conclusion", and "Overview" sections unless they carry facts that appear nowhere else.
- **If a paragraph survives all of the above and still says nothing, cut the paragraph.** This is the highest-value move in the whole skill and the one most often skipped.

### Pass 2: Break the shapes

These are structural, so they survive vocabulary swaps. Rewrite the sentence, do not substitute words.

- **Negative parallelism.** "It's not just X, it's Y" / "Not only X but also Y" / "X rather than Y". Pick one side and state it. If both halves matter, use two sentences.
- **Rule of three.** Three parallel adjectives or three parallel phrases. Cut to one or two, or go to four. Three is the shape that reads as generated.
- **False ranges.** "from strategy to execution", "ranging from A to Z" where nothing sits between the endpoints. Name the actual items or cut.
- **Inline-header bold lists.** `- **Scalability**: The system scales easily.` Convert to prose, or to a plain bullet with no bold lead-in. If the bold phrase is just restated in the sentence after it, delete the bold phrase.

### Pass 3: Restore plain language

- Put back **is, are, has, there is**. Replace "serves as", "stands as", "functions as", "represents", "boasts", "features", "offers" wherever a copula was avoided.
- Plain verbs: **wrote** not authored, **used** not utilized, **moved** not relocated, **tried** not attempted, **died** not passed away, **started** not embarked upon, **helped** not facilitated.
- Strip the vocabulary flagged in `references/tells.md`. Take it literally: the specific overused word is the problem, not its synonyms. Do not swap "delve" for "plumb the depths of".

### Pass 4: Add human texture

This is the pass that gets skipped, and skipping it is why aggressive edits go flat. See `references/human-markers.md` for worked examples.

- **Rhythm.** In every 10 sentences, at least one under 8 words and at least one over 25. Vary paragraphs between 1 and 6 sentences. A one-sentence paragraph is a human move.
- **Specifics.** One concrete anchor per paragraph: a number, a name, a date, a place, a product, a real example. If the draft has no specifics available, that is a research gap, not a style problem. Flag it rather than inventing detail.
- **Hedges.** "probably", "tends to", "in most cases", "I think", "roughly". Models are trained toward confident flatness, so honest uncertainty reads as human.
- **Flat superlatives.** "the only", "the first", "the worst", "one of the best". Use them where they are true.
- **Voice.** One opinionated or first-person sentence per section, where the format allows it.
- **Mild wordiness.** "in order to", "the fact that", "a part of", "as a result of". Do not hunt these down. Leaving one or two in is a human signal.

### Pass 5: Punctuation and surface

- Em dashes: at most one per 500 words, and unspaced if kept. Replace the rest with commas, periods, or parentheses.
- Straight quotes and straight apostrophes, not curly.
- Sentence case in headings, not Title Case.
- No emoji in headings or bullets.
- No bold used for mechanical emphasis on every instance of a key term.

## Output format

Use this structure every time:

```
## Score: [N]/100 — [band label]

**Deductions**
- A. Puffery: -[N] ([count] instances)
- B. Sentence shapes: -[N] ([count] instances)
- C. Vocabulary/copulas: -[N] ([count] instances)
- D. Formatting: -[N] ([count] instances)
- E. Vagueness: -[N] ([count] instances)
- F. Missing human texture: -[N] ([what is absent])

## What's flagged

**[Category]**
- "[exact quote]" → [why it reads as AI, in a few words]

## Rewrite

[the rewritten text, clean, no annotations inside it]

## Score after: [N]/100

[One or two lines on what still can't be fixed by editing, e.g. missing specifics
the writer needs to supply, or a claim with no evidence behind it.]
```

If the user asked only for a rewrite, give the rewrite and a one-line before/after score. Do not pad the response with the full audit they did not ask for.

## Format-specific notes

- **Blog and SEO articles.** The heaviest offenders are inline-header bold lists, the "In today's [industry]" opener, and rhetorical-question openers ("Have you ever wondered..."). Open with a fact, a number, or a scene instead. Keep the H2 structure SEO needs, but write the sections as prose.
- **Pitch decks and investor docs.** Puffery and false ranges dominate here, and investors are unusually well-calibrated to them. Every adjective should be replaceable by a number. "Rapidly growing market" becomes the growth rate. "Strong traction" becomes the actual figure. If there is no number, cut the claim rather than softening it.
- **Email.** Cut "I hope this email finds you well" and every closing offer of further assistance. Short, uneven sentences. One ask per email, stated plainly.
- **LinkedIn and X.** Negative parallelism is the dominant tell on these platforms because it became the house style of engagement-bait. One-line paragraphs are fine here, but the rhythm rule still applies. Do not let every line be the same length.
- **Technical and code documentation.** Relax the formatting rules. Bulleted lists with bold terms are conventional in docs, and Markdown is native. Keep the vocabulary and puffery passes.

## Guardrails

- **Never change facts, figures, names, dates, or quotations** to make prose flow better. If a fact makes a sentence awkward, rewrite around it.
- **Never invent specifics** to satisfy the concreteness rule. Flag the gap and ask the user for the real number.
- **Leave code blocks, citations, and legal or regulatory language alone.** Those have conventions that outrank style.
- **Preserve the user's existing voice** if the draft has one. The target is the user sounding like themselves, not like a generic good writer.
- **Do not claim the output will defeat AI detectors.** Detectors are unreliable in both directions, and the goal here is writing that is genuinely better, not writing that games a classifier.
- Where disclosure of AI assistance is expected (academic submissions, journals, Wikipedia, some client contracts), this skill improves the prose but does not remove the disclosure obligation. Say so plainly if the context suggests it, once, without lecturing.

## Reference files

- `references/tells.md` — full detection catalog: all six categories, words-to-watch lists, era-specific vocabulary, model-specific fingerprints. Read before scoring anything substantial.
- `references/human-markers.md` — the additive side: rhythm targets, specificity injection, and before/after rewrites.
