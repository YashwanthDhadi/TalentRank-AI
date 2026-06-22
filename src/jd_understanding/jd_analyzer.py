"""Analyze a job description for downstream ranking modules."""

import re

from src.skills.jd_skill_extractor import JDSkillExtractor


class JDAnalyzer:
    """Extract ranking inputs from a job description."""

    def __init__(self, jd_text: str):
        if not isinstance(jd_text, str) or not jd_text.strip():
            raise ValueError("Job description text must be a non-empty string.")
        self.jd_text = jd_text.lower()
        self.skill_extractor = JDSkillExtractor()

    def analyze(self) -> dict:
        """Return structured job-description signals for ranking."""
        return {
            "experience": self.extract_experience(),
            "required_skills": self.skill_extractor.extract(self.jd_text),
            "preferred_skills": self.extract_preferred_skills(),
            "negative_signals": self.extract_negative_signals(),
            "work_mode": self.extract_work_mode(),
        }

    def extract_experience(self) -> dict:
        """Extract experience bounds from the job description text."""
        match = re.search(
            r"experience required:\s*(\d+)\s*[â€“-]\s*(\d+)",
            self.jd_text,
        )
        if match:
            return {
                "min": int(match.group(1)),
                "max": int(match.group(2)),
            }
        return {"min": 0, "max": 100}

    def extract_preferred_skills(self) -> list[str]:
        """Extract preferred skills from keyword matches."""
        preferred = [
            "lora",
            "qlora",
            "peft",
            "learning-to-rank",
            "xgboost",
            "marketplace",
            "distributed systems",
            "open source",
        ]
        found: list[str] = []
        for skill in preferred:
            if skill.lower() in self.jd_text:
                found.append(skill)
        return sorted(found)

    def extract_negative_signals(self) -> list[str]:
        """Extract negative screening signals from keyword matches."""
        negatives = [
            "langchain",
            "consulting firms",
            "computer vision",
            "robotics",
            "speech",
        ]
        found: list[str] = []
        for signal in negatives:
            if signal.lower() in self.jd_text:
                found.append(signal)
        return found

    def extract_work_mode(self) -> str:
        """Infer work mode from the job description text."""
        if "hybrid" in self.jd_text:
            return "hybrid"
        if "remote" in self.jd_text:
            return "remote"
        return "onsite"
