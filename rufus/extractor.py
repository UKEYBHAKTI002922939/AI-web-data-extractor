import requests
from bs4 import BeautifulSoup
from rufus.config import HTTP_TIMEOUT, USER_AGENT
from rufus.utils import clean_text

def extract_text(url: str) -> str:
    """
    Extract and clean text content from a web page.
    """
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(url, timeout=HTTP_TIMEOUT, headers=headers)
        if response.status_code != 200:
            return ""
        soup = BeautifulSoup(response.text, "html.parser")
        # Remove unwanted tags (scripts, styles, etc.)
        for tag in soup(["script", "style"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)
        return clean_text(text)
    except Exception as e:
        print(f"Error extracting text from {url}: {e}")
        return ""
