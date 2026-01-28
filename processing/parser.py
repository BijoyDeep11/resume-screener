import os
import PyPDF2
import docx

# -------------------------
# OCR Safe Imports
# -------------------------
try:
    from pdf2image import convert_from_path
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


def parse_resume(file_path: str) -> str:
    """
    Extract text from PDF/DOCX.
    If PDF text extraction fails, fall back to OCR (if available).
    """

    if file_path.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file_path)

        # ---- OCR FALLBACK (GUARDED) ----
        if not text.strip():
            if OCR_AVAILABLE:
                print("⚠️ No text found in PDF. Using OCR fallback...")
                text = ocr_from_pdf(file_path)
            else:
                print("⚠️ OCR not available. Skipping OCR fallback.")
                text = ""

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
    try:
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception:
        # Fail silently and allow OCR fallback
        pass

    return text


def extract_text_from_docx(path: str) -> str:
    doc = docx.Document(path)
    return "\n".join(p.text for p in doc.paragraphs)


# -------------------------
# OCR FUNCTIONS (GUARDED)
# -------------------------

def ocr_from_pdf(pdf_path: str) -> str:
    """
    Convert PDF pages to images and run OCR.
    Only executed if OCR_AVAILABLE is True.
    """
    if not OCR_AVAILABLE:
        return ""

    text = ""
    try:
        images = convert_from_path(pdf_path)
        for img in images:
            text += pytesseract.image_to_string(img)
    except Exception:
        # OCR failed → return empty string safely
        pass

    return text


# -------------------------
# JD Parsing
# -------------------------

def parse_text_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_required_experience(text: str) -> int:
    import re
    match = re.search(r"(\d+)\+?\s+years", text.lower())
    if match:
        return int(match.group(1))
    return 0
