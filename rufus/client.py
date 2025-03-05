# rufus/client.py

import asyncio
import logging
from rufus.config import DEFAULT_CRAWL_DEPTH
from rufus.crawler import Crawler
from rufus.synthesizer import Synthesizer

class RufusClient:
    def __init__(self, api_key: str):
        """
        Initialize the Rufus client with an API key.
        (The API key can be used later for authentication or to configure external services.)
        """
        self.api_key = api_key
        logging.info("RufusClient initialized.")

    def scrape(self, url: str, instructions: str = "", depth: int = None) -> dict:
        """
        Crawl the given URL with user-defined instructions, synthesize the relevant content,
        and return a structured document.
        
        :param url: Starting URL for crawling.
        :param instructions: Brief instructions (e.g., "Find information about product features and customer FAQs").
        :param depth: Maximum crawl depth (defaults to DEFAULT_CRAWL_DEPTH if not provided).
        :return: Dictionary containing the source URL, instructions, synthesized summary, and count of pages found.
        """
        if depth is None:
            depth = DEFAULT_CRAWL_DEPTH

        visited = set()
        logging.info(f"Starting asynchronous crawl at {url} with depth={depth} and instructions: '{instructions}'")
        
        # Run the async crawl; using asyncio.get_event_loop() for compatibility
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(
            async_crawl(url, depth=0, max_depth=depth, visited=visited, instructions=instructions, delay=1.0)
        )
        logging.info(f"Found {len(results)} relevant pages after filtering.")
        
        # Aggregate text content from all relevant pages
        aggregated_text = "\n\n".join(item["content"] for item in results if item["content"])
        logging.info("Aggregated text content from all pages.")

        # Use the Synthesizer to summarize the aggregated text
        synthesizer = Synthesizer()
        summary = synthesizer.synthesize(aggregated_text)
        logging.info("Summarization complete.")

        # Build structured output
        output = {
            "source_url": url,
            "instructions": instructions,
            "synthesized_summary": summary,
            "pages_found": len(results)
        }
        logging.info("Returning structured output from RufusClient.scrape().")
        return output
