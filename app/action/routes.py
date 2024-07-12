from flask import render_template,request
from . import action
from . import action_config

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

#ルーティング定義
# ログインページ

@action.route("/action")
def action():
    return render_template( "action_input.html",
         
    )
@action_config.route("/action_input", methods=["POST"])
def action_input():
    dbcon,cur = my_open( **dsn )
    
    new_place=0
    userID = 3
    start_date_time = request.form["start_date_time"]
    end_date_time = request.form["end_date_time"]
    method = request.form["method"]
    place_of_departure1 = request.form["place_of_departure1"]
    place_of_departure2 = request.form["place_of_departure2"]
    departure_crowd = request.form["departure_crowd"]
    # フォームから同行者データを取得
    companion_data = []
    for key, value in request.form.items():
        if key.startswith("companion_person_"):
            companion_index = key.split("_")[-1]
            companion_name = value
            mask_option = request.form.get("mask_" + companion_index)  # マスクの有無を取得
            mask = mask_option == "yes"
            companion_data.append((companion_name, mask))
    # 出発地の処理
    if place_of_departure1 == "other":
        new_place = place_of_departure2
    if place_of_departure1 in ["1", "2", "3", "4", "5"]:  # 出発地が1から5の場合
        place_of_departure = place_of_departure1
        
    #更新日時取得
    import datetime
    dt_now = datetime.datetime.now()
    sqlstring = f"""
        INSERT INTO place_table
            (place,lastupdate)
            VALUES
            ('{new_place}','{dt_now}')
        ;
        """
    my_query(sqlstring,cur)
    dbcon.commit()
    sqlstring = f"""
        INSERT INTO action_table
            (userID,action_date_start,action_date_end,lastupdate)
            VALUES
            ({userID},'{start_date_time}','{end_date_time}','{dt_now}')
            ;
        """
    my_query(sqlstring,cur)
    dbcon.commit()
    #最後の挿入したaction_tableのactionIDを取得
    actionID = cur.lastrowid
    # 同行者名をcompanion_tableに挿入
    for companion_name, mask  in companion_data:
        sqlstring = f"""
            INSERT INTO companion_table
                (companion_name, action_tableID, _mask, lastupdate)
                VALUES
                ('{companion_name}',{actionID}, {mask}, '{dt_now}');
            """
    my_query(sqlstring, cur)
    dbcon.commit()
    
    return render_template("action_output.html",
                           title="レコード更新完了",
                           message="アクションと同行者を登録しました。")
    my_close( dbcon,cur )
    
    return render_template("action_output.html",
    title = "レコード更新完了",
    message = f"action_table テーブルにレコードを追加しました"
    )

#if __name__ == "__main__":
#    app.run(host="localhost", port=5000, debug=True)
    
#プログラム起動
