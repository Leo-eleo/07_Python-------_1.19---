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


output_header = ["�e�X�gID","SEQ","�N�_����","�ďo�K�w","�ďo�S���Y","�ďo���@","�ďo���Y","���Y����"]


def write_excel_multi_sheet(filename,df_list,sheet_name_list,path,output_header=output_header):
    writer = pd.ExcelWriter(path+"/"+filename,engine='xlsxwriter')
    writer.book.use_zip64()
    # writer = pd.ExcelWriter(filename,engine='xlsxwriter')
    for list,sheet_name in zip(df_list,sheet_name_list):
        df = pd.DataFrame(list,columns=output_header)
        df.to_excel(writer, sheet_name=sheet_name,index=False)
        
    writer._save()
    writer.close()
    
def make_file_name(test_id,num,source):
    date = datetime.datetime.now()
    date = date.strftime('%y%m%d_%H%M%S')    
    
    filename = test_id + "_" + str(num).zfill(4) + "_" +source + "_" + date + ".xlsx"
    return filename


### 100�������ɕ�������
lim = 1000000
def create_output(test_id,num,source,ans_list,title):
    M = len(ans_list)
    lis = []
    for i in range(M//lim+1):
        lis.append(ans_list[i*lim:min(M,(i+1)*lim)])
        
    if lis[-1] == []:
        lis.pop()
    filename = make_file_name(test_id,num,source)
    sheet_names = []
    for i in range(len(lis)):
        if i == 0:
            sheet_names.append("���p_���Y�K�w�}")
        else:
            sheet_names.append("���p_���Y�K�w�}" + str(i+1))
    write_excel_multi_sheet(filename,lis,sheet_names,title)
    

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
        if "�֘A����������" not in sheet:
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

    
def main(db_name,title,relations_merge_path,output_separate="True",maxnum=2000000):
    

    M = int(maxnum) ### �����̍ő�l�@����𒴂�����~�߂�

    if os.path.isdir(title) == False:
        os.makedirs(title)
        
    if type(output_separate) != bool:
        output_separate = output_separate == "True"
          
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
        if valid_flg == "��":
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

    ### �ύX20191011
    sql =   """\
            SELECT * FROM TEST_�e�X�g���{�P��
            """
            
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)
    
    print("�O���t�̍쐬���������܂����B")

    ### �e�X�g���{�P�ʂ��珇�ԂɎ��Y�K�w�}���쐬����
    ### �����̓O���t�ɑ΂��� �[���D��T��(DFS = Depth First Search) ��{�I�̓A���S���Y���Ȃ̂ŕK�v������Ό������Ă݂�Ɨǂ��ł��B

    ans_list_all = []
    ans_list_all_dic = {}
  
    for i,(test_id,num,source,out_folder) in enumerate(zip(df["TEST_ID"],df["���s����"],df["���sJOB"],df["�o�̓t�H���_"])):
        ans_list = []

        if out_folder in groups_list:
            group_id = groups_list.index(out_folder)
        else:
            group_id = -1
            
        if out_folder != "":
            out_title = os.path.join(title,out_folder)
        else:
            out_title = title
            
        if os.path.isdir(out_title) == False:
            os.makedirs(out_title)
            
        if out_title not in ans_list_all_dic:
            ans_list_all_dic[out_title] = []
        
        ans_list_all = ans_list_all_dic[out_title]
        
         ### source = �N�_���Y�����Y�֘A�����̌ďo���A�ďo��ɂ��Ȃ��ꍇ�� �ϊ��\�� name_dic[source] �ŃA�N�Z�X����ƃG���[�ɂȂ邽�� (�z��O�Q�Ƃ̂悤�Ȃ���)�A�ŏ��ɏ�������
        if source not in name_dic or len(relation_graph[name_dic[source]]) == 0:
            ans_list.append([test_id,num,source,0,source+"(END)","","",""])
            if output_separate == True:
                create_output(test_id,num,source,ans_list,out_title)
            else:
                for lis in ans_list:
                    ans_list_all.append(lis)
            continue
        
        sind = name_dic[source]
        q = deque([[sind,str(sind).zfill(7),""]])
        
        ncount = 0 ### ���Y�K�w�}�̌����𐔂��� maxnum(default��200����) �𒴂���ƒ�������̂ň�U�ł��؂�
        
        while q:
            now,all_vis,all_relations = q.pop()
        
            for nex,nind,valid_relation_flg in relation_graph[now]:
                
                if group_id != -1 and relation_group_info[nind][group_id] != "��":
                    continue
                
                
                if valid_relation_flg == False and now != sind:
                    continue
                
                
                ### ���܂Ō����ďo�S�K�w�̏�񂪐����łœ����Ă��� 0000100&0004931&0999999 �̂悤�Ȋ���
                ### str(nex).zfill(7) �� 7���܂�0���߂����Ă���̂� �Ⴆ�ΐ��������̂܂� 100&4931&999990 �Ƃ��� 
                ### ���� 9 ������ƂȂ����Ƃ��ɂ� 9 �����̕�����Ɋ܂܂�邩�Ŕ��肷��� 4931 �Ɋ܂܂�� 9 �����Ċ��ɒT�������ƌ�F�����Ă��܂��̂�h������
                all_vis_nex = all_vis + "&" +str(nex).zfill(7) 
                all_relations_nex = all_relations + "&" + str(nind).zfill(7)
                
                
                _,relation_type,to,received,_ = relation_list[nind] ### ���X�̎��Y�֘A���̌Ăяo�����@�Ȃǂ̏��͏o�͂Ŏg���̂Ŏ��o���Ă���
                
                ### �t�ϊ��\���g���Đ������玑�Y���̌ďo�S�K�w���𕜌�����
                rev = all_vis_nex.split("&")
                rev_name = [rev_name_dic[int(ind)] for ind in rev] 
                all_list = "��".join(rev_name)
                
                
                if str(nex).zfill(7) in all_vis:
                    all_list += "(�d��)"
                    ans_list.append([test_id,num,source,len(rev)-1,all_list,relation_type,to,received,all_relations_nex])
                    ncount += 1
                else:
                    all_list += "(END)"
                    ans_list.append([test_id,num,source,len(rev)-1,all_list,relation_type,to,received,all_relations_nex])            
                    q.append([nex,all_vis_nex,all_relations_nex])
                    ncount += 1
                
                if ncount > M:
                    break
        if ncount > M:
            print(test_id,num,source,str(M)+"�ȏ�ɂȂ邽�߁A�r���őł��~�߂܂����B")
            ans_list = ans_list[:M]     
        ans_list.sort(key=lambda x: x[-1])
        ans_list = [lis[:-1] for lis in ans_list]
        if output_separate == True:
            create_output(test_id,num,source,ans_list,out_title)
        else:
            for lis in ans_list:
                ans_list_all.append(lis)
                        
        
    if output_separate == False:
        for out_title in ans_list_all_dic.keys():
            ans_list_all = ans_list_all_dic[out_title]
            create_output("���Y�K�w�}","2","�o��",ans_list_all,out_title)
            

    
if __name__ == "__main__":

    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    
    ### ����1 DBPath ����2 �o�̓t�H���_ 