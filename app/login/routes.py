from flask import render_template,request
from . import login

@login.route("/login")
def login():
    return render_template("login.html")    

    
    