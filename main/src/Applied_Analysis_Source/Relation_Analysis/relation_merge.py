#!/usr/bin/env python
# -*- coding: shift-jis -*-

import pandas as pd
import os
import sys
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

key_list = ["呼出元資産（元情報）","呼出元資産（メンバのみ）","呼び出し方法","呼び出し先資産","備考"]

def main(folder_path,title):
    print("start to merge each relation result")
    today = str(datetime.date.today())
    
    path = title
    if os.path.isdir(path) == False:
        os.makedirs(path)
        
        
    excel_files = glob_files(folder_path)
    merge_relation_list = []
    for excel_file in excel_files:
        if "資産関連性" not in excel_file:
            continue
        excel_name,_ = get_filenames(excel_file)
        print("read_excel : " + excel_name);
        df = pd.read_excel(excel_file,sheet_name=None)
        df_sheet_list = df.keys()
        for sheet_name in df_sheet_list:
            if sheet_name == "XPBKIC":
                continue
            df_now = df[sheet_name]
            df_now.fillna("",inplace=True)
            if sheet_name == "画面定義":
                for i in range(len(df_now)):
                    data = df_now.iloc[i]
                    now_list = [str(data[key]) for key in key_list] + [excel_name,sheet_name]
                    if data["呼出元資産（元情報）"] == "":
                        # now_list[0] = data["MCP定義"]
                        now_list[4] += " " + data["MCP定義"]
                    merge_relation_list.append(now_list)
                
                
            else:
                for i in range(len(df_now)):
                    data = df_now.iloc[i]
                    now_list = [data[key] for key in key_list] + [excel_name,sheet_name]
                    merge_relation_list.append(now_list)
    merge_relation_list.sort(key=lambda x: (str(x[2]),str(x[0]),str(x[1]),str(x[3])))
    write_excel_multi_sheet(join_file_name_xlsx(today,"関連性マージ"),merge_relation_list,"資産関連性調査結果",path,["呼出元資産","呼出元資産（メンバのみ）","呼び出し方法","呼び出し先資産","備考","Excel_Name","Sheet_Name"])
        
    print("finish merge relations")
        
        
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])