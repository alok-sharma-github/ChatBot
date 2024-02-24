
from utils import extract_info, preprocess_data, get_similarity_matrix, get_recommendations
from data import load_dataset

file_path = "movies (1).csv"

# Dataset ko load karein
movies = load_dataset(file_path)

intents = {
    'greetings': ['Hey','Hi','Good Morning'],
    'movie_info': ['movie', 'film', 'about','plot','story'],
    'genre_info': ['genre', 'type', 'category'],
    'cast_info': ['cast', 'actors', 'actresses','lead role','hero','heroine','lead actor','lead actress','acted'],
    'director_info': ['director', 'filmmaker', 'producer','directed','produced'],
    'release_date_info': ['release date', 'when', 'premiere','released'],
    'revenue_info': ['revenue', 'box office', 'earnings','collection'],
    'runtime_info': ['duration', 'length', 'runtime','long'],
    'rating_info': ['rating', 'score', 'imdb'],
    'recommendations': ['recommend', 'suggest', 'watch','like', 'similar to'],
    }

responses = {
    'greetings': "Your servant at your service. Let me know how can I help you ?",
    'movie_info': "Here's some information about the movie '{movie_title}': {overview}",
    'genre_info': "The genre of '{movie_title}' is {genre}.",
    'cast_info': "The main cast of '{movie_title}' includes: {cast}",
    'director_info': "The director of '{movie_title}' is {director}.",
    'release_date_info': "The movie '{movie_title}' was released on {release_date}.",
    'revenue_info': "The movie '{movie_title}' earned {revenue} at the box office.",
    'runtime_info': "The runtime of '{movie_title}' is {runtime} minutes.",
    'rating_info': "The average rating of '{movie_title}' is {rating}.",
    'recommendations': "{recommendations}",
    }


# Function to get information about a specific movie
def get_movie_info(query):
    movie_data = extract_info(movies) 
    for movie_title, genre, budget, cast, director, overview, languages, release_date, revenue, popularity, tagline, keywords,runtime in movie_data:
        if movie_title.lower() in query:
            return responses['movie_info'].format(movie_title=movie_title, 
                                                  overview=overview,
                                                  genre=genre,
                                                  cast=cast,
                                                  director=director,
                                                  release_date=release_date,
                                                  revenue=revenue,                                                  
                                                  popularity=popularity,
                                                  budget= budget,
                                                  languages=languages,
                                                  tagline=tagline,
                                                  keywords = keywords)
    return "Sorry, I couldn't find information about that movie."
def get_genre_info(query):
    movie_data = extract_info(movies) 
    for movie_title, genre, budget, cast, director, overview, languages, release_date, revenue, popularity, tagline, keywords,runtime in movie_data:
        if movie_title.lower() in query:
            return responses['genre_info'].format(movie_title=movie_title, 
                                                  overview=overview,
                                                  genre=genre,
                                                  cast=cast,
                                                  director=director,
                                                  release_date=release_date,
                                                  revenue=revenue,                                                  
                                                  popularity=popularity,
                                                  budget= budget,
                                                  languages=languages,
                                                  tagline=tagline,
                                                  keywords = keywords)
    return "Sorry, I couldn't find information about that movie."
def get_cast_info(query):
    movie_data = extract_info(movies)  # Call extract_info to get movie data
    for movie_title, genre, budget, cast, director, overview, languages, release_date, revenue, popularity, tagline, keywords,runtime in movie_data:
        if movie_title.lower() in query:
            return responses['cast_info'].format(movie_title=movie_title, 
                                                  overview=overview,
                                                  genre=genre,
                                                  cast=cast,
                                                  director=director,
                                                  release_date=release_date,
                                                  revenue=revenue,                                                  
                                                  popularity=popularity,
                                                  budget= budget,
                                                  languages=languages,
                                                  tagline=tagline,
                                                  keywords = keywords)
    return "Sorry, I couldn't find information about that movie."
def get_director_info(query):
    movie_data = extract_info(movies)  # Call extract_info to get movie data
    for movie_title, genre, budget, cast, director, overview, languages, release_date, revenue, popularity, tagline, keywords,runtime in movie_data:
        if movie_title.lower() in query:
            return responses['director_info'].format(movie_title=movie_title, 
                                                  overview=overview,
                                                  genre=genre,
                                                  cast=cast,
                                                  director=director,
                                                  release_date=release_date,
                                                  revenue=revenue,                                                  
                                                  popularity=popularity,
                                                  budget= budget,
                                                  languages=languages,
                                                  tagline=tagline,
                                                  keywords = keywords)
    return "Sorry, I couldn't find information about that movie."
def get_release_date_info(query):
    movie_data = extract_info(movies)  # Call extract_info to get movie data
    for movie_title, genre, budget, cast, director, overview, languages, release_date, revenue, popularity, tagline, keywords,runtime in movie_data:
        if movie_title.lower() in query:
            return responses['release_date_info'].format(movie_title=movie_title, 
                                                  overview=overview,
                                                  genre=genre,
                                                  cast=cast,
                                                  director=director,
                                                  release_date=release_date,
                                                  revenue=revenue,                                                  
                                                  popularity=popularity,
                                                  budget= budget,
                                                  languages=languages,
                                                  tagline=tagline,
                                                  keywords = keywords)
    return "Sorry, I couldn't find information about that movie."
def get_revenue_info(query):
    movie_data = extract_info(movies)  # Call extract_info to get movie data
    for movie_title, genre, budget, cast, director, overview, languages, release_date, revenue, popularity, tagline, keywords,runtime in movie_data:
        if movie_title.lower() in query:
            return responses['revenue_info'].format(movie_title=movie_title, 
                                                  overview=overview,
                                                  genre=genre,
                                                  cast=cast,
                                                  director=director,
                                                  release_date=release_date,
                                                  revenue=revenue,                                                  
                                                  popularity=popularity,
                                                  budget= budget,
                                                  languages=languages,
                                                  tagline=tagline,
                                                  keywords = keywords)
    return "Sorry, I couldn't find information about that movie."
def get_runtime_info(query):
    movie_data = extract_info(movies)  # Call extract_info to get movie data
    for movie_title, genre, budget, cast, director, overview, languages, release_date, revenue, popularity, tagline, keywords, runtime in movie_data:
        if movie_title.lower() in query:
            return responses['runtime_info'].format(movie_title=movie_title, 
                                                  overview=overview,
                                                  genre=genre,
                                                  cast=cast,
                                                  director=director,
                                                  release_date=release_date,
                                                  revenue=revenue,                                                  
                                                  popularity=popularity,
                                                  budget= budget,
                                                  languages=languages,
                                                  tagline=tagline,
                                                  keywords = keywords,
                                                  runtime = runtime)
    return "Sorry, I couldn't find information about that movie."
def get_rating_info(query):
    movie_data = extract_info(movies)  # Call extract_info to get movie data
    for movie_title, genre, budget, cast, director, overview, languages, release_date, revenue, popularity, tagline, keywords, runtime in movie_data:
        if movie_title.lower()  in query:
            return responses['rating_info'].format(movie_title=movie_title, 
                                                  overview=overview,
                                                  genre=genre,
                                                  cast=cast,
                                                  director=director,
                                                  release_date=release_date,
                                                  revenue=revenue,                                                  
                                                  rating=popularity,
                                                  budget= budget,
                                                  languages=languages,
                                                  tagline=tagline,
                                                  keywords = keywords,
                                                  runtime = runtime)
    return "Sorry, I couldn't find information about that movie."

def get_recommended_list(query, movies, similarity_matrix):
    movie_data = extract_info(movies)  # Call extract_info to get movie data
    for movie_title, genre, budget, cast, director, overview, languages, release_date, revenue, popularity, tagline, keywords, runtime in movie_data:
        if movie_title.lower() in query.lower():
            recommendations = get_recommendations(movie_title, movies, similarity_matrix)
            if isinstance(recommendations, str):  # If get_recommendations returns an error message
                return recommendations
            else:
                return recommendations
    return "Sorry, I couldn't find information about that movie."









def handle_query(query):
    query = query.lower()  # Convert query to lowercase
    for intent, keywords in intents.items():
        for keyword in keywords:
            if keyword in query:
                if intent == 'movie_info' or intent == 'general':
                    return get_movie_info(query)
                if intent == 'genre_info':
                    return get_genre_info(query)
                if intent == 'cast_info':
                    return get_cast_info(query)
                if intent == 'director_info':
                    return get_director_info(query)
                if intent == 'release_date_info':
                    return get_release_date_info(query)
                if intent == 'revenue_info':
                    return get_revenue_info(query)
                if intent == 'runtime_info':
                    return get_runtime_info(query)
                if intent == 'rating_info':
                    return get_rating_info(query)
                if intent == 'recommendations':
                    recommendations = get_recommended_list(query, movies.copy(), similarity_matrix)
                    return responses['recommendations'].format(recommendations="\n".join(recommendations))
    return "Sorry, I don't understand that query."
