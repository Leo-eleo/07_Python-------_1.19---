#!/usr/bin/env python
# -*- coding: cp932 -*-
from hashlib import new
import sys
import os
import pyodbc
import pandas as pd
import datetime

from collections import deque

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

dt_now = str(datetime.date.today())



# groups_list = ["Gr1(形鋼・基盤・その他)","Gr1(形鋼)","Gr1(基盤)","Gr1(その他)","Gr2","Gr3","Gr4","Gr5(冷延・電磁・出荷)","Gr5(冷延)","Gr5(電磁)","Gr5(出荷)","Gr6","Gr7"]

same_modules = ["コイル","スラブ","形鋼","計画","材試","熱延","熱仕"]
same_modules_group = ["Gr6","Gr6","Gr1","Gr6","Gr3","Gr6","Gr6"]
# len_groups = len(groups_list)
all_starting_asset_header = ["TEST_ID","実行順序","実行JOB","補足","出力フォルダ"]


groups_key_list = ["Gr1(形鋼・基盤・その他)","Gr2","Gr3","Gr4","Gr5(冷延・電磁・出荷)","Gr5(冷延・電磁・出荷)","Gr5(冷延・電磁・出荷)",\
                    "Gr6(管理系・操業系)","Gr6(管理系・操業系)",\
                    "Gr7(製鋼系・棒線系・条鋼出荷系)","Gr7(製鋼系・棒線系・条鋼出荷系)","Gr7(製鋼系・棒線系・条鋼出荷系)","Gr7(製鋼系・棒線系・条鋼出荷系)","Gr7(製鋼系・棒線系・条鋼出荷系)"]
groups_info_list = ["Gr1","Gr2","Gr3","Gr4","Gr5(冷延)","Gr5(電磁)","Gr5(出荷)",\
                    "Gr6(管理系)","Gr6(操業系)","Gr7(製鋼系・管理系)","Gr7(製鋼系・操業系)","Gr7(棒線系・管理系)","Gr7(棒線系・操業系)","Gr7(条鋼出荷系・操業系)"
                    ]


comparizon_header = ["KEY2","登録者用資産ID","資産分類(ACN)","資産要否(合成結果)","資産利用システム","日本語名称"]
# group_all_use = ["○"]*len_groups
# group_all_empty = [""]*len_groups


asset_id_index = 1 ### 登録者用資産ID の index
reasons_index = 6 ### 差分の理由を記載するindex

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

def make_relations_group(base_path,gr_info):
    
    search_path = os.path.join(base_path)
    folder_files = glob_files(search_path)
    
    for file_path in folder_files:
        if "顧客別_資産関連性情報" not in file_path or gr_info not in file_path:
            continue
        relations_group_df = pd.read_excel(file_path,sheet_name="顧客別_資産関連性情報")
        relations_group_df.fillna("",inplace=True)
        relations_group_df = relations_group_df[relations_group_df["暫定無効FLG"] != "○"]
        
        return relations_group_df
    
    print("Error, there is no file of relations on {} in {}".format(gr_info,base_path))
    return pd.DataFrame([])

    
def make_relation_merge_set(base_path):
    
    base_files = glob_files(base_path)
    relation_merge_set = set()
    for file in base_files:
        if "資産関連性調査結果マージ版" not in file:
            continue
        df_relation_merge = pd.read_excel(file,sheet_name=None)  
        df_sheet_list = df_relation_merge.keys()
        for sheetname in df_sheet_list:
            if "資産関連性調査結果" not in sheetname:
                continue
            df = df_relation_merge[sheetname]
            df.fillna("",inplace=True)
            for source_from,relation_type,source_to in zip(df["呼出元資産（メンバのみ）"],df["呼び出し方法"],df["呼び出し先資産"]):
                relation_merge_set.add((source_from,relation_type,source_to))
            
    for file in base_files:
        if "起点資産一覧" not in file:
            continue
        df = pd.read_excel(file,sheet_name="起点資産関連性",header=1)  
        df.fillna("",inplace=True)
        for source_from,relation_type,source_to in zip(df["呼出元資産（メンバのみ）"],df["呼出方法"],df["呼出先資産"]):
            relation_merge_set.add((source_from,relation_type,source_to))
       
    if relation_merge_set:
        return relation_merge_set

    print("Error, there is no file of merged relations in {}".format(base_path))
    return pd.DataFrame([])


def make_starting_asset(new_path,gr_info):

    search_path = os.path.join(new_path)
    
    folder_files = glob_files(search_path)
    
    for file_path in folder_files:
        if "起点情報" not in file_path or gr_info not in file_path:
            continue
        
        df_received_asset = pd.read_excel(file_path,sheet_name="TEST_実施単位")
        starting_asset = set([asset for asset in df_received_asset["実行JOB"]])
        return starting_asset

    print("Error, there is no info of starting asset of {} in {}.".format(gr_info,new_path))
    return set()
   
  
    
def make_search_graph(df):
    
    
    asset_set = set() ### 呼出元 or 呼出先 の資産一覧を重複を除いて作成する

    relation_set = set() ### 顧客別_資産関連性情報から関連性の一覧を重複を除いて取得する

    for fr,relation_type,to in zip(df["呼出元資産"],df["呼出方法"],df["呼出先資産"]):
        fr_true = check_module_name(fr)
        asset_set.add(fr_true)
        
        asset_set.add(to)
        relation_set.add((fr,relation_type,to))
      

    asset_set = sorted(asset_set)
    relation_list = sorted(relation_set)

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
    for i,(fr,_,to) in enumerate(relation_list):
        fr_true = check_module_name(fr)
        find = name_dic[fr_true]
        tind = name_dic[to]
        relation_graph[find].append((tind,i))
        
    return relation_graph,relation_list,relation_set,name_dic,rev_name_dic,n


def search_path_target_asset(starting_asset_list,target_set,relation_graph,relation_list,name_dic,rev_name_dic,n):
    
    ### テスト実施単位から順番に関連資産を作成する
    ### やり方はグラフに対する 幅優先探索(BFS = Bred First Search) 基本的はアルゴリズムなので必要があれば検索してみると良いです。
    
    visited_id = [-1]*n
    path_par_id = [-1]*n
    target_path_dic = {}
    for i,source in enumerate(starting_asset_list):
        ### source = 起点資産が資産関連性情報の呼出元、呼出先にいない場合は 変換表で name_dic[source] でアクセスするとエラーになるため (配列外参照のようなこと)、最初に処理する
        
        if source not in name_dic:
            continue
        sind = name_dic[source]
        q = deque([sind])
        visited_id[sind] = i
        path_par_id[sind] = -1
        while q:
            now = q.popleft()
        
            for nex,nind in relation_graph[now]:
                
                if visited_id[nex] == i:
                    continue
                visited_id[nex] = i
                path_par_id[nex] = [now,nind]
              
                nname = rev_name_dic[nex]
                q.append(nex)
                
                if nname not in target_set:
                    continue
                
                target_set.remove(nname)
                
                target_path = []
                
                pos = nex
                while pos != sind:
                    npos,nind = path_par_id[pos]
                    target_path.append(relation_list[nind][:3])
                    pos = npos
                target_path = reversed(target_path)
                target_path_dic[nname] = target_path
        

    return target_path_dic


   
def make_exclude_set(base_path,gr_info):
    base_files = glob_files(base_path)
    for file in base_files:
        if "受領資産一覧作成処理_入力" not in file:
            continue
        
        df_exclude_all = pd.read_excel(file,sheet_name=None)  
        df_sheet_list = df_exclude_all.keys()
        
        exclude_all = set(df_exclude_all["運用系JCL_完全除外"]["除外資産名"].values.tolist())
        exclude_to_source = set(df_exclude_all["除外資産_Gr共通"]["除外資産名"].values.tolist())
        
        sheet_name = "除外資産_" + gr_info
        if sheet_name in df_sheet_list:
            exclude_group = set(df_exclude_all[sheet_name]["除外資産名"].values.tolist())
        else:
            exclude_group = set()
            
        return exclude_all|exclude_to_source|exclude_group
    
    return set()

 
def update_from_revival_asset(additions_asset,deletions_asset,new_revival_asset_list,old_revival_asset_list):
    
    new_revival_asset_set = set([revival_asset for revival_asset in new_revival_asset_list["登録者用資産ID"]])
    old_revival_asset_set = set([revival_asset for revival_asset in old_revival_asset_list["登録者用資産ID"]])

    additions_revival_asset = set()
    deletions_revival_asset = set()
    for asset in new_revival_asset_set:
        if asset not in old_revival_asset_set:
            additions_revival_asset.add(asset)
            
    for asset in old_revival_asset_set:
        if asset not in new_revival_asset_set:
            deletions_revival_asset.add(asset)
            
            
    for i in range(len(additions_asset)):
        if additions_asset[i][reasons_index] != "":
            continue
        if additions_asset[i][asset_id_index] in additions_revival_asset:
            additions_asset[i][reasons_index] = "復活資産の追加"
            
    for i in range(len(deletions_asset)):
        if deletions_asset[i][reasons_index] != "":
            continue
        if deletions_asset[i][asset_id_index] in deletions_revival_asset:
            deletions_asset[i][reasons_index] = "復活資産の削除"
    
    return additions_asset,deletions_asset


def update_from_exclude_asset(additions_asset,deletions_asset,new_exclude_set,old_exclude_set):
    
    for i in range(len(additions_asset)):
        if additions_asset[i][reasons_index] != "":
            continue
        asset_id = additions_asset[i][asset_id_index]
        if asset_id in old_exclude_set and asset_id not in new_exclude_set:
            additions_asset[i][reasons_index] = "除外資産の削除"
            
    for i in range(len(deletions_asset)):
        if deletions_asset[i][reasons_index] != "":
            continue
        asset_id = deletions_asset[i][asset_id_index]
        if asset_id in new_exclude_set and asset_id not in old_exclude_set:
            deletions_asset[i][reasons_index] = "除外資産の追加"
    
    return additions_asset,deletions_asset


def update_from_starting_asset(additions_asset,deletions_asset,new_starting_asset,old_starting_asset,new_additions_screen_asset,old_additions_screen_asset):
    
    new_all_asset = new_starting_asset | new_additions_screen_asset
    old_all_asset = old_starting_asset | old_additions_screen_asset
    for i in range(len(additions_asset)):
        if additions_asset[i][reasons_index] != "":
            continue
        asset_id = additions_asset[i][asset_id_index]
        if asset_id in new_starting_asset and asset_id not in old_all_asset:
            additions_asset[i][reasons_index] = "起点資産の追加"
            
        elif asset_id in new_additions_screen_asset and asset_id not in old_all_asset:
            additions_asset[i][reasons_index] = "起点資産の追加_追加移行対象画面資産"
            
    for i in range(len(deletions_asset)):
        if deletions_asset[i][reasons_index] != "":
            continue
        asset_id = deletions_asset[i][asset_id_index]
        if asset_id in old_starting_asset and asset_id not in new_all_asset:
            deletions_asset[i][reasons_index] = "起点資産の削除"
            
        elif asset_id in old_additions_screen_asset and asset_id not in new_all_asset:
            deletions_asset[i][reasons_index] = "起点資産の削除_追加移行対象画面資産"
    
    return additions_asset,deletions_asset

def update_from_related_asset(additions_asset,deletions_asset,new_starting_asset,old_starting_asset,new_additions_screen_asset,old_additions_screen_asset,new_relations_group_df,old_relations_group_df,new_relation_merge_set,old_relation_merge_set,new_exclude_set,old_exclude_set):
    
    ### 顧客別_資産関連性情報からグラフを作成する
    new_relation_graph,new_relation_list,new_relation_set,new_name_dic,new_rev_name_dic,new_n = make_search_graph(new_relations_group_df)
    old_relation_graph,old_relation_list,old_relation_set,old_name_dic,old_rev_name_dic,old_n = make_search_graph(old_relations_group_df)
    
    new_starting_asset |= new_additions_screen_asset
    old_starting_asset |= old_additions_screen_asset
    
    additions_target = set()
    for i in range(len(additions_asset)):
        if additions_asset[i][reasons_index] != "":
            continue
        additions_target.add(additions_asset[i][asset_id_index])
        
    
    additions_path_dic = search_path_target_asset(new_starting_asset,additions_target,new_relation_graph,new_relation_list,new_name_dic,new_rev_name_dic,new_n)
    
    for i in range(len(additions_asset)):
        if additions_asset[i][reasons_index] != "":
            continue
        asset = additions_asset[i][asset_id_index]
        
        if asset not in additions_path_dic:
            additions_asset[i][reasons_index] = "原因不明"
            continue
        asset_relation_path = additions_path_dic[asset]

        for num,(source_from,relation_type,source_to) in enumerate(asset_relation_path):
            
            if num == 0 and source_from not in old_starting_asset:
                additions_asset[i][reasons_index] = "起点資産の追加: " + source_from
                break
            relation_tuple = (source_from,relation_type,source_to)
            if relation_tuple in old_relation_set:
                continue
            
            if source_from in old_exclude_set:
                additions_asset[i][reasons_index] = "除外資産の削除による関連性の追加"+source_from+": " + source_from + "→" + source_to + " 関連性=" + relation_type
                break
            
            if source_to in old_exclude_set: 
                additions_asset[i][reasons_index] = "除外資産の削除による関連性の追加"+source_to+": " + source_from + "→" + source_to + " 関連性=" + relation_type
                break
            
            if relation_tuple not in old_relation_merge_set:
                additions_asset[i][reasons_index] = "関連性の追加: " + source_from + "→" + source_to + " 関連性=" + relation_type
                break 
            else:
                additions_asset[i][reasons_index] = "メンバ一覧の更新による関連性Grの変更: " + source_from + "→" + source_to + " 関連性=" + relation_type
                break
        if additions_asset[i][reasons_index] == "":
            additions_asset[i][reasons_index] = "原因不明"
    
    
    deletions_target = set()
    for i in range(len(deletions_asset)):
        if deletions_asset[i][reasons_index] != "":
            continue
        deletions_target.add(deletions_asset[i][asset_id_index])
        
    deletions_path_dic = search_path_target_asset(old_starting_asset,deletions_target,old_relation_graph,old_relation_list,old_name_dic,old_rev_name_dic,old_n)
    
    for i in range(len(deletions_asset)):
        if deletions_asset[i][reasons_index] != "":
            continue
        asset = deletions_asset[i][asset_id_index]
        
        if asset not in deletions_path_dic:
            deletions_asset[i][reasons_index] = "原因不明"
            continue
        
        asset_relation_path = deletions_path_dic[asset]
        
        
        for num,(source_from,relation_type,source_to) in enumerate(asset_relation_path):
            
            if num == 0 and source_from not in new_starting_asset:
                deletions_asset[i][reasons_index] = "起点資産の削除: " + source_from
                break
            
            relation_tuple = (source_from,relation_type,source_to)
            if relation_tuple in new_relation_set:
                continue
            
            if source_from in new_exclude_set:
                deletions_asset[i][reasons_index] = "除外資産の追加による関連性の削除"+source_from+": " + source_from + "→" + source_to + " 関連性=" + relation_type
                break
            
            if source_to in new_exclude_set: 
                deletions_asset[i][reasons_index] = "除外資産の追加による関連性の削除"+source_to+": " + source_from + "→" + source_to + " 関連性=" + relation_type
                break
            
            if relation_tuple not in new_relation_merge_set:
                deletions_asset[i][reasons_index] = "関連性の削除: " + source_from + "→" + source_to + " 関連性=" + relation_type
                break 
            else:
                deletions_asset[i][reasons_index] = "メンバ一覧の更新による関連性Grの変更: " + source_from + "→" + source_to + " 関連性=" + relation_type
                break
        if deletions_asset[i][reasons_index] == "":
            deletions_asset[i][reasons_index] = "原因不明"
    
    return additions_asset,deletions_asset
def comparizon_asset_inventory_group(new_path,old_path,gr_key,gr_info,title,new_relation_merge_set,old_relation_merge_set):
    
    new_files = glob_files(new_path)
    old_files = glob_files(old_path)
    
    new_asset_inventory_df = []
    old_asset_inventory_df = []
    for new_file in new_files:
        if "棚卸用資産一覧" not in new_file or gr_info not in new_file:
            continue
        
        new_asset_inventory_df = pd.read_excel(new_file,sheet_name=None)
        
    for old_file in old_files:
        if "棚卸用資産一覧" not in old_file or gr_info not in old_file:
            continue
        
        old_asset_inventory_df = pd.read_excel(old_file,sheet_name=None)
    
    
    if old_asset_inventory_df == []:
        print("棚卸用資産一覧 {} には古い情報が {} に存在しないため、比較解析をスキップします。".format(gr_info,old_path))
        
        return 1
    
    
    new_asset_inventory_main = new_asset_inventory_df["棚卸用資産一覧"]
    old_asset_inventory_main = old_asset_inventory_df["棚卸用資産一覧"]
    
    new_asset_inventory_main.fillna("",inplace=True)
    old_asset_inventory_main.fillna("",inplace=True)
    
    new_asset_inventory_main_matching_dic = {new_asset_inventory_main.iloc[i]["KEY2"]:new_asset_inventory_main.iloc[i] for i in range(len(new_asset_inventory_main))}
    old_asset_inventory_main_all_set = set([old_asset_inventory_main.iloc[i]["KEY2"] for i in range(len(old_asset_inventory_main))])
    new_asset_inventory_used_asset_list = new_asset_inventory_main[new_asset_inventory_main["利用判定"] != ""]
    old_asset_inventory_used_asset_list = old_asset_inventory_main[old_asset_inventory_main["利用判定"] != ""]
    new_asset_inventory_used_asset_set = set([key for key in new_asset_inventory_used_asset_list["KEY2"]])
    old_asset_inventory_used_asset_set = set([key for key in old_asset_inventory_used_asset_list["KEY2"]])
    
    additions_asset = []
    deletions_asset = []
    
    for asset in new_asset_inventory_used_asset_set:
        if asset not in old_asset_inventory_used_asset_set:
            if asset not in old_asset_inventory_main_all_set:
                data = new_asset_inventory_main_matching_dic[asset]
                values = [data[key] for key in comparizon_header]
                values.extend(["新規受領資産",""])
                additions_asset.append(values)
            else:
                
                data = new_asset_inventory_main_matching_dic[asset]
                values = [data[key] for key in comparizon_header]
                values.extend(["",""])
                additions_asset.append(values)
            
    for asset in old_asset_inventory_used_asset_set:
        if asset not in new_asset_inventory_used_asset_set:
            if asset in new_asset_inventory_main_matching_dic:
                data = new_asset_inventory_main_matching_dic[asset]
                values = [data[key] for key in comparizon_header]
                values.extend(["",""])
            else:
                values = [asset,"棚卸用資産一覧最新版にデータなし","","","",""]
                values.extend(["",""])
            deletions_asset.append(values)
    
    
    
    new_revival_asset_list = new_asset_inventory_main[new_asset_inventory_main["復活資産"] == "○"]
    old_revival_asset_list = old_asset_inventory_main[old_asset_inventory_main["復活資産"] == "○"]
    
    additions_asset,deletions_asset = update_from_revival_asset(additions_asset,deletions_asset,new_revival_asset_list,old_revival_asset_list)
    
    new_exclude_set = make_exclude_set(new_path,gr_info)
    old_exclude_set = make_exclude_set(old_path,gr_info)
    additions_asset,deletions_asset = update_from_exclude_asset(additions_asset,deletions_asset,new_exclude_set,old_exclude_set)
    
    
    ### Grでの起点一覧を取得
    new_starting_asset = make_starting_asset(new_path,gr_info)
    old_starting_asset = make_starting_asset(old_path,gr_info)
    
    new_additions_screen_asset = new_asset_inventory_df["追加移行対象画面"]
    old_additions_screen_asset = old_asset_inventory_df["追加移行対象画面"]
    
    new_additions_screen_asset = set([asset_id for asset_id in new_additions_screen_asset["登録者用資産ID"]])
    old_additions_screen_asset = set([asset_id for asset_id in old_additions_screen_asset["登録者用資産ID"]])
    
    additions_asset,deletions_asset = update_from_starting_asset(additions_asset,deletions_asset,new_starting_asset,old_starting_asset,new_additions_screen_asset,old_additions_screen_asset)
    
    
    
    ### 関連性情報を取得する
    new_relations_group_df = make_relations_group(new_path,gr_info)
    old_relations_group_df = make_relations_group(old_path,gr_info)
    
    additions_asset,deletions_asset = update_from_related_asset(additions_asset,deletions_asset,new_starting_asset,old_starting_asset,new_additions_screen_asset,old_additions_screen_asset,new_relations_group_df,old_relations_group_df,new_relation_merge_set,old_relation_merge_set,new_exclude_set,old_exclude_set)
    
      
    
    gr_name = gr_info
    if "Gr5" in gr_name:
        gr_name = "Gr5"
    if "Gr6" in gr_name:
        gr_name = "Gr6"
    if "Gr7" in gr_name:
        gr_name = "Gr7"
        
    file_name = "棚卸増減資産一覧_"+gr_info+"_"+dt_now+".xlsx"
    out_title = os.path.join(title,gr_name)
    
    comp_header = comparizon_header + ["移行判定変動理由","移行判定変動理由詳細"]
    if os.path.isdir(out_title) == False:
        os.makedirs(out_title)
        
    write_excel_multi_sheet(file_name,[additions_asset,deletions_asset],["増加資産一覧","減少資産一覧",],out_title,[comp_header,comp_header])
 
def main(new_path,old_path,title):

    if os.path.isdir(title) == False:
        os.makedirs(title)        
    
    
    new_relation_merge_set = make_relation_merge_set(new_path)
    
    old_relation_merge_set = make_relation_merge_set(old_path)
    
    new_path_files = glob_files(new_path)
    
    for file_path in new_path_files:
        if "棚卸用資産一覧" not in file_path:
            continue
        
        gr_info = file_path.split("_")[1]
        gr_key = groups_key_list[groups_info_list.index(gr_info)]
        print("{}の棚卸増減資産一覧の作成を開始します。".format(gr_info))
        comparizon_asset_inventory_group(new_path,old_path,gr_key,gr_info,title,new_relation_merge_set,old_relation_merge_set)
          
if __name__ == "__main__":

    main(sys.argv[1],sys.argv[2],sys.argv[3])
    
    ### 引数1 DBPath 引数2 出力フォルダ 