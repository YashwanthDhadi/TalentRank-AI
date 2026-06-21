"""
experience_ranker.py
"""


class ExperienceRanker:

    @staticmethod
    def score(candidate_exp, jd_min, jd_max):

        if jd_min <= candidate_exp <= jd_max:
            return 1.0

        if candidate_exp < jd_min:

            diff = jd_min - candidate_exp

            return max(0, 1 - diff * 0.15)

        diff = candidate_exp - jd_max

        return max(0.5, 1 - diff * 0.05)