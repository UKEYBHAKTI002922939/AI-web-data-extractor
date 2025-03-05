# rufus/crawler.py

import asyncio
import logging
import time
from urllib.parse import urljoin

import aiohttp
from bs4 import BeautifulSoup
from rufus.config import DEFAULT_CRAWL_DEPTH, USER_AGENT, HTTP_TIMEOUT
from rufus.utils import is_relevant, clean_text

async def fetch_page(session, url):
    """
    Asynchronously fetch page content using aiohttp.
    Returns the page text if successful, or None on failure.
    """
    try:
        logging.info(f"Fetching page: {url}")
        async with session.get(url, timeout=HTTP_TIMEOUT, headers={"User-Agent": USER_AGENT}) as response:
            if response.status != 200:
                logging.warning(f"Received status {response.status} for {url}")
                return None
            text = await response.text()
            return text
    except Exception as e:
        logging.error(f"Failed to fetch {url}: {e}")
        return None

async def async_crawl(url, depth, max_depth, visited, instructions, delay):
    """
    Recursively crawl the website asynchronously up to max_depth.
    Only pages that satisfy the relevance criteria (based on instructions) are returned.
    """
    results = []
    if depth > max_depth or url in visited:
        return results

    visited.add(url)
    page_content = None

    # Use a single session for this call and its children.
    async with aiohttp.ClientSession() as session:
        page_content = await fetch_page(session, url)
    
    if not page_content:
        return results

    soup = BeautifulSoup(page_content, "html.parser")
    # Clean and extract text
    extracted_text = clean_text(soup.get_text(separator="\n", strip=True))

    # Check relevance
    if instructions and not is_relevant(extracted_text, instructions):
        logging.info(f"Skipping {url} due to irrelevance.")
        return results

    logging.info(f"Content is relevant for: {url}")
    results.append({"url": url, "content": extracted_text})

    # Extract links and convert relative to absolute
    links = [a.get("href") for a in soup.find_all("a", href=True)]
    full_links = set(urljoin(url, link) for link in links if link.startswith("http"))

    # Respect a politeness delay before launching child crawls
    await asyncio.sleep(delay)

    # Launch asynchronous crawl for child links
    tasks = [
        async_crawl(link, depth + 1, max_depth, visited, instructions, delay)
        for link in full_links if link not in visited
    ]
    if tasks:
        child_results = await asyncio.gather(*tasks)
        for sublist in child_results:
            results.extend(sublist)
    return results

class Crawler:
    def __init__(self, max_depth=DEFAULT_CRAWL_DEPTH, delay=1, instructions=""):
        """
        Initialize the asynchronous crawler.
        :param max_depth: Maximum crawl depth.
        :param delay: Delay between requests.
        :param instructions: User-defined instructions to filter relevant pages.
        """
        self.max_depth = max_depth
        self.delay = delay
        self.instructions = instructions

    async def crawl_async(self, url):
        """
        Public method to start the asynchronous crawling process.
        """
        visited = set()
        return await async_crawl(url, depth=0, max_depth=self.max_depth, visited=visited,
                                 instructions=self.instructions, delay=self.delay)

    def crawl(self, url):
        """
        Synchronous wrapper to run the asynchronous crawler.
        """
        return asyncio.run(self.crawl_async(url))
