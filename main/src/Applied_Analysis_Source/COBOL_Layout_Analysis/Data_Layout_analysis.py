#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
import re
import pandas as pd
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *
import create_level_layout
import layout_analysis_main
import process_UTL_Step_IO
import DD_joint
import Identity_Resolution
import multi_layout_check

def insert_identify_resolutions(db_path,identify_resolution_set):
    conn = connect_accdb(db_path)
    cursor = conn.cursor()
    
    table_name = "名寄せ条件設定情報"
    sql,_ = make_delete_sql(table_name,[],[])
    cursor.execute(sql)
    conn.commit()
    keys = ["DSN①","DSN②"]
    for dsn1,dsn2 in identify_resolution_set:
        values = [dsn1,dsn2]
        sql,values = make_insert_sql(table_name,values,keys)
        cursor.execute(sql,values)
    conn.commit()
    conn.close()
    
def insert_layout_group_mapping(db_path,ActSheet_All):
    conn = connect_accdb(db_path)
    cursor = conn.cursor()
    
    table_name = "DSNG_レイアウト関連性設定"
    sql,_ = make_delete_sql(table_name,[],[])
    cursor.execute(sql)
    conn.commit()
    keys = ["データセットグループ","レイアウト名"]
    for ActSheet in ActSheet_All:
        dsn_group,scm_file = ActSheet[0],ActSheet[2]
        if not scm_file.endswith(".scm"):
            continue
        
        values = [dsn_group,scm_file]
        sql,values = make_insert_sql(table_name,values,keys)
        cursor.execute(sql,values)
    conn.commit()
    conn.close()
    
def main(base_path,setting_file_path):
    
    base_files = glob_files(base_path)
    
    for file in base_files:
        if "データ資産" not in file:
            continue
        data_db_path = file
        data_db_group_folder = os.path.abspath(os.path.join(file, os.pardir))
        
        data_cobol_group_folder = os.path.join(data_db_group_folder,"COBOL")
        data_schema_group_folder = os.path.join(data_db_group_folder,"SCHEMA")
        if os.path.isdir(data_schema_group_folder) == False:
            os.makedirs(data_schema_group_folder)
        # create_level_layout.main(data_db_path,data_cobol_group_folder,data_schema_group_folder)
        layout_analysis_main.main(data_db_path,data_schema_group_folder,setting_file_path)
        
        identify_resolution_set = process_UTL_Step_IO.process_UTL_Step_IO_main(data_db_path,data_db_group_folder)
        identify_resolution_set |= DD_joint.DD_joint_main(data_db_path,data_db_group_folder)
        insert_identify_resolutions(data_db_path,identify_resolution_set)
        
        Identity_Resolution.identity_resolution_main(data_db_path,data_db_group_folder)
        
        ActSheet_All = multi_layout_check.muiti_layout_main(data_db_path,data_db_group_folder)
        insert_layout_group_mapping(data_db_path,ActSheet_All)
        
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])