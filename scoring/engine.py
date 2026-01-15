from nlp.skills import extract_skills

def calculate_match_score(profile: dict, jd_text: str) -> dict:
    resume_skills = set(profile.get("skills", []))

    # 🔑 Extract skills from JD as well
    jd_skills = set(extract_skills(jd_text))

    matched = list(resume_skills & jd_skills)
    missing = list(jd_skills - resume_skills)

    skill_score = 0
    if jd_skills:
        skill_score = (len(matched) / len(jd_skills)) * 100

    return {
        "skill_match_percent": round(skill_score, 2),
        "matched_skills": matched,
        "missing_skills": missing,
        "jd_skills": list(jd_skills)
    }
