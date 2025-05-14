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


groups_list = ["Gr1(形鋼・基盤・その他)","Gr1(形鋼)","Gr1(基盤)","Gr1(その他)","Gr2","Gr3","Gr4","Gr5(冷延・電磁・出荷)","Gr5(冷延)","Gr5(電磁)","Gr5(出荷)","Gr6","Gr7"]

same_modules = ["コイル","スラブ","形鋼","計画","材試","熱延","熱仕"]
same_modules_group = ["Gr6","Gr6","Gr1","Gr6","Gr3","Gr6","Gr6"]
len_groups = len(groups_list)

group_all_use = ["○"]*len_groups
group_all_empty = [""]*len_groups



def check_module_name(name):
    for module in same_modules:
        if module in name:
            return name[:name.find(module)]
    
    return name    

# def make_member_module_list(setting_path):
    
#     df_members = pd.read_excel(setting_path,sheet_name="メンバ一覧")
#     df_members.fillna("",inplace=True)
#     members_dic = {}
#     key_dic = {}    
    
#     for x in range(len(df_members)):
#         data = df_members.iloc[x]
#         asset,module, = data["KEY2"],data["モジュールID"]
#         gr = [data[s] for s in groups_list]

#         asset = take_extensions(asset)
#         if module not in members_dic:
#             members_dic[module] = []
            
#         members_dic[module].append(gr)

#         if asset not in key_dic:
#             key_dic[asset] = []
#         key_dic[asset].append(gr)
    
#     return members_dic,key_dic


def make_relations_group(relations_merge_path):
    
    relations_group_info_dic = {}
    
    df_all = pd.read_excel(relations_merge_path,sheet_name=None)
    
    df_sheet_list = df_all.keys()
    
    for sheet in df_sheet_list:
        if "資産関連性調査結果" not in sheet:
            continue
        df = df_all[sheet]
        df.fillna("",inplace=True)
        
        for i in range(len(df)):
            data = df.iloc[i]
            
            relation_group_info = [data[gr] for gr in groups_list]
            source_from,relation,source_to = data["呼出元資産（メンバのみ）"],data["呼び出し方法"],data["呼び出し先資産"]
            
            if (source_from,relation,source_to) not in relations_group_info_dic:
                relations_group_info_dic[(source_from,relation,source_to)] = group_all_empty[:]
                
            for j in range(len_groups):
                if relation_group_info[j] == "○":
                    relations_group_info_dic[(source_from,relation,source_to)][j] = "○"
    
    return relations_group_info_dic


def make_received_asset_dic(conn):
    
    sql = "SELECT * FROM 顧客別_受領資産一覧_汎用版"
    df_received_asset = pd.read_sql(sql,conn)
    
    df_received_asset.fillna("",inplace=True)
    received_asset_dic = {}
    for i in range(len(df_received_asset)):
        data = df_received_asset.iloc[i].to_list()
        source = data[0]
        # source = data["資産ID"]
        if source not in received_asset_dic:
            received_asset_dic[source] = set()
        
        
        received_asset_dic[source].add(tuple(data[1:]))
        
    return received_asset_dic


    
def main(db_name,title,relations_merge_path):
    

    if os.path.isdir(title) == False:
        os.makedirs(title)
        
    
    # members_dic,key_dic = make_member_module_list(setting_path)
    
    relations_group_info_dic = make_relations_group(relations_merge_path)
    conn = connect_accdb(db_name)
    cursor = conn.cursor()
    
    sql = "SELECT * FROM 顧客別_受領資産一覧_汎用版"
    df_received_asset = pd.read_sql(sql,conn)
    
    df_received_asset.fillna("",inplace=True)
    received_asset_dic = {}
    for i in range(len(df_received_asset)):
        data = df_received_asset.iloc[i]
        source = data["資産ID"]
        if source not in received_asset_dic:
            received_asset_dic[source] = set()
        
        received_asset_dic[source].add(data["資産分類"])
        
    ### 顧客別_資産関連性情報からグラフを作成する

    ### 変更20191011
    sql =   """\
            SELECT * FROM 顧客別_資産関連性情報
            """
            
    
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)

    asset_set = set() ### 呼出元 or 呼出先 の資産一覧を重複を除いて作成する

    relation_list = set() ### 顧客別_資産関連性情報から関連性の一覧を重複を除いて取得する

    for fr,relation_type,to,received,data_from,valid_flg in zip(df["呼出元資産"],df["呼出方法"],df["呼出先資産"],df["受領判定"],df["登録分類"],df["暫定無効FLG"]):
        if valid_flg != "":
            continue
        
        fr_true = check_module_name(fr)
        asset_set.add(fr_true)
        
        asset_set.add(to)
        relation_list.add((fr,relation_type,to,received,valid_flg))
        
        if "関連性調査結果" not in data_from and (to not in received_asset_dic or received not in received_asset_dic[to]):
            # print(fr,relation_type,to,received)
            if to not in received_asset_dic:
                received_asset_dic[to] = set()
            received_asset_dic[to].add(received)
            
            sql,values = make_insert_sql("顧客別_受領資産一覧_汎用版",[to,received],["資産ID","資産分類"])
            cursor.execute(sql,values)
    

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
    relation_group_info = []
    for i,(fr,relation,to,_,valid_flg) in enumerate(relation_list):
        fr_true = check_module_name(fr)
        find = name_dic[fr_true]
        tind = name_dic[to]
        
        ### 暫定無効FLGが空欄なら valid_relation_flg = True
        ### メニュー画面なら False で起点のときだけ有効にするための flg を持つ
        if valid_flg == "":
            valid_relation_flg = True
        else:
            valid_relation_flg = False
            
        #####
            
        relation_graph[find].append((tind,i,valid_relation_flg))
        
        group_info_i = group_all_empty[:]
        
        if (fr,relation,to) in relations_group_info_dic:
            group_info_i = relations_group_info_dic[(fr,relation,to)]
            
        else:
            group_info_i = group_all_use[:]
            
            # if fr in members_dic:
            #     for gr_info in members_dic[fr]:
            #         for j in range(len_groups):
            #             if gr_info[j] == "○":
            #                 group_info_i[j] = "○"
                            
            # elif fr in key_dic:
            #     for gr_info in key_dic[fr]:
            #         for j in range(len_groups):
            #             if gr_info[j] == "○":
            #                 group_info_i[j] = "○"
            
            # elif fr != fr_true:
            #     for ind,module in enumerate(same_modules):
            #         if module in fr:
            #             sind = ind
            #             break
            #     for j in range(len_groups):
            #         if groups_list[j].startswith(same_modules_group[sind]):
            #             group_info_i[j] = "○"
            #     # print(fr,fr_true,group_info_i,same_modules_group[sind])
        
        if group_info_i[2] == "○" or group_info_i[3] == "○":
            group_info_i = group_all_use[:]
            
        for ind in range(len_groups):
            if group_info_i[ind] == "○":
                sgroup = groups_list[ind][:3]
                for j in range(len_groups):
                    if groups_list[j].startswith(sgroup):
                        group_info_i[j] = "○"
                    
       
        if "○" not in group_info_i:
            # print(fr,relation,to,_)
            group_info_i = group_all_use[:]
        # if group_info_i != group_info_i_old:
        #     print(fr,relation,to)
        #     print(group_info_i)
        #     print(group_info_i_old)
        

        relation_group_info.append(group_info_i)

    # グラフの完成
    ################################# 

    sql,_ = make_delete_sql("TEST_処理起点別関連資産2_JFE",[],[])
    cursor.execute(sql)
    sql,_ = make_delete_sql("TEST_処理起点別関連資産_JFE",[],[])
    cursor.execute(sql)
    
    ### 変更20191011
    sql =   """\
            SELECT * FROM TEST_テスト実施単位_UNIQUE_JFE
            """
            
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)
    
    print("グラフの作成が完了しました。")

  
    ### テスト実施単位から順番に関連資産を作成する
    ### やり方はグラフに対する 深さ優先探索(DFS = Depth First Search) 基本的はアルゴリズムなので必要があれば検索してみると良いです。

    ans_list_all = []
    visited_id = [-1]*n
    visited_id_batch = [-1]*n
    
    add_info_set = set()
    ans_list_all_dic = {}
    for i,(test_id,source,info,out_folder) in enumerate(zip(df["TEST_ID"],df["実行JOB"],df["補足"],df["出力フォルダ"])):
        ### source = 起点資産が資産関連性情報の呼出元、呼出先にいない場合は 変換表で name_dic[source] でアクセスするとエラーになるため (配列外参照のようなこと)、最初に処理する
        
        if out_folder in groups_list:
            group_id = groups_list.index(out_folder)
        else:
            group_id = -1
        # print(out_folder,group_id)
            
            

        if out_folder != "":
            out_title = os.path.join(title,out_folder)
        else:
            out_title = title
        
        
        
        if out_title not in ans_list_all_dic:
            ans_list_all_dic[out_title] = set()
        add_info_set = ans_list_all_dic[out_title]
        
        if source not in name_dic:
            add_info_set.add((test_id,source,info))
            continue
        sind = name_dic[source]
        q = deque([sind])
        q_batch = deque([])
        
        add_info_set.add((test_id,source,info))
        visited_id[sind] = i

        # add_info_set.add((test_id,source,info))
        while q:
            now = q.pop()
        
            for nex,nind,valid_relation_flg in relation_graph[now]:
                
                if group_id != -1 and relation_group_info[nind][group_id] != "○":
                    continue
                
                if valid_relation_flg == False and now != sind:
                    continue
                
                if visited_id[nex] == i:
                    continue
                visited_id[nex] = i
 
                received = relation_list[nind][3]
                info_tmp = info
                if received == "JCL":
                    info_tmp = "BAT"
                nname = rev_name_dic[nex]

                add_info_set.add((test_id,nname,info_tmp))
                if received == "JCL" and info != info_tmp:
                    q_batch.append(nex)
                else:
                    q.append(nex)


        info_tmp = "BAT"
        while q_batch:
            now = q_batch.pop()
        
            for nex,nind,valid_relation_flg in relation_graph[now]:
                
                if group_id != -1 and relation_group_info[nind][group_id] != "○":
                    continue
                
                if valid_relation_flg == False and now != sind:
                    continue
                
                if visited_id_batch[nex] == i:
                    continue
                visited_id_batch[nex] = i
 
                received = relation_list[nind][3]
                nname = rev_name_dic[nex]

                add_info_set.add((test_id,nname,info_tmp))
                q_batch.append(nex)

    received_asset_dic = make_received_asset_dic(conn)
 


    for out_title in ans_list_all_dic.keys():
        add_info_set = ans_list_all_dic[out_title]
        out_name = os.path.split(out_title)[-1]
        print(out_title,len(add_info_set),out_name)
        if os.path.isdir(out_title) == False:
            os.makedirs(out_title)
            
        
        
            
        ans_list_all = []
        for test_id,asset,info in add_info_set:
            if asset not in received_asset_dic:
                ans_list_all.append([test_id,asset,"",info,"","",""])
                continue
            
            for data in received_asset_dic[asset]:
                new_list = [test_id,asset,"",info]
                new_list[2] = data[0]
                new_list += data[1:]
                ans_list_all.append(new_list)
                

        print(len(ans_list_all))
        write_excel_multi_sheet("応用_テスト関連資産出力_" + out_name + ".xlsx",sorted(ans_list_all),"応用_テスト関連資産出力",out_title,["処理起点","関連資産","資産分類","オンバッチ分類","備考①","備考②","備考③"])
    
    
if __name__ == "__main__":

    main(sys.argv[1],sys.argv[2],sys.argv[3])
    
    ### 引数1 DBPath 引数2 出力フォルダ 