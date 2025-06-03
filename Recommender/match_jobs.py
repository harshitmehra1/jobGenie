# recommender/match_jobs.py
import pandas as pd
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')


def find_matching_jobs(resume_skills, job_data_path, top_k=5):
    # df = pd.read_csv(job_data_path)
    df = pd.read_csv(job_data_path).sample(1000, random_state=42)

    df = df.dropna(subset=['title', 'description'])

    df["job_text"] = df["title"] + " " + df["description"]

    # Reduce length for speed (optional)
    df["job_text"] = df["job_text"].str.slice(0, 500)

    # Create search query from skills
    query = " ".join(resume_skills)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode(query, convert_to_tensor=True)

    # 🆕 Batch encode job descriptions
    job_embeddings = model.encode(df["job_text"].tolist(), convert_to_tensor=True, batch_size=64, show_progress_bar=True)

    similarities = util.cos_sim(query_embedding, job_embeddings)[0]
    top_indices = similarities.argsort(descending=True)[:top_k]

    return df.iloc[top_indices.cpu().numpy()][["title", "company_name", "city", "description"]]
