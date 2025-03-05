# Rufus: AI-Powered Web Data Extractor for RAG Pipelines

Rufus is an AI-powered web data extractor designed to prepare content for Retrieval-Augmented Generation (RAG) agents. It intelligently crawls websites based on user-defined prompts, selectively extracts relevant data, and synthesizes the information into structured documents (JSON) that can be directly integrated into your RAG pipelines.

## Features

- **Intelligent Crawling:**  
  Crawl websites recursively with a configurable depth and follow nested links.

- **Dynamic Content Rendering:**  
  Uses Playwright’s async API to render pages with JavaScript, ensuring dynamic content is captured.

- **Selective Extraction:**  
  Filters pages based on user-defined instructions (e.g., "scrape customer FAQs").

- **Document Synthesis:**  
  Aggregates and summarizes content using a transformers-based summarization pipeline (facebook/bart-large-cnn).

- **Robust Error Handling & Logging:**  
  Comprehensive logging and error management ensure reliability and ease of debugging.

- **Intuitive API:**  
  Provides an easy-to-use client interface (`RufusClient`) for integration into RAG pipelines.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/AI-web-data-extractor.git
   cd AI-web-data-extractor
   ```

2. **Set Up the Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright (for dynamic content rendering):**
   ```bash
   pip install playwright
   playwright install
   ```

## Usage

### Command-Line Interface (CLI)

Run Rufus from the command line by providing a URL, maximum crawl depth, and instructions:

```bash
python main.py --url "https://example.com" --depth 2 --instructions "scrape customer FAQs" --output "reports/report.json"

python main.py --url "https://ai.pydantic.dev" \
               --depth 2 \
               --instructions "scrape anything related to RAG" \
               --output "reports/pydantic_report.json"
```

### Programmatic API

You can also use Rufus as a Python module:

```python
pip install Rufus

from Rufus import RufusClient
import os

# Get the API key from environment variables (dummy key during development)
key = os.getenv('Rufus_API_KEY', 'rufus-dummy-key-2025')
client = RufusClient(api_key=key)

instructions = "Find information about product features and customer FAQs."
document = client.scrape("https://example.com", instructions=instructions)
print(document)
```

## Testing

Run all unit tests using the following command:

```bash
python -m unittest discover
```

This will execute tests in the `tests/` folder and output the results.

## Integration into a RAG Pipeline

Rufus outputs a structured JSON document that includes:
- `source_url`
- `instructions`
- `synthesized_summary`
- `pages_found`

You can feed this JSON directly into your RAG system, allowing downstream LLMs to use the structured content for generating enhanced responses.

## Project Structure

```
AI-web-data-extractor/
├── rufus/
│   ├── __init__.py        # Exports RufusClient
│   ├── client.py          # RufusClient API wrapper
│   ├── config.py          # Configuration settings
│   ├── crawler.py         # Asynchronous crawler with dynamic content support
│   ├── extractor.py       # Text extraction and cleaning
│   ├── synthesizer.py     # Content summarization
│   ├── utils.py           # Utility functions (clean_text, is_relevant, chunk_text)
│   └── logs/              # Log files
│       └── rufus.log
├── tests/                 # Unit tests
├── main.py                # Command-line interface for Rufus
├── requirements.txt       # Python dependencies
├── README.md              # Project overview and usage instructions
└── setup.py               # Packaging configuration
```

