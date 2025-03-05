# rufus/crawler.py

import asyncio
import logging
import time
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from rufus.config import DEFAULT_CRAWL_DEPTH, USER_AGENT, HTTP_TIMEOUT
from rufus.utils import is_relevant, clean_text

class Crawler:
    def __init__(self, max_depth=DEFAULT_CRAWL_DEPTH, delay=1, instructions="", dynamic=True):
        """
        Initialize the asynchronous crawler.
        
        :param max_depth: Maximum crawl depth.
        :param delay: Delay (in seconds) between requests.
        :param instructions: User-defined instructions to filter relevant pages.
        :param dynamic: If True, uses Playwright to render JavaScript and capture dynamic content.
        """
        self.max_depth = max_depth
        self.delay = delay
        self.instructions = instructions
        self.dynamic = dynamic

    async def fetch_page(self, url):
        """
        Asynchronously fetch page content.
        If self.dynamic is True, uses Playwright to render the page for JavaScript content.
        Otherwise, uses aiohttp for a simple fetch.
        """
        if self.dynamic:
            from playwright.async_api import async_playwright
            try:
                logging.info(f"Fetching page dynamically with Playwright: {url}")
                async with async_playwright() as p:
                    browser = await p.chromium.launch(headless=True)
                    page = await browser.new_page()
                    # Convert timeout to milliseconds for Playwright
                    await page.goto(url, timeout=HTTP_TIMEOUT * 1000)
                    content = await page.content()
                    await browser.close()
                    return content
            except Exception as e:
                logging.error(f"Failed to fetch {url} dynamically: {e}")
                return None
        else:
            try:
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, timeout=HTTP_TIMEOUT, headers={"User-Agent": USER_AGENT}) as response:
                        if response.status != 200:
                            logging.warning(f"Received status {response.status} for {url}")
                            return None
                        text = await response.text()
                        return text
            except Exception as e:
                logging.error(f"Failed to fetch {url} with aiohttp: {e}")
                return None

    async def _crawl_async(self, url, depth, visited):
        """
        Recursively crawl the website asynchronously up to max_depth.
        Only pages that satisfy the relevance criteria (based on instructions) are returned.
        """
        results = []
        if depth > self.max_depth or url in visited:
            return results

        visited.add(url)
        html_content = await self.fetch_page(url)
        if not html_content:
            return results

        soup = BeautifulSoup(html_content, "html.parser")
        extracted_text = clean_text(soup.get_text(separator="\n", strip=True))

        # Check relevance based on user instructions
        if self.instructions and not is_relevant(extracted_text, self.instructions):
            logging.info(f"Skipping {url} due to irrelevance.")
            return results

        logging.info(f"Content is relevant for: {url}")
        results.append({"url": url, "content": extracted_text})

        # Extract links and convert relative URLs to absolute
        links = [a.get("href") for a in soup.find_all("a", href=True)]
        full_links = set(urljoin(url, link) for link in links if link.startswith("http"))

        await asyncio.sleep(self.delay)  # Politeness delay

        tasks = []
        for link in full_links:
            if link not in visited:
                tasks.append(self._crawl_async(link, depth + 1, visited))
        if tasks:
            child_results = await asyncio.gather(*tasks)
            for sublist in child_results:
                results.extend(sublist)
        return results

    async def crawl_async(self, url):
        """
        Public method to start the asynchronous crawling process.
        """
        visited = set()
        return await self._crawl_async(url, depth=0, visited=visited)

    def crawl(self, url):
        """
        Synchronous wrapper to run the asynchronous crawler.
        """
        return asyncio.run(self.crawl_async(url))
