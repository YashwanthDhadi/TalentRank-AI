"""
dataset_analyzer.py

Description:
    Generates useful dataset statistics.
"""

from collections import Counter


class DatasetAnalyzer:

    def __init__(self, candidate_loader):

        self.loader = candidate_loader

    def total_candidates(self):

        return self.loader.candidate_count()

    def average_skills(self):

        total = 0

        count = 0

        for candidate in self.loader.stream_candidates():

            skills = candidate.get("skills", [])

            total += len(skills)

            count += 1

        if count == 0:
            return 0

        return round(total / count, 2)

    def countries(self):

        counter = Counter()

        for candidate in self.loader.stream_candidates():

            profile = candidate.get("profile", {})

            country = profile.get("country")

            if country:
                counter[country] += 1

        return counter

    def experience_distribution(self):

        counter = Counter()

        for candidate in self.loader.stream_candidates():

            profile = candidate.get("profile", {})

            years = profile.get("years_of_experience", 0)

            counter[years] += 1

        return counter