#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

import pandas as pd
import re
import datetime


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

dt_now = str(datetime.date.today())

received_asset_set_headers = ["���YID","���Y����","���C�u����","�\�[�X�Ǘ����@","JSI���Y�L������","KEY2","���W���[��ID","���{�ꖼ��", \
                              "Gr1(�`�|�E��ՁE���̑�)","Gr1(�`�|)","Gr1(���)","Gr1(���̑�)","Gr2","Gr3","Gr4","Gr5(�≄�E�d���E�o��)","Gr5(�≄)","Gr5(�d��)","Gr5(�o��)",\
                              "Gr6(�Ǘ��n�E���ƌn)","Gr6(�Ǘ��n)","Gr6(���ƌn)",\
                              "Gr7(���|�n�E�_���n�E���|�o�׌n)","Gr7(���|�n)","Gr7(���|�n�E�Ǘ��n)","Gr7(���|�n�E���ƌn)","Gr7(�_���n)","Gr7(�_���n�E�Ǘ��n)","Gr7(�_���n�E���ƌn)","Gr7(���|�o�׌n)","Gr7(���|�o�׌n�E�Ǘ��n)","Gr7(���|�o�׌n�E���ƌn)",
                              "���l","�I����͖����K��","���o��JCL","ToDoNo.120��","���ޕs�v"]

received_asset_summary_headers = ["���YID","���Y����","���l�@\n���[�h���C�u����","���l�A\n���s��","���l�B\n�L�����Y����"]

get_from_member_list_keys = received_asset_set_headers[2:32]
le_member_keys = len(get_from_member_list_keys)

groups_list = ["Gr1(�`�|�E��ՁE���̑�)","Gr1(�`�|)","Gr1(���)","Gr1(���̑�)","Gr2","Gr3","Gr4","Gr5(�≄�E�d���E�o��)","Gr5(�≄)","Gr5(�d��)","Gr5(�o��)",\
                "Gr6(�Ǘ��n�E���ƌn)","Gr6(�Ǘ��n)","Gr6(���ƌn)",\
                "Gr7(���|�n�E�_���n�E���|�o�׌n)","Gr7(���|�n)","Gr7(���|�n�E�Ǘ��n)","Gr7(���|�n�E���ƌn)","Gr7(�_���n)","Gr7(�_���n�E�Ǘ��n)","Gr7(�_���n�E���ƌn)","Gr7(���|�o�׌n)","Gr7(���|�o�׌n�E�Ǘ��n)","Gr7(���|�o�׌n�E���ƌn)"
]

asset_type_get_from_keys = ["JCL","PED","Easy�p�����^","�J�^�v��","DAM�X�L�[�}��`","DB�X�L�[�}��`","DB�T�u�X�L�[�}��`"]

asset_type_get_from_modules = ["COBOL","Fortran","PLI","PSAM��`�i��ʁFFMTGEN�j","PSAM��`�i��ʁFMEDGEN�j",\
                               "�A�Z���u��","AIM���iMSF�j","AIM���iMUKF�j","AIM���iR-LDF�j","AIM���iW-LDF�j","AIM���iXRF�j",\
                               "Focus�p�����^","PSAM��`�i�I�����C�����[�j","PSAM��`�i�o�b�`���[�j","PSAM��`�i���[�FFMTGEN�j",
                               "�I�����C�����iLD�j","�v���O�������iMQN�j","MED��`�i��ʁj"]

received_asset_summary_all_group = set()

def get_jcl_name_from_inner_proc(inner_proc_name:str):
    """
    �����J�^�v�������璊�o��JCL�̏����擾����

    Args:
        inner_proc_name (str): �����J�^�v����

    Returns:
        str: ���o��JCL��
    """
    match=re.match("^(.+)(%[A-Z])%(.+)%(.+)$",inner_proc_name)
    if match :
        return match.group(1) + match.group(2) + "%" + match.group(3)       
    else:
        raise ValueError(f"�����J�^�v���̖����K���ɔ��������Y�����m���܂����B �����J�^�v����={inner_proc_name}")


def get_jcl_name_from_easy_extracted(easy_name:str):
    """
    EASY�����璊�o��JCL�̏����擾����

    Args:
        easy_name (str): easy��

    Returns:
        str: ���o��JCL��
    """
    match=re.match("^(.+)E\d\d\d$",easy_name)
    if match :
        return match.group(1)
    else:
        raise ValueError(f"EASY�̖����K���ɔ��������Y�����m���܂����B EASY��={easy_name}")
    
    
def get_relation_matching_template(df_relation_template):
    
    relation_matching_template_dic = {}
    
    for relaton_type,info,register_name in zip(df_relation_template["�ďo���@"],df_relation_template["�o�^�s"],df_relation_template["�o�^���Y����"]):
        relation_matching_template_dic[relaton_type] = [info,register_name]
        
    return relation_matching_template_dic


def get_asset_set_from_member_list(member_list_path,df_inner_proc_list,df_easy_list,df_utilities_list):
    
    df_member_list = pd.read_excel(member_list_path,sheet_name="�����o�ꗗ�}�[�W��",header=1)
    df_member_list.fillna("", inplace=True)
    received_asset_member_list = []
    
    jcl_info_dic = {}

    ### �����o�ꗗ����擾������
    for i in range(len(df_member_list)):
        data = df_member_list.iloc[i]
        
        asset_type = data["���Y����(ACN)"]
        
        if asset_type == "JCL" or asset_type == "�J�^�v��":
            jcl_info_dic[data["KEY2"]] = data
        if asset_type not in asset_type_get_from_keys and asset_type not in asset_type_get_from_modules:
            continue
        
        if asset_type in asset_type_get_from_keys:
            asset_key = data["KEY2"]
            name_rule = "�����o�ꗗKEY2��"
        elif asset_type in asset_type_get_from_modules:
            asset_key = data["���W���[��ID"]
            name_rule = "�����o�ꗗ���W���[��ID��"

        
        received_asset_row = [asset_key,asset_type] + [data[key] for key in get_from_member_list_keys] 
        
        received_asset_row.extend(["�����o�ꗗ���擾",name_rule,"","",""])
        received_asset_member_list.append(received_asset_row)
        
        
    ### �����J�^�v���ꗗ����擾������
    for inner_proc_name in df_inner_proc_list["�����J�^�v���ꗗ"]:
        jcl_name = get_jcl_name_from_inner_proc(inner_proc_name)
        
        if jcl_name not in jcl_info_dic:
            print("Error this internal proc info is not found in members list {}".format(inner_proc_name))
            continue
        
        asset_type = "�����J�^�v��"
        asset_key = inner_proc_name
        data = jcl_info_dic[jcl_name]
        received_asset_row = [asset_key,asset_type] + [data[key] for key in get_from_member_list_keys] 
        
        received_asset_row.extend(["�����J�^�v�����Y���擾","",jcl_name,"",""])
        received_asset_member_list.append(received_asset_row)
        
    
    ### EASY�ꗗ����擾������    
    for easy_name in df_easy_list["EASY_JCL���o��_�ꗗ"]:
        jcl_name = get_jcl_name_from_easy_extracted(easy_name)
        
        if jcl_name not in jcl_info_dic:
            print("Error this extracted easy info is not found in members list {}".format(easy_name))
            received_asset_row = [easy_name,"EASY_JCL���o��"] + [""]*le_member_keys 
        
            received_asset_row.extend(["EASY���Y���擾","",jcl_name,"",""])
            received_asset_member_list.append(received_asset_row)
            continue
        
        asset_type = "EASY_JCL���o��"
        asset_key = easy_name
        data = jcl_info_dic[jcl_name]
        received_asset_row = [asset_key,asset_type] + [data[key] for key in get_from_member_list_keys] 
        
        received_asset_row.extend(["EASY���Y���擾","",jcl_name,"",""])
        received_asset_member_list.append(received_asset_row)
        
        
    ### Utility����擾������
    for asset_key,asset_type in zip(df_utilities_list["���YID"],df_utilities_list["���Y����"]):
        received_asset_row = [asset_key,asset_type] + [""]*le_member_keys
        
        received_asset_row.extend(["TODONo.120�N��","","","",""])
        received_asset_member_list.append(received_asset_row)
        
        
    return received_asset_member_list
        
        
def get_asset_set_from_relation_merge(relation_merge_path,relation_matching_template):
    
    df_relation_merge = pd.read_excel(relation_merge_path,sheet_name=None)
    received_asset_set_groups = []
    
    sheet_names = df_relation_merge.keys()
    for sheet_name in sheet_names:
        if "���Y�֘A����������" not in sheet_name:
            continue
        
        df_relation_sheet = df_relation_merge[sheet_name]
        df_relation_sheet.fillna("",inplace=True)
        for i in range(len(df_relation_sheet)):
            data = df_relation_sheet.iloc[i]
            
            relation_type = data["�Ăяo�����@"]
    
            if relation_type not in relation_matching_template:
                continue
            
            asset_from,asset_type = relation_matching_template[relation_type]
            
            if asset_from == "�ďo��":
                asset_key = data["�ďo�����Y�i�����o�̂݁j"]
            elif asset_from == "�ďo��":
                asset_key = data["�Ăяo���掑�Y"]
                
            if data["���ޕs�v"] == "��":
                no_need = "��"
            else:
                no_need = ""
                
            received_asset_row = [asset_key,asset_type] + [""]*6 + [data[key] for key in groups_list]
                 
            received_asset_row.extend(["���Y�֘A���������ʂ��쐬","","","",no_need])
            
            received_asset_set_groups.append(received_asset_row)
    
    return received_asset_set_groups
    

            
def make_received_asset_file(received_asset_set_common,received_asset_group,group_prefix,title):
    
    global received_asset_summary_all_group
    
    received_asset_summary_dic = {}
    
    for received_asset_row in received_asset_set_common+received_asset_group:
        asset_key = received_asset_row[0]
        asset_value = received_asset_row[1:5]
        
        if asset_key not in received_asset_summary_dic:
            received_asset_summary_dic[asset_key] = []
        received_asset_summary_dic[asset_key].append(asset_value)
        
        
    received_asset_summary_list = []
    
    for asset_key,asset_value in received_asset_summary_dic.items():
        asset_type = "\n".join(sorted(set([value[0] for value in asset_value])))
        if len(asset_value) > 1:
            received_asset_row = [asset_key,asset_type,"����","����","����"]
        else:
            received_asset_row = [asset_key] + asset_value[0]
            
        received_asset_summary_list.append(received_asset_row)
        received_asset_summary_all_group.add(tuple(received_asset_row))
        
        
    file_name = "��̎��Y�ꗗ_"+group_prefix+"_"+dt_now+".xlsx"
    out_title = os.path.join(title,group_prefix)
    
    if os.path.isdir(out_title) == False:
        os.makedirs(out_title)
        
    write_excel_multi_sheet3(file_name,[received_asset_set_common+received_asset_group,received_asset_summary_list],["��̎��Y�ꗗ","��̎��Y�ꗗ_TOOL���͗p"],out_title,[received_asset_set_headers,received_asset_summary_headers])
        
    
def main(member_list_path,relation_merge_path,received_asset_make_template_path,title):
    
    global received_asset_summary_all_group
    
    df_received_asset_template = pd.read_excel(received_asset_make_template_path,sheet_name=None)
    
    df_relation_template = df_received_asset_template["���Y�֘A���������ʃ}�b�s���O"]
    df_inner_proc_list = df_received_asset_template["�����J�^�v���ꗗ"]
    df_easy_list = df_received_asset_template["EASY�ꗗ"]
    df_utilities_list = df_received_asset_template["Utility�Q"]
    
    
    relation_matching_template = get_relation_matching_template(df_relation_template)
    
    received_asset_set_common = get_asset_set_from_member_list(member_list_path,df_inner_proc_list,df_easy_list,df_utilities_list)
    
    received_asset_set_groups = get_asset_set_from_relation_merge(relation_merge_path,relation_matching_template)
    
    
    for group in range(1,8):
        
        group_prefix = "Gr" + str(group)
        
        received_asset_group = []
        
        for received_asset_row in received_asset_set_groups:
            
            use_in_this_group = False
            sind = 8 ### Gr1(�`�|�E��ՁE���̑�) �̏�񂪋L�ڂ���Ă����index
            
            for i in range(len(groups_list)):
                if (received_asset_set_headers[sind+i].startswith(group_prefix) and received_asset_row[sind+i] == "��") or received_asset_row[-1] == "��":
                    use_in_this_group = True
                    break
                
            if use_in_this_group == True:
                received_asset_group.append(received_asset_row)
        
        make_received_asset_file(received_asset_set_common,received_asset_group,group_prefix,title)
    
    
    file_name = "��̎��Y�ꗗ_�}�[�W��_"+dt_now+".xlsx"
    out_title = os.path.join(title)
    
    if os.path.isdir(out_title) == False:
        os.makedirs(out_title)
        
    write_excel_multi_sheet3(file_name,[sorted(received_asset_summary_all_group)],["��̎��Y�ꗗ_TOOL���͗p"],out_title,[received_asset_summary_headers])
        
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])