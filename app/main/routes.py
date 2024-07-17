from flask import render_template,request,redirect,url_for,session
from . import main
from ..MyDatabase import my_open , my_query , my_close
import pandas as pd

dsn = {
    'host' : '172.30.0.10',  #ホスト名(IPアドレス)
    'port' : '3306',        #mysqlの接続ポート番号
    'user' : 'root',      #dbアクセスするためのユーザid
    'password' : '1234',    #ユーザidに対応するパスワード
    'database' : 'covid19' #オープンするデータベース名
}

@main.route("/",methods=["POST","GET"])
def login_config():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        
        is_admin=False
        is_user=False
        
        dbcon,cur=my_open(**dsn)
        
        admin_list=[
            {"username":"admin","password":"admin1234"},
        ]
        sql_string=f"""
            SELECT user_num,user_pw
            FROM user_table
            WHERE user_num='{username}' AND user_pw='{password}'
            ;
        """
        my_query(sql_string,cur)
        recset=pd.DataFrame(cur.fetchall())
        print(recset)
        
        
        for user in admin_list:
            if user["username"] == username and user["password"] == password:
                is_admin=True
        if not recset.empty:
            is_user=True
    
        if is_admin:
            dbcon,cur=my_open(**dsn)
            sqlstring_related=f"""
                SELECT * 
            """
            return render_template("main_admin.html")
        elif is_user:
            return render_template("main_user.html")
    else:
        return redirect(url_for("login.login_"))
@main.route("/main_user",methods=["POST","GET"])
def main_user():
    if "username" in session:
        dbcon,cur=my_open(**dsn)
        
        sql_string=f"""
            SELECT user_name FROM user_table
            WHERE user_num='{session["username"]}'
            ;
        """
        my_query(sql_string,cur)
        recset=pd.DataFrame(cur.fetchall())
        user_name=recset["user_name"][0]
        
        my_close(dbcon,cur)
        return render_template("main_user.html",userName=user_name)
    else:
        return redirect(url_for("login.login_"))
