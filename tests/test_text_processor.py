"""
BhashaAI — Text Processor Unit Tests
Tests text normalization, sentence segmentation, and chunk recombination.
"""

import unittest
from src.text_processor import (
    normalize_text,
    segment_sentences,
    recombine_sentences,
)


class TestTextProcessor(unittest.TestCase):

    def test_normalize_text(self):
        """Test text normalization."""
        raw_text = "  Hello   world! \n\n  This is   a   test.  "
        cleaned = normalize_text(raw_text)
        self.assertEqual(cleaned, "Hello world! This is a test.")

        empty_cleaned = normalize_text("")
        self.assertEqual(empty_cleaned, "")

    def test_segment_sentences(self):
        """Test sentence segmentation."""
        text = "India is a country full of diversity. It has many languages! Education is key to success."
        sentences = segment_sentences(text)
        self.assertGreaterEqual(len(sentences), 1)

    def test_recombine_sentences(self):
        """Test recombining sentence chunks."""
        chunks = ["भारत विविधता से भरा देश है।", "इसके पास कई भाषाएं हैं!"]
        recombined = recombine_sentences(chunks)
        self.assertEqual(recombined, "भारत विविधता से भरा देश है। इसके पास कई भाषाएं हैं!")


if __name__ == "__main__":
    unittest.main()
