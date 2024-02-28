import requests
import pandas as pd
import streamlit as st

API_KEY = "0b1a7d90a81eb2fdf93a9e59dd6fe48b"
BASE_URL = "https://api.themoviedb.org/3"


def fetch_movie_id(movie_name):
    url = f"{BASE_URL}/search/movie"
    params = {
        "api_key": API_KEY,
        "query": movie_name
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            return data['results'][0]['id']  # Return the first result
    return None

def fetch_movie_suggestions(query):
    url = f"{BASE_URL}/search/movie"
    params = {
        'api_key': API_KEY,
        'query': query
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data:
            suggestions = [movie['title'] for movie in data['results']]
            return suggestions
    return []


def fetch_movie_data(movie_name, api_key):
    movie_id = fetch_movie_id(movie_name)
    # Fetch movie details
    movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}"

    # Fetch movie details
    movie_response = requests.get(movie_url)
    if movie_response.status_code == 200:
        movie_data = movie_response.json()
    else:
        return None, "Failed to fetch movie data."

    # Fetch movie credits
    credits_response = requests.get(credits_url)
    if credits_response.status_code == 200:
        credits_data = credits_response.json()
    else:
        return None, "Failed to fetch movie credits."

    return movie_data, credits_data

# Extract Info
def extract_info(movie_data, credits_data):
    # Extract relevant information from movie data
    movie_title = movie_data['title']
    movie_genres = ', '.join([genre['name'] for genre in movie_data['genres']])
    movie_overview = movie_data['overview']
    movie_release_date = movie_data['release_date']
    movie_popularity = movie_data['popularity']
    languages = ', '.join([lang['name'] for lang in movie_data['spoken_languages']])
    production_companies = ', '.join([company['name'] for company in movie_data['production_companies']])
    # Initialize variables for lead actor, actress, and director
    lead_actor = None
    lead_actress = None
    director = None

    # Extract cast information from credits data
    cast = [{'name': actor['name'], 'character': actor['character'], 'gender': actor['gender'], 'popularity': actor['popularity']} for actor in credits_data['cast']]
    for actor in cast:
        if actor['gender'] == 2:  # Assuming gender 2 represents male actors
            if lead_actor is None or actor['popularity'] > lead_actor['popularity']:
                lead_actor = actor
        elif actor['gender'] == 1:  # Assuming gender 1 represents female actors
            if lead_actress is None or actor['popularity'] > lead_actress['popularity']:
                lead_actress = actor

    # Extract director information from credits data
    crew = [member for member in credits_data['crew'] if member['job'] == 'Director']
    if crew:
        director = crew[0]['name']

    return (movie_title, movie_genres, movie_overview, lead_actor, lead_actress, director, movie_release_date, movie_popularity, languages, production_companies)

# Intent - Response
intents = {
    
    'movie_info': ['movie', 'film', 'about','plot','story'],
    'genre_info': ['genre', 'type', 'category'],
    'cast_info': ['cast', 'actors', 'actresses','lead role','hero','heroine','lead actor','lead actress','acted'],
    'director_info': ['director', 'filmmaker', 'producer','directed','produced'],
    'release_date_info': ['release date', 'when', 'premiere','released'],
    'revenue_info': ['revenue', 'box office', 'earnings','collection'],
    'runtime_info': ['duration', 'length', 'runtime','long'],
    'rating_info': ['rating', 'score', 'imdb'],
    'production_info': ['produced', 'production'],
    'recommendations': ['recommend', 'suggest', 'watch','like', 'similar to'],
    }

responses = {
    
    'movie_info': "Here's some information about the movie '{movie_title}': {overview}",
    'genre_info': "The genre of '{movie_title}' is {genre}.",
    'cast_info': "The main cast of '{movie_title}' includes: {cast}",
    'director_info': "The director of '{movie_title}' is {director}.",
    'release_date_info': "The movie '{movie_title}' was released on {release_date}.",
    'revenue_info': "The movie '{movie_title}' earned {revenue} at the box office.",
    'runtime_info': "The runtime of '{movie_title}' is {runtime} minutes.",
    'rating_info': "The popularity score of '{movie_title}' is {popularity}.",
    'production_info': "The production companies of '{movie_title}' are:  {production_companies}.",
    'recommendations': "{recommendations}",
    }

# Extracting Specific Info
def get_movie_info(query):
    # Fetch movie data using the query
    movie_data, credits_data = fetch_movie_data(query, API_KEY)
    
    # If movie data is fetched successfully
    if movie_data and credits_data:
        # Extract relevant information from movie data and credits data
        movie_title, movie_genres, movie_overview, lead_actor, lead_actress, director, movie_release_date, movie_popularity, languages, production_companies = extract_info(movie_data, credits_data)
        
        # Format the response with the extracted information
        return responses['movie_info'].format(movie_title=movie_title, 
                                              overview=movie_overview,
                                              genre=movie_genres,
                                              cast=f"{lead_actor['name']} as lead actor, {lead_actress['name']} as lead actress",  # Assuming lead actor and actress are required
                                              director=director,
                                              release_date=movie_release_date,
                                              revenue="Not available",  # Adjust as needed based on available data
                                              popularity=movie_popularity,
                                              budget="Not available",  # Adjust as needed based on available data
                                              languages=languages,
                                              tagline="Not available",  # Adjust as needed based on available data
                                              keywords="Not available",  # Adjust as needed based on available data
                                              runtime="Not available"  # Adjust as needed based on available data
                                              )
    else:
        return "Sorry, I couldn't find information about that movie."
def get_genre_info(query):
    # Fetch movie data using the query
    movie_data, credits_data = fetch_movie_data(query, API_KEY)
    
    # If movie data is fetched successfully
    if movie_data and credits_data:
        # Extract relevant information from movie data and credits data
        movie_title, movie_genres, movie_overview, lead_actor, lead_actress, director, movie_release_date, movie_popularity, languages, production_companies = extract_info(movie_data, credits_data)
        
        # Format the response with the extracted information
        return responses['genre_info'].format(movie_title=movie_title, 
                                              overview=movie_overview,
                                              genre=movie_genres,
                                              cast=f"{lead_actor['name']} as lead actor, {lead_actress['name']} as lead actress",  # Assuming lead actor and actress are required
                                              director=director,
                                              release_date=movie_release_date,
                                              revenue="Not available",  # Adjust as needed based on available data
                                              popularity=movie_popularity,
                                              budget="Not available",  # Adjust as needed based on available data
                                              languages=languages,
                                              tagline="Not available",  # Adjust as needed based on available data
                                              keywords="Not available",  # Adjust as needed based on available data
                                              runtime="Not available"  # Adjust as needed based on available data
                                              )
    else:
        return "Sorry, I couldn't find information about that movie."
def get_director_info(query):
    # Fetch movie data using the query
    movie_data, credits_data = fetch_movie_data(query, API_KEY)
    
    # If movie data is fetched successfully
    if movie_data and credits_data:
        # Extract relevant information from movie data and credits data
        movie_title, movie_genres, movie_overview, lead_actor, lead_actress, director, movie_release_date, movie_popularity, languages, production_companies = extract_info(movie_data, credits_data)
        
        # Format the response with the extracted information
        return responses['director_info'].format(movie_title=movie_title, 
                                              overview=movie_overview,
                                              genre=movie_genres,
                                              cast=f"{lead_actor['name']} as lead actor, {lead_actress['name']} as lead actress",  # Assuming lead actor and actress are required
                                              director=director,
                                              release_date=movie_release_date,
                                              revenue="Not available",  # Adjust as needed based on available data
                                              popularity=movie_popularity,
                                              budget="Not available",  # Adjust as needed based on available data
                                              languages=languages,
                                              tagline="Not available",  # Adjust as needed based on available data
                                              keywords="Not available",  # Adjust as needed based on available data
                                              runtime="Not available"  # Adjust as needed based on available data
                                              )
    else:
        return "Sorry, I couldn't find information about that movie."
def get_cast_info(query):
    # Fetch movie data using the query
    movie_data, credits_data = fetch_movie_data(query, API_KEY)
    
    # If movie data is fetched successfully
    if movie_data and credits_data:
        # Extract relevant information from movie data and credits data
        movie_title, movie_genres, movie_overview, lead_actor, lead_actress, director, movie_release_date, movie_popularity, languages, production_companies = extract_info(movie_data, credits_data)
        
        # Format the response with the extracted information
        return responses['cast_info'].format(movie_title=movie_title, 
                                              overview=movie_overview,
                                              genre=movie_genres,
                                              cast=f"{lead_actor['name']} as lead actor, {lead_actress['name']} as lead actress",  # Assuming lead actor and actress are required
                                              director=director,
                                              release_date=movie_release_date,
                                              revenue="Not available",  # Adjust as needed based on available data
                                              popularity=movie_popularity,
                                              budget="Not available",  # Adjust as needed based on available data
                                              languages=languages,
                                              tagline="Not available",  # Adjust as needed based on available data
                                              keywords="Not available",  # Adjust as needed based on available data
                                              runtime="Not available"  # Adjust as needed based on available data
                                              )
    else:
        return "Sorry, I couldn't find information about that movie."
def get_release_date_info(query):
    # Fetch movie data using the query
    movie_data, credits_data = fetch_movie_data(query, API_KEY)
    
    # If movie data is fetched successfully
    if movie_data and credits_data:
        # Extract relevant information from movie data and credits data
        movie_title, movie_genres, movie_overview, lead_actor, lead_actress, director, movie_release_date, movie_popularity, languages, production_companies = extract_info(movie_data, credits_data)
        
        # Format the response with the extracted information
        return responses['release_date_info'].format(movie_title=movie_title, 
                                              overview=movie_overview,
                                              genre=movie_genres,
                                              cast=f"{lead_actor['name']} as lead actor, {lead_actress['name']} as lead actress",  # Assuming lead actor and actress are required
                                              director=director,
                                              release_date=movie_release_date,
                                              revenue="Not available",  # Adjust as needed based on available data
                                              popularity=movie_popularity,
                                              budget="Not available",  # Adjust as needed based on available data
                                              languages=languages,
                                              tagline="Not available",  # Adjust as needed based on available data
                                              keywords="Not available",  # Adjust as needed based on available data
                                              runtime="Not available",
                                               production_companies=production_companies # Adjust as needed based on available data
                                              )
    else:
        return "Sorry, I couldn't find information about that movie."
def get_production_info(query):
    # Fetch movie data using the query
    movie_data, credits_data = fetch_movie_data(query, API_KEY)
    
    # If movie data is fetched successfully
    if movie_data and credits_data:
        # Extract relevant information from movie data and credits data
        movie_title, movie_genres, movie_overview, lead_actor, lead_actress, director, movie_release_date, movie_popularity, languages, production_companies = extract_info(movie_data, credits_data)
        
        # Format the response with the extracted information
        return responses['production_info'].format(movie_title=movie_title, 
                                              overview=movie_overview,
                                              genre=movie_genres,
                                              cast=f"{lead_actor['name']} as lead actor, {lead_actress['name']} as lead actress",  # Assuming lead actor and actress are required
                                              director=director,
                                              release_date=movie_release_date,
                                              revenue="Not available",  # Adjust as needed based on available data
                                              popularity=movie_popularity,
                                              budget="Not available",  # Adjust as needed based on available data
                                              languages=languages,
                                              tagline="Not available",  # Adjust as needed based on available data
                                              keywords="Not available",  # Adjust as needed based on available data
                                              runtime="Not available",
                                               production_companies=production_companies # Adjust as needed based on available data
                                              )
    else:
        return "Sorry, I couldn't find information about that movie."
def get_popularity_info(query):
    # Fetch movie data using the query
    movie_data, credits_data = fetch_movie_data(query, API_KEY)
    
    # If movie data is fetched successfully
    if movie_data and credits_data:
        # Extract relevant information from movie data and credits data
        movie_title, movie_genres, movie_overview, lead_actor, lead_actress, director, movie_release_date, movie_popularity, languages, production_companies = extract_info(movie_data, credits_data)
        
        # Format the response with the extracted information
        return responses['rating_info'].format(movie_title=movie_title, 
                                              overview=movie_overview,
                                              genre=movie_genres,
                                              cast=f"{lead_actor['name']} as lead actor, {lead_actress['name']} as lead actress",  # Assuming lead actor and actress are required
                                              director=director,
                                              release_date=movie_release_date,
                                              revenue="Not available",  # Adjust as needed based on available data
                                              popularity=movie_popularity,
                                              budget="Not available",  # Adjust as needed based on available data
                                              languages=languages,
                                              tagline="Not available",  # Adjust as needed based on available data
                                              keywords="Not available",  # Adjust as needed based on available data
                                              runtime="Not available",
                                               production_companies=production_companies # Adjust as needed based on available data
                                              )
    else:
        return "Sorry, I couldn't find information about that movie."
def get_language_info(query):
    # Fetch movie data using the query
    movie_data, credits_data = fetch_movie_data(query, API_KEY)
    
    # If movie data is fetched successfully
    if movie_data and credits_data:
        # Extract relevant information from movie data and credits data
        movie_title, movie_genres, movie_overview, lead_actor, lead_actress, director, movie_release_date, movie_popularity, languages, production_companies = extract_info(movie_data, credits_data)
        
        # Format the response with the extracted information
        return responses['language_info'].format(movie_title=movie_title, 
                                              overview=movie_overview,
                                              genre=movie_genres,
                                              cast=f"{lead_actor['name']} as lead actor, {lead_actress['name']} as lead actress",  # Assuming lead actor and actress are required
                                              director=director,
                                              release_date=movie_release_date,
                                              revenue="Not available",  # Adjust as needed based on available data
                                              popularity=movie_popularity,
                                              budget="Not available",  # Adjust as needed based on available data
                                              languages=languages,
                                              tagline="Not available",  # Adjust as needed based on available data
                                              keywords="Not available",  # Adjust as needed based on available data
                                              runtime="Not available",
                                               production_companies=production_companies # Adjust as needed based on available data
                                              )
    else:
        return "Sorry, I couldn't find information about that movie."

# Handle Query
# def handle_query(query):
#     print("Original query:", query)  # Debugging step: Print original query
#     query = query.lower()  # Convert query to lowercase
#     print("Lowercased query:", query)  # Debugging step: Print lowercased query
    
#     # Split the query into words
#     words = query.split()
    
#     # Check if the first word indicates an intent
#     for intent, keywords in intents.items():
#         if words[0] in keywords:
#             print("Intent matched:", intent)  # Debugging step: Print matched intent
#             if intent == 'movie_info':
#                 movie_name = ' '.join(words[1:])  # Extract the movie name
#                 print("Movie name:", movie_name)  # Debugging step: Print extracted movie name
#                 return get_movie_info(movie_name)  # Pass the movie name to get_movie_info
    
#     print("No intent matched.")  # Debugging step: Print if no intent matched
#     return "Sorry, I don't understand that query."

# APP
st.markdown(
    """
    <style>
    /* Add custom styles here */
    .stApp {
        font-family: 'Arial', sans-serif;
    }
    .stTextInput>div>div>input {
        font-size: 16px;
        color: #333333;
        background-color: #f2f2f2;
        border-radius: 10px;
        padding: 10px;
        border: 2px solid #cccccc;
    }
    .stMarkdown {
        font-size: 18px;
        color: #444444;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("IMDB ChatBot v-1.2")
query = st.text_input("Enter [intent] [movie name]")
st.markdown("Intents: movie, genre, cast, released, rating, language, production, director")
query = query.lower()
words = query.split()

# movie_title, movie_genres, movie_overview, lead_actor, lead_actress, 
#director, movie_release_date, movie_popularity, languages, production_companies
if words:
    for intent, keywords in intents.items():
        if words[0] in keywords:
            st.write("Intent matched:", intent)
            if intent == 'movie_info':
                movie_name = ' '.join(words[1:])
                st.write('You selected:', movie_name)
                suggested_list = fetch_movie_suggestions(movie_name)
                selected_movie = st.selectbox("choose: ",suggested_list)
                movie_info = get_movie_info(selected_movie)
                st.text_area('Info:', movie_info)
            if intent == 'genre_info':
                movie_name = ' '.join(words[1:])
                st.write('You selected:', movie_name)
                suggested_list = fetch_movie_suggestions(movie_name)
                selected_movie = st.selectbox("choose: ",suggested_list)
                movie_info = get_genre_info(selected_movie)
                st.text_area('Info:', movie_info)
            if intent == 'director_info':
                movie_name = ' '.join(words[1:])
                st.write('You selected:', movie_name)
                suggested_list = fetch_movie_suggestions(movie_name)
                selected_movie = st.selectbox("choose: ",suggested_list)
                movie_info = get_director_info(selected_movie)
                st.text_area('Info:', movie_info)
            if intent == 'cast_info':
                movie_name = ' '.join(words[1:])
                st.write('You selected:', movie_name)
                suggested_list = fetch_movie_suggestions(movie_name)
                selected_movie = st.selectbox("choose: ",suggested_list)
                movie_info = get_cast_info(selected_movie)
                st.text_area('Info:', movie_info)
            if intent == 'release_date_info':
                movie_name = ' '.join(words[1:])
                st.write('You selected:', movie_name)
                suggested_list = fetch_movie_suggestions(movie_name)
                selected_movie = st.selectbox("choose: ",suggested_list)
                movie_info = get_release_date_info(selected_movie)
                st.text_area('Info:', movie_info)
            if intent == 'production_info':
                movie_name = ' '.join(words[1:])
                st.write('You selected:', movie_name)
                suggested_list = fetch_movie_suggestions(movie_name)
                selected_movie = st.selectbox("choose: ",suggested_list)
                movie_info = get_production_info(selected_movie)
                st.text_area('Info:', movie_info)
            if intent == 'rating_info':
                movie_name = ' '.join(words[1:])
                st.write('You selected:', movie_name)
                suggested_list = fetch_movie_suggestions(movie_name)
                selected_movie = st.selectbox("choose: ",suggested_list)
                movie_info = get_popularity_info(selected_movie)
                st.text_area('Info:', movie_info)
            if intent == 'language_info':
                movie_name = ' '.join(words[1:])
                st.write('You selected:', movie_name)
                suggested_list = fetch_movie_suggestions(movie_name)
                selected_movie = st.selectbox("choose: ",suggested_list)
                movie_info = get_language_info(selected_movie)
                st.text_area('Info:', movie_info)

else: st.write("Intents: movie, genre, cast, released, rating, language, production, director")


    
