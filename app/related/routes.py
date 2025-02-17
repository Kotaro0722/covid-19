from flask import render_template,request,redirect,url_for,session
from . import related
from . import related_table
from . import related_search_table
from . import admin_condition
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

@related.route('/related', methods=["POST"])
def related():
    if "username" in session:       
        return render_template("related_search.html",userName=session["username"])
    else:
        return redirect(url_for("login.login_"))
    return render_template('related_search.html',
        title = "関係者リストページ"
    )

@related_table.route('/related_table')
def related_table():
    dbcon,cur = my_open( **dsn )
    #レコード新規挿入のSQL文
    sqlstring = f"""
        SELECT user_table.userID, user_num, user_name, suspension_school, c.body_temp, c.condition_date, v1.vaccination_num, v1.vaccination_date
        FROM condition_details_table c
		INNER JOIN(
            SELECT userID,MAX(condition_date) AS last_input_date
		    FROM condition_details_table
			GROUP BY userID) s
		ON c.userID = s.userID AND c.condition_date = DATE(s.last_input_date)
        RIGHT JOIN user_table
        ON c.userID = user_table.userID
        LEFT JOIN suspension_table
        ON user_table.userID = suspension_table.userID
        LEFT JOIN vaccination_table v1
        INNER JOIN(
            SELECT userID, MAX(vaccination_date) AS last_vaccination_date
            FROM vaccination_table
            GROUP BY userID) v2
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
        FROM condition_details_table c
	        INNER JOIN(
                SELECT userID,MAX(condition_date) AS last_input_date
			    FROM condition_details_table
		        GROUP BY userID) s
	        ON c.userID = s.userID AND c.condition_date = DATE(s.last_input_date)
        RIGHT JOIN user_table
        ON c.userID = user_table.userID
        LEFT JOIN suspension_table
        ON user_table.userID = suspension_table.userID
        LEFT JOIN vaccination_table v1
        INNER JOIN(
            SELECT userID, MAX(vaccination_date) AS last_vaccination_date
            FROM vaccination_table
            GROUP BY userID) v2
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

@admin_condition.route("/admin_condition", methods=["POST"])
def admin_condition():
    #外部キーであるuserIDを取得
    dbcon,cur = my_open( **dsn )
    # sql_string=f"""
    #     SELECT userID FROM user_table
    #     WHERE user_num='{session["username"]}'
    # """
    # my_query(sql_string,cur)
    # recset=pd.DataFrame(cur.fetchall())
    # userID=recset["userID"][0]
    userID = request.form["userID"]
    sql_string=f"""
        SELECT
            user_table.userID,
            user_table.user_name,
            condition_details_table.condition_date,
            condition_details_table.body_temp,
            condition_table.symptomID,
            condition_table.lastupdate
        FROM condition_table
        INNER JOIN condition_details_table
        ON condition_table.condition_details_tableID = condition_details_table.condition_details_tableID
        INNER JOIN user_table
        ON condition_details_table.userID = user_table.userID
        WHERE 
            condition_details_table.userID = {userID};
    """
    my_query(sql_string,cur)
    recset=pd.DataFrame(cur.fetchall())
    #print(recset)
    
    return render_template("condition_table.html",
                           data=recset.to_dict(orient='records'),
                           main_link = "/main_admin"
                           )

@admin_action.route("/admin_action",methods=["POST"])
def admin_action(): 
    #DBオープン    
    dbcon,cur = my_open( **dsn )
    #フォームから主キーの受け取り
    userID = request.form["userID"]
    
    #入力されたuserIDのactionIDを参照し，インナージョインで表示
    sql_string=f"""
        SELECT DISTINCT
            userID,
            action_tableID AS actionID,
            action_date_start AS action_date_start,
            action_date_end AS action_date_end,
            lastupdate AS lastupdate
        FROM action_table
        WHERE 
            userID = {userID};
    """
    # sql_string=f"""
    #     SELECT 
    #         action_table.userID AS userID,
    #         action_table.action_tableID AS actionID,
    #         action_table.action_date_start AS action_date_start,
    #         action_table.action_date_end AS action_date_end,
    #         move_method_table.move_method AS move_method,
    #         crowd_table.place_type_tableID AS place_type_tableID,
    #         crowd_table.crowd_level AS crowd_level,
    #         action_table.lastupdate AS lastupdate
    #     FROM action_table
    #     INNER JOIN 
    #         move_method_table ON action_table.move_method_tableID = move_method_table.move_method_tableID
    #     INNER JOIN 
    #         crowd_table ON action_table.action_tableID = crowd_table.action_tableID  
    #     WHERE 
    #         action_table.userID = {userID};
    # """
    my_query(sql_string,cur)
    #print(sql_string)
    recset=pd.DataFrame(cur.fetchall())

    
    # データベース接続を閉じる
    my_close( dbcon,cur )
    
    return render_template( "action_output.html",
        data=recset.to_dict(orient='records'),
        main_link = "/main_admin"
         
    )