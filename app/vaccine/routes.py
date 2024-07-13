from flask import render_template,request
from . import vaccine
from ..MyDatabase import my_open,my_query,my_close

dsn = {
    'host' : '172.30.0.10',  #ホスト名(IPアドレス)
    'port' : '3306',        #mysqlの接続ポート番号
    'user' : 'root',      #dbアクセスするためのユーザid
    'password' : '1234',    #ユーザidに対応するパスワード
    'database' : 'covid19' #オープンするデータベース名
}

@vaccine.route("/vaccine_input",methods=["POST"])
def vaccine_input():
    return render_template("vaccine.html")

@vaccine.route("/vaccine_process",methods=["POST"])
def vaccine_process():
    vaccine_cnt=request.form["vaccineNumber"]
    vaccine_date=request.form["vaccineDate"]
    
    dbcon,cur=my_open(**dsn)
    
    sql_string=f"""
        INSERT INTO vaccination_table
            (userID,vaccination_num,vaccination_date)
        VALUES
            (1,{vaccine_cnt},'{vaccine_date}')
    """
    my_query(sqlstring=sql_string,cur=cur)
    dbcon.commit()
    
    my_close(dbcon,cur)
    return render_template("main_user.html")