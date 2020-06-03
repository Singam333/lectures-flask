from . import routes
from controllers import video
from middleware.auth import validate_token


@routes.route("/upload", methods=["POST"])
@validate_token
def upload():
    return video.upload()


@routes.route("/videos", methods=["GET"])
@validate_token
def list_videos():
    return video.list_videos()
