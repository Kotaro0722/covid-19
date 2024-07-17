# app/action_input/__init__.py

from flask import Blueprint

close_contact = Blueprint("close_contact", __name__)

# Import routes
from . import routes
