from flask_restx import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.movie_controller import api as movie_ns

blueprint = Blueprint('api', __name__)
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    blueprint,
    title='Movies API',
    version='1.1.0',
    description='Movie API is a web based REST API which can be used in various projects by web developers and even developers working on \
    application development which needs to utilize any feature of IMDb website. This API will enable developers to get data according to their needs in an easy to read javascript object-notation (JSON) format.',
    authorizations=authorizations,
    security='apikey'
)

api.add_namespace(user_ns, path='/api/v1/user')
api.add_namespace(movie_ns, path='/api/v1')
api.add_namespace(auth_ns, path='/api/v1/auth')
