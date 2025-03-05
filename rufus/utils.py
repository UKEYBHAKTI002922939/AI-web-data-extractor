# rufus/utils.py

import re
import logging

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

def is_relevant(text: str, instructions: str) -> bool:
    """
    A simple function to check if the text is relevant to user instructions.
    For demonstration, we do a naive keyword check.
    """
    # Lowercase both text and instructions
    text_lower = text.lower()
    instructions_lower = instructions.lower()

    # Example: if *all* words in instructions are present in text
    # This can be replaced by an LLM approach for more accuracy
    instruction_words = instructions_lower.split()
    match_count = sum(1 for w in instruction_words if w in text_lower)
    threshold = len(instruction_words) * 0.5  # require at least half the words
    if match_count >= threshold:
        logging.info(f"Content is relevant based on instructions: {instructions}")
        return True
    logging.info("Content deemed irrelevant.")
    return False
