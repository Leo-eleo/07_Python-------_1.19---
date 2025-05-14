#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
import pandas as pd

sys.path.append(os.path.abspath("."))
from Common_analysis import *


def main(new_db_path,old_db_path,table_name,title):
    
    if os.path.isdir(title) == False:
        os.makedirs(title)
        
    new_conn = connect_accdb(new_db_path)
    old_conn = connect_accdb(old_db_path)
    
    sql = "SELECT * FROM " + str(table_name)
    
    try:
        new_df = pd.read_sql(sql,new_conn)
        new_df.fillna("",inplace=True)
    except:
        print("Error: table name {} is not found in {}".format(table_name,new_db_path))
        exit()
        
    try:
        old_df = pd.read_sql(sql,old_conn)
        old_df.fillna("",inplace=True)
    except:
        print("Error: table name {} is not found in {}".format(table_name,old_db_path))
        exit()
        
        
    table_keys = new_df.columns.tolist()
    
    for reject_key in ["AUTO_KEY","手動更新FLG","自動更新FLG"]:
        if reject_key in table_keys:
            table_keys.remove(reject_key)
            
    old_data_set = set()
    same_data_set = set()
    
    for i in range(len(old_df)):
        data = old_df.iloc[i]
        column = [str(data[key]) for key in table_keys]
        old_data_set.add(tuple(column))
        
    additions_list = []
    deletions_list = []
    
    for i in range(len(new_df)):
        data = new_df.iloc[i]
        column = [str(data[key]) for key in table_keys]
        column = tuple(column)
        if column in old_data_set:
            same_data_set.add(column)
        else:
            additions_list.append(list(column))
            
    for column in old_data_set:
        if column in same_data_set:
            continue
        deletions_list.append(list(column))
        
    write_excel_multi_sheet5("テーブル比較_"+table_name+".xlsx",[additions_list,deletions_list],["追加情報一覧","削除情報一覧"],title,[table_keys,table_keys])
    
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])