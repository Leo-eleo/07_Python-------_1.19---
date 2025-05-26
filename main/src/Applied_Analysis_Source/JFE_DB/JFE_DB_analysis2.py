#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
# sys.path.append(os.path.dirname(__file__))

import pandas as pd
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

output_header = ["資産ID","COBOL_ID","調査対象PGM名","処理データ分類","元資産行情報","PARM_ALL",\
                "処理レコード①","処理レコード②","処理レコード③","処理レコード④","処理レコード⑤","パラメータ","CRUD判定","IO判定",\
                "関連DSN","関連性設定","PGM-IO","JCL_PGM_DSN","関連PGM（親含む）","補足","JSI用XDBREF"
]

vbLf = "\n"

DB自動登録時PARM = "自動設定（JFE_DB特定）" 
関連資産 = ""
JFE_レコード関連引数位置 = 0
分割文字列 = []
JFE_関連DSN特定_ = None
応用_顧客別_資産関連性情報_INSERT_FOR_COBOL_ = None
応用_顧客別_PGM_IO情報_ = None
顧客別_JCL_PGM_DSN_BMCP以外_ = None
QRY_JCL_PGM_DSN_BMCP_ = None
応用_顧客別_JCL_PGM_DSN_FOR_DB_JFE_ = None

ActSheet = []
ActSheet_x = []
DD_CNT = 0
資産ID = ""
COBOL_ID = ""
関連資産 = ""
JFE_データ分類 = ""
JFE_DSN = ""
JFE_処理レコード = ""
JFE_処理レコード1 = ""
JFE_処理レコード2 = ""
JFE_処理レコード3 = ""
JFE_処理レコード4 = ""
JFE_処理レコード5 = ""
JFE_CRUD判定 = ""
JFE_IO判定 = ""
呼出方法 = ""
判定PGM = ""
IO判定 = ""
JFE_関連DSN = ""
#'20240215 ADD qian.e.wang
分割_関連DSN = []
#'ADD END
関連データ = ""

LIBRARY_ID = ""
JCL_NAME = ""
JOB_SEQ = ""
JOB_ID = ""
STEP_SEQ = ""
STEP_ID = ""
PGM_NAME = ""
PROC_NAME = ""
SYSIN_PGM = ""
判定DD = ""
追加DSN = ""

# 与えられた条件に基づいて関連DSN（データセット名）を特定
class JFE_関連DSN特定:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "【暫定】JFE_DATA関連性設定"
        # self.db_path = db_path

    def setup(self):
        
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for type,id,dsn in zip(df["データ分類"],df["データID"],df["DSN"]):
            if (type,id) not in self.dic:
#'20240215 UPD qian.e.wang
            #    self.dic[(type,id)] = dsn
                self.dic[(type, id)] = []
            self.dic[(type, id)].append(dsn)
#'UPD END
        
    def get(self):
        global JFE_データ分類,JFE_処理レコード
        
        if self.dic == None:
            self.setup()
        
        if (JFE_データ分類,JFE_処理レコード) in self.dic:
#'20240215 UPD qian.e.wang
        #    JFE_関連DSN = JFE_データ分類 + ":" + self.dic[(JFE_データ分類,JFE_処理レコード)] + "(" + JFE_処理レコード + ")"
            JFE_関連DSN = ""
            for dsn in self.dic[(JFE_データ分類, JFE_処理レコード)]:
                JFE_関連DSN += JFE_データ分類 + ":"
                JFE_関連DSN += dsn + "(" + JFE_処理レコード + ")" + ";"
            return JFE_関連DSN
        else:
        #    JFE_関連DSN = JFE_データ分類 + ":" + JFE_処理レコード + "(設定無)"
            return JFE_データ分類 + ":" + JFE_処理レコード + "(設定無)"
        #return JFE_関連DSN

# 与えられた条件に基づいて判定IOを特定
class JFE_判定IO特定:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "【暫定】JFE_DATA関連性設定"
        # self.db_path = db_path

    def setup(self):
        
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for type,id,dsn,io in zip(df["データ分類"],df["データID"],df["DSN"],df["IO判定"]):
            if (type,id,dsn) not in self.dic:
                self.dic[(type, id, dsn)] = []
            self.dic[(type, id, dsn)].append(io)

    def get(self):
        global JFE_データ分類,JFE_処理レコード,JFE_DSN
        
        if self.dic == None:
            self.setup()
        
        # DEBUG
        # print("■② JFE_処理レコード :["+str(JFE_処理レコード)+"] JFE_DSN :["+str(JFE_DSN)+"]\r\n")
        
        if (JFE_データ分類,JFE_処理レコード,JFE_DSN) in self.dic:
            IO判定 = ""
            for io in self.dic[(JFE_データ分類,JFE_処理レコード,JFE_DSN)]:
                if IO判定 == "":
                    IO判定 = io
                elif io == "NA":
                    pass
                else:
                    if IO判定 == io:
                        pass
                    else:
                        IO判定 = "I-O"
            # DEBUG
            # print("■② IO判定 :["+str(IO判定)+"]\r\n")
            return IO判定
        else:
            return ""
#'UPD END


# COBOLプログラムに関連する資産の情報をデータベースに挿入
class 応用_顧客別_資産関連性情報_INSERT_FOR_COBOL:
    
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "顧客別_資産関連性情報"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for from_source,type,to_source in zip(df["呼出元資産"],df["呼出方法"],df["呼出先資産"]):
            self.dic[(from_source,type,to_source)] = 1
    
        
    def insert(self):
        if self.dic == None:
            self.setup()
            
        global COBOL_ID,呼出方法,判定PGM
        global DB自動登録時PARM
        if (COBOL_ID,呼出方法,判定PGM) in self.dic:
            return False
        
        key_list = ["呼出元資産","呼出方法","呼出先資産","登録分類"]
        value_list = [COBOL_ID,呼出方法,判定PGM,DB自動登録時PARM]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        self.dic[(COBOL_ID,呼出方法,判定PGM)] = 1
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
    
 
class 応用_顧客別_JCL_PGM_DSN_FOR_DB_JFE:
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
        df.fillna("",inplace=True)
        
        for jcl,job,step,dd,dsn in zip(df["JCL_NAME"],df["JOB_SEQ"],df["STEP_SEQ"],df["DD_NAME"],df["DSN"]):
            self.dic[(jcl,job,step,dd,dsn)] = 1
    
        
    def insert(self):
        if self.dic == None:
            self.setup()
            
        global DB自動登録時PARM
        global LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME,PROC_NAME,SYSIN_PGM,判定DD,追加DSN,判定PGM
        if (JCL_NAME,JOB_SEQ,STEP_SEQ,判定DD,追加DSN) in self.dic:
            return False

        key_list = ["LIBRARY_ID","JCL_NAME","JOB_SEQ","JOB_ID","STEP_SEQ","STEP_NAME","PGM_NAME","PROC_NAME","SYSIN_PGM","DD_NAME","DSN","手動更新FLG","自動更新FLG"]
        value_list = [LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME,PROC_NAME,SYSIN_PGM,判定DD,追加DSN,"",DB自動登録時PARM]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ,判定DD,追加DSN)] = 1
        
   
        ### 顧客別_JCL_PGM_DSNを更新するので 顧客別_JCL_PGM_DSN_BMCP以外のdic も更新する
        global 顧客別_JCL_PGM_DSN_BMCP以外_
        temp_dic = {key:value for key,value in zip(key_list,value_list)}
        pgm_name = temp_dic["PGM_NAME"]
        if pgm_name not in 顧客別_JCL_PGM_DSN_BMCP以外_.dic:
            顧客別_JCL_PGM_DSN_BMCP以外_.dic[pgm_name] = []
        顧客別_JCL_PGM_DSN_BMCP以外_.dic[pgm_name].append(temp_dic)
        
        sysin_pgm = temp_dic["SYSIN_PGM"]
        if sysin_pgm not in 顧客別_JCL_PGM_DSN_BMCP以外_.dic:
            顧客別_JCL_PGM_DSN_BMCP以外_.dic[sysin_pgm] = []
        顧客別_JCL_PGM_DSN_BMCP以外_.dic[sysin_pgm].append(temp_dic)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
    
    
# プログラムの入出力情報をデータベースに挿入
class 応用_顧客別_PGM_IO情報:
    
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "顧客別_PGM_IO情報"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for type, id, io, file in zip(df["資産分類"],df["資産ID"],df["入出力区分"],df["ファイル名"]):
            if type != "COBOL_自動":
                continue
            self.dic[(id, io, file)] = 1
    
        
    def insert(self):
        if self.dic == None:
            self.setup()
            
        global 判定PGM,IO判定,関連データ
        global DB自動登録時PARM
        if (判定PGM,IO判定,関連データ) in self.dic:
            return False
        
        key_list = ["資産分類","LIBRARY_ID","資産ID","入出力区分","ファイル名"]
        ### 'LIBRARY_ID は暫定措置
        
        value_list = ["COBOL_自動","TEST",判定PGM,IO判定,関連データ]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        self.dic[(判定PGM,IO判定,関連データ)] = 1
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
    
# 特定の条件を除くJCL、PGM、DSNの情報を扱い
class 顧客別_JCL_PGM_DSN_BMCP以外:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "顧客別_JCL_PGM_DSN"
        self.key_list = ["LIBRARY_ID","JCL_NAME","JOB_SEQ","JOB_ID","STEP_SEQ","STEP_NAME","PGM_NAME","PROC_NAME","SYSIN_PGM"]
        # self.db_path = db_path

    def setup(self):
        
        self.dic = {}
        sql = "SELECT DISTINCT LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_NAME,PGM_NAME,PROC_NAME,SYSIN_PGM FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        ### この処理で distinct なデータを取り出す
        
        
        ###
        
        for i in range(len(df)):
            data = df.iloc[i]
            temp_dic = {key:data[key] for key in self.key_list}
            pgm_name = temp_dic["PGM_NAME"]
            if pgm_name not in self.dic:
                self.dic[pgm_name] = []
            self.dic[pgm_name].append(temp_dic)
            
            sysin_pgm = temp_dic["SYSIN_PGM"]
            if sysin_pgm not in self.dic:
                self.dic[sysin_pgm] = []
            self.dic[sysin_pgm].append(temp_dic)
        
        
    def get(self):
        global 判定PGM
        
        if self.dic == None:
            self.setup()
                
        if 判定PGM in self.dic:
            return self.dic[判定PGM]
        
        else:
            return []
            
# 特定の条件（おそらくBMCPに関連する）を持つJCL、PGM、DSNの情報を扱い
class QRY_JCL_PGM_DSN_BMCP:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "QRY_JCL_PGM_DSN_BMCP"
        self.key_list = ["BMCP_PGM","LIBRARY_ID","JCL_NAME","JOB_SEQ","JOB_ID","STEP_SEQ","STEP_NAME","PGM_NAME","PROC_NAME","SYSIN_PGM"]
        # self.db_path = db_path

    def setup(self):
        
        self.dic = {}
        sql = "SELECT DISTINCT LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_NAME,PGM_NAME,PROC_NAME,SYSIN_PGM,BMCP_PGM FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        keys = df.columns.tolist()
        df.sort_values(keys,inplace=True)

        for i in range(len(df)):
            data = df.iloc[i]
            temp_dic = {key:data[key] for key in self.key_list[1:]}
            bmcp_pgm = data["BMCP_PGM"]
            if bmcp_pgm not in self.dic:
                self.dic[bmcp_pgm] = []
            self.dic[bmcp_pgm].append(temp_dic)
            
        
    def get(self):
        global 判定PGM
        
        if self.dic == None:
            self.setup()
                
        if 判定PGM in self.dic:
            return self.dic[判定PGM]
        
        else:
            return []
            
   
   
#関数の定義:BMCP以外処理
def BMCP以外処理():
    global 顧客別_JCL_PGM_DSN_BMCP以外_,応用_顧客別_JCL_PGM_DSN_FOR_DB_JFE_
    global 判定PGM, DD_CNT,関連データ
    global LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME,PROC_NAME,SYSIN_PGM,判定DD,追加DSN
    
    DD_CNT = 0

    df = 顧客別_JCL_PGM_DSN_BMCP以外_.get()
    lis = []
    
    ### get でデータの重複があるため、重複を削除する
    for data in df:
        LIBRARY_ID = data["LIBRARY_ID"]
        JCL_NAME = data["JCL_NAME"]
        JOB_SEQ = data["JOB_SEQ"]
        JOB_ID = data["JOB_ID"]
        STEP_SEQ = data["STEP_SEQ"]
        STEP_ID = data["STEP_NAME"]
        PGM_NAME = data["PGM_NAME"]
        PROC_NAME = data["PROC_NAME"]
        SYSIN_PGM = data["SYSIN_PGM"]
        lis.append((LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME,PROC_NAME,SYSIN_PGM))
    df = set(lis)
    
    ################################################
    
    for data in df:
     
        LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME,PROC_NAME,SYSIN_PGM = data
                            
        判定DD = "_SYSJ001"                # 'ここが違う
        追加DSN = 関連データ
    
        if 応用_顧客別_JCL_PGM_DSN_FOR_DB_JFE_.insert() == False:
            pass
        else:
            DD_CNT = DD_CNT + 1
        
#関数の定義:BMCP処理
def BMCP処理():    
    global QRY_JCL_PGM_DSN_BMCP_,応用_顧客別_JCL_PGM_DSN_FOR_DB_JFE_
    global 判定PGM, DD_CNT,関連データ
    global LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME,PROC_NAME,SYSIN_PGM,判定DD,追加DSN


    df = QRY_JCL_PGM_DSN_BMCP_.get()
    for data in df:
        
        # 'LIBRARY_ID = data["LIBRARY_ID"]
        LIBRARY_ID = data["LIBRARY_ID"]
        JCL_NAME = data["JCL_NAME"]
        JOB_SEQ = data["JOB_SEQ"]
        JOB_ID = data["JOB_ID"]
        STEP_SEQ = data["STEP_SEQ"]
        STEP_ID = data["STEP_NAME"]
        PGM_NAME = data["PGM_NAME"]
        PROC_NAME = data["PROC_NAME"]
        SYSIN_PGM = data["SYSIN_PGM"]
                            
        判定DD = "_SYSB001"                # 'ここが違う
        追加DSN = 関連データ
    
        if 応用_顧客別_JCL_PGM_DSN_FOR_DB_JFE_.insert() == False:
            pass
        else:
            DD_CNT = DD_CNT + 1
                                     
#関数の定義: 特定の処理に基づいてデータベースを更新するための関数
#'20240215 UPD qian.e.wang
#def 各種登録DB更新(P_実行カウント,ActSheet_x):
def 各種登録DB更新(P_実行カウント,ActSheet_x,JFE_関連DSN):
#    global JFE_関連DSN特定_,応用_顧客別_資産関連性情報_INSERT_FOR_COBOL_,応用_顧客別_PGM_IO情報_
    global JFE_判定IO特定_,応用_顧客別_資産関連性情報_INSERT_FOR_COBOL_,応用_顧客別_PGM_IO情報_
#    global 資産ID,COBOL_ID,関連資産,JFE_データ分類,JFE_処理レコード,JFE_CRUD判定,JFE_IO判定,DD_CNT,呼出方法,判定PGM,IO判定,JFE_関連DSN,関連データ
    global 資産ID,COBOL_ID,関連資産,JFE_データ分類,JFE_処理レコード,JFE_CRUD判定,JFE_IO判定,DD_CNT,呼出方法,判定PGM,IO判定,関連データ,JFE_DSN
#'UPD END
    
    if JFE_データ分類 != "" and JFE_処理レコード != "":
        
#'20240215 DEL qian.e.wang
#        if  "-" in JFE_処理レコード:
#            JFE_関連DSN = "変数値要確認"
#        else:
#            JFE_関連DSN = JFE_関連DSN特定_.get()
#'DEL END
           
        #    '===暫定対応（関連性設定されるまで）===
        #    'if JFE_関連DSN = "設定無":
        #    '   JFE_関連DSN = JFE_処理レコード + "(確認中)"
        #    'End If
        #    '======================================
        
        if ActSheet_x[15] == "":
            ActSheet_x[15] = JFE_関連DSN
        else:
            ActSheet_x[15] = ActSheet_x[15] + vbLf + JFE_関連DSN
        
           #2-2 資産関連性情報出力
        DD_CNT = 0
           
        if COBOL_ID != "":
            if JFE_CRUD判定 != "" and JFE_CRUD判定 != "NA":
                if JFE_データ分類 == "DAM":
                    呼出方法 = "COBOL-DAM-" + JFE_CRUD判定
                    判定PGM = JFE_関連DSN                       #'※この処理の「判定PGM」は呼出先PGM　今回の場合はデータ
                if JFE_データ分類 == "独自DAM":
                    呼出方法 = "COBOL-DAM-" + JFE_CRUD判定
                    判定PGM = JFE_関連DSN                       #'※この処理の「判定PGM」は呼出先PGM　今回の場合はデータ
                if JFE_データ分類 == "NDB":
                    呼出方法 = "COBOL-NDB-" + JFE_CRUD判定
                    判定PGM = JFE_処理レコード
#'20240213 ADD qian.e.wang
                if JFE_データ分類 == "ADABAS":
                    呼出方法 = "COBOL-ADABAS-" + JFE_CRUD判定
                    判定PGM = JFE_処理レコード
                if JFE_データ分類 == "DB2":
                    呼出方法 = "COBOL-DB2-" + JFE_CRUD判定
                    判定PGM = JFE_処理レコード
#'END ADD
#'20240611 ADD qian.e.wang 長野県信テストIO出力対応
                if JFE_データ分類 == "SUP":
                    呼出方法 = "COBOL-SUP-" + JFE_CRUD判定
                    判定PGM = JFE_処理レコード
#'ADD END
                if JFE_データ分類 == "基準":
                    呼出方法 = "COBOL-基準"
                    判定PGM = JFE_関連DSN
           
                if 応用_顧客別_資産関連性情報_INSERT_FOR_COBOL_.insert() == False:
                    ActSheet_x[16] = "既存SKIP"
                else:
                    #'ActSheet_x[16] = ActSheet_x[16] + 1
                    DD_CNT = DD_CNT + 1
        else:
            ActSheet_x[16] = "エラー"
        
        #'JSI用XDBREF解析処理
        if P_実行カウント == 1:
            if ActSheet_x[21] != "":
                呼出方法 = "COBOL-NDB(JSI)-" + JFE_CRUD判定
                判定PGM = ActSheet_x[21]
    
                if 応用_顧客別_資産関連性情報_INSERT_FOR_COBOL_.insert() == False:
                    ActSheet_x[16] = "既存SKIP"
                else:
                    #'ActSheet_x[16] = ActSheet_x[16] + 1
                    DD_CNT = DD_CNT + 1
    
    
        if ActSheet_x[16] == "":
            ActSheet_x[16] = DD_CNT
        else:
            ActSheet_x[16] = str(ActSheet_x[16]) + str(DD_CNT)
        
#            '2-3 最上位PGM特定（出来ればバッチのみ）
           
# '処理が重い為一旦保留
# '           判定PGM = COBOL_ID   '
# '           Call 最上位PGM解析   'MHI案件の処理を流用、処理ロジックは「顧客別_資産関連性情報」をベースに解析するように改修
# '           判定PGM = ""         '誤解析防止のため初期化
# '           関連データ = JFE_関連DSN

        #    '2-4 PGM-IO情報出力
#'20240213 UPD qian.e.wang
#        if P_実行カウント == 1:
#            IO判定 = JFE_IO判定
#            判定PGM = COBOL_ID
#            関連データ = JFE_関連DSN
#            if 関連データ != "":
#                if 応用_顧客別_PGM_IO情報_.insert() == False:
#                    pass
#                else:
#                    ActSheet_x[17] = 1
#        判定PGM = COBOL_ID

        判定PGM = 関連資産
        関連データ = JFE_関連DSN
        
        if JFE_データ分類 == "DAM":
            JFE_DSN = 関連データ.replace("DAM:", "").replace("(設定無)", "").replace("(" + 判定PGM + ")", "")
        if JFE_データ分類 == "独自DAM":
            JFE_DSN = 関連データ.replace("独自DAM:", "").replace("(設定無)", "").replace("(" + 判定PGM + ")", "")
        if JFE_データ分類 == "NDB":
            JFE_DSN = 関連データ.replace("NDB:", "").replace("(設定無)", "").replace("(" + 判定PGM + ")", "")
        if JFE_データ分類 == "ADABAS":
            JFE_DSN = 関連データ.replace("ADABAS:", "").replace("(設定無)", "").replace("(" + 判定PGM + ")", "")
        if JFE_データ分類 == "DB2":
            JFE_DSN = 関連データ.replace("DB2:", "").replace("(設定無)", "").replace("(" + 判定PGM + ")", "")
#'20240611 ADD qian.e.wang 長野県信テストIO出力対応
        if JFE_データ分類 == "SUP":
            JFE_DSN = 関連データ.replace("SUP:", "").replace("(設定無)", "").replace("(" + 判定PGM + ")", "")
#'ADD END
        if JFE_データ分類 == "基準":
            JFE_DSN = 関連データ.replace("基準:", "").replace("(設定無)", "").replace("(" + 判定PGM + ")", "")
        
        IO判定 = JFE_判定IO特定_.get()
        if IO判定 == "":
            IO判定 = JFE_IO判定

        if 関連データ != "":
            if 応用_顧客別_PGM_IO情報_.insert() == False:
                pass
            else:
                ActSheet_x[17] = 1

        # DEBUG
        # print("■③ IO判定 :["+str(IO判定)+"] 判定PGM :["+str(判定PGM)+"] 関連データ :["+str(関連データ)+"]\r\n")
#'UPD END

        BMCP以外処理()

        BMCP処理()

        ActSheet_x[18] = DD_CNT

    else:
        if JFE_データ分類 != "" and JFE_処理レコード == "":
            ActSheet_x[20] = "CALL命令文法要確認"
            
    return ActSheet_x


def analysis2(db_path,title,excel_path):
    global JFE_関連DSN特定_,応用_顧客別_資産関連性情報_INSERT_FOR_COBOL_,応用_顧客別_PGM_IO情報_,顧客別_JCL_PGM_DSN_BMCP以外_,QRY_JCL_PGM_DSN_BMCP_,応用_顧客別_JCL_PGM_DSN_FOR_DB_JFE_
#'20240215 ADD qian.e.wang
    global JFE_判定IO特定_
#'ADD END
    global ActSheet, ActSheet_x
    global 資産ID,COBOL_ID,関連資産,JFE_データ分類,JFE_処理レコード,JFE_CRUD判定,JFE_IO判定
    
    if os.path.isdir(title) == False:
        os.makedirs(title)
         
        
    start = time.time()
    ### 既存DB削除
    conn = connect_accdb(db_path)
    cursor = conn.cursor()
    
    sql = "SELECT * FROM 顧客別_資産関連性情報 WHERE 登録分類 = '自動設定（JFE_DB特定）'"
    df = pd.read_sql(sql,conn)
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("顧客別_資産関連性情報",values,keys)
        cursor.execute(sql,values)

    sql = "SELECT * FROM 顧客別_JCL_PGM_DSN WHERE 手動更新FLG = '' AND 自動更新FLG = '自動設定（JFE_DB特定）'"
    df = pd.read_sql(sql,conn)
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("顧客別_JCL_PGM_DSN",values,keys)
        cursor.execute(sql,values)
      
    sql = "SELECT * FROM 顧客別_PGM_IO情報 WHERE 資産分類 = 'COBOL_自動'"
    df = pd.read_sql(sql,conn)
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("顧客別_PGM_IO情報",values,keys)
        cursor.execute(sql,values)
    
    # sql,values = make_delete_sql("顧客別_PGM_IO情報",["COBOL_自動"],["資産分類"])    
    # cursor.execute(sql,values)
    
    # sql,values = make_delete_sql("顧客別_JCL_PGM_DSN",["",DB自動登録時PARM],["手動更新FLG","自動更新FLG"])
    # cursor.execute(sql,values)
    
    # sql,values = make_delete_sql("顧客別_資産関連性情報",[DB自動登録時PARM],["登録分類"])
    # cursor.execute(sql,values)
    
    conn.commit()
    print("DB削除完了", time.time()-start)
    
    ## CRUD判定で "NA" とされている箇所がpandasだと nan になってしまうため、 "NA" のケースだけ除外する。
    na_values = ["", 
             "#N/A", 
             "#N/A N/A", 
             "#NA", 
             "-1.#IND", 
             "-1.#QNAN", 
             "-NaN", 
             "-nan", 
             "1.#IND", 
             "1.#QNAN", 
             "<NA>", 
             "N/A", 
#              "NA", 
             "NULL", 
             "NaN", 
             "n/a", 
             "nan", 
             "null"
             ]

    df = pd.read_excel(excel_path,sheet_name="JFE_DB利用個所特定",na_values=na_values,keep_default_na=False)
    df.fillna("",inplace=True)

    
    JFE_関連DSN特定_ = JFE_関連DSN特定(conn,cursor)
    応用_顧客別_資産関連性情報_INSERT_FOR_COBOL_ = 応用_顧客別_資産関連性情報_INSERT_FOR_COBOL(conn,cursor)
    応用_顧客別_PGM_IO情報_ = 応用_顧客別_PGM_IO情報(conn,cursor)
    顧客別_JCL_PGM_DSN_BMCP以外_ = 顧客別_JCL_PGM_DSN_BMCP以外(conn,cursor)
    QRY_JCL_PGM_DSN_BMCP_ = QRY_JCL_PGM_DSN_BMCP(conn,cursor)
    応用_顧客別_JCL_PGM_DSN_FOR_DB_JFE_ = 応用_顧客別_JCL_PGM_DSN_FOR_DB_JFE(conn,cursor)
    
    ActSheet = []
#'20240215 ADD qian.e.wang
    分割_関連DSN = []
    JFE_判定IO特定_ = JFE_判定IO特定(conn,cursor)
#'ADD END
    
    for i in range(len(df)):
        data = df.iloc[i]
        ActSheet_x = [""]+list(data)
        資産ID = ActSheet_x[1]
        COBOL_ID = ActSheet_x[2]
        関連資産 = ActSheet_x[3]
        JFE_データ分類 = ActSheet_x[4]
        JFE_処理レコード_1_5 = ActSheet_x[7:12]
        JFE_CRUD判定 = ActSheet_x[13]
        JFE_IO判定 = ActSheet_x[14]

        for i in range(5):
            if JFE_処理レコード_1_5[i] != "":
                JFE_処理レコード = JFE_処理レコード_1_5[i]
#'20240215 UPD qian.e.wang
#                ActSheet_x = 各種登録DB更新(i+1,ActSheet_x)
                if  "-" in JFE_処理レコード:
                    JFE_関連DSN = "変数値要確認"
                    ActSheet_x = 各種登録DB更新(i+1,ActSheet_x,JFE_関連DSN)
                    
                    ActSheet.append(ActSheet_x)
                else:
                    JFE_関連DSN = ""
                    分割_関連DSN = JFE_関連DSN特定_.get().split(";")
                    for j in range(len(分割_関連DSN)):
                        JFE_関連DSN = 分割_関連DSN[j]

                        ActSheet_x = [""]+list(data)
                        資産ID = ActSheet_x[1]
                        COBOL_ID = ActSheet_x[2]
                        関連資産 = ActSheet_x[3]
                        JFE_データ分類 = ActSheet_x[4]
                        JFE_処理レコード_1_5 = ActSheet_x[7:12]
                        JFE_CRUD判定 = ActSheet_x[13]
                        JFE_IO判定 = ActSheet_x[14]

                        # DEBUG
                        # print("■① JFE_データ分類 :["+str(JFE_データ分類)+"] JFE_処理レコード :["+str(JFE_処理レコード)+"]  JFE_関連DSN :["+str(JFE_関連DSN)+"]\r\n")

                        if JFE_関連DSN != "":
                            ActSheet_x = 各種登録DB更新(i+j+1,ActSheet_x,JFE_関連DSN)
                            ActSheet.append(ActSheet_x)
            else:
                ActSheet.append(ActSheet_x)

#        ActSheet.append(ActSheet_x)
#'UPD END
        
    ActSheet_all = [actSheet[1:] for actSheet in ActSheet]
    print("解析完了", time.time()-start)
    write_excel_multi_sheet("JFE-DB利用箇所特定2.xlsx",ActSheet_all,"JFE_DB利用個所特定",title,output_header)
    
    conn.close()
    
    # return ActSheet
        
        
        
# analysis2(sys.argv[1],sys.argv[2],sys.argv[3])
