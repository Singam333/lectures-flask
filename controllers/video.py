from flask import request
import jwt
from os import environ
from passlib.hash import sha256_crypt

import constants
from models import db
from models.video import Video
from utils.request import response
from utils.upload import upload_to_cloud, build_url
from utils.validation import validate_email


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

def list_videos():
    try:
        result = Video.query.filter_by(user_id=request.user_id).all()
        videos = [video.to_dict() for video in result]
        videos_with_urls = [{**video, "url": build_url(video["key"])} for video in videos]

        return response(status=constants.SUCCESS, message=constants.GET_LIST_SUCCESS, videos=videos_with_urls)
    except Exception:
        return response(
            status=constants.ERROR, message=constants.SOMETHING_WENT_WRONG, status_code=422
        )