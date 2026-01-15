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
st.write("Upload resumes and a job description to see how well they match.")


# -------------------------
# Upload Section
# -------------------------
resume_files = st.file_uploader(
    "Upload Resume(s) (PDF or DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

jd_file = st.file_uploader("Upload Job Description (TXT)", type=["txt"])


# -------------------------
# Analyze Button
# -------------------------
if st.button("Analyze Match"):

    if not resume_files or not jd_file:
        st.warning("Please upload at least one Resume and the Job Description.")
    else:
        with st.spinner("Analyzing..."):

            # -------------------------
            # Save JD file
            # -------------------------
            with tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8") as tmp_jd:
                jd_text = jd_file.read().decode("utf-8")
                tmp_jd.write(jd_text)
                jd_path = tmp_jd.name

            try:
                start_time = time.time()

                # -------------------------
                # JD pipeline (once)
                # -------------------------
                jd_raw = parse_text_file(jd_path)
                clean_jd = clean_text(jd_raw)

                results = []
                top_candidate_data = None   # used for PDF when only one resume

                # -------------------------
                # Loop over resumes
                # -------------------------
                for resume_file in resume_files:

                    resume_suffix = os.path.splitext(resume_file.name)[1]

                    with tempfile.NamedTemporaryFile(delete=False, suffix=resume_suffix) as tmp_resume:
                        tmp_resume.write(resume_file.read())
                        resume_path = tmp_resume.name

                    try:
                        # -------------------------
                        # Resume pipeline
                        # -------------------------
                        raw_resume = parse_resume(resume_path)
                        clean_resume = clean_text(raw_resume)
                        sections = split_into_sections(clean_resume)
                        profile = build_profile(sections)

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
                        # Skill context
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
                        # Candidate identity
                        # -------------------------
                        candidate_name = extract_candidate_identity(raw_resume)

                        # -------------------------
                        # Store result
                        # -------------------------
                        row = {
                            "Candidate": candidate_name,
                            "Final Match %": round(final_score_result["final_match_percent"], 2),
                            "Matched Skills": ", ".join(skill_result["matched_skills"]) if skill_result["matched_skills"] else "None",
                            "Missing Skills": ", ".join(skill_result["missing_skills"]) if skill_result["missing_skills"] else "None",
                        }

                        results.append(row)

                        # Save data for PDF when only one resume is uploaded
                        if len(resume_files) == 1:
                            under_emphasized = find_under_emphasized_strengths(
                                resume_text=clean_resume,
                                jd_skills=skill_result["jd_skills"]
                            )

                            suggestions = generate_recommendations(
                                skill_result,
                                under_emphasized=under_emphasized
                            )

                            top_candidate_data = {
                                "final_score": final_score_result["final_match_percent"],
                                "matched_skills": skill_result["matched_skills"],
                                "missing_skills": skill_result["missing_skills"],
                                "recommendations": suggestions,
                                "profile": profile,
                                "skill_context": skill_context,
                                "tfidf": tfidf_score,
                                "semantic": semantic_score,
                                "candidate_name": candidate_name
                            }

                    finally:
                        if os.path.exists(resume_path):
                            os.remove(resume_path)

                # -------------------------
                # Rank results
                # -------------------------
                results = sorted(results, key=lambda x: x["Final Match %"], reverse=True)
                for i, r in enumerate(results, start=1):
                    r["Rank"] = i

                # -------------------------
                # UI OUTPUT
                # -------------------------
                st.success("Analysis Complete!")

                # -------- Ranked Table --------
                st.subheader("🏆 Ranked Candidates")

                df = pd.DataFrame(results)
                df = df[["Rank", "Candidate", "Final Match %", "Matched Skills", "Missing Skills"]]
                st.dataframe(df, use_container_width=True)

                # -------------------------
                # Detailed view (only when 1 resume)
                # -------------------------
                if len(resume_files) == 1 and top_candidate_data:

                    st.divider()
                    st.subheader("🔍 Detailed View")

                    st.metric(
                        "Final Match Score",
                        f"{top_candidate_data['final_score']:.2f}%"
                    )

                    st.metric(
                        "TF-IDF Similarity",
                        f"{top_candidate_data['tfidf']:.2f}%"
                    )

                    st.metric(
                        "Semantic Similarity",
                        f"{top_candidate_data['semantic']:.2f}%"
                    )

                    # -------- Skill Context --------
                    st.subheader("📍 Skill Hits in Context")

                    if top_candidate_data["skill_context"]:
                        for snippet, data in top_candidate_data["skill_context"].items():
                            skills_list = ", ".join([s.title() for s in data["skills"]])
                            st.markdown(f"**Skills found here:** {skills_list}")
                            st.markdown(
                                f"<div style='color:#e5e7eb; font-weight:500;'>{data['highlighted']}</div>",
                                unsafe_allow_html=True
                            )
                    else:
                        st.write("No skill occurrences found in resume text.")

                    # -------- Extracted Profile --------
                    profile = top_candidate_data["profile"]

                    st.subheader("🧾 Extracted Profile")

                    st.write(f"**Name**: {top_candidate_data['candidate_name']}")

                    st.write(
                        f"**Skills**: {', '.join(profile['skills'])}"
                        if profile["skills"]
                        else "**Skills**: Not mentioned"
                    )

                    st.caption("(Skills are context-validated to avoid ambiguity.)")

                    if profile["experience_years"] > 0:
                        st.write(f"**Experience**: {profile['experience_years']} years")
                    else:
                        st.write("**Experience**: Fresher / Not mentioned")

                    st.write(
                        f"**Education**: {', '.join(profile['education']).upper()}"
                        if profile["education"]
                        else "**Education**: Not specified"
                    )

                    st.write(
                        f"**Job Titles**: {', '.join(profile['job_titles'])}"
                        if profile["job_titles"]
                        else "**Job Titles**: Not specified in resume"
                    )

                    # -------- Recommendations --------
                    st.subheader("💡 Recommendations")
                    for i, s in enumerate(top_candidate_data["recommendations"], 1):
                        st.write(f"{i}. {s}")

                    # -------------------------
                    # PDF Report
                    # -------------------------
                    report_data = {
                        "final_score": top_candidate_data["final_score"],
                        "matched_skills": top_candidate_data["matched_skills"],
                        "missing_skills": top_candidate_data["missing_skills"],
                        "recommendations": top_candidate_data["recommendations"]
                    }

                    pdf_bytes = generate_pdf_report_bytes(report_data)

                    st.download_button(
                        label="⬇️ Download PDF Report",
                        data=pdf_bytes,
                        file_name="resume_screening_report.pdf",
                        mime="application/pdf"
                    )

                else:
                    st.info(
                        "PDF report and detailed context view are available when "
                        "you upload a single resume."
                    )

                # -------------------------
                # Logging time
                # -------------------------
                total_time = log_time(start_time, "Resume Screening")
                st.caption(f"⏱ Processing time: {total_time}s")

            except Exception as e:
                st.error(f"Something went wrong: {e}")

            finally:
                if os.path.exists(jd_path):
                    os.remove(jd_path)
