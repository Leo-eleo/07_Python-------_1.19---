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

dt_now = str(datetime.date.today())



groups_list = ["Gr1(�`�|�E��ՁE���̑�)","Gr1(�`�|)","Gr1(���)","Gr1(���̑�)","Gr2","Gr3","Gr4","Gr5(�≄�E�d���E�o��)","Gr5(�≄)","Gr5(�d��)","Gr5(�o��)",\
                "Gr6(�Ǘ��n�E���ƌn)","Gr6(�Ǘ��n)","Gr6(���ƌn)",\
                "Gr7(���|�n�E�_���n�E���|�o�׌n)","Gr7(���|�n)","Gr7(���|�n�E�Ǘ��n)","Gr7(���|�n�E���ƌn)","Gr7(�_���n)","Gr7(�_���n�E�Ǘ��n)","Gr7(�_���n�E���ƌn)","Gr7(���|�o�׌n)","Gr7(���|�o�׌n�E�Ǘ��n)","Gr7(���|�o�׌n�E���ƌn)"
]
same_modules = ["�R�C��","�X���u","�`�|","�v��","�ގ�","�M��","�M�d"]
same_modules_group = ["Gr6","Gr6","Gr1","Gr6","Gr3","Gr6","Gr6"]
len_groups = len(groups_list)
all_starting_asset_header = ["TEST_ID","���s����","���sJOB","�⑫","�o�̓t�H���_"]


groups_key_list = ["Gr1(�`�|�E��ՁE���̑�)","Gr2","Gr3","Gr4","Gr5(�≄�E�d���E�o��)","Gr5(�≄�E�d���E�o��)","Gr5(�≄�E�d���E�o��)",\
                    "Gr6(�Ǘ��n�E���ƌn)","Gr6(�Ǘ��n�E���ƌn)",\
                    "Gr7(���|�n�E�_���n�E���|�o�׌n)","Gr7(���|�n�E�_���n�E���|�o�׌n)","Gr7(���|�n�E�_���n�E���|�o�׌n)","Gr7(���|�n�E�_���n�E���|�o�׌n)","Gr7(���|�n�E�_���n�E���|�o�׌n)"]
groups_info_list = ["Gr1","Gr2","Gr3","Gr4","Gr5(�≄)","Gr5(�d��)","Gr5(�o��)",\
                    "Gr6(�Ǘ��n)","Gr6(���ƌn)","Gr7(���|�n�E�Ǘ��n)","Gr7(���|�n�E���ƌn)","Gr7(�_���n�E�Ǘ��n)","Gr7(�_���n�E���ƌn)","Gr7(���|�o�׌n�E���ƌn)"
                    ]




screen_asset_header = ["KEY2","���C�u����","�\�[�X�Ǘ����@","�{�ԍ��@1","�{�ԍ��@2","�{�ԍ��@3","���W���[��ID",\
                    "���Y��̏�","���Y����(ACN)","���Y�v��(��������)","CVT�v��(��������)","JSI���Y�L������","���Y���p�V�X�e��",\
                    "Gr1(�`�|�E��ՁE���̑�)","Gr1(�`�|)","Gr1(���)","Gr1(���̑�)","Gr2","Gr3","Gr4","Gr5(�≄�E�d���E�o��)","Gr5(�≄)","Gr5(�d��)","Gr5(�o��)",\
                    "Gr6(�Ǘ��n�E���ƌn)","Gr6(�Ǘ��n)","Gr6(���ƌn)",\
                    "Gr7(���|�n�E�_���n�E���|�o�׌n)","Gr7(���|�n)","Gr7(���|�n�E�Ǘ��n)","Gr7(���|�n�E���ƌn)","Gr7(�_���n)","Gr7(�_���n�E�Ǘ��n)","Gr7(�_���n�E���ƌn)","Gr7(���|�o�׌n)","Gr7(���|�o�׌n�E�Ǘ��n)","Gr7(���|�o�׌n�E���ƌn)", \
                    "���{�ꖼ��","���o��JCL","�o�^�җp���YID�����K��","�o�^�җp���YID"]

revival_asset_header = ["�����N�_","�֘A���Y","���Y����","�\�[�X��","���l�@\n���[�h���C�u����","���l�A\n���s��","���l�B\n�L�����Y����","�u�֘A���Y�v��\n�����v��","���f���R"]

related_asset_header = ["�����N�_","�֘A���Y","���Y����","�I���o�b�`����","���l�@","���l�A","���l�B"]

starting_asset_merge_header = ["�֘A���Y","���Y����","�N�_���Y=��\n���p���Y=��","�I���o�b�`����"]

asset_inventory_header = ["KEY2","���C�u����","�\�[�X�Ǘ����@","�{�ԍ��@1","�{�ԍ��@2","�{�ԍ��@3","���W���[��ID","���Y��̏�","���Y����(ACN)","���Y�v��(��������)","JSI���Y�L������","CVT�v��(��������)","���Y���p�V�X�e��",\
                          "Gr1(�`�|�E��ՁE���̑�)","Gr1(�`�|)","Gr1(���)","Gr1(���̑�)","Gr2","Gr3","Gr4","Gr5(�≄�E�d���E�o��)","Gr5(�≄)","Gr5(�d��)","Gr5(�o��)",\
                          "Gr6(�Ǘ��n�E���ƌn)","Gr6(�Ǘ��n)","Gr6(���ƌn)",\
                          "Gr7(���|�n�E�_���n�E���|�o�׌n)","Gr7(���|�n)","Gr7(���|�n�E�Ǘ��n)","Gr7(���|�n�E���ƌn)","Gr7(�_���n)","Gr7(�_���n�E�Ǘ��n)","Gr7(�_���n�E���ƌn)","Gr7(���|�o�׌n)","Gr7(���|�o�׌n�E�Ǘ��n)","Gr7(���|�o�׌n�E���ƌn)", \
                          "���{�ꖼ��","���o��JCL","�o�^�җp���YID�����K��","�o�^�җp���YID","�o�b�`���Y","�I�����C�����Y","�I������","�I������(�O��)","���p����","�o�b�`����","�I�����C������",\
                          "�������Y","��ʒǉ��ڍs�Ώێ��Y(�o�b�`���p)","��ʒǉ��ڍs�Ώێ��Y(�I�����C�����p)"]

group_all_use = ["��"]*len_groups
group_all_empty = [""]*len_groups


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


def get_df_revival_asset(setting_file_path,gr_info):
    sheet_name = "�������Y_" + gr_info
    
    try:
        df_revival = pd.read_excel(setting_file_path,sheet_name=sheet_name)
        df_revival = df_revival[revival_asset_header]
        df_revival.fillna("",inplace=True)
    except:
        print("Error there is no sheet of {} for revival asset.".format(sheet_name))
        df_revival = pd.DataFrame([])
        
    return df_revival

    
def make_inventory_template(asset_inventory_template_path):
    inventory_template_df = pd.read_excel(asset_inventory_template_path,sheet_name="�I���p���Y�ꗗ",header=0)
    inventory_template_df.fillna("",inplace=True)
    
    inventory_id_matching_dic = {}
    inventory_key_matching_dic = {}
    
    for i,(key,inventory_id) in enumerate(zip(inventory_template_df["KEY2"],inventory_template_df["�o�^�җp���YID"])):
        if inventory_id not in inventory_id_matching_dic:
            inventory_id_matching_dic[inventory_id] = []
            
        inventory_id_matching_dic[inventory_id].append(i)
        
        if key not in inventory_key_matching_dic:
            inventory_key_matching_dic[key] = []
            
        inventory_key_matching_dic[key].append(i)
        
    return inventory_template_df,inventory_id_matching_dic,inventory_key_matching_dic
    
    
def make_screen_asset_and_judge_from_member_list(member_list_path):
    
    df_member_list = pd.read_excel(member_list_path,sheet_name="�����o�ꗗ�}�[�W��",header=1)
    df_member_list.fillna("", inplace=True)
    
    screen_asset_list = []  
    
    screen_asset_info_list = screen_asset_header[:-3]

    ### �����o�ꗗ����擾������
    for i in range(len(df_member_list)):
        data = df_member_list.iloc[i]
        
        # asset_key,asset_module = data["KEY2"],data["���W���[��ID"]
        
        asset_type,asset_valid = data["���Y����(ACN)"],data["JSI���Y�L������"]
    
        if asset_valid == "":
            continue
        
        if asset_type not in ("PSAM��`�i��ʁFFMTGEN�j","PSAM��`�i��ʁFMEDGEN�j"):
            continue
        
            
        screen_list_row = [data[key] for key in screen_asset_info_list]
        screen_list_row.extend(["","�����o�ꗗ���W���[��ID��",data["���W���[��ID"]])
        screen_asset_list.append(screen_list_row)
        
    return screen_asset_list
        


def make_relations_group_and_adl_definition_list(base_path,gr_info):
    
    adl_definition_dic = {}
    search_path = os.path.join(base_path)
    folder_files = glob_files(search_path)
    
    for file_path in folder_files:
        if "�ڋq��_���Y�֘A�����" not in file_path or gr_info not in file_path:
            continue
        relations_group_df = pd.read_excel(file_path,sheet_name="�ڋq��_���Y�֘A�����")
        relations_group_df.fillna("",inplace=True)
        
        for source_from,relation,source_to in zip(relations_group_df["�ďo�����Y"],relations_group_df["�ďo���@"],relations_group_df["�ďo�掑�Y"]):
 
            if "�t�@�C����" in relation:
                if source_from not in adl_definition_dic:
                    adl_definition_dic[source_from] = set()
                adl_definition_dic[source_from].add(source_to)    
 
        relations_group_df = relations_group_df[relations_group_df["�b�薳��FLG"] != "��"]
        return relations_group_df,adl_definition_dic
    
    
    print("Error, there is no file of relations on {} in {}".format(gr_info,base_path))
    return pd.DataFrame([]),[]


def make_relations_group_starting_point(starting_point_merge_path,gr_base_info):
    starting_asset_set = set()
    
    df_starting_list = pd.read_excel(starting_point_merge_path,sheet_name="�N�_���Y�ꗗ",header=1)
    df_starting_list.fillna("",inplace=True)
    for starting_asset,onbatch,gr_info in zip(df_starting_list["���sJOB"],df_starting_list["ONBAT"],df_starting_list["Group����(JSI��)"]):
        if gr_info.startswith("�~"):
            continue
        if "(" not in gr_info:
            print("Group info format is not matched {},{},{}".format(starting_asset,onbatch,gr_info))
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
                
            starting_asset_set.add((starting_asset,onbatch))
    df_starting_relation = pd.read_excel(starting_point_merge_path,sheet_name="�N�_���Y�֘A��",header=1)
    df_starting_relation.fillna("",inplace=True)
    for source_to,gr_info in zip(df_starting_relation["�ďo�掑�Y"],df_starting_relation["Group����(JSI��)"]):
        if gr_info.startswith("�~"):
            continue
        if "(" not in gr_info:
            print("Group info format is not matched {},{},{}".format(starting_asset,onbatch,gr_info))
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
                
            starting_asset_set.add((source_to,"ON"))
    return starting_asset_set
    


def make_received_asset_dic(base_path,gr_info):
    
    if "Gr5" in gr_info:
        gr_info = "Gr5"
    if "Gr6" in gr_info:
        gr_info = "Gr6"
    if "Gr7" in gr_info:
        gr_info = "Gr7"
        
    search_path = os.path.join(base_path)
    
    folder_files = glob_files(search_path)
    
    for file_path in folder_files:
        if "��̎��Y�ꗗ" not in file_path or gr_info not in file_path:
            continue
        
        df_received_asset = pd.read_excel(file_path,sheet_name="��̎��Y�ꗗ_TOOL���͗p")
        df_received_asset.fillna("",inplace=True)
        
        received_asset_dic = {}
        for i in range(len(df_received_asset)):
            data = df_received_asset.iloc[i].to_list()
            source = data[0]
            if source not in received_asset_dic:
                received_asset_dic[source] = set()
            
            
            received_asset_dic[source].add(tuple(data[1:]))
        
        return received_asset_dic

    print("Error, there is no info of received asset of {} in {}.".format(gr_info,base_path))
    return {}



def make_starting_asset_df(base_path,gr_info):

    search_path = os.path.join(base_path)
    
    folder_files = glob_files(search_path)
    
    for file_path in folder_files:
        if "�N�_���" not in file_path or gr_info not in file_path:
            continue
        
        df_received_asset = pd.read_excel(file_path,sheet_name="TEST_���{�P��")
        df_received_asset.fillna("",inplace=True)
        
        return df_received_asset

    print("Error, there is no info of starting asset of {} in {}.".format(gr_info,base_path))
    return pd.DataFrame([])

def make_starting_asset_merge(related_asset_all,starting_asset_set,gr_info):
    starting_asset_merge = set()
    for i in range(len(related_asset_all)):
        asset,asset_type,onbatch = related_asset_all[i][1:4]
        starting_asset_check = "��"
        
        if (asset,onbatch) in starting_asset_set:
            starting_asset_check = "��"
            
        starting_asset_merge.add((asset,asset_type,starting_asset_check,onbatch))
        
    return sorted(starting_asset_merge)
    

def make_additional_screen_related_asset(screen_asset_list,gr_key,gr_info,asset_all_used_gr_set):
    
    if "Gr5" in gr_info:
        gr_key = gr_info
    if "Gr6" in gr_info:
        gr_key = gr_info
    if "Gr7" in gr_info:
        gr_key = gr_info
    
    if gr_key in screen_asset_header:
        gind = screen_asset_header.index(gr_key)
    else:
        gind = -1
    if gind == -1:
        print("Error group info is not found in this received asset folder")
        return 
    screen_asset_starting_point = set()
    
    additional_screen_asset_list = []
    
    for data in screen_asset_list:
        if data[gind] == "":
            continue
        if data[-1] in asset_all_used_gr_set:
            continue
        screen_asset_starting_point.add((data[0],1,data[-1],"ON",""))
        additional_screen_asset_list.append(data)
        
    screen_asset_starting_point = pd.DataFrame(screen_asset_starting_point,columns=all_starting_asset_header)

    return additional_screen_asset_list,screen_asset_starting_point
    
    
def make_search_graph(df):
    
    
    asset_set = set() ### �ďo�� or �ďo�� �̎��Y�ꗗ���d���������č쐬����

    relation_list = set() ### �ڋq��_���Y�֘A����񂩂�֘A���̈ꗗ���d���������Ď擾����

    for fr,relation_type,to,received in zip(df["�ďo�����Y"],df["�ďo���@"],df["�ďo�掑�Y"],df["��̔���"]):
        fr_true = check_module_name(fr)
        asset_set.add(fr_true)
        
        asset_set.add(to)
        relation_list.add((fr,relation_type,to,received))
      

    asset_set = sorted(asset_set)
    relation_list = sorted(relation_list)

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
    for i,(fr,_,to,_) in enumerate(relation_list):
        fr_true = check_module_name(fr)
        find = name_dic[fr_true]
        tind = name_dic[to]
        relation_graph[find].append((tind,i))
        
    return relation_graph,relation_list,name_dic,rev_name_dic,n


def search_related_asset(starting_asset_df,relation_graph,relation_list,name_dic,rev_name_dic,n):
    
    ### �e�X�g���{�P�ʂ��珇�ԂɊ֘A���Y���쐬����
    ### �����̓O���t�ɑ΂��� ���D��T��(BFS = Bred First Search) ��{�I�̓A���S���Y���Ȃ̂ŕK�v������Ό������Ă݂�Ɨǂ��ł��B
    
    visited_id = [-1]*n
    visited_id_batch = [-1]*n
    related_asset = set()
    for i,(test_id,source,info) in enumerate(zip(starting_asset_df["TEST_ID"],starting_asset_df["���sJOB"],starting_asset_df["�⑫"])):
        ### source = �N�_���Y�����Y�֘A�����̌ďo���A�ďo��ɂ��Ȃ��ꍇ�� �ϊ��\�� name_dic[source] �ŃA�N�Z�X����ƃG���[�ɂȂ邽�� (�z��O�Q�Ƃ̂悤�Ȃ���)�A�ŏ��ɏ�������
        
        if source not in name_dic:
            related_asset.add((test_id,source,info))
            continue
        sind = name_dic[source]
        q = deque([sind])
        q_batch = deque([])
        related_asset.add((test_id,source,info))
        visited_id[sind] = i

        while q:
            now = q.pop()
        
            for nex,nind in relation_graph[now]:
                
                if visited_id[nex] == i:
                    continue
                visited_id[nex] = i
 
                received = relation_list[nind][3]
                info_tmp = info
                if received == "JCL":
                    info_tmp = "BAT"
                nname = rev_name_dic[nex]

                related_asset.add((test_id,nname,info_tmp))
                if received == "JCL" and info != info_tmp:
                    q_batch.append(nex)
                else:
                    q.append(nex)
        
        info_tmp = "BAT"
        while q_batch:
            now = q_batch.pop()
        
            for nex,nind in relation_graph[now]:
                
                if visited_id_batch[nex] == i:
                    continue
                visited_id_batch[nex] = i
 
                received = relation_list[nind][3]
                nname = rev_name_dic[nex]

                related_asset.add((test_id,nname,info_tmp))
                q_batch.append(nex)
                

    return related_asset


def make_matching_related_asset_with_received_list(all_related_asset,received_asset_dic):
    
    related_asset_with_type_list = []
    for test_id,asset,info in all_related_asset:
        if asset not in received_asset_dic:
            related_asset_with_type_list.append([test_id,asset,"",info,"","",""])
            continue
        
        for data in received_asset_dic[asset]:
            new_list = [test_id,asset,"",info]
            new_list[2] = data[0]
            new_list += data[1:]
            related_asset_with_type_list.append(new_list)
                
    return related_asset_with_type_list

   
def make_asset_inventory_group(inventory_template_df,inventory_id_matching_dic,inventory_key_matching_dic,additional_screen_asset_list_all,starting_asset_merge_list,df_revival_asset,gr_info,adl_definition_dic,old_inventory_path):
    
    asset_inventory_group = inventory_template_df.values.tolist()
    
    batch_index = asset_inventory_header.index("�o�b�`���Y")
    online_index = asset_inventory_header.index("�I�����C�����Y")
    asset_inventory_before_index = asset_inventory_header.index("�I������(�O��)")
    
    ### �O��̒I�����Y�ꗗ�̏����X�V
    inventory_asset_folder_path = os.path.join(old_inventory_path)
    inventory_asset_folder_files = glob_files(inventory_asset_folder_path)
    
    file_name = ""
    for invntory_asset_file in inventory_asset_folder_files:
        if gr_info not in invntory_asset_file or "�I���p���Y�ꗗ" not in invntory_asset_file:
            continue
        file_name = invntory_asset_file
        
    if file_name == "":
        print("There is no file of path asset inventory of {}.".format(gr_info))
    else:
        inventory_asset_before_df = pd.read_excel(file_name,sheet_name="�I���p���Y�ꗗ",header=0)
        inventory_asset_before_df.fillna("",inplace=True)
        inventory_asset_before_keys = inventory_asset_before_df.columns.tolist()

        for i in range(len(inventory_asset_before_df)):
            data = inventory_asset_before_df.iloc[i]
            key,is_batch_asset,is_online_asset = data["KEY2"],data["�o�b�`���Y"],data["�I�����C�����Y"]
            if "�I������" in inventory_asset_before_keys:
                judge_inventory = data["�I������"]
            else:
                judge_inventory = ""
            if key not in inventory_key_matching_dic:
                continue
  
            for ind in inventory_key_matching_dic[key]:
                asset_inventory_group[ind][batch_index] = is_batch_asset
                asset_inventory_group[ind][online_index] = is_online_asset
                asset_inventory_group[ind][asset_inventory_before_index] = judge_inventory
    
    
    judge_used_index = asset_inventory_header.index("���p����")
    batch_asset_index = asset_inventory_header.index("�o�b�`����")
    online_asset_index = asset_inventory_header.index("�I�����C������")
    
    batch_asset_screen_index = asset_inventory_header.index("��ʒǉ��ڍs�Ώێ��Y(�o�b�`���p)")
    online_asset_screen_index = asset_inventory_header.index("��ʒǉ��ڍs�Ώێ��Y(�I�����C�����p)")
    
    
    ### ��ʒǉ��ڍs�Ώێ��Y����̊֘A���Y�̃I���o�b�`���̍X�V
    for screen_asset_list in additional_screen_asset_list_all:
        asset = screen_asset_list[1]
        onbatch = screen_asset_list[3]
        
        if asset not in inventory_id_matching_dic:
            continue
        
        if onbatch == "ON":
            for ind in inventory_id_matching_dic[asset]:
                asset_inventory_group[ind][online_asset_screen_index] = "��"
                asset_inventory_group[ind][judge_used_index] = "��"
                asset_inventory_group[ind][online_asset_index] = "��"
        elif onbatch == "BAT":
            for ind in inventory_id_matching_dic[asset]:
                asset_inventory_group[ind][batch_asset_screen_index] = "��"
                asset_inventory_group[ind][judge_used_index] = "��"
                asset_inventory_group[ind][batch_asset_index] = "��"
                
    ### �N�_���Y�}�[�W�V�[�g����̊֘A���Y�̃I���o�b�`���̍X�V
    for asset_list in starting_asset_merge_list:
        asset = asset_list[0]
        starting_asset_check = asset_list[2]
        onbatch = asset_list[3]
        
        if asset not in inventory_id_matching_dic:
            continue
        
        for ind in inventory_id_matching_dic[asset]:
            if asset_inventory_group[ind][judge_used_index] != "��":
                asset_inventory_group[ind][judge_used_index] = starting_asset_check
                
            if onbatch == "ON":
                if asset_inventory_group[ind][online_asset_index] != "��":
                    asset_inventory_group[ind][online_asset_index] = starting_asset_check
                    
            elif onbatch == "BAT":
                if asset_inventory_group[ind][batch_asset_index] != "��":
                    asset_inventory_group[ind][batch_asset_index] = starting_asset_check
      
      
    ### �������Y�̏��̍X�V              
    revival_index = asset_inventory_header.index("�������Y")
    
    for revival_list in df_revival_asset:
        asset = revival_list[1]
        
        if asset in inventory_id_matching_dic:
            for ind in inventory_id_matching_dic[asset]:
                asset_inventory_group[ind][revival_index] = "��"
                if asset_inventory_group[ind][judge_used_index] != "��":
                    asset_inventory_group[ind][judge_used_index] = "��"
            
        elif asset in adl_definition_dic:
            for asset_name in adl_definition_dic[asset]:
                if asset_name in inventory_id_matching_dic:
                    for ind in inventory_id_matching_dic[asset_name]:
                        asset_inventory_group[ind][revival_index] = "��"
                        if asset_inventory_group[ind][judge_used_index] != "��":
                            asset_inventory_group[ind][judge_used_index] = "��"
                
    
    asset_inventory_index = asset_inventory_header.index("�I������")
    
    asset_system_index = asset_inventory_header.index("���Y���p�V�X�e��")
    asset_need_index = asset_inventory_header.index("���Y�v��(��������)")
    asset_source_index = asset_inventory_header.index("���Y����(ACN)")
    
    if gr_info in asset_inventory_header:
        gr_key_index = asset_inventory_header.index(gr_info)
    else:
        if gr_info != "Gr1":
            print("Error group info is something wrong at {}".format(gr_info))
        else:
            gr_key_index = asset_inventory_header.index("Gr1(�`�|)")
            
            
    for i in range(len(asset_inventory_group)):
        if asset_inventory_group[i][judge_used_index] == "":
            continue
        
        if asset_inventory_group[i][batch_asset_index] != "":
            asset_inventory_group[i][batch_index] = "��"
    
        if asset_inventory_group[i][online_asset_index] != "":
            asset_inventory_group[i][online_index] = "��"
            
        system_info = asset_inventory_group[i][asset_system_index]
        need_info = asset_inventory_group[i][asset_need_index]
        source_info = asset_inventory_group[i][asset_source_index]
        
        if system_info == "26) ���" or system_info == "":
            asset_inventory_group[i][asset_inventory_index] = "�~ ���Y���p�V�X�e��: �� or ���"
            continue
        
        if need_info == "�p�~��" or need_info == "�ΏۊO":
            asset_inventory_group[i][asset_inventory_index] = "�~ ���Y�v��: �p�~�� or �ΏۊO"
            continue
        
        if source_info == "�x�m��Utility�E�x�m�ʒ񋟃c�[��":
            asset_inventory_group[i][asset_inventory_index] = "�~ ���Y����: �A�g�ΏۊO���Y"
            continue
        
        if asset_inventory_group[i][gr_key_index] == "":
            asset_inventory_group[i][asset_inventory_index] = "�~ Gr����: ��Gr���莑�Y"
            continue
        
        asset_inventory_group[i][asset_inventory_index] = "��"
        
        
    return asset_inventory_group

    
def output_asset_inventory_group(inventory_template_df,inventory_id_matching_dic,inventory_key_matching_dic,screen_asset_list,starting_point_merge_path,base_path,setting_file_path,gr_key,gr_info,title,old_inventory_path):
    
    ### �֘A������ADL��`�̏����擾����
    relations_group_df,adl_definition_dic = make_relations_group_and_adl_definition_list(base_path,gr_info)
    
    ### �N�_���Y�ƂȂ�ID�̈ꗗ���擾����
    starting_asset_set = make_relations_group_starting_point(starting_point_merge_path,gr_info)
    
    ### ��̎��Y�ꗗ�̏����擾����
    received_asset_dic = make_received_asset_dic(base_path,gr_info)
      
    ### �ڋq��_���Y�֘A����񂩂�O���t���쐬����
    relation_graph,relation_list,name_dic,rev_name_dic,n = make_search_graph(relations_group_df)
    
    ### Gr�ł̋N�_�ꗗ���擾
    starting_asset_df = make_starting_asset_df(base_path,gr_info)
    
    ### �N�_�ꗗ����̊֘A���Y���擾
    all_related_asset = search_related_asset(starting_asset_df,relation_graph,relation_list,name_dic,rev_name_dic,n)
    
    ### ��̎��Y�ꗗ�ƃ}�b�`���O�����֘A���Y�ꗗ���擾
    related_asset_with_received_info = make_matching_related_asset_with_received_list(all_related_asset,received_asset_dic)
    
    ### �N�_���Y�}�[�W�V�[�g�p�̏����擾
    starting_asset_merge_list = make_starting_asset_merge(related_asset_with_received_info,starting_asset_set,gr_info)
    
    ### �ǉ��Ώۉ�ʎ��Y����̏����擾
    asset_all_used_gr_set = set([lis[1] for lis in related_asset_with_received_info])
    
    additional_screen_asset_list,screen_asset_starting_point = make_additional_screen_related_asset(screen_asset_list,gr_key,gr_info,asset_all_used_gr_set)
    
    additional_screen_related_asset = search_related_asset(screen_asset_starting_point,relation_graph,relation_list,name_dic,rev_name_dic,n)
    
    additional_screen_related_asset_with_received_info = make_matching_related_asset_with_received_list(additional_screen_related_asset,received_asset_dic)
    
    ### �������Y�̏����擾
    df_revival_asset = get_df_revival_asset(setting_file_path,gr_info)
    df_revival_asset = df_revival_asset.values.tolist()
    
    
    asset_inventory_gr = make_asset_inventory_group(inventory_template_df,inventory_id_matching_dic,inventory_key_matching_dic,additional_screen_related_asset_with_received_info,starting_asset_merge_list,df_revival_asset,gr_info,adl_definition_dic,old_inventory_path)  
    
    gr_name = gr_info
    if "Gr5" in gr_name:
        gr_name = "Gr5"
    if "Gr6" in gr_name:
        gr_name = "Gr6"
    if "Gr7" in gr_name:
        gr_name = "Gr7"
        
    file_name = "�I���p���Y�ꗗ_"+gr_info+"_"+dt_now+".xlsx"
    out_title = os.path.join(title,gr_name)
    
    if os.path.isdir(out_title) == False:
        os.makedirs(out_title)
        
    write_excel_multi_sheet(file_name,[asset_inventory_gr,additional_screen_asset_list,additional_screen_related_asset_with_received_info,df_revival_asset,starting_asset_merge_list,related_asset_with_received_info],["�I���p���Y�ꗗ","�ǉ��ڍs�Ώۉ��","�ǉ��ڍs�Ώۉ�ʂ���̊֘A���Y�ꗗ","�������Y","�N�_���Y�}�[�W","�֘A���Y�ꗗ"],out_title,[asset_inventory_header,screen_asset_header,related_asset_header,revival_asset_header,starting_asset_merge_header,related_asset_header])

 
def main(member_list_path, starting_point_merge_path,setting_file_path, asset_inventory_template_path,base_path,old_inventory_path,title):

    if os.path.isdir(title) == False:
        os.makedirs(title)        
    
    inventory_template_df,inventory_id_matching_dic,inventory_key_matching_dic = make_inventory_template(asset_inventory_template_path)
    screen_asset_list = make_screen_asset_and_judge_from_member_list(member_list_path)

    base_path_files = glob_files(base_path)
    
    for file_path in base_path_files:
        if "�N�_���" not in file_path:
            continue
        
        gr_info = file_path.split("_")[1]
        gr_key = groups_key_list[groups_info_list.index(gr_info)]
        print("{}�̒I���p���Y�ꗗ�̍쐬���J�n���܂��B".format(gr_info))
        output_asset_inventory_group(inventory_template_df,inventory_id_matching_dic,inventory_key_matching_dic,screen_asset_list,starting_point_merge_path,base_path,setting_file_path,gr_key,gr_info,title,old_inventory_path)
          
if __name__ == "__main__":

    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7])
    
    ### ����1 DBPath ����2 �o�̓t�H���_ 