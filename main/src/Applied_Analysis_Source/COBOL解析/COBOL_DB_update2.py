#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


tables_language_analysis = ["②COBOL_CMD情報","②COBOL_基本情報","②COBOL_関連資産","②COBOL_入出力情報1","②COBOL_入出力情報2","②COBOL_入出力情報3","共通_PGM_IO情報"]
tables_client_db = ["顧客別_COBOL_CMD情報","顧客別_COBOL_基本情報","顧客別_COBOL_関連資産","顧客別_COBOL_入出力情報1","顧客別_COBOL_入出力情報2","顧客別_COBOL_入出力情報3","顧客別_PGM_IO情報"]
keys_list = ["資産ID","資産ID","資産ID","資産ID","資産ID","資産ID","資産ID"]


def main(base_file_path,member_list_path):
    
    
    conn_base = connect_accdb(base_file_path)
    cursor_base = conn_base.cursor()
    
    member_list_df = pd.read_excel(member_list_path)
    
    member_list_dic = {key:asset_class for key,asset_class in zip(member_list_df["KEY2"],member_list_df["資産分類(ACN)"])}
    tables = [table.table_name for table in cursor_base.tables(tableType='TABLE')]
    
    
    if "②COBOL_CMD情報" in tables:
        tables_list = tables_language_analysis
    else:
        tables_list = tables_client_db
        
    table_asset_list = tables_list[1]
    sql = "SELECT * FROM " + table_asset_list
    asset_list_df = pd.read_sql(sql,conn_base)
    
    remove_set = set()
    for key in asset_list_df["資産ID"]:
        key_ext = take_extensions(key)
        
        ### key がメンバ一覧に記載されているとき
        if key_ext in member_list_dic:
            if member_list_dic[key_ext] not in ["COBOL","Easyパラメタ"]:
                print(key,member_list_dic[key_ext])
                remove_set.add(key)
            continue
        
        ### key がメンバ一覧に記載されていないとき
        
        ### JCLからの抽出EASYか確認
        match=re.match("^(.+)E\d\d\d$",key_ext)
        if match:
            name = match.group(1)
            if name in member_list_dic and member_list_dic[name] != "JCL":
                print(key,member_list_dic[name])
                remove_set.add(key)
            continue
        ### key がメンバ一覧に記載されていない and JCL抽出EASY でもない            
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