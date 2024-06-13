#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
import re
import pandas as pd
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *
import COBOL_info_setup
import JCL_info_setup



dt_now = str(datetime.date.today())


groups_list = ["Gr1(形鋼・基盤・その他)","Gr2","Gr3","Gr4","Gr5(冷延・電磁・出荷)","Gr6(管理系・操業系)","Gr7(製鋼系・棒線系・条鋼出荷系)"]

def make_members_df(members_list_path):
    members_df = pd.read_excel(members_list_path,sheet_name="メンバ一覧マージ版",header=1)
    members_df = members_df[["KEY2","資産提供時ライブラリ名"]+groups_list]
    return members_df

def make_group_target_set(members_df,group_name):
    members_group_df = members_df[members_df[group_name] == "○"]
    target_set = set()
    
    for key,received_library in zip(members_group_df["KEY2"],members_group_df["資産提供時ライブラリ名"]):
        target_set.add(key)
        if pd.isna(received_library):
            continue
        received_key = received_library + key[key.index("%"):]
        target_set.add(received_key)
    return target_set
        
    
def main(data_db_empty_path,client_db_path,cobol_db_path,title,setting_file_path):
    
    if os.path.isdir(title) == False:
        os.makedirs(title)
    
    members_df = make_members_df(setting_file_path)
    
    for group in groups_list:
        group_prefix = group[:3]
        target_source_set = make_group_target_set(members_df,group)
        print(group,len(target_source_set))
        out_folder = os.path.join(title,group_prefix)
        
        if os.path.isdir(out_folder) == False:
            os.makedirs(out_folder)

        db_path = f'{out_folder}\\データ資産DB_{group_prefix}_{dt_now}.accdb'
        command = f'copy "{data_db_empty_path}" "{db_path}"'
        subprocess.call(command,shell=True)
        print("create the new accdb file ",db_path)
        COBOL_info_setup.main(db_path,cobol_db_path,target_source_set)
        JCL_info_setup.main(db_path,client_db_path,target_source_set)
        
        exit()
        

        
                
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])