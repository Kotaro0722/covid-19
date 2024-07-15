from flask import render_template,request
from . import main
from ..MyDatabase import my_open , my_query , my_close

dsn = {
    'host' : '172.30.0.10',  #ホスト名(IPアドレス)
    'port' : '3306',        #mysqlの接続ポート番号
    'user' : 'root',      #dbアクセスするためのユーザid
    'password' : '1234',    #ユーザidに対応するパスワード
    'database' : 'covid19' #オープンするデータベース名
}

@main.route("/",methods=["POST"])
def login_config():
    username=request.form["username"]
    password=request.form["password"]
    
    is_admin=False
    is_user=False
    
    admin_list=[
        {"username":"admin","password":"admin1234"},
    ]    
    user_list=[
        {"username":"user1234","password":"pass1234"},
        {"username":"user5678","password":"pass5678"}, 
    ]
    
    for user in admin_list:
        if user["username"] == username and user["password"] == password:
            is_admin=True
    for user in user_list:
        if user["username"] == username and user["password"] == password:
            is_user=True
            
    
    if is_admin:
         # データベース接続
        dbcon,cur = my_open( **dsn )
        
        # 管理者用データ取得クエリ
        sqlstring = """
        SELECT student_id, name, status, latest_temp, latest_record_time
        FROM student_conditions
        ;
        """
        
        data = my_query(sqlstring,cur)
        
        # データベース接続を閉じる
        my_close(dbcon,cur)
        
        # 管理者メインページを表示
        return render_template("main_admin.html", data=data)

    elif is_user:
        return render_template("main_user.html")
    else:
        return render_template("login.html")
    
    