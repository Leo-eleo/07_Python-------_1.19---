#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
import re
import pandas as pd
import shutil

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

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
        
    
def main(cobol_source_folder,title,setting_file_path):
    
    if os.path.isdir(title) == False:
        os.makedirs(title)
    
    cobol_files = glob_files(cobol_source_folder)
    print("COBOLファイルの取得完了 ファイル数:{}".format(len(cobol_files)))
    
    members_df = make_members_df(setting_file_path)
    
    for group in groups_list:
        group_prefix = group[:3]
        target_source_set = make_group_target_set(members_df,group)
        out_folder = os.path.join(title,group_prefix)
        
        if os.path.isdir(out_folder) == False:
            os.makedirs(out_folder)

        group_cobol_folder = os.path.join(out_folder,"COBOL")
    
        if os.path.isdir(group_cobol_folder) == False:
            os.makedirs(group_cobol_folder)
            
        for file in cobol_files:
            file_name = get_filename(file)
            file_name = take_extensions(file_name)

            if file_name in target_source_set:
                # command = f'copy {file} "{group_cobol_folder}"'
                shutil.copy(file,group_cobol_folder)
                # subprocess.call(command,shell=True)
                
            else:
                match=re.match("^(.+)E\d\d\d$",file_name)
                if match:
                    name = match.group(1)
                else:
                    name = file_name
                if name in target_source_set:
                    shutil.copy(file,group_cobol_folder)
                    # command = f'copy {file} "{group_cobol_folder}"'
                    # subprocess.call(command,shell=True)
        exit()
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3])