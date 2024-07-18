from flask import Flask,render_template ,request
from . import close_contact

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

@close_contact.route('/close_contact', methods=["POST"])
def close_contact():
    dbcon,cur = my_open(**dsn)

    #sql
    sqlstring = """
        SELECT DISTINCT 
            user_table.userID, 
            user_num, 
            user_name, 
            suspension_school, 
            c.body_temp, 
            c.condition_date, 
            v1.vaccination_num, 
            v1.vaccination_date
        FROM 
            condition_details_table c
        INNER JOIN (
            SELECT 
                userID, 
                MAX(condition_date) AS last_input_date
            FROM 
                condition_details_table
            GROUP BY 
                userID
        ) s ON c.userID = s.userID AND c.condition_date = DATE(s.last_input_date)
        INNER JOIN 
            user_table ON c.userID = user_table.userID
        LEFT JOIN 
            suspension_table ON user_table.userID = suspension_table.userID
        LEFT JOIN (
            SELECT 
                userID, 
                MAX(vaccination_date) AS last_vaccination_date
            FROM 
                vaccination_table
            GROUP BY 
                userID
        ) v2 ON user_table.userID = v2.userID
        LEFT JOIN 
            vaccination_table v1 ON v1.userID = v2.userID AND v1.vaccination_date = v2.last_vaccination_date
        WHERE 
            suspension_school = 2
        ORDER BY 
            c.condition_date DESC, 
            user_num
    """


    #run query
    my_query(sqlstring, cur)
    recset = pd.DataFrame(cur.fetchall())

    #濃厚接触者がいる場合
    if len(recset) >= 1:
        #型変換
        recset["suspension_school"].fillna("健康", inplace=True)
        recset["suspension_school"].replace(1, '感染者', inplace=True)
        recset["suspension_school"].replace(2, '濃厚接触者', inplace=True)

    #close db
    my_close(dbcon, cur)

    return render_template(  "admin_output.html",
        title = "濃厚接触者のレコード一覧",
        message = f"濃厚接触者数：{len(recset)}人",
        table_data = recset
    )