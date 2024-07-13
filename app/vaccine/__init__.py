from flask import Blueprint

vaccine=Blueprint("vaccine",__name__)

from . import routes