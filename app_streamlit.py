import streamlit as st
import tempfile
import os

from processing.parser import parse_resume, parse_text_file
from processing.cleaner import clean_text
from nlp.extractor import split_into_sections, build_profile
from scoring.similarity import compute_similarity
from scoring.engine import calculate_match_score
from recommendations.advisor import generate_recommendations


st.set_page_config(page_title="AI Resume Screener", layout="centered")

st.title("📄 AI-Powered Resume Screener")
st.write("Upload a resume and a job description to see how well they match.")

# -------------------------
# Upload Section
# -------------------------
resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
jd_file = st.file_uploader("Upload Job Description (TXT)", type=["txt"])

# -------------------------
# Process Button
# -------------------------
if st.button("Analyze Match"):

    if not resume_file or not jd_file:
        st.warning("Please upload both Resume and Job Description.")
    else:
        with st.spinner("Analyzing..."):

            # Save uploaded files temporarily
            with tempfile.NamedTemporaryFile(delete=False) as tmp_resume:
                tmp_resume.write(resume_file.read())
                resume_path = tmp_resume.name

            with tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8") as tmp_jd:
                jd_text = jd_file.read().decode("utf-8")
                tmp_jd.write(jd_text)
                jd_path = tmp_jd.name

            try:
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
                # Matching
                # -------------------------
                similarity_score = compute_similarity(clean_resume, clean_jd)
                skill_result = calculate_match_score(profile, clean_jd)
                suggestions = generate_recommendations(skill_result)

                # -------------------------
                # Display Results
                # -------------------------
                st.success("Analysis Complete!")

                st.subheader("🔍 Match Overview")
                st.metric("Overall Similarity", f"{similarity_score}%")
                st.metric("Skill Match", f"{skill_result['skill_match_percent']}%")

                st.subheader("✅ Matched Skills")
                if skill_result["matched_skills"]:
                    st.write(", ".join(skill_result["matched_skills"]))
                else:
                    st.write("No matching skills found.")

                st.subheader("❌ Missing Skills")
                if skill_result["missing_skills"]:
                    st.write(", ".join(skill_result["missing_skills"]))
                else:
                    st.write("No missing skills. Great fit!")

                st.subheader("💡 Recommendations")
                if suggestions:
                    for i, s in enumerate(suggestions, 1):
                        st.write(f"{i}. {s}")
                else:
                    st.write("Your resume already matches this role well!")

            except Exception as e:
                st.error(f"Something went wrong: {e}")

            finally:
                # Cleanup temp files
                if os.path.exists(resume_path):
                    os.remove(resume_path)
                if os.path.exists(jd_path):
                    os.remove(jd_path)
