from processing.parser import parse_resume, parse_text_file
from processing.cleaner import clean_text
from nlp.extractor import split_into_sections, build_profile
from scoring.similarity import compute_similarity
from scoring.engine import calculate_match_score
from recommendations.advisor import generate_recommendations

if __name__ == "__main__":
    resume_path = "data/resumes/sample_resume.pdf"
    jd_path = "data/jds/sample_jd.txt"

    # Resume pipeline
    raw_resume = parse_resume(resume_path)
    clean_resume = clean_text(raw_resume)
    sections = split_into_sections(clean_resume)
    profile = build_profile(sections)

    # JD pipeline
    jd_text = parse_text_file(jd_path)
    clean_jd = clean_text(jd_text)

    # Similarity
    similarity_score = compute_similarity(clean_resume, clean_jd)

    # Skill matching
    skill_result = calculate_match_score(profile, clean_jd)

    print("\n====== MATCH RESULTS ======")
    print(f"Overall Similarity: {similarity_score}%")
    print("Skill Match:", skill_result)

    suggestions = generate_recommendations(skill_result)

    print("\n====== RECOMMENDATIONS ======")
    for i, s in enumerate(suggestions, 1):
        print(f"{i}. {s}")
