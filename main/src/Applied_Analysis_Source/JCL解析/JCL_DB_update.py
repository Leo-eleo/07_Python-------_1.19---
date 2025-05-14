#!/usr/bin/env python
# -*- coding: cp932 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


tables_language_analysis = ["�@JCL_CMD���","�@JCL_��{���","�@JCL_STEP���","�@JCL_STEP_SYSIN","�@JCL_STEP_SYSIN2","�@JCL_PGM_DSN","�@PROC_PARM"]
tables_client_db = ["�ڋq��_JCL_CMD���","�ڋq��_JCL_��{���","�ڋq��_JCL_STEP���","�ڋq��_JCL_STEP_SYSIN","�ڋq��_JCL_STEP_SYSIN","�ڋq��_JCL_PGM_DSN","�ڋq��_PROC_PARM"]
keys_list = ["���YID","JCL��","JCL_NAME","JCL_NAME","JCL_NAME","JCL_NAME","���YID"]


def main(Folder_JCL_path,base_file_path,new_file_path):
    
    JCL_Files = glob_files(Folder_JCL_path)
    
    conn_base = connect_accdb(base_file_path)
    cursor_base = conn_base.cursor()
    
    conn_new = connect_accdb(new_file_path)
    cursor_new = conn_base.cursor()
    
    tables = [table.table_name for table in cursor_base.tables(tableType='TABLE')]
    
    if "�@JCL_CMD���" in tables:
        tables_list = tables_language_analysis
    else:
        tables_list = tables_client_db
        
    for JCL_File in JCL_Files:
        file_name = get_filename(JCL_File)
        file_name_ext = take_extensions(file_name)
        for table_name,key in zip(tables_list,keys_list):
            sql,values = make_delete_sql(table_name,[file_name],[key])
            cursor_base.execute(sql,values)
            
            sql,values = make_delete_sql(table_name,[file_name_ext],[key])
            cursor_base.execute(sql,values)
            
    
    for table_new,tabel_base in zip(tables_language_analysis,tables_list):
        sql = "SELECT * FROM " + table_new
        
        df = pd.read_sql(sql,conn_new)
        df.fillna("",inplace=True)
        keys = df.columns.tolist()
        if "AUTO_KEY" in keys:
            keys.remove("AUTO_KEY")

        for i in range(len(df)):
            data = df.iloc[i]
            values = [data[key] for key in keys]
            sql,values = make_insert_sql(tabel_base,values,keys)
            cursor_base.execute(sql,values)
      
      
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3])
        
    ### ����1 JCL��͍�DB�̊i�[�t�H���_ ����2 �o�̓t�H���_