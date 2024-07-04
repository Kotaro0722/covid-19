from flask import Blueprint

main = Blueprint('main', __name__)

login = Blueprint('login', __name__)

from . import routes
