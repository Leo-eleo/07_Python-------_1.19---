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

資産関連性_追加_CNT = 0
JCL_PGM_DSN_追加_CNT = 0
JCL_PGM_DSN_更新_CNT = 0
UTL_STEP別_IO情報_追加_CNT = 0

応用_顧客別_JCL_STEP_SYSIN_ = None
#応用_顧客別_資産関連性情報_ = None
応用_顧客別_JCL_PGM_DSN3_ = None


#class 応用_顧客別_資産関連性情報:
#    
#    def __init__(self,conn,cursor):
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
    


def EASY利用個所解析_共通出力(data):
       
       
    global LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME,PROC_NAME,SYSIN_PGM,SYSIN_SEQ,SYSIN

    global 資産関連性_追加_CNT,JCL_PGM_DSN_追加_CNT,JCL_PGM_DSN_更新_CNT,UTL_STEP別_IO情報_追加_CNT
    
    ActSheet_x = [""]*20
    ActSheet_x[1] = data["LIBRARY_ID"]
    ActSheet_x[2] = data["JCL_NAME"]
    ActSheet_x[3] = data["JOB_SEQ"]
    ActSheet_x[4] = data["JOB_ID"]
    ActSheet_x[5] = data["STEP_SEQ"]
    ActSheet_x[6] = data["STEP_NAME"]
    ActSheet_x[7] = data["PGM_NAME"]
    ActSheet_x[8] = data["PROC_NAME"]
    ActSheet_x[9] = data["SYSIN_PGM"]
    ActSheet_x[10] = ""
    ActSheet_x[11] = data["SYSIN"]
    
    LIBRARY_ID = data["LIBRARY_ID"]
    JCL_NAME = data["JCL_NAME"]
    JOB_SEQ = data["JOB_SEQ"]
    JOB_ID = data["JOB_ID"]
    STEP_SEQ = data["STEP_SEQ"]
    STEP_ID = data["STEP_NAME"]
    PGM_NAME = data["PGM_NAME"]
    PROC_NAME = data["PROC_NAME"]
    SYSIN_PGM = data["SYSIN_PGM"]
    ###SYSIN_SEQ = data["SYSIN_SEQ"]
    SYSIN = data["SYSIN"]


    資産関連性_追加_CNT = 0
    JCL_PGM_DSN_追加_CNT = 0
    JCL_PGM_DSN_更新_CNT = 0
    UTL_STEP別_IO情報_追加_CNT = 0
        
    return ActSheet_x


def EASY利用個所解析_解析処理(ActSheet_x):
    #global 応用_顧客別_JCL_STEP_SYSIN_,応用_顧客別_資産関連性情報_,応用_顧客別_JCL_PGM_DSN3_
    global 応用_顧客別_JCL_STEP_SYSIN_,応用_顧客別_JCL_PGM_DSN3_
    global LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME,PROC_NAME,SYSIN_PGM,SYSIN_SEQ,SYSIN,呼出方法,判定PGM,PGM予備,判定MODE
    global 分割文字列,分割文字列2,vbCrLf
    

    
    
    ###○UTL対応
    ###=== DFSRRC00 ===
    if PGM_NAME == "EZTPA00" or PGM_NAME == "EASYTREV" or PGM_NAME == "DFSRRC00" or PROC_NAME == "IMSEASY":  ###QRYでこれ以外のPGMは来ないはず
        
        if SYSIN_PGM == "EZTPA00" or PGM_NAME == "EZTPA00" :
            if SYSIN != "":
                ActSheet_x[12] = "EZTPA00-LIB"
                呼出方法 = "EZTPA00-LIB"
                判定PGM = SYSIN
                PGM予備 = "EZTPA00"
                判定MODE = "EASYP-LIB"
            else:
                ActSheet_x[12] = "EZTPA00-JCL ★PGM名要手動修正"
                呼出方法 = "EZTPA00-JCL"
                判定PGM = JOB_ID + "EA"
                PGM予備 = "EZTPA00"
                判定MODE = "EASYP-JCL"
           
        
        elif SYSIN_PGM == "EASYTREV" or PGM_NAME == "EASYTREV" :
            if SYSIN != "" :
                ActSheet_x[12] = "EASYTREV-LIB"
                呼出方法 = "EASYTREV-LIB"
                判定PGM = SYSIN
                PGM予備 = "EASYTREV"
                判定MODE = "EASY-LIB"
            else:
                ActSheet_x[12] = "EASYTREV-JCL ★PGM名要手動修正"
                呼出方法 = "EASYTREV-JCL"
                判定PGM = JOB_ID + "EA"
                PGM予備 = "EASYTREV"
                判定MODE = "EASY-JCL"
           
                
        elif PROC_NAME == "IMSEASY" :
            if SYSIN != "" :
                ActSheet_x[12] = "EASYTREV-LIB"
                呼出方法 = "EASYTREV-LIB"
                判定PGM = SYSIN
                PGM予備 = "EASYTREV"
                判定MODE = "EASY-LIB"
            else:
                ActSheet_x[12] = "EASYTREV-JCL ★PGM名要手動修正"
                呼出方法 = "EASYTREV-JCL"
                判定PGM = JOB_ID + "EA"
                PGM予備 = "EASYTREV"
                判定MODE = "EASY-JCL"
           
                
        else:
            ActSheet_x[12] = "EASY ★想定外のPGM情報"
            呼出方法 = ""
            判定PGM = ""
        
            
        if 判定PGM != "" :
        
            ###★★★関連性TABLEに出力する処理追加
            #if 応用_顧客別_資産関連性情報_.insert() == False:
            #    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
            #else:
            #    ActSheet_x[13] = 1
            #    ActSheet_x[9]= 判定PGM
            #
            #    ### ===暫定対応
            #    ActSheet_x[17] = 判定PGM
            #    ### ===
 
                ###★★★顧客別_JCL_STEP_SYSINを更新する処理追加
    
            if 応用_顧客別_JCL_STEP_SYSIN_.update() == False:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "更新情報無しの為処理SKIP"
            else:
                ActSheet_x[17] = 判定PGM
                ActSheet_x[19] = 1

                    
        if 判定PGM != "":
                   
            if 応用_顧客別_JCL_PGM_DSN3_.update() == False:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "更新情報無しの為処理SKIP"
            else:
                ActSheet_x[15] = 1
                
        
    return ActSheet_x                  
     
    

    
    
def analysis4_EASY_analysis(conn,cursor):
    
    ### 変更20191011
    sql =   """\
            SELECT * FROM QRY_EASY抽出_UNION
            """
            
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)
    print(len(df),"analysis4_EASY_analysis")
    #global 応用_顧客別_JCL_STEP_SYSIN_,応用_顧客別_資産関連性情報_,応用_顧客別_JCL_PGM_DSN3_
    global 応用_顧客別_JCL_STEP_SYSIN_,応用_顧客別_JCL_PGM_DSN3_
   
    応用_顧客別_JCL_STEP_SYSIN_ = 応用_顧客別_JCL_STEP_SYSIN(conn,cursor)
    #応用_顧客別_資産関連性情報_ = 応用_顧客別_資産関連性情報(conn,cursor)
    応用_顧客別_JCL_PGM_DSN3_ = 応用_顧客別_JCL_PGM_DSN3(conn,cursor)
 
    ### VBAでシートに書き込んでいる代わりにこのリストに追加して最後にまとめて書き込む
    ActSheet = []
    for i in range(len(df)):
        data = df.iloc[i]
        ActSheet_x = EASY利用個所解析_共通出力(data)
        ActSheet_x = EASY利用個所解析_解析処理(ActSheet_x)
        ActSheet.append(ActSheet_x)
    print(len(ActSheet),"analysis4")

    return ActSheet
