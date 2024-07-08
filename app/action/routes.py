from flask import render_template,request
from . import action
from . import action_config
#ex0402　フォームを使ってFlaskモジュールで，DBアクセス&フォームデータの受け渡し

from MyDatabase import my_open , my_query , my_close
import pandas as pd

#Data Source Nameのパラメータを辞書型変数で定義
dsn = {
    'host' : '172.30.0.10',  #ホスト名(IPアドレス)
    'port' : '3306',        #mysqlの接続ポート番号
    'user' : 'root',      #dbアクセスするためのユーザid
    'password' : '1234',    #ユーザidに対応するパスワード
    'database' : 'covid19' #オープンするデータベース名
}

from flask import Flask,render_template ,request
#Flaskのコンストラクタ
#app = Flask(__name__ ,static_folder="static")

#ルーティング定義
#ルーティング定義
@action.route("/action")
def action():
    return render_template( "top.html",
        title = "行動記録入力" 
    )
@action_config.route("/action_input", methods=["POST"])
def action_input():
    dbcon,cur = my_open( **dsn )
    
    action_date = request.form["date"]
    action_time = request.form["time"]
    movement_method = request.form["method"]
    place_of_departure = request.form["departure"]
    #place_of_transit = request.form["mid"]
    place_of_arrival = request.form["arrival"]
    companion = True if request.form.get("companion") == "yes" else False
    companion_person = request.form["companion_person"]
    mask = True if request.form.get("mask") == "yes" else False
    import datetime
    dt_now = datetime.datetime.now()
    
    sqlstring = f"""
        INSERT INTO action_table 
       (action_date, action_time, movement_method, place_of_departure, place_of_arrival, 
        companion, companion_person, mask, lastupdate)
        VALUES 
        ('{date}', '{time}', '{method}', '{departure}',  
        '{arrival}', {companion}, '{companion_person}', {mask}, '{dt_now}')
    """
    my_query(sqlstring,cur)
    dbcon.commit()
    my_close( dbcon,cur )
    
    return render_template("user_output.html")

#if __name__ == "__main__":
#    app.run(host="localhost", port=5000, debug=True)
    
#プログラム起動
