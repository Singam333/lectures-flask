from datetime import datetime, timedelta
from flask import request
import jwt
from os import environ
from passlib.hash import sha256_crypt

from . import apis
import constants
from models import db
from models.auth import User
from utils.validation import validate_email
from utils.request import response


@apis.route("/register", methods=["POST"])
def register():
    try:
        data = request.json
        email, password = data["email"], data["password"]

        if User.query.filter_by(email=email).count() > 0:
            return response(status=constants.ERROR, message=constants.EMAIL_ALREADY_EXISTS)

        if not validate_email(email):
            return response(status=constants.ERROR, message=constants.INVALID_EMAIL)

        user = User()
        user.email = email
        user.password = sha256_crypt.encrypt(str(password))

        db.session.add(user)
        db.session.commit()

        return response(status=constants.SUCCESS, message=constants.REGISTRATION_SUCCESS)
    except Exception:
        return response(
            status=constants.ERROR, message=constants.SOMETHING_WENT_WRONG, status_code=422
        )


@apis.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        email, password = data["email"], data["password"]

        users = User.query.filter_by(email=email)
        if users.count() == 0:
            return response(status=constants.ERROR, message=constants.EMAIL_NOT_REGISTERED)

        user = users.first()
        if not sha256_crypt.verify(password, user.password):
            return response(status=constants.ERROR, message=constants.INVALID_PASSWORD)

        jwt_secret = environ.get("JWT_SECRET")
        bytes_token = jwt.encode(
            {"exp": datetime.utcnow() + timedelta(days=constants.EXPIRY_DAYS), "user_id": user.id},
            jwt_secret,
            algorithm="HS256",
        )

        return response(
            status=constants.SUCCESS, message=constants.LOGIN_SUCCESS, token=bytes_token.decode()
        )
    except Exception:
        return response(
            status=constants.ERROR, message=constants.SOMETHING_WENT_WRONG, status_code=422
        )
