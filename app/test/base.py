from flask_testing import TestCase

from app.main import db
from manage import app

class BaseTestCase(TestCase):
    """Base Tests"""

    def create_app(self):
        """ Create app """
        app.config.from_object('app.main.config.TestingConfig')
        return app

    def setUp(self):
        """ Setting up the app """
        db.create_all()
        db.session.commit()

    def tearDown(self):
        """ Before exiting the app """
        db.session.remove()
        db.drop_all()