def generate_recommendations(match_result: dict) -> list:
    missing = match_result.get("missing_skills", [])

    suggestions = []

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

    # Limit to top 5 suggestions
    return suggestions[:5]
