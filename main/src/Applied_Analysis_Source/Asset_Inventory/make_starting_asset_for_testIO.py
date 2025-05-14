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
    starting_asset_merge_df = starting_asset_merge_df[starting_asset_merge_df["資産要否(合成結果)"] != "廃止済"]
    return starting_asset_merge_df
    
def make_starting_relations_merge_df(starting_relation_merge_path):
    starting_relation_merge_df = pd.read_excel(starting_relation_merge_path,sheet_name="起点資産関連性",header=1)
    starting_relation_merge_df.fillna("",inplace=True)
    starting_relation_merge_df = starting_relation_merge_df[starting_relation_merge_df["呼出方法"] == "MCP起点呼出"]
    
    return starting_relation_merge_df

def starting_asset_list_group(starting_asset_merge_df,gr_base_info):
    
    
    all_starting_asset_set = set()
    
    if gr_base_info == "Gr1":
        gr_set_name = "Gr1(形鋼・基盤・その他)"
    else:
        gr_set_name = gr_base_info
    for test_id,test_num,job_id,onbatch,source_type,gr_info in zip(starting_asset_merge_df["TEST_ID"],starting_asset_merge_df["実行順序"],starting_asset_merge_df["実行JOB"],starting_asset_merge_df["ONBAT"],starting_asset_merge_df["起点資産種別"],starting_asset_merge_df["Group分類(JSI解答)"]):
        
        if gr_info.startswith("×"): #or gr_info.startswith("7"):
            continue
        
        if source_type not in ["FID","GFID","Online","WEB系Online","オンラインJOB"]:
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

            all_starting_asset_set.add((test_id,test_num,job_id,onbatch,gr_set_name))
    
    return all_starting_asset_set
        
def starting_asset_list_group_from_relation(starting_relation_merge_df,gr_base_info):
    
    
    all_starting_relation_set = set()
    
    if gr_base_info == "Gr1":
        gr_set_name = "Gr1(形鋼・基盤・その他)"
    else:
        gr_set_name = gr_base_info
    for job_id,gr_info in zip(starting_relation_merge_df["呼出先資産"],starting_relation_merge_df["Group分類(JSI解答)"]):
        
        if gr_info.startswith("×"): #or gr_info.startswith("7"):
            continue
        
        if "(" not in gr_info:
            print("Group info format is not matched {},{}".format(job_id,gr_info))
            continue
        
        test_id = job_id + "_MCP"
        test_num = 1
        onbatch = "ON"
        
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

            all_starting_relation_set.add((test_id,test_num,job_id,onbatch,gr_set_name))
    
    return all_starting_relation_set

def starting_asset_batch_group(inventory_file_path):
    
    file_name = os.path.split(inventory_file_path)[-1]
    gr_base_info = file_name.split("_")[1]
    
    
    if gr_base_info == "Gr1":
        gr_set_name = "Gr1(形鋼・基盤・その他)"
    else:
        gr_set_name = gr_base_info
        
    starting_asset_batch_group_merge_df = pd.read_excel(inventory_file_path,sheet_name="起点資産マージ")
    starting_asset_batch_group_merge_df = starting_asset_batch_group_merge_df[starting_asset_batch_group_merge_df["資産分類"] == "JCL"]
    starting_asset_batch_group_merge_df.fillna("",inplace=True)
    
    starting_asset_batch_set = set([(job_id,1,job_id,onbatch,gr_set_name) for job_id,onbatch in zip(starting_asset_batch_group_merge_df["関連資産"],starting_asset_batch_group_merge_df["オンバッチ分類"])])
    
    return starting_asset_batch_set

def main(base_path,title):
      
    base_files = glob_files(base_path)
    
    for file in base_files:
        if "起点資産一覧" in file:
            starting_relation_merge_path = file
            
    
    ### オンラインの起点資産を抽出
    starting_asset_merge_df = make_starting_asset_merge_df(starting_relation_merge_path)
    starting_relation_merge_df = make_starting_relations_merge_df(starting_relation_merge_path)

    starting_asset_merge_set = set()
    for gr_info in groups_info_list:
        starting_asset_set_group = starting_asset_list_group(starting_asset_merge_df,gr_info)
        starting_asset_merge_set |= starting_asset_set_group
        
    starting_relation_merge_set = set()
    
    for gr_info in groups_info_list:
        starting_relation_set_group = starting_asset_list_group_from_relation(starting_relation_merge_df,gr_info)
        starting_relation_merge_set |= starting_relation_set_group
            
    
    file_name = "TEST実施単位_オンライン関連資産_"+dt_now+".xlsx"
    out_title = os.path.join(title)
    
    if os.path.isdir(out_title) == False:
        os.makedirs(out_title)
        
    write_excel_multi_sheet3(file_name,[sorted(starting_relation_merge_set)],["TEST_実施単位"],out_title,[all_starting_asset_header])
    
    file_name = "TEST実施単位_オンライン資産階層図_"+dt_now+".xlsx"
    out_title = os.path.join(title)
    
    if os.path.isdir(out_title) == False:
        os.makedirs(out_title)
        
    write_excel_multi_sheet3(file_name,[sorted(starting_asset_merge_set | starting_relation_merge_set)],["TEST_実施単位"],out_title,[all_starting_asset_header])
    
    ### バッチの起点資産を抽出
    
    starting_asset_set_batch_all = set()
    for file in base_files:
        if "棚卸用資産一覧" not in file:
            continue
        if "Template" in file:
            continue
        
        starting_asset_set_batch_group = starting_asset_batch_group(file)
        starting_asset_set_batch_all |= starting_asset_set_batch_group
        
        
    file_name = "TEST実施単位_バッチ_"+dt_now+".xlsx"
    out_title = os.path.join(title)
    
    if os.path.isdir(out_title) == False:
        os.makedirs(out_title)
        
    write_excel_multi_sheet3(file_name,[sorted(starting_asset_set_batch_all)],["TEST_実施単位"],out_title,[all_starting_asset_header])
    
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])
 