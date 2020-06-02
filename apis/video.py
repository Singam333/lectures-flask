from flask import request
import jwt
from os import environ
from passlib.hash import sha256_crypt

from . import apis
import constants
from models import db
from models.video import Video
from middleware.auth import validate_token
from utils.request import response
from utils.upload import upload_to_cloud
from utils.validation import validate_email


@apis.route("/upload", methods=["POST"])
@validate_token
def upload():
    try:
        f = request.files["file"]

        key = upload_to_cloud(f)
        video = Video()
        video.key = key
        video.user_id = request.user_id
        video.filename = f.filename

        db.session.add(video)
        db.session.commit()

        return response(status=constants.SUCCESS, message=constants.UPLOAD_SUCCESS)
    except Exception:
        return response(
            status=constants.ERROR, message=constants.SOMETHING_WENT_WRONG, status_code=422
        )


@apis.route("/videos", methods=["GET"])
@validate_token
def list_videos():
    try:
        result = Video.query.filter_by(user_id=request.user_id).all()
        videos = [video.to_dict() for video in result]
        return response(
            status=constants.SUCCESS, message=constants.GET_LIST_SUCCESS, videos=videos
        )
    except Exception:
        return response(
            status=constants.ERROR, message=constants.SOMETHING_WENT_WRONG, status_code=422
        )
