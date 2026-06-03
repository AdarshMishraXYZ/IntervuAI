def calculate_overall_score(
    resume_score: int,
    github_score: int,
    leetcode_score: int
):
    return round(
        (
            resume_score +
            github_score +
            leetcode_score
        ) / 3
    )


def get_candidate_level(
    overall_score: int
):
    if overall_score >= 85:
        return "Advanced"

    if overall_score >= 70:
        return "Intermediate"

    return "Beginner"