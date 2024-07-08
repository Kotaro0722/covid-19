from flask import render_template,request
from . import action
from . import action_config
#ex0402　フォームを使ってFlaskモジュールで，DBアクセス&フォームデータの受け渡し

from ..MyDatabase import my_open , my_query , my_close
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
    return render_template( "action_input.html",
        title = "行動記録入力" 
    )
@action_config.route("/action_input", methods=["POST"])
def action_input():
    dbcon,cur = my_open( **dsn )
    
    action_date_time = request.form["date_time"]
    movement_method = request.form["method"]
    place_of_departure = request.form["departure"]
    place_of_arrival = request.form["arrival"]
    companion = True if request.form.get("companion") == "yes" else False
    companion_person = request.form["companion_person"]
    mask = True if request.form.get("mask") == "yes" else False
    import datetime
    dt_now = datetime.datetime.now()
    sqlstring = f"""
        UPDATE action_table
        SET action_date_time = '{action_date_time}',
            movement_method = '{movement_method}',
            place_of_departure = {place_of_departure},
            place_of_arrival = {place_of_arrival},
            companion = {companion},
            companion_person = '{companion_person}',
            _mask = {mask},
            lastupdate = '{dt_now}'
        WHERE action_tableID = {action_tableID}
    """
    '''
    sqlstring = f"""
        INSERT INTO action_table 
       (action_date_time, movement_method, place_of_departure, place_of_arrival, 
        companion, companion_person, _mask, lastupdate)
        VALUES 
        ('{action_date_time}', '{movement_method}', '{place_of_departure}',  
        '{place_of_arrival}', {companion}, '{companion_person}', {mask}, '{dt_now}');
        
        
        
    """
    '''
    #WHERE action_tableID = {action_tableID};
    #WHERE user_num = {user_num};
    my_query(sqlstring,cur)
    dbcon.commit()
    my_close( dbcon,cur )
    
    return render_template("action_output.html")

#if __name__ == "__main__":
#    app.run(host="localhost", port=5000, debug=True)
    
#プログラム起動
