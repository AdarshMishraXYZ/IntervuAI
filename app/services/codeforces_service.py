import requests


def fetch_codeforces_profile(username: str):
    url = "https://codeforces.com/api/user.info"

    response = requests.get(
        url,
        params={
            "handles": username
        },
        timeout=10
    )

    if response.status_code != 200:
        return None

    data = response.json()

    if data.get("status") != "OK":
        return None

    users = data.get("result", [])

    if len(users) == 0:
        return None

    user = users[0]

    return {
        "username": user.get("handle", username),
        "rating": user.get("rating", 0),
        "max_rating": user.get("maxRating", 0),
        "rank": user.get("rank", "unrated"),
        "max_rank": user.get("maxRank", "unrated"),
        "contribution": user.get("contribution", 0),
        "friend_count": user.get("friendOfCount", 0)
    }


def calculate_codeforces_score(
    rating: int,
    max_rating: int,
    contribution: int,
    friend_count: int
):
    score = 0

    score += min(rating // 40, 60)
    score += min(max_rating // 100, 25)
    score += min(max(contribution, 0), 10)
    score += min(friend_count // 20, 5)

    return min(score, 100)