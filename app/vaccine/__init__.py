from flask import Blueprint

vaccine_input=Blueprint("vaccine",__name__)

from . import routes