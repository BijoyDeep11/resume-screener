import re

# -------------------------
# Safe spaCy import
# -------------------------
try:
    import spacy
    from spacy.matcher import PhraseMatcher

    nlp = spacy.load("en_core_web_sm")
    SPACY_AVAILABLE = True
except Exception:
    SPACY_AVAILABLE = False
    nlp = None
    PhraseMatcher = None


# -------------------------
# Normalization
# -------------------------
SKILL_SYNONYMS = {
    "js": "javascript",
    "nodejs": "node",
    "py": "python",
    "nlp": "natural language processing",
    "ml": "machine learning",
    "dl": "deep learning",
    "db": "databases",
    "sql db": "sql",
    "postgres": "postgresql"
}


# -------------------------
# Skill vocabulary
# -------------------------
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


# -------------------------
# spaCy matcher (only if available)
# -------------------------
if SPACY_AVAILABLE:
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp(skill) for skill in SKILLS]
    matcher.add("SKILLS", patterns)
else:
    matcher = None


# -------------------------
# Skill Extraction
# -------------------------
def extract_skills(text: str):
    text = text.lower()
    found = set()

    # ---- spaCy-based extraction ----
    if SPACY_AVAILABLE:
        doc = nlp(text)
        matches = matcher(doc)

        for _, start, end in matches:
            skill = doc[start:end].text.lower()
            skill = SKILL_SYNONYMS.get(skill, skill)
            found.add(skill)

    # ---- Rule-based fallback ----
    else:
        for skill in SKILLS:
            if skill in text:
                normalized = SKILL_SYNONYMS.get(skill, skill)
                found.add(normalized)

    return list(found)


# -------------------------
# Experience Extraction
# -------------------------
def extract_experience_years(text: str):
    matches = re.findall(r"(\d+)\+?\s+years?", text.lower())
    if matches:
        return max(int(x) for x in matches)
    return 0


# -------------------------
# Degree Extraction
# -------------------------
def extract_degrees(text: str):
    text = text.lower()
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


# -------------------------
# Job Title Extraction
# -------------------------
def extract_job_titles(text: str):
    text = text.lower()

    COMMON_TITLES = [
        "intern",
        "trainee",
        "developer",
        "software developer",
        "software engineer",
        "backend developer",
        "frontend developer",
        "full stack developer",
        "fullstack developer",
        "data analyst",
        "data scientist",
        "ml engineer",
        "ai engineer",
        "campus ambassador",
        "project lead",
        "team lead",
        "technical lead",
        "engineering intern"
    ]

    found = set()

    for title in COMMON_TITLES:
        if title in text:
            found.add(title)

    # Regex-based fallback
    pattern = r"(worked as|role:|position:)\s+([a-z\s]+)"
    matches = re.findall(pattern, text)

    for _, role in matches:
        role = " ".join(role.split()[:3])
        found.add(role.strip())

    return list(found)
