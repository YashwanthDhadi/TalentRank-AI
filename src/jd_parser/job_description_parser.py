"""
job_description_parser.py

Description:
Parses the job description into structured information.
"""

import re


class JobDescriptionParser:

    def __init__(self, jd_text: str):

        self.jd_text = jd_text

    def parse(self):

        return {

            "job_title": self.extract_job_title(),

            "company": self.extract_company(),

            "location": self.extract_location(),

            "employment_type": self.extract_employment_type(),

            "experience": self.extract_experience(),

            "full_text": self.jd_text
        }

    def extract_job_title(self):

        match = re.search(
            r"Job Description:\s*(.+)",
            self.jd_text
        )

        if match:
            return match.group(1).strip()

        return ""

    def extract_company(self):

        match = re.search(
            r"Company:\s*(.+)",
            self.jd_text
        )

        if match:
            return match.group(1).strip()

        return ""

    def extract_location(self):

        match = re.search(
            r"Location:\s*(.+)",
            self.jd_text
        )

        if match:
            return match.group(1).strip()

        return ""

    def extract_employment_type(self):

        match = re.search(
            r"Employment Type:\s*(.+)",
            self.jd_text
        )

        if match:
            return match.group(1).strip()

        return ""

    def extract_experience(self):

        match = re.search(
            r"Experience Required:\s*(\d+)\s*[–-]\s*(\d+)",
            self.jd_text
        )

        if match:

            return {
                "min": int(match.group(1)),
                "max": int(match.group(2))
            }

        return {
            "min": 0,
            "max": 100
        }