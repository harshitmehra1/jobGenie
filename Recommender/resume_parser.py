# resume_parser/extract_resume.py
from pdfminer.high_level import extract_text
import spacy
import re

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

def extract_details(text):
    doc = nlp(text)

    # Extract email
    email = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    email = email[0] if email else None

    # Extract phone
    phone = re.findall(r"\+?\d[\d\s]{8,15}", text)
    phone = phone[0] if phone else None

    # Extract name (first proper noun in beginning)
    name = None
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break

    # Extract skills (naive skill list matching)
    skills_list = ['python', 'sql', 'machine learning', 'deep learning', 'nlp', 'pandas', 'excel', 'java', 'c++']
    skills = [skill for skill in skills_list if skill.lower() in text.lower()]

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": list(set(skills))
    }

def parse_resume(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    return extract_details(text)
