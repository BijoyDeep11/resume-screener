import re
import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")

# A starter skill list (we'll grow this later)
SKILLS = [
    "python", "java", "c++", "javascript", "react", "node",
    "django", "flask", "sql", "mongodb", "html", "css",
    "machine learning", "deep learning", "nlp",
    "git", "docker", "linux", "aws"
]

matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp(skill) for skill in SKILLS]
matcher.add("SKILLS", patterns)


def extract_skills(text: str):
    doc = nlp(text)
    matches = matcher(doc)

    found = set()
    for _, start, end in matches:
        found.add(doc[start:end].text.lower())

    return list(found)


def extract_experience_years(text: str):
    """
    Looks for patterns like:
    - 2 years
    - 3+ years
    - 1 year experience
    """
    matches = re.findall(r"(\d+)\+?\s+years?", text)
    if matches:
        # return the max mentioned years
        return max(int(x) for x in matches)
    return 0


def extract_degrees(text: str):
    degrees = []

    if "btech" in text or "b.tech" in text:
        degrees.append("btech")
    if "mtech" in text or "m.tech" in text:
        degrees.append("mtech")
    if "bsc" in text:
        degrees.append("bsc")
    if "msc" in text:
        degrees.append("msc")

    return degrees
