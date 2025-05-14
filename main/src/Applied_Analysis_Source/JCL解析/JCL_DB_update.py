#!/usr/bin/env python
# -*- coding: cp932 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


tables_language_analysis = ["①JCL_CMD情報","①JCL_基本情報","①JCL_STEP情報","①JCL_STEP_SYSIN","①JCL_STEP_SYSIN2","①JCL_PGM_DSN","①PROC_PARM"]
tables_client_db = ["顧客別_JCL_CMD情報","顧客別_JCL_基本情報","顧客別_JCL_STEP情報","顧客別_JCL_STEP_SYSIN","顧客別_JCL_STEP_SYSIN","顧客別_JCL_PGM_DSN","顧客別_PROC_PARM"]
keys_list = ["資産ID","JCL名","JCL_NAME","JCL_NAME","JCL_NAME","JCL_NAME","資産ID"]


def main(Folder_JCL_path,base_file_path,new_file_path):
    
    JCL_Files = glob_files(Folder_JCL_path)
    
    conn_base = connect_accdb(base_file_path)
    cursor_base = conn_base.cursor()
    
    conn_new = connect_accdb(new_file_path)
    cursor_new = conn_base.cursor()
    
    tables = [table.table_name for table in cursor_base.tables(tableType='TABLE')]
    
    if "①JCL_CMD情報" in tables:
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
        
    ### 引数1 JCL解析済DBの格納フォルダ 引数2 出力フォルダ