from flask import Blueprint

routes = Blueprint('apis', __name__)

from .auth import *
from .video import *
