# 🧠 AI-Powered Resume Screener

## 1️⃣ Problem Statement (in my own words)

Screening resumes manually is slow, inconsistent, and often biased by surface-level keyword matching. Recruiters usually spend significant time comparing resumes against job descriptions without clear visibility into *why* a candidate matches or doesn’t.

This project aims to build a **transparent, explainable, and practical resume screening system** that:
- goes beyond simple keyword matching,
- understands context using NLP and semantic similarity,
- and provides actionable feedback instead of just a score.

The goal is not to replace human judgment, but to **support faster and more informed shortlisting**.

---

## 2️⃣ How the System Works

At a high level, the system follows this flow:

Resume(s) + Job Description
↓
Document Parsing (PDF / DOCX / OCR fallback)
↓
Text Cleaning & Normalization
↓
Section Detection (skills, experience, education)
↓
Entity Extraction (skills, years, degrees, titles)
↓
Skill Disambiguation (context-aware filtering)
↓
Similarity Computation

TF-IDF + Cosine

Semantic Embeddings (SBERT)
↓
Weighted Scoring Engine
↓
Recommendations Generator
↓
Streamlit UI (ranking + detailed view)
↓
PDF Report (single resume mode)

yaml
Copy code

The system supports:
- **Multiple resumes** for recruiter-style ranking  
- **Single resume deep analysis** for candidate-style feedback  

---

## 3️⃣ Design Decisions

### 🔹 Modular Folder Structure
The project is split into logical modules (`processing`, `nlp`, `scoring`, `recommendations`, `utils`) to:
- keep responsibilities clear,
- simplify debugging,
- and allow independent iteration of components.

This mirrors real-world backend service design.

---

### 🔹 TF-IDF + Semantic Similarity Together
- **TF-IDF** captures exact keyword overlap (important for ATS-style filtering).
- **Semantic similarity (SBERT)** captures meaning even when wording differs.

Using both avoids over-reliance on either rigid keywords or purely abstract embeddings.

---

### 🔹 Rule-based Named Entity Disambiguation
Certain skills like *Spring*, *React*, or *Docker* are ambiguous.

A lightweight **context-based rule system** was implemented to:
- improve precision,
- avoid false positives,
- and keep the system explainable.

This design favors **clarity over black-box complexity**.

---

### 🔹 Synchronous Processing
The application is designed for:
- internship-scale usage,
- controlled resume batches,
- and simplicity over raw throughput.

Synchronous processing keeps logic easy to reason about and debug.  
The design can be extended to async pipelines if needed.

---

## 4️⃣ Known Limitations

- Skill disambiguation is rule-based and may not cover all edge cases.
- OCR accuracy depends on resume scan quality.
- Semantic similarity uses a general-purpose model, not domain-specific embeddings.
- Evaluation dataset is small and manually curated.
- Resume formatting variations can affect extraction accuracy.

These limitations are documented intentionally for transparency.

---

## 5️⃣ How AI Was Used (carefully worded)

AI tools were used during development for:
- early-stage idea exploration,
- understanding alternative approaches,
- and initial scaffolding of some components.

All **core logic**, **system design**, **debugging**, **feature decisions**, and **final implementation** were performed independently with iterative testing and refinement.

The project structure, scoring logic, UI flow, and evaluation methodology reflect deliberate engineering decisions rather than automated code generation.

---

## 🛠️ Tech Stack

- **Language:** Python  
- **NLP:** spaCy / NLTK  
- **Parsing:** PyPDF2, python-docx, pytesseract (OCR)  
- **Similarity:** scikit-learn, sentence-transformers  
- **UI:** Streamlit  
- **Reporting:** reportlab  
- **Evaluation:** scipy (Spearman correlation)

---

## 📌 Final Note

This project prioritizes **explainability, correctness, and real-world relevance** over superficial complexity.  
Each feature serves a clear purpose aligned with practical recruitment workflows.
If you want next:
