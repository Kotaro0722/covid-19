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
        (placeID,place,crowd_label,lastupdate,delflag)
        VALUES
        ('{rowdata.place}', '{rowdata.crowd_label}' , '{dt_now}')
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
        (symptomID,symptom_details)
        VALUES
        ('{rowdata.symptom_details}')
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
        (S_Number, Croom, Math, Eng, Jpn)
        VALUES
        ('{rowdata.S_Number}', '{rowdata.Croom}' , {rowdata.Math}, {rowdata.Eng}, {rowdata.Jpn})
    """
    #print( sqlstring )  #for debug
    my_query( sqlstring )   #1レコード挿入
    i += 1

print(f"suspention_table テーブル{i} レコード追加しました")


############# テーブルuser_tableの新規作成
sqlstring = """
    CREATE TABLE user_table(
        Weather_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        Month INT ,
        Year INT,
        Area VARCHAR(20),
        Temp_max float,
        Temp_mean float,
        Temp_min float,
        Precipitation float,
        Sunshine float
    )
"""
my_query( sqlstring )

i=0  #レコード件数カウント
#ファイルオープン
df = pd.read_csv("./user_table.csv",header=0)
#user_table.csvを1行ずつ処理
for ind,rowdata in df.iterrows():
    #data.Month は， data['Month'] とおなじ
    sqlstring = f"""
        INSERT INTO user_table
        (month,year,area,temp_max,temp_mean,temp_min,precipitation,sunshine)
        VALUES
        ({rowdata.Month}, {rowdata.Year} , '{rowdata.Area}' , {rowdata.Temp_max} , {rowdata.Temp_mean} , 
        {rowdata.Temp_min} , {rowdata.Precipitation} , {rowdata.Sunshine} )
    """
    #print( sqlstring )  #for debug
    my_query( sqlstring )   #1レコード挿入
    i += 1

print(f"user_table テーブル {i} レコード追加しました")


############# テーブルaction_tableの新規作成
sqlstring = """
    CREATE TABLE action_table(
        Weather_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        Month INT ,
        Year INT,
        Area VARCHAR(20),
        Temp_max float,
        Temp_mean float,
        Temp_min float,
        Precipitation float,
        Sunshine float
    )
"""
my_query( sqlstring )

i=0  #レコード件数カウント
#ファイルオープン
df = pd.read_csv("./action_table.csv",header=0)
#action.csvを1行ずつ処理
for ind,rowdata in df.iterrows():
    #data.Month は， data['Month'] とおなじ
    sqlstring = f"""
        INSERT INTO action_table
        (month,year,area,temp_max,temp_mean,temp_min,precipitation,sunshine)
        VALUES
        ({rowdata.Month}, {rowdata.Year} , '{rowdata.Area}' , {rowdata.Temp_max} , {rowdata.Temp_mean} , 
        {rowdata.Temp_min} , {rowdata.Precipitation} , {rowdata.Sunshine} )
    """
    #print( sqlstring )  #for debug
    my_query( sqlstring )   #1レコード挿入
    i += 1

print(f"action_table テーブル {i} レコード追加しました")


############# テーブルcondition_taleの新規作成
sqlstring = """
    CREATE TABLE condition_table(
        siken1_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        cram VARCHAR(20),
        club VARCHAR(20),
        score int
    )
"""
my_query( sqlstring )

i=0  #レコード件数カウント
#ファイルオープン
df = pd.read_csv("./condition_table.csv",header=0)
#condition_table.csvを1行ずつ処理
for ind,rowdata in df.iterrows():
    #data.Month は， data['Month'] とおなじ
    sqlstring = f"""
        INSERT INTO condition_table
        (cram, club, score)
        VALUES
        ('{rowdata.cram}', '{rowdata.club}' , {rowdata.score})
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
