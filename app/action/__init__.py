# app/action_input/__init__.py

from flask import Blueprint

action = Blueprint("action", __name__)
action_config=Blueprint("action-config",__name__)
# Import routes
from . import routes
