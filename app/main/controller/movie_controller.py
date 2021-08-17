from flask import request
from flask_restx import Resource,reqparse

from app.main.util.decorator import token_required, admin_token_required
from ..util.dto import MovieDto, GenreDto, MovieGenreDto
from ..service.movie_service import *
import logging

api = MovieDto.api
_movie = MovieDto.movie

@api.route('/movies/<movie_name>', endpoint='moviesByName')
class MovieByName(Resource):
    @api.doc('Details of the movie.')
    @api.marshal_list_with(_movie,envelope='movies')
    @token_required
    def get(self, movie_name):
        """Details of the movie"""
        return find(movie_name)

    @api.doc('Update the movie details.')
    @api.expect(_movie, validate=True)
    @api.marshal_list_with(_movie, envelope='movies')
    @admin_token_required
    def post(self,movie_name):
        """Update the movie details."""
        data = request.json
        return update_a_movie(movie_name,data=data)

    @api.doc('Delete a movie.')
    @api.marshal_with(_movie)
    @admin_token_required
    def delete(self, movie_name):
        """Delete a movie."""
        return delete_a_record(movie_name)



@api.route('/movies')
class MovieList(Resource):
    @api.doc('Details of all the movie.')
    @token_required
    @api.marshal_list_with(_movie,envelope='movies')
    def get(self):
        """Details of all the movie"""
        return get_all_movies()

    @api.doc("Create a movie record.")
    @api.expect(_movie, validate=True)
    @api.marshal_list_with(_movie,envelope='movies')
    @api.response(201, "Movie record successfully created.")
    @admin_token_required
    def post(self):
        """Create a movie record"""
        data = request.json
        return save_new_movie(data=data)
    
@api.route('/movies/latest')
class LatestMovieList(Resource):
    @api.doc('List of latest movies.')
    @token_required
    @api.marshal_list_with(_movie,envelope='movies')
    def get(self):
        """List of latest movies."""
        return get_latest_movie()

@api.route('/movies/rating')
class RatedMovieList(Resource):
    @api.doc('List of movies by rating.')
    @token_required
    @api.marshal_list_with(_movie,envelope='movies')
    def get(self):
        """List of movies by rating."""
        return get_the_top_movies_by_rating()

@api.route('/genre/<genre_name>',endpoint='genre')
class MovieGenres(Resource):
    @api.doc("List of movies by genre.")
    @token_required
    def get(self,genre_name):
        """List of movies by genre"""
        return get_movie_by_genre(genre_name)

        