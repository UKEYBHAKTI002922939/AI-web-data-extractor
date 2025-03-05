# tests/test_extractor.py

import unittest
from rufus.extractor import extract_text

class TestExtractor(unittest.TestCase):
    def test_extract_text(self):
        text = extract_text("https://www.example.com")
        self.assertIsInstance(text, str, "Extracted text should be a string")

if __name__ == "__main__":
    unittest.main()
