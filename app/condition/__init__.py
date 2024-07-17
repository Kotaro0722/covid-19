from flask import Blueprint

condition = Blueprint('condition', __name__)
condition_output = Blueprint('condition_output', __name__)
condition_table = Blueprint('condition_table', __name__)

from . import routes

