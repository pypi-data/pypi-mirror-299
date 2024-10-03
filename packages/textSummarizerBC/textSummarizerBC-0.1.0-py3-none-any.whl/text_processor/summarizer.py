# text_processor/summarizer.py

from transformers import pipeline

class TextSummarizer:
    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        self.summarizer = pipeline("summarization", model=model_name)

    def summarize(self, text: str, max_length: int = 150, min_length: int = 40, do_sample: bool = False) -> str:
        """
        Summarize the input text.
        Args: text (str): The text to summarize. max_length (int): The maximum length of the summary.
            min_length (int): The minimum length of the summary. do_sample (bool): Whether to sample the summary output.
        Returns:
            str: The summarized text.
        """
        summary = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=do_sample)
        return summary[0]['summary_text']
