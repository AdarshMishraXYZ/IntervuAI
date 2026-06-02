import re

import fitz


SKILLS = [
    "python",
    "java",
    "javascript",
    "typescript",
    "react",
    "node",
    "fastapi",
    "django",
    "flask",
    "sql",
    "postgresql",
    "mongodb",
    "machine learning",
    "deep learning",
    "nlp",
    "computer vision",
    "docker",
    "git",
    "github",
    "aws"
]


def extract_text_from_pdf(file_path: str):
    document = fitz.open(file_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


def extract_skills(text: str):
    text_lower = text.lower()

    found_skills = []

    for skill in SKILLS:
        if skill in text_lower:
            found_skills.append(skill)

    return found_skills


def calculate_resume_score(skills: list[str], text: str):
    score = 0

    score += min(len(skills) * 8, 50)

    if "project" in text.lower() or "projects" in text.lower():
        score += 20

    if "experience" in text.lower() or "internship" in text.lower():
        score += 20

    if "education" in text.lower():
        score += 10

    return min(score, 100)


def analyze_resume_text(text: str):
    skills = extract_skills(text)

    score = calculate_resume_score(
        skills,
        text
    )

    return {
        "skills": skills,
        "resume_score": score,
        "text_preview": text[:1000]
    }