#!/usr/bin/env python
# -*- coding: cp932 -*-
import sys
import os
import pandas as pd
import datetime

from collections import deque

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


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
    

def main(db_path,title,setting_path,output_separate="True",maxnum=2000000):
    
    M = int(maxnum) ### �����̍ő�l�@����𒴂�����~�߂�

    if os.path.isdir(title) == False:
        os.makedirs(title)
        
    if type(output_separate) != bool:
        output_separate = output_separate == "True"
        
        
    df = pd.read_excel(setting_path,sheet_name="�K�{���Y�ꗗ")
    df.fillna("",inplace=True)
    target_set = set()
    for target in df["�K�{���Y"]:
        target_set.add(target)
        
        
    
    conn = connect_accdb(db_path=db_path)


    ### �ڋq��_���Y�֘A����񂩂玑�Y�K�w�}��T�����邽�߂̃O���t���쐬����

    ### �ύX20191011
    sql =   """\
            SELECT * FROM �ڋq��_���Y�֘A����� WHERE �b�薳��FLG =''
            """
            
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)

    asset_set = set() ### �ďo�� or �ďo�� �̎��Y�ꗗ���d���������č쐬����

    relation_list = set() ### �ڋq��_���Y�֘A����񂩂�֘A���̈ꗗ���d���������Ď擾����

    for fr,relation_type,to,received in zip(df["�ďo�����Y"],df["�ďo���@"],df["�ďo�掑�Y"],df["��̔���"]):
        asset_set.add(fr)
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
        find = name_dic[fr]
        tind = name_dic[to]
        relation_graph[find].append((tind,i))
        
    
    # �O���t�̊���
    ################################# 


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
            
            if source not in target_set:
                continue
            
            ans_list.append([test_id,num,source,0,source+"(END)","","",""])
            if output_separate == True:
                create_output(test_id,num,source,ans_list,out_title)
            else:
                for lis in ans_list:
                    ans_list_all.append(lis)
            continue
        
        sind = name_dic[source]
        q = deque([[sind,str(sind).zfill(7),"",0]])
        
        ncount = 0 ### ���Y�K�w�}�̌����𐔂��� maxnum(default��200����) �𒴂���ƒ�������̂ň�U�ł��؂�
        
        while q:
            now,all_vis,all_relations,last_id = q.pop()

            find_next = 0
            for nex,nind in relation_graph[now]:
                
                find_next = 1
                
                ### ���܂Ō����ďo�S�K�w�̏�񂪐����łœ����Ă��� 0000100&0004931&0999999 �̂悤�Ȋ���
                ### str(nex).zfill(7) �� 7���܂�0���߂����Ă���̂� �Ⴆ�ΐ��������̂܂� 100&4931&999990 �Ƃ��� 
                ### ���� 9 ������ƂȂ����Ƃ��ɂ� 9 �����̕�����Ɋ܂܂�邩�Ŕ��肷��� 4931 �Ɋ܂܂�� 9 �����Ċ��ɒT�������ƌ�F�����Ă��܂��̂�h������
                all_vis_nex = all_vis + "&" +str(nex).zfill(7) 
                all_relations_nex = all_relations + "&" + str(nind).zfill(7)
                
                
                _,relation_type,to,received = relation_list[nind] ### ���X�̎��Y�֘A���̌Ăяo�����@�Ȃǂ̏��͏o�͂Ŏg���̂Ŏ��o���Ă���
                
                ### �t�ϊ��\���g���Đ������玑�Y���̌ďo�S�K�w���𕜌�����
                rev = all_vis_nex.split("&")
                rev_name = [rev_name_dic[int(ind)] for ind in rev] 
                
                target_find = 0
                
                for rname in rev_name:
                    if rname in target_set:
                        target_find = 1
                        
                all_list = "��".join(rev_name)
                
                
                if str(nex).zfill(7) in all_vis:
                    if target_find:
                        all_list += "(�d��)"
                        ans_list.append([test_id,num,source,len(rev)-1,all_list,relation_type,to,received,all_relations_nex])
                        ncount += 1
                else:
                    # all_list += "(END)"
                    # ans_list.append([test_id,num,source,len(rev)-1,all_list,relation_type,to,received,all_relations_nex])            
                    q.append([nex,all_vis_nex,all_relations_nex,nind])
                    # ncount += 1
                
                if ncount > M:
                    break
            if find_next:
                continue
            
            rev = all_vis.split("&")
            rev_name = [rev_name_dic[int(ind)] for ind in rev] 
            target_find = 0
                
            for rname in rev_name:
                if rname in target_set:
                    target_find = 1
                    
            if target_find == 0:
                continue
            _,relation_type,to,received = relation_list[last_id]
            all_list = "��".join(rev_name)
            all_list += "(END)"
            ans_list.append([test_id,num,source,len(rev)-1,all_list,relation_type,to,received,all_relations])   
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
    
    ### ����1 DBPath ����2 �o�̓t�H���_ ����3 �t�@�C�����ɏo�͂���ő匏��(�G�N�Z���̃t�@�C���T�C�Y�����ɂ�����Ȃ��͈͂ł͑��₷���Ƃ��ł���Ǝv����B ���Ԃ͂�����)