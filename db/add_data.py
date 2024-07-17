import mysql.connector as mydb
import sys
import pandas as pd
import datetime

dt_now=datetime.datetime.now()

#クエリーの実行
def my_query( sqlstring ):
    try:
        #クエリを実行し，結果をrecsetに代入する
        cur.execute( sqlstring )
    except mydb.Error as e:
        #クエリー実行にエラーが発生した場合，プログラム終了
        print(f"クエリ実行でエラー発生\n{e}")
        print(f"入力されたSQL文は\n{sqlstring}")
        sys.exit()


########### mainルーチン ############

#webprogDBコネクション
try:
    dbcon = mydb.connect(
        host='webprog_db',
        port='3306',
        user='root',
        password='1234'
        #database='covid19'
    )
    # DBを操作するためのカーソルの作成  dictionary=True(フィールド名含む処理)
    cur = dbcon.cursor(dictionary=True)

except mydb.Error as e:
    #コネクション時にエラーが発生した場合，プログラム終了
    print(f"DBコネクションでエラー発生\n{e} ")
    sys.exit()

#もし，テーブルがすでにあれば削除
my_query( "DROP DATABASE IF EXISTS covid19;" )

#データベースの新規作成
my_query( "CREATE DATABASE covid19; ")
my_query( "USE covid19;" )
print("新規データベースcovid19を作成しました")


############# テーブルplace_tableの新規作成
sqlstring = """
    CREATE TABLE place_table (
        place_tableID INT NOT NULL AUTO_INCREMENT,         -- 場所ID
        place VARCHAR(64),                           -- 場所
        lastupdate DATETIME DEFAULT NOW(),           -- 最終更新日時
        delflag BOOLEAN DEFAULT FALSE,               -- 削除フラグ
        PRIMARY KEY (place_tableID)                        -- 主キーの設定
    );
"""
my_query( sqlstring )

i=0  #レコード件数カウント
#ファイルオープン
df = pd.read_csv("./data/place_table.csv",header=0)
#place_table.csvを1行ずつ処理
for ind,rowdata in df.iterrows():
    sqlstring = f"""
        INSERT INTO place_table
        (place)
        VALUES
        ('{rowdata.place}')
    """
    my_query( sqlstring )   #1レコード挿入
    i += 1

print(f"place_tableテーブル{i} レコード追加しました")



############# テーブルsuspension_tableの新規作成
sqlstring = """
    CREATE TABLE suspension_table (
        suspensionID INT NOT NULL AUTO_INCREMENT,     -- 出席停止ID
        suspension_school INT,                        -- 健康、感染、濃厚接触の判断
        suspension_start DATE,                        -- 出席停止開始日
        acceptance BOOLEAN,                           -- 受理
        medical VARCHAR(32),                          -- 医療機関
        doctor VARCHAR(16),                           -- 医師氏名
        lastupdate DATETIME DEFAULT NOW(),            -- 最終更新日時
        delflag BOOLEAN DEFAULT FALSE,                -- 削除フラグ
        PRIMARY KEY (suspensionID)                    -- 主キーの設定
);
"""
my_query( sqlstring )

i=0  #レコード件数カウント
#ファイルオープン
df = pd.read_csv("./data/suspension_table.csv",header=0)
#suspension_table.csvを1行ずつ処理
for ind,rowdata in df.iterrows():
    if rowdata.suspension_school == 1:
        sqlstring = f"""
            INSERT INTO suspension_table
            (suspension_school)
            VALUES
            ({rowdata.suspension_school})
        """
        my_query( sqlstring )   #1レコード挿入
        i += 1
    elif rowdata.suspension_school == 2:
        sqlstring = f"""
            INSERT INTO suspension_table
            (suspension_school,suspension_start,acceptance,medical,doctor)
            VALUES
            ({rowdata.suspension_school}, '{rowdata.suspension_start}' , {rowdata.acceptance}, '{rowdata.medical}','{rowdata.doctor}')
        """
        my_query( sqlstring )   #1レコード挿入
        i += 1
    elif rowdata.suspension_school == 3:
        sqlstring = f"""
            INSERT INTO suspension_table
            (suspension_school,suspension_start,acceptance)
            VALUES
            ({rowdata.suspension_school}, '{rowdata.suspension_start}' , {rowdata.acceptance})
        """
        my_query( sqlstring )   #1レコード挿入
        i += 1

print(f"suspension_table テーブル{i} レコード追加しました")


############# テーブルuser_tableの新規作成
sqlstring = """
    CREATE TABLE user_table (
        userID INT NOT NULL AUTO_INCREMENT,         -- 個人のID
        user_num VARCHAR(16) NOT NULL UNIQUE,       -- 個人番号
        user_pw VARCHAR(16) NOT NULL,               -- パスワード
        _class VARCHAR(16),                         -- 役職
        affiliation VARCHAR(16),                    -- 所属
        tel VARCHAR(16),                            -- 電話番号
        user_name VARCHAR(16),                      -- 氏名
        lastupdate DATETIME DEFAULT NOW(),          -- 最終更新日時
        delflag BOOLEAN DEFAULT FALSE,              -- 削除フラグ
        PRIMARY KEY (userID)                        -- 主キーの設定
);
"""
my_query( sqlstring )

i=0  #レコード件数カウント
#ファイルオープン
df = pd.read_csv("./data/user_table.csv",header=0)
#user_table.csvを1行ずつ処理
for ind,rowdata in df.iterrows():
    sqlstring = f"""
        INSERT INTO user_table
        (user_num,user_pw,_class,affiliation,tel,user_name)
        VALUES
        ('{rowdata.user_num}','{rowdata.user_pw}', '{rowdata._class}' , '{rowdata.affiliation}' , '{rowdata.tel}' , '{rowdata.user_name}' )
    """
    my_query( sqlstring )   #1レコード挿入
    i += 1

print(f"user_table テーブル {i} レコード追加しました")

############# テーブルmove_method_tableの新規作成
sqlstring = """
    CREATE TABLE move_method_table (
        move_method_tableID INT NOT NULL AUTO_INCREMENT,   -- 移動方法ID
        move_method VARCHAR(50),                            -- 番号
        lastupdate DATETIME DEFAULT NOW(),            -- 最終更新日時
        delflag BOOLEAN DEFAULT FALSE,                -- 削除フラグ
        PRIMARY KEY (move_method_tableID),                 -- 主キーの設定
);
"""
my_query( sqlstring )

i=0  #レコード件数カウント
#ファイルオープン
df = pd.read_csv("./data/move_method_table.csv",header=0)
#action.csvを1行ずつ処理
for ind,rowdata in df.iterrows():
    #data.Month は， data['Month'] とおなじ
    sqlstring = f"""
        INSERT INTO move_method_table
        (action_tableID,move_method)
        VALUES
        ({rowdata.action_tableID}, '{rowdata.move_method}' )
    """
    #print( sqlstring )  #for debug
    my_query( sqlstring )   #1レコード挿入
    i += 1

print(f"move_method_table テーブル {i} レコード追加しました")


############# テーブルaction_tableの新規作成
sqlstring = """
    CREATE TABLE action_table (
        action_tableID INT NOT NULL AUTO_INCREMENT,   -- アクションID
        userID INT,                                   -- 個人番号
        action_date_start DATETIME,                   -- 日付と時間
        action_date_end DATETIME,                     -- 日付と時間
        move_method INT                               -- 移動方法
        lastupdate DATETIME DEFAULT NOW(),            -- 最終更新日時
        delflag BOOLEAN DEFAULT FALSE,                -- 削除フラグ
        PRIMARY KEY (action_tableID),                 -- 主キーの設定
        FOREIGN KEY (userID)                          -- 外部キー制約
            REFERENCES user_table(userID)
            ON DELETE cascade
            ON UPDATE cascade
        FOREIGN KEY (move_method)                          -- 外部キー制約
            REFERENCES move_method_table(move_method_tableID)
            ON DELETE cascade
            ON UPDATE cascade
);
"""
my_query( sqlstring )

i=0  #レコード件数カウント
#ファイルオープン
df = pd.read_csv("./data/action_table.csv",header=0)
#action.csvを1行ずつ処理
for ind,rowdata in df.iterrows():
    #data.Month は， data['Month'] とおなじ
    sqlstring = f"""
        INSERT INTO action_table
        (userID,action_date_start,action_date_end)
        VALUES
        ({rowdata.userID}, '{rowdata.action_date_start}' ,' {rowdata.action_date_end}' )
    """
    #print( sqlstring )  #for debug
    my_query( sqlstring )   #1レコード挿入
    i += 1

print(f"action_table テーブル {i} レコード追加しました")




############# テーブルcrowd_tableの新規作成
sqlstring = """
    CREATE TABLE crowd_table (
        crowd_tableID INT NOT NULL AUTO_INCREMENT,    -- クラウドテーブルID
        action_tableID INT,                           -- アクションID
        place_tableID INT,                            -- place_tableのID
        crowd_level INT,                              -- 混み具合
        place_type_tableID VARCHAR(32),                       -- 出発地・中継地・到着地の区別
        lastupdate DATETIME DEFAULT NOW(),            -- 最終更新日時
        delflag BOOLEAN DEFAULT FALSE,                -- 削除フラグ
        PRIMARY KEY (crowd_tableID),                  -- 主キーの設定
        FOREIGN KEY (action_tableID)                  -- 外部キー制約
            REFERENCES action_table(action_tableID)
            ON DELETE cascade
            ON UPDATE cascade,
        FOREIGN KEY (place_tableID)                  -- 外部キー制約
            REFERENCES place_table(place_tableID)
            ON DELETE cascade
            ON UPDATE cascade
);
"""
my_query( sqlstring )

i=0  #レコード件数カウント
#ファイルオープン
df = pd.read_csv("./data/crowd_table.csv",header=0)
#action.csvを1行ずつ処理
for ind,rowdata in df.iterrows():
    #data.Month は， data['Month'] とおなじ
    sqlstring = f"""
        INSERT INTO crowd_table
        (action_tableID,place_tableID,crowd_level,place_type_tableID)
        VALUES
        ({rowdata.action_tableID}, {rowdata.place_tableID}, {rowdata.crowd_level},{rowdata.place_type_tableID}  )
    """
    #print( sqlstring )  #for debug
    my_query( sqlstring )   #1レコード挿入
    i += 1

print(f"crowd_table テーブル {i} レコード追加しました")


############# テーブルcompanion_tableの新規作成
sqlstring = """
    CREATE TABLE companion_table (
        companion_tableID INT NOT NULL AUTO_INCREMENT,-- コンパニオンテーブルID
        action_tableID INT,                           -- アクションID
        companion_name VARCHAR(32),                   -- 同行者の名前
        _mask BOOLEAN,                                -- マスクを着けているかどうか
        lastupdate DATETIME DEFAULT NOW(),            -- 最終更新日時
        delflag BOOLEAN DEFAULT FALSE,                -- 削除フラグ
        PRIMARY KEY (companion_tableID),                  -- 主キーの設定
        FOREIGN KEY (action_tableID)                  -- 外部キー制約
            REFERENCES action_table(action_tableID)
            ON DELETE cascade
            ON UPDATE cascade
);
"""
my_query( sqlstring )

i=0  #レコード件数カウント
#ファイルオープン
df = pd.read_csv("./data/companion_table.csv",header=0)
#action.csvを1行ずつ処理
for ind,rowdata in df.iterrows():
    #data.Month は， data['Month'] とおなじ
    sqlstring = f"""
        INSERT INTO companion_table
        (action_tableID,companion_name,_mask)
        VALUES
        ({rowdata.action_tableID}, '{rowdata.companion_name}', {rowdata._mask} )
    """
    #print( sqlstring )  #for debug
    my_query( sqlstring )   #1レコード挿入
    i += 1

print(f"companion_table テーブル {i} レコード追加しました")


############# テーブルcondition_details_tableの新規作成
sqlstring = """
    CREATE TABLE condition_details_table (
        condition_details_tableID INT NOT NULL AUTO_INCREMENT,   -- 詳細詳細テーブルID
        userID INT,                                              -- 個人ID
        condition_date DATE,                                     -- 入力日
        body_temp FLOAT,                                         -- 体温
        lastupdate DATETIME DEFAULT NOW(),                       -- 最終更新日時
        delflag BOOLEAN DEFAULT FALSE,                           -- 削除フラグ
        PRIMARY KEY (condition_details_tableID),                             -- 主キーの設定
        FOREIGN KEY (userID)                             -- 外部キー制約
            REFERENCES user_table(userID)
            ON DELETE cascade
            ON UPDATE cascade
);
"""
my_query( sqlstring )

i=0  #レコード件数カウント
#ファイルオープン
df = pd.read_csv("./data/condition_details_table.csv",header=0)
#action.csvを1行ずつ処理
for ind,rowdata in df.iterrows():
    #data.Month は， data['Month'] とおなじ
    sqlstring = f"""
        INSERT INTO condition_details_table
        (userID,condition_date,body_temp)
        VALUES
        ({rowdata.userID}, '{rowdata.condition_date}', {rowdata.body_temp} )
    """
    #print( sqlstring )  #for debug
    my_query( sqlstring )   #1レコード挿入
    i += 1

print(f"condition_details_table テーブル {i} レコード追加しました")


############# テーブルcondition_taleの新規作成
sqlstring = """
    CREATE TABLE condition_table(
        condition_tableID INT NOT NULL AUTO_INCREMENT,     -- 体調ID
        condition_details_tableID INT,               -- 体調詳細テーブルID
        symptomID INT,                               -- 症状ID
        lastupdate DATETIME DEFAULT NOW(),           -- 最終更新日時
        delflag BOOLEAN DEFAULT FALSE,               -- 削除フラグ
        PRIMARY KEY (condition_tableID),                   -- 主キーの設定
        FOREIGN KEY (condition_details_tableID)                             -- 外部キー制約
            REFERENCES condition_details_table(condition_details_tableID)
            ON DELETE cascade
            ON UPDATE cascade
    )
"""
my_query( sqlstring )

i=0  #レコード件数カウント
#ファイルオープン
df = pd.read_csv("./data/condition_table.csv",header=0)
#condition_table.csvを1行ずつ処理
for ind,rowdata in df.iterrows():
    #data.Month は， data['Month'] とおなじ
    sqlstring = f"""
        INSERT INTO condition_table
        (condition_details_tableID,symptomID)
        VALUES
        ({rowdata.condition_details_tableID},  {rowdata.symptomID})
    """
    #print( sqlstring )  #for debug
    my_query( sqlstring )   #1レコード挿入
    i += 1

print(f"condition_table テーブル{i} レコード追加しました")


############# テーブルcondition_taleの新規作成
sqlstring = """
    CREATE TABLE vaccination_table(
        vaccination_tableID INT NOT NULL AUTO_INCREMENT,     -- ワクチン接種ID
        userID INT,                                          -- 個人ID
        vaccination_num INT,                                 -- 接種回数
        vaccination_date DATE,                               -- 接種日時
        lastupdate DATETIME DEFAULT NOW(),                   -- 最終更新日時
        delflag BOOLEAN DEFAULT FALSE,                       -- 削除フラグ
        PRIMARY KEY (vaccination_tableID),                           -- 主キーの設定
        FOREIGN KEY (userID)                                 -- 外部キー制約
            REFERENCES user_table(userID)
            ON DELETE cascade
            ON UPDATE cascade
    )
"""
my_query( sqlstring )

i=0  #レコード件数カウント
#ファイルオープン
df = pd.read_csv("./data/vaccination_table.csv",header=0)
#condition_table.csvを1行ずつ処理
for ind,rowdata in df.iterrows():
    #data.Month は， data['Month'] とおなじ
    sqlstring = f"""
        INSERT INTO vaccination_table
        (userID,vaccination_num,vaccination_date)
        VALUES
        ({rowdata.userID},  {rowdata.vaccination_num}, '{rowdata.vaccination_date}')
    """
    #print( sqlstring )  #for debug
    my_query( sqlstring )   #1レコード挿入
    i += 1

print(f"vaccination_table テーブル{i} レコード追加しました")


#DBに書き込み
dbcon.commit()  

#カーソルとDBコンソールのクローズ
cur.close()
dbcon.close()
