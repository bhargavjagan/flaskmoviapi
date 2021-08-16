from flask_restx import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns

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
    version='1.0.1',
    description='Movie API is a web based REST API which can be used in various projects by web developers and even developers working on \
application development which needs to utilize any feature of IMDb website. This API will enable developers to get data according to their needs in an easy to read javascript object-notation (JSON) format.',
)
api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
