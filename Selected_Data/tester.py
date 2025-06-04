import pandas as pd
import re
from tqdm import tqdm

# Load job data
df = pd.read_csv("./Selected_Data/under_100mb.csv")

# Load skills from file
with open("./Selected_Data/skills.txt", "r", encoding="utf-8") as file:
    skills = [line.strip().lower() for line in file if line.strip()]

# Function to match skills in description
def extract_matched_skills(description, skill_set):
    if pd.isnull(description):
        return []
    description = description.lower()
    matches = [skill for skill in skill_set if re.search(r'\b' + re.escape(skill) + r'\b', description)]
    return matches

print("Scanning job descriptions...")

batch_size = 2000  # adjust if needed

matched_indices = []
unmatched_indices = []

for start in tqdm(range(0, len(df), batch_size), desc="Processing batches"):
    end = min(start + batch_size, len(df))
    chunk = df.iloc[start:end]

    for idx, desc in zip(chunk.index, chunk['description']):
        matched = extract_matched_skills(desc, skills)
        if matched:
            matched_indices.append(idx)
        else:
            unmatched_indices.append(idx)

print("\n✅ Job titles with at least one skill match:", len(matched_indices))
print("❌ Job titles with no skill match:", len(unmatched_indices))

# Save unmatched descriptions to CSV
df_unmatched = df.loc[unmatched_indices]
df_unmatched.to_csv("./Selected_Data/unmatched_descriptions.csv", index=False)

print("Unmatched job descriptions saved to ./Selected_Data/unmatched_descriptions.csv")
