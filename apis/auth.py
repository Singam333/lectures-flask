from flask import request, Response
import json
import jwt
from os import environ
from passlib.hash import sha256_crypt

from . import apis
from models import db
from models.auth import User
from utils.validation import validate_email


@apis.route("/register", methods=["POST"])
def register():
    try:
        data = request.json
        email, password = data["email"], data["password"]

        if User.query.filter_by(email=email).count() > 0:
            return Response(
                json.dumps({"status": "error", "message": "Email already registered"}),
                mimetype="application/json",
            )

        if not validate_email(email):
            return Response(
                json.dumps({"status": "error", "message": "Email is invalid"}),
                mimetype="application/json",
            )

        user = User()
        user.email = email
        user.password = sha256_crypt.encrypt(str(password))

        db.session.add(user)
        db.session.commit()

        return Response(
            json.dumps({"status": "success", "message": "Succesfully registred"}),
            mimetype="application/json",
        )
    except Exception:
        return Response(
            json.dumps({"status": "error", "message": "Something went wrong"}),
            status=422,
            mimetype="application/json",
        )


@apis.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        email, password = data["email"], data["password"]

        users = User.query.filter_by(email=email)
        if users.count() == 0:
            return Response(
                json.dumps({"status": "error", "message": "Email is not registered"}),
                mimetype="application/json",
            )

        user = users.first()
        if not sha256_crypt.verify(password, user.password):
            return Response(
                json.dumps({"status": "error", "message": "Invalid password"}),
                mimetype="application/json",
            )

        jwt_secret = environ.get("JWT_SECRET")
        bytes_token = jwt.encode(
            {"email": user.email}, jwt_secret, algorithm="HS256"
        )
        return Response(
            json.dumps({"status": "success", "token": bytes_token.decode()}),
            mimetype="application/json",
        )
    except Exception:
        return Response(
            json.dumps({"status": "error", "message": "Something went wrong"}),
            status=422,
            mimetype="application/json",
        )
