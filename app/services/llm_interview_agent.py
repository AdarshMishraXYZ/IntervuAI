import json

from google import genai

from app.core.config import settings


gemini_client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


def generate_fallback_question(
    role: str,
    candidate_intelligence: dict,
    previous_qa: list
):
    if len(previous_qa) == 0:
        return {
            "question": (
                "Based on your profile, choose your most technically challenging "
                "project and explain the architecture, technologies used, design "
                "decisions, and your exact contribution."
            ),
            "reason": "Fallback question based on project depth",
            "difficulty": "Medium",
            "focus_area": "Project Architecture"
        }

    return {
        "question": (
            f"For a {role} role, explain one technical decision from your project "
            "and justify it with trade-offs."
        ),
        "reason": "Fallback adaptive follow-up",
        "difficulty": "Medium",
        "focus_area": "Project Trade-offs"
    }


def generate_llm_interview_question(
    role: str,
    candidate_intelligence: dict,
    previous_qa: list
):
    prompt = {
        "target_role": role,
        "candidate_intelligence": candidate_intelligence,
        "previous_questions_and_answers": previous_qa,
        "instruction": (
            "You are IntervuAI, a serious technical interviewer. "
            "Generate exactly one next interview question. "
            "Use the candidate intelligence, strengths, weaknesses, recommended roles, "
            "and interview strategy. The question must be personalized and not generic. "
            "If previous answers are shallow, ask a deeper follow-up. "
            "If previous answers are strong, move to the next important focus area. "
            "Return ONLY valid JSON with exact keys: question, reason, difficulty, focus_area. "
            "No markdown. No explanation outside JSON."
        )
    }

    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=json.dumps(prompt)
        )

        raw_text = response.text.strip()

        if raw_text.startswith("```"):
            raw_text = raw_text.replace("```json", "").replace("```", "").strip()

        return json.loads(raw_text)

    except Exception as error:
        print("Gemini interview agent failed:", repr(error), flush=True)

        return generate_fallback_question(
            role,
            candidate_intelligence,
            previous_qa
        )