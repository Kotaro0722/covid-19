from flask import Blueprint

login = Blueprint("login", __name__)
login_config=Blueprint("login_config",__name__)

from . import routes
