from flask import Blueprint

condition = Blueprint('condition', __name__)

from . import routes

