from app.main import db
from datetime import datetime
from typing import List
import logging

class Movie(db.Model):
    """ Movies model stores the information of the movies. """
    __tablename__ ="movie"

    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    popularity = db.Column(db.Float, nullable=False)
    director = db.Column(db.String(500), nullable=True)
    imdb_score = db.Column(db.Float, nullable=False)
    name = db.Column(db.String(500), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)

    #one to many relationship with movie_genre
    genre = db.relationship('MovieGenre', backref="movie",lazy=True)

    def __init__(self,**kwargs):
        self.created_on = datetime.now()
        super(Movie, self).__init__(**kwargs)


    def __repr__(self):
        return '<Movie {}: {}>'.format(self.movie_id, self.name)

    def save_new_movie(data):
        """Insert the data of new movies into the database."""
        movie = Movie.query.filter_by(movie)

class Genre(db.Model):
    """ Genre model stores the types of genres of movies."""

    __tablename__ = "genre"

    genre_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(500), nullable=False, unique=True)

    #one to many relationship with movie_genre
    movie = db.relationship('MovieGenre', backref="genre",lazy=True)
    
    def __repr__(self):
        return '<Genre : {}>'.format(self.name)

class MovieGenre(db.Model):
    """ Movie Genre model stores the relation between the movie and the genres."""

    __tablename__ = "moviegenre"
    
    movie_genre_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_name = db.Column(db.String(500), db.ForeignKey('movie.name'))
    genre_name = db.Column(db.String(500), db.ForeignKey('genre.name'))

    def __repr__(self):
        return '{}'.format(self.genre_name)