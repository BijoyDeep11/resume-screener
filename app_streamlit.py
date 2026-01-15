import streamlit as st
import tempfile
import os
import time
import pandas as pd

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

from reports.pdf_generator import generate_pdf_report_bytes
from utils.logger import log_time
from utils.identity import extract_candidate_identity
from utils.highlighter import find_skill_context


# -------------------------
# Page setup
# -------------------------
st.set_page_config(page_title="AI Resume Screener", layout="centered")

st.title("📄 AI-Powered Resume Screener")
st.write("Upload a resume and a job description to see how well they match.")


# -------------------------
# Upload Section
# -------------------------
resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
jd_file = st.file_uploader("Upload Job Description (TXT)", type=["txt"])


# -------------------------
# Analyze Button
# -------------------------
if st.button("Analyze Match"):

    if not resume_file or not jd_file:
        st.warning("Please upload both Resume and Job Description.")
    else:
        with st.spinner("Analyzing..."):

            # -------------------------
            # Save uploaded files (KEEP EXTENSION!)
            # -------------------------
            resume_suffix = os.path.splitext(resume_file.name)[1]

            with tempfile.NamedTemporaryFile(delete=False, suffix=resume_suffix) as tmp_resume:
                tmp_resume.write(resume_file.read())
                resume_path = tmp_resume.name

            with tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8") as tmp_jd:
                jd_text = jd_file.read().decode("utf-8")
                tmp_jd.write(jd_text)
                jd_path = tmp_jd.name

            try:
                start_time = time.time()

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
                jd_raw = parse_text_file(jd_path)
                clean_jd = clean_text(jd_raw)

                # -------------------------
                # Similarity
                # -------------------------
                tfidf_score = compute_similarity(clean_resume, clean_jd)
                semantic_score = compute_semantic_similarity(clean_resume, clean_jd)

                # -------------------------
                # Skill matching
                # -------------------------
                skill_result = calculate_match_score(profile, clean_jd)

                # -------------------------
                # Skill context in resume
                # -------------------------
                skill_context = find_skill_context(
                    clean_resume,
                    skill_result["matched_skills"]
                )

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
                    keyword_similarity=tfidf_score
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
                # UI OUTPUT
                # -------------------------
                st.success("Analysis Complete!")

                # -------------------------
                # Candidate identity
                # -------------------------
                candidate_name = extract_candidate_identity(raw_resume)

                # -------- Results Table --------
                st.subheader("📊 Results Table")

                result_row = {
                    "Candidate": candidate_name,
                    "Final Match %": round(final_score_result["final_match_percent"], 2),
                    "Matched Skills": ", ".join(skill_result["matched_skills"]) if skill_result["matched_skills"] else "None",
                    "Missing Skills": ", ".join(skill_result["missing_skills"]) if skill_result["missing_skills"] else "None"
                }

                df = pd.DataFrame([result_row])
                st.dataframe(df, use_container_width=True)

                # -------- Metrics --------
                st.subheader("🔍 Match Overview")
                st.metric("Final Match Score", f"{final_score_result['final_match_percent']:.2f}%")
                st.metric("TF-IDF Similarity", f"{tfidf_score:.2f}%")
                st.metric("Semantic Similarity", f"{semantic_score:.2f}%")

                # -------- Skills --------
                # -------- Matched Skills --------
                st.subheader("✅ Matched Skills")
                if skill_result["matched_skills"]:
                    st.write(", ".join(skill_result["matched_skills"]))
                else:
                    st.write("No matching skills found.")

                # -------- Skill context --------
                st.subheader("📍 Skill Hits in Context")

                if skill_context:
                    for snippet, data in skill_context.items():
                        skills_list = ", ".join([s.title() for s in data["skills"]])
                        st.markdown(f"**Skills found here:** {skills_list}")
                        st.markdown(
                            f"<div style='color:#e5e7eb; font-weight:500;'>{data['highlighted']}</div>",
                            unsafe_allow_html=True
                        )
                else:
                    st.write("No skill occurrences found in resume text.")



                st.subheader("❌ Missing Skills")
                if skill_result["missing_skills"]:
                    st.write(", ".join(skill_result["missing_skills"]))
                else:
                    st.write("No missing skills. Great fit!")

                # -------- Recommendations --------
                st.subheader("💡 Recommendations")
                if suggestions:
                    for i, s in enumerate(suggestions, 1):
                        st.write(f"{i}. {s}")
                else:
                    st.write("Your resume already matches this role well!")

                # -------- Extracted Profile --------
                st.subheader("🧾 Extracted Profile")

                if profile["skills"]:
                    st.write(f"**Skills**: {', '.join(profile['skills'])}")
                else:
                    st.write("**Skills**: Not mentioned")

                if profile["experience_years"] > 0:
                    st.write(f"**Experience**: {profile['experience_years']} years")
                else:
                    st.write("**Experience**: Fresher / Not mentioned")

                if profile["education"]:
                    st.write(f"**Education**: {', '.join(profile['education']).upper()}")
                else:
                    st.write("**Education**: Not specified")

                if profile["job_titles"]:
                    st.write(f"**Job Titles**: {', '.join(profile['job_titles'])}")
                else:
                    st.write("**Job Titles**: Not specified in resume")

                # -------------------------
                # PDF Report
                # -------------------------
                report_data = {
                    "final_score": final_score_result["final_match_percent"],
                    "matched_skills": skill_result["matched_skills"],
                    "missing_skills": skill_result["missing_skills"],
                    "recommendations": suggestions
                }

                pdf_bytes = generate_pdf_report_bytes(report_data)

                st.download_button(
                    label="⬇️ Download PDF Report",
                    data=pdf_bytes,
                    file_name="resume_screening_report.pdf",
                    mime="application/pdf"
                )

                # -------------------------
                # Logging time
                # -------------------------
                total_time = log_time(start_time, "Resume Screening")
                st.caption(f"⏱ Processing time: {total_time}s")

            except Exception as e:
                st.error(f"Something went wrong: {e}")

            finally:
                # -------------------------
                # Cleanup temp files
                # -------------------------
                if os.path.exists(resume_path):
                    os.remove(resume_path)
                if os.path.exists(jd_path):
                    os.remove(jd_path)
