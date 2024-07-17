from flask import render_template, request, redirect, url_for
from . import condition
from ..MyDatabase import my_open, my_query, my_close
from datetime import datetime, timedelta

dsn = {
    'host': '172.30.0.10',  # ホスト名(IPアドレス)
    'port': '3306',         # MySQLの接続ポート番号
    'user': 'root',         # DBアクセスするためのユーザID
    'password': '1234',     # ユーザIDに対応するパスワード
    'database': 'covid19'  # オープンするデータベース名
}

@condition.route("/condition_input", methods=["GET", "POST"])
def condition_input():
    return render_template("condition_input.html")

@condition.route("/condition_output", methods=["POST"])
def condition_output():
    date = request.form.get('date')
    temperature = request.form.get('temperature')
    symptoms = request.form.getlist('symptoms')
    status = request.form.get('status')
    user_tableID = 1  # 実際にはセッションや他の方法で取得する必要があります

    if not symptoms:
        symptoms = ['健康']

    release_date = (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=7)).strftime('%Y-%m-%d')

    dbcon, cur = my_open(**dsn)

    # 体調観察表詳細テーブルへの挿入
    sql_condition_details = f"""
        INSERT INTO condition_details_table
            (user_tableID, condition_date, body_temp, lastupdate)
        VALUES
            ('{user_tableID}', '{date}', '{temperature}', NOW())
    """
    
    print(sql_condition_details)

    # 出席停止テーブルへの挿入
    sql_suspension = f"""
        INSERT INTO suspention_table
            (suspention_school, suspention_start, suspention_end, lastupdate)
        VALUES
            ('{status}', '{date}', '{release_date}', NOW())
    """
    
    print(sql_suspension)


    # condition_table への挿入（症状IDのマッピング）
    for symptom in symptoms:
        sql_condition_symptom = f"""
            INSERT INTO condition_table
                (symptomID, lastupdate)
            VALUES
                ('{symptom}', NOW())
        """
        my_query(sql_condition_symptom, cur)
        
        print(sql_condition_symptom)


    dbcon.commit()
    my_close(dbcon, cur)

    return render_template("condition_output.html", date=date, temperature=temperature, symptoms=symptoms, status=status, release_date=release_date)

@condition.route("/main_user", methods=["GET"])
def main_user():
    return render_template("main_user.html")

