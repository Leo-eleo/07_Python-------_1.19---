#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


def main(output_data_db_path,qry_dd_excel_path,utl_step_io_excel_path):
      
    qry_dd_df = pd.read_excel(qry_dd_excel_path,sheet_name="QRY_DD�A�����")
    utl_step_io_df = pd.read_excel(utl_step_io_excel_path,sheet_name="UTL_STEP��_IO���(���H)")
    
    identity_dsn_set = set()
    
    qry_dd_df = qry_dd_df[qry_dd_df["���茋��"] == "OK"]
    utl_step_io_df = utl_step_io_df[utl_step_io_df["���OSTEP"] == "OK"]
    
    for dsn1,dsn2 in zip(qry_dd_df["DSN �@"],qry_dd_df["DSN �A"]):
        identity_dsn_set.add((dsn1,dsn2))
        
    for dsn1,dsn2 in zip(utl_step_io_df["INPUT_DSN"],utl_step_io_df["OUTPUT_DSN"]):
        identity_dsn_set.add((dsn1,dsn2))
    
    conn = connect_accdb(output_data_db_path)
    cursor = conn.cursor()

    sql,_ = make_delete_sql("���񂹏����ݒ���",[],[])
    cursor.execute(sql)
    conn.commit()
    sql = "SELECT * FROM ���񂹏����ݒ���"
    df = pd.read_sql(sql,conn)
    keys = df.columns.tolist()
    
    for dsn1,dsn2 in identity_dsn_set:
        
    
        sql,values = make_insert_sql("���񂹏����ݒ���",[dsn1,dsn2],keys)
        cursor.execute(sql,values)
        
    conn.commit()
    conn.close()
        
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3])
