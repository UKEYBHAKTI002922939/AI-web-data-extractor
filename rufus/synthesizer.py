from transformers import pipeline
from rufus.config import SUMMARIZATION_MODEL, CHUNK_SIZE, SUMMARY_MIN_LENGTH, SUMMARY_MAX_LENGTH
from rufus.utils import chunk_text

class Synthesizer:
    def __init__(self, model_name: str = SUMMARIZATION_MODEL):
        # Initialize the summarization pipeline
        self.summarizer = pipeline("summarization", model=model_name)

    def synthesize(self, text: str) -> str:
        """
        Summarize the given text into a structured summary.
        """
        chunks = chunk_text(text, CHUNK_SIZE)
        summaries = []
        for chunk in chunks:
            try:
                summary = self.summarizer(
                    chunk,
                    min_length=SUMMARY_MIN_LENGTH,
                    max_length=SUMMARY_MAX_LENGTH,
                    do_sample=False
                )
                summaries.append(summary[0]['summary_text'])
            except Exception as e:
                print(f"Summarization error: {e}")
        combined_text = " ".join(summaries)
        # Optional: re-summarize if multiple chunks were processed
        if len(summaries) > 1:
            try:
                final_summary = self.summarizer(
                    combined_text,
                    min_length=SUMMARY_MIN_LENGTH,
                    max_length=SUMMARY_MAX_LENGTH,
                    do_sample=False
                )
                return final_summary[0]['summary_text']
            except Exception as e:
                print(f"Final summarization error: {e}")
        return combined_text
