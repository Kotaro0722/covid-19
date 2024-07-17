from flask import Flask,render_template ,request
from . import related
from . import related_table
from . import related_search_table
from . import condition_action

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
        SELECT user_num, user_name, suspension_school, c.body_temp, c.condition_date
        FROM	condition_table c
		        INNER JOIN(SELECT user_tableID,
								MAX(condition_date) AS last_input_date
						    FROM condition_table
						    GROUP BY user_tableID) s
					    ON c.user_tableID = s.user_tableID 
						    AND c.condition_date = DATE(s.last_input_date)
        INNER JOIN user_table
        ON c.user_tableID = user_table.user_tableID
        INNER JOIN suspension_table
        ON user_table.suspensionID = suspension_table.suspensionID
        ;
    """
    my_query(sqlstring,cur)
    recset = pd.DataFrame( cur.fetchall() )

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
        SELECT user_num, user_name, suspension_school, c.body_temp, c.condition_date
        FROM	condition_table c
		        INNER JOIN(SELECT user_tableID,
								MAX(condition_date) AS last_input_date
						    FROM condition_table
						    GROUP BY user_tableID) s
					    ON c.user_tableID = s.user_tableID 
						    AND c.condition_date = DATE(s.last_input_date)
        INNER JOIN user_table
        ON c.user_tableID = user_table.user_tableID
        INNER JOIN suspension_table
        ON user_table.suspensionID = suspension_table.suspensionID
        WHERE user_num = '{name_userNum}' OR user_name = '{name_userNum}'
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

@condition_action.route("/condition_action",methods=["POST"])
def condition_action(): 
    #DBオープン    
    dbcon,cur = my_open( **dsn )
    #フォームから主キーの受け取り
    user_num = request.form["user_num"]
    
    #レコード新規挿入のSQL文
    sqlstring = f"""
        SELECT user_num, user_name, suspension_school, condition_date, body_temp, symptom_details, condition_table.delflag
        FROM symptom_table
        INNER JOIN condition_table
        ON symptom_table.symptomID = condition_table.symptomID
        INNER JOIN user_table
        ON condition_table.user_tableID = user_table.user_tableID
        INNER JOIN suspension_table
        ON user_table.suspensionID = suspension_table.suspensionID
        WHERE user_num = '{user_num}'
        ;
    """
    my_query(sqlstring,cur)
    recset_c = pd.DataFrame( cur.fetchall() )
    #DataFrame形式(2次元)をSeries形式(1次元ベクトルデータ)に変換する
    rowdata_c = pd.Series( recset_c.iloc[0] )

    #レコード新規挿入のSQL文
    sqlstring = f"""
        SELECT action_table.user_num, user_name, suspension_school, action_number, action_date_time, movement_method, place, companion, companion_person, _mask, action_table.delflag
        FROM place_table
        INNER JOIN action_table
        ON place_table.placeID = action_table.place_of_departure
        INNER JOIN user_table
        ON action_table.user_num = user_table.user_num
        INNER JOIN suspension_table
        ON user_table.suspensionID = suspension_table.suspensionID
        WHERE action_table.user_num = '{user_num}'
        ;
    """
    my_query(sqlstring,cur)
    recset_a = pd.DataFrame( cur.fetchall() )
    #DataFrame形式(2次元)をSeries形式(1次元ベクトルデータ)に変換する
    rowdata_a = pd.Series( recset_a.iloc[0] )

    #DBクローズ
    my_close( dbcon,cur )

    print(rowdata_c)
    print(rowdata_a)

    return render_template("condition_action_table.html",
        title=f"個人番号={user_num} の体調管理表と行動記録表",
        table_data_c = rowdata_c,
        # table_data_a = rowdata_a
    )
