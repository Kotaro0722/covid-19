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
    departure_crowd = int(request.form["departure_crowd"])  # 混み具合をint型に変換
    waypoint1 = request.form["waypoint1"]
    waypoint1_2 = request.form["waypoint1_2"]
    waypoint2 = request.form["waypoint2"]
    waypoint2_2 = request.form["waypoint2_2"]
    waypoint3 = request.form["waypoint3"]
    waypoint3_2 = request.form["waypoint3_2"]
    waypoint1_crowd = int(request.form.get("waypoint1_crowd", 0))  # 混み具合をint型に変換
    waypoint2_crowd = int(request.form.get("waypoint2_crowd", 0))  # 混み具合をint型に変換
    waypoint3_crowd = int(request.form.get("waypoint3_crowd", 0))  # 混み具合をint型に変換
    arrival_crowd = int(request.form["arrival_crowd"])  # 混み具合をint型に変換
    place_of_arrival1 = request.form["place_of_arrival1"]
    place_of_arrival2 = request.form["place_of_arrival2"]
    arrival_crowd = int(request.form["arrival_crowd"])  # 混み具合をint型に変換
    place_of_arrival1 = request.form["place_of_arrival1"]
    place_of_arrival2 = request.form["place_of_arrival2"]
    #更新日時取得
    import datetime
    dt_now = datetime.datetime.now()
    # フォームから同行者データを取得
    companion_data = []
    for key, value in request.form.items():
        if key.startswith("companion_person_"):
            companion_index = key.split("_")[-1]
            companion_name = value
            mask_option = request.form.get("mask_" + companion_index)  # マスクの有無を取得
            mask = mask_option == "yes"
            companion_data.append((companion_name, mask))
    
    #action_tableへの挿入
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
    #move_method_tableへの挿入
    sqlstring = f"""
        INSERT INTO move_method_table
            (action_tableID,move_method,lastupdate)
            VALUES
            ({actionID},'{method}','{dt_now}')
            ;
        """
    my_query(sqlstring,cur)
    dbcon.commit()
    # 出発地の処理
    if place_of_departure1 == "other":
        new_place = place_of_departure2
        place_of_departure = place_of_departure2
        #出発地のplace_tableへの挿入
        sqlstring = f"""
        INSERT INTO place_table
            (place,lastupdate)
            VALUES
            ('{new_place}','{dt_now}')
        ;
        """
    my_query(sqlstring,cur)
    dbcon.commit()

    # 最後に挿入したplace_tableのplace_tableIDを取得
    departureID = cur.lastrowid
    if place_of_departure1 in ["1", "2", "3", "4", "5"]:  # 出発地が1から5の場合
    
        departureID = place_of_departure1
        sqlstring = f"""
        SELECT place FROM place_table WHERE place_tableID = {departureID};
        """
    cur.execute(sqlstring)
    place_of_departure = cur.fetchone()#[0]
        
    #出発地のcrowd_tableの挿入
    departure_type = "出発地"
    sqlstring = f"""
    INSERT INTO crowd_table
        (action_tableID,place_tableID,crowd_level,place_type_tableID,lastupdate)
        VALUES
        ({actionID},{departureID},{departure_crowd},'{departure_type}','{dt_now}')
        ;
    """
    my_query(sqlstring,cur)
    dbcon.commit()
    
    #中継地1の処理
    if waypoint1 == "other":
        new_place = waypoint1_2
        waypoint1 = waypoint1_2
        #中継地1のplace_tableへの挿入
        sqlstring = f"""
        INSERT INTO place_table
            (place,lastupdate)
            VALUES
            ('{new_place}','{dt_now}')
        ;
        """
        my_query(sqlstring,cur)
        dbcon.commit()
         # 最後に挿入したplace_tableのplace_tableIDを取得
        waypoint1ID = cur.lastrowid

    if waypoint1 in ["1", "2", "3", "4", "5"]:  #中継地1が1から5の場合
        waypoint1ID = waypoint1
        sqlstring = f"""
        SELECT place FROM place_table WHERE place_tableID = {waypoint1ID};
        """
        cur.execute(sqlstring)
        waypoint1 = cur.fetchone()#[0]
    if waypoint1 == "no"  :
        waypoint1 = "なし" 
    
    waypoint1_type = "中継地1"
    #crowd_tableの出発地への挿入
    if waypoint1 == "other":
        sqlstring = f"""
        INSERT INTO crowd_table
            (action_tableID,place_tableID,crowd_level,place_type_tableID,lastupdate)
            VALUES
            ({actionID},{waypoint1ID},{waypoint1_crowd},'{waypoint1_type}','{dt_now}')
            ;
        """
        my_query(sqlstring,cur)
        dbcon.commit()
    if waypoint1 == 1 or waypoint1 == 2 or waypoint1 == 3 or waypoint1 == 4 or waypoint1 == 5:
        sqlstring = f"""
        INSERT INTO crowd_table
            (action_tableID,place_tableID,crowd_level,place_type_tableID,lastupdate)
            VALUES
            ({actionID},{waypoint1ID},{waypoint1_crowd},'{waypoint1_type}','{dt_now}')
            ;
        """
        my_query(sqlstring,cur)
        dbcon.commit()
    #変更点
    if waypoint1_crowd == 6:
        waypoint1_crowd = "なし"
    #中継地2の処理
    if waypoint2 == "other":
        new_place = waypoint2_2
        waypoint2 = waypoint2_2
        #中継地2のplace_tableへの挿入
        sqlstring = f"""
        INSERT INTO place_table
            (place,lastupdate)
            VALUES
            ('{new_place}','{dt_now}')
        ;
        """
        my_query(sqlstring,cur)
        dbcon.commit()
         # 最後に挿入したplace_tableのplace_tableIDを取得
        waypoint2ID = cur.lastrowid

    if waypoint2 in ["1", "2", "3", "4", "5"]:  #中継地2が1から5の場合
        waypoint2ID = waypoint2
        sqlstring = f"""
        SELECT place FROM place_table WHERE place_tableID = {waypoint2ID};
        """
        cur.execute(sqlstring)
        waypoint2 = cur.fetchone()#[0] 
    waypoint2_type = "中継地2"
    #crowd_tableの中継地2への挿入
    if waypoint1 == "other":
        sqlstring = f"""
        INSERT INTO crowd_table
            (action_tableID,place_tableID,crowd_level,place_type_tableID,lastupdate)
            VALUES
            ({actionID},{waypoint2ID},{waypoint2_crowd},'{waypoint2_type}','{dt_now}')
            ;
        """
        my_query(sqlstring,cur)
        dbcon.commit()
    if waypoint2 == 1 or waypoint2 == 2 or waypoint2 == 3 or waypoint2 == 4 or waypoint2 == 5:
        sqlstring = f"""
        INSERT INTO crowd_table
            (action_tableID,place_tableID,crowd_level,place_type_tableID,lastupdate)
            VALUES
            ({actionID},{waypoint2ID},{waypoint2_crowd},'{waypoint2_type}','{dt_now}')
            ;
        """
        my_query(sqlstring,cur)
        dbcon.commit()
    if waypoint2 == "no"  :
        waypoint2 = "なし" 
    if waypoint2_crowd == 6:
        waypoint2_crowd = "なし"
    #中継地3の処理
    if waypoint3 == "other":
        new_place = waypoint3_2
        waypoint3 = waypoint3_2
        #中継地2のplace_tableへの挿入
        sqlstring = f"""
        INSERT INTO place_table
            (place,lastupdate)
            VALUES
            ('{new_place}','{dt_now}')
        ;
        """
        my_query(sqlstring,cur)
        dbcon.commit()
         # 最後に挿入したplace_tableのplace_tableIDを取得
        waypoint3ID = cur.lastrowid

    if waypoint3 in ["1", "2", "3", "4", "5"]:  #中継地2が1から5の場合
        waypoint3ID = waypoint3
        sqlstring = f"""
        SELECT place FROM place_table WHERE place_tableID = {waypoint3ID};
        """
        cur.execute(sqlstring)
        waypoint3 = cur.fetchone()#[0] 
    if waypoint3 == "no"  :
        waypoint3 = "なし"
    waypoint3_type = "中継地3"
    #crowd_tableの中継地2への挿入
    if waypoint3 == "other":
        sqlstring = f"""
        INSERT INTO crowd_table
            (action_tableID,place_tableID,crowd_level,place_type_tableID,lastupdate)
            VALUES
            ({actionID},{waypoint3ID},{waypoint3_crowd},'{waypoint3_type}','{dt_now}')
            ;
        """
        my_query(sqlstring,cur)
        dbcon.commit()
    if waypoint3 == 1 or waypoint3 == 2 or waypoint3 == 3 or waypoint3 == 4 or waypoint3 == 5:
        sqlstring = f"""
        INSERT INTO crowd_table
            (action_tableID,place_tableID,crowd_level,place_type_tableID,lastupdate)
            VALUES
            ({actionID},{waypoint3ID},{waypoint3_crowd},'{waypoint3_type}','{dt_now}')
            ;
        """
        my_query(sqlstring,cur)
        dbcon.commit()
    if waypoint3_crowd == 6:
        waypoint3_crowd = "なし"
    # 到着地の処理
    if place_of_arrival1 == "other":
        new_place = place_of_arrival2
        place_of_arrival = place_of_arrival2
        #出発地のplace_tableへの挿入
        sqlstring = f"""
        INSERT INTO place_table
            (place,lastupdate)
            VALUES
            ('{new_place}','{dt_now}')
        ;
        """
        my_query(sqlstring,cur)
        dbcon.commit()
        # 最後に挿入したplace_tableのplace_tableIDを取得
        arrival1ID = cur.lastrowid
        
    if place_of_arrival1 in ["1", "2", "3", "4", "5"]:  # 出発地が1から5の場合
        arrival1ID = place_of_arrival1
        sqlstring = f"""
        SELECT place FROM place_table WHERE place_tableID = {arrival1ID};
        """
        cur.execute(sqlstring)
        place_of_arrival = cur.fetchone()#[0] 
  
    #到着地のcrowd_tableの挿入
    arrival_type = "到着地"
    sqlstring = f"""
        INSERT INTO crowd_table
            (action_tableID,place_tableID,crowd_level,place_type_tableID,lastupdate)
            VALUES
            ({actionID},{arrival1ID},{arrival_crowd},'{arrival_type}','{dt_now}')
            ;
        """
    my_query(sqlstring,cur)
    dbcon.commit()
    '''
    #出発地を文字列に変換
    sqlstring = f"""
    SELECT place FROM place_table WHERE placeID = {departureID};
    """
    cur.execute(sqlstring)
    place_of_departure = cur.fetchone()[0]
   
    #中継地1を文字列に変換
    if waypoint1 in ["1", "2", "3", "4", "5"]:
        sqlstring = f"""
        SELECT place FROM place_table WHERE placeID = {waypoint1ID};
        """
        cur.execute(sqlstring)
        waypoint1 = cur.fetchone()[0]

    #中継地2を文字列に変換
    if waypoint2 in ["1", "2", "3", "4", "5"]:    
        sqlstring = f"""
        SELECT place FROM place_table WHERE placeID = {waypoint2ID};
        """
        cur.execute(sqlstring)
        waypoint2 = cur.fetchone()[0]            

    #中継地3を文字列に変換
    if waypoint3 in ["1", "2", "3", "4", "5"]:     
        sqlstring = f"""
        SELECT place FROM place_table WHERE placeID = {waypoint3ID};
        """
        cur.execute(sqlstring)
        waypoint3 = cur.fetchone()[0]  

    #到着地を文字列に変換
    sqlstring = f"""
    SELECT place FROM place_table WHERE placeID = {arrivalID};
    """
    cur.execute(sqlstring)
    place_of_arrival = cur.fetchone()[0]   
    '''
    return render_template(
        "action_output.html",
        title="レコード更新完了",
        message="行動記録を登録しました。",
        start_date_time=start_date_time,
        end_date_time=end_date_time,
        method=method,
        place_of_departure=place_of_departure,
        departure_crowd=departure_crowd,
        waypoint1=waypoint1,
        waypoint1_crowd=waypoint1_crowd,
        waypoint2=waypoint2,
        waypoint2_crowd=waypoint2_crowd,
        waypoint3=waypoint3,
        waypoint3_crowd=waypoint3_crowd,
        place_of_arrival=place_of_arrival,
        arrival_crowd=arrival_crowd,
        companion_data=companion_data
        )
    my_close( dbcon,cur )  
   

    
#if __name__ == "__main__":
#    app.run(host="localhost", port=5000, debug=True)
    
#プログラム起動
