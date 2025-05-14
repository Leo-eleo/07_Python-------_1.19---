#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

db1 = "C:\\Users\\kohei.mori\\Downloads\\データ資産.accdb"

db2 = "C:\\Users\\kohei.mori\\Downloads\\顧客別DB_V1.2.0.2_B1-00_B1-41_B2-00-B2-05_⑤CRUD準備.accdb"

conn1 = connect_accdb(db1)
cursor1 = conn1.cursor()

conn2 = connect_accdb(db2)
cursor2 = conn2.cursor()

sql,_ = make_delete_sql("顧客別_COBOL_入出力情報1",[],[])
cursor1.execute(sql)
conn1.commit()

# sql,_ = make_delete_sql("②利用DSN一覧",[],[])
# cursor1.execute(sql)
# conn1.commit()

all_dsn = set()
sql = "SELECT * FROM QRY_顧客別_JCL_PGM_DSN_NOTNULL"
# df = pd.read_sql(sql,conn2)
df = pd.read_excel("C:\\Users\\kohei.mori\\Downloads\\COBOL_B1-00_B1-41_B2-00-B2-05_merge版.xlsx",sheet_name="COBOL_入出力情報1")
df.fillna("",inplace=True)
keys = df.columns.tolist()

for i in range(len(df)):
    # if i >= 700000:
    #     break
    data = df.iloc[i]
    
    dsn = data["ASSIGN_ID"]
    if "-" in str(dsn):
        data["ASSIGN_ID"] = data["ASSIGN_ID"].split("-")[-1]
    l = [data[key] for key in keys]
    # all_dsn.add(data["DSN"])
    
    sql,values = make_insert_sql("顧客別_COBOL_入出力情報1",l,keys)
    cursor1.execute(sql,values)
    
# for dsn in all_dsn:
#     sql,values = make_insert_sql("②利用DSN一覧",[dsn],["DSN名"])
#     cursor1.execute(sql,values)
    

