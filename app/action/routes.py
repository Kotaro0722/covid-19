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
    place_of_departure = request.form["place_of_departure"]
    place_of_departure_other = request.form.get("place_of_departure_other", "")
    #waypoint1 = request.form["waypoint1"]
    waypoint1 = request.form["waypoint1"]
    if waypoint1 in ["1", "2", "3"]:
        waypoint1_value = int(waypoint1)
    elif waypoint1 == "other":
        waypoint1_value = None  # その他の場合、後で処理
    else:
        waypoint1_value = None  # 必要に応じてエラーハンドリング

    waypoint1_other = request.form.get("waypoint1_other")
    # 中継地点2の処理
    waypoint2 = request.form["waypoint2"]
    if waypoint2 in ["1", "2", "3"]:
        waypoint2_value = int(waypoint2)
    elif waypoint2 == "other":
        waypoint2_value = None  # その他の場合、後で処理
    else:
        waypoint2_value = None  # 必要に応じてエラーハンドリング

    waypoint2_other = request.form.get("waypoint2_other")

    # 中継地点3の処理
    waypoint3 = request.form["waypoint3"]
    if waypoint3 in ["1", "2", "3"]:
        waypoint3_value = int(waypoint3)
    elif waypoint3 == "other":
        waypoint3_value = None  # その他の場合、後で処理
    else:
        waypoint3_value = None  # 必要に応じてエラーハンドリング

    waypoint3_other = request.form.get("waypoint3_other")

    # 各中継地点の新しい場所をplace_tableに登録する
    for index, (waypoint, waypoint_other) in enumerate([(waypoint1, waypoint1_other), (waypoint2, waypoint2_other), (waypoint3, waypoint3_other)], start=1):
        if waypoint == "other" and waypoint_other:
            # 既存の場所名と一致するかを確認する
            sql_check = f"SELECT placeID FROM place_table WHERE place = '{waypoint_other}'"
            cur.execute(sql_check)
            result = cur.fetchone()

            if result:
                waypoint_value = result[0]  # 既存の場所があればそのIDを使用する
            else:
                # 新しい場所を登録する
                sql_insert_place = f"""
                    INSERT INTO place_table (place, crowd_level, lastupdate)
                    VALUES ('{waypoint_other}', 3, NOW())
                """
                cur.execute(sql_insert_place)
                dbcon.commit()
                waypoint_value = cur.lastrowid  # 新しく挿入された場所のIDを取得する

            # 中継地点の値を更新
            locals()[f"waypoint{index}_value"] = waypoint_value

    action_date_time = request.form.get("date_time")  # 必要に応じて他のフォームデータを取得する

    dt_now = datetime.datetime.now()

    sqlstring = f"""
        INSERT INTO action_table (waypoint1, waypoint2, waypoint3, action_date_time, lastupdate)
        VALUES ({waypoint1_value}, {waypoint2_value}, {waypoint3_value}, '{action_date_time}', '{dt_now}')
    """


    

    waypoint1_crowd = request.form["waypoint1_crowd"]
    waypoint1_other = request.form.get("waypoint1_other", "")
    waypoint2 = request.form["waypoint2"]
    waypoint2_crowd = request.form["waypoint2_crowd"]
    waypoint2_other = request.form.get("waypoint2_other", "")
    waypoint3 = request.form["waypoint3"]
    waypoint3_crowd = request.form["waypoint3_crowd"]
    waypoint3_other = request.form.get("waypoint3_other", "")
    place_of_arrival = request.form["place_of_arrival"]
    place_of_arrival_other = request.form.get("place_of_arrival_other", "")
    arrival_crowd = request.form["arrival_crowd"]
    companion = True if request.form.get("companion") == "yes" else False
    companion_person = request.form["companion_person"]
    mask = True if request.form.get("mask") == "yes" else False
    dt_now = datetime.datetime.now()

    sqlstring = f"""
        INSERT INTO action_table
        (action_date_time, movement_method, place_of_departure, place_of_departure_other, 
         waypoint1, waypoint1_crowd, waypoint1_other, waypoint2, waypoint2_crowd, waypoint2_other, 
         waypoint3, waypoint3_crowd, waypoint3_other, place_of_arrival, place_of_arrival_other, arrival_crowd, 
         companion, companion_person, mask, lastupdate)
        VALUES
        ('{action_date_time}', '{movement_method}', '{place_of_departure}', '{place_of_departure_other}', 
         '{waypoint1}', '{waypoint1_crowd}', '{waypoint1_other}', '{waypoint2}', '{waypoint2_crowd}', '{waypoint2_other}', 
         '{waypoint3}', '{waypoint3_crowd}', '{waypoint3_other}', '{place_of_arrival}', '{place_of_arrival_other}', '{arrival_crowd}', 
         {companion}, '{companion_person}', {mask}, '{dt_now}')
    """

    my_query(sqlstring,cur)
    dbcon.commit()
    my_close( dbcon,cur )
    
    return render_template("action_output.html")

#if __name__ == "__main__":
#    app.run(host="localhost", port=5000, debug=True)
    
#プログラム起動
