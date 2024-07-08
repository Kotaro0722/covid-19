from flask import Blueprint

main_user=Blueprint("main_user",__name__)
main_admin=Blueprint("main_admin",__name__)

from . import routes