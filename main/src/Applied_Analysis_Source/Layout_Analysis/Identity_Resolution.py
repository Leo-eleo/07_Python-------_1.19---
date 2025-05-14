#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


class Unionfind:
     
    def __init__(self,n):
        self.uf = [-1]*n
        self.dsn_group_list = [i for i in range(n)]
 
    def find(self,x):
        if self.uf[x] < 0:
            return x
        else:
            self.uf[x] = self.find(self.uf[x])
            return self.uf[x]
 
    def get_dsn_group(self,x):
        
        index = self.find(x)
        return self.dsn_group_list[index]
        
    def same(self,x,y):
        return self.find(x) == self.find(y)
 
    def union(self,x,y):
        x = self.find(x)
        y = self.find(y)
        
        dsn_name = self.get_dsn_group(y)
        
        if x == y:
            return False
        if self.uf[x] > self.uf[y]:
            x,y = y,x
        self.uf[x] += self.uf[y]
        self.uf[y] = x
        self.dsn_group_list[x] = self.dsn_group_list[y] = dsn_name
        
        return True
 
    def size(self,x):
        x = self.find(x)
        return -self.uf[x]
    
 
def identity_resolution_main(db_path,title):
    
    
    conn = connect_accdb(db_path)
    cursor = conn.cursor()
    
    
    sql = "SELECT * FROM QRY_名寄せ_入力情報②"
    
    df = pd.read_sql(sql,conn)
    df.fillna("", inplace=True)
    
    ActSheet = set()
    for i in range(len(df)):
        data = df.iloc[i]
        if data["DSN名"] == "DUMMY":
            continue
        ActSheet.add((str(data["DSN名"]),data["COBOL_ID"] + "_" + data["ASSIGN_ID"]))
        
    ActSheet = sorted(ActSheet,key=lambda x: x[1],reverse=True)
    ActSheet = [[dsn,name,""] for dsn,name in ActSheet]
    
    DSNG_CNT = 0
    KEY_old = ""
    
    for i in range(len(ActSheet)):
        KEY = ActSheet[i][1]
        if KEY == "_":
            DSNG_CNT += 1
        elif KEY != KEY_old:
            DSNG_CNT += 1
            KEY_old = KEY
        ActSheet[i][2] = "G-" + str(DSNG_CNT).zfill(7)
       
    dsn_key_dic = {}
    ActSheet.sort(key=lambda x: (x[0],x[2]))
    
    dsn_group_union_find = Unionfind(DSNG_CNT+5)
    dsn_old = ""
    g_old = -1
    for i in range(len(ActSheet)):
        dsn = ActSheet[i][0]
        if dsn_old != "" and dsn_old == dsn:
            dsn_group_union_find.union(int(ActSheet[i][2][2:]),g_old)
        else:
            dsn_old = dsn
            g_old = int(ActSheet[i][2][2:])

    for i in range(len(ActSheet)):
        dsn_group = dsn_group_union_find.get_dsn_group(int(ActSheet[i][2][2:]))
        ActSheet[i][2] = "G-" + str(dsn_group).zfill(7)
        dsn_key_dic[ActSheet[i][0]] = dsn_group
        
    sql = "SELECT * FROM 名寄せ条件設定情報"
    
    df = pd.read_sql(sql,conn)
    df.fillna("", inplace=True)
    
    for dsn1,dsn2 in zip(df["DSN①"],df["DSN②"]):
        if dsn1 not in dsn_key_dic or dsn2 not in dsn_key_dic:
            continue
        dsn_group_union_find.union(dsn_key_dic[dsn2],dsn_key_dic[dsn1])
        
    for i in range(len(ActSheet)):
        dsn = ActSheet[i][0]
        
        dsn_group = dsn_group_union_find.get_dsn_group(dsn_key_dic[dsn])
        ActSheet[i][2] = "G-" + str(dsn_group).zfill(7)
      
    sql,values = make_delete_sql("名寄せWORK",[],[])
    cursor.execute(sql)
      
    for i in range(len(ActSheet)):
        
        sql,values = make_insert_sql("名寄せWORK",ActSheet[i],["DSN","レイアウト","DSNグループ"])
        cursor.execute(sql,values)
    conn.commit()
    
    dsn_all_set = set()
    for i in range(len(ActSheet)):
        dsn_all_set.add((ActSheet[i][0],ActSheet[i][2]))
        
    sql = "SELECT * FROM ②利用DSN一覧"
    df_dsn = pd.read_sql(sql,conn)
    df_dsn.fillna("",inplace=True)
    sql,values = make_delete_sql("②利用DSN一覧",[],[])
    cursor.execute(sql)
      
    dsn_group_dic = {dsn:group for dsn,group in dsn_all_set}
    for i in range(len(df_dsn)):
        data = df_dsn.iloc[i]
        
        dsn = data["DSN名"]
        group = ""
        if dsn in dsn_group_dic:
            group = dsn_group_dic[dsn]
            
        sql,values = make_insert_sql("②利用DSN一覧",[dsn,group],["DSN名","データセットグループ①"])
        cursor.execute(sql,values)
        
    # for dsn,group in dsn_all_set:
        
    #     sql,values = make_insert_sql("②利用DSN一覧",[dsn,group],["DSN名","データセットグループ①"])
    #     cursor.execute(sql,values)
    conn.commit()
        
if __name__ == "__main__":
    identity_resolution_main(sys.argv[1],sys.argv[2])