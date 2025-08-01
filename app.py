import streamlit as st
import pickle
import pandas as pd
import requests

# Your OMDb API key (replace with your actual key)
OMDB_API_KEY = '12d75fbd'


def fetch_poster(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data.get('Response') == 'True' and data.get('Poster') != 'N/A':
        return data['Poster']
    else:
        return "https://via.placeholder.com/300x450.png?text=No+Poster+Found"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_lists = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    for i in movie_lists:
        title = movies.iloc[i[0]].title
        poster_url = fetch_poster(title)
        recommended_movies.append((title, poster_url))
    return recommended_movies


# Load data
movies_list = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_list)

# Streamlit UI
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox('Select a movie to get recommendations:', movies['title'].values)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)

    cols = st.columns(5)
    for idx, (title, poster_url) in enumerate(recommendations):
        with cols[idx]:
            st.text(title)
            st.image(poster_url)
