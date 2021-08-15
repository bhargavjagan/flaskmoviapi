from flask_restful import Api
from flask import Blueprint

#Flask Blueprint
blueprint = Blueprint('api',__name__)

#configure the api 
api = Api(blueprint,
title='FLASK MOVIES API',
version='1.0',
authorization=authorizations,
security='apikey'
)

#Add resources
