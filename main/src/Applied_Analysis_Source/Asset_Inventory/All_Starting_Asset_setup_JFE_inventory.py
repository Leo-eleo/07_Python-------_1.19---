#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
import pandas as pd
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


dt_now = str(datetime.date.today())


all_starting_asset_header = ["TEST_ID","実行順序","実行JOB","補足","出力フォルダ"]


groups_key_list = ["Gr1(形鋼・基盤・その他)","Gr2","Gr3","Gr4","Gr5(冷延・電磁・出荷)","Gr5(冷延・電磁・出荷)","Gr5(冷延・電磁・出荷)",\
                    "Gr6(管理系・操業系)","Gr6(管理系・操業系)",\
                    "Gr7(製鋼系・棒線系・条鋼出荷系)","Gr7(製鋼系・棒線系・条鋼出荷系)","Gr7(製鋼系・棒線系・条鋼出荷系)","Gr7(製鋼系・棒線系・条鋼出荷系)","Gr7(製鋼系・棒線系・条鋼出荷系)"]
groups_info_list = ["Gr1","Gr2","Gr3","Gr4","Gr5(冷延)","Gr5(電磁)","Gr5(出荷)",\
                    "Gr6(管理系)","Gr6(操業系)","Gr7(製鋼系・管理系)","Gr7(製鋼系・操業系)","Gr7(棒線系・管理系)","Gr7(棒線系・操業系)","Gr7(条鋼出荷系・操業系)"
                    ]


        
def make_starting_asset_merge_df(starting_relation_merge_path):
    starting_asset_merge_df = pd.read_excel(starting_relation_merge_path,sheet_name="起点資産一覧",header=1)
    starting_asset_merge_df.fillna("",inplace=True)
    
    return starting_asset_merge_df
    

def output_starting_asset_list_group(starting_asset_merge_df,gr_base_info,title):
    
    
    all_starting_asset_set = set()
    
    for test_id,test_num,job_id,onbatch,gr_info in zip(starting_asset_merge_df["TEST_ID"],starting_asset_merge_df["実行順序"],starting_asset_merge_df["実行JOB"],starting_asset_merge_df["ONBAT"],starting_asset_merge_df["Group分類(JSI解答)"]):
        
        if gr_info.startswith("×"): #or gr_info.startswith("7"):
            continue
        
        if "(" not in gr_info:
            print("Group info format is not matched {},{},{},{}".format(test_id,job_id,onbatch,gr_info))
            continue
        
        gr_lis = gr_info[:gr_info.find("(")].split("・")
        for gr in gr_lis:
            gr_name = "Gr" + gr
            if gr_name not in gr_base_info:
                continue
            
            if gr_name == "Gr5" and gr_base_info[4:6] not in gr_info:
                continue

            if gr_name == "Gr6" or gr_name == "Gr7":
                if gr_base_info[4:len(gr_base_info)-1] not in gr_info:
                    continue
                
            all_starting_asset_set.add((test_id,test_num,job_id,onbatch,""))
    
    
            
    gr_name = gr_base_info
    if "Gr5" in gr_name:
        gr_name = "Gr5"
    if "Gr6" in gr_name:
        gr_name = "Gr6"
    if "Gr7" in gr_name:
        gr_name = "Gr7"
        
        
    file_name = "起点情報_"+gr_base_info+"_"+dt_now+".xlsx"
    out_title = os.path.join(title,gr_name)
    
    if os.path.isdir(out_title) == False:
        os.makedirs(out_title)
        
    write_excel_multi_sheet3(file_name,[sorted(all_starting_asset_set)],["TEST_実施単位"],out_title,[all_starting_asset_header])
        

def main(starting_relation_merge_path,title):
      
    starting_asset_merge_df = make_starting_asset_merge_df(starting_relation_merge_path)
    

    for gr_info in groups_info_list:
        output_starting_asset_list_group(starting_asset_merge_df,gr_info,title)
    
            
    
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])
 