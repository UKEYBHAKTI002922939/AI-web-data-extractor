# tests/test_crawler.py

import unittest
from rufus.crawler import Crawler

DUMMY_HTML = """
<html>
  <head><title>Dummy Page</title></head>
  <body>
    <p>This page contains product features and customer FAQs for testing purposes.</p>
    <a href="https://example.com/page2">Page 2</a>
  </body>
</html>
"""

class DummyCrawler(Crawler):
    async def fetch_page(self, session, url):
        # Instead of making a network call, return our dummy HTML.
        return DUMMY_HTML

class TestCrawler(unittest.TestCase):
    def test_crawl_returns_relevant_page(self):
        instructions = "product features customer FAQs"
        crawler = DummyCrawler(max_depth=1, instructions=instructions)
        results = crawler.crawl("https://example.com")
        # We expect at least one page (the seed) to be returned.
        self.assertTrue(len(results) > 0, "Expected at least one result.")
        # Verify that the content contains the keywords (in lowercase).
        self.assertIn("product features", results[0]["content"].lower(), "Expected content to include 'product features'")

if __name__ == "__main__":
    unittest.main()
