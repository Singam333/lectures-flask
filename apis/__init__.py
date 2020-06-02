from flask import Blueprint

apis = Blueprint('apis', __name__)

from .auth import *
