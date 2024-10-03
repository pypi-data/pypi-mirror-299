# tests/test_summarizer.py

import unittest
from text_processor import TextSummarizer

class TestTextSummarizer(unittest.TestCase):

    def test_summarize(self):
        summarizer = TextSummarizer()
        result = summarizer.summarize("This is a very long text that needs to be summarized.", max_length=20, min_length=5)
        self.assertTrue(len(result) > 0)  # Ensure that a summary is returned
        print(f"Summary: {result}")

if __name__ == '__main__':
    unittest.main()
