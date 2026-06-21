"""
behavior_ranker.py
"""


class BehaviorRanker:

    @staticmethod
    def score(signals):

        score = 0

        if signals.get("open_to_work_flag"):
            score += 0.30

        if signals.get("verified_email"):
            score += 0.10

        if signals.get("verified_phone"):
            score += 0.10

        response = signals.get(
            "recruiter_response_rate",
            0
        )

        score += response * 0.30

        completion = signals.get(
            "profile_completeness_score",
            0
        )

        score += completion * 0.20

        return min(score, 1.0)