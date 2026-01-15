import os
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import PyPDF2
import docx


def parse_resume(file_path: str) -> str:
    """
    Extract text from PDF/DOCX.
    If PDF text extraction fails, fall back to OCR.
    """

    if file_path.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file_path)

        # ---- OCR FALLBACK ----
        if not text.strip():
            print("⚠️ No text found in PDF. Using OCR fallback...")
            text = ocr_from_pdf(file_path)

        return text

    elif file_path.lower().endswith(".docx"):
        return extract_text_from_docx(file_path)

    else:
        raise ValueError("Unsupported file format")


# -------------------------
# Helpers
# -------------------------

def extract_text_from_pdf(path: str) -> str:
    text = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
    return text


def extract_text_from_docx(path: str) -> str:
    doc = docx.Document(path)
    return "\n".join(p.text for p in doc.paragraphs)


# -------------------------
# OCR FUNCTIONS
# -------------------------

def ocr_from_pdf(pdf_path: str) -> str:
    """
    Convert PDF pages to images and run OCR.
    """
    images = convert_from_path(pdf_path)
    text = ""

    for img in images:
        text += pytesseract.image_to_string(img)

    return text


def parse_text_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_required_experience(text: str) -> int:
    import re
    match = re.search(r"(\d+)\+?\s+years", text.lower())
    if match:
        return int(match.group(1))
    return 0
