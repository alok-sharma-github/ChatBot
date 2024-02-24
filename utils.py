import numpy as np
import pandas as pd
# once we complete, user gives name which might have error--closest match
import difflib 
#vectorizer function --> convert textual data to numerical value
from sklearn.feature_extraction.text import TfidfVectorizer
# similarity score of all different movie with input movie name
from sklearn.metrics.pairwise import cosine_similarity
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches
from data import load_dataset
file_path = "C:\\Users\\alok\Documents\\book\Projects\\recommender\\movies (1).csv"
# Dataset ko load karein
movies = load_dataset(file_path)


def extract_info(dataset):
    """
    Extract movie titles, genres, budget, cast, director, overview, languages,
    release date, revenue, and popularity,keywords,tagline from the dataset.
    
    Args:
    dataset (DataFrame): The movie dataset.
    
    Returns:
    list: A list of tuples containing movie titles, genres, budget, cast, director,
          overview, languages, release date, revenue, and popularity.
    """    
    
    movie_titles = dataset["title"]
    movie_keywords = dataset["keywords"]
    movie_tagline = dataset["tagline"]
    movie_genres = dataset['genres']
    movie_budgets = dataset['budget']
    movie_cast = dataset['cast']
    movie_directors = dataset['director']
    movie_overviews = dataset['overview']
    movie_languages = dataset['spoken_languages']
    movie_release_dates = dataset['release_date']
    movie_revenues = dataset['revenue']
    movie_popularities = dataset['popularity']
    movie_runtime = dataset["runtime"]
       
    
    return [(title, genre, budget, cast, director, overview, languages, release_date, revenue, popularity,tagline,keywords,runtime) 
            for title, genre, budget, cast, director, overview, languages, release_date, revenue, popularity, tagline, keywords,runtime 
            in zip(movie_titles, movie_genres, movie_budgets, movie_cast, movie_directors, movie_overviews, 
                   movie_languages, movie_release_dates, movie_revenues, movie_popularities, movie_tagline, movie_keywords,movie_runtime)]

#-----------------------------------------------------------------------------------------------------------


def preprocess_data(movies):
    selected_features = ['genres', 'keywords', 'tagline', 'cast', 'director']
    for feature in selected_features:
        movies[feature] = movies[feature].fillna('')
    combined_features = movies['genres'] + ' ' + movies['keywords'] + ' ' + movies['tagline'] + ' ' + movies['cast'] + ' ' + movies['director']
    return combined_features

def get_similarity_matrix(combined_features):
    vectorizer = TfidfVectorizer()
    feature_vector = vectorizer.fit_transform(combined_features)
    similarity_matrix = cosine_similarity(feature_vector)
    return similarity_matrix

def get_recommendations(movie_name, movies, similarity_matrix):
  """
  Recommends movies similar to the given movie.

  Args:
    movie_name (str): The name of the movie for which recommendations are sought.
    movies (DataFrame): The movie dataset.
    similarity_matrix (ndarray): The similarity matrix.

  Returns:
    list: A list of recommended movie titles.
  """

  list_of_all_titles = movies['title'].tolist()
  close_match_list = get_close_matches(movie_name, list_of_all_titles)

  if not close_match_list:
    return "Sorry, no close match found for the given movie name."

  closest_match = close_match_list[0]
  input_movie_index = movies[movies['title'] == closest_match].index[0]

  similarity_score = list(enumerate(similarity_matrix[input_movie_index]))
  sorted_similar_movie_list = sorted(similarity_score, key=lambda x: x[1], reverse=True)

  recommended_list = []
  for i, movie in enumerate(sorted_similar_movie_list):
    index = movie[0]
    title_from_index = movies.iloc[index]['title']
    if i < 10:  # Recommend only the top 10 similar movies
      recommended_list.append(f"{i+1}. {title_from_index}")

  return recommended_list

# Preprocess data
combined_features = preprocess_data(movies)
# Calculate similarity matrix
similarity_matrix = get_similarity_matrix(combined_features)

#-----------------------------------------------------------------------------------------------------------


# intents = {
#     'greetings': ['Hey','Hi','Good Morning'],
#     'movie_info': ['movie', 'film', 'about','plot','story'],
#     'genre_info': ['genre', 'type', 'category'],
#     'cast_info': ['cast', 'actors', 'actresses','lead role','hero','heroine','lead actor','lead actress','acted'],
#     'director_info': ['director', 'filmmaker', 'producer','directed','produced'],
#     'release_date_info': ['release date', 'when', 'premiere','released'],
#     'revenue_info': ['revenue', 'box office', 'earnings','collection'],
#     'runtime_info': ['duration', 'length', 'runtime','long'],
#     'rating_info': ['rating', 'score', 'imdb'],
#     'recommendations': ['recommend', 'suggest', 'watch','like', 'similar to'],
#     }

# responses = {
#     'greetings': "Your servant at your service. Let me know how can I help you ?",
#     'movie_info': "Here's some information about the movie '{movie_title}': {overview}",
#     'genre_info': "The genre of '{movie_title}' is {genre}.",
#     'cast_info': "The main cast of '{movie_title}' includes: {cast}",
#     'director_info': "The director of '{movie_title}' is {director}.",
#     'release_date_info': "The movie '{movie_title}' was released on {release_date}.",
#     'revenue_info': "The movie '{movie_title}' earned {revenue} at the box office.",
#     'runtime_info': "The runtime of '{movie_title}' is {runtime} minutes.",
#     'rating_info': "The average rating of '{movie_title}' is {rating}.",
#     'recommendations': "{recommendations}",
#     }



#-----------------------------------------------------------------------------------------------------------

# # Function to get information about a specific movie
# def get_movie_info(query):
#     movie_data = extract_info(movies) 
#     for movie_title, genre, budget, cast, director, overview, languages, release_date, revenue, popularity, tagline, keywords,runtime in movie_data:
#         if movie_title.lower() or movie_title in query:
#             return responses['movie_info'].format(movie_title=movie_title, 
#                                                   overview=overview,
#                                                   genre=genre,
#                                                   cast=cast,
#                                                   director=director,
#                                                   release_date=release_date,
#                                                   revenue=revenue,                                                  
#                                                   popularity=popularity,
#                                                   budget= budget,
#                                                   languages=languages,
#                                                   tagline=tagline,
#                                                   keywords = keywords)
#     return "Sorry, I couldn't find information about that movie."
# def get_genre_info(query):
#     movie_data = extract_info(movies) 
#     for movie_title, genre, budget, cast, director, overview, languages, release_date, revenue, popularity, tagline, keywords,runtime in movie_data:
#         if movie_title.lower() or movie_title in query:
#             return responses['genre_info'].format(movie_title=movie_title, 
#                                                   overview=overview,
#                                                   genre=genre,
#                                                   cast=cast,
#                                                   director=director,
#                                                   release_date=release_date,
#                                                   revenue=revenue,                                                  
#                                                   popularity=popularity,
#                                                   budget= budget,
#                                                   languages=languages,
#                                                   tagline=tagline,
#                                                   keywords = keywords)
#     return "Sorry, I couldn't find information about that movie."
# def get_cast_info(query):
#     movie_data = extract_info(movies)  # Call extract_info to get movie data
#     for movie_title, genre, budget, cast, director, overview, languages, release_date, revenue, popularity, tagline, keywords,runtime in movie_data:
#         if movie_title.lower() or movie_title in query:
#             return responses['cast_info'].format(movie_title=movie_title, 
#                                                   overview=overview,
#                                                   genre=genre,
#                                                   cast=cast,
#                                                   director=director,
#                                                   release_date=release_date,
#                                                   revenue=revenue,                                                  
#                                                   popularity=popularity,
#                                                   budget= budget,
#                                                   languages=languages,
#                                                   tagline=tagline,
#                                                   keywords = keywords)
#     return "Sorry, I couldn't find information about that movie."
# def get_director_info(query):
#     movie_data = extract_info(movies)  # Call extract_info to get movie data
#     for movie_title, genre, budget, cast, director, overview, languages, release_date, revenue, popularity, tagline, keywords,runtime in movie_data:
#         if movie_title.lower() or movie_title in query:
#             return responses['director_info'].format(movie_title=movie_title, 
#                                                   overview=overview,
#                                                   genre=genre,
#                                                   cast=cast,
#                                                   director=director,
#                                                   release_date=release_date,
#                                                   revenue=revenue,                                                  
#                                                   popularity=popularity,
#                                                   budget= budget,
#                                                   languages=languages,
#                                                   tagline=tagline,
#                                                   keywords = keywords)
#     return "Sorry, I couldn't find information about that movie."
# def get_release_date_info(query):
#     movie_data = extract_info(movies)  # Call extract_info to get movie data
#     for movie_title, genre, budget, cast, director, overview, languages, release_date, revenue, popularity, tagline, keywords,runtime in movie_data:
#         if movie_title.lower() or movie_title in query:
#             return responses['release_date_info'].format(movie_title=movie_title, 
#                                                   overview=overview,
#                                                   genre=genre,
#                                                   cast=cast,
#                                                   director=director,
#                                                   release_date=release_date,
#                                                   revenue=revenue,                                                  
#                                                   popularity=popularity,
#                                                   budget= budget,
#                                                   languages=languages,
#                                                   tagline=tagline,
#                                                   keywords = keywords)
#     return "Sorry, I couldn't find information about that movie."
# def get_revenue_info(query):
#     movie_data = extract_info(movies)  # Call extract_info to get movie data
#     for movie_title, genre, budget, cast, director, overview, languages, release_date, revenue, popularity, tagline, keywords,runtime in movie_data:
#         if movie_title.lower() or movie_title in query:
#             return responses['revenue_info'].format(movie_title=movie_title, 
#                                                   overview=overview,
#                                                   genre=genre,
#                                                   cast=cast,
#                                                   director=director,
#                                                   release_date=release_date,
#                                                   revenue=revenue,                                                  
#                                                   popularity=popularity,
#                                                   budget= budget,
#                                                   languages=languages,
#                                                   tagline=tagline,
#                                                   keywords = keywords)
#     return "Sorry, I couldn't find information about that movie."
# def get_runtime_info(query):
#     movie_data = extract_info(movies)  # Call extract_info to get movie data
#     for movie_title, genre, budget, cast, director, overview, languages, release_date, revenue, popularity, tagline, keywords, runtime in movie_data:
#         if movie_title.lower() or movie_title in query:
#             return responses['runtime_info'].format(movie_title=movie_title, 
#                                                   overview=overview,
#                                                   genre=genre,
#                                                   cast=cast,
#                                                   director=director,
#                                                   release_date=release_date,
#                                                   revenue=revenue,                                                  
#                                                   popularity=popularity,
#                                                   budget= budget,
#                                                   languages=languages,
#                                                   tagline=tagline,
#                                                   keywords = keywords,
#                                                   runtime = runtime)
#     return "Sorry, I couldn't find information about that movie."
# def get_rating_info(query):
#     movie_data = extract_info(movies)  # Call extract_info to get movie data
#     for movie_title, genre, budget, cast, director, overview, languages, release_date, revenue, popularity, tagline, keywords, runtime in movie_data:
#         if movie_title.lower() or movie_title in query:
#             return responses['rating_info'].format(movie_title=movie_title, 
#                                                   overview=overview,
#                                                   genre=genre,
#                                                   cast=cast,
#                                                   director=director,
#                                                   release_date=release_date,
#                                                   revenue=revenue,                                                  
#                                                   rating=popularity,
#                                                   budget= budget,
#                                                   languages=languages,
#                                                   tagline=tagline,
#                                                   keywords = keywords,
#                                                   runtime = runtime)
#     return "Sorry, I couldn't find information about that movie."

# def get_recommended_list(query, movies, similarity_matrix):
#     movie_data = extract_info(movies)  # Call extract_info to get movie data
#     for movie_title, genre, budget, cast, director, overview, languages, release_date, revenue, popularity, tagline, keywords, runtime in movie_data:
#         if movie_title.lower() in query.lower():
#             recommendations = get_recommendations(movie_title, movies, similarity_matrix)
#             if isinstance(recommendations, str):  # If get_recommendations returns an error message
#                 return recommendations
#             else:
#                 return recommendations
#     return "Sorry, I couldn't find information about that movie."




# def chat():
#     print("Movie Bot: Hi there! How can I help you?")
#     while True:
#         user_input = input("You: ")
        
#         if user_input.lower() == 'exit':
#             print("Movie Bot: Goodbye!")
#             break
#         response = handle_query(user_input.lower())
#         print("Movie Bot:", response)