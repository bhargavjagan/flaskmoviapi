from flask_restx import Namespace, fields

"""
DTO : data transfer object - It is responsible for carrying data between processes.
"""


class UserDto:
    api = Namespace('user', description='User related operations.')
    user = api.model('user', {
        'email': fields.String(required=True, description='Email address of the user.'),
        'username': fields.String(required=True, description='Username of the user.'),
        'password': fields.String(required=True, description='Password of the user.'),
        'public_id': fields.String(description='User Identifier')
    })


class AuthDto:
    api = Namespace('auth', description='Authentication related operations.')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address.'),
        'password': fields.String(required=True, description='The user password.'),
    })

class MovieDto:
    api = Namespace('movie', description='Movies related operations.')
    movie = api.model('movie_details',{
        'name': fields.String(required=True, description="Name of the movie."),
        'popularity': fields.Float(description="99Rating of the movie."),
        'imdb_score': fields.Float(description="IMDB score of the movie."),
        'director': fields.String(description="Director of the movie."),
        'genre': fields.List(fields.String,description="Genres of the movie.")
    })

class GenreDto:
    api = Namespace('genre', description='Genre related operations.')
    genre = api.model('genre_details',{
        'genre_id': fields.Integer(required=True, description="ID of the genre."),
        'name': fields.String(required=True,description="Name of the genre.")
    })

class MovieGenreDto:
    api = Namespace('moviegenre',description='Movie Genere relation operations.')
    movie_genre = api.model('movie_genre_details',{
        'movie_genre_id': fields.Integer(required=True,decription="ID of the movie-genre."),
        'movie_id':fields.String(required=True,description='Foreign key of the movie.'),
        'genre_id':fields.String(required=True, description='Foreign key of the genre.')
    })
