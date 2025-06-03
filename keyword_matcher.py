import pandas as pd
import re
import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset - use relative path for GitHub friendliness
@st.cache_data
def load_data():
    return pd.read_csv("./Selected_Data/under_100mb.csv")

df = load_data()

df['combined'] = (
    df['title'].fillna('') + ' ' +
    df['description'].fillna('') + ' ' +
    df['city'].fillna('') + ' ' +
    df['state'].fillna('') + ' ' +
    df['company_name'].fillna('')
).str.lower()

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return text.strip()

def highlight_keywords(text, query_terms):
    for term in query_terms:
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        # Use Streamlit's markdown bold
        text = pattern.sub(lambda m: f"**{m.group(0)}**", text)
    return text

def recommend_jobs(title_query, location_query, top_n=10):
    combined_query = f"{title_query} {location_query}".strip()
    if combined_query == "":
        st.warning("Please enter job title or location to get recommendations.")
        return

    cleaned_query = clean_text(combined_query)

    vectorizer = CountVectorizer().fit_transform([cleaned_query] + df['combined'].tolist())
    similarity_scores = cosine_similarity(vectorizer[0:1], vectorizer[1:]).flatten()

    top_indices = similarity_scores.argsort()[-top_n:][::-1]
    recommended = df.iloc[top_indices][['title', 'city', 'state', 'company_name']]

    st.write("### Top Recommended Jobs:\n")
    query_terms = title_query.split()
    for _, row in recommended.iterrows():
        highlighted_title = highlight_keywords(row['title'], query_terms)
        st.markdown(f"📌 {highlighted_title} — {row['company_name']} ({row['city']}, {row['state']})")


def main():
    st.title("Job Recommendation System")

    title_input = st.text_input("Enter job title or keywords (leave blank if none):").strip().lower()
    location_input = st.text_input("Enter preferred location (city/state/country, leave blank if none):").strip().lower()

    if st.button("Recommend Jobs"):
        recommend_jobs(title_input, location_input, top_n=10)
    else:
        st.info("Please enter your job title or location above and click 'Recommend Jobs'.")

if __name__ == "__main__":
    main()
