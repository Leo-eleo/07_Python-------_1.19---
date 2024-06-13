#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


def main(output_data_db_path,input_client_db_path):
    conn_output = connect_accdb(output_data_db_path)
    cursor_output = conn_output.cursor()

    conn_input = connect_accdb(input_client_db_path)
    cursor_input = conn_input.cursor()


    sql,_ = make_delete_sql("③DSN使用箇所",[],[])    
    cursor_output.execute(sql)
    conn_output.commit()
    
    sql,_ = make_delete_sql("②利用DSN一覧",[],[])
    cursor_output.execute(sql)
    conn_output.commit()
    
    sql,_ = make_delete_sql("UTL_STEP別_IO情報",[],[])
    cursor_output.execute(sql)
    conn_output.commit()
    
    sql_in = "SELECT * FROM ③DSN使用箇所"
    df_in = pd.read_sql(sql_in,conn_output)
    keys = df_in.columns.tolist()


    sql = "SELECT * FROM 顧客別_JCL_PGM_DSN"
    df = pd.read_sql(sql,conn_input)
    df.fillna("",inplace=True)
    df = df[df["DSN"] != ""]
    all_dsn = set()


    for i in range(len(df)):
        data = df.iloc[i]
        key2 = data["JCL_NAME"]
        key2 = take_extensions(key2)
                
        if str(data["DSN"]).startswith("&&"):
            data["DSN"] = key2 + data["DSN"]
        l = [data[key] for key in keys]
        
        sql,values = make_insert_sql("③DSN使用箇所",l,keys)
        cursor_output.execute(sql,values)
        
        all_dsn.add(data["DSN"])
        
    for dsn in all_dsn:
        sql,values = make_insert_sql("②利用DSN一覧",[dsn],["DSN名"])
        cursor_output.execute(sql,values)
        
    sql = "SELECT * FROM UTL_STEP別_IO情報"
    df = pd.read_sql(sql,conn_input)
    df = df.dropna(subset=["DD名"])
    df.fillna("",inplace=True)
    keys = df.columns.tolist()

    for i in range(len(df)):
        data = df.iloc[i]
        key2 = data["JCL_NAME"]
        key2 = take_extensions(key2)
                
        l = [data[key] for key in keys]
        
        sql,values = make_insert_sql("UTL_STEP別_IO情報",l,keys)
        cursor_output.execute(sql,values)

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])
