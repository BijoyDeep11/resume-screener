def generate_recommendations(match_result: dict, under_emphasized: list = None) -> list:
    missing = match_result.get("missing_skills", [])

    suggestions = []

    # --- Missing skill advice ---
    for skill in missing:
        if skill in ["django", "flask"]:
            suggestions.append(
                "Add a backend project using Django or Flask and highlight API development."
            )
        elif skill in ["sql", "mysql", "postgresql"]:
            suggestions.append(
                "Showcase database usage by mentioning how you designed tables or optimized queries."
            )
        elif skill in ["docker"]:
            suggestions.append(
                "Learn Docker basics and add a simple containerized project to your resume."
            )
        elif skill in ["aws"]:
            suggestions.append(
                "Gain exposure to AWS by deploying a small app and mentioning it under projects."
            )
        else:
            suggestions.append(
                f"Consider adding experience or coursework related to {skill}."
            )

    # --- Under-emphasized strengths advice ---
    if under_emphasized:
        for skill in under_emphasized:
            suggestions.append(
                f"You already have experience with {skill}. Emphasize it more in your projects or achievements."
            )

    return suggestions[:5]


def find_under_emphasized_strengths(resume_text: str, jd_skills: list):
    """
    Finds skills that exist in resume but are mentioned only once,
    while being important in the JD.
    """
    text = resume_text.lower()
    strengths = []

    for skill in jd_skills:
        count = text.count(skill.lower())
        if count == 1:
            strengths.append(skill)

    return strengths

