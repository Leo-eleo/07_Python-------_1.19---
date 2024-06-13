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


def make_relations_group(base_path,gr_info,exclude_flg):
    
   
    search_path = os.path.join(base_path)
    folder_files = glob_files(search_path)
    
    for file_path in folder_files:
        if "顧客別_資産関連性情報" not in file_path or gr_info not in file_path:
            continue
        relations_group_df = pd.read_excel(file_path,sheet_name="顧客別_資産関連性情報")
        relations_group_df.fillna("",inplace=True)
        
        if exclude_flg:
            relations_group_df = relations_group_df[relations_group_df["暫定無効FLG"] != "○"]
        return relations_group_df
    
    
    print("Error, there is no file of relations on {} in {}".format(gr_info,base_path))
    return pd.DataFrame([]),[]



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

def output_related_asset_group(base_path,gr_key,gr_info,title,exclude_flg,file_path):
    
    ### 関連性情報とADL定義の情報を取得する
    relations_group_df = make_relations_group(base_path,gr_info,exclude_flg)
    
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
    
    gr_name = gr_info
    if "Gr5" in gr_name:
        gr_name = "Gr5"
    if "Gr6" in gr_name:
        gr_name = "Gr6"
    if "Gr7" in gr_name:
        gr_name = "Gr7"
        
    file_suffix = os.path.split(file_path)[-1]
    file_suffix = file_suffix[file_suffix.index("_"):]
    file_name = "関連資産一覧"+file_suffix
    out_title = os.path.join(title,gr_name)
    
    if os.path.isdir(out_title) == False:
        os.makedirs(out_title)
        
    write_excel_multi_sheet(file_name,[related_asset_with_received_info],["関連資産一覧"],out_title,[related_asset_header])

 
def main(base_path,title,exclude_flg):
    if type(exclude_flg) == str:
        exclude_flg = exclude_flg == "True"
        
    if os.path.isdir(title) == False:
        os.makedirs(title)        
    
    base_path_files = glob_files(base_path)
    
    for file_path in base_path_files:
        if "起点情報" not in file_path:
            continue

        gr_info = file_path.split("_")[-2]
        gr_key = groups_key_list[groups_info_list.index(gr_info)]
        print("{}の関連資産一覧の作成を開始します。".format(gr_info))
        output_related_asset_group(base_path,gr_key,gr_info,title,exclude_flg,file_path)
        
if __name__ == "__main__":

    main(sys.argv[1],sys.argv[2],sys.argv[3])
    
    ### 引数1 DBPath 引数2 出力フォルダ 