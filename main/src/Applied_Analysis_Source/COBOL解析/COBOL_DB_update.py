#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


tables_language_analysis = ["�ACOBOL_CMD���","�ACOBOL_��{���","�ACOBOL_�֘A���Y","�ACOBOL_���o�͏��1","�ACOBOL_���o�͏��2","�ACOBOL_���o�͏��3","����_PGM_IO���"]
tables_client_db = ["�ڋq��_COBOL_CMD���","�ڋq��_COBOL_��{���","�ڋq��_COBOL_�֘A���Y","�ڋq��_COBOL_���o�͏��1","�ڋq��_COBOL_���o�͏��2","�ڋq��_COBOL_���o�͏��3","�ڋq��_PGM_IO���"]
keys_list = ["���YID","���YID","���YID","���YID","���YID","���YID","���YID"]


def main(Folder_COBOL_path,base_file_path,new_file_path):

    COBOL_Files = glob_files(Folder_COBOL_path)
    
    conn_base = connect_accdb(base_file_path)
    cursor_base = conn_base.cursor()
    
    # conn_new = connect_accdb(new_file_path)
    # cursor_new = conn_base.cursor()
    new_files = glob_files(new_file_path)
    
    tables = [table.table_name for table in cursor_base.tables(tableType='TABLE')]
    
    if "�ACOBOL_CMD���" in tables:
        tables_list = tables_language_analysis
    else:
        tables_list = tables_client_db
        
    for COBOL_File in COBOL_Files:
        file_name = get_filename(COBOL_File)
        file_name_ext = take_extensions(file_name)
        for table_name,key in zip(tables_list,keys_list):
            sql,values = make_delete_sql(table_name,[file_name],[key])
            # try:
            cursor_base.execute(sql,values)
            # except:
            #     print("error", sql)
            #     # continue
                # # sql = "SELECT * FROM "+table_name
                # # df = pd.read_sql(sql,conn_base)
                
                # print(df.columns.tolist(),key in df.columns.tolist())
                # exit()
                
            
            sql,values = make_delete_sql(table_name,[file_name_ext],[key])
            cursor_base.execute(sql,values)
            
    
    for new_file in new_files:  
        conn_new = connect_accdb(new_file)
        for table_new,tabel_base in zip(tables_language_analysis,tables_list):
            
            if table_new == "�ACOBOL_CMD���":
                sql =   """\
                            SELECT * FROM �ACOBOL_CMD��� WHERE CMD���� = 'CALL'
                            """
            else:
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
                # print(sql,values)
                cursor_base.execute(sql,values)
      
      
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3])