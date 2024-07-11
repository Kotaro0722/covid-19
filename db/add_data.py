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
        placeID INT NOT NULL AUTO_INCREMENT,         -- 場所ID
        place VARCHAR(64),                           -- 場所
        crowd_level INT,                             -- 混み具合
        lastupdate DATETIME DEFAULT NOW(),           -- 最終更新日時
        delflag BOOLEAN DEFAULT FALSE,               -- 削除フラグ
        PRIMARY KEY (placeID)                        -- 主キーの設定
    );
"""
my_query( sqlstring )

i=0  #レコード件数カウント
#ファイルオープン
df = pd.read_csv("./data/place_table.csv",header=0)
#place_table.csvを1行ずつ処理
for ind,rowdata in df.iterrows():
    #data.Month は， data['Month'] とおなじ
    sqlstring = f"""
        INSERT INTO place_table
        (place,crowd_level)
        VALUES
        ('{rowdata.place}', {rowdata.crowd_level})
    """
    #print( sqlstring )  #for debug
    my_query( sqlstring )   #1レコード挿入
    i += 1

print(f"place_tableテーブル{i} レコード追加しました")


############# テーブルsymptom_tableの新規作成
sqlstring = """
    CREATE TABLE symptom_table (
        symptomID INT NOT NULL AUTO_INCREMENT,       -- 症状ID
        symptom_details VARCHAR(16),                 -- 症状
        lastupdate DATETIME DEFAULT NOW(),           -- 最終更新日時
        delflag BOOLEAN DEFAULT FALSE,               -- 削除フラグ
        PRIMARY KEY (symptomID)                      -- 主キーの設定
    );
"""
my_query( sqlstring )

i=0  #レコード件数カウント
#ファイルオープン
df = pd.read_csv("./data/symptom_table.csv",header=0)
#symptom_table.csvを1行ずつ処理
for ind,rowdata in df.iterrows():
    #data.Month は， data['Month'] とおなじ
    sqlstring = f"""
        INSERT INTO symptom_table
        (symptom_details)
        VALUES
        ('{rowdata.symptom_details}')
    """
    #print( sqlstring )  #for debug
    my_query( sqlstring )   #1レコード挿入
    i += 1

print(f"symptom_table テーブル{i} レコード追加しました")



############# テーブルsuspension_tableの新規作成
sqlstring = """
    CREATE TABLE suspension_table (
        suspensionID INT NOT NULL AUTO_INCREMENT,     -- 出席停止ID
        suspension_school BOOLEAN,                    -- 出席停止
        suspension_start DATE,                        -- 出席停止開始日
        suspension_end DATE,                          -- 出席停止終了日
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
    #data.Month は， data['Month'] とおなじ
    if rowdata.suspension_school==True:
        sqlstring = f"""
            INSERT INTO suspension_table
            (suspension_school,suspension_start,suspension_end,acceptance,medical,doctor)
            VALUES
            ({rowdata.suspension_school}, '{rowdata.suspension_start}' , '{rowdata.suspension_end}', {rowdata.acceptance}, '{rowdata.medical}','{rowdata.doctor}')
        """
        #print( sqlstring )  #for debug
        my_query( sqlstring )   #1レコード挿入
        i += 1
    else:
        sqlstring = f"""
            INSERT INTO suspension_table
            (suspension_school)
            VALUES
            ({rowdata.suspension_school})
        """
        #print( sqlstring )  #for debug
        my_query( sqlstring )   #1レコード挿入
        i += 1

print(f"suspension_table テーブル{i} レコード追加しました")


############# テーブルuser_tableの新規作成
sqlstring = """
    CREATE TABLE user_table (
        user_tableID INT NOT NULL AUTO_INCREMENT,         -- 個人のID
        user_num VARCHAR(16) NOT NULL UNIQUE,       -- 個人番号
        _class VARCHAR(16),                          -- 役職
        affiliation VARCHAR(16),                    -- 所属
        tel VARCHAR(16),                            -- 電話番号
        user_name VARCHAR(16),                      -- 氏名
        suspensionID INT,                           -- 出席停止ID
        lastupdate DATETIME DEFAULT NOW(),          -- 最終更新日時
        delflag BOOLEAN DEFAULT FALSE,              -- 削除フラグ
        PRIMARY KEY (user_tableID)                        -- 主キーの設定
);
"""
my_query( sqlstring )

i=0  #レコード件数カウント
#ファイルオープン
df = pd.read_csv("./data/user_table.csv",header=0)
#user_table.csvを1行ずつ処理
for ind,rowdata in df.iterrows():
    #data.Month は， data['Month'] とおなじ
    sqlstring = f"""
        INSERT INTO user_table
        (user_num,_class,affiliation,tel,user_name,suspensionID)
        VALUES
        ('{rowdata.user_num}', '{rowdata._class}' , '{rowdata.affiliation}' , '{rowdata.tel}' , '{rowdata.user_name}' , 
        {rowdata.suspensionID}  )
    """
    #print( sqlstring )  #for debug
    my_query( sqlstring )   #1レコード挿入
    i += 1

print(f"user_table テーブル {i} レコード追加しました")


############# テーブルaction_tableの新規作成
sqlstring = """
    CREATE TABLE action_table (
        action_tableID INT NOT NULL AUTO_INCREMENT,   -- アクションID
        user_num VARCHAR(16),                         -- 個人番号
        action_number INT,                            -- 番号
        action_date_time DATETIME,                    -- 日付と時間
        movement_method VARCHAR(50),                  -- 移動方法
        place_of_departure INT,                       -- 出発地
        waypoint1 INT,                                -- 中継地点1
        waypoint2 INT,                                -- 中継地点2
        waypoint3 INT,                                -- 中継地点3
        place_of_arrival INT,                         -- 到着地
        companion BOOLEAN,                            -- 同行者有無
        companion_person VARCHAR(50),                 -- 同行者名
        _mask BOOLEAN,                                 -- マスクの有無
        lastupdate DATETIME DEFAULT NOW(),            -- 最終更新日時
        delflag BOOLEAN DEFAULT FALSE,                -- 削除フラグ
        PRIMARY KEY (action_tableID),                 -- 主キーの設定
        FOREIGN KEY (user_num) REFERENCES user_table(user_num),  -- 外部キー制約
        FOREIGN KEY (place_of_departure) REFERENCES place_table(placeID),  -- 外部キー制約（仮想の場所テーブル）
        FOREIGN KEY (place_of_arrival) REFERENCES place_table(placeID)     -- 外部キー制約（仮想の場所テーブル）
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
        (user_num,action_number,action_date_time,movement_method,place_of_departure,place_of_arrival,companion,companion_person,_mask)
        VALUES
        ('{rowdata.user_num}', {rowdata.action_number} , '{rowdata.action_date_time}' ,' {rowdata.movement_method}' , 
        {rowdata.place_of_departure} , {rowdata.place_of_arrival} , {rowdata.companion}, '{rowdata.companion_person}',{rowdata._mask})
    """
    #print( sqlstring )  #for debug
    my_query( sqlstring )   #1レコード挿入
    i += 1

print(f"action_table テーブル {i} レコード追加しました")


############# テーブルcondition_taleの新規作成
sqlstring = """
    CREATE TABLE condition_table(
        conditionID INT NOT NULL AUTO_INCREMENT,     -- 体調ID
        user_tableID INT,                            -- 個人番号
        condition_date DATE,                         -- 日付
        body_temp FLOAT,                             -- 体温
        symptomID INT,                               -- 症状ID
        lastupdate DATETIME DEFAULT NOW(),           -- 最終更新日時
        delflag BOOLEAN DEFAULT FALSE,               -- 削除フラグ
        PRIMARY KEY (conditionID),                   -- 主キーの設定
        FOREIGN KEY (user_tableID) REFERENCES user_table(user_tableID),  -- 外部キー制約
        FOREIGN KEY (symptomID) REFERENCES symptom_table(symptomID) -- 外部キー制約（仮想の症状テーブル）
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
        (user_tableID,condition_date,body_temp,symptomID)
        VALUES
        ('{rowdata.user_tableID}', '{rowdata.condition_date}' , {rowdata.body_temp}, {rowdata.symptomID})
    """
    #print( sqlstring )  #for debug
    my_query( sqlstring )   #1レコード挿入
    i += 1

print(f"condition_table テーブル{i} レコード追加しました")


#DBに書き込み
dbcon.commit()  

#カーソルとDBコンソールのクローズ
cur.close()
dbcon.close()
