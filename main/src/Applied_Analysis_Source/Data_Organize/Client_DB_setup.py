#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


language_analysis_db_tables = ["�@JCL_��{���","�@JCL_STEP_SYSIN","�@JCL_STEP_SYSIN2","�@JCL_STEP���","�@JCL_PGM_DSN","�@JCL_CMD���","�@PROC_PARM","�ACOBOL_CMD���","�ACOBOL_�֘A���Y","�ACOBOL_��{���","�ACOBOL_���o�͏��1","�ACOBOL_���o�͏��2","�ACOBOL_���o�͏��3"]
client_db_tables = ["�ڋq��_JCL_��{���","�ڋq��_JCL_STEP_SYSIN","�ڋq��_JCL_STEP_SYSIN","�ڋq��_JCL_STEP���","�ڋq��_JCL_PGM_DSN","�ڋq��_JCL_CMD���","�ڋq��_PROC_PARM","�ڋq��_COBOL_CMD���","�ڋq��_COBOL_�֘A���Y","�ڋq��_COBOL_��{���","�ڋq��_COBOL_���o�͏��1","�ڋq��_COBOL_���o�͏��2","�ڋq��_COBOL_���o�͏��3"]

def main(output_path,input_path,IsDelete):
    

    print("start preparation for analysis.")

    if type(IsDelete) != bool:
        IsDelete = IsDelete == "True"
        
    conn_out = connect_accdb(output_path)
    cursor_out = conn_out.cursor()
    
    if IsDelete == True:
        print("you chose to clear db, so clear the remaining data.")
        
        for table in client_db_tables:
            sql,_ = make_delete_sql(table,[],[])
            cursor_out.execute(sql)
            conn_out.commit()
            
        conn_out.close()
        compact_accdb(output_path)
        conn_out = connect_accdb(output_path)
        cursor_out = conn_out.cursor()

    files = glob_files(input_path)
    for db_in_file in files:
        conn_in = connect_accdb(db_in_file)
        
        for table_in,table_out in zip(language_analysis_db_tables,client_db_tables):
            
            if table_in in ["�ACOBOL_���o�͏��2","�ACOBOL_���o�͏��3"]:
                print("{}�͗e�ʐ����̂��߁A�ǉ����X�L�b�v���܂��B".format(table_in))
                continue
            
            if table_in == "�ACOBOL_CMD���":
                sql =   """\
                        SELECT * FROM �ACOBOL_CMD��� WHERE CMD���� = 'CALL'
                        """
            else:
                sql = "SELECT * FROM "+table_in
                
            df = pd.read_sql(sql,conn_in)
            df.fillna("",inplace=True)
            keys = df.columns.tolist()
            if "AUTO_KEY" in keys:
                keys.remove("AUTO_KEY")
            values = df[keys].values.tolist()
            values = exclude_take_all_extensions(values, keys)
            
            for value in values:
                sql,v = make_insert_sql(table_out,value,keys)
                cursor_out.execute(sql,v)
                
                
            if values:
                conn_out.close()
                compact_accdb(output_path)
                conn_out = connect_accdb(output_path)
                cursor_out = conn_out.cursor()
    
    print("finish preparation")
if __name__ == "__main__":     
    main(sys.argv[1],sys.argv[2],sys.argv[3])