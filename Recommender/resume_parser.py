# resume_parser/extract_resume.py
from pdfminer.high_level import extract_text
import spacy
import re
import os

nlp = spacy.load("en_core_web_sm")

# ✅ Load known skills from external file (skills.txt)
def load_skills_from_file(file_path='./Selected_Data/skills.txt'):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Skills file not found at: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as file:
        return set(line.strip().lower() for line in file.readlines())

# ✅ Extract plain text from PDF
def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

# ✅ Extract structured details from text
def extract_details(text):
    doc = nlp(text)

    # Email extraction
    email = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    email = email[0] if email else None

    # Phone number extraction
    phone = re.findall(r"\+?\d[\d\s]{8,15}", text)
    phone = phone[0] if phone else None

    # Name (using first PERSON entity)
    name = None
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break

    # ✅ Load skill list and extract matching skills from text
    known_skills = load_skills_from_file()
    words = re.findall(r'\b[a-zA-Z][a-zA-Z\s]+\b', text.lower())  # extract all possible phrases
    found_skills = set()

    # Match both one-word and multi-word skills
    for skill in known_skills:
        if skill.lower() in text.lower():
            found_skills.add(skill)

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": sorted(list(found_skills))
    }

# ✅ Entry point for resume parsing
def parse_resume(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    return extract_details(text)
