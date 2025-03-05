# rufus/crawler.py

import logging
import time
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from rufus.config import DEFAULT_CRAWL_DEPTH, USER_AGENT, HTTP_TIMEOUT
from rufus.utils import is_relevant

class Crawler:
    def __init__(self, max_depth=DEFAULT_CRAWL_DEPTH, delay=1, instructions=""):
        """
        :param max_depth: Maximum crawl depth
        :param delay: Seconds to wait between requests
        :param instructions: User-defined instructions to filter relevant pages
        """
        self.max_depth = max_depth
        self.delay = delay
        self.instructions = instructions
        self.session = HTMLSession()

    def fetch_page(self, url):
        """
        Fetch page content using an HTML session and handle JavaScript.
        """
        try:
            logging.info(f"Fetching page: {url}")
            response = self.session.get(url, timeout=HTTP_TIMEOUT, headers={"User-Agent": USER_AGENT})
            # Attempt to render JavaScript if present
            response.html.render(timeout=10)
            return response.text
        except Exception as e:
            logging.error(f"Failed to fetch {url}: {str(e)}")
            return None

    def crawl(self, url, depth=0, visited=None):
        """
        Recursively crawl the website up to max_depth, returning relevant pages only.
        """
        if visited is None:
            visited = set()

        # Base cases
        if depth > self.max_depth or url in visited:
            return []

        visited.add(url)
        html_content = self.fetch_page(url)
        if not html_content:
            return []

        # Extract text
        soup = BeautifulSoup(html_content, "html.parser")
        extracted_text = soup.get_text(separator="\n", strip=True)

        # Filter out irrelevant pages based on instructions
        if self.instructions and not is_relevant(extracted_text, self.instructions):
            logging.info(f"Skipping {url} due to irrelevance.")
            return []

        # Gather the result for this page
        current_result = {
            "url": url,
            "content": extracted_text
        }

        # Extract & normalize links
        links = [a.get("href") for a in soup.find_all("a", href=True)]
        # Filter out only absolute HTTP(S) links
        from requests.compat import urljoin
        full_links = set()
        for link in links:
            # Convert relative links to absolute
            absolute = urljoin(url, link)
            if absolute.startswith("http"):
                full_links.add(absolute)

        time.sleep(self.delay)  # Politeness delay

        # Crawl child links recursively
        nested_results = []
        for link in full_links:
            nested_results.extend(self.crawl(link, depth + 1, visited))

        return [current_result] + nested_results
