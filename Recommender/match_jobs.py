import pandas as pd
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def find_matching_jobs(resume_skills, job_data_path, top_k=10):
    df = pd.read_csv(job_data_path)
    df = df.dropna(subset=['title', 'description'])

    df["job_text"] = (df["title"] + " " + df["description"]).str.slice(0, 500)

    # Match skills by text search
    def match_skills(text):
        return [skill for skill in resume_skills if skill.lower() in text.lower()]

    df["matched_skills"] = df["job_text"].apply(match_skills)
    df["skill_match_count"] = df["matched_skills"].apply(len)

    # Now sort by skill match count
    df = df[df["skill_match_count"] > 0]  # Optional: filter out jobs with 0 matches
    df_sorted = df.sort_values(by="skill_match_count", ascending=False)

    # Optional: apply semantic ranking only to top-N
    top_jobs = df_sorted.head(top_k)
    return top_jobs[["title", "company_name", "city", "matched_skills", "skill_match_count"]]
