import os 
import unittest

from flask_migrate import Migrate
from flask_script import Manager

from app import blueprint
from app.main import create_app, db
from app.main.model import user, movie

app = create_app(os.getenv('FLASK_APP_ENV') or 'dev')
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

#manager.add_command('db', MigrateCommand)

@manager.command
def run():
    """Run the flask application."""
    db.create_all()
    app.run()

@manager.command
def test():
    """Runs all the unit tests"""
    tests = unittest.TestLoader().discover('app/test','test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == "__main__":
    manager.run()