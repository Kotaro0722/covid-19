from flask import render_template,request,session,redirect,url_for
from . import vaccine
from ..MyDatabase import my_open,my_query,my_close
import pandas as pd

dsn = {
    'host' : '172.30.0.10',  #ホスト名(IPアドレス)
    'port' : '3306',        #mysqlの接続ポート番号
    'user' : 'root',      #dbアクセスするためのユーザid
    'password' : '1234',    #ユーザidに対応するパスワード
    'database' : 'covid19' #オープンするデータベース名
}

@vaccine.route("/vaccine_input",methods=["POST","GET"])
def vaccine_input():
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
        
        return render_template("vaccine.html",userName=user_name)
    else:
        return redirect(url_for("login.login_"))

@vaccine.route("/vaccine_process",methods=["POST","GET"])
def vaccine_process():
  
    vaccine_cnt=request.form["vaccineNumber"]
    vaccine_date=request.form["vaccineDate"]
    
    dbcon,cur=my_open(**dsn)
    
    sql_string=f"""
        SELECT userID FROM user_table
        WHERE user_num='{session["username"]}'
    """
    my_query(sql_string,cur)
    recset=pd.DataFrame(cur.fetchall())
    userID=recset["userID"][0]
    
    sql_string=f"""
        INSERT INTO vaccination_table
            (userID,vaccination_num,vaccination_date)
        VALUES
            ({userID},{vaccine_cnt},'{vaccine_date}')
    """
    my_query(sqlstring=sql_string,cur=cur)
    dbcon.commit()
    
    my_close(dbcon,cur)
    return render_template("result.html")
