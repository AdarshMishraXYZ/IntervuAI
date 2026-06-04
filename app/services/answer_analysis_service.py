def analyze_answer_quality(answer: str):
    words = answer.split()
    word_count = len(words)

    answer_lower = answer.lower()

    quality_signals = [
        "because",
        "architecture",
        "database",
        "api",
        "tradeoff",
        "scalable",
        "security",
        "testing",
        "deployment",
        "error"
    ]

    signal_count = 0

    for signal in quality_signals:
        if signal in answer_lower:
            signal_count += 1

    if word_count >= 80 and signal_count >= 3:
        return "strong"

    if word_count >= 40 and signal_count >= 1:
        return "moderate"

    return "weak"


def generate_follow_up_question(
    original_question: str,
    answer: str
):
    quality = analyze_answer_quality(answer)

    if quality == "strong":
        return None

    if "project" in original_question.lower():
        return "Your answer was brief. Can you explain the architecture, your exact contribution, and one technical challenge in more depth?"

    if "database" in original_question.lower():
        return "Can you explain the database tables, relationships, indexing choices, and how you would optimize slow queries?"

    if "backend" in original_question.lower() or "api" in original_question.lower():
        return "Can you explain the API endpoints, authentication flow, error handling, and how you would scale this backend?"

    return "Can you explain your answer in more technical depth with a concrete example?"