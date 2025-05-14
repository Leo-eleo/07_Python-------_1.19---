#!/usr/bin/env python
# -*- coding: shift-jis -*-

import pandas as pd
import os
import time
import datetime
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


def main(new_path,old_path,title):
    
    print("start to check the difference of relations")
    start = time.time()
    today = str(datetime.date.today())
    
    path = title
    if os.path.isdir(path) == False:
        os.makedirs(path)
 
    
    
    df_old_all = pd.read_excel(old_path,sheet_name=None)
    
    df_new_all = pd.read_excel(new_path,sheet_name=None)

    update_info_list = []
    delete_cand_list = []
    not_in_new_list = []
    same_data_list = []
    old_full_key = {}
    old_less_key = {}
    
    need_check_less_key = {}
    old_list = []
    
    old_deleted_full_dic = {}
    df_sheet_list = df_old_all.keys()
    i = 0
    for sheet in df_sheet_list:
        if "資産関連性調査結果" not in sheet:
            continue
        df_old = df_old_all[sheet]
        for source1,source2,type,to_source,sub_info,excel_name,sheet_name in zip(df_old["呼出元資産"],df_old["呼出元資産（メンバのみ）"],df_old["呼び出し方法"],df_old["呼び出し先資産"],df_old["備考"],df_old["Excel_Name"],df_old["Sheet_Name"]):
            to_source = str(to_source)
            
            old_list.append([source1,source2,type,to_source,sub_info,excel_name,sheet_name])
            
            full_source = source1
            if type == "画面→PGM呼出" and "パターン1" in sub_info:
                full_source = sub_info.split(" ")[-1]
            if type == "COBOL-ENTRY" or type == "ASM-ENTRY":
                full_source = sub_info
                
            if pd.isna(full_source) == False and "%" in str(full_source):
                if (full_source,source2,type) not in old_full_key:
                    old_full_key[(full_source,source2,type)] = []
                    
                old_full_key[(full_source,source2,type)].append([to_source,i])
                
            else:
                if pd.isna(full_source):
                    full_source = ""
                if (full_source,source2,type) not in old_less_key:
                    old_less_key[(full_source,source2,type)] = []
                    
                old_less_key[(full_source,source2,type)].append([to_source,i])
            
            i += 1
            

    
    old_is_used = [0]*len(old_list)
    old_in_new = [0]*len(old_list)
    old_index_dic = {}
    new_list = []
    df_sheet_list = df_new_all.keys()
    i = 0
    for sheet in df_sheet_list:
        if "資産関連性調査結果" not in sheet:
            continue
        df_new = df_new_all[sheet]
        for source1,source2,type,to_source,sub_info,excel_name,sheet_name in zip(df_new["呼出元資産"],df_new["呼出元資産（メンバのみ）"],df_new["呼び出し方法"],df_new["呼び出し先資産"],df_new["備考"],df_new["Excel_Name"],df_new["Sheet_Name"]):
            to_source = str(to_source)
     
            new_list.append([source1,source2,type,to_source,sub_info,excel_name,sheet_name])
            full_source = source1
            if type == "画面→PGM呼出" and "パターン1" in sub_info:
                full_source = sub_info.split(" ")[-1]
            if type == "COBOL-ENTRY"  or type == "ASM-ENTRY":
                full_source = sub_info
            
            if pd.isna(full_source) == False and "%" in str(full_source):

                if (full_source,source2,type) in old_full_key:
                    old_deleted_full_dic[(full_source,source2,type)] = set()
                    for to,ind in old_full_key[(full_source,source2,type)]:
                        #delete_cand_list.append(old_list[ind])
                        old_is_used[ind] = 1
                        old_deleted_full_dic[(full_source,source2,type)].add(to)
                        if (full_source,source2,type,to) not in old_index_dic:
                            old_index_dic[(full_source,source2,type,to)] = []
                            
                        old_index_dic[(full_source,source2,type,to)].append(ind)
                        
                        
                        
                    del old_full_key[((full_source,source2,type))]
                    
                if (full_source,source2,type) in old_deleted_full_dic and to_source in old_deleted_full_dic[(full_source,source2,type)]:
                    same_data_list.append([source1,source2,type,to_source,sub_info,excel_name,sheet_name])
                    for ind in old_index_dic[(full_source,source2,type,to_source)]:
                        old_in_new[ind] = 1
                else:
                    update_info_list.append([source1,source2,type,to_source,sub_info,excel_name,sheet_name])
                
            else:
                if pd.isna(full_source):
                    full_source = ""
         
                if (full_source,source2,type) in need_check_less_key:
                    need_check_less_key[(full_source,source2,type)][0].append([to_source,i])
                    i += 1
                    continue
                
                elif (full_source,source2,type) in old_less_key:
                    need_check_less_key[(full_source,source2,type)] = [[] for j in range(2)]
                    for to,ind in old_less_key[(full_source,source2,type)]:
                        need_check_less_key[(full_source,source2,type)][1].append([to,ind])
                        old_is_used[ind] = 1
                        old_in_new[ind] = 1
                    
                    del old_less_key[(full_source,source2,type)]
                    
                    need_check_less_key[(full_source,source2,type)][0].append([to_source,i])   
    
                else:
                    update_info_list.append([source1,source2,type,to_source,sub_info,excel_name,sheet_name])
                    
            i += 1
            
    for i,(is_used,in_new) in enumerate(zip(old_is_used,old_in_new)):
        if is_used == 1:
            if in_new == 0:
                delete_cand_list.append(old_list[i])
        else: 
            not_in_new_list.append(old_list[i])
        
    need_check_list = []
    for key,value in need_check_less_key.items():
        source1,source2,type = key
        
        new_cand,old_cand = value
        
        new_cand_set = set([new_cand[i][0] for i in range(len(new_cand))])
        old_cand_set = set([old_cand[i][0] for i in range(len(old_cand))])
        # print(key,value,new_cand,old_cand)
        for new_source, new_ind in new_cand:
            if new_source in old_cand_set:
                same_data_list.append(new_list[new_ind])
               
            else:
                need_check_list.append([source1,source2,type,new_source,"","","",""])
                
        for old_source, old_ind in old_cand:
            if old_source in new_cand_set:
                continue
            else:
                need_check_list.append(["","","","",source1,source2,type,old_source])
                
            
    write_excel_multi_sheet4(join_file_name_xlsx(today,"関連性差分調査対象情報"),[need_check_list],["調査対象情報"],path,["呼出元資産","呼出元資産（メンバのみ）","呼び出し方法","呼び出し先資産（更新ファイル）","呼出元資産","呼出元資産（メンバのみ）","呼び出し方法","呼び出し先資産（既存ファイル）"])
        
      

    write_excel_multi_sheet4(join_file_name_xlsx(today,"関連性差分更新情報"),[update_info_list,delete_cand_list,same_data_list,not_in_new_list],["更新対象情報","削除対象情報","重複情報","更新なし情報"],path,["呼出元資産","呼出元資産（メンバのみ）","呼び出し方法","呼び出し先資産","備考","Excel_Name","Sheet_Name"])
    
    
    print("finish to check the difference of relations")
        
        
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3])