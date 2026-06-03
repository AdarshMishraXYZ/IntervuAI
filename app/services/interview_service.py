import json

from openai import OpenAI

from app.core.config import settings


client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


def generate_ai_interview_questions(
    role: str,
    candidate_level: str,
    resume_skills: str,
    github_score: int,
    leetcode_score: int,
    overall_score: int
):
    prompt = f"""
Generate 8 intelligent interview questions for a candidate.

Role: {role}
Candidate Level: {candidate_level}
Resume Skills: {resume_skills}
GitHub Score: {github_score}
LeetCode Score: {leetcode_score}
Overall Score: {overall_score}

Rules:
Return only valid JSON.
Do not add markdown.
Each question must have:
question
category
difficulty

Make questions personalized, practical, and realistic.
Include resume-based, GitHub-based, DSA, backend/system-design, and behavioral questions.
"""

    response = client.responses.create(
        model="gpt-5.5",
        input=prompt
    )

    return json.loads(response.output_text)