import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
df = pd.read_csv("dataset.csv")

# Clean column names
df.columns = df.columns.str.lower()

# Helper function to safely get columns
def safe_col(col):
    return df[col].fillna('') if col in df.columns else ''

# Build features safely (works even if some columns are missing)
df['features'] = (
    safe_col('genre') + " " +
    safe_col('cast') + " " +
    safe_col('actors') + " " +
    safe_col('director') + " " +
    safe_col('description') + " " +
    safe_col('plot')
)

# Vectorization
vectorizer = TfidfVectorizer(stop_words='english')
feature_matrix = vectorizer.fit_transform(df['features'])

# Similarity matrix
similarity = cosine_similarity(feature_matrix)

# Recommendation function
def recommend(movie_name):
    movie_name = movie_name.lower()

    if movie_name not in df['title'].str.lower().values:
        return ["Movie not found"]

    index = df[df['title'].str.lower() == movie_name].index[0]

    distances = list(enumerate(similarity[index]))
    sorted_movies = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]

    return [df.iloc[i[0]]['title'] for i in sorted_movies]