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
        (place,crowd_level,lastupdate)
        VALUES
        ('{rowdata.place}', {rowdata.crowd_level} , '{dt_now}')
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
        (symptom_details,lastupdate)
        VALUES
        ('{rowdata.symptom_details}','{dt_now}')
    """
    #print( sqlstring )  #for debug
    my_query( sqlstring )   #1レコード挿入
    i += 1

print(f"symptom_table テーブル{i} レコード追加しました")



############# テーブルsuspention_tableの新規作成
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
df = pd.read_csv("./data/suspention_table.csv",header=0)
#suspention_table.csvを1行ずつ処理
for ind,rowdata in df.iterrows():
    #data.Month は， data['Month'] とおなじ
    sqlstring = f"""
        INSERT INTO suspention_table
        (suspention_school,suspention_start,suspention_end,acceptance,medical,doctor,lastupdate)
        VALUES
        ({rowdata.suspention_school}, '{rowdata.suspention_start}' , '{rowdata.suspention_end}', {rowdata.acceptance}, '{rowdata.medical}','{rowdata.doctor}','{dt_now}')
    """
    #print( sqlstring )  #for debug
    my_query( sqlstring )   #1レコード挿入
    i += 1

print(f"suspention_table テーブル{i} レコード追加しました")


############# テーブルuser_tableの新規作成
sqlstring = """
    CREATE TABLE user_table (
        userID INT NOT NULL AUTO_INCREMENT,         -- 個人のID
        user_num VARCHAR(16) NOT NULL UNIQUE,       -- 個人番号
        _class VARCHAR(16),                          -- 役職
        affiliation VARCHAR(16),                    -- 所属
        tel VARCHAR(16),                            -- 電話番号
        user_name VARCHAR(16),                      -- 氏名
        suspensionID INT,                           -- 出席停止ID
        action_tableID INT,                         -- アクションID
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
    #data.Month は， data['Month'] とおなじ
    sqlstring = f"""
        INSERT INTO user_table
        (user_num,_class,affiliation,tel,user_name,suspentionID,action_tableID,lastupdate)
        VALUES
        ('{rowdata.user_num}', '{rowdata._class}' , '{rowdata.affiliation}' , {rowdata.tel} , {rowdata.user_name} , 
        {rowdata.suspensionID} , {rowdata.action_tableID} , '{dt_now}' )
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
        action_date VARCHAR(50),                      -- 日付
        action_time VARCHAR(50),                      -- 時間
        movement_method VARCHAR(50),                  -- 移動方法
        place_of_departure VARCHAR(50),               -- 出発地
        place_of_arrival VARCHAR(50),                 -- 到着地
        companion BOOLEAN,                            -- 同行者有無
        companion_person VARCHAR(50),                 -- 同行者名
        mask BOOLEAN,                                 -- マスクの有無
        lastupdate DATETIME DEFAULT NOW(),            -- 最終更新日時
        delflag BOOLEAN DEFAULT FALSE,                -- 削除フラグ
        PRIMARY KEY (action_tableID),                 -- 主キーの設定
        FOREIGN KEY (user_num) REFERENCES personal(user_num),  -- 外部キー制約
        FOREIGN KEY (place_of_departure) REFERENCES places(place_name),  -- 外部キー制約（仮想の場所テーブル）
        FOREIGN KEY (place_of_arrival) REFERENCES places(place_name)     -- 外部キー制約（仮想の場所テーブル）
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
        (user_num,action_number,action_date,action_time,movement_method,place_of_departure,place_of_arrival,companion,companion_person,mask,lastupdate)
        VALUES
        ('{rowdata.user_num}', {rowdata.action_number} , '{rowdata.action_date}' , {rowdata.action_time} ,' {rowdata.movement_method}' , 
        '{rowdata.place_of_departure}' , '{rowdata.place_of_arrival}' , {rowdata.companion}, '{rowdata.companion_person}',{rowdata.mask},{dt_now})
    """
    #print( sqlstring )  #for debug
    my_query( sqlstring )   #1レコード挿入
    i += 1

print(f"action_table テーブル {i} レコード追加しました")


############# テーブルcondition_taleの新規作成
sqlstring = """
    CREATE TABLE condition_table(
        conditionID INT NOT NULL AUTO_INCREMENT,     -- 体調ID
        user_num VARCHAR(16),                        -- 個人番号
        condition_date DATE,                         -- 日付
        body_temp FLOAT,                             -- 体温
        symptomID INT,                               -- 症状ID
        lastupdate DATETIME DEFAULT NOW(),           -- 最終更新日時
        delflag BOOLEAN DEFAULT FALSE,               -- 削除フラグ
        PRIMARY KEY (conditionID),                   -- 主キーの設定
        FOREIGN KEY (user_num) REFERENCES personal(user_num),  -- 外部キー制約
        FOREIGN KEY (symptomID) REFERENCES symptoms(symptomID) -- 外部キー制約（仮想の症状テーブル）
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
        (user_num,condition_date,body_temp,symptomID,lastupdate)
        VALUES
        ('{rowdata.user_num}', '{rowdata.condition_date}' , {rowdata.body_temp}, {rowdata.symptomID},{dt_now})
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
