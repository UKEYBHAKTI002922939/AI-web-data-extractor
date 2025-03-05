# tests/test_crawler.py

import unittest
from rufus.crawler import Crawler
from rufus.utils import clean_text

# Dummy HTML content that simulates a page with relevant content
DUMMY_HTML = """
<html>
  <head><title>Test Page</title></head>
  <body>
    <p>This page contains product features and customer FAQs for testing purposes.</p>
    <a href="https://example.com/page2">Page 2</a>
  </body>
</html>
"""

# DummyCrawler overrides fetch_page to return our DUMMY_HTML instead of doing a real HTTP request
class DummyCrawler(Crawler):
    def fetch_page(self, url):
        return DUMMY_HTML

class TestCrawler(unittest.TestCase):
    def test_crawl_returns_relevant_page(self):
        # Use instructions that match content in DUMMY_HTML
        instructions = "product features customer FAQs"
        crawler = DummyCrawler(max_depth=1, instructions=instructions)
        results = crawler.crawl("https://example.com")
        self.assertTrue(len(results) > 0, "Expected at least one result.")
        self.assertIn("product features", results[0]["content"].lower(),
                      "Content should include 'product features'.")

    def test_crawl_skips_irrelevant_page(self):
        # Use instructions that don't appear in DUMMY_HTML
        instructions = "nonexistent keyword"
        crawler = DummyCrawler(max_depth=1, instructions=instructions)
        results = crawler.crawl("https://example.com")
        self.assertEqual(len(results), 0, "Expected no results as content is irrelevant.")

if __name__ == "__main__":
    unittest.main()
