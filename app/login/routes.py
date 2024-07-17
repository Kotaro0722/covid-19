from flask import render_template,request,redirect,url_for,session
from . import login
from ..MyDatabase import my_open , my_query , my_close

dsn = {
    'host' : '172.30.0.10',  #ホスト名(IPアドレス)
    'port' : '3306',        #mysqlの接続ポート番号
    'user' : 'root',      #dbアクセスするためのユーザid
    'password' : '1234',    #ユーザidに対応するパスワード
    'database' : 'covid19' #オープンするデータベース名
}

@login.route("/login")
def login_():
    return render_template("login.html")    

@login.route("/signup")
def signup():
    return render_template("signup.html")

@login.route("/signUp",methods=["POST"])
def signUp():
    user_num=request.form["user_num"]
    password=request.form["password"]
    username=request.form["username"]
    _class=request.form["class"]
    affiliation=request.form["affiliation"]
    tel=request.form["tel"]
    
    dbcon,cur=my_open(**dsn)
    
    sql_string=f"""
        INSERT INTO user_table
            (user_num,user_pw,_class,affiliation,tel,user_name)
        VALUES
            ('{user_num}','{password}','{_class}','{affiliation}','{tel}','{username}')
    """
    my_query(sql_string,cur)
    dbcon.commit()
    
    my_close(dbcon,cur)
    return render_template("result.html")

@login.route("/logout",methods=["POST"])
def logout():
    session.pop("username", None)
    return redirect(url_for("login.login_"))
