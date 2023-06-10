import streamlit as st
import pickle
import pandas as pd
import requests # to request from API

st.title('Movie Recommender System')

# Getting the movie names from the dataframe (importing DF as a dictionary)
movies_dict = pd.read_pickle('movie_dict.pkl')
movies = pd.DataFrame(movies_dict)

# Getting the similarity DF to be used in recommend fn.
similarity = pd.read_pickle('similarity.pkl')

# Creating a function'recommend' to get similar movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    # We use enumerate so that the index position stays intact (tuple) after sorting also
    # sorting to be done on 2nd col (cosine similarity) not on index hence lambda fn used
    # We need 1st to 5th item from the sorted list
    movies_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x: x[1])[1:6]
        
    # Getting the similar movies list to display
    recommended_movies =[]
    recommended_movies_posters= []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        
        recommended_movies.append(movies.iloc[i[0]].title)
        #Fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=3c150442effd5a565f449c1ea075c05e&language=en-US'.format(movie_id))
    data = response.json()
    
    return "https://image.tmdb.org/t/p/original/" + data['poster_path'] # complete poster path

# SELECTION: Fetching the selected movie name and display the same
selected_movie_name = st.selectbox(
'**Which Movie type you want recommendation for?**',
movies['title'].values)

# st.write('You selected:', selected_movie_name)


if st.button('Recommend'):
# Using 'recommend' fn to get similar movies
    recommendations = recommend(selected_movie_name)
# RECOMMENDATION OUTPUT  
    st.markdown(f"Based on your selection of <span style='font-weight:bold; color:red'>{selected_movie_name}</span>, we recommend 5 movies that are akin to your taste and bound to captivate your senses.", unsafe_allow_html=True)
    names,posters = recommend(selected_movie_name)
    for i in recommendations:
        # st.write(i)
        
        col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        # st.text(names[0],unsafe_allow_html=True)  #...without text wrap 
        st.image(posters[0], use_column_width=True)
        st.markdown(f"<p style='word-wrap: break-word'>{names[0]}</p>", unsafe_allow_html=True)
        

    with col2:
        st.image(posters[1], use_column_width=True)
        st.markdown(f"<p style='word-wrap: break-word'>{names[1]}</p>", unsafe_allow_html=True)
        
    with col3:
        st.image(posters[2], use_column_width=True)
        st.markdown(f"<p style='word-wrap: break-word'>{names[2]}</p>", unsafe_allow_html=True)
                
    with col4:
        st.image(posters[3], use_column_width=True)
        st.markdown(f"<p style='word-wrap: break-word'>{names[3]}</p>", unsafe_allow_html=True)

    with col5:
        st.image(posters[4], use_column_width=True)
        st.markdown(f"<p style='word-wrap: break-word'>{names[4]}</p>", unsafe_allow_html=True)
        