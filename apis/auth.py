from flask import request, Response
import json
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
