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


    sql,_ = make_delete_sql("�BDSN�g�p�ӏ�",[],[])    
    cursor_output.execute(sql)
    conn_output.commit()
    
    sql,_ = make_delete_sql("�A���pDSN�ꗗ",[],[])
    cursor_output.execute(sql)
    conn_output.commit()
    
    sql,_ = make_delete_sql("UTL_STEP��_IO���",[],[])
    cursor_output.execute(sql)
    conn_output.commit()
    
    sql_in = "SELECT * FROM �BDSN�g�p�ӏ�"
    df_in = pd.read_sql(sql_in,conn_output)
    keys = df_in.columns.tolist()


    sql = "SELECT * FROM �ڋq��_JCL_PGM_DSN"
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
        
        sql,values = make_insert_sql("�BDSN�g�p�ӏ�",l,keys)
        cursor_output.execute(sql,values)
        
        all_dsn.add(data["DSN"])
        
    for dsn in all_dsn:
        sql,values = make_insert_sql("�A���pDSN�ꗗ",[dsn],["DSN��"])
        cursor_output.execute(sql,values)
        
    sql = "SELECT * FROM UTL_STEP��_IO���"
    df = pd.read_sql(sql,conn_input)
    df = df.dropna(subset=["DD��"])
    df.fillna("",inplace=True)
    keys = df.columns.tolist()

    for i in range(len(df)):
        data = df.iloc[i]
        key2 = data["JCL_NAME"]
        key2 = take_extensions(key2)
                
        l = [data[key] for key in keys]
        
        sql,values = make_insert_sql("UTL_STEP��_IO���",l,keys)
        cursor_output.execute(sql,values)

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])
