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


def make_relations_group(base_path,gr_info,exclude_flg):
    
   
    search_path = os.path.join(base_path)
    folder_files = glob_files(search_path)
    
    for file_path in folder_files:
        if "�ڋq��_���Y�֘A�����" not in file_path or gr_info not in file_path:
            continue
        relations_group_df = pd.read_excel(file_path,sheet_name="�ڋq��_���Y�֘A�����")
        relations_group_df.fillna("",inplace=True)
        
        if exclude_flg:
            relations_group_df = relations_group_df[relations_group_df["�b�薳��FLG"] != "��"]
        return relations_group_df
    
    
    print("Error, there is no file of relations on {} in {}".format(gr_info,base_path))
    return pd.DataFrame([]),[]



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

def output_related_asset_group(base_path,gr_key,gr_info,title,exclude_flg,file_path):
    
    ### �֘A������ADL��`�̏����擾����
    relations_group_df = make_relations_group(base_path,gr_info,exclude_flg)
    
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
    
    gr_name = gr_info
    if "Gr5" in gr_name:
        gr_name = "Gr5"
    if "Gr6" in gr_name:
        gr_name = "Gr6"
    if "Gr7" in gr_name:
        gr_name = "Gr7"
        
    file_suffix = os.path.split(file_path)[-1]
    file_suffix = file_suffix[file_suffix.index("_"):]
    file_name = "�֘A���Y�ꗗ"+file_suffix
    out_title = os.path.join(title,gr_name)
    
    if os.path.isdir(out_title) == False:
        os.makedirs(out_title)
        
    write_excel_multi_sheet(file_name,[related_asset_with_received_info],["�֘A���Y�ꗗ"],out_title,[related_asset_header])

 
def main(base_path,title,exclude_flg):
    if type(exclude_flg) == str:
        exclude_flg = exclude_flg == "True"
        
    if os.path.isdir(title) == False:
        os.makedirs(title)        
    
    base_path_files = glob_files(base_path)
    
    for file_path in base_path_files:
        if "�N�_���" not in file_path:
            continue

        gr_info = file_path.split("_")[-2]
        gr_key = groups_key_list[groups_info_list.index(gr_info)]
        print("{}�̊֘A���Y�ꗗ�̍쐬���J�n���܂��B".format(gr_info))
        output_related_asset_group(base_path,gr_key,gr_info,title,exclude_flg,file_path)
        
if __name__ == "__main__":

    main(sys.argv[1],sys.argv[2],sys.argv[3])
    
    ### ����1 DBPath ����2 �o�̓t�H���_ 