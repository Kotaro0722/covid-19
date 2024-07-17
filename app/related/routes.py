from flask import Flask,render_template ,request
from . import related
from . import related_table
from . import related_search_table
from . import admin_action

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

@related.route('/related')
def related():
    return render_template('related_search.html',
        title = "関係者リストページ"
    )

@related_table.route('/related_table')
def related_table():
    dbcon,cur = my_open( **dsn )
    #レコード新規挿入のSQL文
    sqlstring = f"""
        SELECT user_table.userID, user_num, user_name, suspension_school, c.body_temp, c.condition_date, v1.vaccination_num, v1.vaccination_date
        FROM	condition_details_table c
		        INNER JOIN(SELECT userID,
								MAX(condition_date) AS last_input_date
						    FROM condition_details_table
						    GROUP BY userID) s
					    ON c.userID = s.userID 
						    AND c.condition_date = DATE(s.last_input_date)
        INNER JOIN user_table
        ON c.userID = user_table.userID
        -- INNER JOIN condition_table
        -- ON c.condition_details_tableID = condition_table.condition_details_tableID
        LEFT JOIN suspension_table
        ON user_table.userID = suspension_table.userID
        LEFT JOIN vaccination_table v1
            INNER JOIN(
                SELECT userID, MAX(vaccination_date) AS last_vaccination_date
                FROM vaccination_table
                GROUP BY userID
            ) v2
            ON v1.userID = v2.userID AND v1.vaccination_date = v2.last_vaccination_date
        ON user_table.userID = v1.userID
        ORDER BY c.condition_date DESC, user_num
        ;
    """
    my_query(sqlstring,cur)
    recset = pd.DataFrame( cur.fetchall() )

    #型変換
    recset["suspension_school"].fillna("健康", inplace=True)
    recset["suspension_school"].replace(1, '感染者', inplace=True)
    recset["suspension_school"].replace(2, '濃厚接触者', inplace=True)

    return render_template( "admin_output.html",
        title = "関係者リストページ",
        table_data = recset
    )

@related_search_table.route('/related_search_table', methods=["POST"])
def related_search_table():
    dbcon,cur = my_open(**dsn)

    #receive form variable
    name_userNum = request.form["name_userNum"]

    #sql
    sqlstring = f"""
        SELECT user_table.userID, user_num, user_name, suspension_school, c.body_temp, c.condition_date, v1.vaccination_num, v1.vaccination_date
        FROM	condition_details_table c
		        INNER JOIN(SELECT userID,
								MAX(condition_date) AS last_input_date
						    FROM condition_details_table
						    GROUP BY userID) s
					    ON c.userID = s.userID 
						    AND c.condition_date = DATE(s.last_input_date)
        INNER JOIN user_table
        ON c.userID = user_table.userID
        LEFT JOIN suspension_table
        ON user_table.userID = suspension_table.userID
        LEFT JOIN vaccination_table v1
            INNER JOIN(
                SELECT userID, MAX(vaccination_date) AS last_vaccination_date
                FROM vaccination_table
                GROUP BY userID
            ) v2
            ON v1.userID = v2.userID AND v1.vaccination_date = v2.last_vaccination_date
        ON user_table.userID = v1.userID
        WHERE user_num = '{name_userNum}' OR user_name = '{name_userNum}'
        ORDER BY c.condition_date DESC, user_num
        ;
    """

    #run query
    my_query(sqlstring, cur)
    recset = pd.DataFrame(cur.fetchall())

    #close db
    my_close(dbcon, cur)

    return render_template(  "admin_output.html",
        title = f"{name_userNum}のレコード一覧",
        table_data = recset
    )

@admin_action.route("/admin_action",methods=["POST"])
def admin_action(): 
    #DBオープン    
    dbcon,cur = my_open( **dsn )
    #フォームから主キーの受け取り
    userID = request.form["userID"]
    
    #入力されたuserIDのactionIDを参照し，インナージョインで表示
    sql_string=f"""
        SELECT 
            action_table.action_tableID AS actionID,
            action_table.action_date_start AS action_date_start,
            action_table.action_date_end AS action_date_end,
            move_method_table.move_method AS move_method,
            crowd_table.place_type AS place_type,
            crowd_table.crowd_level AS crowd_level,
            action_table.lastupdate AS lastupdate
        FROM action_table
        INNER JOIN 
            move_method_table ON action_table.action_tableID = move_method_table.action_tableID
        INNER JOIN 
            crowd_table ON move_method_table.action_tableID = crowd_table.action_tableID  
        WHERE 
            action_table.userID = {userID};
    """
    my_query(sql_string,cur)
    #print(sql_string)
    recset=pd.DataFrame(cur.fetchall())

    
    # データベース接続を閉じる
    my_close( dbcon,cur )
    
    return render_template( "action_output.html",data=recset.to_dict(orient='records')
         
    )
    
    

    # #レコード新規挿入のSQL文
    # sqlstring = f"""
    #     SELECT user_num, user_name, suspension_school, condition_date, body_temp, symptomID as symptom, condition_table.delflag
    #     FROM condition_table
    #     INNER JOIN user_table
    #     ON condition_table.user_tableID = user_table.user_tableID
    #     INNER JOIN suspension_table
    #     ON user_table.suspensionID = suspension_table.suspensionID
    #     WHERE user_num = '{user_num}'
    #     ;
    # """
    # my_query(sqlstring,cur)
    # recset_c = pd.DataFrame( cur.fetchall() )
    # print(recset_c)
    # #DataFrame形式(2次元)をSeries形式(1次元ベクトルデータ)に変換する
    # rowdata_c = pd.Series( recset_c.iloc[0] )

    # #レコード新規挿入のSQL文
    # sqlstring = f"""
    #     SELECT action_table.user_num, user_name, suspension_school, action_number, action_date_time, movement_method, place, companion, companion_person, _mask, action_table.delflag
    #     FROM place_table
    #     INNER JOIN action_table
    #     ON place_table.placeID = action_table.place_of_departure
    #     INNER JOIN user_table
    #     ON action_table.user_num = user_table.user_num
    #     INNER JOIN suspension_table
    #     ON user_table.suspensionID = suspension_table.suspensionID
    #     WHERE action_table.user_num = '{user_num}'
    #     ;
    # """
    # my_query(sqlstring,cur)
    # recset_a = pd.DataFrame( cur.fetchall() )
    # #DataFrame形式(2次元)をSeries形式(1次元ベクトルデータ)に変換する
    # rowdata_a = pd.Series( recset_a.iloc[0] )

    # #DBクローズ
    # my_close( dbcon,cur )

    # print(rowdata_c)
    # print(rowdata_a)

    # return render_template("condition_action_table.html",
    #     title=f"個人番号={user_num} の体調管理表と行動記録表",
    #     table_data_c = rowdata_c,
    #     # table_data_a = rowdata_a
    # )