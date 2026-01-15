from processing.parser import parse_resume

if __name__ == "__main__":
    resume_path = "data/resumes/sample_resume.pdf"  # change if DOCX
    text = parse_resume(resume_path)

    print("====== RAW RESUME TEXT ======")
    print(text[:1000])  # print first 1000 chars
