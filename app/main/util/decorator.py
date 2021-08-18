from functools import wraps

from flask import request

from app.main.service.auth_helper import Auth

import logging

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        logging.debug(request)
        data, status = Auth.get_logged_in_user(request)
        logging.debug(data)
        logging.debug(status)
        token = data.get('data')
        logging.debug(token)

        if not token:
            return data, status

        return f(*args, **kwargs)

    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        logging.debug(request)
        data, status = Auth.get_logged_in_user(request)
        logging.debug(data)
        logging.debug(status)
        token = data.get('data')
        logging.debug(token)

        if not token:
            return data, status

        admin = token.get('admin')
        if not admin:
            response_object = {
                'status': 'fail',
                'message': 'admin token required'
            }
            return response_object, 401

        return f(*args, **kwargs)

    return decorated
