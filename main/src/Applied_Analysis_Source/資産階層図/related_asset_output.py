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



def main(db_name,title):
    
    print("start analysis")
    if os.path.isdir(title) == False:
        os.makedirs(title)
        
    conn = connect_accdb(db_name)
    cursor = conn.cursor()
    
    ### �ڋq��_���Y�֘A����񂩂�O���t���쐬����

    ### �ύX20191011
    sql =   """\
            SELECT * FROM �ڋq��_���Y�֘A�����
            """
            
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)

    asset_set = set() ### �ďo�� or �ďo�� �̎��Y�ꗗ���d���������č쐬����

    relation_list = set() ### �ڋq��_���Y�֘A����񂩂�֘A���̈ꗗ���d���������Ď擾����

    for fr,relation_type,to,received,valid_flg in zip(df["�ďo�����Y"],df["�ďo���@"],df["�ďo�掑�Y"],df["��̔���"],df["�b�薳��FLG"]):
        if valid_flg != "":
            continue    
        
        asset_set.add(fr)
        asset_set.add(to)
        relation_list.add((fr,relation_type,to,received,valid_flg))
        
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
    for i,(fr,relation,to,_,valid_flg) in enumerate(relation_list):
        find = name_dic[fr]
        tind = name_dic[to]
        
        ### �b�薳��FLG���󗓂Ȃ� valid_relation_flg = True
        ### ���j���[��ʂȂ� False �ŋN�_�̂Ƃ������L���ɂ��邽�߂� flg ������
        if valid_flg == "":
            valid_relation_flg = True
        else:
            valid_relation_flg = False
            
        #####
        
        relation_graph[find].append((tind,i,valid_relation_flg))
        
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

    ### �e�X�g���{�P�ʂ��珇�ԂɎ��Y�K�w�}���쐬����
    ### �����̓O���t�ɑ΂��� �[���D��T��(DFS = Depth First Search) ��{�I�̓A���S���Y���Ȃ̂ŕK�v������Ό������Ă݂�Ɨǂ��ł��B

    ans_list_all = []
    visited_id = [-1]*n
    visited_id_batch = [-1]*n
    
    add_info_set = set()
    ans_list_all_dic = {}
    for i,(test_id,source,info,out_folder) in enumerate(zip(df["TEST_ID"],df["���sJOB"],df["�⑫"],df["�o�̓t�H���_"])):
        ### source = �N�_���Y�����Y�֘A�����̌ďo���A�ďo��ɂ��Ȃ��ꍇ�� �ϊ��\�� name_dic[source] �ŃA�N�Z�X����ƃG���[�ɂȂ邽�� (�z��O�Q�Ƃ̂悤�Ȃ���)�A�ŏ��ɏ�������
        
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

        print(out_title,len(add_info_set))
        
        if os.path.isdir(out_title) == False:
            os.makedirs(out_title)
            
        # df = pd.DataFrame(list(add_info_set),columns=["�����N�_","�֘A���Y","�I���o�b�`����"])
        # table_name = "TEST_�����N�_�ʊ֘A���Y2_JFE"
        # cursor.executemany(
            # f"INSERT INTO [{table_name}] (�����N�_, �֘A���Y,�I���o�b�`����) VALUES (?, ?, ?)",
            # df.itertuples(index=False))

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
        write_excel_multi_sheet("���p_�e�X�g�֘A���Y�o��.xlsx",sorted(ans_list_all),"���p_�e�X�g�֘A���Y�o��",out_title,["�����N�_","�֘A���Y","���Y����","�I���o�b�`����","���l�@","���l�A","���l�B"])

    print("finish analysis")
    
if __name__ == "__main__":

    main(sys.argv[1],sys.argv[2])
    
    ### ����1 DBPath ����2 �o�̓t�H���_ 