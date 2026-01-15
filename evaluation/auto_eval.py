import csv
from scipy.stats import spearmanr

from processing.parser import parse_resume, parse_text_file, extract_required_experience
from processing.cleaner import clean_text
from nlp.extractor import split_into_sections, build_profile
from scoring.similarity import compute_similarity, compute_semantic_similarity
from scoring.engine import calculate_match_score
from scoring.final_score import compute_final_score


def run_model(resume_path, jd_path):
    # Resume pipeline
    raw_resume = parse_resume(resume_path)
    clean_resume = clean_text(raw_resume)
    sections = split_into_sections(clean_resume)
    profile = build_profile(sections)

    # JD pipeline
    jd_raw = parse_text_file(jd_path)
    clean_jd = clean_text(jd_raw)

    # Similarities
    tfidf_score = compute_similarity(clean_resume, clean_jd)
    semantic_score = compute_semantic_similarity(clean_resume, clean_jd)

    # Skill matching
    skill_result = calculate_match_score(profile, clean_jd)

    # Final weighted score
    required_exp = extract_required_experience(clean_jd)
    has_degree = "btech" in profile.get("education", [])

    final_score = compute_final_score(
        skill_match_percent=skill_result["skill_match_percent"],
        semantic_similarity=semantic_score,
        experience_years=profile["experience_years"],
        required_experience=required_exp,
        has_required_degree=has_degree,
        keyword_similarity=tfidf_score
    )

    return float(final_score["final_match_percent"])


# -------------------------
# Evaluation Runner
# -------------------------
human_scores = []
model_scores = []

with open("evaluation/labels.csv", newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
        resume_path = f"data/resumes/{row['resume_file']}"
        jd_path = f"data/jds/{row['jd_file']}"

        human_scores.append(int(row["human_score"]))

        try:
            model_score = run_model(resume_path, jd_path)
        except Exception as e:
            print("Error processing:", resume_path, jd_path, e)
            continue

        model_scores.append(model_score)

# -------------------------
# Spearman Correlation
# -------------------------
corr, p_value = spearmanr(human_scores, model_scores)

print("\n===== EVALUATION RESULTS =====")
print("Human scores :", human_scores)
print("Model scores :", [round(x, 2) for x in model_scores])
print("Spearman correlation:", round(corr, 2))
print("P-value:", round(p_value, 4))
