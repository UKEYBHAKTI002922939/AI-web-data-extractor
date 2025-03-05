import re

def clean_text(text: str) -> str:
    """
    Clean and normalize text by removing extra whitespace.
    """
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def chunk_text(text: str, max_words: int) -> list:
    """
    Split text into chunks of up to `max_words` words.
    """
    words = text.split()
    return [" ".join(words[i:i+max_words]) for i in range(0, len(words), max_words)]
