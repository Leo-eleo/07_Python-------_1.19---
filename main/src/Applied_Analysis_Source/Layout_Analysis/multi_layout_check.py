#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

     
class UTL_STEP別_IO情報_DSNテーブル:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "UTL_STEP別_IO情報_DSNテーブル"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
        sql = "SELECT * FROM "+self.dbname + " ORDER BY JCL_NAME,JOB_SEQ,STEP_SEQ,IO DESC"
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        keys = df.columns.tolist()
        
        for i in range(len(df)):
            data = df.iloc[i]
            
            jcl_name = data["JCL_NAME"]
            job_seq = data["JOB_SEQ"]
            job_id = data["JOB_ID"]
            step_seq = data["STEP_SEQ"]
            step_name = data["STEP名"]
            utility_id = data["Utility_ID"]
            
            if (jcl_name,job_seq,job_id,step_seq,step_name,utility_id) not in self.dic:
                self.dic[(jcl_name,job_seq,job_id,step_seq,step_name,utility_id)] = []
                
            dic = {key:data[key] for key in keys}
            self.dic[(jcl_name,job_seq,job_id,step_seq,step_name,utility_id)].append(dic)
        
        
    def get(self, jcl_name,job_seq,job_id,step_seq,step_name,utility_id):
        if self.dic == None:
            self.setup()
            
            
        if (jcl_name,job_seq,job_id,step_seq,step_name,utility_id) in self.dic:
            return self.dic[(jcl_name,job_seq,job_id,step_seq,step_name,utility_id)]
        else:
            return []
            
    def _close_conn(self):
        if self.conn != None:
            self.cursor.close()
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
     
     
class QRY_DSN単位_レイアウト明細:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "QRY_DSN単位_レイアウト明細"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
        sql = "SELECT * FROM "+self.dbname + " ORDER BY データセットグループ①,DSN名"
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        keys = df.columns.tolist()
        
        for i in range(len(df)):
            data = df.iloc[i]
            
            group_name = data["データセットグループ①"]
            dsn = data["DSN名"]
            # print(group_name,dsn)
            if group_name not in self.dic:
                self.dic[group_name] = []
            if dsn not in self.dic:
                self.dic[dsn] = []
                

            dic = {key:data[key] for key in keys}
            self.dic[group_name].append(dic)
            self.dic[dsn].append(dic)
        
        
    def get(self, name):
        if self.dic == None:
            self.setup()
            
            
        if name in self.dic:
            return self.dic[name]
        else:
            return []
            
    def _close_conn(self):
        if self.conn != None:
            self.cursor.close()
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
     
class スキーマ_基本情報:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "スキーマ_基本情報"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        keys = df.columns.tolist()
        
        for i in range(len(df)):
            data = df.iloc[i]
            
            layout = data["レイアウト名"]
            if layout not in self.dic:
                self.dic[layout] = []
                
            dic = {key:data[key] for key in keys}
            self.dic[layout].append(dic)
        
        
    def get(self, name):
        if self.dic == None:
            self.setup()
            
            
        if name in self.dic:
            return self.dic[name]
        else:
            return []
            
    def _close_conn(self):
        if self.conn != None:
            self.cursor.close()
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
     
     
class レイアウト解析文字列:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "レイアウト解析情報"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        keys = df.columns.tolist()
        
        for layout,layout_string in zip(df["レイアウト名"],df["レイアウト情報"]):
            self.dic[layout] = layout_string

    def get(self, name):
        if self.dic == None:
            self.setup()
            
            
        if name in self.dic:
            return self.dic[name]
        else:
            return ""
            
    def _close_conn(self):
        if self.conn != None:
            self.cursor.close()
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
        
  
   
def 共通_マルチレイアウト判定(P_STR):

    if  " " in P_STR:
       return False
    elif "?" in P_STR:
       return True
    elif P_STR == "XX":
       return False
    elif P_STR == "99":
       return False
    elif P_STR == "ZZ":
       return False
    elif P_STR == "BB":
       return False
    elif P_STR == "PP":
       return False
    elif P_STR == "NN":
       return False
    elif P_STR == "X9" or P_STR == "9X":
       return False
    elif P_STR == "XZ" or P_STR == "ZX":
       return True
    elif P_STR == "XB" or P_STR == "BX":
       return True
    elif P_STR == "XP" or P_STR == "PX":
       return True
    elif P_STR == "XN" or P_STR == "NX":
       return True
    elif P_STR == "9Z" or P_STR == "Z9":
       return True
    elif P_STR == "9B" or P_STR == "B9":
       return True
    elif P_STR == "9P" or P_STR == "P9":
       return True
    elif P_STR == "9N" or P_STR == "N9":
       return True
    elif P_STR == "ZB" or P_STR == "BZ":
       return True
    elif P_STR == "ZP" or P_STR == "PZ":
       return True
    elif P_STR == "ZN" or P_STR == "NZ":
       return True
    elif P_STR == "BP" or P_STR == "PB":   # 'マルチレイアウトではない
       return False
    elif P_STR == "PN" or P_STR == "NP":
       return True
    else:
       return True

      
def マルチレイアウト解析明細処理(myRS2,OutSheet_GYO):
    global スキーマ_基本情報_,レイアウト解析文字列_
    global OutSheet2,マルチレイアウト判定
    TmpSheet = []
 
    for data in myRS2:
        OutSheet2_GYO = [""]*11
        
        OutSheet2_GYO[1] = data["データセットグループ①"]
        OutSheet2_GYO[2] = data["DSN名"]
        OutSheet2_GYO[3] = data["レイアウト名"]

        PARM2 = data["レイアウト名"]

        if PARM2 != "":

            myRS3_all = スキーマ_基本情報_.get(PARM2)
            if myRS3_all == []:
                OutSheet_GYO[5] = "解析情報無"
                OutSheet2_GYO[10] = "該当するレイアウト情報は存在しません"
                OutSheet2.append(OutSheet2_GYO)
                
                continue
            
            for myRS3 in myRS3_all:    
                OutSheet2_GYO = [""]*11
        
                OutSheet2_GYO[1] = data["データセットグループ①"]
                OutSheet2_GYO[2] = data["DSN名"]
                OutSheet2_GYO[3] = data["レイアウト名"]
                OutSheet2_GYO[4] = myRS3["レコード名"]
                OutSheet2_GYO[5] = myRS3["レコード長"]
                OutSheet2_GYO[6] = myRS3["マルチレイアウト判定"]
                if myRS3["マルチレイアウト判定"] == "YES":
                    OutSheet_GYO[4] = "有"
                    マルチレイアウト判定 = "YES"
                
                OutSheet2_GYO[7] = myRS3["REDIFINE有無"]
                OutSheet2_GYO[8] = myRS3["X項目のみ"]
                OutSheet2_GYO[9] = myRS3["レイアウト行数"]
                if OutSheet2_GYO[10] == "":
                    OutSheet2_GYO[10] = myRS3["エラー情報"]
                TmpSheet.append(レイアウト解析文字列_.get(PARM2))
                OutSheet2.append(OutSheet2_GYO)
                
    return TmpSheet,OutSheet_GYO

        
def muiti_layout_main(db_path,title,マルチレイアウトチェック単位="①データセットグループ"):
    
    global OutSheet2,マルチレイアウト判定
    global スキーマ_基本情報_,レイアウト解析文字列_
    conn = connect_accdb(db_path)
    cursor = conn.cursor()
    
    QRY_DSN単位_レイアウト明細_ = QRY_DSN単位_レイアウト明細(conn,cursor)
    スキーマ_基本情報_ = スキーマ_基本情報(conn,cursor)
    レイアウト解析文字列_ = レイアウト解析文字列(conn,cursor)
    OutSheet = []
    OutSheet2 = []
    
    if マルチレイアウトチェック単位 == "①データセットグループ":
        qry = "QRY_DSNグループ単位_レイアウト件数"
    else:
        qry = "QRY_DSN単位_レイアウト件数"
        
    sql = "SELECT * FROM " + qry
    
    df = pd.read_sql(sql,conn)
    for i in range(len(df)):
        data = df.iloc[i]
        
        if マルチレイアウトチェック単位 == "①データセットグループ":
            解析単位 = data["データセットグループ①"]
        else:
            解析単位 = data["DSN名"]
        
        if "&" in 解析単位:
            continue
            
        OutSheet_GYO = [""]*6
        OutSheet_GYO[1] = 解析単位
        OutSheet_GYO[2] = data["CNT"]
        
        PARM = 解析単位
        レイアウト数 = int(OutSheet_GYO[2])
        マルチレイアウト判定 = "NO"
        
        myRS2 = QRY_DSN単位_レイアウト明細_.get(PARM)
        
        if myRS2 == []:
            OutSheet_GYO[3] = "NO"
            OutSheet_GYO[5] = "解析情報無"
            OutSheet.append(OutSheet_GYO)
            continue
        
        TmpSheet,OutSheet_GYO = マルチレイアウト解析明細処理(myRS2,OutSheet_GYO)

        if マルチレイアウト判定 == "YES":
            OutSheet_GYO[3] = "YES"
            OutSheet.append(OutSheet_GYO)
            continue
        
        for i in range(len(TmpSheet)-1):
            l_str1 = TmpSheet[i]
            l_str2 = TmpSheet[i+1]
            
            if len(l_str1) != len(l_str2):
                if OutSheet_GYO[5] == "解析情報無":
                    OutSheet_GYO[5] == "解析情報無" + "\n" + "レコード長不整合"
                # elif "レコード長" in OutSheet_GYO[5]:
                #     pass
                else:
                    OutSheet_GYO[5] = "レコード長不整合"

                マルチレイアウト判定 = "YES"
                break
                
            for j in range(len(l_str1)):
                if 共通_マルチレイアウト判定(l_str1[j] + l_str2[j]):
                    マルチレイアウト判定 = "YES"
            if マルチレイアウト判定 == "YES":
                break
        
        OutSheet_GYO[3] = マルチレイアウト判定
        OutSheet.append(OutSheet_GYO)
                    
                

            
    ActSheet_all = [actSheet[1:] for actSheet in OutSheet]
    output_header = ["解析単位","解析レイアウト数","マルチレイアウト判定","単体レベルマルチレイアウト有無","エラー情報"]
    write_excel_multi_sheet("マルチレイアウト解析結果(サマリ).xlsx",ActSheet_all,"マルチレイアウト解析結果(サマリ)",title,output_header)
    
    ActSheet_all = [actSheet[1:] for actSheet in OutSheet2]
    output_header = ["データセットグループ①","DSN名","レイアウト情報","レコード名","レコード長","マルチレイアウト判定","再定義有無","Ｘ項目のみ","レイアウト行数","エラー情報"]
    write_excel_multi_sheet("マルチレイアウト解析結果(明細).xlsx",ActSheet_all,"マルチレイアウト解析結果(明細)",title,output_header)
    
if __name__ == "__main__":
    muiti_layout_main(sys.argv[1],sys.argv[2])