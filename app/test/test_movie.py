import unittest
import datetime,logging,json,uuid
import requests as req
import json

from flask import session
from app.main import db
from app.main.model.movie import Movie, Genre, MovieGenre
from app.test.base import BaseTestCase



def register_user(self):
    logging.info('register_user')
    
    return self.client.post(
        '/api/v1/user/',
        data=json.dumps(dict(
            email='user2@gmail.com',
            username='user2',
            password='Pass123456'
        )),
        content_type='application/json'
    )


def login_user(self):
    return self.client.post(
        '/api/v1/auth/login',
        data=json.dumps(dict(
            email='user2@gmail.com',
            password='Pass123456'
        )),
        content_type='application/json'
    )

def create_super_admin(self):
    """Create a super admin for user management."""
    from app.main.model.user import User
    from app.main.service.user_service import generate_token
    try:
        admin_user = User(
            public_id=str(uuid.uuid4()),
            username='admin',
            admin=True,
            email='admin', 
            password= "admin",
            registered_on=datetime.datetime.utcnow()
            )
        db.session.add(admin_user)
        db.session.commit()
    except Exception as e:
        logging.error(e)
        return "User not created!"

    return generate_token(admin_user)

class TestMovie(BaseTestCase):
    user_token = ""
    admin_token = ""

    url_base = "http://localhost:5000/api/v1"
    
    def test_create_a_super_admin(self):
        """Testing the creation of a super admin"""
        response, status = create_super_admin(self)
        self.assertTrue(response['status'] == 'success')
        self.assertTrue(response['message'] == 'Successfully registered.')
        self.assertTrue(response['Authorization'])
        self.assertEqual(status, 201)
        self.admin_token = response['Authorization']
        

    def test_create_a_user(self):
        """Testing the creation of a user"""
        with self.client:
            response = register_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)
            self.user_token = data['Authorization']
            

    def test_create_movie_without_usertoken(self):
        """Create a movie record without a normal user token."""
        response = self.client.post(
                    '/api/v1/movies',
                    data = json.dumps(dict(
                    name= "test_movie",
                    popularity= 80.2,
                    imdb_score= 86.9,
                    director="director1",
                    genre= [
                        "Adventure"
                        ]
                    )),
                    content_type='application/json'
                )
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code,401)
        
        for i in data['movies'].keys():
            self.assertIsNone(data['movies'][i])
         
    def test_create_movies_with_user_token(self):
        """Create a movie record with a user token"""
        with self.client:
            user_response = register_user(self)
            user_data = json.loads(user_response.data.decode())
            token = user_data['Authorization']
            logging.debug(token)

            response = self.client.post(
                    '/api/v1/movies',
                    data = json.dumps(dict(
                    name= "test_movie",
                    popularity= 80.2,
                    imdb_score= 86.9,
                    director="director1",
                    genre= [
                        "Adventure"
                        ]
                    )),
                    content_type='application/json',
                    headers = {'Authentication':'Bearer '+token}
                )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code,401)
            for i in data['movies'].keys():
                self.assertIsNone(data['movies'][i])
    
    def test_create_movie_with_admin_token(self):
        """Create a movie record with an admin token."""
        with self.client:
            user,status = create_super_admin(self)
            
            token = user['Authorization']
            header = {
                'Authorization':'Bearer '+token,
                'Content-Type': 'application/json'
            }
            payload = json.dumps({
                "name": "new_movie",
                "popularity": 8.90,
                "imdb_score": 90.7,
                "director": "director",
                "genre": [
                    "genre1"
                ]
                })

            response = self.client.post(
                '/api/v1/movies',
                data = payload,
                content_type='application/json',
                headers = header
            )
            
            data = json.loads(response.data.decode('utf-8'))
            
            self.assert200(response)
            self.assertEqual(data['movies']['name'],"new_movie")
            self.assertEqual(data['movies']['popularity'],8.90)
            self.assertEqual(data['movies']['imdb_score'],90.7)
            self.assertEqual(data['movies']['director'],"director")
            self.assertEqual(data['movies']['genre'],['genre1'])
    
    def test_get_all_the_movies_without_token(self):
        """Get all the movies in the database with out user token."""
        response = self.client.get('/api/v1/movies')
        data = json.loads(response.data.decode())
        
        self.assertEqual(data['status'],'fail')
        self.assertEqual(data['message'],"Provide a valid auth token.")


    def test_get_all_the_movies_with_user_token(self):
        """Get all the movies in the database with user token"""
        with self.client:
            user = register_user(self)
            user_data = json.loads(user.data.decode('utf-8'))
            token = user_data['Authorization']
                        
            headers = {
                    'Authorization': 'Bearer '+token,
                    'Content-Type': 'application/json'
                    }
            payload = json.dumps({
                    "name": "string",
                    "popularity": 0,
                    "imdb_score": 0,
                    "director": "string",
                    "genre": [
                        "string"
                    ]
                    })

            response = self.client.get(
                self.url_base+'/movies',
                headers=headers, 
                data=payload,
                content_type='application/json'
                )
            res= json.loads(response.data.decode('utf-8'))
            self.assertIsInstance(res,dict)
            self.assert200(response)
            self.assertIsNotNone(res)
            
    def test_get_all_the_latest_movies_with_user_token(self):
        """Get all the latest movies in the database with user token"""
        with self.client:
            admin,status = create_super_admin(self)
            user=register_user(self)
            user_data = json.loads(user.data.decode('utf-8'))
            
            admin_token = admin['Authorization']
            token = user_data['Authorization']
            header = {
                'Authorization':'Bearer '+admin_token,
                'Content-Type': 'application/json'
            }
            payload = json.dumps({
                "name": "new_movie",
                "popularity": 8.90,
                "imdb_score": 90.7,
                "director": "director",
                "genre": [
                    "genre1"
                ]
                })

            response = self.client.post(
                '/api/v1/movies',
                data = payload,
                content_type='application/json',
                headers = header
            )
            
            data = json.loads(response.data.decode('utf-8'))
            
            self.assert200(response)
            self.assertEqual(data['movies']['name'],"new_movie")
            self.assertEqual(data['movies']['popularity'],8.90)
            self.assertEqual(data['movies']['imdb_score'],90.7)
            self.assertEqual(data['movies']['director'],"director")
            self.assertEqual(data['movies']['genre'],['genre1'])
            
            payload = {}

            del_header = {
                'Authorization':'Bearer '+token
            }
            
            del_response = self.client.get(
                '/api/v1/movies/latest',
                data=payload,
                headers = del_header
            )
            
            data = json.loads(del_response.data.decode('utf-8'))
            
            self.assert200(response)
            self.assertIsInstance(data['movies'],list)
            self.assertIsNotNone(data['movies'][0]['name'])
            self.assertIsNotNone(data['movies'][0]['popularity'])
            self.assertIsNotNone(data['movies'][0]['imdb_score'])
            self.assertIsNotNone(data['movies'][0]['director'])
            self.assertIsNotNone(data['movies'][0]['genre'])

    def test_get_all_the_popular_movies_with_user_token(self):
        """Get all the latest movies in the database with user token"""
        with self.client:
            admin,status = create_super_admin(self)
            user=register_user(self)
            user_data = json.loads(user.data.decode('utf-8'))
            
            admin_token = admin['Authorization']
            token = user_data['Authorization']
            header = {
                'Authorization':'Bearer '+admin_token,
                'Content-Type': 'application/json'
            }
            payload = json.dumps({
                "name": "new_movie",
                "popularity": 8.90,
                "imdb_score": 90.7,
                "director": "director",
                "genre": [
                    "genre1"
                ]
                })

            response = self.client.post(
                '/api/v1/movies',
                data = payload,
                content_type='application/json',
                headers = header
            )
            
            data = json.loads(response.data.decode('utf-8'))
            
            self.assert200(response)
            self.assertEqual(data['movies']['name'],"new_movie")
            self.assertEqual(data['movies']['popularity'],8.90)
            self.assertEqual(data['movies']['imdb_score'],90.7)
            self.assertEqual(data['movies']['director'],"director")
            self.assertEqual(data['movies']['genre'],['genre1'])
            
            payload = {}

            del_header = {
                'Authorization':'Bearer '+token
            }
            
            del_response = self.client.get(
                '/api/v1/movies/latest',
                data=payload,
                headers = del_header
            )
            data = json.loads(del_response.data.decode('utf-8'))
            
            self.assert200(response)
            self.assertIsInstance(data['movies'],list)
            self.assertIsNotNone(data['movies'][0]['name'])
            self.assertIsNotNone(data['movies'][0]['popularity'])
            self.assertIsNotNone(data['movies'][0]['imdb_score'])
            self.assertIsNotNone(data['movies'][0]['director'])
            self.assertIsNotNone(data['movies'][0]['genre'])


    def test_delete_a_movie_with_admin_token(self):
        """Delete a movie with the admin token"""
        with self.client:
            user,status = create_super_admin(self)
            
            token = user['Authorization']
            header = {
                'Authorization':'Bearer '+token,
                'Content-Type': 'application/json'
            }
            payload = json.dumps({
                "name": "new_movie",
                "popularity": 8.90,
                "imdb_score": 90.7,
                "director": "director",
                "genre": [
                    "genre1"
                ]
                })

            response = self.client.post(
                '/api/v1/movies',
                data = payload,
                content_type='application/json',
                headers = header
            )
            
            data = json.loads(response.data.decode('utf-8'))
            
            self.assert200(response)
            self.assertEqual(data['movies']['name'],"new_movie")
            self.assertEqual(data['movies']['popularity'],8.90)
            self.assertEqual(data['movies']['imdb_score'],90.7)
            self.assertEqual(data['movies']['director'],"director")
            self.assertEqual(data['movies']['genre'],['genre1'])

            payload = {}
            
            del_response = self.client.delete(
                '/api/v1/movies/'+ data['movies']['name'],
                data=payload,
                headers = header
            )

            data = json.loads(del_response.data.decode('utf-8'))
            self.assert200(response)
            self.assertEqual(data['name'],"new_movie")
            self.assertEqual(data['popularity'],8.90)
            self.assertEqual(data['imdb_score'],90.7)
            self.assertEqual(data['director'],"director")
            self.assertEqual(data['genre'],['genre1'])

        
    def test_delete_a_movie_with_user_token(self):
        """Delete a movie with the user token"""
        with self.client:
            admin,status = create_super_admin(self)
            user=register_user(self)
            user_data = json.loads(user.data.decode('utf-8'))
            
            admin_token = admin['Authorization']
            token = user_data['Authorization']
            header = {
                'Authorization':'Bearer '+admin_token,
                'Content-Type': 'application/json'
            }
            payload = json.dumps({
                "name": "new_movie",
                "popularity": 8.90,
                "imdb_score": 90.7,
                "director": "director",
                "genre": [
                    "genre1"
                ]
                })

            response = self.client.post(
                '/api/v1/movies',
                data = payload,
                content_type='application/json',
                headers = header
            )
            
            data = json.loads(response.data.decode('utf-8'))
            
            self.assert200(response)
            self.assertEqual(data['movies']['name'],"new_movie")
            self.assertEqual(data['movies']['popularity'],8.90)
            self.assertEqual(data['movies']['imdb_score'],90.7)
            self.assertEqual(data['movies']['director'],"director")
            self.assertEqual(data['movies']['genre'],['genre1'])
            
            payload = {}

            del_header = {
                'Authorization':'Bearer '+token,
                'Content-Type': 'application/json'
            }
            
            del_response = self.client.delete(
                '/api/v1/movies/'+ data['movies']['name'],
                data=payload,
                headers = del_header
            )
            data = json.loads(del_response.data.decode('utf-8'))
            
            self.assert200(response)
            self.assertIsNone(data['name'])
            self.assertIsNone(data['popularity'])
            self.assertIsNone(data['imdb_score'])
            self.assertIsNone(data['director'])
            self.assertIsNone(data['genre'])
