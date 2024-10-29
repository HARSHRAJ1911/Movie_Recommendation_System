
import pandas as pd
import streamlit as st
import pickle
import requests


def fetch_poster(movie_id):
    try:
        # Replace with your valid API key
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=0c0b7dd774cfacd8463415194c360f36")
        data = response.json()

        if 'poster_path' in data and data['poster_path'] is not None:
            poster_url = f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
            print(f"Poster URL fetched: {poster_url}")
            return poster_url
        else:
            print(f"No poster available for movie_id: {movie_id}")
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except Exception as e:
        print(f"Error fetching poster for movie_id: {movie_id}. Error: {e}")
        return "https://via.placeholder.com/500x750?text=Error+Fetching+Poster"







movies_lists = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_lists)
movies_list = movies['title'].values
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox("Select a movie:", movies_list)

st.write("You selected:", selected_movie_name)

def recommend(movie):
    global movies_list
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:16]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        poster_url = fetch_poster(movie_id)
        recommended_movies_posters.append(poster_url)

    return recommended_movies, recommended_movies_posters

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(15)

    for i in range(15):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])