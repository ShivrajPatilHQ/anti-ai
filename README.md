# anti-ai

A Claude skill that scores writing 0-100 on how machine-generated it reads, then rewrites it.

It is built as the inverse of Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), a roughly 15,000-word field guide that WikiProject AI Cleanup assembled from thousands of flagged submissions. That page exists to help editors catch machine text. This repo runs the same catalogue backwards.

The bundled scanner is a plain Python script with no dependencies, so you can also use it on its own without Claude.

## Why the obvious approach fails

Most humanizer tools are a ban list. Delete "delve", delete em dashes, delete "it's not X, it's Y", ship it.

That does not work, and Wikipedia's own editors say so. Strip every tell and you get flat, hedged, uniform prose, which reads more artificial rather than less, because uniformity is the thing all the surface patterns are symptoms of. The root cause is statistical: a model picks the likeliest continuation, so specific facts get smoothed into generic praise. "Inventor of the first train-coupling device" becomes "a revolutionary titan of industry".

So deleting the puffery is only half a fix. You have to put a real fact back where it was, and if there is no real fact, the sentence should not exist.

The other half is stranger. The markers that read as human are mostly things every style guide tells you to cut: simple "is" and "has" phrasing, hedges like "perhaps" and "tends to", flat superlatives like "the only", and mild wordiness like "in order to". Wikipedia measured these across 25 years of human editing. Ruthless compression is a machine signature.

## Install

As a Claude skill, drop the folder into your skills directory:

```
~/.claude/skills/anti-ai/
```

Claude Code, Cowork, and claude.ai all read from there. You can also upload the packaged `.skill` file through the Claude settings UI. Grab it from the [latest release](https://github.com/ShivrajPatilHQ/anti-ai/releases/latest), or build it yourself:

```bash
./scripts/build-skill.sh    # writes dist/anti-ai.skill
```

To use the scanner on its own, you need Python 3.8 or newer and nothing else:

```bash
git clone https://github.com/ShivrajPatilHQ/anti-ai.git
python3 anti-ai/scripts/scan.py draft.md
```

## Usage

Ask Claude to check or rewrite something and the skill triggers on its own. "Does this sound like AI", "humanize this", "polish this before I publish" all work.

Directly:

```bash
python3 scripts/scan.py draft.md            # full report
python3 scripts/scan.py draft.md --quiet    # just the score
python3 scripts/scan.py draft.md --json     # machine-readable
cat draft.md | python3 scripts/scan.py -    # stdin
```

Under about 40 words it reports `n/a` rather than a score, since the statistics are noise at that length.

## What it catches

The scoring rubric has six categories plus one override.

Residue is leftover machinery: `utm_source=chatgpt.com`, `contentReference`, `[cite: 1]`, `grok_card`, unfilled placeholders, "I hope this helps". Any single hit caps the score at 20, because that is not a style problem, it is evidence the text was pasted without being read. Vendor signatures for ChatGPT, Gemini, Grok, DeepSeek, and Perplexity are all in `references/tells.md`.

Puffery covers inflated significance and promotional tone. Sentence shapes covers negative parallelism in its three forms, rule of three, and false ranges. Vocabulary is tracked by model era, so a draft heavy on "delve" and "tapestry" reads as 2023 output while one heavy on "showcasing" and "emphasizing" reads as 2025. Formatting covers inline-header bold lists, title case headings, em dashes, and curly quotes. Vagueness covers weasel attribution and hallucinated citations.

The sixth category is scored on absence, not presence. A draft can be clean of every tell above and still read as machine-written because it has no hedges, no specifics, and no variation in sentence length.

There is also a density override, because per-category caps meant a document saturated with one tell type could only lose that category's points. Density and co-occurrence are what actually separate machine text from human text.

## Example

From `examples/`. Before, at 0/100:

> In today's rapidly evolving business landscape, workflow automation has emerged as a pivotal force, serving as a testament to the growing demand for intelligent enterprise solutions.

After, at 95/100:

> TechFlow started in 2019. The product is task management with an analytics layer on top, sold to mid-market ops teams.

The metric that moved most was the copula rate: 1.6 uses of is/are/has per 100 words before, 7.4 after. One study found a drop of more than 10% in "is" and "are" across academic writing in 2023 with no prior trend, and found models removed them even when asked only to revise a sentence. That number has been the most reliable signal in my testing. Sentence length variance is close behind.

## What it will not do

It does not claim to beat AI detectors. Those are unreliable in both directions and the goal here is prose that is actually better, not prose that games a classifier.

It will not invent specifics to satisfy the concreteness rule. If a draft has no real numbers, that is a research gap and the skill flags it rather than making one up.

It will not change facts, figures, names, or quotations to improve flow.

And where disclosure of AI assistance is expected, such as academic submissions or journals or Wikipedia itself, better prose does not remove that obligation. The skill says so once and moves on.

## Tests

```bash
python3 -m unittest discover tests -v
```

32 tests covering detection, false positives on human baselines, score bounds, determinism, and robustness against empty, tiny, unicode, and CRLF input. The false positive tests matter most. A detector that flags everything is worse than no detector.

## Contributing

Model output drifts. The vocabulary lists in particular go stale fast, since "delve" peaked in 2023 and had largely dropped off by 2025. If you spot a new tell or a new vendor residue signature, open an issue with an example.

Pull requests that add a detection pattern should include a test for the pattern and a test showing it does not fire on human writing.

## Credits

The detection catalogue is derived from [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup and licensed CC BY-SA 4.0. The interpretation, scoring rubric, and code here are mine.

## License

MIT. See [LICENSE](LICENSE).
