from functools import wraps

from flask import request

from typing import Callable

def token_required(f) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):
        data, status = Auth.get