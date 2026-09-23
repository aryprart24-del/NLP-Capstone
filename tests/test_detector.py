"""
BhashaAI — Language Detector Unit Tests
Tests Lingua-based language detection and NLLB code resolution.
"""

import unittest
from src.language_detector import detect_language, is_supported, get_display_name


class TestLanguageDetector(unittest.TestCase):

    def test_detect_english(self):
        """Test English detection."""
        nllb_code, name, conf = detect_language("India is a country full of diversity.")
        self.assertEqual(nllb_code, "eng_Latn")
        self.assertEqual(name, "English")

    def test_detect_hindi(self):
        """Test Hindi detection."""
        nllb_code, name, conf = detect_language("भारत विविधता से भरा देश है।")
        self.assertEqual(nllb_code, "hin_Deva")
        self.assertEqual(name, "Hindi")

    def test_is_supported(self):
        """Test supported NLLB language check."""
        self.assertTrue(is_supported("hin_Deva"))
        self.assertTrue(is_supported("mar_Deva"))
        self.assertFalse(is_supported("xyz_Fake"))

    def test_empty_input(self):
        """Test detection with empty string."""
        code, name, conf = detect_language("")
        self.assertIsNone(code)


if __name__ == "__main__":
    unittest.main()
