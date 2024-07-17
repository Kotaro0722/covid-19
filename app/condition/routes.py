from flask import render_template, request, redirect, url_for, session
from . import condition
from . import condition_output
from . import condition_table
from ..MyDatabase import my_open, my_query, my_close
from datetime import datetime, timedelta
import pandas as pd

dsn = {
    'host': '172.30.0.10',  # ホスト名(IPアドレス)
    'port': '3306',         # MySQLの接続ポート番号
    'user': 'root',         # DBアクセスするためのユーザID
    'password': '1234',     # ユーザIDに対応するパスワード
    'database': 'covid19'   # オープンするデータベース名
}

@condition.route("/condition_input", methods=["GET", "POST"])
def condition_input():
    return render_template("condition_input.html")

@condition_output.route("/condition_output", methods=["POST"])
def condition_output():
    date = request.form.get('date')
    temperature = request.form.get('temperature')
    symptoms = request.form.getlist('symptoms')
    status = request.form.get('status')
    user_tableID = 1  # 実際にはセッションや他の方法で取得する必要があります

    if not symptoms:
        symptoms = ['健康']

    release_date = (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=7)).strftime('%Y-%m-%d')

    dt_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    dbcon, cur = my_open(**dsn)

    sql_string = f"""
        SELECT userID FROM user_table
        WHERE user_num='{session["username"]}'
    """

    my_query(sql_string, cur)
    recset = pd.DataFrame(cur.fetchall())
    userID = recset["userID"][0]

    # 体調観察表詳細テーブルへの挿入
    sql_condition_details = f"""
        INSERT INTO condition_details_table
            (userID, condition_date, body_temp, lastupdate)
        VALUES
            ('{userID}', '{date}', '{temperature}', '{dt_now}')
    """
    my_query(sql_condition_details, cur)
    dbcon.commit()

    # 出席停止テーブルへの挿入
    sql_suspension = f"""
        INSERT INTO suspension_table
            (suspension_school, suspension_start, lastupdate)
        VALUES
            ('{status}', '{date}', '{dt_now}')
    """
    my_query(sql_suspension, cur)
    dbcon.commit()
    my_close(dbcon, cur)
    
    


    return render_template("condition_output.html", date=date, temperature=temperature, symptoms=symptoms, status=status, release_date=release_date)
    
@condition_table.route("/condition_table_output", methods=["POST"])
def condition_table():
    dbcon, cur = my_open(**dsn)
    #外部キーであるuserIDを取得
    dbcon,cur = my_open( **dsn )
    sql_string=f"""
        SELECT userID FROM user_table
        WHERE user_num='{session["username"]}'
    """
    my_query(sql_string,cur)
    recset=pd.DataFrame(cur.fetchall())
    userID=recset["userID"][0]
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
    print(recset)
    
    return render_template("condition_table.html",
                           data=recset.to_dict(orient='records')
                           )

@condition.route("/main_user", methods=["GET"])
def main_user():
    return render_template("main_user.html")
