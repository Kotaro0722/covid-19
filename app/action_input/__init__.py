# app/action_input/__init__.py

from flask import Blueprint

action_input_bp = Blueprint('action_input', __name__)

# Import routes
from app.action_input import routes
