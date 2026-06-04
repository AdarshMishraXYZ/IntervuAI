def generate_candidate_intelligence(
    resume_score: int,
    github_score: int,
    leetcode_score: int,
    codeforces_score: int,
    skills: str
):
    skills_lower = skills.lower() if skills else ""

    strengths = []
    weaknesses = []
    interview_focus = []
    recommended_roles = []
    learning_areas = []

    if resume_score >= 75:
        strengths.append("Strong resume foundation with relevant project exposure")
    else:
        weaknesses.append("Resume needs stronger project explanation and measurable impact")
        learning_areas.append("Resume storytelling and project documentation")

    if github_score >= 60:
        strengths.append("Good project visibility through GitHub")
    else:
        weaknesses.append("GitHub profile needs more polished public repositories")
        learning_areas.append("GitHub project structure, README writing, and clean commits")

    if leetcode_score >= 50:
        strengths.append("Good DSA practice through LeetCode")
    else:
        weaknesses.append("LeetCode problem-solving signal is currently weak")
        learning_areas.append("Arrays, strings, hashing, two pointers, and sliding window")

    if codeforces_score >= 70:
        strengths.append("Strong competitive programming signal")
    else:
        weaknesses.append("Competitive programming consistency can be improved")
        learning_areas.append("Greedy, binary search, dynamic programming, and graph basics")

    if "python" in skills_lower:
        strengths.append("Python programming foundation")
        recommended_roles.append("Backend Developer Intern")

    if "javascript" in skills_lower or "node" in skills_lower:
        strengths.append("Web development exposure")
        recommended_roles.append("Full Stack Developer Intern")

    if "git" in skills_lower or "github" in skills_lower:
        strengths.append("Version control awareness")

    if "sql" not in skills_lower and "postgresql" not in skills_lower:
        weaknesses.append("Database and SQL fundamentals need improvement")
        learning_areas.append("SQL joins, indexing, transactions, and schema design")

    interview_focus = [
        "Resume project deep-dive",
        "Project architecture and trade-offs",
        "Backend API design",
        "Database design and SQL fundamentals",
        "Problem-solving approach",
        "Communication clarity"
    ]

    if codeforces_score >= 70:
        interview_focus.append("Competitive programming reasoning under time pressure")

    if not recommended_roles:
        recommended_roles.append("Software Engineering Intern")

    confidence_score = round(
        resume_score * 0.40
        + github_score * 0.10
        + leetcode_score * 0.10
        + codeforces_score * 0.10
        + 70 * 0.30
    )

    if confidence_score >= 85:
        candidate_type = "Advanced Technical Candidate"
        next_best_action = "Take a senior-level mock interview and prepare for system design rounds"
    elif confidence_score >= 70:
        candidate_type = "Promising Intermediate Candidate"
        next_best_action = "Start targeted mock interviews and improve weak areas before internship applications"
    elif confidence_score >= 55:
        candidate_type = "Developing Candidate"
        next_best_action = "Strengthen fundamentals and complete 2-3 polished projects before applying widely"
    else:
        candidate_type = "Early Stage Candidate"
        next_best_action = "Focus on fundamentals, project building, and beginner interview practice"

    candidate_summary = (
        "The candidate shows a developing technical profile built from resume signals, "
        "coding platform activity, GitHub visibility, and detected technical skills. "
        "The profile suggests potential for internship roles, with interview focus needed "
        "on project depth, backend fundamentals, and communication clarity."
    )

    return {
        "candidate_type": candidate_type,
        "confidence_score": confidence_score,
        "candidate_summary": candidate_summary,
        "technical_profile": {
            "resume_score": resume_score,
            "github_score": github_score,
            "leetcode_score": leetcode_score,
            "codeforces_score": codeforces_score,
            "detected_skills": skills
        },
        "strengths": strengths,
        "weaknesses": weaknesses,
        "interview_strategy": {
            "primary_focus": interview_focus[:4],
            "secondary_focus": interview_focus[4:]
        },
        "recommended_roles": recommended_roles,
        "recommended_learning_areas": learning_areas,
        "next_best_action": next_best_action
    }