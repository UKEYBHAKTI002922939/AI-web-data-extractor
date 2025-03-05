# rufus/extractor.py

import logging
import requests
from bs4 import BeautifulSoup
from rufus.config import HTTP_TIMEOUT, USER_AGENT
from rufus.utils import clean_text

def extract_text(url: str) -> str:
    """
    Extract and clean text content from a web page.
    Returns an empty string if extraction fails.
    """
    try:
        logging.info(f"Extracting text from: {url}")
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(url, timeout=HTTP_TIMEOUT, headers=headers)
        if response.status_code != 200:
            logging.warning(f"Received status {response.status_code} for {url}")
            return ""

        soup = BeautifulSoup(response.text, "html.parser")
        # Remove scripts and styles
        for tag in soup(["script", "style"]):
            tag.decompose()

        raw_text = soup.get_text(separator=" ", strip=True)
        return clean_text(raw_text)
    except Exception as e:
        logging.error(f"Error extracting text from {url}: {e}")
        return ""
