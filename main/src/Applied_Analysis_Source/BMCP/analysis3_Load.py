#!/usr/bin/env python
# -*- coding: cp932 -*-
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


def analysis3_Load(BMCP_Sheet,conn,cursor):
    
    sql = "SELECT * FROM BMCP_PGM情報"
    df = pd.read_sql(sql,conn)
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("BMCP_PGM情報",values,keys)
        cursor.execute(sql,values)
        
    # sql,_ = make_delete_sql("BMCP_PGM情報",[],[])
    # cursor.execute(sql)
    # conn.commit()
    for i in range(len(BMCP_Sheet)):
        
        sql,values = make_insert_sql("BMCP_PGM情報",BMCP_Sheet[i][1:],["JCL_NAME","JOB_SEQ","STEP_SEQ","PGM_NAME","SYSIN_PGM","BMCP_PGM"])
        cursor.execute(sql,values)
    conn.commit()