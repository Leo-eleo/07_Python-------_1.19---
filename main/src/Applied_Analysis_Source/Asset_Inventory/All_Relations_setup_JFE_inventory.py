#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
import pandas as pd
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


dt_now = str(datetime.date.today())


all_relation_header = ["�ďo�����Y","�ďo���@","�ďo�掑�Y","��̔���","�b�薳��FLG","�ϐ���","�ďo��PARM","�o�^����"]

groups_key_list = ["Gr1(�`�|�E��ՁE���̑�)","Gr2","Gr3","Gr4","Gr5(�≄�E�d���E�o��)","Gr5(�≄�E�d���E�o��)","Gr5(�≄�E�d���E�o��)",\
                    "Gr6(�Ǘ��n�E���ƌn)","Gr6(�Ǘ��n�E���ƌn)",\
                    "Gr7(���|�n�E�_���n�E���|�o�׌n)","Gr7(���|�n�E�_���n�E���|�o�׌n)","Gr7(���|�n�E�_���n�E���|�o�׌n)","Gr7(���|�n�E�_���n�E���|�o�׌n)","Gr7(���|�n�E�_���n�E���|�o�׌n)"]
groups_info_list = ["Gr1","Gr2","Gr3","Gr4","Gr5(�≄)","Gr5(�d��)","Gr5(�o��)",\
                    "Gr6(�Ǘ��n)","Gr6(���ƌn)","Gr7(���|�n�E�Ǘ��n)","Gr7(���|�n�E���ƌn)","Gr7(�_���n�E�Ǘ��n)","Gr7(�_���n�E���ƌn)","Gr7(���|�o�׌n�E���ƌn)"
                    ]




def make_member_list(member_list_path):
    
    df_member_list = pd.read_excel(member_list_path,sheet_name="�����o�ꗗ�}�[�W��",header=1)
    df_member_list.fillna("", inplace=True)
    
    member_list_key_dic = {}
    member_list_module_dic = {}
    

    ### �����o�ꗗ����擾������
    for i in range(len(df_member_list)):
        data = df_member_list.iloc[i]
        
        asset_key,asset_module = data["KEY2"],data["���W���[��ID"]
        
        asset_type,asset_need = data["���Y����(ACN)"],data["���Y�v��(��������)"]
    
        if asset_key in member_list_key_dic:
            print("Error KEY2 = {} found multiple line in members list".format(asset_key))
            # print(member_list_key_dic[asset_key])
            new_library = data["�V���Ǘ����C�u������"]
            if new_library != "":
                member_list_key_dic[asset_key] = [asset_type,asset_need]
            # print(new_library,member_list_key_dic[asset_key])
        else:
            member_list_key_dic[asset_key] = [asset_type,asset_need]
            
        if asset_module not in member_list_module_dic:
            member_list_module_dic[asset_module] = [0,0]
            
        if asset_need in ("�p�~��","�ΏۊO"):
            member_list_module_dic[asset_module][0] += 1
        else:
            member_list_module_dic[asset_module][1] += 1
        
        
    return member_list_key_dic,member_list_module_dic


def make_relation_merge_df(excel_relation_merge_path):
    
    df_relation_merge = pd.read_excel(excel_relation_merge_path,sheet_name=None)  
    df_sheet_list = df_relation_merge.keys()

    relation_merge_df = []
    for sheetname in df_sheet_list:
        if "���Y�֘A����������" not in sheetname:
            continue
        df = df_relation_merge[sheetname]
        df.fillna("",inplace=True)
        relation_merge_df.append(df)
        
    return pd.concat(relation_merge_df)
        
def make_starting_relation_merge_df(starting_relation_merge_path):
    starting_relation_merge_df = pd.read_excel(starting_relation_merge_path,sheet_name="�N�_���Y�֘A��",header=1)
    starting_relation_merge_df.fillna("",inplace=True)
    
    return starting_relation_merge_df
    
def make_exclude_dic(setting_file_path):
    df_exclude_all = pd.read_excel(setting_file_path,sheet_name=None)  
    df_sheet_list = df_exclude_all.keys()
    
    exclude_all = set(df_exclude_all["�^�p�nJCL_���S���O"]["���O���Y��"].values.tolist())
    exclude_from_source = set()
    df_exclude = df_exclude_all["���O���Y_Gr����"]
    
    for asset,info in zip(df_exclude["���O���Y��"],df_exclude["�Q�Ə��"]):
        if info == "�a�����Ώ�JOB�l�b�g":
            exclude_all.add(asset)
        else:
            exclude_from_source.add(asset)
            
    exclude_group = {}
    for group in groups_info_list:
        sheet_name = "���O���Y_" + group
        if sheet_name in df_sheet_list:
            df_exclude = df_exclude_all[sheet_name]
            exclude_all_group = set()
            exclude_from_source_group = set()
            for asset,info in zip(df_exclude["���O���Y��"],df_exclude["�Q�Ə��"]):
                if info == "�a�����Ώ�JOB�l�b�g":
                    exclude_all_group.add(asset)
                else:
                    exclude_from_source_group.add(asset)
            
            exclude_group[group] = [exclude_all_group,exclude_from_source_group]
        else:
            exclude_group[group] = [[],[]]
            
    return exclude_all,exclude_from_source,exclude_group



def output_relation_list_group(relation_merge_df,starting_relation_merge_df,member_list_key_dic,member_list_module_dic,exclude_all,exclude_from_source,exclude_group,gr_key,gr_base_info,title):
    
    
    all_relation_set = set()
    
    df_group = relation_merge_df[(relation_merge_df[gr_key] == "��") | (relation_merge_df["���ޕs�v"] == "��")]
    for source,relation,to_source,asset_name,asset_need in zip(df_group["�ďo�����Y�i�����o�̂݁j"],df_group["�Ăяo�����@"],df_group["�Ăяo���掑�Y"],df_group["�֘A���L�ڎ��Y��"],df_group["���Y�v��"]):
                
        extract_flg = ""
        ### �^�p�nJCL_���S���O �̎��Y�����O
        if source in exclude_all or to_source in exclude_all:
            extract_flg = "��"
            
        ### �a�����Ώ�JOB�l�b�g �̎��Y�����O
        if source in exclude_group[0] or to_source in exclude_group[0]:
            extract_flg = "��"
        
        ### �w�菜�O���Y �̎��Y�����O
        if source in exclude_from_source or source in exclude_group[1]:
            extract_flg = "��"
        
        
        ### ��ʁ�PGM�ďo�ɂ����� MCP��`�̏��O
        if relation == "��ʁ�PGM�ďo":
            if asset_name in member_list_key_dic and member_list_key_dic[asset_name][0] == "ACS�iMCP��`�j" and asset_need in ("�p�~��","�ΏۊO"):
                extract_flg = "��"
            
        ### �����o�ꗗ�̔p�~��,�ΏۊO���Y�̏��O    
        if to_source in member_list_key_dic and member_list_key_dic[to_source][1] in ("�p�~��","�ΏۊO"):
            extract_flg = "��"
        
        if to_source in member_list_module_dic and (member_list_module_dic[to_source][0] > 0 and member_list_module_dic[to_source][1] == 0):
            extract_flg = "��"
            
        if (source,to_source,gr_base_info) == ("N2DAIKOU","KZ71FW00","Gr5(�o��)"):
            extract_flg = "��"
            
        if to_source in member_list_key_dic:
            source_type = member_list_key_dic[to_source][0]
        else:
            source_type = ""
            
        all_relation_set.add((source,relation,to_source,source_type,extract_flg,"","",""))
        
    for source,relation,to_source,gr_info in zip(starting_relation_merge_df["�ďo�����Y�i�����o�̂݁j"],starting_relation_merge_df["�ďo���@"],starting_relation_merge_df["�ďo�掑�Y"],starting_relation_merge_df["Group����(JSI��)"]):
        
        extract_flg = ""
        
        ### �^�p�nJCL_���S���O �̎��Y�����O
        if source in exclude_all or to_source in exclude_all:
            extract_flg = "��"
        
        ### �a�����Ώ�JOB�l�b�g �̎��Y�����O
        if source in exclude_group[0] or to_source in exclude_group[0]:
            extract_flg = "��"
        
        ### �w�菜�O���Y �̎��Y�����O
        if source in exclude_from_source or source in exclude_group[1]:
            extract_flg = "��"
        
        ### �����o�ꗗ�̔p�~��,�ΏۊO���Y�̏��O    
        if to_source in member_list_key_dic and member_list_key_dic[to_source][1] in ("�p�~��","�ΏۊO"):
            extract_flg = "��"
        
        if to_source in member_list_module_dic and (member_list_module_dic[to_source][0] > 0 and member_list_module_dic[to_source][1] == 0):
            extract_flg = "��"
    
        
        if gr_info.startswith("�~"):# or gr_info.startswith("7"):
            continue
        
        if "(" not in gr_info:
            print("Group info format is not matched {},{},{},{}".format(source,relation,to_source,gr_info))
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
                
            
            if to_source in member_list_key_dic:
                source_type = member_list_key_dic[to_source][0]
            else:
                source_type = ""
                
            all_relation_set.add((source,relation,to_source,source_type,extract_flg,"","",""))
            
    gr_name = gr_base_info
    if "Gr5" in gr_name:
        gr_name = "Gr5"
    if "Gr6" in gr_name:
        gr_name = "Gr6"
    if "Gr7" in gr_name:
        gr_name = "Gr7"
        
    file_name = "�ڋq��_���Y�֘A�����_"+gr_base_info+"_"+dt_now+".xlsx"
    out_title = os.path.join(title,gr_name)
    
    if os.path.isdir(out_title) == False:
        os.makedirs(out_title)
        
    write_excel_multi_sheet3(file_name,[sorted(all_relation_set)],["�ڋq��_���Y�֘A�����"],out_title,[all_relation_header])
        

def main(member_list_path,excel_relation_merge_path,starting_relation_merge_path,setting_file_path,title):
  
    exclude_all,exclude_from_source,exclude_group = make_exclude_dic(setting_file_path)

    member_list_key_dic,member_list_module_dic = make_member_list(member_list_path)
        
    relation_merge_df = make_relation_merge_df(excel_relation_merge_path)
    
    starting_relation_merge_df = make_starting_relation_merge_df(starting_relation_merge_path)
    
    for gr_key,gr_info in zip(groups_key_list,groups_info_list):
        output_relation_list_group(relation_merge_df,starting_relation_merge_df,member_list_key_dic,member_list_module_dic,exclude_all,exclude_from_source,exclude_group[gr_info],gr_key,gr_info,title)
    
            
    
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
 