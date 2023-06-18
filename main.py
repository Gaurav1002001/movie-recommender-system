import pandas as pd
import requests
import streamlit as st
import pickle

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/find/{}?external_source=tmdb_id".format(movie_id)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxYWQwMmM4YjA2NzE3YzJhZmM5Y2RkYTc2NWIxNjJhMCIsInN1YiI6IjY0OGQ5ODk4NDJiZjAxMDEwMWJlMzI4YSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Tsk3_BDVkDC1k_tD-Z8smF29XBE-oU097GtuQll2VD4"
    }

    data = requests.get(url, headers=headers).json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']


def recommend(movie):
    # finding the index of movie in the dataframe
    movie_idx = movies[movies['title'] == movie].index[0]
    dist = similarity[movie_idx]
    movies_list = sorted(list(enumerate(dist)), reverse=True, key=lambda x: x[1])[1:11]

    movies_title = []
    # movies_poster = []
    for movie in movies_list:
        movies_title.append(movies.iloc[movie[0]].title)
        # movies_poster.append(fetch_poster(movie[0]))

    return movies_title


st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values)

if st.button('Recommend'):
    names = recommend(selected_movie_name)
    for name in names:
        st.write(name)

