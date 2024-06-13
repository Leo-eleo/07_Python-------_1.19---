#!/usr/bin/env python
# -*- coding: cp932 -*-
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


vbCrLf = "\n"
分割文字列 = []
分割文字列2 = []

LIBRARY_ID = ""
JCL_NAME = ""
JOB_SEQ = ""
JOB_ID = ""
STEP_SEQ = ""
STEP_ID = ""
PGM_NAME = ""
PROC_NAME = ""
SYSIN_PGM = ""
SYSIN_SEQ = ""
PARM_EXEC = ""
PARM_PROC = ""
SYSIN = ""
呼出方法 = ""
判定PGM = ""
DB自動登録時PARM = "自動設定（UTL解析）"
PGM予備 = ""
判定MODE = ""


応用_顧客別_JCL_STEP_SYSIN_ = None
#応用_顧客別_資産関連性情報_ = None
応用_顧客別_JCL_PGM_DSN3_ = None
応用_UTL_STEP別_IO情報_ = None
DSNMTV01利用PGM取得_ = None

#class 応用_顧客別_資産関連性情報:
#    
#    def __init__(self,conn):
#        self.dic = None
#        self.conn = conn
#        self.cursor = cursor
#        self.dbname = "顧客別_資産関連性情報"
    #    self.db_path = db_path
#
#    def setup(self):
#        self.dic = {}
#        sql = "SELECT * FROM "+self.dbname
#        
#        df = pd.read_sql(sql,self.conn)
#        
#        for from_source,type,to_source in zip(df["呼出元資産"],df["呼出方法"],df["呼出先資産"]):
#            self.dic[(from_source,type,to_source)] = 1
#    
#        
#    def insert(self):
#        if self.dic == None:
#            self.setup()
#            
#        global JCL_NAME,呼出方法,判定PGM,DB自動登録時PARM
#        if (JCL_NAME,呼出方法,判定PGM) in self.dic:
#            return False
#        
#        key_list = ["呼出元資産","呼出方法","呼出先資産","登録分類"]
#        value_list = [JCL_NAME,呼出方法,判定PGM,DB自動登録時PARM]
#        
#        sql,value = make_insert_sql(self.dbname,value_list,key_list)
#        
#        self.cursor.execute(sql,value)
#        self.dic[(JCL_NAME,呼出方法,判定PGM)] = 1
#        
#        return True
#    
#    def _close_conn(self):
#        if self.conn != None:
#            self.conn.close() 
#    
#    def close_conn(self):
#        self._close_conn()
    
    
class 応用_顧客別_JCL_PGM_DSN3:
    
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "顧客別_JCL_PGM_DSN"
        # self.db_path = db_path
        
    def setup(self):
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        
        for jcl,job,step in zip(df["JCL_NAME"],df["JOB_SEQ"],df["STEP_SEQ"]):
            self.dic[(jcl,job,step)] = 1
    
        
    def update(self):
        if self.dic == None:
            self.setup()
            
        global JCL_NAME,JOB_SEQ,STEP_SEQ,判定PGM,PGM予備,判定MODE,DB自動登録時PARM
        
        if (JCL_NAME,JOB_SEQ,STEP_SEQ) not in self.dic:
            return False
        

        set_key_list = ["SYSIN_PGM","PGM予備","実行モード","自動更新FLG"]
        set_value_list = [判定PGM,PGM予備,判定MODE,DB自動登録時PARM]
        
        where_key_list = ["JCL_NAME","JOB_SEQ","STEP_SEQ"]
        where_value_list = [JCL_NAME,JOB_SEQ,STEP_SEQ]
                
        sql,value = make_update_sql(self.dbname,set_value_list, set_key_list,where_value_list,where_key_list)
        self.cursor.execute(sql,value)
       
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
        
         
class 応用_顧客別_JCL_STEP_SYSIN:
    
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "顧客別_JCL_STEP_SYSIN"
        # self.db_path = db_path
        
    def setup(self):
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        
        for jcl,job,step in zip(df["JCL_NAME"],df["JOB_SEQ"],df["STEP_SEQ"]):
            self.dic[(jcl,job,step)] = 1
    
        
    def update(self):
        if self.dic == None:
            self.setup()
            
        global JCL_NAME,JOB_SEQ,STEP_SEQ,判定PGM,DB自動登録時PARM
        
        if (JCL_NAME,JOB_SEQ,STEP_SEQ) not in self.dic:
            return False
        

        set_key_list = ["SYSIN_PGM","自動更新FLG"]
        set_value_list = [判定PGM,DB自動登録時PARM]
        
        where_key_list = ["JCL_NAME","JOB_SEQ","STEP_SEQ"]
        where_value_list = [JCL_NAME,JOB_SEQ,STEP_SEQ]
                
        
        sql,value = make_update_sql(self.dbname,set_value_list, set_key_list,where_value_list,where_key_list)
        self.cursor.execute(sql,value)
       
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
    
class DSNMTV01利用PGM取得:
    
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "QRY_DFSRRC00_DSNMTV01"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        
        for jcl,job,step,sysin in zip(df["JCL_NAME"],df["JOB_SEQ"],df["STEP_SEQ"],df["SYSIN"]):
            self.dic[(jcl,job,step)] = str(sysin)
        
    
        
    def get(self):
        global JCL_NAME,JOB_SEQ,STEP_SEQ
           
        if self.dic == None:
            self.setup()
            
        if (JCL_NAME,JOB_SEQ,STEP_SEQ) in self.dic:
            return self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ)]
        
        else:
            return ""


def DFSRRC00_BMP_DLI_共通出力(data):
       
       
    global LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME,PROC_NAME,SYSIN_PGM,SYSIN_SEQ,PARM_EXEC,PARM_PROC
    global 分割文字列,分割文字列2,vbCrLf
    
     
    
    ActSheet_x = [""]*20
    ActSheet_x[1] = ""                 ###JCL_CMD情報に当該項目がないので仮設定
    ActSheet_x[2] = data["資産ID"]
    ActSheet_x[3] = data["JOB_SEQ"]       ###対応済
    ActSheet_x[4] = data["JCL_ID"]
    ActSheet_x[5] = data["STEP_SEQ"]
    ActSheet_x[6] = data["STEP_NAME"]
    ActSheet_x[7] = data["PGM_NAME"]
    ActSheet_x[8] = data["PROC_NAME"]
    ActSheet_x[9] = ""                 ###JCL_CMD情報に当該項目がないので仮設定
    ActSheet_x[10] = 0                  ###使わない
    ActSheet_x[11] = str(data["PARM_EXEC"]) + vbCrLf + str(data["PARM_PROC"])
    
    
    
    ###LIBRARY_ID = data["LIBRARY_ID"]
    JCL_NAME = data["資産ID"]
    JOB_SEQ = data["JOB_SEQ"]
    JOB_ID = data["JCL_ID"]
    STEP_SEQ = data["STEP_SEQ"]
    STEP_ID = data["STEP_NAME"]
    PGM_NAME = data["PGM_NAME"]
    PROC_NAME = data["PROC_NAME"]
    SYSIN_PGM = ""
    ###SYSIN_SEQ = data["SYSIN_SEQ"]
    PARM_EXEC = data["PARM_EXEC"]
    PARM_PROC = data["PARM_PROC"]
    
    
    分割文字列 = ArrayEmptyDelete(data["PARM_EXEC"].split(" "))    
    分割文字列2 = ArrayEmptyDelete(data["PARM_PROC"].split(" "))
    
    
    return ActSheet_x


def DFSRRC00_BMP_DLI_解析処理(ActSheet_x):
    #global 応用_顧客別_JCL_STEP_SYSIN_,応用_顧客別_資産関連性情報_,応用_顧客別_JCL_PGM_DSN3_,DSNMTV01利用PGM取得_
    global 応用_顧客別_JCL_STEP_SYSIN_,応用_顧客別_JCL_PGM_DSN3_,DSNMTV01利用PGM取得_
    global LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME,PROC_NAME,SYSIN_PGM,SYSIN_SEQ,PARM_EXEC,PARM_PROC,呼出方法,判定PGM
    global 分割文字列,分割文字列2,判定MODE,PGM予備,vbCrLf,SYSIN
    
    L_DLI_TYPE = ""
    L_DLI_MBR = ""

    
    ###○UTL対応
    ###=== DFSRRC00 ===
    if PGM_NAME == "DFSRRC00":
        L_DLI_TYPE = ""
        L_DLI_MBR = ""
        for i in range(len(分割文字列)):
            if 分割文字列[i] == "PARM":
                
                if  (i + 4) >= len(分割文字列):
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "DFSRRC00-BMP_DLI 配列要素不足"
                    continue
                
                if 分割文字列[i + 1] == "=" and 分割文字列[i + 2] == "(":
                    L_DLI_TYPE = 分割文字列[i + 3]
                    L_DLI_MBR = 分割文字列[i + 4]
                    
                    if L_DLI_TYPE == "BMP":
                        ActSheet_x[12] = "DFSRRC00-BMP"
                        呼出方法 = "DFSRRC00-BMP"
                        判定MODE = "BMP"
                    elif L_DLI_TYPE =="DLI":
                        ActSheet_x[12] = "DFSRRC00-DLI"
                        呼出方法 = "DFSRRC00-DLI"
                        判定MODE = "DLI"
                    elif L_DLI_TYPE =="ULU":
                        ActSheet_x[12] = "DFSRRC00-ULU"
                        呼出方法 = "DFSRRC00-ULU"
                        判定MODE = "ULU"
                    else:
                        ActSheet_x[12] = "DFSRRC00-OTHER"
                        呼出方法 = "DFSRRC00-" + L_DLI_TYPE
                        判定MODE = "OTHER"
                    
                    
                    if "&" in L_DLI_MBR:
                        L_DLI_MBR = 分割文字列[i + 4].replace("&", "")
                    
                        for j in range(len(分割文字列2)):
                            if 分割文字列2[j] == L_DLI_MBR:
                                if (j + 2) < len(分割文字列2):
                                    if 分割文字列2[j + 1] == "=":
                                        判定PGM = 分割文字列2[j + 2]
                                    else:
                                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "DFSRRC00-BMP_DLI 配列要素不正"
                                    
                                else:
                                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "DFSRRC00-BMP_DLI 配列要素不足"
                    
                        
                        if 判定PGM == "":
                            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "DFSRRC00-BMP_DLI PGM不明"
                    
                        
                    else:
                        判定PGM = L_DLI_MBR
            
                ###ULUモードの場合「(」がない場合がある
                elif 分割文字列[i + 1] == "=" and 分割文字列[i + 2] == "ULU":
                    if i + 3 < len(分割文字列):
                        L_DLI_TYPE = 分割文字列[i + 2]
                        判定PGM = 分割文字列[i + 3].replace("&","").replace("\"", "")
                        ActSheet_x[12] = "DFSRRC00-ULU"
                        呼出方法 = "DFSRRC00-ULU"
                        判定MODE = "ULU"
                        
                    else:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "DFSRRC00-ULU 配列要素不正"
                    
                else:
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "DFSRRC00-BMP_DLI 配列要素不正"
                

    if 判定PGM != "" and 判定PGM != "DSNMTV01":     ### DSNMTV01 は　「DFSRRC00_DSNMTV01_解析処理」で処理する
        #if 応用_顧客別_資産関連性情報_.insert() == False:
        #    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
        #else:
        #    ActSheet_x[13] = 1
        #    
        #    ActSheet_x[9]= 判定PGM
        #
        #    ### ===暫定対応
        #    ActSheet_x[17] = 判定PGM
        #    ### ===
   
                      
        PGM予備 = ""     ###設定しないので初期化する
        if  応用_顧客別_JCL_PGM_DSN3_.update() == False:
            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "更新情報無しの為処理SKIP"
        else:
            ActSheet_x[15] = 1
       
        ### ★★★顧客別_JCL_STEP_SYSINを更新する処理追加
       
        if 応用_顧客別_JCL_STEP_SYSIN_.update() == False:
            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "更新情報無しの為処理SKIP"
        else:
            ActSheet_x[17] = 判定PGM
            ActSheet_x[19] = 1
              
    ### ★★★DSNMTV01 対応
    elif 判定PGM == "DSNMTV01":
        呼出方法 = 呼出方法 + "-DSNMTV01"
        ActSheet_x[12] = 呼出方法
        SYSIN = DSNMTV01利用PGM取得_.get()
        分割文字列3 = SYSIN.split(" ")
        ActSheet_x[11] = ActSheet_x[11] + vbCrLf + SYSIN ### 間違ってそう 12では?
        if len(分割文字列3) > 7:
           
            判定PGM = 分割文字列3[7]  ### 後で確認
            
            if 判定PGM != "":
                #if 応用_顧客別_資産関連性情報_.insert() == False:
                #    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                #else:
                #    ActSheet_x[13] = 1
                #    ActSheet_x[9]= 判定PGM
                #
                #    ### ===暫定対応
                #    ActSheet_x[17] = 判定PGM
                #    ### ===
                                
                      
                ### ★★★顧客別_JCL_STEP_SYSINを更新する処理追加
       
                if 応用_顧客別_JCL_STEP_SYSIN_.update() == False:
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "更新情報無しの為処理SKIP"
                else:
                    ActSheet_x[17] = 判定PGM
                    ActSheet_x[19] = 1

            else:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "DFSRRC00-DSNMTV01 配列要素空"
 
            if 判定PGM != "":
           
                PGM予備 = "DSNMTV01"
                if 応用_顧客別_JCL_PGM_DSN3_.update() == False:
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "更新情報無しの為処理SKIP"
                else:
                    ActSheet_x[15] = 1

        else:
            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "DFSRRC00-DSNMTV01 PGM名取得エラー"
           
    else:
        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "DFSRRC00-BMP_DLI 配列要素空"
        
    return ActSheet_x


def analysis2_DFSRRC00(conn,cursor):
    
    ### 変更20191011
    sql =   """\
            SELECT * FROM QRY_DFSRRC00_BMP_DLI_ULU
            """
            
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)

    #global 応用_顧客別_JCL_STEP_SYSIN_,応用_顧客別_資産関連性情報_,応用_顧客別_JCL_PGM_DSN3_,DSNMTV01利用PGM取得_
    global 応用_顧客別_JCL_STEP_SYSIN_,応用_顧客別_JCL_PGM_DSN3_,DSNMTV01利用PGM取得_
    
    応用_顧客別_JCL_STEP_SYSIN_ = 応用_顧客別_JCL_STEP_SYSIN(conn,cursor)
    #応用_顧客別_資産関連性情報_ = 応用_顧客別_資産関連性情報(conn,cursor)
    応用_顧客別_JCL_PGM_DSN3_ = 応用_顧客別_JCL_PGM_DSN3(conn,cursor)
    DSNMTV01利用PGM取得_ = DSNMTV01利用PGM取得(conn,cursor)
  

    ### VBAでシートに書き込んでいる代わりにこのリストに追加して最後にまとめて書き込む
    ActSheet = []
    print(len(df),"analysis2_DFSRRC00")
    for i in range(len(df)):
        data = df.iloc[i]
        ActSheet_x = DFSRRC00_BMP_DLI_共通出力(data)
        ActSheet_x = DFSRRC00_BMP_DLI_解析処理(ActSheet_x)
        ActSheet.append(ActSheet_x)
        
    print(len(ActSheet),"analysis2")
    
    
    return ActSheet
    

    