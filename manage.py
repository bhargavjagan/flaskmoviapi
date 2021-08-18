import os 
import unittest
import logging,uuid,datetime

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
    logging.info('Application is running.')
    db.create_all()
    app.run()

@manager.command
def test():
    """Runs all the unit tests"""
    logging.info("TestRun")
    tests = unittest.TestLoader().discover('app/test','test_*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    logging.debug(result)
    if result.wasSuccessful():
        logging.info("Test was successfull.")
        return 0
    logging.info("Test was un-successfull.")
    return 1
    

from app.main.util.load_db import DB

@manager.command
def data_load():
    """Load the initial data"""
    logging.info('Data Load started.')
    db_instance = DB()
    db_instance.split_data()
    db_instance.make_connection()
    db_instance.insert()
    db_instance.insert_movie_genre()
    logging.info('Data load completed.')

@manager.command
def drop_data():
    """Drop the data of the movies table"""
    db_instance = DB()
    db_instance.make_connection()
    db_instance.drop_all()
    logging.info("Data is successfully dropped from the database.")

@manager.command
def create_super_admin():
    """Create a super admin for user management."""
    from app.main.model.user import User
    from app.main.service.user_service import generate_token
    try:
        admin_user = User(
            public_id=str(uuid.uuid4()),
            username=input("Name of the user :"),
            admin=True,
            email=input("Email Address :"), 
            password= input("Password :"),
            registered_on=datetime.datetime.utcnow()
            )
        db.session.add(admin_user)
        db.session.commit()
    except Exception as e:
        logging.error(e)
        print("Error creating the user. Check logs for more details.")
        return "User not created!"

    return generate_token(admin_user)[0]['Authorization']

if __name__ == "__main__":
    manager.run()