import requests


def fetch_leetcode_profile(username: str):
    url = "https://leetcode.com/graphql"

    query = """
    query getUserProfile($username: String!) {
      matchedUser(username: $username) {
        username
        submitStats {
          acSubmissionNum {
            difficulty
            count
          }
        }
      }
    }
    """

    payload = {
        "query": query,
        "variables": {
            "username": username
        }
    }

    response = requests.post(
        url,
        json=payload,
        timeout=10
    )

    if response.status_code != 200:
        return None

    data = response.json()

    matched_user = data.get("data", {}).get("matchedUser")

    if not matched_user:
        return None

    stats = matched_user["submitStats"]["acSubmissionNum"]

    result = {
        "username": matched_user["username"],
        "total_solved": 0,
        "easy_solved": 0,
        "medium_solved": 0,
        "hard_solved": 0
    }

    for item in stats:
        difficulty = item["difficulty"]
        count = item["count"]

        if difficulty == "All":
            result["total_solved"] = count

        if difficulty == "Easy":
            result["easy_solved"] = count

        if difficulty == "Medium":
            result["medium_solved"] = count

        if difficulty == "Hard":
            result["hard_solved"] = count

    return result


def calculate_leetcode_score(
    easy: int,
    medium: int,
    hard: int
):
    score = 0

    score += min(easy * 1, 25)
    score += min(medium * 2, 45)
    score += min(hard * 4, 30)

    return min(score, 100)