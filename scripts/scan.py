#!/usr/bin/env python3
"""
scan.py - deterministic detector for mechanical AI-writing tells.

Catches what a regex can catch: residue, vocabulary, sentence-shape formulas,
formatting, and the texture statistics you cannot eyeball. It deliberately does
NOT judge tone, so puffery, vague attribution, and hollow structure still need a
human read. Treat the score as a floor, not a verdict.

Usage:
    python3 scan.py draft.md
    cat draft.md | python3 scan.py -
    python3 scan.py draft.md --json
    python3 scan.py draft.md --quiet     # score line only

Standard library only. No network, no dependencies.
"""

import argparse
import json
import re
import statistics
import sys

# --------------------------------------------------------------------------
# R. Residue. Any hit caps the total score at 20.
# --------------------------------------------------------------------------

RESIDUE = [
    ("chatgpt-contentref", r"contentReference|oaicite|oai_citation"),
    ("chatgpt-turn", r"\bcite?turn\d|turn\d(search|image|news|file)\d"),
    ("chatgpt-attribution", r'\{"attribution"\s*:\s*\{"attributableIndex"'),
    ("gemini-cite", r"\[cite:\s*\d+"),
    ("gemini-span", r"\[span_\d+\]\((start|end)_span\)"),
    ("grok-card", r"grok_card|grok_render_citation_card_json|grok-card data-id"),
    ("deepseek-lenticular", r"\u3010\d+\u2020"),
    ("perplexity-tags", r"\[attached_file:\d+\]|\[web:\d+\]|ppl-ai-file-upload"),
    ("writing-block", r":::writing\{"),
    ("utm-openai", r"utm_source=(openai|chatgpt\.com)"),
    ("utm-copilot", r"utm_source=copilot\.com"),
    ("utm-grok", r"referrer=grok\.com"),
    ("placeholder-date", r"\b20\d\d-(xx|XX)-(xx|XX)\b"),
    ("placeholder-slot", r"\b(INSERT_[A-Z_]+|SOURCE_PUBLISHER|\[[A-Z][A-Z_]{4,}\])"),
    ("footnote-arrow", r"\u21a9"),
    ("chat-leftover", r"(?i)\b(i hope this helps|hope this helps!|certainly!|of course!|"
                      r"you're absolutely right|would you like me to|let me know if you|"
                      r"is there anything else|here'?s a more detailed breakdown)"),
    ("cutoff-disclaimer", r"(?i)\b(as an ai language model|as a large language model|"
                          r"as of my last (knowledge|training) update|up to my last)"),
    ("gap-speculation", r"(?i)\b(not widely (documented|available|disclosed)|"
                        r"while specific (details|information) (about|are|is)|"
                        r"in the (provided|available) (sources|search results)|"
                        r"maintains a low profile|keeps personal details private)"),
]

# --------------------------------------------------------------------------
# A. Puffery and inflated significance  (-4 each, cap -20)
# --------------------------------------------------------------------------

PUFFERY = [
    ("significance-claim", r"(?i)\b(stands as|serves as) (a|an|the)\b|"
                           r"\b(is|as) a testament to\b|\ba (crucial|pivotal|vital|"
                           r"significant|key) (role|moment|turning point)\b|"
                           r"\bplays? a (crucial|pivotal|vital|key|central) role\b"),
    ("broader-trends", r"(?i)\b(reflects? (a )?broader|contributing to the broader|"
                       r"part of a (broader|larger) (movement|trend|shift)|"
                       r"(represents|marks) a (significant )?shift|"
                       r"setting the stage for|evolving landscape|"
                       r"(leaving|left) an indelible mark|lasting (impact|legacy)|"
                       r"watershed moment|deeply rooted in)"),
    ("participle-tail", r",\s+(highlighting|underscoring|emphasizing|reflecting|"
                        r"symbolizing|showcasing|cementing|solidifying|cultivating|"
                        r"fostering|reinforcing|ensuring|contributing to|"
                        r"demonstrating|illustrating|marking)\s+(the|its|his|her|"
                        r"their|a|an)\b"),
    ("promo-adjectives", r"(?i)\b(boasts a|nestled in|in the heart of|rich (tapestry|"
                         r"heritage|history) of|vibrant (community|culture|ecosystem)|"
                         r"state-of-the-art|cutting-edge|groundbreaking|world-class|"
                         r"seamless(ly)? integrat|breathtaking|renowned for its)"),
    ("canned-notability", r"(?i)\b(independent coverage|trade publications|"
                          r"(regional|national|local) media outlets|"
                          r"(maintains?|has) an active social media presence|"
                          r"profiled in (major|leading))"),
    ("didactic-aside", r"(?i)\b(it'?s (important|crucial|worth) (to )?(note|noting|"
                       r"remember|mention)|no discussion (of|would be)|"
                       r"it is worth noting)"),
]

# --------------------------------------------------------------------------
# B. Sentence-shape formulas  (-4 each, cap -20)
# --------------------------------------------------------------------------

SHAPES = [
    ("neg-parallel-notjust", r"(?i)\b(not just|not only|not merely) [^.!?\n]{2,60}?\b"
                             r"(but|it'?s|they'?re)\b"),
    ("neg-parallel-isnt", r"(?i)\b(it|this|that|he|she|they)'?s not (about )?[^.!?\n]{2,60}?"
                          r",\s*(it|this|that|they)'?s\b"),
    ("neg-parallel-stack", r"(?i)\bno [a-z]+, no [a-z]+,\s*(just|only)\b"),
    ("neg-parallel-rather", r"(?i)\brather than (ideological|merely|simply|just)\b|"
                            r"\bless about [^.!?\n]{2,40} and more about\b"),
    ("false-range", r"(?i)\b(rang(e|es|ing) from|from) [a-z][a-z\s-]{2,30} to "
                    r"[a-z][a-z\s-]{2,30}[,.]"),
    ("section-summary", r"(?im)^\s*(in (summary|conclusion|closing)|overall|"
                        r"to sum up|in short)\b[,:]"),
    ("conclusion-heading", r"(?im)^#{1,4}\s*(conclusion|final thoughts|key takeaways|"
                           r"future (prospects|outlook)|challenges( and .*)?)\s*$"),
    ("challenges-formula", r"(?i)despite (its|their|the) [^.!?\n]{3,60}"
                           r"(faces?|face) (several |a number of |significant )?"
                           r"(challenges|obstacles|hurdles)"),
]

RULE_OF_THREE = re.compile(
    r"\b([a-z]{4,}),\s+([a-z]{4,}),\s+and\s+([a-z]{4,})\b"
)

# --------------------------------------------------------------------------
# C. Vocabulary and copula avoidance  (-3 each, cap -15)
# --------------------------------------------------------------------------

AI_VOCAB = {
    "gpt4": ["delve", "tapestry", "intricate", "intricacies", "meticulous",
             "meticulously", "bolstered", "garner", "garnered", "interplay",
             "testament", "pivotal", "underscore", "underscores", "underscoring",
             "vibrant", "boasts", "enduring", "multifaceted", "myriad"],
    "gpt4o": ["showcase", "showcases", "showcasing", "foster", "fosters",
              "fostering", "enhance", "enhances", "enhancing", "align with",
              "aligns with", "crucial", "landscape", "realm", "leverage",
              "leveraging", "seamless", "robust", "holistic"],
    "gpt5": ["emphasizing", "highlighting", "spearhead", "spearheaded",
             "transformative", "paramount", "cornerstone", "reimagine",
             "empower", "empowering", "catalyst", "elevate", "unlock"],
    "grok": ["empirical", "causal", "correlate", "correlates"],
}

COPULA_AVOIDANCE = re.compile(
    r"(?i)\b(serves? as|stands? as|functions? as|operates? as|acts? as)\s+(a|an|the)\b"
    r"|\b(boasts|features|offers|maintains|possesses)\s+(a|an|\d|over|more than)\b"
    r"|\b(has emerged as|has established itself as|refers to the)\b"
)

STIFF_SYNONYMS = re.compile(
    r"(?i)\b(authored|relocated|utiliz(e|es|ed|ing)|attempted to|passed away|"
    r"facilitat(e|es|ed|ing)|embark(ed)? (up)?on|demonstrat(e|es|ed) that|"
    r"possess(es|ed)?|commenc(e|ed|ing)|endeavou?r(ed)?|"
    r"in order to ascertain)\b"
)

# --------------------------------------------------------------------------
# D. Formatting  (-5 each, cap -15)
# --------------------------------------------------------------------------

INLINE_HEADER_LIST = re.compile(
    r"(?m)^\s*(?:[-*+\u2022\u2013]|\d+[.)])\s+(?:\*\*|__)[^*_\n]{2,60}(?:\*\*|__)\s*:"
)
TITLE_CASE_HEADING = re.compile(
    r"(?m)^#{1,6}\s+(?:[A-Z][a-z]+\s+){1,}(?:[A-Z][a-z]+)\s*$"
)
EMOJI = re.compile(
    "[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F]"
)
CURLY = re.compile("[\u2018\u2019\u201c\u201d]")
EM_DASH = re.compile("\u2014")
THEMATIC_BREAK = re.compile(r"(?m)^\s*(-{3,}|\*{3,}|_{3,})\s*\n+#{1,6}\s")

# --------------------------------------------------------------------------
# E. Vagueness and weasel attribution  (-3 each, cap -15)
# --------------------------------------------------------------------------

WEASEL = re.compile(
    r"(?i)\b(industry (experts|reports|observers|analysts)|experts (say|argue|agree|"
    r"note|believe)|observers (have )?(noted|cited)|some (critics|analysts|"
    r"observers|experts)|(many|most) (believe|argue|agree)|studies (show|suggest|"
    r"indicate)|research (shows|suggests|indicates)|(several|multiple|various) "
    r"(sources|publications|studies|reports)|(it is|is) widely (regarded|considered|"
    r"believed|seen as)|reviewers (have )?(praised|noted)|critics (have )?(praised|noted))\b"
)

# --------------------------------------------------------------------------
# F. Human texture markers (absence is the problem)
# --------------------------------------------------------------------------

HEDGES = re.compile(
    r"(?i)\b(probably|perhaps|roughly|tends? to|in most cases|i think|my guess|"
    r"more or less|sort of|kind of|maybe|apparently|arguably|fairly|pretty much|"
    r"at least in|somewhat|a bit|not sure|seems? to)\b"
)
SUPERLATIVES = re.compile(
    r"(?i)\b(the only|the first|the worst|the best|one of the (best|worst|few)|"
    r"nobody|never once|the single (biggest|best|worst))\b"
)
# Copula and auxiliary density. Research found a >10% drop in "is"/"are" across
# academic writing in 2023, so a low rate here is a real signal, not decoration.
COPULA = re.compile(r"(?i)\b(is|are|was|were|be|been|being|has|have|had)\b")
FIRST_PERSON = re.compile(r"(?i)(?<![\w'])(i|we|my|our|us|me)(?![\w'])")
MILD_WORDINESS = re.compile(
    r"(?i)\b(in order to|the fact that|as a result of|all of the|a part of|"
    r"due to the fact)\b"
)
SPECIFICS = re.compile(
    r"[$\u20b9\u20ac\u00a3]\s?\d[\d,.]*"
    r"|\b\d[\d,.]*\s*(%|percent|million|billion|bn\b|k\b|x\b)"
    r"|\b(19|20)\d\d\b"
    r"|\b\d+[\d,.]*[-\s]+(users|customers|people|employees|seats?|days?|weeks?|"
    r"months?|years?|hours?|minutes?)\b"
)

SENT_SPLIT = re.compile(r"(?<=[.!?])[\s\n]+")


def strip_code(text):
    """Remove fenced code blocks and inline code so markup isn't scored as prose."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"~~~.*?~~~", " ", text, flags=re.S)
    text = re.sub(r"`[^`\n]+`", " ", text)
    return text


def strip_quoted(text):
    """
    Remove blockquotes and short quoted spans.

    This handles the mention-versus-use problem: a style guide that quotes
    "it's not X, it's Y" as a bad example is not itself committing the tell,
    and neither is an article quoting a source. Without this, any writing
    *about* AI writing scores as AI writing, which is both wrong and funny.

    Only short spans are stripped, since a long block in quotation marks is
    usually the author's own prose rather than a cited example.
    """
    text = re.sub(r"(?m)^\s*>.*$", " ", text)              # markdown blockquotes
    text = re.sub(r"[\"\u201c][^\"\u201c\u201d\n]{1,80}[\"\u201d]", " ", text)
    text = re.sub(r"(?<![A-Za-z])['\u2018][^'\u2018\u2019\n]{1,60}['\u2019](?![A-Za-z])",
                  " ", text)
    return text


def find_all(patterns, text):
    """Run a list of (name, regex) pairs. Return {name: [matched strings]}."""
    hits = {}
    for name, pat in patterns:
        found = [m.group(0).strip() for m in re.finditer(pat, text)]
        if found:
            hits[name] = found
    return hits


def vocab_hits(text):
    lower = text.lower()
    out = {}
    for era, words in AI_VOCAB.items():
        found = []
        for w in words:
            n = len(re.findall(r"\b" + re.escape(w) + r"\b", lower))
            if n:
                found.append({"word": w, "count": n})
        if found:
            out[era] = sorted(found, key=lambda d: -d["count"])
    return out


def texture(text):
    sentences = [s.strip() for s in SENT_SPLIT.split(text) if s.strip()]
    lengths = [len(s.split()) for s in sentences if len(s.split()) > 1]
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    para_lens = [len(SENT_SPLIT.split(p)) for p in paras]

    stdev = statistics.pstdev(lengths) if len(lengths) > 1 else 0.0
    return {
        "sentences": len(lengths),
        "mean_sentence_len": round(statistics.mean(lengths), 1) if lengths else 0,
        "stdev_sentence_len": round(stdev, 1),
        "shortest": min(lengths) if lengths else 0,
        "longest": max(lengths) if lengths else 0,
        "has_short_sentence": any(l < 8 for l in lengths),
        "has_long_sentence": any(l > 25 for l in lengths),
        "paragraph_len_stdev": round(statistics.pstdev(para_lens), 1)
                               if len(para_lens) > 1 else 0.0,
        "hedges": len(HEDGES.findall(text)),
        "superlatives": len(SUPERLATIVES.findall(text)),
        "copula_rate_per_100w": round(100.0 * len(COPULA.findall(text))
                                     / max(len(text.split()), 1), 1),
        "first_person": len(FIRST_PERSON.findall(text)),
        "mild_wordiness": len(MILD_WORDINESS.findall(text)),
        "specifics": len(SPECIFICS.findall(text)),
    }


def analyze(raw, score_everything=False):
    if score_everything:
        prose = raw
        residue_src = raw
    else:
        prose = strip_quoted(strip_code(raw))
        # Residue is checked with code stripped but quotes intact, since real
        # residue lives in URLs and sentence tails, not inside backticks.
        residue_src = strip_quoted(strip_code(raw))
    words = max(len(prose.split()), 1)
    scale = 500.0 / words  # normalize counts to a 500-word window

    residue = find_all(RESIDUE, residue_src)
    puffery = find_all(PUFFERY, prose)
    shapes = find_all(SHAPES, prose)

    three = [" ".join(m.groups()) for m in RULE_OF_THREE.finditer(prose)]
    if three:
        shapes["rule-of-three"] = three

    vocab = vocab_hits(prose)
    vocab_count = sum(d["count"] for era in vocab.values() for d in era)

    copulas = [m.group(0) for m in COPULA_AVOIDANCE.finditer(prose)]
    stiff = [m.group(0) for m in STIFF_SYNONYMS.finditer(prose)]

    fmt = {}
    for name, pat in [
        ("inline-header-list", INLINE_HEADER_LIST),
        ("title-case-heading", TITLE_CASE_HEADING),
        ("emoji", EMOJI),
        ("curly-quotes", CURLY),
        ("em-dash", EM_DASH),
        ("thematic-break-before-heading", THEMATIC_BREAK),
    ]:
        found = [m.group(0).strip() for m in pat.finditer(prose if not score_everything else raw)]
        if found:
            fmt[name] = found

    weasel = [m.group(0) for m in WEASEL.finditer(prose)]
    tex = texture(prose)

    def norm(n):
        return n * scale

    # Category deductions, normalized per 500 words, capped.
    a = min(20, 4 * norm(sum(len(v) for v in puffery.values())))
    b = min(20, 4 * norm(sum(len(v) for v in shapes.values())))
    c = min(15, 3 * norm(vocab_count + len(copulas) + len(stiff)))
    d = min(15, 5 * norm(sum(len(v) for v in fmt.values())))
    e = min(15, 3 * norm(len(weasel)))

    # F is scored on absence.
    missing = []
    if not tex["has_short_sentence"]:
        missing.append("no sentence under 8 words")
    if not tex["has_long_sentence"]:
        missing.append("no sentence over 25 words")
    if tex["stdev_sentence_len"] < 6 and tex["sentences"] >= 5:
        missing.append("flat sentence-length variance (stdev %.1f)"
                       % tex["stdev_sentence_len"])
    if tex["specifics"] == 0:
        missing.append("no numbers, dates, or figures")
    if tex["hedges"] == 0:
        missing.append("no hedges or qualifiers")
    if tex["copula_rate_per_100w"] < 3.0 and tex["sentences"] >= 5:
        missing.append("copula-starved (%.1f per 100 words; human prose runs 5-8)"
                       % tex["copula_rate_per_100w"])
    if tex["superlatives"] == 0 and tex["first_person"] == 0:
        missing.append("no superlatives and no first person")
    f = min(15, 5 * len(missing))

    # Density override. Category caps mean a text saturated with a single tell
    # type can only lose that one category's worth of points, which understates
    # how machine-shaped it is. Wikipedia's guide is explicit that density and
    # co-occurrence are what actually separate machine text from human text, so
    # score the total load as well as the per-category load.
    total_hits = (sum(len(v) for v in puffery.values())
                  + sum(len(v) for v in shapes.values())
                  + vocab_count + len(copulas) + len(stiff)
                  + sum(len(v) for v in fmt.values())
                  + len(weasel))
    density = norm(total_hits)  # tells per 500 words
    if density >= 40:
        density_penalty = 25
    elif density >= 25:
        density_penalty = 15
    elif density >= 15:
        density_penalty = 8
    else:
        density_penalty = 0

    score = 100 - (a + b + c + d + e + f + density_penalty)
    capped_by_residue = bool(residue)
    if capped_by_residue:
        score = min(score, 20)
    score = max(0, min(100, round(score)))

    if score >= 90:
        band = "reads human"
    elif score >= 75:
        band = "mostly clean, a few tells"
    elif score >= 60:
        band = "recognizably AI-assisted"
    elif score >= 40:
        band = "model output, lightly edited"
    else:
        band = "raw model output"

    return {
        "score": score,
        "band": band,
        "word_count": words,
        "capped_by_residue": capped_by_residue,
        "tell_density_per_500w": round(density, 1),
        "too_short_to_score": words < 40,
        "deductions": {
            "A_puffery": round(a, 1),
            "B_sentence_shapes": round(b, 1),
            "C_vocabulary_copulas": round(c, 1),
            "D_formatting": round(d, 1),
            "E_vagueness": round(e, 1),
            "F_missing_texture": round(f, 1),
            "density_override": density_penalty,
        },
        "hits": {
            "R_residue": residue,
            "A_puffery": puffery,
            "B_sentence_shapes": shapes,
            "C_ai_vocabulary": vocab,
            "C_copula_avoidance": copulas,
            "C_stiff_synonyms": stiff,
            "D_formatting": fmt,
            "E_weasel_attribution": weasel,
        },
        "texture": tex,
        "missing_human_markers": missing,
    }


def render(r):
    out = []
    if r["too_short_to_score"]:
        out.append("SCORE: n/a - only %d words. Under ~40 words the statistics are"
                   " noise; hits below are still real." % r["word_count"])
    else:
        out.append("SCORE: %d/100  (%s)" % (r["score"], r["band"]))
    out.append("%d words scanned" % r["word_count"])
    if r["capped_by_residue"]:
        out.append("!! RESIDUE FOUND - score capped at 20. "
                   "Machine markup left in the text.")
    out.append("")

    out.append("DEDUCTIONS")
    labels = {
        "A_puffery": "A. Puffery / inflated significance",
        "B_sentence_shapes": "B. Sentence-shape formulas",
        "C_vocabulary_copulas": "C. AI vocabulary / copula avoidance",
        "D_formatting": "D. Formatting",
        "E_vagueness": "E. Vague attribution",
        "F_missing_texture": "F. Missing human texture",
    }
    labels["density_override"] = "Density override (%.0f tells/500w)" % r["tell_density_per_500w"]
    for k, v in r["deductions"].items():
        if k == "density_override" and not v:
            continue
        bar = "#" * int(v)
        out.append("  %-38s -%-5.1f %s" % (labels[k], v, bar))
    out.append("")

    for cat, hits in r["hits"].items():
        if not hits:
            continue
        out.append(cat.replace("_", " ").upper())
        if cat == "C_ai_vocabulary":
            for era, words in hits.items():
                joined = ", ".join("%s x%d" % (w["word"], w["count"]) for w in words)
                out.append("  [%s] %s" % (era, joined))
        elif isinstance(hits, dict):
            for name, items in hits.items():
                sample = "; ".join(repr(i) for i in items[:3])
                more = " (+%d more)" % (len(items) - 3) if len(items) > 3 else ""
                out.append("  %-32s %s%s" % (name, sample, more))
        else:
            sample = "; ".join(repr(i) for i in hits[:5])
            more = " (+%d more)" % (len(hits) - 5) if len(hits) > 5 else ""
            out.append("  %s%s" % (sample, more))
        out.append("")

    t = r["texture"]
    out.append("TEXTURE")
    out.append("  sentence length: mean %.1f, stdev %.1f, range %d-%d"
               % (t["mean_sentence_len"], t["stdev_sentence_len"],
                  t["shortest"], t["longest"]))
    out.append("  hedges %d | superlatives %d | copulas %.1f/100w | first person %d"
               % (t["hedges"], t["superlatives"], t["copula_rate_per_100w"],
                  t["first_person"]))
    out.append("  specifics (numbers/dates) %d | mild wordiness %d"
               % (t["specifics"], t["mild_wordiness"]))
    if r["missing_human_markers"]:
        out.append("  MISSING: " + "; ".join(r["missing_human_markers"]))
    out.append("")
    out.append("Note: this scanner cannot see tone. Read for puffery, hollow "
               "structure, and unverified attribution yourself.")
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("path", help="file to scan, or - for stdin")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    p.add_argument("--quiet", action="store_true", help="score line only")
    p.add_argument("--score-everything", action="store_true",
                   help="do not exclude code blocks, blockquotes, or quoted "
                        "examples (off by default, so writing *about* AI tells "
                        "is not flagged for quoting them)")
    args = p.parse_args()

    if args.path == "-":
        raw = sys.stdin.read()
    else:
        with open(args.path, encoding="utf-8") as fh:
            raw = fh.read()

    if not raw.strip():
        print("Nothing to scan.", file=sys.stderr)
        return 1

    result = analyze(raw, score_everything=args.score_everything)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.quiet:
        if result["too_short_to_score"]:
            print("n/a (only %d word(s))" % result["word_count"])
        else:
            print("%d/100 (%s)" % (result["score"], result["band"]))
    else:
        print(render(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
