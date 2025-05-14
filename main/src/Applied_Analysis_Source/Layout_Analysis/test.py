#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

db1 = "C:\\Users\\kohei.mori\\Downloads\\�f�[�^���Y.accdb"

db2 = "C:\\Users\\kohei.mori\\Downloads\\�ڋq��DB_V1.2.0.2_B1-00_B1-41_B2-00-B2-05_�DCRUD����.accdb"

conn1 = connect_accdb(db1)
cursor1 = conn1.cursor()

conn2 = connect_accdb(db2)
cursor2 = conn2.cursor()

sql,_ = make_delete_sql("�ڋq��_COBOL_���o�͏��1",[],[])
cursor1.execute(sql)
conn1.commit()

# sql,_ = make_delete_sql("�A���pDSN�ꗗ",[],[])
# cursor1.execute(sql)
# conn1.commit()

all_dsn = set()
sql = "SELECT * FROM QRY_�ڋq��_JCL_PGM_DSN_NOTNULL"
# df = pd.read_sql(sql,conn2)
df = pd.read_excel("C:\\Users\\kohei.mori\\Downloads\\COBOL_B1-00_B1-41_B2-00-B2-05_merge��.xlsx",sheet_name="COBOL_���o�͏��1")
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
    
    sql,values = make_insert_sql("�ڋq��_COBOL_���o�͏��1",l,keys)
    cursor1.execute(sql,values)
    
# for dsn in all_dsn:
#     sql,values = make_insert_sql("�A���pDSN�ꗗ",[dsn],["DSN��"])
#     cursor1.execute(sql,values)
    

