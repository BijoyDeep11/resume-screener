from PyPDF2 import PdfReader
from docx import Document
import os
import re

def parse_pdf(file_path):
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text


def parse_docx(file_path):
    text = ""
    try:
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX: {e}")
    return text


def parse_resume(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return parse_pdf(file_path)
    elif ext == ".docx":
        return parse_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Use PDF or DOCX.")

def parse_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_required_experience(jd_text: str) -> int:
    """
    Extracts required experience from JD text.
    Example: '2 years experience' → 2
    """
    matches = re.findall(r"(\d+)\+?\s+years?", jd_text.lower())
    if matches:
        return max(int(x) for x in matches)
    return 0