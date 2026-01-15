from processing.parser import parse_resume, parse_text_file, extract_required_experience
from processing.cleaner import clean_text
from nlp.extractor import split_into_sections, build_profile

from scoring.similarity import compute_similarity, compute_semantic_similarity
from scoring.engine import calculate_match_score
from scoring.final_score import compute_final_score

from recommendations.advisor import (
    generate_recommendations,
    find_under_emphasized_strengths
)

if __name__ == "__main__":
    resume_path = "data/resumes/sample_resume.pdf"
    jd_path = "data/jds/sample_jd.txt"

    # -------------------------
    # Resume pipeline
    # -------------------------
    raw_resume = parse_resume(resume_path)
    clean_resume = clean_text(raw_resume)
    sections = split_into_sections(clean_resume)
    profile = build_profile(sections)

    # -------------------------
    # JD pipeline
    # -------------------------
    jd_text = parse_text_file(jd_path)
    clean_jd = clean_text(jd_text)

    # -------------------------
    # Similarity
    # -------------------------
    similarity_score = compute_similarity(clean_resume, clean_jd)
    semantic_score = compute_semantic_similarity(clean_resume, clean_jd)

    # -------------------------
    # Skill matching
    # -------------------------
    skill_result = calculate_match_score(profile, clean_jd)

    # -------------------------
    # Final weighted score
    # -------------------------
    required_exp = extract_required_experience(clean_jd)
    has_degree = "btech" in profile.get("education", [])

    final_score_result = compute_final_score(
        skill_match_percent=skill_result["skill_match_percent"],
        semantic_similarity=semantic_score,
        experience_years=profile["experience_years"],
        required_experience=required_exp,
        has_required_degree=has_degree,
        keyword_similarity=similarity_score
    )

    # -------------------------
    # Under-emphasized strengths
    # -------------------------
    under_emphasized = find_under_emphasized_strengths(
        resume_text=clean_resume,
        jd_skills=skill_result["jd_skills"]
    )

    # -------------------------
    # Recommendations
    # -------------------------
    suggestions = generate_recommendations(
        skill_result,
        under_emphasized=under_emphasized
    )

    # -------------------------
    # OUTPUT
    # -------------------------

    print("\n====== MATCH RESULTS ======")
    print(f"TF-IDF Similarity: {similarity_score}%")
    print(f"Semantic Similarity: {semantic_score}%")
    print("Skill Match:", skill_result)

    print("\n====== RECOMMENDATIONS ======")
    for i, s in enumerate(suggestions, 1):
        print(f"{i}. {s}")

    print("\n====== EXTRACTED PROFILE ======")
    for k, v in profile.items():
        print(f"{k}: {v}")

    print("\n====== FINAL MATCH SCORE ======")
    print(final_score_result)
