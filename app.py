from processing.parser import parse_resume
from processing.cleaner import clean_text

if __name__ == "__main__":
    resume_path = "data/resumes/sample_resume.pdf"  # or .docx

    raw_text = parse_resume(resume_path)
    cleaned_text = clean_text(raw_text)

    print("====== CLEANED RESUME TEXT ======")
    print(cleaned_text[:1000])  # first 1000 chars
