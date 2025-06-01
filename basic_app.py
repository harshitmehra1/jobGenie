import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_csv("./Selected_Data/under_100mb.csv") 

df = load_data()

st.title("💼 Job Filter System")

# Step 1: Job Role (Title)
job_titles = sorted(df['title'].dropna().unique())
title_options = ["Any"] + job_titles if len(job_titles) > 1 else job_titles
selected_title = st.selectbox("Select Job Role", title_options)

if selected_title != "Any":
    df = df[df['title'] == selected_title]

# Step 2: Company (filtered by previous)
companies = sorted(df['company_name'].dropna().unique())
company_options = ["Any"] + companies if len(companies) > 1 else companies
selected_company = st.selectbox("Select Company", company_options)

if selected_company != "Any":
    df = df[df['company_name'] == selected_company]

# Step 3: State (filtered by title + company)
states = sorted(df['state'].dropna().unique())
state_options = ["Any"] + states if len(states) > 1 else states
selected_state = st.selectbox("Select State", state_options)

if selected_state != "Any":
    df = df[df['state'] == selected_state]

# Step 4: City (filtered by title + company + state)
if selected_state != "Any":
    cities = sorted(df['city'].dropna().unique())
else:
    cities = sorted(df['city'].dropna().unique())

city_options = ["Any"] + cities if len(cities) > 1 else cities
selected_city = st.selectbox("Select City", city_options)

if selected_city != "Any":
    df = df[df['city'] == selected_city]

# Show Results
st.subheader("🎯 Matching Jobs")
st.write(f"Found {len(df)} job(s)")
st.dataframe(df[['title', 'company_name', 'state', 'city', 'work_type', 'description']])
