from flask import render_template,request
from . import login
from . import login_config

@login.route("/login")
def login():
    return render_template("login.html")    


@login_config.route("/",methods=["POST"])
def login_config():
    username=request.form["username"]
    password=request.form["password"]
    
    is_admin=False
    is_user=False
    
    admin_list=[
        {"username":"admin","password":"admin1234"},
    ]    
    user_list=[
        {"username":"user1234","password":"pass1234"},
        {"username":"user5678","password":"pass5678"}, 
    ]
    
    for user in admin_list:
        if user["username"] == username and user["password"] == password:
            is_admin=True
    for user in user_list:
        if user["username"] == username and user["password"] == password:
            is_user=True
            
    
    if is_admin:
        return render_template("main_admin.html")
    elif is_user:
        return render_template("main_user.html")
    else:
        return render_template("login.html")
    
    
    
    
