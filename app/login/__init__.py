from flask import Blueprint

login = Blueprint("login", __name__)
login_config=Blueprint("login-config",__name__)

from . import routes
