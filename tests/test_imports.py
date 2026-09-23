"""
BhashaAI — Import Verification Tests
Ensures all key packages and internal modules can be imported without errors.
"""

import unittest


class TestImports(unittest.TestCase):

    def test_internal_module_imports(self):
        """Test importing custom BhashaAI modules."""
        from src import config
        from src import language_detector
        from src import text_processor
        from src import evaluator
        from src import history
        from src import document_processor

        self.assertTrue(hasattr(config, "SUPPORTED_LANGUAGES"))
        self.assertTrue(hasattr(config, "MODEL_NAME"))


if __name__ == "__main__":
    unittest.main()
