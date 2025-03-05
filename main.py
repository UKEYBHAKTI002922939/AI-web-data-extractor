# main.py

import argparse
import json
import logging
import os

from rufus.crawler import Crawler
from rufus.extractor import extract_text
from rufus.synthesizer import Synthesizer
from rufus.config import LOG_FILE, LOG_LEVEL

def setup_logging():
    """
    Configure logging for the entire application.
    """
    log_dir = os.path.join("rufus", "logs")
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(
        filename=os.path.join(log_dir, LOG_FILE),
        level=getattr(logging, LOG_LEVEL),
        format='%(asctime)s [%(levelname)s] %(name)s - %(message)s'
    )
    console = logging.StreamHandler()
    console.setLevel(getattr(logging, LOG_LEVEL))
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

def main():
    setup_logging()
    logging.info("Starting Rufus...")

    parser = argparse.ArgumentParser(
        description="Rufus: AI-powered web scraper and synthesizer for RAG pipelines."
    )
    parser.add_argument("--url", type=str, required=True, help="Starting URL for crawling")
    parser.add_argument("--depth", type=int, default=2, help="Maximum crawl depth")
    parser.add_argument("--instructions", type=str, default="", help="User instructions (e.g., 'scrape customer FAQs')")
    parser.add_argument("--output", type=str, default="report.json", help="Output file for the synthesized document")
    args = parser.parse_args()

    # Initialize the asynchronous crawler with the specified depth and instructions
    crawler = Crawler(max_depth=args.depth, instructions=args.instructions)
    results = crawler.crawl(args.url)
    logging.info(f"Found {len(results)} relevant pages after filtering.")

    # Aggregate text content from all discovered pages
    aggregated_text = "\n\n".join(item["content"] for item in results if item["content"])

    # Summarize the aggregated text
    synthesizer = Synthesizer()
    summary = synthesizer.synthesize(aggregated_text)

    # Prepare structured output
    output = {
        "source_url": args.url,
        "instructions": args.instructions,
        "summary": summary,
        "pages_found": len(results)
    }

    # Save to JSON
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    logging.info(f"Synthesized document saved to {args.output}")

if __name__ == "__main__":
    main()
