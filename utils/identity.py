import re

def extract_candidate_identity(text: str) -> str:
    """
    Priority:
    1. Name
    2. Email
    3. Phone
    """

    lines = [l.strip() for l in text.split("\n") if l.strip()]

    # -------------------------
    # 1️⃣ Try to extract NAME
    # -------------------------
    for line in lines[:5]:  # usually name is at top
        # Only alphabets + spaces, no keywords
        if re.match(r"^[A-Za-z\s]{3,40}$", line):
            if not any(k in line.lower() for k in ["resume", "cv", "profile"]):
                return line.title()

    # -------------------------
    # 2️⃣ Try to extract EMAIL
    # -------------------------
    email_match = re.search(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        text
    )
    if email_match:
        return email_match.group()

    # -------------------------
    # 3️⃣ Try to extract PHONE
    # -------------------------
    phone_match = re.search(
        r"(\+?\d{1,3}[-.\s]?)?\d{10}",
        text
    )
    if phone_match:
        return phone_match.group()

    # -------------------------
    # Fallback
    # -------------------------
    return "Candidate"
