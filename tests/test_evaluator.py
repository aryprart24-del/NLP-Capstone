"""
BhashaAI — Evaluator Unit Tests
Tests BLEU and chrF metric calculation using SacreBLEU.
"""

import unittest
from evaluation.metrics import bleu, chrf, compute_all_metrics


class TestEvaluator(unittest.TestCase):

    def test_exact_match(self):
        """Exact predictions and references should produce high BLEU/chrF."""
        preds = ["The student submitted the application yesterday."]
        refs = ["The student submitted the application yesterday."]

        res_bleu = bleu(preds, refs)
        res_chrf = chrf(preds, refs)

        self.assertAlmostEqual(res_bleu["score"], 100.0, places=1)
        self.assertAlmostEqual(res_chrf["score"], 100.0, places=1)

    def test_compute_all_metrics(self):
        """Test compute_all_metrics helper."""
        preds = ["India is a diverse country.", "Education is crucial."]
        refs = ["India is a country full of diversity.", "Education is essential."]

        res = compute_all_metrics(preds, refs)
        self.assertIn("bleu", res)
        self.assertIn("chrf", res)
        self.assertGreater(res["bleu"], 0)
        self.assertGreater(res["chrf"], 0)


if __name__ == "__main__":
    unittest.main()
