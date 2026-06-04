def generate_questions_from_strategy(
    intelligence
):
    questions = []

    primary_focus = intelligence["interview_strategy"]["primary_focus"]

    for focus in primary_focus:

        if focus == "Resume project deep-dive":
            questions.append(
                "Choose the most technically challenging project from your resume and explain the architecture, technologies used, design decisions, and your exact contribution."
            )

        elif focus == "Project architecture and trade-offs":
            questions.append(
                "Describe a major design decision from one of your projects. What alternatives did you evaluate and why did you choose your final solution?"
            )

        elif focus == "Backend API design":
            questions.append(
                "Design the backend architecture for a production-ready interview platform similar to IntervuAI. Explain authentication, API structure, database design, scalability, and error handling."
            )

        elif focus == "Database design and SQL fundamentals":
            questions.append(
                "Design the database schema for an interview platform. Explain tables, relationships, indexing strategy, and query optimization."
            )

    questions.append(
        "Tell me about a difficult technical bug you encountered. Explain how you identified the root cause and fixed it."
    )

    return questions