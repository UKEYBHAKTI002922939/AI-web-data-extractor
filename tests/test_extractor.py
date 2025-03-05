import unittest
from rufus.extractor import extract_text

class TestExtractor(unittest.TestCase):
    def test_extract_text(self):
        text = extract_text("https://www.example.com")
        self.assertIsInstance(text, str)

if __name__ == "__main__":
    unittest.main()