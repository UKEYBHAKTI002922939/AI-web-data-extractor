import unittest
from rufus.synthesizer import Synthesizer

class TestSynthesizer(unittest.TestCase):
    def test_synthesize(self):
        synthesizer = Synthesizer()
        input_text = "This is a test text. " * 100
        summary = synthesizer.synthesize(input_text)
        self.assertIsInstance(summary, str)
        self.assertTrue(len(summary) > 0)

if __name__ == "__main__":
    unittest.main()