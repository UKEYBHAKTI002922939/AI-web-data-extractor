# tests/test_synthesizer.py

import unittest
from rufus.synthesizer import Synthesizer

class TestSynthesizer(unittest.TestCase):
    def test_synthesize(self):
        synthesizer = Synthesizer()
        input_text = "This is a test text. " * 100  # Repeat to simulate a longer text
        summary = synthesizer.synthesize(input_text)
        self.assertIsInstance(summary, str, "Synthesizer output should be a string.")
        self.assertTrue(len(summary) > 0, "Summary should not be empty.")

if __name__ == "__main__":
    unittest.main()
