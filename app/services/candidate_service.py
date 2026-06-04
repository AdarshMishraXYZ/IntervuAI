def calculate_overall_score(
    resume_score: int,
    github_score: int,
    leetcode_score: int,
    codeforces_score: int
):
    return round(
        (
            resume_score * 0.70 +
            github_score * 0.10 +
            leetcode_score * 0.10 +
            codeforces_score * 0.10
        )
    )


def get_candidate_level(
    overall_score: int
):
    if overall_score >= 85:
        return "Advanced"

    if overall_score >= 70:
        return "Intermediate"

    return "Beginner"