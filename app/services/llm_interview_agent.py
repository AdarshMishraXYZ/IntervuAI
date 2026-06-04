import json

from openai import OpenAI

from app.core.config import settings


client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


def generate_fallback_question(
    role: str,
    candidate_intelligence: dict,
    previous_qa: list
):
    primary_focus = candidate_intelligence.get(
        "interview_strategy",
        {}
    ).get(
        "primary_focus",
        []
    )

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

    if len(previous_qa) == 1:
        return {
            "question": (
                "Now explain one major trade-off you faced in that project. "
                "What alternatives did you consider and why did you choose your final approach?"
            ),
            "reason": "Fallback follow-up based on previous project answer",
            "difficulty": "Medium",
            "focus_area": "Project Trade-offs"
        }

    if len(previous_qa) == 2:
        return {
            "question": (
                f"For a {role} role, design the backend of an interview platform. "
                "Explain APIs, authentication, database schema, error handling, and scalability."
            ),
            "reason": "Fallback backend design question",
            "difficulty": "Medium",
            "focus_area": "Backend Design"
        }

    if len(previous_qa) == 3:
        return {
            "question": (
                "Design the database schema for an interview platform. "
                "Explain tables, relationships, indexes, and query optimization."
            ),
            "reason": "Fallback database design question",
            "difficulty": "Medium",
            "focus_area": "Database Design"
        }

    return {
        "question": (
            "Tell me about a difficult technical bug you faced. "
            "How did you identify the root cause, debug it, and prevent it from happening again?"
        ),
        "reason": "Fallback debugging question",
        "difficulty": "Medium",
        "focus_area": "Debugging"
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
            "Use the candidate intelligence, detected strengths, weaknesses, "
            "recommended roles, and interview strategy. "
            "The question must be personalized and should not be generic. "
            "If previous answers are shallow, ask a deeper follow-up. "
            "If previous answers are strong, move to the next important focus area. "
            "Return ONLY valid JSON with these exact keys: "
            "question, reason, difficulty, focus_area. "
            "Do not include markdown. Do not include explanation outside JSON."
        )
    }

    try:
        response = client.responses.create(
           model="gpt-4o-mini",
            input=json.dumps(prompt)
        )

        raw_text = response.output_text.strip()

        return json.loads(raw_text)

    except Exception as error:
        print("LLM interview agent failed:", repr(error), flush=True)

        return generate_fallback_question(
            role,
            candidate_intelligence,
            previous_qa
        )