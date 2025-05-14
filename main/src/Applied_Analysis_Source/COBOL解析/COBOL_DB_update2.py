#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


tables_language_analysis = ["�ACOBOL_CMD���","�ACOBOL_��{���","�ACOBOL_�֘A���Y","�ACOBOL_���o�͏��1","�ACOBOL_���o�͏��2","�ACOBOL_���o�͏��3","����_PGM_IO���"]
tables_client_db = ["�ڋq��_COBOL_CMD���","�ڋq��_COBOL_��{���","�ڋq��_COBOL_�֘A���Y","�ڋq��_COBOL_���o�͏��1","�ڋq��_COBOL_���o�͏��2","�ڋq��_COBOL_���o�͏��3","�ڋq��_PGM_IO���"]
keys_list = ["���YID","���YID","���YID","���YID","���YID","���YID","���YID"]


def main(base_file_path,member_list_path):
    
    
    conn_base = connect_accdb(base_file_path)
    cursor_base = conn_base.cursor()
    
    member_list_df = pd.read_excel(member_list_path)
    
    member_list_dic = {key:asset_class for key,asset_class in zip(member_list_df["KEY2"],member_list_df["���Y����(ACN)"])}
    tables = [table.table_name for table in cursor_base.tables(tableType='TABLE')]
    
    
    if "�ACOBOL_CMD���" in tables:
        tables_list = tables_language_analysis
    else:
        tables_list = tables_client_db
        
    table_asset_list = tables_list[1]
    sql = "SELECT * FROM " + table_asset_list
    asset_list_df = pd.read_sql(sql,conn_base)
    
    remove_set = set()
    for key in asset_list_df["���YID"]:
        key_ext = take_extensions(key)
        
        ### key �������o�ꗗ�ɋL�ڂ���Ă���Ƃ�
        if key_ext in member_list_dic:
            if member_list_dic[key_ext] not in ["COBOL","Easy�p�����^"]:
                print(key,member_list_dic[key_ext])
                remove_set.add(key)
            continue
        
        ### key �������o�ꗗ�ɋL�ڂ���Ă��Ȃ��Ƃ�
        
        ### JCL����̒��oEASY���m�F
        match=re.match("^(.+)E\d\d\d$",key_ext)
        if match:
            name = match.group(1)
            if name in member_list_dic and member_list_dic[name] != "JCL":
                print(key,member_list_dic[name])
                remove_set.add(key)
            continue
        ### key �������o�ꗗ�ɋL�ڂ���Ă��Ȃ� and JCL���oEASY �ł��Ȃ�            
        print(key)
        remove_set.add(key)
        
    # for key in remove_set:
    #     file_name = get_filename(key)
    #     file_name_ext = take_extensions(file_name)
    #     for table_name,key in zip(tables_list,keys_list):
    #         sql,values = make_delete_sql(table_name,[file_name],[key])
    #         cursor_base.execute(sql,values)
            
    #         sql,values = make_delete_sql(table_name,[file_name_ext],[key])
    #         cursor_base.execute(sql,values)
    
    
      
      
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])