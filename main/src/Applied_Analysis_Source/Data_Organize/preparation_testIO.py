#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
import pandas as pd
import shutil
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *
import Create_Common_Asset.create_screen_asset

dt_now = str(datetime.date.today())
received_asset_table_keys = ["���YID","���Y����","���l�@","���l�A","���l�B"]
all_relations_table_keys = ["�ďo�����Y","�ďo���@","�ďo�掑�Y","��̔���","�b�薳��FLG","�ϐ���","�ďo��PARM","�o�^����"]

def preparation_received_asset(conn_preparation,cursor_preparation,received_asset_merge_path):
    
    
    received_asset_merge_df = pd.read_excel(received_asset_merge_path,sheet_name="��̎��Y�ꗗ_TOOL���͗p")
    received_asset_merge_df.fillna("",inplace=True)
    
    received_asset_dic = {}
    for i in range(len(received_asset_merge_df)):
        data = received_asset_merge_df.iloc[i]
        source_type = data["���Y����"].split("\n")
        source = Trim(data["���YID"])
        if source not in received_asset_dic:
            received_asset_dic[source] = set()
        
        for s_type in source_type:
            received_asset_dic[source].add(Trim(s_type))
            
        value = data.to_list()
        sql,values = make_insert_sql("�ڋq��_��̎��Y�ꗗ_�ėp��",value,received_asset_table_keys)
        cursor_preparation.execute(sql,values)
    conn_preparation.commit()
    
    return received_asset_dic
    
    
def make_all_relations_output(db_relations_path,excel_relation_merge_path,received_asset_dic):
    
    all_relations_set = set()

    sql = "SELECT * FROM �ڋq��_���Y�֘A�����"
    conn_relation_file = connect_accdb(db_relations_path)
    df_relation_all = pd.read_sql(sql,conn_relation_file)
    df_relation_all.fillna("",inplace=True)
    
    df_relation_keys = df_relation_all.columns.tolist()
    for i in range(len(df_relation_all)):
        data = df_relation_all.iloc[i]
        if "�֘A����������" in data["�o�^����"]:
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
        
        data[4] = ""
            
        if data[7] != file_name:
            if data[3] == "":
                relation,to_source = str(data[1]),str(data[2])
                if relation.startswith("COBOL-NDB"):
                    data[3] = "NDB"
                elif relation.startswith("COBOL-�"):
                    data[3] = "�"
                else:
                    if to_source.startswith("DAM:") or to_source.startswith("�Ǝ�DAM:"):
                        
                        if to_source.startswith("DAM:"):
                            data[3] = "DAM"
                        elif to_source.startswith("�Ǝ�DAM:"):
                            data[3] = "�Ǝ�DAM"
                
                to_source = take_prefix(to_source,"DBIR-")
                to_source = take_prefix(to_source,"�:")
                to_source = take_prefix(to_source,"DAM:")
                to_source = take_prefix(to_source,"�Ǝ�DAM:")
                
                if "_�d������_" in to_source:
                    to_source = to_source[:to_source.find("_�d������_")]
                
                if "(" in to_source:
                    to_source = to_source[:to_source.find("(")]
                    
                if data[2] != to_source:
                    data[2] = to_source
                
                if data[2] in received_asset_dic:
                    if "DSN" in received_asset_dic[data[2]] and (data[3] == "DAM" or data[3] == "�Ǝ�DAM"):
                        data[3] += "(DSN)"
                    else:
                        if data[3] == "":
                            print(data)        
      
        else:
            
            if data[2] in received_asset_dic:
                data[3] = ",".join(sorted(received_asset_dic[data[2]]))
                
        all_output.append(data)
        
    return all_output    
    
def make_relations_setup_db(db_path,all_relations_output,common_modules_set,screen_asset_set,exclution_relation_set):
    
    conn = connect_accdb(db_path)
    cursor = conn.cursor()
    
    for data in all_relations_output:
        if data[0] in common_modules_set or data[1] in exclution_relation_set:
            data[4] = "��"
        elif data[0] in screen_asset_set:
            data[4] = "���j���[���"
        else:
            data[4] = ""
            
        sql,values = make_insert_sql("�ڋq��_���Y�֘A�����",data,all_relations_table_keys)
        cursor.execute(sql,values)

    conn.commit()
    
def main(db_empty_path,db_relations_path,excel_relation_merge_path,received_asset_merge_path,setting_file_path,title):
    
    
    db_preparation_file_name = "�ڋq��DB_��̎��Y����_"+dt_now+".accdb"
    db_preparation_path = os.path.join(title,db_preparation_file_name)
    shutil.copyfile(db_empty_path,db_preparation_path)
    
    conn_preparation = connect_accdb(db_preparation_path)
    cursor_preparation = conn_preparation.cursor()
    
    ### �t�@�C���̑Ώۃe�[�u���̏�����
    sql,_ = make_delete_sql("�ڋq��_���Y�֘A�����",[],[])
    cursor_preparation.execute(sql)
    conn_preparation.commit()
    
    sql,_ = make_delete_sql("�ڋq��_��̎��Y�ꗗ_�ėp��",[],[])
    cursor_preparation.execute(sql)
    conn_preparation.commit()
    
    
    received_asset_dic = preparation_received_asset(conn_preparation,cursor_preparation,received_asset_merge_path)
    
    
    ### �����ݒ�p�̏����擾
    common_modules_df = pd.read_excel(setting_file_path,sheet_name="���O�ݒ莑�Y")
    common_modules_set = set([module for module in common_modules_df["���YID"]])
    
    ## screen_asset_list ["��ʎ��Y�i�����o�j","�֘A���Y��","menu��ʔ���"] ���i�[����Ă���

    screen_asset_list = Create_Common_Asset.create_screen_asset.main(excel_relation_merge_path,title,False)
    screen_asset_set = set()
    for screen_source,_,judge_screen in screen_asset_list:
        if judge_screen == "��":
            screen_asset_set.add(Trim(screen_source))


    df_relation_exclution = pd.read_excel(setting_file_path,sheet_name="�I�����C���֘A�������ݒ�")
    df_relation_exclution.fillna("",inplace=True)
    exclution_relation_set = set()
    for relation,exclution in zip(df_relation_exclution["�֘A��"],df_relation_exclution["�����ݒ�"]):
        if exclution == "��":
            exclution_relation_set.add(Trim(relation))
            
    all_relations_output = make_all_relations_output(db_relations_path,excel_relation_merge_path,received_asset_dic)
    
    
    
    db_common_relation_connections_file_name = "�ڋq��DB_���ʎ��Y�K�w�}_"+dt_now+".accdb"
    db_common_relation_connections_path = os.path.join(title,db_common_relation_connections_file_name)
    shutil.copyfile(db_preparation_path,db_common_relation_connections_path)
    make_relations_setup_db(db_common_relation_connections_path,all_relations_output,set(),set(),set())
            
    db_batch_related_asset_file_name = "�ڋq��DB_�o�b�`�֘A���Y_"+dt_now+".accdb"
    db_batch_related_asset_path = os.path.join(title,db_batch_related_asset_file_name)
    shutil.copyfile(db_common_relation_connections_path,db_batch_related_asset_path)
    
    db_online_relation_connections_file_name = "�ڋq��DB_�I�����C�����Y�K�w�}_"+dt_now+".accdb"
    db_online_relation_connections_path = os.path.join(title,db_online_relation_connections_file_name)
    shutil.copyfile(db_preparation_path,db_online_relation_connections_path)
    make_relations_setup_db(db_online_relation_connections_path,all_relations_output,common_modules_set,screen_asset_set,exclution_relation_set)
    
            
    db_online_related_asset_file_name = "�ڋq��DB_�I�����C���֘A���Y_"+dt_now+".accdb"
    db_online_related_asset_path = os.path.join(title,db_online_related_asset_file_name)
    shutil.copyfile(db_preparation_path,db_online_related_asset_path)
    make_relations_setup_db(db_online_related_asset_path,all_relations_output,set(),screen_asset_set,exclution_relation_set)
            
    db_common_related_asset_file_name = "�ڋq��DB_���ʊ֘A���Y_"+dt_now+".accdb"
    db_common_related_asset_path = os.path.join(title,db_common_related_asset_file_name)
    shutil.copyfile(db_online_related_asset_path,db_common_related_asset_path)
    
    
    
    write_excel_multi_sheet("��ʎ��Y�ꗗ.xlsx",screen_asset_list,"��ʎ��Y�ꗗ",title,["��ʎ��Y�i�����o�j","�֘A���Y��","menu��ʔ���"])
    write_excel_multi_sheet("�ڋq��_���Y�֘A�����.xlsx",all_relations_output,"�ڋq��_���Y�֘A�����",title,all_relations_table_keys)
    
    
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])
 