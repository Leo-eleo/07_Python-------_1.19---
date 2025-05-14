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

dt_now = str(datetime.date.today())



groups_list = ["Gr1(形鋼・基盤・その他)","Gr1(形鋼)","Gr1(基盤)","Gr1(その他)","Gr2","Gr3","Gr4","Gr5(冷延・電磁・出荷)","Gr5(冷延)","Gr5(電磁)","Gr5(出荷)",\
                "Gr6(管理系・操業系)","Gr6(管理系)","Gr6(操業系)",\
                "Gr7(製鋼系・棒線系・条鋼出荷系)","Gr7(製鋼系)","Gr7(製鋼系・管理系)","Gr7(製鋼系・操業系)","Gr7(棒線系)","Gr7(棒線系・管理系)","Gr7(棒線系・操業系)","Gr7(条鋼出荷系)","Gr7(条鋼出荷系・管理系)","Gr7(条鋼出荷系・操業系)"
]
same_modules = ["コイル","スラブ","形鋼","計画","材試","熱延","熱仕"]
same_modules_group = ["Gr6","Gr6","Gr1","Gr6","Gr3","Gr6","Gr6"]
len_groups = len(groups_list)
all_starting_asset_header = ["TEST_ID","実行順序","実行JOB","補足","出力フォルダ"]


groups_key_list = ["Gr1(形鋼・基盤・その他)","Gr2","Gr3","Gr4","Gr5(冷延・電磁・出荷)","Gr5(冷延・電磁・出荷)","Gr5(冷延・電磁・出荷)",\
                    "Gr6(管理系・操業系)","Gr6(管理系・操業系)",\
                    "Gr7(製鋼系・棒線系・条鋼出荷系)","Gr7(製鋼系・棒線系・条鋼出荷系)","Gr7(製鋼系・棒線系・条鋼出荷系)","Gr7(製鋼系・棒線系・条鋼出荷系)","Gr7(製鋼系・棒線系・条鋼出荷系)"]
groups_info_list = ["Gr1","Gr2","Gr3","Gr4","Gr5(冷延)","Gr5(電磁)","Gr5(出荷)",\
                    "Gr6(管理系)","Gr6(操業系)","Gr7(製鋼系・管理系)","Gr7(製鋼系・操業系)","Gr7(棒線系・管理系)","Gr7(棒線系・操業系)","Gr7(条鋼出荷系・操業系)"
                    ]




screen_asset_header = ["KEY2","ライブラリ","ソース管理号機","本番号機1","本番号機2","本番号機3","モジュールID",\
                    "資産受領状況","資産分類(ACN)","資産要否(合成結果)","CVT要否(合成結果)","JSI資産有効判定","資産利用システム",\
                    "Gr1(形鋼・基盤・その他)","Gr1(形鋼)","Gr1(基盤)","Gr1(その他)","Gr2","Gr3","Gr4","Gr5(冷延・電磁・出荷)","Gr5(冷延)","Gr5(電磁)","Gr5(出荷)",\
                    "Gr6(管理系・操業系)","Gr6(管理系)","Gr6(操業系)",\
                    "Gr7(製鋼系・棒線系・条鋼出荷系)","Gr7(製鋼系)","Gr7(製鋼系・管理系)","Gr7(製鋼系・操業系)","Gr7(棒線系)","Gr7(棒線系・管理系)","Gr7(棒線系・操業系)","Gr7(条鋼出荷系)","Gr7(条鋼出荷系・管理系)","Gr7(条鋼出荷系・操業系)", \
                    "日本語名称","抽出元JCL","登録者用資産ID命名規則","登録者用資産ID"]

revival_asset_header = ["処理起点","関連資産","資産分類","ソース名","備考①\nロードライブラリ","備考②\n実行環境","備考③\n有効資産判定","「関連資産」の\n復活要否","判断理由"]

related_asset_header = ["処理起点","関連資産","資産分類","オンバッチ分類","備考①","備考②","備考③"]

starting_asset_merge_header = ["関連資産","資産分類","起点資産=◎\n利用資産=○","オンバッチ分類"]

asset_inventory_header = ["KEY2","ライブラリ","ソース管理号機","本番号機1","本番号機2","本番号機3","モジュールID","資産受領状況","資産分類(ACN)","資産要否(合成結果)","JSI資産有効判定","CVT要否(合成結果)","資産利用システム",\
                          "Gr1(形鋼・基盤・その他)","Gr1(形鋼)","Gr1(基盤)","Gr1(その他)","Gr2","Gr3","Gr4","Gr5(冷延・電磁・出荷)","Gr5(冷延)","Gr5(電磁)","Gr5(出荷)",\
                          "Gr6(管理系・操業系)","Gr6(管理系)","Gr6(操業系)",\
                          "Gr7(製鋼系・棒線系・条鋼出荷系)","Gr7(製鋼系)","Gr7(製鋼系・管理系)","Gr7(製鋼系・操業系)","Gr7(棒線系)","Gr7(棒線系・管理系)","Gr7(棒線系・操業系)","Gr7(条鋼出荷系)","Gr7(条鋼出荷系・管理系)","Gr7(条鋼出荷系・操業系)", \
                          "日本語名称","抽出元JCL","登録者用資産ID命名規則","登録者用資産ID","バッチ資産","オンライン資産","棚卸判定","棚卸判定(前回)","利用判定","バッチ判定","オンライン判定",\
                          "復活資産","画面追加移行対象資産(バッチ利用)","画面追加移行対象資産(オンライン利用)"]

group_all_use = ["○"]*len_groups
group_all_empty = [""]*len_groups


name_dic = {}
rev_name_dic = {}
relation_graph = []
relation_group_info = {}
relation_list = {}
visited_id = []



def write_excel_multi_sheet(filename,dfs,sheet_names,path,output_headers):
    
    Sheet_lim = 10**6
    writer = pd.ExcelWriter(path+"/"+filename,engine='xlsxwriter')
    writer.book.use_zip64()
    sheet_name_list = []
    
    df_list = []
    output_header_list = []
    for df,header,sheet_name in zip(dfs,output_headers,sheet_names):
        M = len(df)
        for i in range(M//Sheet_lim+1):
            df_list.append(df[i*Sheet_lim:min(M,(i+1)*Sheet_lim)])
            output_header_list.append(header)
            if i == 0:
                sheet_name_list.append(sheet_name)
            else:
                sheet_name_list.append(sheet_name +"_" + str(i+1))
            
    for list,sheet_name,header in zip(df_list,sheet_name_list,output_header_list):
        df = pd.DataFrame(list,columns=header)
        df.to_excel(writer, sheet_name=sheet_name,index=False)
        
    writer._save()
    writer.close()
    
    
def check_module_name(name):
    for module in same_modules:
        if module in name:
            return name[:name.find(module)]
    
    return name    


def get_df_revival_asset(setting_file_path,gr_info):
    sheet_name = "復活資産_" + gr_info
    
    try:
        df_revival = pd.read_excel(setting_file_path,sheet_name=sheet_name)
        df_revival = df_revival[revival_asset_header]
        df_revival.fillna("",inplace=True)
    except:
        print("Error there is no sheet of {} for revival asset.".format(sheet_name))
        df_revival = pd.DataFrame([])
        
    return df_revival

    
def make_inventory_template(asset_inventory_template_path):
    inventory_template_df = pd.read_excel(asset_inventory_template_path,sheet_name="棚卸用資産一覧",header=0)
    inventory_template_df.fillna("",inplace=True)
    
    inventory_id_matching_dic = {}
    inventory_key_matching_dic = {}
    
    for i,(key,inventory_id) in enumerate(zip(inventory_template_df["KEY2"],inventory_template_df["登録者用資産ID"])):
        if inventory_id not in inventory_id_matching_dic:
            inventory_id_matching_dic[inventory_id] = []
            
        inventory_id_matching_dic[inventory_id].append(i)
        
        if key not in inventory_key_matching_dic:
            inventory_key_matching_dic[key] = []
            
        inventory_key_matching_dic[key].append(i)
        
    return inventory_template_df,inventory_id_matching_dic,inventory_key_matching_dic
    
    
def make_screen_asset_and_judge_from_member_list(member_list_path):
    
    df_member_list = pd.read_excel(member_list_path,sheet_name="メンバ一覧マージ版",header=1)
    df_member_list.fillna("", inplace=True)
    
    screen_asset_list = []  
    
    screen_asset_info_list = screen_asset_header[:-3]

    ### メンバ一覧から取得する情報
    for i in range(len(df_member_list)):
        data = df_member_list.iloc[i]
        
        # asset_key,asset_module = data["KEY2"],data["モジュールID"]
        
        asset_type,asset_valid = data["資産分類(ACN)"],data["JSI資産有効判定"]
    
        if asset_valid == "":
            continue
        
        if asset_type not in ("PSAM定義（画面：FMTGEN）","PSAM定義（画面：MEDGEN）"):
            continue
        
            
        screen_list_row = [data[key] for key in screen_asset_info_list]
        screen_list_row.extend(["","メンバ一覧モジュールID列",data["モジュールID"]])
        screen_asset_list.append(screen_list_row)
        
    return screen_asset_list
        


def make_relations_group_and_adl_definition_list(base_path,gr_info):
    
    adl_definition_dic = {}
    search_path = os.path.join(base_path)
    folder_files = glob_files(search_path)
    
    for file_path in folder_files:
        if "顧客別_資産関連性情報" not in file_path or gr_info not in file_path:
            continue
        relations_group_df = pd.read_excel(file_path,sheet_name="顧客別_資産関連性情報")
        relations_group_df.fillna("",inplace=True)
        
        for source_from,relation,source_to in zip(relations_group_df["呼出元資産"],relations_group_df["呼出方法"],relations_group_df["呼出先資産"]):
 
            if "ファイル名" in relation:
                if source_from not in adl_definition_dic:
                    adl_definition_dic[source_from] = set()
                adl_definition_dic[source_from].add(source_to)    
 
        relations_group_df = relations_group_df[relations_group_df["暫定無効FLG"] != "○"]
        return relations_group_df,adl_definition_dic
    
    
    print("Error, there is no file of relations on {} in {}".format(gr_info,base_path))
    return pd.DataFrame([]),[]


def make_relations_group_starting_point(starting_point_merge_path,gr_base_info):
    starting_asset_set = set()
    
    df_starting_list = pd.read_excel(starting_point_merge_path,sheet_name="起点資産一覧",header=1)
    df_starting_list.fillna("",inplace=True)
    for starting_asset,onbatch,gr_info in zip(df_starting_list["実行JOB"],df_starting_list["ONBAT"],df_starting_list["Group分類(JSI解答)"]):
        if gr_info.startswith("×"):
            continue
        if "(" not in gr_info:
            print("Group info format is not matched {},{},{}".format(starting_asset,onbatch,gr_info))
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
                
            starting_asset_set.add((starting_asset,onbatch))
    df_starting_relation = pd.read_excel(starting_point_merge_path,sheet_name="起点資産関連性",header=1)
    df_starting_relation.fillna("",inplace=True)
    for source_to,gr_info in zip(df_starting_relation["呼出先資産"],df_starting_relation["Group分類(JSI解答)"]):
        if gr_info.startswith("×"):
            continue
        if "(" not in gr_info:
            print("Group info format is not matched {},{},{}".format(starting_asset,onbatch,gr_info))
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
                
            starting_asset_set.add((source_to,"ON"))
    return starting_asset_set
    


def make_received_asset_dic(base_path,gr_info):
    
    if "Gr5" in gr_info:
        gr_info = "Gr5"
    if "Gr6" in gr_info:
        gr_info = "Gr6"
    if "Gr7" in gr_info:
        gr_info = "Gr7"
        
    search_path = os.path.join(base_path)
    
    folder_files = glob_files(search_path)
    
    for file_path in folder_files:
        if "受領資産一覧" not in file_path or gr_info not in file_path:
            continue
        
        df_received_asset = pd.read_excel(file_path,sheet_name="受領資産一覧_TOOL入力用")
        df_received_asset.fillna("",inplace=True)
        
        received_asset_dic = {}
        for i in range(len(df_received_asset)):
            data = df_received_asset.iloc[i].to_list()
            source = data[0]
            if source not in received_asset_dic:
                received_asset_dic[source] = set()
            
            
            received_asset_dic[source].add(tuple(data[1:]))
        
        return received_asset_dic

    print("Error, there is no info of received asset of {} in {}.".format(gr_info,base_path))
    return {}



def make_starting_asset_df(base_path,gr_info):

    search_path = os.path.join(base_path)
    
    folder_files = glob_files(search_path)
    
    for file_path in folder_files:
        if "起点情報" not in file_path or gr_info not in file_path:
            continue
        
        df_received_asset = pd.read_excel(file_path,sheet_name="TEST_実施単位")
        df_received_asset.fillna("",inplace=True)
        
        return df_received_asset

    print("Error, there is no info of starting asset of {} in {}.".format(gr_info,base_path))
    return pd.DataFrame([])

def make_starting_asset_merge(related_asset_all,starting_asset_set,gr_info):
    starting_asset_merge = set()
    for i in range(len(related_asset_all)):
        asset,asset_type,onbatch = related_asset_all[i][1:4]
        starting_asset_check = "○"
        
        if (asset,onbatch) in starting_asset_set:
            starting_asset_check = "◎"
            
        starting_asset_merge.add((asset,asset_type,starting_asset_check,onbatch))
        
    return sorted(starting_asset_merge)
    

def make_additional_screen_related_asset(screen_asset_list,gr_key,gr_info,asset_all_used_gr_set):
    
    if "Gr5" in gr_info:
        gr_key = gr_info
    if "Gr6" in gr_info:
        gr_key = gr_info
    if "Gr7" in gr_info:
        gr_key = gr_info
    
    if gr_key in screen_asset_header:
        gind = screen_asset_header.index(gr_key)
    else:
        gind = -1
    if gind == -1:
        print("Error group info is not found in this received asset folder")
        return 
    screen_asset_starting_point = set()
    
    additional_screen_asset_list = []
    
    for data in screen_asset_list:
        if data[gind] == "":
            continue
        if data[-1] in asset_all_used_gr_set:
            continue
        screen_asset_starting_point.add((data[0],1,data[-1],"ON",""))
        additional_screen_asset_list.append(data)
        
    screen_asset_starting_point = pd.DataFrame(screen_asset_starting_point,columns=all_starting_asset_header)

    return additional_screen_asset_list,screen_asset_starting_point
    
    
def make_search_graph(df):
    
    
    asset_set = set() ### 呼出元 or 呼出先 の資産一覧を重複を除いて作成する

    relation_list = set() ### 顧客別_資産関連性情報から関連性の一覧を重複を除いて取得する

    for fr,relation_type,to,received in zip(df["呼出元資産"],df["呼出方法"],df["呼出先資産"],df["受領判定"]):
        fr_true = check_module_name(fr)
        asset_set.add(fr_true)
        
        asset_set.add(to)
        relation_list.add((fr,relation_type,to,received))
      

    asset_set = sorted(asset_set)
    relation_list = sorted(relation_list)

    ### グラフを作成する際に DXDAIKOU のような名前を元にするより DXDAIKOU = 1, JXDAIKOU = 2 のような対応表を作って 数字で扱えるようにした方が高速に動作するため 変換表と逆変換表を作成する

    ### 変換表 name_dic["DXDAIKOU"] = 1 のように 名前から数字が取得できる
    name_dic = {s:i for i,s in enumerate(asset_set)} 

    ### 逆変換表 rev_name_dic[1] = "DXDAIKOU" のように 数字から名前が取得できる 出力の際は名前に戻すのでそこで使う
    rev_name_dic = {i:s for i,s in enumerate(asset_set)}

    ### グラフに呼出元資産から呼出先資産に向かう辺として関連性の情報を追加する
    ### 例えば 関連性に DXDAIKOU CALL JXDAIKOU があったときは
    ### relation_graph[1] のリストには JXDAIKOUの数字 2 が入って relation_graph[1] = [(2,xxx),(y,zzz)] みたいになっている 
    n = len(asset_set)
    relation_graph = [[] for i in range(n)]
    for i,(fr,_,to,_) in enumerate(relation_list):
        fr_true = check_module_name(fr)
        find = name_dic[fr_true]
        tind = name_dic[to]
        relation_graph[find].append((tind,i))
        
    return relation_graph,relation_list,name_dic,rev_name_dic,n


def search_related_asset(starting_asset_df,relation_graph,relation_list,name_dic,rev_name_dic,n):
    
    ### テスト実施単位から順番に関連資産を作成する
    ### やり方はグラフに対する 幅優先探索(BFS = Bred First Search) 基本的はアルゴリズムなので必要があれば検索してみると良いです。
    
    visited_id = [-1]*n
    visited_id_batch = [-1]*n
    related_asset = set()
    for i,(test_id,source,info) in enumerate(zip(starting_asset_df["TEST_ID"],starting_asset_df["実行JOB"],starting_asset_df["補足"])):
        ### source = 起点資産が資産関連性情報の呼出元、呼出先にいない場合は 変換表で name_dic[source] でアクセスするとエラーになるため (配列外参照のようなこと)、最初に処理する
        
        if source not in name_dic:
            related_asset.add((test_id,source,info))
            continue
        sind = name_dic[source]
        q = deque([sind])
        q_batch = deque([])
        related_asset.add((test_id,source,info))
        visited_id[sind] = i

        while q:
            now = q.pop()
        
            for nex,nind in relation_graph[now]:
                
                if visited_id[nex] == i:
                    continue
                visited_id[nex] = i
 
                received = relation_list[nind][3]
                info_tmp = info
                if received == "JCL":
                    info_tmp = "BAT"
                nname = rev_name_dic[nex]

                related_asset.add((test_id,nname,info_tmp))
                if received == "JCL" and info != info_tmp:
                    q_batch.append(nex)
                else:
                    q.append(nex)
        
        info_tmp = "BAT"
        while q_batch:
            now = q_batch.pop()
        
            for nex,nind in relation_graph[now]:
                
                if visited_id_batch[nex] == i:
                    continue
                visited_id_batch[nex] = i
 
                received = relation_list[nind][3]
                nname = rev_name_dic[nex]

                related_asset.add((test_id,nname,info_tmp))
                q_batch.append(nex)
                

    return related_asset


def make_matching_related_asset_with_received_list(all_related_asset,received_asset_dic):
    
    related_asset_with_type_list = []
    for test_id,asset,info in all_related_asset:
        if asset not in received_asset_dic:
            related_asset_with_type_list.append([test_id,asset,"",info,"","",""])
            continue
        
        for data in received_asset_dic[asset]:
            new_list = [test_id,asset,"",info]
            new_list[2] = data[0]
            new_list += data[1:]
            related_asset_with_type_list.append(new_list)
                
    return related_asset_with_type_list

   
def make_asset_inventory_group(inventory_template_df,inventory_id_matching_dic,inventory_key_matching_dic,additional_screen_asset_list_all,starting_asset_merge_list,df_revival_asset,gr_info,adl_definition_dic,old_inventory_path):
    
    asset_inventory_group = inventory_template_df.values.tolist()
    
    batch_index = asset_inventory_header.index("バッチ資産")
    online_index = asset_inventory_header.index("オンライン資産")
    asset_inventory_before_index = asset_inventory_header.index("棚卸判定(前回)")
    
    ### 前回の棚卸資産一覧の情報を更新
    inventory_asset_folder_path = os.path.join(old_inventory_path)
    inventory_asset_folder_files = glob_files(inventory_asset_folder_path)
    
    file_name = ""
    for invntory_asset_file in inventory_asset_folder_files:
        if gr_info not in invntory_asset_file or "棚卸用資産一覧" not in invntory_asset_file:
            continue
        file_name = invntory_asset_file
        
    if file_name == "":
        print("There is no file of path asset inventory of {}.".format(gr_info))
    else:
        inventory_asset_before_df = pd.read_excel(file_name,sheet_name="棚卸用資産一覧",header=0)
        inventory_asset_before_df.fillna("",inplace=True)
        inventory_asset_before_keys = inventory_asset_before_df.columns.tolist()

        for i in range(len(inventory_asset_before_df)):
            data = inventory_asset_before_df.iloc[i]
            key,is_batch_asset,is_online_asset = data["KEY2"],data["バッチ資産"],data["オンライン資産"]
            if "棚卸判定" in inventory_asset_before_keys:
                judge_inventory = data["棚卸判定"]
            else:
                judge_inventory = ""
            if key not in inventory_key_matching_dic:
                continue
  
            for ind in inventory_key_matching_dic[key]:
                asset_inventory_group[ind][batch_index] = is_batch_asset
                asset_inventory_group[ind][online_index] = is_online_asset
                asset_inventory_group[ind][asset_inventory_before_index] = judge_inventory
    
    
    judge_used_index = asset_inventory_header.index("利用判定")
    batch_asset_index = asset_inventory_header.index("バッチ判定")
    online_asset_index = asset_inventory_header.index("オンライン判定")
    
    batch_asset_screen_index = asset_inventory_header.index("画面追加移行対象資産(バッチ利用)")
    online_asset_screen_index = asset_inventory_header.index("画面追加移行対象資産(オンライン利用)")
    
    
    ### 画面追加移行対象資産からの関連資産のオンバッチ情報の更新
    for screen_asset_list in additional_screen_asset_list_all:
        asset = screen_asset_list[1]
        onbatch = screen_asset_list[3]
        
        if asset not in inventory_id_matching_dic:
            continue
        
        if onbatch == "ON":
            for ind in inventory_id_matching_dic[asset]:
                asset_inventory_group[ind][online_asset_screen_index] = "○"
                asset_inventory_group[ind][judge_used_index] = "○"
                asset_inventory_group[ind][online_asset_index] = "○"
        elif onbatch == "BAT":
            for ind in inventory_id_matching_dic[asset]:
                asset_inventory_group[ind][batch_asset_screen_index] = "○"
                asset_inventory_group[ind][judge_used_index] = "○"
                asset_inventory_group[ind][batch_asset_index] = "○"
                
    ### 起点資産マージシートからの関連資産のオンバッチ情報の更新
    for asset_list in starting_asset_merge_list:
        asset = asset_list[0]
        starting_asset_check = asset_list[2]
        onbatch = asset_list[3]
        
        if asset not in inventory_id_matching_dic:
            continue
        
        for ind in inventory_id_matching_dic[asset]:
            if asset_inventory_group[ind][judge_used_index] != "◎":
                asset_inventory_group[ind][judge_used_index] = starting_asset_check
                
            if onbatch == "ON":
                if asset_inventory_group[ind][online_asset_index] != "◎":
                    asset_inventory_group[ind][online_asset_index] = starting_asset_check
                    
            elif onbatch == "BAT":
                if asset_inventory_group[ind][batch_asset_index] != "◎":
                    asset_inventory_group[ind][batch_asset_index] = starting_asset_check
      
      
    ### 復活資産の情報の更新              
    revival_index = asset_inventory_header.index("復活資産")
    
    for revival_list in df_revival_asset:
        asset = revival_list[1]
        
        if asset in inventory_id_matching_dic:
            for ind in inventory_id_matching_dic[asset]:
                asset_inventory_group[ind][revival_index] = "○"
                if asset_inventory_group[ind][judge_used_index] != "◎":
                    asset_inventory_group[ind][judge_used_index] = "○"
            
        elif asset in adl_definition_dic:
            for asset_name in adl_definition_dic[asset]:
                if asset_name in inventory_id_matching_dic:
                    for ind in inventory_id_matching_dic[asset_name]:
                        asset_inventory_group[ind][revival_index] = "○"
                        if asset_inventory_group[ind][judge_used_index] != "◎":
                            asset_inventory_group[ind][judge_used_index] = "○"
                
    
    asset_inventory_index = asset_inventory_header.index("棚卸判定")
    
    asset_system_index = asset_inventory_header.index("資産利用システム")
    asset_need_index = asset_inventory_header.index("資産要否(合成結果)")
    asset_source_index = asset_inventory_header.index("資産分類(ACN)")
    
    if gr_info in asset_inventory_header:
        gr_key_index = asset_inventory_header.index(gr_info)
    else:
        if gr_info != "Gr1":
            print("Error group info is something wrong at {}".format(gr_info))
        else:
            gr_key_index = asset_inventory_header.index("Gr1(形鋼)")
            
            
    for i in range(len(asset_inventory_group)):
        if asset_inventory_group[i][judge_used_index] == "":
            continue
        
        if asset_inventory_group[i][batch_asset_index] != "":
            asset_inventory_group[i][batch_index] = "○"
    
        if asset_inventory_group[i][online_asset_index] != "":
            asset_inventory_group[i][online_index] = "○"
            
        system_info = asset_inventory_group[i][asset_system_index]
        need_info = asset_inventory_group[i][asset_need_index]
        source_info = asset_inventory_group[i][asset_source_index]
        
        if system_info == "26) 基盤" or system_info == "":
            asset_inventory_group[i][asset_inventory_index] = "× 資産利用システム: 空白 or 基盤"
            continue
        
        if need_info == "廃止済" or need_info == "対象外":
            asset_inventory_group[i][asset_inventory_index] = "× 資産要否: 廃止済 or 対象外"
            continue
        
        if source_info == "富士通Utility・富士通提供ツール":
            asset_inventory_group[i][asset_inventory_index] = "× 資産分類: 連携対象外資産"
            continue
        
        if asset_inventory_group[i][gr_key_index] == "":
            asset_inventory_group[i][asset_inventory_index] = "× Gr分類: 他Gr判定資産"
            continue
        
        asset_inventory_group[i][asset_inventory_index] = "○"
        
        
    return asset_inventory_group

    
def output_asset_inventory_group(inventory_template_df,inventory_id_matching_dic,inventory_key_matching_dic,screen_asset_list,starting_point_merge_path,base_path,setting_file_path,gr_key,gr_info,title,old_inventory_path):
    
    ### 関連性情報とADL定義の情報を取得する
    relations_group_df,adl_definition_dic = make_relations_group_and_adl_definition_list(base_path,gr_info)
    
    ### 起点資産となるIDの一覧を取得する
    starting_asset_set = make_relations_group_starting_point(starting_point_merge_path,gr_info)
    
    ### 受領資産一覧の情報を取得する
    received_asset_dic = make_received_asset_dic(base_path,gr_info)
      
    ### 顧客別_資産関連性情報からグラフを作成する
    relation_graph,relation_list,name_dic,rev_name_dic,n = make_search_graph(relations_group_df)
    
    ### Grでの起点一覧を取得
    starting_asset_df = make_starting_asset_df(base_path,gr_info)
    
    ### 起点一覧からの関連資産を取得
    all_related_asset = search_related_asset(starting_asset_df,relation_graph,relation_list,name_dic,rev_name_dic,n)
    
    ### 受領資産一覧とマッチングした関連資産一覧を取得
    related_asset_with_received_info = make_matching_related_asset_with_received_list(all_related_asset,received_asset_dic)
    
    ### 起点資産マージシート用の情報を取得
    starting_asset_merge_list = make_starting_asset_merge(related_asset_with_received_info,starting_asset_set,gr_info)
    
    ### 追加対象画面資産からの情報を取得
    asset_all_used_gr_set = set([lis[1] for lis in related_asset_with_received_info])
    
    additional_screen_asset_list,screen_asset_starting_point = make_additional_screen_related_asset(screen_asset_list,gr_key,gr_info,asset_all_used_gr_set)
    
    additional_screen_related_asset = search_related_asset(screen_asset_starting_point,relation_graph,relation_list,name_dic,rev_name_dic,n)
    
    additional_screen_related_asset_with_received_info = make_matching_related_asset_with_received_list(additional_screen_related_asset,received_asset_dic)
    
    ### 復活資産の情報を取得
    df_revival_asset = get_df_revival_asset(setting_file_path,gr_info)
    df_revival_asset = df_revival_asset.values.tolist()
    
    
    asset_inventory_gr = make_asset_inventory_group(inventory_template_df,inventory_id_matching_dic,inventory_key_matching_dic,additional_screen_related_asset_with_received_info,starting_asset_merge_list,df_revival_asset,gr_info,adl_definition_dic,old_inventory_path)  
    
    gr_name = gr_info
    if "Gr5" in gr_name:
        gr_name = "Gr5"
    if "Gr6" in gr_name:
        gr_name = "Gr6"
    if "Gr7" in gr_name:
        gr_name = "Gr7"
        
    file_name = "棚卸用資産一覧_"+gr_info+"_"+dt_now+".xlsx"
    out_title = os.path.join(title,gr_name)
    
    if os.path.isdir(out_title) == False:
        os.makedirs(out_title)
        
    write_excel_multi_sheet(file_name,[asset_inventory_gr,additional_screen_asset_list,additional_screen_related_asset_with_received_info,df_revival_asset,starting_asset_merge_list,related_asset_with_received_info],["棚卸用資産一覧","追加移行対象画面","追加移行対象画面からの関連資産一覧","復活資産","起点資産マージ","関連資産一覧"],out_title,[asset_inventory_header,screen_asset_header,related_asset_header,revival_asset_header,starting_asset_merge_header,related_asset_header])

 
def main(member_list_path, starting_point_merge_path,setting_file_path, asset_inventory_template_path,base_path,old_inventory_path,title):

    if os.path.isdir(title) == False:
        os.makedirs(title)        
    
    inventory_template_df,inventory_id_matching_dic,inventory_key_matching_dic = make_inventory_template(asset_inventory_template_path)
    screen_asset_list = make_screen_asset_and_judge_from_member_list(member_list_path)

    base_path_files = glob_files(base_path)
    
    for file_path in base_path_files:
        if "起点情報" not in file_path:
            continue
        
        gr_info = file_path.split("_")[1]
        gr_key = groups_key_list[groups_info_list.index(gr_info)]
        print("{}の棚卸用資産一覧の作成を開始します。".format(gr_info))
        output_asset_inventory_group(inventory_template_df,inventory_id_matching_dic,inventory_key_matching_dic,screen_asset_list,starting_point_merge_path,base_path,setting_file_path,gr_key,gr_info,title,old_inventory_path)
          
if __name__ == "__main__":

    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7])
    
    ### 引数1 DBPath 引数2 出力フォルダ 