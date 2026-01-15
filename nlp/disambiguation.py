from typing import List

# Context keywords for each ambiguous skill
DISAMBIGUATION_RULES = {
    "spring": {
        "tech": ["java", "boot", "mvc", "hibernate", "microservice"],
        "non_tech": ["season", "weather", "flowers"]
    },
    "react": {
        "tech": ["javascript", "node", "frontend", "library", "framework"],
        "non_tech": ["feel", "emotion", "respond"]
    },
    "docker": {
        "tech": ["container", "kubernetes", "devops", "deployment"],
        "non_tech": ["ship", "harbor", "dock"]
    }
}


def disambiguate_skills(skills: List[str], text: str) -> List[str]:
    """
    Keeps only technically valid skills using context.
    """
    text_lower = text.lower()
    final_skills = []

    for skill in skills:
        s = skill.lower()

        if s not in DISAMBIGUATION_RULES:
            # not ambiguous → keep
            final_skills.append(skill)
            continue

        rules = DISAMBIGUATION_RULES[s]

        # if any tech-context word appears → accept
        if any(word in text_lower for word in rules["tech"]):
            final_skills.append(skill)
        else:
            # ambiguous but no tech context → drop
            pass

    return final_skills
