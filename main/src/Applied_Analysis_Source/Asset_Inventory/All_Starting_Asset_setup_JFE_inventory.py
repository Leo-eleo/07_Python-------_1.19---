#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
import pandas as pd
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


dt_now = str(datetime.date.today())


all_starting_asset_header = ["TEST_ID","ΐs","ΐsJOB","β«","oΝtH_"]


groups_key_list = ["Gr1(`|EξΥE»ΜΌ)","Gr2","Gr3","Gr4","Gr5(βEd₯EoΧ)","Gr5(βEd₯EoΧ)","Gr5(βEd₯EoΧ)",\
                    "Gr6(ΗnEΖn)","Gr6(ΗnEΖn)",\
                    "Gr7(»|nE_όnEπ|oΧn)","Gr7(»|nE_όnEπ|oΧn)","Gr7(»|nE_όnEπ|oΧn)","Gr7(»|nE_όnEπ|oΧn)","Gr7(»|nE_όnEπ|oΧn)"]
groups_info_list = ["Gr1","Gr2","Gr3","Gr4","Gr5(β)","Gr5(d₯)","Gr5(oΧ)",\
                    "Gr6(Ηn)","Gr6(Ζn)","Gr7(»|nEΗn)","Gr7(»|nEΖn)","Gr7(_όnEΗn)","Gr7(_όnEΖn)","Gr7(π|oΧnEΖn)"
                    ]


        
def make_starting_asset_merge_df(starting_relation_merge_path):
    starting_asset_merge_df = pd.read_excel(starting_relation_merge_path,sheet_name="N_Yκ",header=1)
    starting_asset_merge_df.fillna("",inplace=True)
    
    return starting_asset_merge_df
    

def output_starting_asset_list_group(starting_asset_merge_df,gr_base_info,title):
    
    
    all_starting_asset_set = set()
    
    for test_id,test_num,job_id,onbatch,gr_info in zip(starting_asset_merge_df["TEST_ID"],starting_asset_merge_df["ΐs"],starting_asset_merge_df["ΐsJOB"],starting_asset_merge_df["ONBAT"],starting_asset_merge_df["Groupͺή(JSIπ)"]):
        
        if gr_info.startswith("~"): #or gr_info.startswith("7"):
            continue
        
        if "(" not in gr_info:
            print("Group info format is not matched {},{},{},{}".format(test_id,job_id,onbatch,gr_info))
            continue
        
        gr_lis = gr_info[:gr_info.find("(")].split("E")
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
        
        
    file_name = "N_ξρ_"+gr_base_info+"_"+dt_now+".xlsx"
    out_title = os.path.join(title,gr_name)
    
    if os.path.isdir(out_title) == False:
        os.makedirs(out_title)
        
    write_excel_multi_sheet3(file_name,[sorted(all_starting_asset_set)],["TEST_ΐ{PΚ"],out_title,[all_starting_asset_header])
        

def main(starting_relation_merge_path,title):
      
    starting_asset_merge_df = make_starting_asset_merge_df(starting_relation_merge_path)
    

    for gr_info in groups_info_list:
        output_starting_asset_list_group(starting_asset_merge_df,gr_info,title)
    
            
    
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])
 