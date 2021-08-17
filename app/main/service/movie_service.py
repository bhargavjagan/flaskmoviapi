import datetime

from app.main import db
from app.main.model.user import User
from app.main.model.movie import Movie, Genre, MovieGenre
import logging

def get_all_movies():
    """Get all the movies."""
    movies = Movie.query.all()
    #return [movie.name for movie in movies]
    return movies

def save_new_movie(data):
    """Create a new movie record"""
    logging.info(data)
    if data['name']:
        movie= Movie.query.filter_by(name=data['name']).first()
        if not movie:
            new_movie = Movie(
                popularity =data['popularity'],
                director=data['director'],
                imdb_score = data['imdb_score'],
                name=data['name']
            )
            save_changes(new_movie)
            logging.debug(new_movie)
            genre_list = [i.name for i in Genre.query.all()]
            for gen in data['genre']:
                mg = MovieGenre(movie_name=data['name'], genre_name=gen)
                logging.debug(mg)
                if gen not in genre_list:
                    g = Genre(name=gen)
                    logging.debug(g)
                    save_changes(g)
                    genre_list.append(gen)
                save_changes(mg)
            movie = Movie.query.filter_by(name=data['name']).first()
            logging.debug(movie) 
            return Movie.query.filter_by(name=data['name']).first()
        else:
            logging.debug('else')
            response_object = {
                'status': 'fail',
                'message': 'Movie already exists. Please use the /movies/<movie_name> for update.'
            }
            return response_object, 409
    else:
        logging.debug('No Data')
        response_object = {
            'status': 'fail',
            'message': 'Name field had no value.'
        }
        return response_object, 409
        

def find(movie_name):
    """Searchs the movie details by name"""
    if movie_name in [movie.name for movie in Movie.query.all()]:
        return Movie.query.filter_by(name = movie_name).first()
    else:
        return []  

def update_a_movie(movie_name,data):
    """updates the data of a movie """
    arg=list(data.keys())
    if movie_name in [movie.name for movie in Movie.query.all()]:
        movie = Movie.query.filter_by(name=movie_name).first()
        for i in arg:
            if i == 'popularity':
                movie.popularity = str(data['popularity'])
            elif i =='imdb_score':
                movie.imdb_score = data['imdb_score']
            elif i == 'director':
                movie.director = data['director']
        save_changes(movie)
        return movie
    else:
        return []

def delete_a_record(movie_name):
    """delete a movie by name."""
    movie = Movie.query.filter_by(name=movie_name).first()
    if movie:
        del_m = movie
        db.session.delete(movie)
        db.session.commit()
        return del_m
    else:
        return [],409


def get_latest_movie():
    """Get the rating of the movies by the movie_id"""
    return Movie.query.order_by('created_on').all()

def get_the_top_movies_by_rating():
    """Get the list of movies by rating"""
    return Movie.query.order_by('popularity').all()

def get_movie_by_genre(genre_name):
    """Get the movies by genre"""
    genre_list = [genre.name for genre in Genre.query.all()]
    if genre_name in genre_list:
        response_object = {
            'status': 'success',
            'movies': [i.movie_name for i in Genre.query.filter_by(name=genre_name).first().movie]
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'No such genre exists.'
        }
        return response_object, 409

def save_changes(data):
    """Save the changes to the db."""
    db.session.add(data)
    db.session.commit()
