import re

def clean_text(text: str) -> str:
    if not text:
        return ""

    # 1. Lowercase everything
    text = text.lower()

    # 2. Remove unwanted characters (keep letters, numbers, basic punctuation)
    text = re.sub(r"[^a-z0-9\s\.\,\-\+]", " ", text)

    # 3. Replace multiple spaces/newlines with a single space
    text = re.sub(r"\s+", " ", text)

    # 4. Strip leading/trailing spaces
    text = text.strip()

    return text
