import pandas as pd
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def find_matching_jobs(resume_skills, job_data_path, top_k=10):
    df = pd.read_csv(job_data_path).sample(1000, random_state=42)
    df = df.dropna(subset=['title', 'description'])

    df["job_text"] = df["title"] + " " + df["description"]
    df["job_text"] = df["job_text"].str.slice(0, 500)

    # Semantic Search Step (to filter top 100 jobs quickly)
    query = " ".join(resume_skills)
    query_embedding = model.encode(query, convert_to_tensor=True)

    job_embeddings = model.encode(
        df["job_text"].tolist(),
        convert_to_tensor=True,
        batch_size=64,
        show_progress_bar=True
    )

    similarities = util.cos_sim(query_embedding, job_embeddings)[0]
    top_indices = similarities.argsort(descending=True)[:100]  # Only keep top 100 semantically similar

    filtered_jobs = df.iloc[top_indices.cpu().numpy()].copy()

    # Skill Matching
    filtered_jobs["matched_skills"] = filtered_jobs["job_text"].apply(
        lambda text: [skill for skill in resume_skills if skill.lower() in text.lower()]
    )
    filtered_jobs["skill_match_count"] = filtered_jobs["matched_skills"].apply(len)

    # Rank by skill match count (descending)
    ranked_jobs = filtered_jobs.sort_values(by="skill_match_count", ascending=False)

    return ranked_jobs.head(top_k)[["title", "company_name", "city", "description", "matched_skills", "skill_match_count"]]
