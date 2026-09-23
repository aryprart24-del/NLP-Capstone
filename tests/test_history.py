"""
BhashaAI — History Unit Tests
Tests saving, loading, search, and clearing translation history.
"""

import unittest
from src.history import save_translation, load_history, clear_history, get_recent


class TestHistory(unittest.TestCase):

    def setUp(self):
        """Clear history before each test."""
        clear_history()

    def tearDown(self):
        """Clear history after each test."""
        clear_history()

    def test_save_and_load(self):
        """Test saving and retrieving translations."""
        save_translation(
            source_text="Hello world",
            translated_text="नमस्ते दुनिया",
            source_lang="eng_Latn",
            target_lang="hin_Deva",
            translation_time=0.15,
        )

        history = load_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["source_text"], "Hello world")
        self.assertEqual(history[0]["translated_text"], "नमस्ते दुनिया")

    def test_get_recent(self):
        """Test retrieving N recent translations."""
        for i in range(5):
            save_translation(f"Text {i}", f"अनुवाद {i}", "eng_Latn", "hin_Deva")

        recent_3 = get_recent(3)
        self.assertEqual(len(recent_3), 3)
        self.assertEqual(recent_3[0]["source_text"], "Text 4")

    def test_clear_history(self):
        """Test clearing translation history."""
        save_translation("Test", "परीक्षण", "eng_Latn", "mar_Deva")
        clear_history()
        history = load_history()
        self.assertEqual(len(history), 0)


if __name__ == "__main__":
    unittest.main()
