import streamlit as st
import requests
import pandas as pd
import time
from recommender import recommend, df

st.set_page_config(page_title="CineAI", layout="wide")

# -------------------------------
# 🎨 DARK THEME UI
# -------------------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 📌 SIDEBAR MENU
# -------------------------------
st.sidebar.title("🎬 CineAI Menu")
page = st.sidebar.selectbox("Navigate", ["Home", "Recommend Movies", "Trending Movies"])

# -------------------------------
# 🎬 OMDB POSTER FUNCTION
# -------------------------------
def fetch_poster(movie_name):
    api_key = "f76d24eb"

    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    if data.get("Poster") and data["Poster"] != "N/A":
        return data["Poster"]

    return "https://via.placeholder.com/300x450?text=No+Image"

# -------------------------------
# 🏠 HOME PAGE
# -------------------------------
if page == "Home":
    st.title("🍿 Welcome to CineAI")
    st.subheader("AI-based Indian Movie Recommendation System")
    st.write("Discover movies like Netflix using AI ✨")

# -------------------------------
# 🤖 RECOMMEND PAGE
# -------------------------------
elif page == "Recommend Movies":

    st.title("🎯 Get Movie Recommendations")

    # Search bar
    search = st.text_input("🔍 Search a movie")

    movie_list = df['title'].values
    selected_movie = st.selectbox("🎥 Select Movie", movie_list)

    # Genre filter
    genre_filter = st.selectbox("🎭 Filter by Genre (optional)", ["All"] + list(df['genre'].dropna().unique()))

    if st.button("Recommend"):

        with st.spinner("Finding best movies for you... 🎬"):
            time.sleep(2)

        results = recommend(selected_movie)

        st.subheader("🍿 Recommended Movies")

        cols = st.columns(5)

        for i, movie in enumerate(results):
            poster = fetch_poster(movie)

            with cols[i % 5]:
                st.image(poster, use_column_width=True)
                st.write(movie)

# -------------------------------
# 🔥 TRENDING PAGE
# -------------------------------
elif page == "Trending Movies":

    st.title("🔥 Trending Indian Movies")

    st.write("Top movies based on dataset")

    # if rating column exists
    if "rating" in df.columns:
        top_movies = df.sort_values("rating", ascending=False).head(10)
    else:
        top_movies = df.head(10)

    cols = st.columns(5)

    for i, row in top_movies.iterrows():
        poster = fetch_poster(row['title'])

        with cols[i % 5]:
            st.image(poster, use_column_width=True)
            st.write(row['title'])
