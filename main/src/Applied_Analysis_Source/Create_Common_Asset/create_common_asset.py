#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


def main(excel_path,title):
    
    # print("input the title of folders and press enter ")
    # title = input()
    
    if os.path.isdir(title) == False:
        os.makedirs(title)
        

    df_all = pd.read_excel(excel_path,sheet_name=None)
    
    
    common_module_dic = {}
    
    df_sheet_list = df_all.keys()
    
    for sheetname in df_sheet_list:
        if "資産関連性調査結果" not in sheetname:
            continue
        df = df_all[sheetname]
        df.fillna("",inplace=True)
        for source,relation,to_source in zip(df["呼び出し先資産"],df["呼び出し方法"],df["呼出元資産（メンバのみ）"]):
            source,relation,to_source = Trim(source),Trim(relation),Trim(to_source)
            if str(relation).startswith("COBOL") or str(relation).endswith("PGM") or str(relation).endswith("PGM呼出"):
                if source not in common_module_dic:
                    common_module_dic[source] = set()
                common_module_dic[source].add(to_source)

    common_module_list = []
    for key,value in common_module_dic.items():
        judge = ""
        if len(value) > 1:
            judge = "●"
        common_module_list.append([key,len(value),judge])
    
    common_module_list.sort()
    
    write_excel_multi_sheet("共通モジュール一覧.xlsx",common_module_list,"共通モジュール一覧",title,["COBOL資産（メンバ）","関連資産数","共通モジュール判定"])
if __name__ == "__main__":     

    main(sys.argv[1],sys.argv[2])