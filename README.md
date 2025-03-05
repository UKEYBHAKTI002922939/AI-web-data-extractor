# AI-web-data-extractor

virtual environment
pip install .e -- setup.py

python -m rufus.main --url https://ai.pydantic.dev/ --depth 2 --output output.json



challenges:
not added logging logic crawled 81 urls

python main.py --url "https://www.sfgov.com" \
               --depth 2 \
               --instructions "scrape customer FAQ's" \
               --output "sfgov_report.json"




python main.py --url "https://ai.pydantic.dev" \
               --depth 2 \
               --instructions "scrape anything related to RAG" \
               --output "pydantic_report.json"



python main.py --url "https://www.python.org/" \
               --depth 2 \
               --instructions "scrape FAQ" \
               --output "reports/python_report.json"


issues with the summarizer part with sequential fetching initially
concurrent fetching
issues faced and improvement on working with 

What’s Changing?
Synchronous vs. Asynchronous:
The current crawler uses requests_html and sleeps between requests. In an asynchronous version, we use libraries like aiohttp and asyncio to concurrently fetch multiple pages, which speeds up the process.

Concurrency:
Instead of a recursive call that waits for each request to finish, an asynchronous implementation launches several requests at once (using tasks), then waits for them all to complete.

Breakdown of Changes in crawler.py:
aiohttp & asyncio:
We import and use aiohttp for asynchronous HTTP requests and asyncio for managing concurrency.

fetch_page(session, url):
An asynchronous function that replaces self.session.get(). It uses async with to handle the request and awaits the response text.

async_crawl(...):
A recursive asynchronous function that:

Checks if the current depth exceeds the maximum or if the URL was already visited.
Uses an aiohttp.ClientSession() to fetch the page.
Uses BeautifulSoup to parse the content and then calls clean_text() from your utils.
Checks relevance using your is_relevant() function.
Extracts and normalizes links using urljoin.
Waits for a delay (await asyncio.sleep(delay)).
Launches asynchronous tasks for each child link and waits for them concurrently with asyncio.gather().
Crawler Class Methods:

crawl_async: Public asynchronous method that initializes the visited set and starts the async crawling.
crawl: Synchronous wrapper that calls asyncio.run() on the async crawler, allowing you to call crawl() from synchronous code (e.g., in main.py).


# Example usage in a separate script or interactive shell

from Rufus import RufusClient
import os

# Get the API key from environment variables
key = os.getenv('Rufus_API_KEY', 'your-default-api-key')

client = RufusClient(api_key=key)

instructions = "Find information about product features and customer FAQs."
# Call the scrape method with a target URL and instructions
document = client.scrape("https://example.com", instructions=instructions)

print(document)
Rufus_API_KEY="rufus-dummy-key-2025"
export Rufus_API_KEY="dummy-key"

