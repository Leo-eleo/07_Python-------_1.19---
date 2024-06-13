#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
import pandas as pd
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


dt_now = str(datetime.date.today())


all_starting_asset_header = ["TEST_ID","���s����","���sJOB","�⑫","�o�̓t�H���_"]


groups_key_list = ["Gr1(�`�|�E��ՁE���̑�)","Gr2","Gr3","Gr4","Gr5(�≄�E�d���E�o��)","Gr5(�≄�E�d���E�o��)","Gr5(�≄�E�d���E�o��)",\
                    "Gr6(�Ǘ��n�E���ƌn)","Gr6(�Ǘ��n�E���ƌn)",\
                    "Gr7(���|�n�E�_���n�E���|�o�׌n)","Gr7(���|�n�E�_���n�E���|�o�׌n)","Gr7(���|�n�E�_���n�E���|�o�׌n)","Gr7(���|�n�E�_���n�E���|�o�׌n)","Gr7(���|�n�E�_���n�E���|�o�׌n)"]
groups_info_list = ["Gr1","Gr2","Gr3","Gr4","Gr5(�≄)","Gr5(�d��)","Gr5(�o��)",\
                    "Gr6(�Ǘ��n)","Gr6(���ƌn)","Gr7(���|�n�E�Ǘ��n)","Gr7(���|�n�E���ƌn)","Gr7(�_���n�E�Ǘ��n)","Gr7(�_���n�E���ƌn)","Gr7(���|�o�׌n�E���ƌn)"
                    ]


        
def make_starting_asset_merge_df(starting_relation_merge_path):
    starting_asset_merge_df = pd.read_excel(starting_relation_merge_path,sheet_name="�N�_���Y�ꗗ",header=1)
    starting_asset_merge_df.fillna("",inplace=True)
    
    return starting_asset_merge_df
    

def output_starting_asset_list_group(starting_asset_merge_df,gr_base_info,title):
    
    
    all_starting_asset_set = set()
    
    for test_id,test_num,job_id,onbatch,gr_info in zip(starting_asset_merge_df["TEST_ID"],starting_asset_merge_df["���s����"],starting_asset_merge_df["���sJOB"],starting_asset_merge_df["ONBAT"],starting_asset_merge_df["Group����(JSI��)"]):
        
        if gr_info.startswith("�~"): #or gr_info.startswith("7"):
            continue
        
        if "(" not in gr_info:
            print("Group info format is not matched {},{},{},{}".format(test_id,job_id,onbatch,gr_info))
            continue
        
        gr_lis = gr_info[:gr_info.find("(")].split("�E")
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
        
        
    file_name = "�N�_���_"+gr_base_info+"_"+dt_now+".xlsx"
    out_title = os.path.join(title,gr_name)
    
    if os.path.isdir(out_title) == False:
        os.makedirs(out_title)
        
    write_excel_multi_sheet3(file_name,[sorted(all_starting_asset_set)],["TEST_���{�P��"],out_title,[all_starting_asset_header])
        

def main(starting_relation_merge_path,title):
      
    starting_asset_merge_df = make_starting_asset_merge_df(starting_relation_merge_path)
    

    for gr_info in groups_info_list:
        output_starting_asset_list_group(starting_asset_merge_df,gr_info,title)
    
            
    
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])
 