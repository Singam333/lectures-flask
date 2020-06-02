from flask import request
from functools import wraps
from os import environ
import jwt

import constants
from utils.request import response


def validate_token(f):
    @wraps(f)
    def wrapped_function(*args, **kwargs):
        try:
            auth_header = request.headers["Authorization"]
            token = auth_header.split()[1]
            secret = environ.get("JWT_SECRET")
            decoded_jwt = jwt.decode(token, secret, algorithms=["HS256"])
            request.user_id = decoded_jwt["user_id"]
            return f(*args, **kwargs)
        except jwt.exceptions.DecodeError:
            return response(constants.ERROR, constants.INVALID_TOKEN, status_code=401)
        except Exception:
            return response(constants.ERROR, constants.TOKEN_VERIFICATION_FAILED, status_code=401)

    return wrapped_function
