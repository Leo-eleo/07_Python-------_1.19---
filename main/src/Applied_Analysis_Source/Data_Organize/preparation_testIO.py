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
received_asset_table_keys = ["資産ID","資産分類","備考①","備考②","備考③"]
all_relations_table_keys = ["呼出元資産","呼出方法","呼出先資産","受領判定","暫定無効FLG","変数名","呼出時PARM","登録分類"]

def preparation_received_asset(conn_preparation,cursor_preparation,received_asset_merge_path):
    
    
    received_asset_merge_df = pd.read_excel(received_asset_merge_path,sheet_name="受領資産一覧_TOOL入力用")
    received_asset_merge_df.fillna("",inplace=True)
    
    received_asset_dic = {}
    for i in range(len(received_asset_merge_df)):
        data = received_asset_merge_df.iloc[i]
        source_type = data["資産分類"].split("\n")
        source = Trim(data["資産ID"])
        if source not in received_asset_dic:
            received_asset_dic[source] = set()
        
        for s_type in source_type:
            received_asset_dic[source].add(Trim(s_type))
            
        value = data.to_list()
        sql,values = make_insert_sql("顧客別_受領資産一覧_汎用版",value,received_asset_table_keys)
        cursor_preparation.execute(sql,values)
    conn_preparation.commit()
    
    return received_asset_dic
    
    
def make_all_relations_output(db_relations_path,excel_relation_merge_path,received_asset_dic):
    
    all_relations_set = set()

    sql = "SELECT * FROM 顧客別_資産関連性情報"
    conn_relation_file = connect_accdb(db_relations_path)
    df_relation_all = pd.read_sql(sql,conn_relation_file)
    df_relation_all.fillna("",inplace=True)
    
    df_relation_keys = df_relation_all.columns.tolist()
    for i in range(len(df_relation_all)):
        data = df_relation_all.iloc[i]
        if "関連性調査結果" in data["登録分類"]:
            continue
        relation_list = [Trim(data[key]) for key in df_relation_keys]
        all_relations_set.add(tuple(relation_list))
        
        
    df_relation_merge = pd.read_excel(excel_relation_merge_path,sheet_name=None)  
    df_sheet_list = df_relation_merge.keys()

    file_name = os.path.split(excel_relation_merge_path)[-1]
    
    for sheetname in df_sheet_list:
        if "資産関連性調査結果" not in sheetname:
            continue
        df = df_relation_merge[sheetname]
        df.fillna("",inplace=True)
        for source,relation,to_source in zip(df["呼出元資産（メンバのみ）"],df["呼び出し方法"],df["呼び出し先資産"]):
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
                elif relation.startswith("COBOL-基準"):
                    data[3] = "基準"
                else:
                    if to_source.startswith("DAM:") or to_source.startswith("独自DAM:"):
                        
                        if to_source.startswith("DAM:"):
                            data[3] = "DAM"
                        elif to_source.startswith("独自DAM:"):
                            data[3] = "独自DAM"
                
                to_source = take_prefix(to_source,"DBIR-")
                to_source = take_prefix(to_source,"基準:")
                to_source = take_prefix(to_source,"DAM:")
                to_source = take_prefix(to_source,"独自DAM:")
                
                if "_重複あり_" in to_source:
                    to_source = to_source[:to_source.find("_重複あり_")]
                
                if "(" in to_source:
                    to_source = to_source[:to_source.find("(")]
                    
                if data[2] != to_source:
                    data[2] = to_source
                
                if data[2] in received_asset_dic:
                    if "DSN" in received_asset_dic[data[2]] and (data[3] == "DAM" or data[3] == "独自DAM"):
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
            data[4] = "●"
        elif data[0] in screen_asset_set:
            data[4] = "メニュー画面"
        else:
            data[4] = ""
            
        sql,values = make_insert_sql("顧客別_資産関連性情報",data,all_relations_table_keys)
        cursor.execute(sql,values)

    conn.commit()
    
def main(db_empty_path,db_relations_path,excel_relation_merge_path,received_asset_merge_path,setting_file_path,title):
    
    
    db_preparation_file_name = "顧客別DB_受領資産準備_"+dt_now+".accdb"
    db_preparation_path = os.path.join(title,db_preparation_file_name)
    shutil.copyfile(db_empty_path,db_preparation_path)
    
    conn_preparation = connect_accdb(db_preparation_path)
    cursor_preparation = conn_preparation.cursor()
    
    ### ファイルの対象テーブルの初期化
    sql,_ = make_delete_sql("顧客別_資産関連性情報",[],[])
    cursor_preparation.execute(sql)
    conn_preparation.commit()
    
    sql,_ = make_delete_sql("顧客別_受領資産一覧_汎用版",[],[])
    cursor_preparation.execute(sql)
    conn_preparation.commit()
    
    
    received_asset_dic = preparation_received_asset(conn_preparation,cursor_preparation,received_asset_merge_path)
    
    
    ### 無効設定用の情報を取得
    common_modules_df = pd.read_excel(setting_file_path,sheet_name="除外設定資産")
    common_modules_set = set([module for module in common_modules_df["資産ID"]])
    
    ## screen_asset_list ["画面資産（メンバ）","関連資産数","menu画面判定"] が格納されている

    screen_asset_list = Create_Common_Asset.create_screen_asset.main(excel_relation_merge_path,title,False)
    screen_asset_set = set()
    for screen_source,_,judge_screen in screen_asset_list:
        if judge_screen == "●":
            screen_asset_set.add(Trim(screen_source))


    df_relation_exclution = pd.read_excel(setting_file_path,sheet_name="オンライン関連性無効設定")
    df_relation_exclution.fillna("",inplace=True)
    exclution_relation_set = set()
    for relation,exclution in zip(df_relation_exclution["関連性"],df_relation_exclution["無効設定"]):
        if exclution == "●":
            exclution_relation_set.add(Trim(relation))
            
    all_relations_output = make_all_relations_output(db_relations_path,excel_relation_merge_path,received_asset_dic)
    
    
    
    db_common_relation_connections_file_name = "顧客別DB_共通資産階層図_"+dt_now+".accdb"
    db_common_relation_connections_path = os.path.join(title,db_common_relation_connections_file_name)
    shutil.copyfile(db_preparation_path,db_common_relation_connections_path)
    make_relations_setup_db(db_common_relation_connections_path,all_relations_output,set(),set(),set())
            
    db_batch_related_asset_file_name = "顧客別DB_バッチ関連資産_"+dt_now+".accdb"
    db_batch_related_asset_path = os.path.join(title,db_batch_related_asset_file_name)
    shutil.copyfile(db_common_relation_connections_path,db_batch_related_asset_path)
    
    db_online_relation_connections_file_name = "顧客別DB_オンライン資産階層図_"+dt_now+".accdb"
    db_online_relation_connections_path = os.path.join(title,db_online_relation_connections_file_name)
    shutil.copyfile(db_preparation_path,db_online_relation_connections_path)
    make_relations_setup_db(db_online_relation_connections_path,all_relations_output,common_modules_set,screen_asset_set,exclution_relation_set)
    
            
    db_online_related_asset_file_name = "顧客別DB_オンライン関連資産_"+dt_now+".accdb"
    db_online_related_asset_path = os.path.join(title,db_online_related_asset_file_name)
    shutil.copyfile(db_preparation_path,db_online_related_asset_path)
    make_relations_setup_db(db_online_related_asset_path,all_relations_output,set(),screen_asset_set,exclution_relation_set)
            
    db_common_related_asset_file_name = "顧客別DB_共通関連資産_"+dt_now+".accdb"
    db_common_related_asset_path = os.path.join(title,db_common_related_asset_file_name)
    shutil.copyfile(db_online_related_asset_path,db_common_related_asset_path)
    
    
    
    write_excel_multi_sheet("画面資産一覧.xlsx",screen_asset_list,"画面資産一覧",title,["画面資産（メンバ）","関連資産数","menu画面判定"])
    write_excel_multi_sheet("顧客別_資産関連性情報.xlsx",all_relations_output,"顧客別_資産関連性情報",title,all_relations_table_keys)
    
    
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])
 