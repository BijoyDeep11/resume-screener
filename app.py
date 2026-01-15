from processing.parser import parse_resume
from processing.cleaner import clean_text
from nlp.extractor import split_into_sections

if __name__ == "__main__":
    resume_path = "data/resumes/sample_resume.pdf"

    raw_text = parse_resume(resume_path)
    cleaned_text = clean_text(raw_text)

    sections = split_into_sections(cleaned_text)

    print("\n====== SECTIONS ======")
    for k, v in sections.items():
        print(f"\n--- {k.upper()} ---")
        print(v[:400])
