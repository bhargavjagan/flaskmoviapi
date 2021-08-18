import sqlite3
import unittest
import os, json

import logging, datetime
from app.app_config import DATA_DIR, LOG_DIR

def exception_handler(func):
    def wrapper_func(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            logging.error(e)
            print(e)
    return wrapper_func
            
data_basedir = DATA_DIR
logs_dir = LOG_DIR
logging.basicConfig(filename= os.path.join(logs_dir,'load_data.log'), encoding='utf-8', level=logging.DEBUG)


class DB():
    conn = None
    movies_info = []
    genre_info = []
    movie_genre_info = []

    @exception_handler
    def make_connection(self,environment='dev'):
        env_sb_map = {'dev':'db_dev.db','test':'db_test.db'}
        path =   os.path.join(data_basedir,env_sb_map[environment])
        self.conn = sqlite3.connect(path)
        if self.conn:
            logging.info('Connecetion created.')
            print("Connection created : ",self.conn)

        return self.conn

    @exception_handler
    def split_data(self):
        logging.info('Started the function split data.')
        data = ""
        file_path = os.path.join(data_basedir, 'movies.json')
        with open(file_path,'r') as f_ptr:
            data = json.loads(f_ptr.read())
        
        for i in range(len(data)):
            self.movies_info.append({
                '99popularity': data[i]['99popularity'],
                'director': data[i]['director'],
                'imdb_score': data[i]['imdb_score'],
                'name': data[i]['name']
            })
        
    
            for j in data[i]['genre']:
                if j not in self.genre_info:
                    self.genre_info.append(j)
                self.movie_genre_info.append({
                    'genre':j,
                    'movie':data[i]['name']})
        logging.info('Conversion completed :{} : {} : {}'.format(len(self.movies_info),len(self.movie_genre_info), len(self.genre_info)))
        
    @exception_handler
    def insert(self):
        logging.info('Data load function started!')
        cur = self.conn.cursor()
        for i in self.genre_info:
            genre_stmt = """INSERT INTO genre ('name') VALUES(?);"""
            cur.execute(genre_stmt,(i,))
        self.conn.commit()

        for movie in self.movies_info:
            #movies_stmt = f"INSERT INTO movie ('popularity','director','name','created_on','imdb_score') VALUES (%f,%s,%s,%s,%f)" %( movie['99popularity'],str(movie['director']), movie['name'],str(datetime.datetime.utcnow()) ,movie['imdb_score'])
            movies_stmt = """INSERT INTO movie ('popularity','director','name','created_on','imdb_score') VALUES (?,?,?,?,?)"""
            cur.execute(movies_stmt,(movie['99popularity'],movie['director'], movie['name'],str(datetime.datetime.utcnow()) ,movie['imdb_score']))
        self.conn.commit()
        logging.info('Data for movie and genre completed.')

    @exception_handler
    def insert_movie_genre(self):
        cur = self.conn.cursor()
        """
        movies = cur.execute('select * from movie').fetchall()
        list_of_movies = [movie[4] for movie in movies]
        genres = cur.execute('select * from genre').fetchall()
        genre_list = [genre[1] for genre in genres]
        """
        moveigenre_stmt = "INSERT INTO moviegenre ('movie_name', 'genre_name') VALUES (?,?)"
        
        for record in self.movie_genre_info:
            #cur.execute(moveigenre_stmt, (movies[list_of_movies.index(record['movie'])][0],genres[genre_list.index(record['genre'])][0]))
            cur.execute(moveigenre_stmt, (record['movie'],record['genre']))
        self.conn.commit()
        logging.info('Data load to the table movie genre completed :'+str(len(self.movie_genre_info)))

    @exception_handler
    def drop_all(self):
        cur = self.conn.cursor()
        cur.execute('DROP TABLE IF EXISTS movie ')
        logging.debug('Dropped movie table.')
        cur.execute('DROP TABLE IF EXISTS genre')
        logging.debug('Dropped genre table.')
        cur.execute('DROP TABLE IF EXISTS moviegenre')
        logging.debug('Dropped moviegenre table.')
        self.conn.commit()

"""
if __name__ == "__main__":
    instance = TestDB()
    instance.split_data()
    logging.info('connection')
    con = instance.make_connection()
    instance.insert()
    instance.select()
    #instance.drop_all()
"""
