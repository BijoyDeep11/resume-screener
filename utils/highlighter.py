import re
from typing import Dict, List


def find_skill_context(text: str, skills: List[str]) -> Dict[str, dict]:
    """
    Returns:
    {
      snippet: {
         "skills": [skill1, skill2],
         "highlighted": snippet_with_html_bold_skills
      }
    }
    """

    snippet = None
    found_skills = []

    for skill in skills:
        pattern = re.compile(rf"{re.escape(skill)}", re.IGNORECASE)
        match = pattern.search(text)

        if match:
            if not snippet:
                start = max(0, match.start() - 60)
                end = min(len(text), match.end() + 60)
                snippet = text[start:end].strip()
                snippet = f"...{snippet}..."

            found_skills.append(skill)

    if not snippet:
        return {}

    highlighted = snippet
    for skill in found_skills:
        pattern = re.compile(rf"{re.escape(skill)}", re.IGNORECASE)
        highlighted = pattern.sub(
            lambda m: f"<strong>{m.group(0)}</strong>",
            highlighted
        )

    return {
        snippet: {
            "skills": found_skills,
            "highlighted": highlighted
        }
    }
