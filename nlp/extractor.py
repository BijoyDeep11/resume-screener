def split_into_sections(text: str) -> dict:
    sections = {
        "skills": "",
        "experience": "",
        "education": "",
        "projects": ""
    }

    current_section = None

    lines = text.split(" ")

    for word in lines:
        w = word.lower()

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

        if current_section:
            sections[current_section] += word + " "

    return sections
