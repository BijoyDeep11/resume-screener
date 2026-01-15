# scoring/final_score.py

def compute_final_score(
    skill_match_percent: float,
    semantic_similarity: float,
    experience_years: int,
    required_experience: int,
    has_required_degree: bool,
    keyword_similarity: float,
    weights: dict = None
) -> dict:
    """
    Combines multiple signals into one final match score (0–100).

    Default weights:
    - skills: 50%
    - experience: 30%
    - education: 10%
    - keywords: 10%
    """

    if weights is None:
        weights = {
            "skills": 0.5,
            "experience": 0.3,
            "education": 0.1,
            "keywords": 0.1
        }

    # -------------------
    # 1. Skill score
    # -------------------
    skill_score = skill_match_percent

    # -------------------
    # 2. Experience score
    # -------------------
    if required_experience > 0:
        exp_ratio = min(experience_years / required_experience, 1)
        experience_score = exp_ratio * 100
    else:
        experience_score = 50  # neutral if JD doesn't specify

    # -------------------
    # 3. Education score
    # -------------------
    education_score = 100 if has_required_degree else 50

    # -------------------
    # 4. Keyword score
    # -------------------
    keyword_score = keyword_similarity

    # -------------------
    # Final weighted score
    # -------------------
    final_score = (
        skill_score * weights["skills"] +
        experience_score * weights["experience"] +
        education_score * weights["education"] +
        keyword_score * weights["keywords"]
    )

    return {
    "final_match_percent": float(round(final_score, 2)),
    "breakdown": {
        "skills": float(round(skill_score, 2)),
        "experience": float(round(experience_score, 2)),
        "education": float(round(education_score, 2)),
        "keywords": float(round(keyword_score, 2))
    },
    "weights_used": weights
}

