from flask import render_template,request
from . import condition
from ..MyDatabase import my_open , my_query , my_close

dsn = {
    'host' : '172.30.0.10',  #ホスト名(IPアドレス)
    'port' : '3306',        #mysqlの接続ポート番号
    'user' : 'root',      #dbアクセスするためのユーザid
    'password' : '1234',    #ユーザidに対応するパスワード
    'database' : 'covid-19' #オープンするデータベース名
}

@condition.route("/condition",methods=["GET","POST"])
def condition():
    return render_template("condition_input.html")  
    
