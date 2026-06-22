"""Read the job description from a DOCX file."""

from pathlib import Path

from docx import Document

from src.utils.artifact_utils import ensure_file_exists


class JobDescriptionLoader:
    """Read the job description from a DOCX file."""

    def __init__(self, jd_path: str):
        self.jd_path = Path(jd_path)

    def load(self) -> str:
        """Load and validate the job description text."""
        ensure_file_exists(self.jd_path, "job description")
        document = Document(self.jd_path)
        paragraphs: list[str] = []
        for paragraph in document.paragraphs:
            text = paragraph.text.strip()
            if text:
                paragraphs.append(text)
        jd_text = "\n".join(paragraphs).strip()
        if not jd_text:
            raise ValueError(
                f"Job description '{self.jd_path}' does not contain readable text."
            )
        return jd_text
