import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load your cleaned dataset
df = pd.read_csv("./Selected_Data/under_100mb.csv")

# Combine important fields into a single searchable column
df['combined'] = (
    df['title'].fillna('') + ' ' +
    df['description'].fillna('') + ' ' +
    df['city'].fillna('') + ' ' +
    df['state'].fillna('') + ' ' +
    df['company_name'].fillna('')
).str.lower()

# Clean text helper
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return text.strip()

# Highlight matched keywords in job title
def highlight_keywords(text, query_terms):
    for term in query_terms:
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        text = pattern.sub(lambda m: f"\033[1m{m.group(0)}\033[0m", text)  # Bold in terminal
    return text

# Get input from user
def get_user_input():
    title = input("Enter job title or keywords (leave blank if none): ").strip().lower()
    location = input("Enter preferred location (city/state/country, leave blank if none): ").strip().lower()
    
    if not title and not location:
        print("❌ You must enter either a job title or a location.")
        exit()
    
    return title, location

# Recommend jobs
def recommend_jobs(title_query, location_query, top_n=10):
    combined_query = f"{title_query} {location_query}".strip()
    cleaned_query = clean_text(combined_query)

    # Vectorize
    vectorizer = CountVectorizer().fit_transform([cleaned_query] + df['combined'].tolist())
    similarity_scores = cosine_similarity(vectorizer[0:1], vectorizer[1:]).flatten()

    # Get top N matches
    top_indices = similarity_scores.argsort()[-top_n:][::-1]
    recommended = df.iloc[top_indices][['title', 'city', 'state', 'company_name']]

    # Print results with highlight
    print("\nTop Recommended Jobs:\n")
    query_terms = title_query.split()  # Only highlight keywords, not location
    for _, row in recommended.iterrows():
        highlighted_title = highlight_keywords(row['title'], query_terms)
        print(f"📌 {highlighted_title} — {row['company_name']} ({row['city']}, {row['state']})")

# Main execution
if __name__ == "__main__":
    title_input, location_input = get_user_input()
    recommend_jobs(title_input, location_input, top_n=10)
