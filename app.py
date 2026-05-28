import streamlit as st
import requests
from recommender import recommend, df

st.set_page_config(page_title="CineAI", layout="wide")

st.title("🎬 CineAI - Indian Movie Recommendation System")

# -------------------------------
# OMDb Poster Function
# -------------------------------
def fetch_poster(movie_name):
    api_key = "f76d24eb"  # 🔴 Replace this

    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    if data.get("Poster") and data["Poster"] != "N/A":
        return data["Poster"]

    return "https://via.placeholder.com/300x450?text=No+Image"


# -------------------------------
# Movie Selection
# -------------------------------
movie_list = df['title'].values
selected_movie = st.selectbox("🎥 Select a Movie", movie_list)

# -------------------------------
# Recommendation Button
# -------------------------------
if st.button("Recommend"):
    results = recommend(selected_movie)

    st.subheader("🍿 Recommended Movies")

    cols = st.columns(len(results))

    for i, movie in enumerate(results):
        poster_url = fetch_poster(movie)

        with cols[i]:
            st.image(poster_url, use_column_width=True)
            st.write(movie)