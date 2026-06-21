"""
text_cleaner.py

Description:
    Cleans and normalizes text before AI processing.
"""

import re


class TextCleaner:
    """
    Utility class for cleaning text.
    """

    @staticmethod
    def clean(text: str) -> str:
        """
        Clean a piece of text.

        Steps:
        - Handle None
        - Convert to lowercase
        - Remove extra spaces
        - Remove special characters
        """

        if text is None:
            return ""

        text = text.lower()

        text = re.sub(r"\s+", " ", text)

        text = re.sub(r"[^a-z0-9\s]", "", text)

        return text.strip()