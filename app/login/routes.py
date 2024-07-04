from flask import render_template
from . import login

@login.route('/')
def home():
    return render_template('index.html')
