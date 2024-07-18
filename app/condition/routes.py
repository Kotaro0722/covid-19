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
    if "username" in session:
        dbcon,cur=my_open(**dsn)
        
        sql_string=f"""
            SELECT user_name FROM user_table
            WHERE user_num='{session["username"]}'
            ;
        """
        my_query(sql_string,cur)
        recset=pd.DataFrame(cur.fetchall())
        user_name=recset["user_name"][0]
        
        return render_template("condition_input.html",userName=user_name)
    else:
        return redirect(url_for("login.login_"))

@condition_output.route("/condition_output", methods=["POST"])
def condition_output():
    if "username" in session:
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
        
        condition_details_rowID=cur.lastrowid
        
        for symptom in symptoms:
            # 体調観察表テーブルへの挿入
            sql_condition_details = f"""
                INSERT INTO condition_table
                    (condition_details_tableID,symptomID)
                VALUES
                    ({condition_details_rowID},{int(symptom)})
            """
            my_query(sql_condition_details, cur)

        # 出席停止テーブルへの挿入
        sql_suspension = f"""
            INSERT INTO suspension_table
                (userId,suspension_school, suspension_start, lastupdate)
            VALUES
                ({userID},'{status}', '{date}', '{dt_now}')
        """
        my_query(sql_suspension, cur)
        
        sql_string=f"""
            SELECT user_name FROM user_table
            WHERE user_num='{session["username"]}'
            ;
        """
        my_query(sql_string,cur)
        recset=pd.DataFrame(cur.fetchall())
        user_name=recset["user_name"][0]
        
        dbcon.commit()
        my_close(dbcon, cur)
        return render_template(
            "condition_output.html", 
            date=date, 
            temperature=temperature, 
            symptoms=symptoms, 
            status=status, 
            release_date=release_date,
            userName=user_name
            )
    else:
        return redirect(url_for("login.login_"))
    
@condition_table.route("/condition_table", methods=["POST"])
def condition_table():
    if "username" in session:
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
        tableData=recset
        if len(tableData) >= 1:
            tableData["symptomID"].replace(1, "関節・筋肉痛", inplace=True)
            tableData["symptomID"].replace(2, "だるさ", inplace=True)
            tableData["symptomID"].replace(3, "頭痛", inplace=True)
            tableData["symptomID"].replace(4, "咽頭痛", inplace=True)
            tableData["symptomID"].replace(5, "息苦しさ", inplace=True)
            tableData["symptomID"].replace(6, "咳・くしゃみ", inplace=True)
            tableData["symptomID"].replace(7, "吐気・嘔吐", inplace=True)
            tableData["symptomID"].replace(8, "腹痛・下痢", inplace=True)
            tableData["symptomID"].replace(9, "味覚障害", inplace=True)
            tableData["symptomID"].replace(10, "味覚障害", inplace=True)
        
        sql_string=f"""
            SELECT user_name FROM user_table
            WHERE user_num='{session["username"]}'
            ;
        """
        my_query(sql_string,cur)
        recset=pd.DataFrame(cur.fetchall())
        user_name=recset["user_name"][0]
        
        return render_template(
            "condition_table.html",
            data=tableData.to_dict(orient='records'),
            main_link = "/main_user",
            userName=user_name
            )
    else:
        return redirect(url_for("login.login_"))

@condition.route("/main_user", methods=["GET"])
def main_user():
    return render_template("main_user.html")
