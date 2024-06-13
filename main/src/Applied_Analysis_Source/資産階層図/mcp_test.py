#!/usr/bin/env python
# -*- coding: cp932 -*-
import sys
import os
import pyodbc
import pandas as pd
import datetime

from collections import deque

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


members_list_key = ["KEY2","���W���[��ID","���Y����(ACN)","���Y�v��(��������)","���Y���p�V�X�e��","Gr1(�`�|�E��ՁE���̑�)","Gr1(�`�|)","Gr1(���)","Gr1(���̑�)","Gr2","Gr3","Gr4","Gr5(�≄�E�d���E�o��)","Gr5(�≄)","Gr5(�d��)","Gr5(�o��)","Gr6","Gr7"]

not_found_info = ["�}�b�`������Ȃ�"]*len(members_list_key)
related_asset_key = ["�����N�_","�֘A���Y","���Y����","�I���o�b�`����","���l�@","���l�A","���l�B"]
    
def make_member_list_dic(member_list_path):
    member_list_df = pd.read_excel(member_list_path,sheet_name="�����o�ꗗ�}�[�W��",header=1)
    member_list_key_dic = {}
    members_list_module_dic = {}
    
    member_list_df.fillna("",inplace=True)
    for i in range(len(member_list_df)):
        data = member_list_df.iloc[i]
        key,module = data["KEY2"],data["���W���[��ID"]

        info_lis = [data[key] for key in members_list_key]
        
        if module not in members_list_module_dic:
            members_list_module_dic[module] = []
        members_list_module_dic[module].append(info_lis)
        
        if key in member_list_key_dic:
            print(key,"error")
        member_list_key_dic[key] = info_lis
        
    return member_list_key_dic,members_list_module_dic


def make_mcp_relatad_info(file,member_list_key_dic,members_list_module_dic):
    
    new_folder,new_file = os.path.split(file)
    new_file = new_file.replace("���p_�e�X�g�֘A���Y�o��","MCP�֘A���Y���")
    
    new_line = []
    
    base_df = pd.read_excel(file)
    base_df.fillna("",inplace=True)
    for i in range(len(base_df)):
        data = base_df.iloc[i]
        line = [data[key] for key in related_asset_key]
        key = line[1]
        
        if key in member_list_key_dic:
            line.extend(member_list_key_dic[key])
            new_line.append(line)
            continue
        
        if key in members_list_module_dic:
            for info in members_list_module_dic[key]:
                temp_line = line + info
                new_line.append(temp_line)
        
        else:
            line.extend(not_found_info)
            new_line.append(line)
    
    write_excel_multi_sheet5(new_file,[new_line],["MCP�֘A���Y"],new_folder,[related_asset_key+members_list_key])
    
def main(base_file_path,member_list_path):
    print("here")
    member_list_key_dic,members_list_module_dic = make_member_list_dic(member_list_path)
    
    files = glob_files(base_file_path)
    
    for file in files:
        if "���p_�e�X�g�֘A���Y�o��" not in file:
            continue
        print(file)
        make_mcp_relatad_info(file,member_list_key_dic,members_list_module_dic)
        
    


    
if __name__ == "__main__":

    main(sys.argv[1],sys.argv[2])
    
    ### ����1 DBPath ����2 �o�̓t�H���_ 