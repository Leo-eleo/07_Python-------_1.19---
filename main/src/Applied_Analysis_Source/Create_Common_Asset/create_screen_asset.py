#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


def main(excel_path,title,make_file=True):
    
    # print("input the title of folders and press enter ")
    # title = input()
    
    if os.path.isdir(title) == False:
        os.makedirs(title)
        

    df_all = pd.read_excel(excel_path,sheet_name=None)
    
    screen_module_dic = {}
    
    df_sheet_list = df_all.keys()
    
    for sheetname in df_sheet_list:
        if "���Y�֘A����������" not in sheetname:
            continue
        df = df_all[sheetname]
        df.fillna("",inplace=True)
        for source,relation,to_source in zip(df["�ďo�����Y�i�����o�̂݁j"],df["�Ăяo�����@"],df["�Ăяo���掑�Y"]):
            source,relation,to_source = Trim(source),Trim(relation),Trim(to_source)
            if str(relation).startswith("���"):
                if source not in screen_module_dic:
                    screen_module_dic[source] = set()
                screen_module_dic[source].add(to_source)
   

    screen_module_list = []
    
    for key,value in screen_module_dic.items():
        judge = ""
        if len(value) > 1:
            judge = "��"
        screen_module_list.append([key,len(value),judge])
        
    screen_module_list.sort()
    if make_file:
        write_excel_multi_sheet("��ʎ��Y�ꗗ.xlsx",screen_module_list,"��ʎ��Y�ꗗ",title,["��ʎ��Y�i�����o�j","�֘A���Y��","menu��ʔ���"])
    else:
        return screen_module_list
    
if __name__ == "__main__":     

    main(sys.argv[1],sys.argv[2])