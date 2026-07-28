#!/usr/bin/env python3
"""
Test suite for scan.py. Standard library only.

Run from the repo root:
    python3 -m unittest discover tests -v
    python3 tests/test_scan.py
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import scan  # noqa: E402


HUMAN = """
TechFlow started in 2019 selling workflow automation to mid-market companies. The
product is task management with an analytics layer bolted on, which is a less
exciting description than the one on their homepage but a more accurate one. It works.

We priced it at $49 per seat for the first eighteen months. That was wrong, and it
took an embarrassingly long time to figure out why: our buyers were ops leads with a
departmental budget of roughly $2,000 a quarter, so a 20-person team blew through the
budget in month one and then had to go ask finance, which killed about half our deals
somewhere in procurement.

The fix was boring. We moved to a flat team price and stopped counting seats.

Retention is the open question. We have not published a number, and I am not going to
pretend the one we have internally is good. It is probably fine for a company at this
stage. Probably.
"""

SLOP = """
In today's rapidly evolving business landscape, workflow automation has emerged as a
pivotal force, serving as a testament to the growing demand for intelligent enterprise
solutions. TechFlow boasts a comprehensive suite of tools that range from task
management to advanced analytics, empowering organizations to streamline operations.

Industry experts have noted that TechFlow's approach represents a significant shift in
how enterprises think about automation, underscoring its commitment to innovation.
Studies show that companies adopting such platforms see improvements in efficiency,
productivity, and collaboration.

It's important to note that this is not just a product launch, it's a fundamental
rethinking of how work gets done. Despite its rapid growth, the company faces
challenges in an increasingly competitive market.

In conclusion, TechFlow remains well-positioned to capitalize on emerging
opportunities in the evolving automation landscape.
"""


class TestResidue(unittest.TestCase):
    """Residue is near-proof of unedited output, so it caps the score at 20."""

    def test_residue_caps_score(self):
        text = HUMAN + "\nSource: https://x.com/a?utm_source=chatgpt.com\n"
        r = scan.analyze(text)
        self.assertTrue(r["capped_by_residue"])
        self.assertLessEqual(r["score"], 20)

    def test_clean_text_has_no_residue(self):
        self.assertFalse(scan.analyze(HUMAN)["capped_by_residue"])

    def test_vendor_signatures(self):
        cases = {
            "See :contentReference[oaicite:0]{index=0} here.": "chatgpt-contentref",
            "As noted [cite: 4] in the report.": "gemini-cite",
            "Result [span_1](start_span) follows.": "gemini-span",
            "Data from [attached_file:1] shows.": "perplexity-tags",
            "Accessed 2025-xx-xx by the team.": "placeholder-date",
            "I hope this helps! Tell me more.": "chat-leftover",
            "As of my last knowledge update in 2024.": "cutoff-disclaimer",
        }
        for text, expected_key in cases.items():
            with self.subTest(text=text):
                hits = scan.analyze(text)["hits"]["R_residue"]
                self.assertIn(expected_key, hits)


class TestDetection(unittest.TestCase):

    def test_participle_tail(self):
        text = ("The population reached 56,998 inhabitants, highlighting the "
                "growing importance of the region. " * 3)
        self.assertIn("participle-tail", scan.analyze(text)["hits"]["A_puffery"])

    def test_negative_parallelism(self):
        shapes = scan.analyze("It's not a product, it's a philosophy. " * 3)["hits"]["B_sentence_shapes"]
        self.assertIn("neg-parallel-isnt", shapes)

    def test_rule_of_three(self):
        shapes = scan.analyze("It improves speed, clarity, and accuracy overall. " * 3)["hits"]["B_sentence_shapes"]
        self.assertIn("rule-of-three", shapes)

    def test_inline_header_list(self):
        text = "Intro line here.\n\n- **Scalability**: it scales.\n- **Security**: it is secure.\n"
        self.assertIn("inline-header-list", scan.analyze(text)["hits"]["D_formatting"])

    def test_weasel_attribution(self):
        self.assertTrue(scan.analyze("Industry experts have noted the trend. " * 3)["hits"]["E_weasel_attribution"])

    def test_ai_vocabulary_by_era(self):
        vocab = scan.analyze("We delve into the rich tapestry of pivotal moments. " * 3)["hits"]["C_ai_vocabulary"]
        self.assertIn("gpt4", vocab)


class TestFalsePositives(unittest.TestCase):
    """A detector that flags everything is worse than useless."""

    def test_human_text_scores_high(self):
        r = scan.analyze(HUMAN)
        self.assertGreaterEqual(r["score"], 85, "human baseline should not be flagged")

    def test_code_blocks_excluded_from_prose(self):
        text = HUMAN + "\n```python\n# delve tapestry pivotal meticulous underscore\n```\n"
        self.assertEqual(scan.analyze(text)["hits"].get("C_ai_vocabulary", {}), {})

    def test_inline_code_excluded(self):
        text = HUMAN + "\nThe `pivotal` and `tapestry` variables are named badly.\n"
        self.assertEqual(scan.analyze(text)["hits"].get("C_ai_vocabulary", {}), {})

    def test_em_dash_alone_is_not_fatal(self):
        text = HUMAN.replace("It works.", "It works \u2014 mostly.")
        self.assertGreaterEqual(scan.analyze(text)["score"], 80)


class TestMentionVersusUse(unittest.TestCase):
    """Writing *about* AI tells must not be scored as containing them."""

    def test_quoted_example_not_scored(self):
        text = HUMAN + '\nAvoid the phrase "it is not X, it is Y" in your drafts.\n'
        self.assertGreaterEqual(scan.analyze(text)["score"], 85)

    def test_blockquoted_example_not_scored(self):
        text = HUMAN + "\n> serving as a testament to the pivotal role it plays\n"
        self.assertGreaterEqual(scan.analyze(text)["score"], 85)

    def test_backticked_residue_not_capping(self):
        text = HUMAN + "\nStrip `utm_source=chatgpt.com` from any URL you paste.\n"
        self.assertFalse(scan.analyze(text)["capped_by_residue"])

    def test_real_residue_still_caught_in_url(self):
        text = HUMAN + "\nSource: https://x.com/report?utm_source=chatgpt.com\n"
        self.assertTrue(scan.analyze(text)["capped_by_residue"])

    def test_score_everything_flag_restores_strictness(self):
        text = HUMAN + '\nAvoid "serving as a testament to the pivotal role" here.\n'
        lenient = scan.analyze(text)["score"]
        strict = scan.analyze(text, score_everything=True)["score"]
        self.assertLess(strict, lenient)


class TestScoring(unittest.TestCase):

    def test_slop_scores_low(self):
        self.assertLessEqual(scan.analyze(SLOP)["score"], 30)

    def test_separation(self):
        self.assertGreater(scan.analyze(HUMAN)["score"],
                           scan.analyze(SLOP)["score"] + 50)

    def test_score_bounds(self):
        for text in [HUMAN, SLOP, "word " * 500, "The system serves as a pivotal component. " * 200]:
            r = scan.analyze(text)
            self.assertGreaterEqual(r["score"], 0)
            self.assertLessEqual(r["score"], 100)

    def test_density_override_fires_on_saturation(self):
        r = scan.analyze("The system serves as a pivotal component. " * 200)
        self.assertGreater(r["deductions"]["density_override"], 0)
        self.assertLessEqual(r["score"], 40)

    def test_short_text_not_scored(self):
        self.assertTrue(scan.analyze("Hello there friend.")["too_short_to_score"])

    def test_deterministic(self):
        self.assertEqual(scan.analyze(SLOP)["score"], scan.analyze(SLOP)["score"])


class TestTexture(unittest.TestCase):

    def test_copula_rate_separates(self):
        self.assertGreater(scan.analyze(HUMAN)["texture"]["copula_rate_per_100w"],
                           scan.analyze(SLOP)["texture"]["copula_rate_per_100w"])

    def test_sentence_variance_separates(self):
        self.assertGreater(scan.analyze(HUMAN)["texture"]["stdev_sentence_len"],
                           scan.analyze(SLOP)["texture"]["stdev_sentence_len"])

    def test_specifics_counts_currency_and_years(self):
        self.assertGreaterEqual(scan.analyze(HUMAN)["texture"]["specifics"], 3)

    def test_missing_markers_reported(self):
        self.assertTrue(scan.analyze(SLOP)["missing_human_markers"])


class TestRobustness(unittest.TestCase):

    def test_empty_and_tiny_inputs(self):
        for text in [" ", "\n\n", "Hi.", "a"]:
            with self.subTest(text=repr(text)):
                scan.analyze(text)  # must not raise

    def test_unicode(self):
        scan.analyze("Caf\u00e9 na\u00efve \u65e5\u672c\u8a9e \U0001F3AF test. " * 10)

    def test_crlf(self):
        scan.analyze("First line.\r\nSecond line here.\r\n" * 10)

    def test_render_does_not_crash(self):
        for text in [HUMAN, SLOP, "Hi.", " "]:
            scan.render(scan.analyze(text))


if __name__ == "__main__":
    unittest.main(verbosity=2)
