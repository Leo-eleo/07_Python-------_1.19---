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
        if "���Y�֘A����������" not in sheetname:
            continue
        df = df_all[sheetname]
        df.fillna("",inplace=True)
        for source,relation,to_source in zip(df["�Ăяo���掑�Y"],df["�Ăяo�����@"],df["�ďo�����Y�i�����o�̂݁j"]):
            source,relation,to_source = Trim(source),Trim(relation),Trim(to_source)
            if str(relation).startswith("COBOL") or str(relation).endswith("PGM") or str(relation).endswith("PGM�ďo"):
                if source not in common_module_dic:
                    common_module_dic[source] = set()
                common_module_dic[source].add(to_source)

    common_module_list = []
    for key,value in common_module_dic.items():
        judge = ""
        if len(value) > 1:
            judge = "��"
        common_module_list.append([key,len(value),judge])
    
    common_module_list.sort()
    
    write_excel_multi_sheet("���ʃ��W���[���ꗗ.xlsx",common_module_list,"���ʃ��W���[���ꗗ",title,["COBOL���Y�i�����o�j","�֘A���Y��","���ʃ��W���[������"])
if __name__ == "__main__":     

    main(sys.argv[1],sys.argv[2])