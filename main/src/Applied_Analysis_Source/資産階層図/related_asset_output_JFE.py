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


groups_list = ["Gr1(�`�|�E��ՁE���̑�)","Gr1(�`�|)","Gr1(���)","Gr1(���̑�)","Gr2","Gr3","Gr4","Gr5(�≄�E�d���E�o��)","Gr5(�≄)","Gr5(�d��)","Gr5(�o��)","Gr6","Gr7"]

same_modules = ["�R�C��","�X���u","�`�|","�v��","�ގ�","�M��","�M�d"]
same_modules_group = ["Gr6","Gr6","Gr1","Gr6","Gr3","Gr6","Gr6"]
len_groups = len(groups_list)

group_all_use = ["��"]*len_groups
group_all_empty = [""]*len_groups



def check_module_name(name):
    for module in same_modules:
        if module in name:
            return name[:name.find(module)]
    
    return name    

# def make_member_module_list(setting_path):
    
#     df_members = pd.read_excel(setting_path,sheet_name="�����o�ꗗ")
#     df_members.fillna("",inplace=True)
#     members_dic = {}
#     key_dic = {}    
    
#     for x in range(len(df_members)):
#         data = df_members.iloc[x]
#         asset,module, = data["KEY2"],data["���W���[��ID"]
#         gr = [data[s] for s in groups_list]

#         asset = take_extensions(asset)
#         if module not in members_dic:
#             members_dic[module] = []
            
#         members_dic[module].append(gr)

#         if asset not in key_dic:
#             key_dic[asset] = []
#         key_dic[asset].append(gr)
    
#     return members_dic,key_dic


def make_relations_group(relations_merge_path):
    
    relations_group_info_dic = {}
    
    df_all = pd.read_excel(relations_merge_path,sheet_name=None)
    
    df_sheet_list = df_all.keys()
    
    for sheet in df_sheet_list:
        if "���Y�֘A����������" not in sheet:
            continue
        df = df_all[sheet]
        df.fillna("",inplace=True)
        
        for i in range(len(df)):
            data = df.iloc[i]
            
            relation_group_info = [data[gr] for gr in groups_list]
            source_from,relation,source_to = data["�ďo�����Y�i�����o�̂݁j"],data["�Ăяo�����@"],data["�Ăяo���掑�Y"]
            
            if (source_from,relation,source_to) not in relations_group_info_dic:
                relations_group_info_dic[(source_from,relation,source_to)] = group_all_empty[:]
                
            for j in range(len_groups):
                if relation_group_info[j] == "��":
                    relations_group_info_dic[(source_from,relation,source_to)][j] = "��"
    
    return relations_group_info_dic


def make_received_asset_dic(conn):
    
    sql = "SELECT * FROM �ڋq��_��̎��Y�ꗗ_�ėp��"
    df_received_asset = pd.read_sql(sql,conn)
    
    df_received_asset.fillna("",inplace=True)
    received_asset_dic = {}
    for i in range(len(df_received_asset)):
        data = df_received_asset.iloc[i].to_list()
        source = data[0]
        # source = data["���YID"]
        if source not in received_asset_dic:
            received_asset_dic[source] = set()
        
        
        received_asset_dic[source].add(tuple(data[1:]))
        
    return received_asset_dic


    
def main(db_name,title,relations_merge_path):
    

    if os.path.isdir(title) == False:
        os.makedirs(title)
        
    
    # members_dic,key_dic = make_member_module_list(setting_path)
    
    relations_group_info_dic = make_relations_group(relations_merge_path)
    conn = connect_accdb(db_name)
    cursor = conn.cursor()
    
    sql = "SELECT * FROM �ڋq��_��̎��Y�ꗗ_�ėp��"
    df_received_asset = pd.read_sql(sql,conn)
    
    df_received_asset.fillna("",inplace=True)
    received_asset_dic = {}
    for i in range(len(df_received_asset)):
        data = df_received_asset.iloc[i]
        source = data["���YID"]
        if source not in received_asset_dic:
            received_asset_dic[source] = set()
        
        received_asset_dic[source].add(data["���Y����"])
        
    ### �ڋq��_���Y�֘A����񂩂�O���t���쐬����

    ### �ύX20191011
    sql =   """\
            SELECT * FROM �ڋq��_���Y�֘A�����
            """
            
    
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)

    asset_set = set() ### �ďo�� or �ďo�� �̎��Y�ꗗ���d���������č쐬����

    relation_list = set() ### �ڋq��_���Y�֘A����񂩂�֘A���̈ꗗ���d���������Ď擾����

    for fr,relation_type,to,received,data_from,valid_flg in zip(df["�ďo�����Y"],df["�ďo���@"],df["�ďo�掑�Y"],df["��̔���"],df["�o�^����"],df["�b�薳��FLG"]):
        if valid_flg != "":
            continue
        
        fr_true = check_module_name(fr)
        asset_set.add(fr_true)
        
        asset_set.add(to)
        relation_list.add((fr,relation_type,to,received,valid_flg))
        
        if "�֘A����������" not in data_from and (to not in received_asset_dic or received not in received_asset_dic[to]):
            # print(fr,relation_type,to,received)
            if to not in received_asset_dic:
                received_asset_dic[to] = set()
            received_asset_dic[to].add(received)
            
            sql,values = make_insert_sql("�ڋq��_��̎��Y�ꗗ_�ėp��",[to,received],["���YID","���Y����"])
            cursor.execute(sql,values)
    

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
    relation_group_info = []
    for i,(fr,relation,to,_,valid_flg) in enumerate(relation_list):
        fr_true = check_module_name(fr)
        find = name_dic[fr_true]
        tind = name_dic[to]
        
        ### �b�薳��FLG���󗓂Ȃ� valid_relation_flg = True
        ### ���j���[��ʂȂ� False �ŋN�_�̂Ƃ������L���ɂ��邽�߂� flg ������
        if valid_flg == "":
            valid_relation_flg = True
        else:
            valid_relation_flg = False
            
        #####
            
        relation_graph[find].append((tind,i,valid_relation_flg))
        
        group_info_i = group_all_empty[:]
        
        if (fr,relation,to) in relations_group_info_dic:
            group_info_i = relations_group_info_dic[(fr,relation,to)]
            
        else:
            group_info_i = group_all_use[:]
            
            # if fr in members_dic:
            #     for gr_info in members_dic[fr]:
            #         for j in range(len_groups):
            #             if gr_info[j] == "��":
            #                 group_info_i[j] = "��"
                            
            # elif fr in key_dic:
            #     for gr_info in key_dic[fr]:
            #         for j in range(len_groups):
            #             if gr_info[j] == "��":
            #                 group_info_i[j] = "��"
            
            # elif fr != fr_true:
            #     for ind,module in enumerate(same_modules):
            #         if module in fr:
            #             sind = ind
            #             break
            #     for j in range(len_groups):
            #         if groups_list[j].startswith(same_modules_group[sind]):
            #             group_info_i[j] = "��"
            #     # print(fr,fr_true,group_info_i,same_modules_group[sind])
        
        if group_info_i[2] == "��" or group_info_i[3] == "��":
            group_info_i = group_all_use[:]
            
        for ind in range(len_groups):
            if group_info_i[ind] == "��":
                sgroup = groups_list[ind][:3]
                for j in range(len_groups):
                    if groups_list[j].startswith(sgroup):
                        group_info_i[j] = "��"
                    
       
        if "��" not in group_info_i:
            # print(fr,relation,to,_)
            group_info_i = group_all_use[:]
        # if group_info_i != group_info_i_old:
        #     print(fr,relation,to)
        #     print(group_info_i)
        #     print(group_info_i_old)
        

        relation_group_info.append(group_info_i)

    # �O���t�̊���
    ################################# 

    sql,_ = make_delete_sql("TEST_�����N�_�ʊ֘A���Y2_JFE",[],[])
    cursor.execute(sql)
    sql,_ = make_delete_sql("TEST_�����N�_�ʊ֘A���Y_JFE",[],[])
    cursor.execute(sql)
    
    ### �ύX20191011
    sql =   """\
            SELECT * FROM TEST_�e�X�g���{�P��_UNIQUE_JFE
            """
            
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)
    
    print("�O���t�̍쐬���������܂����B")

  
    ### �e�X�g���{�P�ʂ��珇�ԂɊ֘A���Y���쐬����
    ### �����̓O���t�ɑ΂��� �[���D��T��(DFS = Depth First Search) ��{�I�̓A���S���Y���Ȃ̂ŕK�v������Ό������Ă݂�Ɨǂ��ł��B

    ans_list_all = []
    visited_id = [-1]*n
    visited_id_batch = [-1]*n
    
    add_info_set = set()
    ans_list_all_dic = {}
    for i,(test_id,source,info,out_folder) in enumerate(zip(df["TEST_ID"],df["���sJOB"],df["�⑫"],df["�o�̓t�H���_"])):
        ### source = �N�_���Y�����Y�֘A�����̌ďo���A�ďo��ɂ��Ȃ��ꍇ�� �ϊ��\�� name_dic[source] �ŃA�N�Z�X����ƃG���[�ɂȂ邽�� (�z��O�Q�Ƃ̂悤�Ȃ���)�A�ŏ��ɏ�������
        
        if out_folder in groups_list:
            group_id = groups_list.index(out_folder)
        else:
            group_id = -1
        # print(out_folder,group_id)
            
            

        if out_folder != "":
            out_title = os.path.join(title,out_folder)
        else:
            out_title = title
        
        
        
        if out_title not in ans_list_all_dic:
            ans_list_all_dic[out_title] = set()
        add_info_set = ans_list_all_dic[out_title]
        
        if source not in name_dic:
            add_info_set.add((test_id,source,info))
            continue
        sind = name_dic[source]
        q = deque([sind])
        q_batch = deque([])
        
        add_info_set.add((test_id,source,info))
        visited_id[sind] = i

        # add_info_set.add((test_id,source,info))
        while q:
            now = q.pop()
        
            for nex,nind,valid_relation_flg in relation_graph[now]:
                
                if group_id != -1 and relation_group_info[nind][group_id] != "��":
                    continue
                
                if valid_relation_flg == False and now != sind:
                    continue
                
                if visited_id[nex] == i:
                    continue
                visited_id[nex] = i
 
                received = relation_list[nind][3]
                info_tmp = info
                if received == "JCL":
                    info_tmp = "BAT"
                nname = rev_name_dic[nex]

                add_info_set.add((test_id,nname,info_tmp))
                if received == "JCL" and info != info_tmp:
                    q_batch.append(nex)
                else:
                    q.append(nex)


        info_tmp = "BAT"
        while q_batch:
            now = q_batch.pop()
        
            for nex,nind,valid_relation_flg in relation_graph[now]:
                
                if group_id != -1 and relation_group_info[nind][group_id] != "��":
                    continue
                
                if valid_relation_flg == False and now != sind:
                    continue
                
                if visited_id_batch[nex] == i:
                    continue
                visited_id_batch[nex] = i
 
                received = relation_list[nind][3]
                nname = rev_name_dic[nex]

                add_info_set.add((test_id,nname,info_tmp))
                q_batch.append(nex)

    received_asset_dic = make_received_asset_dic(conn)
 


    for out_title in ans_list_all_dic.keys():
        add_info_set = ans_list_all_dic[out_title]
        out_name = os.path.split(out_title)[-1]
        print(out_title,len(add_info_set),out_name)
        if os.path.isdir(out_title) == False:
            os.makedirs(out_title)
            
        
        
            
        ans_list_all = []
        for test_id,asset,info in add_info_set:
            if asset not in received_asset_dic:
                ans_list_all.append([test_id,asset,"",info,"","",""])
                continue
            
            for data in received_asset_dic[asset]:
                new_list = [test_id,asset,"",info]
                new_list[2] = data[0]
                new_list += data[1:]
                ans_list_all.append(new_list)
                

        print(len(ans_list_all))
        write_excel_multi_sheet("���p_�e�X�g�֘A���Y�o��_" + out_name + ".xlsx",sorted(ans_list_all),"���p_�e�X�g�֘A���Y�o��",out_title,["�����N�_","�֘A���Y","���Y����","�I���o�b�`����","���l�@","���l�A","���l�B"])
    
    
if __name__ == "__main__":

    main(sys.argv[1],sys.argv[2],sys.argv[3])
    
    ### ����1 DBPath ����2 �o�̓t�H���_ 