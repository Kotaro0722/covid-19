# app/action_input/__init__.py

from flask import Blueprint

infected = Blueprint("infected", __name__)

# Import routes
from . import routes
