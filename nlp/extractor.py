from typing import Dict
from nlp.skills import extract_skills, extract_experience_years, extract_degrees


def split_into_sections(text: str) -> Dict[str, str]:
    """
    Splits cleaned resume text into basic sections
    based on simple keyword anchors.
    """

    sections = {
        "skills": "",
        "experience": "",
        "education": "",
        "projects": ""
    }

    current_section = None

    # We already cleaned text, so splitting by space is fine for now
    words = text.split(" ")

    for word in words:
        w = word.lower()

        # --- Detect section switches ---
        if "skill" in w:
            current_section = "skills"
            continue
        elif "experience" in w:
            current_section = "experience"
            continue
        elif "education" in w:
            current_section = "education"
            continue
        elif "project" in w:
            current_section = "projects"
            continue

        # --- Collect words under current section ---
        if current_section:
            sections[current_section] += word + " "

    return sections


def build_profile(sections: Dict[str, str]) -> Dict:
    """
    Builds a structured candidate profile
    from extracted sections.
    """

    # Combine all text for global extraction
    combined_text = " ".join(sections.values())

    skills = extract_skills(combined_text)
    exp_years = extract_experience_years(combined_text)
    degrees = extract_degrees(combined_text)

    profile = {
        "skills": skills,
        "experience_years": exp_years,
        "education": degrees
    }

    return profile
