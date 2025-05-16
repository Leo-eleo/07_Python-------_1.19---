#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


language_analysis_db_tables = ["①JCL_基本情報","①JCL_STEP_SYSIN","①JCL_STEP_SYSIN2","①JCL_STEP情報","①JCL_PGM_DSN","①JCL_CMD情報","①PROC_PARM","②COBOL_CMD情報","②COBOL_関連資産","②COBOL_基本情報","②COBOL_入出力情報1","②COBOL_入出力情報2","②COBOL_入出力情報3"]
client_db_tables = ["顧客別_JCL_基本情報","顧客別_JCL_STEP_SYSIN","顧客別_JCL_STEP_SYSIN","顧客別_JCL_STEP情報","顧客別_JCL_PGM_DSN","顧客別_JCL_CMD情報","顧客別_PROC_PARM","顧客別_COBOL_CMD情報","顧客別_COBOL_関連資産","顧客別_COBOL_基本情報","顧客別_COBOL_入出力情報1","顧客別_COBOL_入出力情報2","顧客別_COBOL_入出力情報3"]

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
            
            if table_in in ["②COBOL_入出力情報2","②COBOL_入出力情報3"]:
                print("{}は容量制限のため、追加をスキップします。".format(table_in))
                continue
            
            if table_in == "②COBOL_CMD情報":
                sql =   """\
                        SELECT * FROM ②COBOL_CMD情報 WHERE CMD分類 = 'CALL'
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