import streamlit as st
import requests
import time
from recommender import recommend, df

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="CineAI", layout="wide")

# -------------------------------
# SESSION STATE (WATCHLIST)
# -------------------------------
if "favorites" not in st.session_state:
    st.session_state.favorites = []

# -------------------------------
# SIDEBAR MENU
# -------------------------------
st.sidebar.title("🎬 CineAI Menu")
page = st.sidebar.selectbox(
    "Navigate",
    ["Home", "Recommend Movies", "Trending Movies", "My Watchlist"]
)

# -------------------------------
# OMDB POSTER FUNCTION
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
# HOME PAGE
# -------------------------------
if page == "Home":
    st.title("🍿 Welcome to CineAI")

    st.markdown("""
    ### 🎬 About CineAI

    CineAI is an **AI-based movie recommendation system** that suggests Indian movies based on user preferences.

    It uses **Machine Learning (TF-IDF + Cosine Similarity)** to find similar movies.

    #### 🚀 Features:
    - 🎥 AI Movie Recommendations  
    - 🧠 Content-Based Filtering  
    - 🖼️ Movie Posters (OMDb API)  
    - 🔥 Trending Movies  
    - ❤️ Watchlist Feature  
    - 📱 Netflix-style UI  

    #### 🎯 Objective:
    Improve movie discovery using AI.
    """)

    st.subheader("👉 Use sidebar to explore")

# -------------------------------
# RECOMMEND PAGE
# -------------------------------
elif page == "Recommend Movies":

    st.title("🎯 Get Movie Recommendations")

    movie_list = df['title'].values
    selected_movie = st.selectbox("🎥 Select a Movie", movie_list)

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

                if st.button(f"❤️ Add", key=movie):
                    if movie not in st.session_state.favorites:
                        st.session_state.favorites.append(movie)
                        st.success("Added to Watchlist!")

# -------------------------------
# TRENDING PAGE
# -------------------------------
elif page == "Trending Movies":

    st.title("🔥 Trending Indian Movies")

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

# -------------------------------
# WATCHLIST PAGE
# -------------------------------
elif page == "My Watchlist":

    st.title("❤️ My Watchlist")

    if len(st.session_state.favorites) == 0:
        st.write("No movies added yet 😢")
    else:
        cols = st.columns(5)

        for i, movie in enumerate(st.session_state.favorites):
            poster = fetch_poster(movie)

            with cols[i % 5]:
                st.image(poster, use_column_width=True)
                st.write(movie)
