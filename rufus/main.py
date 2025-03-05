import argparse
import json
from rufus.crawler import Crawler
from rufus.extractor import extract_text
from rufus.synthesizer import Synthesizer

def main():
    parser = argparse.ArgumentParser(
        description="Rufus: AI-powered web scraper and synthesizer for RAG pipelines."
    )
    parser.add_argument("--url", type=str, required=True, help="Starting URL for crawling")
    parser.add_argument("--depth", type=int, default=2, help="Maximum crawl depth")
    parser.add_argument("--output", type=str, default="report.json", help="Output file for the synthesized document")
    args = parser.parse_args()

    # Initialize the crawler with the specified depth
    crawler = Crawler(max_depth=args.depth)
    urls = crawler.crawl(args.url)
    print(f"Found {len(urls)} URLs.")

    # Aggregate text content from all discovered URLs
    aggregated_text = ""
    for url in urls:
        text = extract_text(url)
        if text:
            aggregated_text += text + "\n\n"

    # Synthesize the aggregated text into a summary document
    synthesizer = Synthesizer()
    summary = synthesizer.synthesize(aggregated_text)

    # Save the output in JSON format
    output = {
        "source_url": args.url,
        "synthesized_summary": summary
    }
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f"Synthesized document saved to {args.output}")

if __name__ == "__main__":
    main()
