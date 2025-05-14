#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
import pandas as pd
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


dt_now = str(datetime.date.today())


all_relation_header = ["呼出元資産","呼出方法","呼出先資産","受領判定","暫定無効FLG","変数名","呼出時PARM","登録分類"]

groups_key_list = ["Gr1(形鋼・基盤・その他)","Gr2","Gr3","Gr4","Gr5(冷延・電磁・出荷)","Gr5(冷延・電磁・出荷)","Gr5(冷延・電磁・出荷)",\
                    "Gr6(管理系・操業系)","Gr6(管理系・操業系)",\
                    "Gr7(製鋼系・棒線系・条鋼出荷系)","Gr7(製鋼系・棒線系・条鋼出荷系)","Gr7(製鋼系・棒線系・条鋼出荷系)","Gr7(製鋼系・棒線系・条鋼出荷系)","Gr7(製鋼系・棒線系・条鋼出荷系)"]
groups_info_list = ["Gr1","Gr2","Gr3","Gr4","Gr5(冷延)","Gr5(電磁)","Gr5(出荷)",\
                    "Gr6(管理系)","Gr6(操業系)","Gr7(製鋼系・管理系)","Gr7(製鋼系・操業系)","Gr7(棒線系・管理系)","Gr7(棒線系・操業系)","Gr7(条鋼出荷系・操業系)"
                    ]




def make_member_list(member_list_path):
    
    df_member_list = pd.read_excel(member_list_path,sheet_name="メンバ一覧マージ版",header=1)
    df_member_list.fillna("", inplace=True)
    
    member_list_key_dic = {}
    member_list_module_dic = {}
    

    ### メンバ一覧から取得する情報
    for i in range(len(df_member_list)):
        data = df_member_list.iloc[i]
        
        asset_key,asset_module = data["KEY2"],data["モジュールID"]
        
        asset_type,asset_need = data["資産分類(ACN)"],data["資産要否(合成結果)"]
    
        if asset_key in member_list_key_dic:
            print("Error KEY2 = {} found multiple line in members list".format(asset_key))
            # print(member_list_key_dic[asset_key])
            new_library = data["新環境管理ライブラリ名"]
            if new_library != "":
                member_list_key_dic[asset_key] = [asset_type,asset_need]
            # print(new_library,member_list_key_dic[asset_key])
        else:
            member_list_key_dic[asset_key] = [asset_type,asset_need]
            
        if asset_module not in member_list_module_dic:
            member_list_module_dic[asset_module] = [0,0]
            
        if asset_need in ("廃止済","対象外"):
            member_list_module_dic[asset_module][0] += 1
        else:
            member_list_module_dic[asset_module][1] += 1
        
        
    return member_list_key_dic,member_list_module_dic


def make_relation_merge_df(excel_relation_merge_path):
    
    df_relation_merge = pd.read_excel(excel_relation_merge_path,sheet_name=None)  
    df_sheet_list = df_relation_merge.keys()

    relation_merge_df = []
    for sheetname in df_sheet_list:
        if "資産関連性調査結果" not in sheetname:
            continue
        df = df_relation_merge[sheetname]
        df.fillna("",inplace=True)
        relation_merge_df.append(df)
        
    return pd.concat(relation_merge_df)
        
def make_starting_relation_merge_df(starting_relation_merge_path):
    starting_relation_merge_df = pd.read_excel(starting_relation_merge_path,sheet_name="起点資産関連性",header=1)
    starting_relation_merge_df.fillna("",inplace=True)
    
    return starting_relation_merge_df
    
def make_exclude_dic(setting_file_path):
    df_exclude_all = pd.read_excel(setting_file_path,sheet_name=None)  
    df_sheet_list = df_exclude_all.keys()
    
    exclude_all = set(df_exclude_all["運用系JCL_完全除外"]["除外資産名"].values.tolist())
    exclude_from_source = set()
    df_exclude = df_exclude_all["除外資産_Gr共通"]
    
    for asset,info in zip(df_exclude["除外資産名"],df_exclude["参照情報"]):
        if info == "疎結合対象JOBネット":
            exclude_all.add(asset)
        else:
            exclude_from_source.add(asset)
            
    exclude_group = {}
    for group in groups_info_list:
        sheet_name = "除外資産_" + group
        if sheet_name in df_sheet_list:
            df_exclude = df_exclude_all[sheet_name]
            exclude_all_group = set()
            exclude_from_source_group = set()
            for asset,info in zip(df_exclude["除外資産名"],df_exclude["参照情報"]):
                if info == "疎結合対象JOBネット":
                    exclude_all_group.add(asset)
                else:
                    exclude_from_source_group.add(asset)
            
            exclude_group[group] = [exclude_all_group,exclude_from_source_group]
        else:
            exclude_group[group] = [[],[]]
            
    return exclude_all,exclude_from_source,exclude_group



def output_relation_list_group(relation_merge_df,starting_relation_merge_df,member_list_key_dic,member_list_module_dic,exclude_all,exclude_from_source,exclude_group,gr_key,gr_base_info,title):
    
    
    all_relation_set = set()
    
    df_group = relation_merge_df[(relation_merge_df[gr_key] == "○") | (relation_merge_df["分類不要"] == "○")]
    for source,relation,to_source,asset_name,asset_need in zip(df_group["呼出元資産（メンバのみ）"],df_group["呼び出し方法"],df_group["呼び出し先資産"],df_group["関連性記載資産名"],df_group["資産要否"]):
                
        extract_flg = ""
        ### 運用系JCL_完全除外 の資産を除外
        if source in exclude_all or to_source in exclude_all:
            extract_flg = "○"
            
        ### 疎結合対象JOBネット の資産を除外
        if source in exclude_group[0] or to_source in exclude_group[0]:
            extract_flg = "○"
        
        ### 指定除外資産 の資産を除外
        if source in exclude_from_source or source in exclude_group[1]:
            extract_flg = "○"
        
        
        ### 画面→PGM呼出における MCP定義の除外
        if relation == "画面→PGM呼出":
            if asset_name in member_list_key_dic and member_list_key_dic[asset_name][0] == "ACS（MCP定義）" and asset_need in ("廃止済","対象外"):
                extract_flg = "○"
            
        ### メンバ一覧の廃止済,対象外資産の除外    
        if to_source in member_list_key_dic and member_list_key_dic[to_source][1] in ("廃止済","対象外"):
            extract_flg = "○"
        
        if to_source in member_list_module_dic and (member_list_module_dic[to_source][0] > 0 and member_list_module_dic[to_source][1] == 0):
            extract_flg = "○"
            
        if (source,to_source,gr_base_info) == ("N2DAIKOU","KZ71FW00","Gr5(出荷)"):
            extract_flg = "○"
            
        if to_source in member_list_key_dic:
            source_type = member_list_key_dic[to_source][0]
        else:
            source_type = ""
            
        all_relation_set.add((source,relation,to_source,source_type,extract_flg,"","",""))
        
    for source,relation,to_source,gr_info in zip(starting_relation_merge_df["呼出元資産（メンバのみ）"],starting_relation_merge_df["呼出方法"],starting_relation_merge_df["呼出先資産"],starting_relation_merge_df["Group分類(JSI解答)"]):
        
        extract_flg = ""
        
        ### 運用系JCL_完全除外 の資産を除外
        if source in exclude_all or to_source in exclude_all:
            extract_flg = "○"
        
        ### 疎結合対象JOBネット の資産を除外
        if source in exclude_group[0] or to_source in exclude_group[0]:
            extract_flg = "○"
        
        ### 指定除外資産 の資産を除外
        if source in exclude_from_source or source in exclude_group[1]:
            extract_flg = "○"
        
        ### メンバ一覧の廃止済,対象外資産の除外    
        if to_source in member_list_key_dic and member_list_key_dic[to_source][1] in ("廃止済","対象外"):
            extract_flg = "○"
        
        if to_source in member_list_module_dic and (member_list_module_dic[to_source][0] > 0 and member_list_module_dic[to_source][1] == 0):
            extract_flg = "○"
    
        
        if gr_info.startswith("×"):# or gr_info.startswith("7"):
            continue
        
        if "(" not in gr_info:
            print("Group info format is not matched {},{},{},{}".format(source,relation,to_source,gr_info))
            continue
        
        gr_lis = gr_info[:gr_info.find("(")].split("・")
        for gr in gr_lis:
            gr_name = "Gr" + gr
            if gr_name not in gr_base_info:
                continue
            
            if gr_name == "Gr5" and gr_base_info[4:6] not in gr_info:
                continue
            
            if gr_name == "Gr6" or gr_name == "Gr7":
                if gr_base_info[4:len(gr_base_info)-1] not in gr_info:
                    continue
                
            
            if to_source in member_list_key_dic:
                source_type = member_list_key_dic[to_source][0]
            else:
                source_type = ""
                
            all_relation_set.add((source,relation,to_source,source_type,extract_flg,"","",""))
            
    gr_name = gr_base_info
    if "Gr5" in gr_name:
        gr_name = "Gr5"
    if "Gr6" in gr_name:
        gr_name = "Gr6"
    if "Gr7" in gr_name:
        gr_name = "Gr7"
        
    file_name = "顧客別_資産関連性情報_"+gr_base_info+"_"+dt_now+".xlsx"
    out_title = os.path.join(title,gr_name)
    
    if os.path.isdir(out_title) == False:
        os.makedirs(out_title)
        
    write_excel_multi_sheet3(file_name,[sorted(all_relation_set)],["顧客別_資産関連性情報"],out_title,[all_relation_header])
        

def main(member_list_path,excel_relation_merge_path,starting_relation_merge_path,setting_file_path,title):
  
    exclude_all,exclude_from_source,exclude_group = make_exclude_dic(setting_file_path)

    member_list_key_dic,member_list_module_dic = make_member_list(member_list_path)
        
    relation_merge_df = make_relation_merge_df(excel_relation_merge_path)
    
    starting_relation_merge_df = make_starting_relation_merge_df(starting_relation_merge_path)
    
    for gr_key,gr_info in zip(groups_key_list,groups_info_list):
        output_relation_list_group(relation_merge_df,starting_relation_merge_df,member_list_key_dic,member_list_module_dic,exclude_all,exclude_from_source,exclude_group[gr_info],gr_key,gr_info,title)
    
            
    
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
 