import re
import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")


JOB_TITLES = [
    "software engineer",
    "backend developer",
    "frontend developer",
    "full stack developer",
    "data analyst",
    "data scientist",
    "machine learning engineer",
    "ai engineer",
    "web developer",
    "intern",
    "trainee",
    "campus ambassador",
    "project intern"
]


# A starter skill list (we'll grow this later)
SKILLS = [
    # Programming
    "python", "java", "c", "c++", "javascript",

    # Web
    "html", "css", "responsive web design",
    "react", "node", "express",

    # Backend
    "django", "flask", "rest api",

    # Databases
    "sql", "mysql", "postgresql", "mongodb", "databases",

    # DevOps / Cloud
    "docker", "aws", "linux", "git",

    # Data / AI
    "machine learning", "deep learning", "nlp"
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

def extract_job_titles(text: str):
    found = set()
    text_lower = text.lower()

    for title in JOB_TITLES:
        if title in text_lower:
            found.add(title)

    return list(found)
