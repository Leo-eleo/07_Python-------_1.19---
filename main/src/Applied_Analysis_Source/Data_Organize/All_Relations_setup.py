#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *
import Create_Common_Asset.create_screen_asset

def main(db_path,excel_path,excel_relation_merge_path,title,exclude_screen=True):
    
    if type(exclude_screen) != bool:
        exclude_screen = exclude_screen == "True"
        
    exclude_screen = False
    conn = connect_accdb(db_path)
    cursor = conn.cursor()
    sql = "SELECT * FROM �ڋq��_��̎��Y�ꗗ_�ėp��"
    df_received_asset = pd.read_sql(sql,conn)
    
    df_received_asset.fillna("",inplace=True)
    received_asset_dic = {}
    for i in range(len(df_received_asset)):
        data = df_received_asset.iloc[i]
        source_type = data["���Y����"].split("\n")
        source = Trim(data["���YID"])
        if source not in received_asset_dic:
            received_asset_dic[source] = set()
        
        for s_type in source_type:
            received_asset_dic[source].add(Trim(s_type))
            
    df_exclution_module = pd.read_excel(excel_path,sheet_name="���O�ݒ莑�Y")
    df_exclution_module.fillna("",inplace=True)
    # print(df_exclution_module.columns.tolist())
    exclution_module_set = set()
    for source,exclution in zip(df_exclution_module["���YID"],df_exclution_module["���O�ݒ�"]):
        if exclution == "��":
            exclution_module_set.add(Trim(source))
    
    ## screen_asset_list ["��ʎ��Y�i�����o�j","�֘A���Y��","menu��ʔ���"] ���i�[����Ă���
    if exclude_screen:
        screen_asset_list = Create_Common_Asset.create_screen_asset.main(excel_relation_merge_path,title,False)
        screen_asset_set = set()
        for screen_source,relation_num,judge_screen in screen_asset_list:
            if judge_screen == "��":
                screen_asset_set.add(Trim(screen_source))
    else:
        screen_asset_list = []
        screen_asset_set = set()

    df_relation_exclution = pd.read_excel(excel_path,sheet_name="�I�����C���֘A�������ݒ�")
    df_relation_exclution.fillna("",inplace=True)
    exclution_relation_set = set()
    for relation,exclution in zip(df_relation_exclution["�֘A��"],df_relation_exclution["�����ݒ�"]):
        if exclution == "��":
            exclution_relation_set.add(Trim(relation))
            

    sql = "SELECT * FROM �ڋq��_���Y�֘A�����"
    df_relation_all = pd.read_sql(sql,conn)
    df_relation_all.fillna("",inplace=True)
    
    sql,_ = make_delete_sql("�ڋq��_���Y�֘A�����",[],[])
    cursor.execute(sql)
    conn.commit()
    
    all_relations_set = set()
    df_relation_keys = df_relation_all.columns.tolist()
    for i in range(len(df_relation_all)):
        data = df_relation_all.iloc[i]
        if "���Y�֘A����������" in data["�o�^����"]:
            continue
        relation_list = [Trim(data[key]) for key in df_relation_keys]
        all_relations_set.add(tuple(relation_list))
        
        
    df_relation_merge = pd.read_excel(excel_relation_merge_path,sheet_name=None)  
    df_sheet_list = df_relation_merge.keys()

    file_name = os.path.split(excel_relation_merge_path)[-1]
    
    for sheetname in df_sheet_list:
        if "���Y�֘A����������" not in sheetname:
            continue
        df = df_relation_merge[sheetname]
        df.fillna("",inplace=True)
        for source,relation,to_source in zip(df["�ďo�����Y�i�����o�̂݁j"],df["�Ăяo�����@"],df["�Ăяo���掑�Y"]):
            relation_list = [""]*8
            relation_list[0] = Trim(source)
            relation_list[1] = Trim(relation)
            relation_list[2] = Trim(to_source)
            relation_list[7] = file_name
            all_relations_set.add(tuple(relation_list))
            
            
            
    all_relations_set = sorted(all_relations_set)
    all_output = []
    for i in range(len(all_relations_set)):
        data = list(all_relations_set[i])
        
        if data[2] in received_asset_dic:
            data[3] = ",".join(sorted(received_asset_dic[data[2]]))
        
        if data[0] in exclution_module_set or  data[1] in exclution_relation_set:
            data[4] = "��"
        elif data[0] in screen_asset_set:
            data[4] = "���j���[���"
            
            
        sql,values = make_insert_sql("�ڋq��_���Y�֘A�����",data,df_relation_keys)
        cursor.execute(sql,values)
        all_output.append(data)
            
    
    write_excel_multi_sheet("��ʎ��Y�ꗗ.xlsx",screen_asset_list,"��ʎ��Y�ꗗ",title,["��ʎ��Y�i�����o�j","�֘A���Y��","menu��ʔ���"])
    write_excel_multi_sheet("�ڋq��_���Y�֘A�����.xlsx",all_output,"�ڋq��_���Y�֘A�����",title,["�ďo�����Y","�ďo���@","�ďo�掑�Y","��̔���","�b�薳��FLG","�ϐ���","�ďo��PARM","�o�^����"])
    
    
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
 