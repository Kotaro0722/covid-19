from flask import render_template,request
from . import main_user
from . import main_admin

@main_user.route("/")
def main_user():
    return render_template("")

@main_admin.route("/admin")
def main_admin():
    return render_template("")