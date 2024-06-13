#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

import pandas as pd
import re
import datetime


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

dt_now = str(datetime.date.today())

received_asset_set_headers = ["資産ID","資産分類","ライブラリ","ソース管理号機","JSI資産有効判定","KEY2","モジュールID","日本語名称", \
                              "Gr1(形鋼・基盤・その他)","Gr1(形鋼)","Gr1(基盤)","Gr1(その他)","Gr2","Gr3","Gr4","Gr5(冷延・電磁・出荷)","Gr5(冷延)","Gr5(電磁)","Gr5(出荷)",\
                              "Gr6(管理系・操業系)","Gr6(管理系)","Gr6(操業系)",\
                              "Gr7(製鋼系・棒線系・条鋼出荷系)","Gr7(製鋼系)","Gr7(製鋼系・管理系)","Gr7(製鋼系・操業系)","Gr7(棒線系)","Gr7(棒線系・管理系)","Gr7(棒線系・操業系)","Gr7(条鋼出荷系)","Gr7(条鋼出荷系・管理系)","Gr7(条鋼出荷系・操業系)",
                              "備考","棚卸解析命名規則","抽出元JCL","ToDoNo.120回答","分類不要"]

received_asset_summary_headers = ["資産ID","資産分類","備考①\nロードライブラリ","備考②\n実行環境","備考③\n有効資産判定"]

get_from_member_list_keys = received_asset_set_headers[2:32]
le_member_keys = len(get_from_member_list_keys)

groups_list = ["Gr1(形鋼・基盤・その他)","Gr1(形鋼)","Gr1(基盤)","Gr1(その他)","Gr2","Gr3","Gr4","Gr5(冷延・電磁・出荷)","Gr5(冷延)","Gr5(電磁)","Gr5(出荷)",\
                "Gr6(管理系・操業系)","Gr6(管理系)","Gr6(操業系)",\
                "Gr7(製鋼系・棒線系・条鋼出荷系)","Gr7(製鋼系)","Gr7(製鋼系・管理系)","Gr7(製鋼系・操業系)","Gr7(棒線系)","Gr7(棒線系・管理系)","Gr7(棒線系・操業系)","Gr7(条鋼出荷系)","Gr7(条鋼出荷系・管理系)","Gr7(条鋼出荷系・操業系)"
]

asset_type_get_from_keys = ["JCL","PED","Easyパラメタ","カタプロ","DAMスキーマ定義","DBスキーマ定義","DBサブスキーマ定義"]

asset_type_get_from_modules = ["COBOL","Fortran","PLI","PSAM定義（画面：FMTGEN）","PSAM定義（画面：MEDGEN）",\
                               "アセンブラ","AIM環境（MSF）","AIM環境（MUKF）","AIM環境（R-LDF）","AIM環境（W-LDF）","AIM環境（XRF）",\
                               "Focusパラメタ","PSAM定義（オンライン帳票）","PSAM定義（バッチ帳票）","PSAM定義（帳票：FMTGEN）",
                               "オンライン環境（LD）","プログラム環境（MQN）","MED定義（画面）"]

received_asset_summary_all_group = set()

def get_jcl_name_from_inner_proc(inner_proc_name:str):
    """
    内部カタプロ名から抽出元JCLの情報を取得する

    Args:
        inner_proc_name (str): 内部カタプロ名

    Returns:
        str: 抽出元JCL名
    """
    match=re.match("^(.+)(%[A-Z])%(.+)%(.+)$",inner_proc_name)
    if match :
        return match.group(1) + match.group(2) + "%" + match.group(3)       
    else:
        raise ValueError(f"内部カタプロの命名規則に反した資産を検知しました。 内部カタプロ名={inner_proc_name}")


def get_jcl_name_from_easy_extracted(easy_name:str):
    """
    EASY名から抽出元JCLの情報を取得する

    Args:
        easy_name (str): easy名

    Returns:
        str: 抽出元JCL名
    """
    match=re.match("^(.+)E\d\d\d$",easy_name)
    if match :
        return match.group(1)
    else:
        raise ValueError(f"EASYの命名規則に反した資産を検知しました。 EASY名={easy_name}")
    
    
def get_relation_matching_template(df_relation_template):
    
    relation_matching_template_dic = {}
    
    for relaton_type,info,register_name in zip(df_relation_template["呼出方法"],df_relation_template["登録行"],df_relation_template["登録資産分類"]):
        relation_matching_template_dic[relaton_type] = [info,register_name]
        
    return relation_matching_template_dic


def get_asset_set_from_member_list(member_list_path,df_inner_proc_list,df_easy_list,df_utilities_list):
    
    df_member_list = pd.read_excel(member_list_path,sheet_name="メンバ一覧マージ版",header=1)
    df_member_list.fillna("", inplace=True)
    received_asset_member_list = []
    
    jcl_info_dic = {}

    ### メンバ一覧から取得する情報
    for i in range(len(df_member_list)):
        data = df_member_list.iloc[i]
        
        asset_type = data["資産分類(ACN)"]
        
        if asset_type == "JCL" or asset_type == "カタプロ":
            jcl_info_dic[data["KEY2"]] = data
        if asset_type not in asset_type_get_from_keys and asset_type not in asset_type_get_from_modules:
            continue
        
        if asset_type in asset_type_get_from_keys:
            asset_key = data["KEY2"]
            name_rule = "メンバ一覧KEY2列"
        elif asset_type in asset_type_get_from_modules:
            asset_key = data["モジュールID"]
            name_rule = "メンバ一覧モジュールID列"

        
        received_asset_row = [asset_key,asset_type] + [data[key] for key in get_from_member_list_keys] 
        
        received_asset_row.extend(["メンバ一覧より取得",name_rule,"","",""])
        received_asset_member_list.append(received_asset_row)
        
        
    ### 内部カタプロ一覧から取得する情報
    for inner_proc_name in df_inner_proc_list["内部カタプロ一覧"]:
        jcl_name = get_jcl_name_from_inner_proc(inner_proc_name)
        
        if jcl_name not in jcl_info_dic:
            print("Error this internal proc info is not found in members list {}".format(inner_proc_name))
            continue
        
        asset_type = "内部カタプロ"
        asset_key = inner_proc_name
        data = jcl_info_dic[jcl_name]
        received_asset_row = [asset_key,asset_type] + [data[key] for key in get_from_member_list_keys] 
        
        received_asset_row.extend(["内部カタプロ資産より取得","",jcl_name,"",""])
        received_asset_member_list.append(received_asset_row)
        
    
    ### EASY一覧から取得する情報    
    for easy_name in df_easy_list["EASY_JCL抽出分_一覧"]:
        jcl_name = get_jcl_name_from_easy_extracted(easy_name)
        
        if jcl_name not in jcl_info_dic:
            print("Error this extracted easy info is not found in members list {}".format(easy_name))
            received_asset_row = [easy_name,"EASY_JCL抽出分"] + [""]*le_member_keys 
        
            received_asset_row.extend(["EASY資産より取得","",jcl_name,"",""])
            received_asset_member_list.append(received_asset_row)
            continue
        
        asset_type = "EASY_JCL抽出分"
        asset_key = easy_name
        data = jcl_info_dic[jcl_name]
        received_asset_row = [asset_key,asset_type] + [data[key] for key in get_from_member_list_keys] 
        
        received_asset_row.extend(["EASY資産より取得","",jcl_name,"",""])
        received_asset_member_list.append(received_asset_row)
        
        
    ### Utilityから取得する情報
    for asset_key,asset_type in zip(df_utilities_list["資産ID"],df_utilities_list["資産分類"]):
        received_asset_row = [asset_key,asset_type] + [""]*le_member_keys
        
        received_asset_row.extend(["TODONo.120起因","","","",""])
        received_asset_member_list.append(received_asset_row)
        
        
    return received_asset_member_list
        
        
def get_asset_set_from_relation_merge(relation_merge_path,relation_matching_template):
    
    df_relation_merge = pd.read_excel(relation_merge_path,sheet_name=None)
    received_asset_set_groups = []
    
    sheet_names = df_relation_merge.keys()
    for sheet_name in sheet_names:
        if "資産関連性調査結果" not in sheet_name:
            continue
        
        df_relation_sheet = df_relation_merge[sheet_name]
        df_relation_sheet.fillna("",inplace=True)
        for i in range(len(df_relation_sheet)):
            data = df_relation_sheet.iloc[i]
            
            relation_type = data["呼び出し方法"]
    
            if relation_type not in relation_matching_template:
                continue
            
            asset_from,asset_type = relation_matching_template[relation_type]
            
            if asset_from == "呼出元":
                asset_key = data["呼出元資産（メンバのみ）"]
            elif asset_from == "呼出先":
                asset_key = data["呼び出し先資産"]
                
            if data["分類不要"] == "○":
                no_need = "○"
            else:
                no_need = ""
                
            received_asset_row = [asset_key,asset_type] + [""]*6 + [data[key] for key in groups_list]
                 
            received_asset_row.extend(["資産関連性調査結果より作成","","","",no_need])
            
            received_asset_set_groups.append(received_asset_row)
    
    return received_asset_set_groups
    

            
def make_received_asset_file(received_asset_set_common,received_asset_group,group_prefix,title):
    
    global received_asset_summary_all_group
    
    received_asset_summary_dic = {}
    
    for received_asset_row in received_asset_set_common+received_asset_group:
        asset_key = received_asset_row[0]
        asset_value = received_asset_row[1:5]
        
        if asset_key not in received_asset_summary_dic:
            received_asset_summary_dic[asset_key] = []
        received_asset_summary_dic[asset_key].append(asset_value)
        
        
    received_asset_summary_list = []
    
    for asset_key,asset_value in received_asset_summary_dic.items():
        asset_type = "\n".join(sorted(set([value[0] for value in asset_value])))
        if len(asset_value) > 1:
            received_asset_row = [asset_key,asset_type,"複数","複数","複数"]
        else:
            received_asset_row = [asset_key] + asset_value[0]
            
        received_asset_summary_list.append(received_asset_row)
        received_asset_summary_all_group.add(tuple(received_asset_row))
        
        
    file_name = "受領資産一覧_"+group_prefix+"_"+dt_now+".xlsx"
    out_title = os.path.join(title,group_prefix)
    
    if os.path.isdir(out_title) == False:
        os.makedirs(out_title)
        
    write_excel_multi_sheet3(file_name,[received_asset_set_common+received_asset_group,received_asset_summary_list],["受領資産一覧","受領資産一覧_TOOL入力用"],out_title,[received_asset_set_headers,received_asset_summary_headers])
        
    
def main(member_list_path,relation_merge_path,received_asset_make_template_path,title):
    
    global received_asset_summary_all_group
    
    df_received_asset_template = pd.read_excel(received_asset_make_template_path,sheet_name=None)
    
    df_relation_template = df_received_asset_template["資産関連性調査結果マッピング"]
    df_inner_proc_list = df_received_asset_template["内部カタプロ一覧"]
    df_easy_list = df_received_asset_template["EASY一覧"]
    df_utilities_list = df_received_asset_template["Utility群"]
    
    
    relation_matching_template = get_relation_matching_template(df_relation_template)
    
    received_asset_set_common = get_asset_set_from_member_list(member_list_path,df_inner_proc_list,df_easy_list,df_utilities_list)
    
    received_asset_set_groups = get_asset_set_from_relation_merge(relation_merge_path,relation_matching_template)
    
    
    for group in range(1,8):
        
        group_prefix = "Gr" + str(group)
        
        received_asset_group = []
        
        for received_asset_row in received_asset_set_groups:
            
            use_in_this_group = False
            sind = 8 ### Gr1(形鋼・基盤・その他) の情報が記載されている列index
            
            for i in range(len(groups_list)):
                if (received_asset_set_headers[sind+i].startswith(group_prefix) and received_asset_row[sind+i] == "○") or received_asset_row[-1] == "○":
                    use_in_this_group = True
                    break
                
            if use_in_this_group == True:
                received_asset_group.append(received_asset_row)
        
        make_received_asset_file(received_asset_set_common,received_asset_group,group_prefix,title)
    
    
    file_name = "受領資産一覧_マージ版_"+dt_now+".xlsx"
    out_title = os.path.join(title)
    
    if os.path.isdir(out_title) == False:
        os.makedirs(out_title)
        
    write_excel_multi_sheet3(file_name,[sorted(received_asset_summary_all_group)],["受領資産一覧_TOOL入力用"],out_title,[received_asset_summary_headers])
        
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])