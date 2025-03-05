import unittest
from rufus.crawler import Crawler

class TestCrawler(unittest.TestCase):
    def test_is_valid_url(self):
        crawler = Crawler()
        self.assertTrue(crawler.is_valid_url("https://example.com"))
        self.assertFalse(crawler.is_valid_url("not_a_url"))

if __name__ == "__main__":
    unittest.main()
