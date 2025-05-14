#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

OUTPUT_TABLES = ["顧客別_COBOL_入出力情報1","顧客別_COBOL_入出力情報2"]

INPUT_TABLES_LANGUAGE_ANALYSIS = ["②COBOL_入出力情報1","②COBOL_入出力情報2"]
INPUT_TABLES_CLIENT_DB = OUTPUT_TABLES

def main(output_data_db_path,input_cobol_db_path):
    
    conn_output = connect_accdb(output_data_db_path)
    cursor_output = conn_output.cursor()

    conn_input = connect_accdb(input_cobol_db_path)
    cursor_input = conn_input.cursor()
    
    tables = [table.table_name for table in cursor_input.tables(tableType='TABLE')]
    if INPUT_TABLES_LANGUAGE_ANALYSIS[0] in tables:
        INPUT_TABLES = INPUT_TABLES_LANGUAGE_ANALYSIS
    else:
        INPUT_TABLES = INPUT_TABLES_CLIENT_DB
    
    for table_in,table_out in zip(INPUT_TABLES,OUTPUT_TABLES):
        sql,_ = make_delete_sql(table_out,[],[])
        cursor_output.execute(sql)
        conn_output.commit()
        
        sql = "SELECT * FROM " + table_in
        
        df = pd.read_sql(sql,conn_input)
        df.fillna("",inplace=True)  
        keys = df.columns.tolist()
        for i in range(len(df)):
            data = df.iloc[i]

            key2 = data["資産ID"]
            key2 = take_extensions(key2)
                
            if "ASSIGN_ID" in keys:
                dsn = data["ASSIGN_ID"]
                if "-" in str(dsn):
                    data["ASSIGN_ID"] = data["ASSIGN_ID"].split("-")[-1]
            l = [data[key] for key in keys]
            
            sql,values = make_insert_sql(table_out,l,keys)
            cursor_output.execute(sql,values)
    conn_output.close()
    conn_input.close()

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])
