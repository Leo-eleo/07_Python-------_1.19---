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


output_header = ["テストID","SEQ","起点処理","呼出階層","呼出全資産","呼出方法","呼出資産","資産分類"]


def write_excel_multi_sheet(filename,df_list,sheet_name_list,path,output_header=output_header):
    writer = pd.ExcelWriter(path+"/"+filename,engine='xlsxwriter')
    writer.book.use_zip64()
    # writer = pd.ExcelWriter(filename,engine='xlsxwriter')
    for list,sheet_name in zip(df_list,sheet_name_list):
        df = pd.DataFrame(list,columns=output_header)
        df.to_excel(writer, sheet_name=sheet_name,index=False)
        
    writer._save()
    writer.close()
    
def make_file_name(test_id,num,source):
    date = datetime.datetime.now()
    date = date.strftime('%y%m%d_%H%M%S')    
    
    filename = test_id + "_" + str(num).zfill(4) + "_" +source + "_" + date + ".xlsx"
    return filename


### 100万件毎に分割する
lim = 1000000
def create_output(test_id,num,source,ans_list,title):
    M = len(ans_list)
    lis = []
    for i in range(M//lim+1):
        lis.append(ans_list[i*lim:min(M,(i+1)*lim)])
        
    if lis[-1] == []:
        lis.pop()
    filename = make_file_name(test_id,num,source)
    sheet_names = []
    for i in range(len(lis)):
        if i == 0:
            sheet_names.append("応用_資産階層図")
        else:
            sheet_names.append("応用_資産階層図" + str(i+1))
    write_excel_multi_sheet(filename,lis,sheet_names,title)
    

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
        if "関連性調査結果" not in sheet:
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

    
def main(db_name,title,relations_merge_path,output_separate="True",maxnum=2000000):
    

    M = int(maxnum) ### 件数の最大値　これを超えたら止める

    if os.path.isdir(title) == False:
        os.makedirs(title)
        
    if type(output_separate) != bool:
        output_separate = output_separate == "True"
          
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
        if valid_flg == "●":
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

    ### 変更20191011
    sql =   """\
            SELECT * FROM TEST_テスト実施単位
            """
            
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)
    
    print("グラフの作成が完了しました。")

    ### テスト実施単位から順番に資産階層図を作成する
    ### やり方はグラフに対する 深さ優先探索(DFS = Depth First Search) 基本的はアルゴリズムなので必要があれば検索してみると良いです。

    ans_list_all = []
    ans_list_all_dic = {}
  
    for i,(test_id,num,source,out_folder) in enumerate(zip(df["TEST_ID"],df["実行順序"],df["実行JOB"],df["出力フォルダ"])):
        ans_list = []

        if out_folder in groups_list:
            group_id = groups_list.index(out_folder)
        else:
            group_id = -1
            
        if out_folder != "":
            out_title = os.path.join(title,out_folder)
        else:
            out_title = title
            
        if os.path.isdir(out_title) == False:
            os.makedirs(out_title)
            
        if out_title not in ans_list_all_dic:
            ans_list_all_dic[out_title] = []
        
        ans_list_all = ans_list_all_dic[out_title]
        
         ### source = 起点資産が資産関連性情報の呼出元、呼出先にいない場合は 変換表で name_dic[source] でアクセスするとエラーになるため (配列外参照のようなこと)、最初に処理する
        if source not in name_dic or len(relation_graph[name_dic[source]]) == 0:
            ans_list.append([test_id,num,source,0,source+"(END)","","",""])
            if output_separate == True:
                create_output(test_id,num,source,ans_list,out_title)
            else:
                for lis in ans_list:
                    ans_list_all.append(lis)
            continue
        
        sind = name_dic[source]
        q = deque([[sind,str(sind).zfill(7),""]])
        
        ncount = 0 ### 資産階層図の件数を数える maxnum(defaultは200万件) を超えると長すぎるので一旦打ち切る
        
        while q:
            now,all_vis,all_relations = q.pop()
        
            for nex,nind,valid_relation_flg in relation_graph[now]:
                
                if group_id != -1 and relation_group_info[nind][group_id] != "○":
                    continue
                
                
                if valid_relation_flg == False and now != sind:
                    continue
                
                
                ### 今まで見た呼出全階層の情報が数字版で入っている 0000100&0004931&0999999 のような感じ
                ### str(nex).zfill(7) で 7桁まで0埋めをしているのは 例えば数字をそのまま 100&4931&999990 として 
                ### 次が 9 を見るとなったときには 9 がこの文字列に含まれるかで判定すると 4931 に含まれる 9 を見て既に探索したと誤認識してしまうのを防ぐため
                all_vis_nex = all_vis + "&" +str(nex).zfill(7) 
                all_relations_nex = all_relations + "&" + str(nind).zfill(7)
                
                
                _,relation_type,to,received,_ = relation_list[nind] ### 元々の資産関連性の呼び出し方法などの情報は出力で使うので取り出しておく
                
                ### 逆変換表を使って数字から資産名の呼出全階層情報を復元する
                rev = all_vis_nex.split("&")
                rev_name = [rev_name_dic[int(ind)] for ind in rev] 
                all_list = "→".join(rev_name)
                
                
                if str(nex).zfill(7) in all_vis:
                    all_list += "(重複)"
                    ans_list.append([test_id,num,source,len(rev)-1,all_list,relation_type,to,received,all_relations_nex])
                    ncount += 1
                else:
                    all_list += "(END)"
                    ans_list.append([test_id,num,source,len(rev)-1,all_list,relation_type,to,received,all_relations_nex])            
                    q.append([nex,all_vis_nex,all_relations_nex])
                    ncount += 1
                
                if ncount > M:
                    break
        if ncount > M:
            print(test_id,num,source,str(M)+"以上になるため、途中で打ち止めました。")
            ans_list = ans_list[:M]     
        ans_list.sort(key=lambda x: x[-1])
        ans_list = [lis[:-1] for lis in ans_list]
        if output_separate == True:
            create_output(test_id,num,source,ans_list,out_title)
        else:
            for lis in ans_list:
                ans_list_all.append(lis)
                        
        
    if output_separate == False:
        for out_title in ans_list_all_dic.keys():
            ans_list_all = ans_list_all_dic[out_title]
            create_output("資産階層図","2","出力",ans_list_all,out_title)
            

    
if __name__ == "__main__":

    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    
    ### 引数1 DBPath 引数2 出力フォルダ 