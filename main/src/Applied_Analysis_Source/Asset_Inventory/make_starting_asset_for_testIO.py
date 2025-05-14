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
    starting_asset_merge_df = starting_asset_merge_df[starting_asset_merge_df["���Y�v��(��������)"] != "�p�~��"]
    return starting_asset_merge_df
    
def make_starting_relations_merge_df(starting_relation_merge_path):
    starting_relation_merge_df = pd.read_excel(starting_relation_merge_path,sheet_name="�N�_���Y�֘A��",header=1)
    starting_relation_merge_df.fillna("",inplace=True)
    starting_relation_merge_df = starting_relation_merge_df[starting_relation_merge_df["�ďo���@"] == "MCP�N�_�ďo"]
    
    return starting_relation_merge_df

def starting_asset_list_group(starting_asset_merge_df,gr_base_info):
    
    
    all_starting_asset_set = set()
    
    if gr_base_info == "Gr1":
        gr_set_name = "Gr1(�`�|�E��ՁE���̑�)"
    else:
        gr_set_name = gr_base_info
    for test_id,test_num,job_id,onbatch,source_type,gr_info in zip(starting_asset_merge_df["TEST_ID"],starting_asset_merge_df["���s����"],starting_asset_merge_df["���sJOB"],starting_asset_merge_df["ONBAT"],starting_asset_merge_df["�N�_���Y���"],starting_asset_merge_df["Group����(JSI��)"]):
        
        if gr_info.startswith("�~"): #or gr_info.startswith("7"):
            continue
        
        if source_type not in ["FID","GFID","Online","WEB�nOnline","�I�����C��JOB"]:
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

            all_starting_asset_set.add((test_id,test_num,job_id,onbatch,gr_set_name))
    
    return all_starting_asset_set
        
def starting_asset_list_group_from_relation(starting_relation_merge_df,gr_base_info):
    
    
    all_starting_relation_set = set()
    
    if gr_base_info == "Gr1":
        gr_set_name = "Gr1(�`�|�E��ՁE���̑�)"
    else:
        gr_set_name = gr_base_info
    for job_id,gr_info in zip(starting_relation_merge_df["�ďo�掑�Y"],starting_relation_merge_df["Group����(JSI��)"]):
        
        if gr_info.startswith("�~"): #or gr_info.startswith("7"):
            continue
        
        if "(" not in gr_info:
            print("Group info format is not matched {},{}".format(job_id,gr_info))
            continue
        
        test_id = job_id + "_MCP"
        test_num = 1
        onbatch = "ON"
        
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

            all_starting_relation_set.add((test_id,test_num,job_id,onbatch,gr_set_name))
    
    return all_starting_relation_set

def starting_asset_batch_group(inventory_file_path):
    
    file_name = os.path.split(inventory_file_path)[-1]
    gr_base_info = file_name.split("_")[1]
    
    
    if gr_base_info == "Gr1":
        gr_set_name = "Gr1(�`�|�E��ՁE���̑�)"
    else:
        gr_set_name = gr_base_info
        
    starting_asset_batch_group_merge_df = pd.read_excel(inventory_file_path,sheet_name="�N�_���Y�}�[�W")
    starting_asset_batch_group_merge_df = starting_asset_batch_group_merge_df[starting_asset_batch_group_merge_df["���Y����"] == "JCL"]
    starting_asset_batch_group_merge_df.fillna("",inplace=True)
    
    starting_asset_batch_set = set([(job_id,1,job_id,onbatch,gr_set_name) for job_id,onbatch in zip(starting_asset_batch_group_merge_df["�֘A���Y"],starting_asset_batch_group_merge_df["�I���o�b�`����"])])
    
    return starting_asset_batch_set

def main(base_path,title):
      
    base_files = glob_files(base_path)
    
    for file in base_files:
        if "�N�_���Y�ꗗ" in file:
            starting_relation_merge_path = file
            
    
    ### �I�����C���̋N�_���Y�𒊏o
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
            
    
    file_name = "TEST���{�P��_�I�����C���֘A���Y_"+dt_now+".xlsx"
    out_title = os.path.join(title)
    
    if os.path.isdir(out_title) == False:
        os.makedirs(out_title)
        
    write_excel_multi_sheet3(file_name,[sorted(starting_relation_merge_set)],["TEST_���{�P��"],out_title,[all_starting_asset_header])
    
    file_name = "TEST���{�P��_�I�����C�����Y�K�w�}_"+dt_now+".xlsx"
    out_title = os.path.join(title)
    
    if os.path.isdir(out_title) == False:
        os.makedirs(out_title)
        
    write_excel_multi_sheet3(file_name,[sorted(starting_asset_merge_set | starting_relation_merge_set)],["TEST_���{�P��"],out_title,[all_starting_asset_header])
    
    ### �o�b�`�̋N�_���Y�𒊏o
    
    starting_asset_set_batch_all = set()
    for file in base_files:
        if "�I���p���Y�ꗗ" not in file:
            continue
        if "Template" in file:
            continue
        
        starting_asset_set_batch_group = starting_asset_batch_group(file)
        starting_asset_set_batch_all |= starting_asset_set_batch_group
        
        
    file_name = "TEST���{�P��_�o�b�`_"+dt_now+".xlsx"
    out_title = os.path.join(title)
    
    if os.path.isdir(out_title) == False:
        os.makedirs(out_title)
        
    write_excel_multi_sheet3(file_name,[sorted(starting_asset_set_batch_all)],["TEST_���{�P��"],out_title,[all_starting_asset_header])
    
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])
 