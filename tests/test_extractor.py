# tests/test_extractor.py

import unittest
from rufus.extractor import extract_text

class TestExtractor(unittest.TestCase):
    def test_extract_text_returns_string(self):
        text = extract_text("https://www.example.com")
        self.assertIsInstance(text, str, "extract_text should return a string.")
        # Optionally: self.assertTrue(len(text) > 0, "Expected non-empty text.")

if __name__ == "__main__":
    unittest.main()
