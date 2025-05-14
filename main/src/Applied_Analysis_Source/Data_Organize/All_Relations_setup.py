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
    sql = "SELECT * FROM 顧客別_受領資産一覧_汎用版"
    df_received_asset = pd.read_sql(sql,conn)
    
    df_received_asset.fillna("",inplace=True)
    received_asset_dic = {}
    for i in range(len(df_received_asset)):
        data = df_received_asset.iloc[i]
        source_type = data["資産分類"].split("\n")
        source = Trim(data["資産ID"])
        if source not in received_asset_dic:
            received_asset_dic[source] = set()
        
        for s_type in source_type:
            received_asset_dic[source].add(Trim(s_type))
            
    df_exclution_module = pd.read_excel(excel_path,sheet_name="除外設定資産")
    df_exclution_module.fillna("",inplace=True)
    # print(df_exclution_module.columns.tolist())
    exclution_module_set = set()
    for source,exclution in zip(df_exclution_module["資産ID"],df_exclution_module["除外設定"]):
        if exclution == "●":
            exclution_module_set.add(Trim(source))
    
    ## screen_asset_list ["画面資産（メンバ）","関連資産数","menu画面判定"] が格納されている
    if exclude_screen:
        screen_asset_list = Create_Common_Asset.create_screen_asset.main(excel_relation_merge_path,title,False)
        screen_asset_set = set()
        for screen_source,relation_num,judge_screen in screen_asset_list:
            if judge_screen == "●":
                screen_asset_set.add(Trim(screen_source))
    else:
        screen_asset_list = []
        screen_asset_set = set()

    df_relation_exclution = pd.read_excel(excel_path,sheet_name="オンライン関連性無効設定")
    df_relation_exclution.fillna("",inplace=True)
    exclution_relation_set = set()
    for relation,exclution in zip(df_relation_exclution["関連性"],df_relation_exclution["無効設定"]):
        if exclution == "●":
            exclution_relation_set.add(Trim(relation))
            

    sql = "SELECT * FROM 顧客別_資産関連性情報"
    df_relation_all = pd.read_sql(sql,conn)
    df_relation_all.fillna("",inplace=True)
    
    sql,_ = make_delete_sql("顧客別_資産関連性情報",[],[])
    cursor.execute(sql)
    conn.commit()
    
    all_relations_set = set()
    df_relation_keys = df_relation_all.columns.tolist()
    for i in range(len(df_relation_all)):
        data = df_relation_all.iloc[i]
        if "資産関連性調査結果" in data["登録分類"]:
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
        
        if data[2] in received_asset_dic:
            data[3] = ",".join(sorted(received_asset_dic[data[2]]))
        
        if data[0] in exclution_module_set or  data[1] in exclution_relation_set:
            data[4] = "●"
        elif data[0] in screen_asset_set:
            data[4] = "メニュー画面"
            
            
        sql,values = make_insert_sql("顧客別_資産関連性情報",data,df_relation_keys)
        cursor.execute(sql,values)
        all_output.append(data)
            
    
    write_excel_multi_sheet("画面資産一覧.xlsx",screen_asset_list,"画面資産一覧",title,["画面資産（メンバ）","関連資産数","menu画面判定"])
    write_excel_multi_sheet("顧客別_資産関連性情報.xlsx",all_output,"顧客別_資産関連性情報",title,["呼出元資産","呼出方法","呼出先資産","受領判定","暫定無効FLG","変数名","呼出時PARM","登録分類"])
    
    
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
 