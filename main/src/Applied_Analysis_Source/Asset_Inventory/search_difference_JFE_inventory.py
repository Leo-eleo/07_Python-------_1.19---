#!/usr/bin/env python
# -*- coding: cp932 -*-
from hashlib import new
import sys
import os
import pyodbc
import pandas as pd
import datetime

from collections import deque

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

dt_now = str(datetime.date.today())



# groups_list = ["Gr1(�`�|�E��ՁE���̑�)","Gr1(�`�|)","Gr1(���)","Gr1(���̑�)","Gr2","Gr3","Gr4","Gr5(�≄�E�d���E�o��)","Gr5(�≄)","Gr5(�d��)","Gr5(�o��)","Gr6","Gr7"]

same_modules = ["�R�C��","�X���u","�`�|","�v��","�ގ�","�M��","�M�d"]
same_modules_group = ["Gr6","Gr6","Gr1","Gr6","Gr3","Gr6","Gr6"]
# len_groups = len(groups_list)
all_starting_asset_header = ["TEST_ID","���s����","���sJOB","�⑫","�o�̓t�H���_"]


groups_key_list = ["Gr1(�`�|�E��ՁE���̑�)","Gr2","Gr3","Gr4","Gr5(�≄�E�d���E�o��)","Gr5(�≄�E�d���E�o��)","Gr5(�≄�E�d���E�o��)",\
                    "Gr6(�Ǘ��n�E���ƌn)","Gr6(�Ǘ��n�E���ƌn)",\
                    "Gr7(���|�n�E�_���n�E���|�o�׌n)","Gr7(���|�n�E�_���n�E���|�o�׌n)","Gr7(���|�n�E�_���n�E���|�o�׌n)","Gr7(���|�n�E�_���n�E���|�o�׌n)","Gr7(���|�n�E�_���n�E���|�o�׌n)"]
groups_info_list = ["Gr1","Gr2","Gr3","Gr4","Gr5(�≄)","Gr5(�d��)","Gr5(�o��)",\
                    "Gr6(�Ǘ��n)","Gr6(���ƌn)","Gr7(���|�n�E�Ǘ��n)","Gr7(���|�n�E���ƌn)","Gr7(�_���n�E�Ǘ��n)","Gr7(�_���n�E���ƌn)","Gr7(���|�o�׌n�E���ƌn)"
                    ]


comparizon_header = ["KEY2","�o�^�җp���YID","���Y����(ACN)","���Y�v��(��������)","���Y���p�V�X�e��","���{�ꖼ��"]
# group_all_use = ["��"]*len_groups
# group_all_empty = [""]*len_groups


asset_id_index = 1 ### �o�^�җp���YID �� index
reasons_index = 6 ### �����̗��R���L�ڂ���index

name_dic = {}
rev_name_dic = {}
relation_graph = []
relation_group_info = {}
relation_list = {}
visited_id = []



def write_excel_multi_sheet(filename,dfs,sheet_names,path,output_headers):
    
    Sheet_lim = 10**6
    writer = pd.ExcelWriter(path+"/"+filename,engine='xlsxwriter')
    writer.book.use_zip64()
    sheet_name_list = []
    
    df_list = []
    output_header_list = []
    for df,header,sheet_name in zip(dfs,output_headers,sheet_names):
        M = len(df)
        for i in range(M//Sheet_lim+1):
            df_list.append(df[i*Sheet_lim:min(M,(i+1)*Sheet_lim)])
            output_header_list.append(header)
            if i == 0:
                sheet_name_list.append(sheet_name)
            else:
                sheet_name_list.append(sheet_name +"_" + str(i+1))
            
    for list,sheet_name,header in zip(df_list,sheet_name_list,output_header_list):
        df = pd.DataFrame(list,columns=header)
        df.to_excel(writer, sheet_name=sheet_name,index=False)
        
    writer._save()
    writer.close()
    
    
def check_module_name(name):
    for module in same_modules:
        if module in name:
            return name[:name.find(module)]
    
    return name        

def make_relations_group(base_path,gr_info):
    
    search_path = os.path.join(base_path)
    folder_files = glob_files(search_path)
    
    for file_path in folder_files:
        if "�ڋq��_���Y�֘A�����" not in file_path or gr_info not in file_path:
            continue
        relations_group_df = pd.read_excel(file_path,sheet_name="�ڋq��_���Y�֘A�����")
        relations_group_df.fillna("",inplace=True)
        relations_group_df = relations_group_df[relations_group_df["�b�薳��FLG"] != "��"]
        
        return relations_group_df
    
    print("Error, there is no file of relations on {} in {}".format(gr_info,base_path))
    return pd.DataFrame([])

    
def make_relation_merge_set(base_path):
    
    base_files = glob_files(base_path)
    relation_merge_set = set()
    for file in base_files:
        if "���Y�֘A���������ʃ}�[�W��" not in file:
            continue
        df_relation_merge = pd.read_excel(file,sheet_name=None)  
        df_sheet_list = df_relation_merge.keys()
        for sheetname in df_sheet_list:
            if "���Y�֘A����������" not in sheetname:
                continue
            df = df_relation_merge[sheetname]
            df.fillna("",inplace=True)
            for source_from,relation_type,source_to in zip(df["�ďo�����Y�i�����o�̂݁j"],df["�Ăяo�����@"],df["�Ăяo���掑�Y"]):
                relation_merge_set.add((source_from,relation_type,source_to))
            
    for file in base_files:
        if "�N�_���Y�ꗗ" not in file:
            continue
        df = pd.read_excel(file,sheet_name="�N�_���Y�֘A��",header=1)  
        df.fillna("",inplace=True)
        for source_from,relation_type,source_to in zip(df["�ďo�����Y�i�����o�̂݁j"],df["�ďo���@"],df["�ďo�掑�Y"]):
            relation_merge_set.add((source_from,relation_type,source_to))
       
    if relation_merge_set:
        return relation_merge_set

    print("Error, there is no file of merged relations in {}".format(base_path))
    return pd.DataFrame([])


def make_starting_asset(new_path,gr_info):

    search_path = os.path.join(new_path)
    
    folder_files = glob_files(search_path)
    
    for file_path in folder_files:
        if "�N�_���" not in file_path or gr_info not in file_path:
            continue
        
        df_received_asset = pd.read_excel(file_path,sheet_name="TEST_���{�P��")
        starting_asset = set([asset for asset in df_received_asset["���sJOB"]])
        return starting_asset

    print("Error, there is no info of starting asset of {} in {}.".format(gr_info,new_path))
    return set()
   
  
    
def make_search_graph(df):
    
    
    asset_set = set() ### �ďo�� or �ďo�� �̎��Y�ꗗ���d���������č쐬����

    relation_set = set() ### �ڋq��_���Y�֘A����񂩂�֘A���̈ꗗ���d���������Ď擾����

    for fr,relation_type,to in zip(df["�ďo�����Y"],df["�ďo���@"],df["�ďo�掑�Y"]):
        fr_true = check_module_name(fr)
        asset_set.add(fr_true)
        
        asset_set.add(to)
        relation_set.add((fr,relation_type,to))
      

    asset_set = sorted(asset_set)
    relation_list = sorted(relation_set)

    ### �O���t���쐬����ۂ� DXDAIKOU �̂悤�Ȗ��O�����ɂ����� DXDAIKOU = 1, JXDAIKOU = 2 �̂悤�ȑΉ��\������� �����ň�����悤�ɂ������������ɓ��삷�邽�� �ϊ��\�Ƌt�ϊ��\���쐬����

    ### �ϊ��\ name_dic["DXDAIKOU"] = 1 �̂悤�� ���O���琔�����擾�ł���
    name_dic = {s:i for i,s in enumerate(asset_set)} 

    ### �t�ϊ��\ rev_name_dic[1] = "DXDAIKOU" �̂悤�� �������疼�O���擾�ł��� �o�͂̍ۂ͖��O�ɖ߂��̂ł����Ŏg��
    rev_name_dic = {i:s for i,s in enumerate(asset_set)}

    ### �O���t�Ɍďo�����Y����ďo�掑�Y�Ɍ������ӂƂ��Ċ֘A���̏���ǉ�����
    ### �Ⴆ�� �֘A���� DXDAIKOU CALL JXDAIKOU ���������Ƃ���
    ### relation_graph[1] �̃��X�g�ɂ� JXDAIKOU�̐��� 2 �������� relation_graph[1] = [(2,xxx),(y,zzz)] �݂����ɂȂ��Ă��� 
    n = len(asset_set)
    relation_graph = [[] for i in range(n)]
    for i,(fr,_,to) in enumerate(relation_list):
        fr_true = check_module_name(fr)
        find = name_dic[fr_true]
        tind = name_dic[to]
        relation_graph[find].append((tind,i))
        
    return relation_graph,relation_list,relation_set,name_dic,rev_name_dic,n


def search_path_target_asset(starting_asset_list,target_set,relation_graph,relation_list,name_dic,rev_name_dic,n):
    
    ### �e�X�g���{�P�ʂ��珇�ԂɊ֘A���Y���쐬����
    ### �����̓O���t�ɑ΂��� ���D��T��(BFS = Bred First Search) ��{�I�̓A���S���Y���Ȃ̂ŕK�v������Ό������Ă݂�Ɨǂ��ł��B
    
    visited_id = [-1]*n
    path_par_id = [-1]*n
    target_path_dic = {}
    for i,source in enumerate(starting_asset_list):
        ### source = �N�_���Y�����Y�֘A�����̌ďo���A�ďo��ɂ��Ȃ��ꍇ�� �ϊ��\�� name_dic[source] �ŃA�N�Z�X����ƃG���[�ɂȂ邽�� (�z��O�Q�Ƃ̂悤�Ȃ���)�A�ŏ��ɏ�������
        
        if source not in name_dic:
            continue
        sind = name_dic[source]
        q = deque([sind])
        visited_id[sind] = i
        path_par_id[sind] = -1
        while q:
            now = q.popleft()
        
            for nex,nind in relation_graph[now]:
                
                if visited_id[nex] == i:
                    continue
                visited_id[nex] = i
                path_par_id[nex] = [now,nind]
              
                nname = rev_name_dic[nex]
                q.append(nex)
                
                if nname not in target_set:
                    continue
                
                target_set.remove(nname)
                
                target_path = []
                
                pos = nex
                while pos != sind:
                    npos,nind = path_par_id[pos]
                    target_path.append(relation_list[nind][:3])
                    pos = npos
                target_path = reversed(target_path)
                target_path_dic[nname] = target_path
        

    return target_path_dic


   
def make_exclude_set(base_path,gr_info):
    base_files = glob_files(base_path)
    for file in base_files:
        if "��̎��Y�ꗗ�쐬����_����" not in file:
            continue
        
        df_exclude_all = pd.read_excel(file,sheet_name=None)  
        df_sheet_list = df_exclude_all.keys()
        
        exclude_all = set(df_exclude_all["�^�p�nJCL_���S���O"]["���O���Y��"].values.tolist())
        exclude_to_source = set(df_exclude_all["���O���Y_Gr����"]["���O���Y��"].values.tolist())
        
        sheet_name = "���O���Y_" + gr_info
        if sheet_name in df_sheet_list:
            exclude_group = set(df_exclude_all[sheet_name]["���O���Y��"].values.tolist())
        else:
            exclude_group = set()
            
        return exclude_all|exclude_to_source|exclude_group
    
    return set()

 
def update_from_revival_asset(additions_asset,deletions_asset,new_revival_asset_list,old_revival_asset_list):
    
    new_revival_asset_set = set([revival_asset for revival_asset in new_revival_asset_list["�o�^�җp���YID"]])
    old_revival_asset_set = set([revival_asset for revival_asset in old_revival_asset_list["�o�^�җp���YID"]])

    additions_revival_asset = set()
    deletions_revival_asset = set()
    for asset in new_revival_asset_set:
        if asset not in old_revival_asset_set:
            additions_revival_asset.add(asset)
            
    for asset in old_revival_asset_set:
        if asset not in new_revival_asset_set:
            deletions_revival_asset.add(asset)
            
            
    for i in range(len(additions_asset)):
        if additions_asset[i][reasons_index] != "":
            continue
        if additions_asset[i][asset_id_index] in additions_revival_asset:
            additions_asset[i][reasons_index] = "�������Y�̒ǉ�"
            
    for i in range(len(deletions_asset)):
        if deletions_asset[i][reasons_index] != "":
            continue
        if deletions_asset[i][asset_id_index] in deletions_revival_asset:
            deletions_asset[i][reasons_index] = "�������Y�̍폜"
    
    return additions_asset,deletions_asset


def update_from_exclude_asset(additions_asset,deletions_asset,new_exclude_set,old_exclude_set):
    
    for i in range(len(additions_asset)):
        if additions_asset[i][reasons_index] != "":
            continue
        asset_id = additions_asset[i][asset_id_index]
        if asset_id in old_exclude_set and asset_id not in new_exclude_set:
            additions_asset[i][reasons_index] = "���O���Y�̍폜"
            
    for i in range(len(deletions_asset)):
        if deletions_asset[i][reasons_index] != "":
            continue
        asset_id = deletions_asset[i][asset_id_index]
        if asset_id in new_exclude_set and asset_id not in old_exclude_set:
            deletions_asset[i][reasons_index] = "���O���Y�̒ǉ�"
    
    return additions_asset,deletions_asset


def update_from_starting_asset(additions_asset,deletions_asset,new_starting_asset,old_starting_asset,new_additions_screen_asset,old_additions_screen_asset):
    
    new_all_asset = new_starting_asset | new_additions_screen_asset
    old_all_asset = old_starting_asset | old_additions_screen_asset
    for i in range(len(additions_asset)):
        if additions_asset[i][reasons_index] != "":
            continue
        asset_id = additions_asset[i][asset_id_index]
        if asset_id in new_starting_asset and asset_id not in old_all_asset:
            additions_asset[i][reasons_index] = "�N�_���Y�̒ǉ�"
            
        elif asset_id in new_additions_screen_asset and asset_id not in old_all_asset:
            additions_asset[i][reasons_index] = "�N�_���Y�̒ǉ�_�ǉ��ڍs�Ώۉ�ʎ��Y"
            
    for i in range(len(deletions_asset)):
        if deletions_asset[i][reasons_index] != "":
            continue
        asset_id = deletions_asset[i][asset_id_index]
        if asset_id in old_starting_asset and asset_id not in new_all_asset:
            deletions_asset[i][reasons_index] = "�N�_���Y�̍폜"
            
        elif asset_id in old_additions_screen_asset and asset_id not in new_all_asset:
            deletions_asset[i][reasons_index] = "�N�_���Y�̍폜_�ǉ��ڍs�Ώۉ�ʎ��Y"
    
    return additions_asset,deletions_asset

def update_from_related_asset(additions_asset,deletions_asset,new_starting_asset,old_starting_asset,new_additions_screen_asset,old_additions_screen_asset,new_relations_group_df,old_relations_group_df,new_relation_merge_set,old_relation_merge_set,new_exclude_set,old_exclude_set):
    
    ### �ڋq��_���Y�֘A����񂩂�O���t���쐬����
    new_relation_graph,new_relation_list,new_relation_set,new_name_dic,new_rev_name_dic,new_n = make_search_graph(new_relations_group_df)
    old_relation_graph,old_relation_list,old_relation_set,old_name_dic,old_rev_name_dic,old_n = make_search_graph(old_relations_group_df)
    
    new_starting_asset |= new_additions_screen_asset
    old_starting_asset |= old_additions_screen_asset
    
    additions_target = set()
    for i in range(len(additions_asset)):
        if additions_asset[i][reasons_index] != "":
            continue
        additions_target.add(additions_asset[i][asset_id_index])
        
    
    additions_path_dic = search_path_target_asset(new_starting_asset,additions_target,new_relation_graph,new_relation_list,new_name_dic,new_rev_name_dic,new_n)
    
    for i in range(len(additions_asset)):
        if additions_asset[i][reasons_index] != "":
            continue
        asset = additions_asset[i][asset_id_index]
        
        if asset not in additions_path_dic:
            additions_asset[i][reasons_index] = "�����s��"
            continue
        asset_relation_path = additions_path_dic[asset]

        for num,(source_from,relation_type,source_to) in enumerate(asset_relation_path):
            
            if num == 0 and source_from not in old_starting_asset:
                additions_asset[i][reasons_index] = "�N�_���Y�̒ǉ�: " + source_from
                break
            relation_tuple = (source_from,relation_type,source_to)
            if relation_tuple in old_relation_set:
                continue
            
            if source_from in old_exclude_set:
                additions_asset[i][reasons_index] = "���O���Y�̍폜�ɂ��֘A���̒ǉ�"+source_from+": " + source_from + "��" + source_to + " �֘A��=" + relation_type
                break
            
            if source_to in old_exclude_set: 
                additions_asset[i][reasons_index] = "���O���Y�̍폜�ɂ��֘A���̒ǉ�"+source_to+": " + source_from + "��" + source_to + " �֘A��=" + relation_type
                break
            
            if relation_tuple not in old_relation_merge_set:
                additions_asset[i][reasons_index] = "�֘A���̒ǉ�: " + source_from + "��" + source_to + " �֘A��=" + relation_type
                break 
            else:
                additions_asset[i][reasons_index] = "�����o�ꗗ�̍X�V�ɂ��֘A��Gr�̕ύX: " + source_from + "��" + source_to + " �֘A��=" + relation_type
                break
        if additions_asset[i][reasons_index] == "":
            additions_asset[i][reasons_index] = "�����s��"
    
    
    deletions_target = set()
    for i in range(len(deletions_asset)):
        if deletions_asset[i][reasons_index] != "":
            continue
        deletions_target.add(deletions_asset[i][asset_id_index])
        
    deletions_path_dic = search_path_target_asset(old_starting_asset,deletions_target,old_relation_graph,old_relation_list,old_name_dic,old_rev_name_dic,old_n)
    
    for i in range(len(deletions_asset)):
        if deletions_asset[i][reasons_index] != "":
            continue
        asset = deletions_asset[i][asset_id_index]
        
        if asset not in deletions_path_dic:
            deletions_asset[i][reasons_index] = "�����s��"
            continue
        
        asset_relation_path = deletions_path_dic[asset]
        
        
        for num,(source_from,relation_type,source_to) in enumerate(asset_relation_path):
            
            if num == 0 and source_from not in new_starting_asset:
                deletions_asset[i][reasons_index] = "�N�_���Y�̍폜: " + source_from
                break
            
            relation_tuple = (source_from,relation_type,source_to)
            if relation_tuple in new_relation_set:
                continue
            
            if source_from in new_exclude_set:
                deletions_asset[i][reasons_index] = "���O���Y�̒ǉ��ɂ��֘A���̍폜"+source_from+": " + source_from + "��" + source_to + " �֘A��=" + relation_type
                break
            
            if source_to in new_exclude_set: 
                deletions_asset[i][reasons_index] = "���O���Y�̒ǉ��ɂ��֘A���̍폜"+source_to+": " + source_from + "��" + source_to + " �֘A��=" + relation_type
                break
            
            if relation_tuple not in new_relation_merge_set:
                deletions_asset[i][reasons_index] = "�֘A���̍폜: " + source_from + "��" + source_to + " �֘A��=" + relation_type
                break 
            else:
                deletions_asset[i][reasons_index] = "�����o�ꗗ�̍X�V�ɂ��֘A��Gr�̕ύX: " + source_from + "��" + source_to + " �֘A��=" + relation_type
                break
        if deletions_asset[i][reasons_index] == "":
            deletions_asset[i][reasons_index] = "�����s��"
    
    return additions_asset,deletions_asset
def comparizon_asset_inventory_group(new_path,old_path,gr_key,gr_info,title,new_relation_merge_set,old_relation_merge_set):
    
    new_files = glob_files(new_path)
    old_files = glob_files(old_path)
    
    new_asset_inventory_df = []
    old_asset_inventory_df = []
    for new_file in new_files:
        if "�I���p���Y�ꗗ" not in new_file or gr_info not in new_file:
            continue
        
        new_asset_inventory_df = pd.read_excel(new_file,sheet_name=None)
        
    for old_file in old_files:
        if "�I���p���Y�ꗗ" not in old_file or gr_info not in old_file:
            continue
        
        old_asset_inventory_df = pd.read_excel(old_file,sheet_name=None)
    
    
    if old_asset_inventory_df == []:
        print("�I���p���Y�ꗗ {} �ɂ͌Â���� {} �ɑ��݂��Ȃ����߁A��r��͂��X�L�b�v���܂��B".format(gr_info,old_path))
        
        return 1
    
    
    new_asset_inventory_main = new_asset_inventory_df["�I���p���Y�ꗗ"]
    old_asset_inventory_main = old_asset_inventory_df["�I���p���Y�ꗗ"]
    
    new_asset_inventory_main.fillna("",inplace=True)
    old_asset_inventory_main.fillna("",inplace=True)
    
    new_asset_inventory_main_matching_dic = {new_asset_inventory_main.iloc[i]["KEY2"]:new_asset_inventory_main.iloc[i] for i in range(len(new_asset_inventory_main))}
    old_asset_inventory_main_all_set = set([old_asset_inventory_main.iloc[i]["KEY2"] for i in range(len(old_asset_inventory_main))])
    new_asset_inventory_used_asset_list = new_asset_inventory_main[new_asset_inventory_main["���p����"] != ""]
    old_asset_inventory_used_asset_list = old_asset_inventory_main[old_asset_inventory_main["���p����"] != ""]
    new_asset_inventory_used_asset_set = set([key for key in new_asset_inventory_used_asset_list["KEY2"]])
    old_asset_inventory_used_asset_set = set([key for key in old_asset_inventory_used_asset_list["KEY2"]])
    
    additions_asset = []
    deletions_asset = []
    
    for asset in new_asset_inventory_used_asset_set:
        if asset not in old_asset_inventory_used_asset_set:
            if asset not in old_asset_inventory_main_all_set:
                data = new_asset_inventory_main_matching_dic[asset]
                values = [data[key] for key in comparizon_header]
                values.extend(["�V�K��̎��Y",""])
                additions_asset.append(values)
            else:
                
                data = new_asset_inventory_main_matching_dic[asset]
                values = [data[key] for key in comparizon_header]
                values.extend(["",""])
                additions_asset.append(values)
            
    for asset in old_asset_inventory_used_asset_set:
        if asset not in new_asset_inventory_used_asset_set:
            if asset in new_asset_inventory_main_matching_dic:
                data = new_asset_inventory_main_matching_dic[asset]
                values = [data[key] for key in comparizon_header]
                values.extend(["",""])
            else:
                values = [asset,"�I���p���Y�ꗗ�ŐV�łɃf�[�^�Ȃ�","","","",""]
                values.extend(["",""])
            deletions_asset.append(values)
    
    
    
    new_revival_asset_list = new_asset_inventory_main[new_asset_inventory_main["�������Y"] == "��"]
    old_revival_asset_list = old_asset_inventory_main[old_asset_inventory_main["�������Y"] == "��"]
    
    additions_asset,deletions_asset = update_from_revival_asset(additions_asset,deletions_asset,new_revival_asset_list,old_revival_asset_list)
    
    new_exclude_set = make_exclude_set(new_path,gr_info)
    old_exclude_set = make_exclude_set(old_path,gr_info)
    additions_asset,deletions_asset = update_from_exclude_asset(additions_asset,deletions_asset,new_exclude_set,old_exclude_set)
    
    
    ### Gr�ł̋N�_�ꗗ���擾
    new_starting_asset = make_starting_asset(new_path,gr_info)
    old_starting_asset = make_starting_asset(old_path,gr_info)
    
    new_additions_screen_asset = new_asset_inventory_df["�ǉ��ڍs�Ώۉ��"]
    old_additions_screen_asset = old_asset_inventory_df["�ǉ��ڍs�Ώۉ��"]
    
    new_additions_screen_asset = set([asset_id for asset_id in new_additions_screen_asset["�o�^�җp���YID"]])
    old_additions_screen_asset = set([asset_id for asset_id in old_additions_screen_asset["�o�^�җp���YID"]])
    
    additions_asset,deletions_asset = update_from_starting_asset(additions_asset,deletions_asset,new_starting_asset,old_starting_asset,new_additions_screen_asset,old_additions_screen_asset)
    
    
    
    ### �֘A�������擾����
    new_relations_group_df = make_relations_group(new_path,gr_info)
    old_relations_group_df = make_relations_group(old_path,gr_info)
    
    additions_asset,deletions_asset = update_from_related_asset(additions_asset,deletions_asset,new_starting_asset,old_starting_asset,new_additions_screen_asset,old_additions_screen_asset,new_relations_group_df,old_relations_group_df,new_relation_merge_set,old_relation_merge_set,new_exclude_set,old_exclude_set)
    
      
    
    gr_name = gr_info
    if "Gr5" in gr_name:
        gr_name = "Gr5"
    if "Gr6" in gr_name:
        gr_name = "Gr6"
    if "Gr7" in gr_name:
        gr_name = "Gr7"
        
    file_name = "�I���������Y�ꗗ_"+gr_info+"_"+dt_now+".xlsx"
    out_title = os.path.join(title,gr_name)
    
    comp_header = comparizon_header + ["�ڍs����ϓ����R","�ڍs����ϓ����R�ڍ�"]
    if os.path.isdir(out_title) == False:
        os.makedirs(out_title)
        
    write_excel_multi_sheet(file_name,[additions_asset,deletions_asset],["�������Y�ꗗ","�������Y�ꗗ",],out_title,[comp_header,comp_header])
 
def main(new_path,old_path,title):

    if os.path.isdir(title) == False:
        os.makedirs(title)        
    
    
    new_relation_merge_set = make_relation_merge_set(new_path)
    
    old_relation_merge_set = make_relation_merge_set(old_path)
    
    new_path_files = glob_files(new_path)
    
    for file_path in new_path_files:
        if "�I���p���Y�ꗗ" not in file_path:
            continue
        
        gr_info = file_path.split("_")[1]
        gr_key = groups_key_list[groups_info_list.index(gr_info)]
        print("{}�̒I���������Y�ꗗ�̍쐬���J�n���܂��B".format(gr_info))
        comparizon_asset_inventory_group(new_path,old_path,gr_key,gr_info,title,new_relation_merge_set,old_relation_merge_set)
          
if __name__ == "__main__":

    main(sys.argv[1],sys.argv[2],sys.argv[3])
    
    ### ����1 DBPath ����2 �o�̓t�H���_ 