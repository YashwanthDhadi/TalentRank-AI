"""
career_ranker.py
"""


class CareerRanker:

    @staticmethod
    def score(history):

        if len(history) == 0:
            return 0

        return min(

            len(history) / 5,

            1.0

        )