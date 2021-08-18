import uuid
import datetime

from app.main import db
from app.main.model.user import User
from typing import Dict, Tuple
import logging

def save_new_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    """save the new user to the database"""
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow()
        )
        save_changes(new_user)
        logging.debug(data)
        return generate_token(new_user)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def get_all_users():
    """list of all the users"""
    return User.query.all()


def get_a_user(public_id):
    """get the user details with the public id"""
    return User.query.filter_by(public_id=public_id).first()


def generate_token(user: User) -> Tuple[Dict[str, str], int]:
    """generate the token for the user """
    try:
        auth_token = User.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401


def save_changes(data: User) -> None:
    """save the changes """
    db.session.add(data)
    db.session.commit()

