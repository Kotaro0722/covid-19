# app/action_input/__init__.py

from flask import Blueprint

related = Blueprint("related", __name__)
related_table = Blueprint("related_table", __name__)
related_search_table = Blueprint("related_search_table", __name__)
admin_condition = Blueprint("admin_condition", __name__)
admin_action = Blueprint("admin_action", __name__)

# Import routes
from . import routes
