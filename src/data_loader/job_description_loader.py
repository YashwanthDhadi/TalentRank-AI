"""
job_description_loader.py

Description:
    Reads the Job Description from DOCX.
"""

from pathlib import Path
from docx import Document


class JobDescriptionLoader:

    def __init__(self, jd_path: str):

        self.jd_path = Path(jd_path)

    def load(self) -> str:

        document = Document(self.jd_path)

        paragraphs = []

        for paragraph in document.paragraphs:

            text = paragraph.text.strip()

            if text:
                paragraphs.append(text)

        return "\n".join(paragraphs)