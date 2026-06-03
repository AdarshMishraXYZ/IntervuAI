import requests


def fetch_github_profile(username: str):
    url = f"https://api.github.com/users/{username}"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    return response.json()


def calculate_github_score(
    repos: int,
    followers: int
):
    score = 0

    score += min(repos * 2, 60)
    score += min(followers, 40)

    return min(score, 100)