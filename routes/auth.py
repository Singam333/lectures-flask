from . import routes
from controllers import auth


@routes.route("/register", methods=["POST"])
def register():
    return auth.register()


@routes.route("/login", methods=["POST"])
def login():
    return auth.login()
