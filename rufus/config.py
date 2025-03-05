# Configuration file for Rufus

# Default crawling depth
DEFAULT_CRAWL_DEPTH = 2

# Timeout for HTTP requests (in seconds)
HTTP_TIMEOUT = 5

# Summarization settings
SUMMARIZATION_MODEL = "facebook/bart-large-cnn"
CHUNK_SIZE = 500  # Number of words per chunk
SUMMARY_MIN_LENGTH = 40
SUMMARY_MAX_LENGTH = 150

# User Agent for web requests
USER_AGENT = "RufusBot/0.1 (+https://github.com/UKEYBHAKTI002922939/AI-web-data-extractor)"