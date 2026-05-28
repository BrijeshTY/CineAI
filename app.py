import streamlit as st
import requests
import time
from recommender import recommend, df

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="CineAI", layout="wide")

# -------------------------------
# SESSION STATE (IMPORTANT FIX)
# -------------------------------
if "favorites" not in st.session_state:
    st.session_state.favorites = []

# -------------------------------
# OMDB POSTER FUNCTION
# -------------------------------
def fetch_poster(movie_name):
    api_key = "f76d24eb"  # 🔴 replace this

    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    if data.get("Poster") and data["Poster"] != "N/A":
        return data["Poster"]

    return "https://via.placeholder.com/300x450?text=No+Image"

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("🎬 CineAI Menu")
page = st.sidebar.selectbox(
    "Navigate",
    ["Home", "Recommend Movies", "Trending Movies", "My Watchlist"]
)

# -------------------------------
# HOME
# -------------------------------
if page == "Home":
    st.title("🍿 CineAI - AI Movie Recommender")

    st.markdown("""
    ### 🎬 About CineAI
    AI-based Indian movie recommendation system using ML.

    ✔ TF-IDF + Cosine Similarity  
    ✔ Movie Posters via OMDb API  
    ✔ Watchlist Feature  
    ✔ Netflix-style UI  
    """)

# -------------------------------
# RECOMMENDATION PAGE
# -------------------------------
elif page == "Recommend Movies":

    st.title("🎯 Movie Recommendations")

    movie_list = df['title'].values
    selected_movie = st.selectbox("🎥 Select a Movie", movie_list)

    if st.button("Recommend"):

        with st.spinner("Finding best movies... 🎬"):
            time.sleep(1)

        results = recommend(selected_movie)

        st.subheader("🍿 Recommended Movies")

        cols = st.columns(5)

        for i, movie in enumerate(results):

            poster = fetch_poster(movie)

            with cols[i % 5]:
                st.image(poster, use_column_width=True)
                st.write(movie)

                # ✅ FIXED WATCHLIST BUTTON
                btn_key = f"fav_{movie}"

                if st.button("❤️ Add to Watchlist", key=btn_key):
                    if movie not in st.session_state.favorites:
                        st.session_state.favorites.append(movie)
                        st.success(f"Added {movie} ✅")

# -------------------------------
# TRENDING PAGE
# -------------------------------
elif page == "Trending Movies":

    st.title("🔥 Trending Movies")

    if "rating" in df.columns:
        top_movies = df.sort_values("rating", ascending=False).head(10)
    else:
        top_movies = df.head(10)

    cols = st.columns(5)

    for i, row in enumerate(top_movies.itertuples()):
        poster = fetch_poster(row.title)

        with cols[i % 5]:
            st.image(poster, use_column_width=True)
            st.write(row.title)

# -------------------------------
# WATCHLIST PAGE
# -------------------------------
elif page == "My Watchlist":

    st.title("❤️ My Watchlist")

    if len(st.session_state.favorites) == 0:
        st.warning("No movies added yet 😢")
    else:
        cols = st.columns(5)

        for i, movie in enumerate(st.session_state.favorites):

            poster = fetch_poster(movie)

            with cols[i % 5]:
                st.image(poster, use_column_width=True)
                st.write(movie)
