import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Set
from rufus.config import HTTP_TIMEOUT, USER_AGENT

class Crawler:
    def __init__(self, max_depth: int = 2):
        self.max_depth = max_depth
        self.visited: Set[str] = set()

    def crawl(self, url: str, depth: int = 0) -> List[str]:
        """
        Recursively crawl a website up to the given depth.
        Returns a list of discovered URLs.
        """
        if depth > self.max_depth or url in self.visited:
            return []
        self.visited.add(url)
        print(f"Crawling: {url}")
        try:
            headers = {'User-Agent': USER_AGENT}
            response = requests.get(url, timeout=HTTP_TIMEOUT, headers=headers)
            if response.status_code != 200:
                return []
            content = response.text
            soup = BeautifulSoup(content, "html.parser")
            links = []
            for a in soup.find_all("a", href=True):
                link = urljoin(url, a["href"])
                if self.is_valid_url(link):
                    links.append(link)
            # Recursively crawl the discovered links
            crawled_links = [url]
            for link in links:
                crawled_links.extend(self.crawl(link, depth + 1))
            return list(set(crawled_links))
        except Exception as e:
            print(f"Error crawling {url}: {e}")
            return []

    def is_valid_url(self, url: str) -> bool:
        """
        Check if a URL is valid.
        """
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)
