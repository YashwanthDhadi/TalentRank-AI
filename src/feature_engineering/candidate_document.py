"""
candidate_document.py

Description:
Builds a semantic document from a parsed candidate.
"""


class CandidateDocument:

    @staticmethod
    def build(candidate: dict) -> str:

        profile = []

        headline = candidate.get("headline", "")
        summary = candidate.get("summary", "")
        title = candidate.get("current_title", "")
        company = candidate.get("current_company", "")

        if headline:
            profile.append(headline)

        if summary:
            profile.append(summary)

        if title:
            profile.append(title)

        if company:
            profile.append(company)

        skills = [
            skill["name"]
            for skill in candidate.get("skills", [])
        ]

        if skills:
            profile.append("Skills: " + ", ".join(skills))

        careers = []

        for career in candidate.get("career_history", []):

            company = career.get("company", "")
            title = career.get("title", "")
            description = career.get("description", "")

            text = f"{title} {company} {description}".strip()

            if text:
                careers.append(text)

        if careers:
            profile.append("Career: " + " ".join(careers))

        education = []

        for edu in candidate.get("education", []):

            degree = edu.get("degree", "")
            field = edu.get("field_of_study", "")
            institute = edu.get("institution", "")

            text = f"{degree} {field} {institute}".strip()

            if text:
                education.append(text)

        if education:
            profile.append("Education: " + " ".join(education))

        return "\n".join(profile)