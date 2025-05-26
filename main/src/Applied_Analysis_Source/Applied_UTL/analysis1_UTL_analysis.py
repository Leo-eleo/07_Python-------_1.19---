#!/usr/bin/env python
# -*- coding: cp932 -*-
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


conn = None
cursor = None

分割文字列 = []
分割文字列2 = []
vbCrLf = "\n"
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
呼出方法 = ""
判定PGM = ""
DB自動登録時PARM = "自動設定（UTL解析）"
PGM予備 = ""
判定MODE = ""

JCL_NAME_SV = ""
JOB_SEQ_SV = 0
STEP_SEQ_SV = 0
DELETE継続 = False
DUMP継続 = False
RESTORE継続 = False
FTP継続 = False
DEFCL継続 = False
### 20210312 Add Horiuchi
DEFPATH継続 = False
DEFAIX継続 = False
DEFNVSAM継続 = False
DEFUCAT継続 = False
COPY継続 = False
LOAD継続 = False
UNLOAD継続 = False
UTACH継続 = False
#'20240215 ADD qian.e.wang
ADARUN3V継続 = False
JYAADP継続 = False
ADM継続 = False
#'ADD END
判定DD = ""
追加DSN = ""
IO判定 = ""
RESTOREモード = ""
置換DSN = ""
判定DD_OUT_SV = ""
動的要素 = []
REPRO_OUTDATASET_利用DD取得_ = None
応用_顧客別_JCL_STEP_SYSIN_ = None
#応用_顧客別_資産関連性情報_ = None
応用_顧客別_JCL_PGM_DSN_ = None
応用_UTL_STEP別_IO情報_ = None
ActSheet = []
転送継続 = ""


class REPRO_OUTDATASET_利用DD取得:
    
    def __init__(self,db_path):
        self.dic = None
        # self.conn = None
        # self.cursor = None
        self.dbname = "顧客別_JCL_PGM_DSN"
        self.db_path = db_path
        

    def setup(self):
        self.dic = {}
        global conn,cursor
        # self.conn = connect_accdb(self.db_path)
        # self.cursor = self.conn.cursor()
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,conn)
        df.fillna("",inplace=True)
        
        for jcl,job,step,dsn,dd in zip(df["JCL_NAME"],df["JOB_SEQ"],df["STEP_SEQ"],df["DSN"],df["DD_NAME"]):
            self.dic[(jcl,job,step,dsn)] = str(dd)
            
        
    def get(self):
        global JCL_NAME,JOB_SEQ,STEP_SEQ,追加DSN
           
        if self.dic == None:
            self.setup()
            
        if (JCL_NAME,JOB_SEQ,STEP_SEQ,追加DSN) in self.dic:
            return self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ,追加DSN)]
        
        else:
            return ""
        
class 応用_顧客別_JCL_STEP_SYSIN:
    
    def __init__(self,db_path):
        self.dic = None
        # self.conn = None
        # self.cursor = None
        self.all_list = None
        self.update_info_dic = {}
        self.db_key_list = None
        self.key_to_index = {}
        self.dbname = "顧客別_JCL_STEP_SYSIN"
        self.db_path = db_path
        
        self.step_sysin_update_dic = {}
        
    def setup(self):
        self.dic = {}
        global conn,cursor
        # self.conn = connect_accdb(self.db_path)
        # self.cursor = self.conn.cursor()
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,conn)
        df.fillna("",inplace=True)
        self.all_list = df.values.tolist()
        self.db_key_list = df.columns.tolist()
        self.key_to_index = {key:i for i,key in enumerate(self.db_key_list)}
        
        for i,data in enumerate(self.all_list):
            jcl,job,step = data[self.key_to_index["JCL_NAME"]],data[self.key_to_index["JOB_SEQ"]],data[self.key_to_index["STEP_SEQ"]]
            if (jcl,job,step) not in self.dic:
                self.dic[(jcl,job,step)] = []
            self.dic[(jcl,job,step)].append(i)
            
            if (jcl,job,step) not in self.update_info_dic:
                self.update_info_dic[(jcl,job,step)] = []
            self.update_info_dic[(jcl,job,step)].append(i)
    
        
    def update(self):
        if self.dic == None:
            self.setup()
            
        global JCL_NAME,JOB_SEQ,STEP_SEQ,判定PGM,DB自動登録時PARM
        
        if (JCL_NAME,JOB_SEQ,STEP_SEQ) not in self.dic:
            return False

        for index in self.update_info_dic[(JCL_NAME,JOB_SEQ,STEP_SEQ)]:
            self.all_list[index][self.key_to_index["SYSIN_PGM"]] = 判定PGM
            self.all_list[index][self.key_to_index["自動更新FLG"]] = DB自動登録時PARM  
        
        self.step_sysin_update_dic[(JCL_NAME,JOB_SEQ,STEP_SEQ)] = 判定PGM # VBAの場合はDBをUPDATEすると myRSの内容も更新されるが、pythonでは異なるので更新された内容を持っておく
                
        return True
    
    def _close_conn(self):
        global conn
        
        if conn != None:
            conn.close()
            
        # if self.conn != None:
        #     self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
        
        
    def _delete_all(self):
        sql,values = make_delete_sql(self.dbname,[],[])
        global conn,cursor
        cursor.execute(sql,values)
        conn.commit()
        
        
    def update_all(self):
        global conn,cursor
        # self.conn = connect_accdb(self.db_path)
        # self.cursor = self.conn.cursor()
        
        self._delete_all()
        self._close_conn()
        compact_accdb(self.db_path)
        
        conn = connect_accdb(self.db_path)
        cursor = conn.cursor()
        # self.conn = connect_accdb(self.db_path)
        # self.cursor = self.conn.cursor()

        if self.all_list != None:
            for data in self.all_list:

                sql,value = make_insert_sql(self.dbname,data,self.db_key_list)
                cursor.execute(sql,value)
                # self.cursor.execute(sql,value)
                # self.conn.commit()
        conn.commit()
        # self._close_conn()
            
    
#class 応用_顧客別_資産関連性情報:
#    
#    def __init__(self,db_path):
#        self.dic = None
#        self.conn = None
#        self.cursor = None
#        self.dbname = "顧客別_資産関連性情報"
#        self.db_path = db_path
#
#    def setup(self):
#        self.dic = {}
#        self.conn = connect_accdb(self.db_path)
#        self.cursor = self.conn.cursor()
#        sql = "SELECT * FROM "+self.dbname
#        
#        df = pd.read_sql(sql,self.conn)
#        df.fillna("",inplace=True)
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
#        self.conn.commit()
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
    
class 応用_顧客別_JCL_PGM_DSN:
    def __init__(self,db_path):
        self.dic = None
        # self.conn = None
        # self.cursor = None
        self.all_list = None
        self.update_info_dic = {}
        self.db_key_list = None
        self.key_to_index = {}
        self.dbname = "顧客別_JCL_PGM_DSN"
        self.db_path = db_path

    def setup(self):
        self.dic = {}
        global conn,cursor
        # self.conn = connect_accdb(self.db_path)
        # self.cursor = self.conn.cursor()
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,conn)
        df.fillna("",inplace=True)
        self.all_list = df.values.tolist()
        self.db_key_list = df.columns.tolist()
        self.key_to_index = {key:i for i,key in enumerate(self.db_key_list)}
        
        for i,data in enumerate(self.all_list):
            jcl,job,step,dd,dsn = data[self.key_to_index["JCL_NAME"]],data[self.key_to_index["JOB_SEQ"]],data[self.key_to_index["STEP_SEQ"]],data[self.key_to_index["DD_NAME"]],data[self.key_to_index["DSN"]]
                        
            self.dic[(jcl,job,step,dd,dsn)] = 1
            if (jcl,job,step) not in self.dic:
                self.dic[(jcl,job,step)] = []
            self.dic[(jcl,job,step)].append([dd,dsn])


            if (jcl,job,step) not in self.update_info_dic:
                self.update_info_dic[(jcl,job,step)] = []
            self.update_info_dic[(jcl,job,step)].append(i)
        
    def insert(self):
        if self.dic == None:
            self.setup()
        
        global LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME,PROC_NAME
        
        global 判定PGM,DB自動登録時PARM,判定DD,追加DSN

        if (JCL_NAME,JOB_SEQ,STEP_SEQ,判定DD,追加DSN) in self.dic and self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ,判定DD,追加DSN)] == 1:
            return False
        
        insert_list = [""]*len(self.db_key_list)
        
        key_list = ["LIBRARY_ID","JCL_NAME","JOB_SEQ","JOB_ID","STEP_SEQ","STEP_NAME","PGM_NAME","PROC_NAME","SYSIN_PGM","DD_NAME","DSN","手動更新FLG","自動更新FLG"]
        value_list = [LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME,PROC_NAME,判定PGM,判定DD,追加DSN.replace("\"",""),"",DB自動登録時PARM]

        for key,value in zip(key_list,value_list):
            insert_list[self.key_to_index[key]] = value
        
        if (JCL_NAME,JOB_SEQ,STEP_SEQ) not in self.update_info_dic:
            self.update_info_dic[(JCL_NAME,JOB_SEQ,STEP_SEQ)] = []
        
        self.update_info_dic[(JCL_NAME,JOB_SEQ,STEP_SEQ)].append(len(self.all_list))
        self.all_list.append(insert_list)

        self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ,判定DD,追加DSN)] = 1
        self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ)] = 1
        
        return True

    def update(self):
        if self.dic == None:
            self.setup()
        
        global JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID
        
        global 判定PGM,DB自動登録時PARM,判定DD,追加DSN

        if (JCL_NAME,JOB_SEQ,STEP_SEQ) not in self.dic:
            return False
        
        for index in self.update_info_dic[(JCL_NAME,JOB_SEQ,STEP_SEQ)]:
            self.all_list[index][self.key_to_index["SYSIN_PGM"]] = 判定PGM
            self.all_list[index][self.key_to_index["自動更新FLG"]] = DB自動登録時PARM  
            
        for i,v in enumerate(str(self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ)])):
            #pgm,dd = v
            #self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ)][i][0] = 判定PGM
            #self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ,pgm,dd)] = 0
            #self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ,判定PGM,dd)] = 1
            if len(v) == 2:
                pgm,dd = v
                self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ)][i][0] = 判定PGM
                self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ,pgm,dd)] = 0
                self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ,判定PGM,dd)] = 1
        
        return True
    
    def _close_conn(self):
        global conn
        
        if conn != None:
            conn.close()
            
        # if self.conn != None:
        #     self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
        
        
    def _delete_all(self):
        sql,values = make_delete_sql(self.dbname,[],[])
        global conn,cursor
        cursor.execute(sql,values)
        conn.commit()
        
        
    def update_all(self):
        global conn,cursor
        # self.conn = connect_accdb(self.db_path)
        # self.cursor = self.conn.cursor()
        
        self._delete_all()
        self._close_conn()
        compact_accdb(self.db_path)
        
        conn = connect_accdb(self.db_path)
        cursor = conn.cursor()
        # self.conn = connect_accdb(self.db_path)
        # self.cursor = self.conn.cursor()

        if self.all_list != None:
            for data in self.all_list:

                sql,value = make_insert_sql(self.dbname,data,self.db_key_list)
                cursor.execute(sql,value)
                # self.cursor.execute(sql,value)
                # self.conn.commit()
        conn.commit()
        # self._close_conn()
    
        

class 応用_UTL_STEP別_IO情報:
    def __init__(self,db_path):
        self.dic = None
        # self.conn = None
        # self.cursor = None
        self.all_list = None
        self.update_info_dic = {}
        self.db_key_list = None
        self.key_to_index = {}
        
        self.dbname = "UTL_STEP別_IO情報"
        self.db_path= db_path

    def setup(self):
        self.dic = {}
        global conn,cursor
        # self.conn = connect_accdb(self.db_path)
        # self.cursor = self.conn.cursor()
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,conn)
        df.fillna("",inplace=True)
        
        self.all_list = df.values.tolist()
        self.db_key_list = df.columns.tolist()
        self.key_to_index = {key:i for i,key in enumerate(self.db_key_list)}
        
        for i,data in enumerate(self.all_list):
            jcl,job,step,dd,io = data[self.key_to_index["JCL_NAME"]],data[self.key_to_index["JOB_SEQ"]],data[self.key_to_index["STEP_SEQ"]],data[self.key_to_index["DD名"]],data[self.key_to_index["IO"]]
                        
            if io == "DELETE":
                self.dic[(jcl,job,step,dd)] = 1
            else:
                self.dic[(jcl,job,step,dd)] = 0
                
            if (jcl,job,step,dd) not in self.update_info_dic:
                self.update_info_dic[(jcl,job,step,dd)] = []
            self.update_info_dic[(jcl,job,step,dd)].append(i)
    
        
    def update(self):
        if self.dic == None:
            self.setup()
        
        global JCL_NAME,JOB_SEQ,STEP_SEQ
        
        global DB自動登録時PARM,判定DD,IO判定

        if (JCL_NAME,JOB_SEQ,STEP_SEQ,判定DD) not in self.dic or self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ,判定DD)] == 0:
            return False

        for index in self.update_info_dic[(JCL_NAME,JOB_SEQ,STEP_SEQ,判定DD)]:
            self.all_list[index][self.key_to_index["IO"]] = IO判定
            self.all_list[index][self.key_to_index["補足"]] = DB自動登録時PARM 
        
        if IO判定 != "DELETE":
            self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ,判定DD)] = 0
            
        
        return True
    
    def insert(self):
        if self.dic == None:
            self.setup()
        
        global JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME
        
        global DB自動登録時PARM,判定DD,IO判定

        if (JCL_NAME,JOB_SEQ,STEP_SEQ,判定DD) in self.dic:
            return False
        
        insert_list = [""]*len(self.db_key_list)
        
        key_list = ["JCL_NAME","JOB_SEQ","JOB_ID","STEP_SEQ","STEP名","DD名","IO","Utility_ID","補足"]
        value_list = [JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,判定DD,IO判定,PGM_NAME,DB自動登録時PARM]
        for key,value in zip(key_list,value_list):
            insert_list[self.key_to_index[key]] = value
        
        self.update_info_dic[(JCL_NAME,JOB_SEQ,STEP_SEQ,判定DD)] = [len(self.all_list)]
        self.all_list.append(insert_list)
        
        if IO判定 == "DELETE":
            self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ,判定DD)] = 1
        else:
            self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ,判定DD)] = 0
        
        return True
    
    def _close_conn(self):
        global conn
        
        if conn != None:
            conn.close()
            
        # if self.conn != None:
        #     self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
        
        
    def _delete_all(self):
        sql,values = make_delete_sql(self.dbname,[],[])
        global conn,cursor
        #cursor.execute(sql,values)
        #conn.commit()
        
        
    def update_all(self):
        global conn,cursor
        # self.conn = connect_accdb(self.db_path)
        # self.cursor = self.conn.cursor()
        
        self._delete_all()
        self._close_conn()
        compact_accdb(self.db_path)
        
        conn = connect_accdb(self.db_path)
        cursor = conn.cursor()
        # self.conn = connect_accdb(self.db_path)
        # self.cursor = self.conn.cursor()

        if self.all_list != None:
            for data in self.all_list:

                sql,value = make_insert_sql(self.dbname,data,self.db_key_list)
                cursor.execute(sql,value)
                # self.cursor.execute(sql,value)
                # self.conn.commit()
        conn.commit()
        # self._close_conn()
        
    

def JCL_STEP_SYSIN解析_共通出力(data):
    
	global 応用_顧客別_JCL_STEP_SYSIN_
	global LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME,PROC_NAME,SYSIN_PGM,SYSIN_SEQ,PARM_EXEC,PARM_PROC,SYSIN
	global 分割文字列,分割文字列2,資産関連性_追加_CNT,JCL_PGM_DSN_追加_CNT,JCL_PGM_DSN_更新_CNT,UTL_STEP別_IO情報_追加_CNT

	ActSheet_x = [""]*20

	ActSheet_x[1]= data["LIBRARY_ID"]
	ActSheet_x[2]= data["JCL_NAME"]
	ActSheet_x[3]= data["JOB_SEQ"]
	ActSheet_x[4]= data["JOB_ID"]
	ActSheet_x[5]= data["STEP_SEQ"]
	ActSheet_x[6]= data["STEP_ID"]
	ActSheet_x[7]= data["PGM_NAME"]
	ActSheet_x[8]= data["PROC_NAME"]
	ActSheet_x[9]= data["SYSIN_PGM"]
	ActSheet_x[10]= data["SYSIN_SEQ"]
	ActSheet_x[11]= data["SYSIN"]
	# ActSheet_x[14]= 0
	LIBRARY_ID = data["LIBRARY_ID"]
	JCL_NAME = data["JCL_NAME"]
	JOB_SEQ = data["JOB_SEQ"]
	JOB_ID = data["JOB_ID"]
	STEP_SEQ = data["STEP_SEQ"]
	STEP_ID = data["STEP_ID"]
	PGM_NAME = data["PGM_NAME"]
	PROC_NAME = data["PROC_NAME"]
	SYSIN_PGM = data["SYSIN_PGM"]
	SYSIN_SEQ = data["SYSIN_SEQ"]
	SYSIN = data["SYSIN"]

	if (JCL_NAME,JOB_SEQ,STEP_SEQ) in 応用_顧客別_JCL_STEP_SYSIN_.step_sysin_update_dic:
		SYSIN_PGM =  応用_顧客別_JCL_STEP_SYSIN_.step_sysin_update_dic[(JCL_NAME,JOB_SEQ,STEP_SEQ)]
		ActSheet_x[9] = SYSIN_PGM

#'20240215 UPD qian.e.wang
#	分割文字列 = SYSIN.split(" ")
	分割文字列 = Mid(SYSIN, 0, 72).split(" ")
#	分割文字列2 = ArrayEmptyDelete(SYSIN.split(" "))       ###2020/2/13 追加
	分割文字列2 = ArrayEmptyDelete(Mid(SYSIN, 0, 72).split(" "))
#'UPD END

	資産関連性_追加_CNT = 0
	JCL_PGM_DSN_追加_CNT = 0
	JCL_PGM_DSN_更新_CNT = 0
	UTL_STEP別_IO情報_追加_CNT = 0

	return ActSheet_x


def 継続処理解除判定(ActSheet_x,data):
    global 応用_顧客別_JCL_PGM_DSN_,応用_UTL_STEP別_IO情報_
    global SYSIN
    global DELETE継続,DUMP継続,RESTORE継続,FTP継続,DEFCL継続,DEFPATH継続,DEFAIX継続,DEFNVSAM継続,DEFUCAT継続,COPY継続,LOAD継続,UNLOAD継続,UTACH継続
    global DD_CNT,判定DD,IO判定,追加DSN,判定DD_OUT_SV,分割文字列,分割文字列2,vbCrLf
#'20240215 ADD qian.e.wang
    global ADARUN3V継続,JYAADP継続,ADM継続
#'ADD END
    
    L_str = ""
    
    
    ###共通判定
    if data["SYSIN_SEQ"] == 1:
       DD_CNT = 0

    if DUMP継続:
        if data["SYSIN_SEQ"] == 1:
            DUMP継続 = False
            ###DD_CNT = 0
 
    ###if RESTORE継続:    'ここでは解除しないRESTorE処理内で実施
    ###    if data["SYSIN_SEQ = 1:
    ###      RESTORE継続 = False
    ###      'DD_CNT = 0
       
    if DELETE継続:
        if data["SYSIN_SEQ"] == 1:
            DELETE継続 = False
            ###DD_CNT = 0
        elif "DEFINE " in SYSIN or  "DEF " in SYSIN:
            DELETE継続 = False

    if COPY継続:
        if data["SYSIN_SEQ"] == 1:
            COPY継続 = False
            ###DD_CNT = 0
        elif "COPY " not in SYSIN:
            COPY継続 = False

    if LOAD継続:
        if data["SYSIN_SEQ"] == 1:
            LOAD継続 = False
        else:
            ActSheet_x[12] = "LOAD継続"
            if "INTO " in SYSIN and " TABLE " in SYSIN:
                for i in range(len(分割文字列2)):
                    if 分割文字列2[i] == "TABLE":
                        判定DD = "_SYSD001"
                        IO判定 = "OUTPUT"
           
                      ###UTL_STEP別_IO情報 出力
                    if 応用_UTL_STEP別_IO情報_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                        ActSheet_x[16] = 0
                    else:
                        ActSheet_x[16] = 1
           
                      ### 顧客別_JCL_PGM_DSN 出力
                    if i + 1 < len(分割文字列2):
                        追加DSN = 分割文字列2[i + 1]
                        
                        追加DSN = 追加DSN.replace("JBDB2.", "")     ###MHI案件のみ暫定対応
                        if 応用_顧客別_JCL_PGM_DSN_.insert() == False:
                            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                            ActSheet_x[14] = 0
                        else:
                            ActSheet_x[14] = 1
                        ActSheet_x[17] = 追加DSN
                    else:
                        ActSheet_x[12] = ActSheet_x[12] + " 配列要素要確認"      ###LOAD先情報は1行内に記載がある想定


    if UNLOAD継続:
        if data["SYSIN_SEQ"] == 1:
            UNLOAD継続 = False
        else:
           ActSheet_x[12] = "UNLOAD継続"
           if "FROM " in SYSIN and " TABLE " in SYSIN:
           
                for i in range(len(分割文字列2)):
                    if 分割文字列2[i] == "TABLE":
                        判定DD = "_SYSD001"
                        IO判定 = "INPUT"
           
                      ###UTL_STEP別_IO情報 出力
                        if 応用_UTL_STEP別_IO情報_.insert() == False:
                            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                            ActSheet_x[16] = 0
                        else:
                            ActSheet_x[16] = 1
           
                      ###顧客別_JCL_PGM_DSN 出力
                        if i + 1 < len(分割文字列2):
                            追加DSN = 分割文字列2[i + 1]
                            追加DSN = 追加DSN.replace("JBDB2.", "")     ###MHI案件のみ暫定対応
                            if 応用_顧客別_JCL_PGM_DSN_.insert() == False:
                                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                                ActSheet_x[14] = 0
                            else:
                                ActSheet_x[14] = 1
                            ActSheet_x[17] = 追加DSN
                        else:
                            ActSheet_x[12] = ActSheet_x[12] + " 配列要素要確認"      ###UNLOAD元情報は1行内に記載がある想定


    if DEFCL継続:   ###DEFCL継続とDELETE継続は重複することがある
         
        if "NAME" in SYSIN:     ###1行で完結するかどうか
                  
            for i in range(len(分割文字列)):
                if "NAME" in 分割文字列[i]:
                    追加DSN = 分割文字列[i].replace("CLUSTER", "").replace("NAME", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
         
             ###顧客別_JCL_PGM_DSN 出力
             
            if 応用_顧客別_JCL_PGM_DSN_.insert() == False:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                ActSheet_x[14] = 0
            else:
                ActSheet_x[14] = 1
            ActSheet_x[17] = 追加DSN     ###CHKのために追加 2020/1/10
                      
            DEFCL継続 = False
        
        if data["SYSIN_SEQ"] == 1:  ###上のNAME定義が見つからなかった場合の為に念のため
            DEFCL継続 = False
            ###DD_CNT = 0
    
    ###20210312 Add Horiuchi
    if DEFAIX継続 or DEFPATH継続 or DEFNVSAM継続 or DEFUCAT継続:   ###DEFCL継続とDELETE継続は重複することがある
        if "NAME" in SYSIN:     ###1行で完結するかどうか
            for i in range(len(分割文字列)):
                if "NAME" in 分割文字列[i]:
                    if DEFAIX継続:
                        追加DSN = 分割文字列[i].replace("ALTERNATEINDEX", "").replace("AIX", "").replace("NAME", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
                    elif DEFPATH継続:
                        追加DSN = 分割文字列[i].replace("PATH", "").replace("NAME", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
                    elif DEFNVSAM継続:
                        追加DSN = 分割文字列[i].replace("NONVSAM", "").replace("NVSAM", "").replace("NAME", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
                    elif DEFUCAT継続:
                        追加DSN = 分割文字列[i].replace("USERCATALOG", "").replace("UCAT", "").replace("NAME", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
  
           
             ###顧客別_JCL_PGM_DSN 出力
             
            if 応用_顧客別_JCL_PGM_DSN_.insert() == False:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                ActSheet_x[14] = 0
            else:
                ActSheet_x[14] = 1
            ActSheet_x[17] = 追加DSN     ###CHKのために追加 2020/1/10
                      
            DEFAIX継続 = False
            DEFPATH継続 = False
            DEFNVSAM継続 = False
            DEFUCAT継続 = False
        if data["SYSIN_SEQ"] == 1:  ###上のNAME定義が見つからなかった場合の為に念のため
            DEFAIX継続 = False
            DEFPATH継続 = False
            DEFNVSAM継続 = False
            DEFUCAT継続 = False
   
    if UTACH継続:
        if data["SYSIN_SEQ"] == 1:
            UTACH継続 = False
   
#'20240215 ADD qian.e.wang
    if ADARUN3V継続:
        if data["SYSIN_SEQ"] == 1:
            ADARUN3V継続 = False
   
    if JYAADP継続:
        if data["SYSIN_SEQ"] == 1:
            JYAADP継続 = False
   
    if ADM継続:
        if data["SYSIN_SEQ"] == 1:
            ADM継続 = False
#'ADD END

    return ActSheet_x



def DELETE継続処理(ActSheet_x,data):
    global 応用_顧客別_JCL_PGM_DSN_,応用_UTL_STEP別_IO情報_
    global SYSIN
    global DELETE継続,DEFCL継続
    global DD_CNT,判定DD,IO判定,追加DSN,判定PGM,分割文字列,分割文字列2,vbCrLf
    
    
    
    ActSheet_x[12] = "DELETE-継続"
               
    SYSIN = data["SYSIN"]
    if "DELETE " in SYSIN or "DEL " in SYSIN:
            DD_CNT = DD_CNT + 1
            追加DSN = SYSIN[:72].replace("  CLUSTER", "").replace("*", "")
            追加DSN = 追加DSN.replace("DELETE ", "").replace("DEL ", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
            判定DD = "_SYSD" + str(DD_CNT).zfill(3)
            IO判定 = "DELETE"
            判定PGM = PGM_NAME

            ### UTL_STEP別_IO情報 出力
            if 応用_UTL_STEP別_IO情報_.insert() == False:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                ActSheet_x[16] = 0
            else:
                ActSheet_x[16] = 1
            
            判定PGM = ""     ###
            ActSheet_x[17] = 追加DSN
            
            ### 顧客別_JCL_PGM_DSN 出力
            if 応用_顧客別_JCL_PGM_DSN_.insert() == False:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                ActSheet_x[14] = 0
            else:
                ActSheet_x[14] = 1

    
    ###DELETE継続中（後）にDEFINE CLUSTERのコマンドが発行される場合の対応
    if "DEFINE " in SYSIN or "DEF " in SYSIN:
        DELETE継続 = False
        ActSheet_x[12] = "DEFCL-継続"
    
        判定DD = "_SYSD" + str(DD_CNT).zfill(3)
        DD_CNT = DD_CNT + 1
        
        ### UTL_STEP別_IO情報 出力
        if 応用_UTL_STEP別_IO情報_.insert() == False:
            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
        else:
            ActSheet_x[16] = 1
    
        if "NAME" in SYSIN:     ###1行で完結するかどうか
            
            for i in range(len(分割文字列)):
                if "NAME" in 分割文字列[i]:
                    追加DSN = 分割文字列[i].replace("CLUSTER", "").replace("NAME", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")

            ### 顧客別_JCL_PGM_DSN 出力    注：ブレイク後なので1行前に出力する（仮）
            if 応用_顧客別_JCL_PGM_DSN_.insert() == False:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
            else:
                ActSheet_x[14] = 1
 
        else:
            DEFCL継続 = True

    return ActSheet_x

def DUMP継続処理(ActSheet_x,data):
    global 応用_顧客別_JCL_PGM_DSN_,応用_UTL_STEP別_IO情報_
    global SYSIN
    global DD_CNT,判定DD,IO判定,追加DSN,判定PGM,vbCrLf
    
    
    
    ActSheet_x[12] = "DUMP-継続"
              
    SYSIN = data["SYSIN"]
            
    if "ENQF" in SYSIN:
        pass
    else:
        追加DSN = SYSIN[:72].replace("DATASET", "").replace("INCLUDE", "").replace("INCL(", "").replace("DS(", "") ###追加対応※見にくいので行分離
        追加DSN = 追加DSN.replace("-", "").replace("(", "").replace(")", "").replace( " ", "")
        DD_CNT = DD_CNT + 1
        判定DD = "_SYSD" + str(DD_CNT).zfill(3)
        ###IO判定 = "INPUT"  'MHI暫定対応　バックアップのINPUTは受領判定しない
        IO判定 = "INPUT_判定除外"
        判定PGM = PGM_NAME
        
        ###不正OPTION除外
        if 追加DSN == "SHR" or 追加DSN == "SETMAXCC=0" or 追加DSN == "OPT4" or 追加DSN == "DELUNCATPURGE":  ###  '発生の都度追加する
            ActSheet_x[17] = 追加DSN
            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "OPTIONキーワードの為処理SKIP"
            return ActSheet_x
    
        
        ### UTL_STEP別_IO情報 出力?A
        if 応用_UTL_STEP別_IO情報_.insert() == False:
            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
        else:
            ActSheet_x[16] = 1
        
        ActSheet_x[17] = 追加DSN
        判定PGM = ""     ###'
        
        ### 顧客別_JCL_PGM_DSN 出力
        if 応用_顧客別_JCL_PGM_DSN_.insert() == False:
            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
        else:
            ActSheet_x[14] = 1

    return ActSheet_x
    

def RESTORE継続処理(ActSheet_x,data):
    global 応用_顧客別_JCL_PGM_DSN_
    global ActSheet 
    global SYSIN

    global DD_CNT,判定DD,IO判定,追加DSN,判定PGM,置換DSN,判定DD_OUT_SV,vbCrLf
    global 分割文字列,分割文字列2,動的要素,要素数
    global JCL_NAME,JOB_SEQ,STEP_SEQ,RESTORE継続
    global L_JCL_NAME_SV, L_JOB_SEQ_SV,L_STEP_SEQ_SV,RESTOREモード
    global JCL_NAME_SV,JOB_SEQ_SV,STEP_SEQ_SV 
    
    global PGM_NAME
    
    L_JCL_NAME_SV = ""   ###ブレイク後に利用するので退避する
    L_JOB_SEQ_SV = ""
    L_STEP_SEQ_SV = ""
    

    goto_flag = False  ### GO TO 文の代わりの flag
    if len(data) == 0:     ###複数行にまたがって処理が完結するためここで実施
        goto_flag = True
    else:
    
        if data["SYSIN_SEQ"] == 1:
           goto_flag = True
        
        if goto_flag == False:
            ### 継続処理
            
            ActSheet_x[12] = " RESTORE-継続"
                    
            if RESTOREモード == "":
            
                if "DATASET(" in SYSIN:
                    RESTOREモード = "DATASET"
                    for i in range(len(分割文字列2)):
                        if "DATASET(" in 分割文字列2[i]:
                            追加DSN = 分割文字列2[0].replace(" ", "").replace("-", "").replace("INCLUDE", "").replace("DATASET", "").replace("(", "").replace(")", "") ###後で確認する　たぶん i が正しい
                    要素数 = 1
                    動的要素 = [追加DSN]
                    ActSheet_x[17] = 追加DSN
                    
            elif RESTOREモード == "DATASET":
            
                if "RENAMEU" in SYSIN:
                    RESTOREモード = "RENAMEU"
                    追加DSN = ""
                    置換DSN = ""
                    for i in range(len(分割文字列2)):
                        if "RENAMEU(" in 分割文字列2[i]:
                            if 追加DSN == "":
                                追加DSN = 分割文字列2[i].replace("RENAMEU", "").replace("(", "")
                        elif 置換DSN == "":
                            if 追加DSN != "":
                                置換DSN = 分割文字列2[i].replace("RENAMEU", "").replace("(", "").replace(")", "")
                    
                    if 追加DSN != "" and 置換DSN != "":
                        for j in range(len(動的要素)):
                            動的要素[j] = 動的要素[j].replace(追加DSN, 置換DSN)
                        ActSheet_x[17] = 置換DSN
                    
                else: ### '複数DATASET処理　配列に格納
                                            
                    追加DSN = 分割文字列2[0].replace(" ", "").replace("-", "").replace("INCLUDE", "").replace("DATASET", "").replace("(", "").replace(")", "")
                    要素数 += 1
                    動的要素.append(追加DSN)
                    ActSheet_x[17] = 追加DSN
                
            elif RESTOREモード == "RENAMEU":
            
                if len(分割文字列2) > 1:
                    追加DSN = 分割文字列2[0].replace("RENAMEU", "").replace("(", "")
                    置換DSN = 分割文字列2[1].replace("RENAMEU", "").replace("(", "").replace(")", "")
            
                    if 追加DSN != "" and 置換DSN != "":
                        for j in range(len(動的要素)):
                            動的要素[j] = 動的要素[j].replace(追加DSN, 置換DSN)
                        ActSheet_x[17] = 置換DSN
                else:
                    ActSheet_x[12] = ActSheet_x[12] + " SKIP"
                

            if data["SYSIN_SEQ"] != 1:
                return ActSheet_x

            
        ###継続解除判定  ※RENAMEUがない場合はここで解除される ※処理する1行前を処理する
        ###　ブレイク時処理　

   

    L_JCL_NAME_SV = JCL_NAME   ###最新状態の退避
    L_JOB_SEQ_SV = JOB_SEQ
    L_STEP_SEQ_SV = STEP_SEQ

    JCL_NAME = JCL_NAME_SV     ### 退避していた値の復元
    JOB_SEQ = JOB_SEQ_SV
    STEP_SEQ = STEP_SEQ_SV

    判定DD = 判定DD_OUT_SV
    for j in range(len(動的要素)):
        if 動的要素[j] == "":
            continue
        
        追加DSN = 動的要素[j]
        ### 顧客別_JCL_PGM_DSN 出力    '
        if len(ActSheet) > 0:
            if 応用_顧客別_JCL_PGM_DSN_.insert() == False:
                ActSheet[-1][12] = ActSheet[-1][12] + vbCrLf + "KEY重複の為処理SKIP"
            else:
                if ActSheet[-1][14] == "":
                    ActSheet[-1][14] = 1
                else:
                    ActSheet[-1][14] = ActSheet[-1][14] + 1
        

    追加DSN = ""
    判定DD = ""
    判定DD_OUT_SV = ""
        
    JCL_NAME_SV = ""
    JOB_SEQ_SV = 0
    STEP_SEQ_SV = 0
        
    JCL_NAME = L_JCL_NAME_SV   ### 退避していた値の復元
    JOB_SEQ = L_JOB_SEQ_SV
    STEP_SEQ = L_STEP_SEQ_SV
        
    RESTORE継続 = False

    return ActSheet_x
    


def FTP継続処理(ActSheet_x,data):
    global 応用_顧客別_JCL_PGM_DSN_,応用_UTL_STEP別_IO情報_
    global FTP継続,SYSIN,転送継続
    global DD_CNT,判定DD,IO判定,追加DSN,判定PGM
    global UTL_STEP別_IO情報_追加_CNT,JCL_PGM_DSN_追加_CNT,分割文字列2,vbCrLf
    

    
    # '=== FTP （MSP）===   2021/12/16 ADD
    # 'JCLサンプル
    # 'FTP A('TISP.FTP.ATTR')
    # 'HOST 172.22.106.41
    # 'SEND IN('USR1.TESTDATA')
    # '     OUT('D:\TESTDATA.bin')
    # '     T(B)
    # '     SYN
    # '     CNVT(NO)
    # '     TYPE(TEXT)
    # '     V(SZIA22)
    # 'RECV IN('D:\Work\IEBGENER.txt')
    # '     OUT('USR1.JCL(IEBGENER)')
    # '     T(T)
    # '     C(Y)
    # '     SYN
    # 'END

    if data["SYSIN_SEQ"] == 1:
        FTP継続 = False
    else:
        ###転送開始
        if " SEND " in SYSIN or str(SYSIN).startswith("SEND "):
            転送継続 = "SEND"
        if " RECV " in SYSIN or str(SYSIN).startswith("RECV "):
            転送継続 = "RECV"
        ### 転送終了
        
        if " END " in SYSIN or str(SYSIN).startswith("END "):
            FTP継続 = False
            転送継続 = ""
       
        if 転送継続 != "" and ( " IN(" in SYSIN or " OUT(" in SYSIN):
            ActSheet_x[12] = " FTP-" + 転送継続 + "-継続"
            追加DSN = ""
            
            for i in range(len(分割文字列2)):
                if "IN(" in 分割文字列2[i]:
                    ### UTL_STEP別_IO情報 出力
                    判定DD = "FTP_" + 転送継続 + "_IN"
                    IO判定 = "INPUT"
                    if 応用_UTL_STEP別_IO情報_.insert() == False:
                       ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                    else:
                       UTL_STEP別_IO情報_追加_CNT = UTL_STEP別_IO情報_追加_CNT + 1
                    
                    ### 顧客別_JCL_PGM_DSN 出力
                    追加DSN = 分割文字列2[i].replace("IN(", "").replace(")", "").replace("\'", "").replace("\"", "").rstrip("\+\-")
                    if 応用_顧客別_JCL_PGM_DSN_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                    else:
                        JCL_PGM_DSN_追加_CNT = JCL_PGM_DSN_追加_CNT + 1
                
                if "OUT(" in 分割文字列2[i]:
                    ### UTL_STEP別_IO情報 出力
                    判定DD = "FTP_" + 転送継続 + "_OUT"
                    IO判定 = "OUTPUT"
                    if 応用_UTL_STEP別_IO情報_.insert() == False:
                       ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                    else:
                       UTL_STEP別_IO情報_追加_CNT = UTL_STEP別_IO情報_追加_CNT + 1
                    
                    ### 顧客別_JCL_PGM_DSN 出力
                    追加DSN = 分割文字列2[i].replace("OUT(", "").replace(")", "").replace("\'", "").replace("\"", "").rstrip("\+\-")
                    if 応用_顧客別_JCL_PGM_DSN_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                    else:
                        JCL_PGM_DSN_追加_CNT = JCL_PGM_DSN_追加_CNT + 1
                
                ActSheet_x[14] = JCL_PGM_DSN_追加_CNT
                ActSheet_x[16] = UTL_STEP別_IO情報_追加_CNT
                ActSheet_x[17] = ActSheet_x[17] + vbCrLf + 追加DSN
                
    return ActSheet_x

def JCL_STEP_SYSIN解析_特殊UTL判定ロジック(ActSheet_x,data):
    #global REPRO_OUTDATASET_利用DD取得_,応用_顧客別_JCL_STEP_SYSIN_,応用_顧客別_資産関連性情報_,応用_顧客別_JCL_PGM_DSN_,応用_UTL_STEP別_IO情報_
    global REPRO_OUTDATASET_利用DD取得_,応用_顧客別_JCL_STEP_SYSIN_,応用_顧客別_JCL_PGM_DSN_,応用_UTL_STEP別_IO情報_
    ###○UTL対応
    ### === IDCAMS ===
    global SYSIN
    global LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME,PROC_NAME,SYSIN_PGM,SYSIN_SEQ,PARM_EXEC,PARM_PROC
    global DELETE継続,DUMP継続,RESTORE継続,FTP継続,DEFCL継続,DEFPATH継続,DEFAIX継続,DEFNVSAM継続,DEFUCAT継続,COPY継続,LOAD継続,UNLOAD継続,UTACH継続
    global DD_CNT,判定DD,IO判定,追加DSN,判定PGM,RESTOREモード,判定DD_OUT_SV,呼出方法,分割文字列,分割文字列2,UTL_STEP別_IO情報_追加_CNT,JCL_PGM_DSN_追加_CNT
    global 要素数,動的要素
    global JCL_NAME_SV,JOB_SEQ_SV,STEP_SEQ_SV,vbCrLf
#'20240215 ADD qian.e.wang
    global ADARUN3V継続,JYAADP継続,ADM継続
    # DEBUG
    # print("■ JCL_NAME :["+str(JCL_NAME)+"] PGM_NAME :["+str(PGM_NAME)+"]  SYSIN :["+str(SYSIN)+"]\r\n")
#'ADD END
    
    
    if PGM_NAME == "IDCAMS":                     ###SAM,VSAM,カタログ操作
        if "REPRO " in SYSIN:
            ActSheet_x[12] = "REPRO"
            for i in range(len(分割文字列)):
                if "INFILE" in 分割文字列[i]:
                    判定DD = 分割文字列[i].replace("INFILE", "").replace("(", "").replace(")", "")
                    IO判定 = "INPUT"
 
                    ### UTL_STEP別_IO情報 出力
                    if 応用_UTL_STEP別_IO情報_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                    else:
                        UTL_STEP別_IO情報_追加_CNT = UTL_STEP別_IO情報_追加_CNT + 1
 
                elif "OUTFILE" in 分割文字列[i]:
                    判定DD = 分割文字列[i].replace("OUTFILE", "").replace("(", "").replace(")", "")
                    IO判定 = "OUTPUT"
 
                  ###UTL_STEP別_IO情報 出力
                    if 応用_UTL_STEP別_IO情報_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                    else:
                        UTL_STEP別_IO情報_追加_CNT = UTL_STEP別_IO情報_追加_CNT + 1
                  
                elif "OUTDATASET" in 分割文字列[i]:
                    追加DSN = 分割文字列[i].replace("OUTDATASET(", "").replace(")", "")
                    ActSheet_x[17] = 追加DSN
                    判定DD = REPRO_OUTDATASET_利用DD取得_.get()
                    IO判定 = "OUTPUT"
                    if 判定DD != "":
                    
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "OUTDATASET 既存DD: " + 判定DD
                       ###UTL_STEP別_IO情報 出力
                        if 応用_UTL_STEP別_IO情報_.update() == False:
                            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                        else:
                            UTL_STEP別_IO情報_追加_CNT = UTL_STEP別_IO情報_追加_CNT + 1
                    
                    else:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "OUTDATASET 既存DD無し⇒追加"
                        DD_CNT = DD_CNT + 1
                        判定DD = "_SYSD" + str(DD_CNT).zfill(3)
                        ###UTL_STEP別_IO情報 出力
                        if 応用_UTL_STEP別_IO情報_.insert() == False:
                            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                        else:
                            UTL_STEP別_IO情報_追加_CNT = UTL_STEP別_IO情報_追加_CNT + 1
                       
                        ###顧客別_JCL_PGM_DSN 出力
                        if 応用_顧客別_JCL_PGM_DSN_.insert() == False:
                            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                            ActSheet_x[14] = 0
                        else:
                            ActSheet_x[14] = 1
                  
            ActSheet_x[16] = UTL_STEP別_IO情報_追加_CNT
            if UTL_STEP別_IO情報_追加_CNT != 2:
                ActSheet_x[12] = ActSheet_x[12] + " 要確認"
           
        elif "DELETE " in SYSIN or "DEL " in SYSIN:
            ActSheet_x[12] = "DELETE"
        #    'for i in range(len(分割文字列)
        #    '    if InStr(分割文字列[i], "DELETE" in SYSIN Or InStr(分割文字列[i], "DEL" in SYSIN:
                  
                #   '判定DD = "_SYSD001"
            DD_CNT = DD_CNT + 1
            判定DD = "_SYSD" + str(DD_CNT).zfill(3)
            IO判定 = "DELETE"
            追加DSN = SYSIN[:72].replace("  CLUSTER", "")
            追加DSN = 追加DSN.replace("DELETE ", "").replace("DEL ", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
            判定PGM = PGM_NAME
                  
                      
          ###UTL_STEP別_IO情報 出力
            if 応用_UTL_STEP別_IO情報_.insert() == False:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                ActSheet_x[16] = 0
            else:
                ActSheet_x[16] = 1
            ActSheet_x[17] = 追加DSN
                   
            判定PGM = ""    ### '
                   
        #    顧客別_JCL_PGM_DSN 出力
            if 応用_顧客別_JCL_PGM_DSN_.insert() == False:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                ActSheet_x[14] = 0
            else:
                ActSheet_x[14] = 1
                      
           ###DD_CNT = 1
            DD_CNT = DD_CNT + 1
            DELETE継続 = True

           
        elif "DEFINE " in SYSIN or "DEF " in SYSIN:
            ActSheet_x[12] = "DEF-CL"
           
           ###判定DD = "_SYSD001"
            DD_CNT = DD_CNT + 1
            判定DD = "_SYSD" + str(DD_CNT).zfill(3)
           
            IO判定 = "OUTPUT"
          
            ###UTL_STEP別_IO情報 出力
            if 応用_UTL_STEP別_IO情報_.insert() == False:
                if 応用_UTL_STEP別_IO情報_.update() == False:
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                    ActSheet_x[16] = 0
                else:
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "STEP-IO更新(OUTPUT)"
                    ActSheet_x[16] = 1
            else:
                ActSheet_x[16] = 1
           
            if "NAME" in SYSIN:     ###1行で完結するかどうか
                  
                for i in range(len(分割文字列)):
                    if "NAME" in 分割文字列[i]:
                        追加DSN = 分割文字列[i].replace("CLUSTER", "").replace("CL(", "").replace("NAME", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
           
                ###顧客別_JCL_PGM_DSN 出力    '注：ブレイク後なので1行前に出力する（仮）
                if 応用_顧客別_JCL_PGM_DSN_.insert() == False:
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                    ActSheet_x[14] = 0
                else:
                    ActSheet_x[14] = 1
                ActSheet_x[17] = 追加DSN     ###CHKのために追加 2020/1/10
           
            else:
                DEFCL継続 = True

    elif PGM_NAME == "KQCAMS":
        if "BLDINDEX " in SYSIN or "BIX " in SYSIN:
            # '=============================================================
            # 'コマンド : BLDINDEX'
            # '=============================================================
            ActSheet_x[12] = "BIX"
            for i in range(len(分割文字列)):
                
                if 分割文字列[i] == "":
                    pass
                    ###空文字はスルー
                    
                elif "INFILE" in 分割文字列[i] or "IFILE" in 分割文字列[i]:
                        # '---------------------------------
                        # 'Operand : INFILE
                        # '---------------------------------
                    判定DD = 分割文字列[i].replace("INFILE", "").replace("IFILE", "").replace("(", "").replace(")", "")
                    IO判定 = "INPUT"
                    # 'UTL_STEP別_IO情報 出力
                    if 応用_UTL_STEP別_IO情報_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                    else:
                        UTL_STEP別_IO情報_追加_CNT = UTL_STEP別_IO情報_追加_CNT + 1
                        
                elif "OUTFILE" in 分割文字列[i] or "OFILE" in 分割文字列[i]:
                        # '---------------------------------
                        # 'Operand : OUTFILE
                        # '---------------------------------
                    判定DD = 分割文字列[i].replace("OUTFILE", "").replace("OFILE", "").replace("(", "").replace(")", "")
                    IO判定 = "OUTPUT"
                    # 'UTL_STEP別_IO情報 出力
                    if 応用_UTL_STEP別_IO情報_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                    else:
                        UTL_STEP別_IO情報_追加_CNT = UTL_STEP別_IO情報_追加_CNT + 1
                        
                elif "INDATASET" in 分割文字列[i] or "IDS" in 分割文字列[i]:
                    # '---------------------------------
                    # 'Operand : INDATASET
                    # '---------------------------------
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + " KQCAMS/BULDINDEX/INDATASET使用 : ツール改修が必要"
                elif "OUTDATASET" in 分割文字列[i] or "ODS" in 分割文字列[i]:
                    # '---------------------------------
                    # 'Operand : OUTDATASET
                    # '---------------------------------
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + " KQCAMS/BULDINDEX/OUTDATASET使用 : ツール改修が必要"
           
            ActSheet_x[16] = UTL_STEP別_IO情報_追加_CNT
            if UTL_STEP別_IO情報_追加_CNT != 2:
                ###IN/OUTで2件追加されるはず
                ActSheet_x[12] = ActSheet_x[12] + " 要確認"
                
        elif "REPRO " in SYSIN:
            ActSheet_x[12] = "REPRO"
            for i in range(len(分割文字列)):
                if "INFILE" in 分割文字列[i]:
                    判定DD = 分割文字列[i].replace("INFILE", "").replace("(", "").replace(")", "")
                    IO判定 = "INPUT"
 
                  ###UTL_STEP別_IO情報 出力
                    if 応用_UTL_STEP別_IO情報_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                    else:
                        UTL_STEP別_IO情報_追加_CNT = UTL_STEP別_IO情報_追加_CNT + 1
 
                elif "OUTFILE" in 分割文字列[i]:
                    判定DD = 分割文字列[i].replace("OUTFILE", "").replace("(", "").replace(")", "")
                    IO判定 = "OUTPUT"
 
                  ###UTL_STEP別_IO情報 出力
                    if 応用_UTL_STEP別_IO情報_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                    else:
                        UTL_STEP別_IO情報_追加_CNT = UTL_STEP別_IO情報_追加_CNT + 1
                  
                elif "OUTDATASET" in 分割文字列[i]:
                    追加DSN = 分割文字列[i].replace("OUTDATASET(", "").replace(")", "")
                    ActSheet_x[17] = 追加DSN
                    判定DD = REPRO_OUTDATASET_利用DD取得_.get()
                    IO判定 = "OUTPUT"
                    if 判定DD != "":
                    
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "OUTDATASET 既存DD: " + 判定DD
                        ####UTL_STEP別_IO情報 出力
                        if 応用_UTL_STEP別_IO情報_.update() == False:
                            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                        else:
                            UTL_STEP別_IO情報_追加_CNT = UTL_STEP別_IO情報_追加_CNT + 1
                    
                    else:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "OUTDATASET 既存DD無し⇒追加"
                        DD_CNT = DD_CNT + 1
                        判定DD = "_SYSD" + str(DD_CNT).zfill(3)
                        ###UTL_STEP別_IO情報 出力
                        if 応用_UTL_STEP別_IO情報_.insert() == False:
                            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                        else:
                            UTL_STEP別_IO情報_追加_CNT = UTL_STEP別_IO情報_追加_CNT + 1
                       
                        ###顧客別_JCL_PGM_DSN 出力
                        if 応用_顧客別_JCL_PGM_DSN_.insert() == False:
                            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                            ActSheet_x[14] = 0
                        else:
                            ActSheet_x[14] = 1
                  
            ActSheet_x[16] = UTL_STEP別_IO情報_追加_CNT
            if UTL_STEP別_IO情報_追加_CNT != 2:
                ActSheet_x[12] = ActSheet_x[12] + " 要確認"
           
        elif "DELETE " in SYSIN or "DEL " in SYSIN:
            # '=============================================================
            # 'コマンド : DELETE / DEL'
            # '=============================================================
            ActSheet_x[12] = "DELETE"
            DD_CNT = DD_CNT + 1
            判定DD = "_SYSD" + str(DD_CNT).zfill(3)
            IO判定 = "DELETE"
            追加DSN = SYSIN[:72].replace("  CLUSTER", "")
            追加DSN = 追加DSN.replace("DELETE ", "").replace("DEL ", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
            判定PGM = PGM_NAME
        #   UTL_STEP別_IO情報 出力
            if 応用_UTL_STEP別_IO情報_.insert() == False:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                ActSheet_x[16] = 0
            else:
                ActSheet_x[16] = 1
            ActSheet_x[17] = 追加DSN
                   
            判定PGM = ""     ###'
            ###顧客別_JCL_PGM_DSN 出力
            if 応用_顧客別_JCL_PGM_DSN_.insert() == False:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                ActSheet_x[14] = 0
            else:
                ActSheet_x[14] = 1
                      
            DD_CNT = DD_CNT + 1
            DELETE継続 = True
        elif "EXPORT " in SYSIN:
            # '=============================================================
            # 'コマンド : EXPORT'
            # '=============================================================
            # '現状は継続行判定は不要なので、未対応
            ActSheet_x[12] = "EXPORT"
            for i in range(len(分割文字列)):
                
                if "OUTFILE" in 分割文字列[i] or  "OFILE" in 分割文字列[i]:
                    # '---------------------------------
                    # 'Operand : OUTFILE
                    # '---------------------------------
                    判定DD = 分割文字列[i].replace("OUTFILE", "").replace("OFILE", "").replace("(", "").replace(")", "")
                    IO判定 = "OUTPUT"
                    if 応用_UTL_STEP別_IO情報_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                    else:
                        UTL_STEP別_IO情報_追加_CNT = UTL_STEP別_IO情報_追加_CNT + 1
                elif "INFILE" in 分割文字列[i] or "IFILE" in 分割文字列[i]:
                    # '---------------------------------
                    # 'Operand : INFILE
                    # '---------------------------------
                    判定DD = 分割文字列[i].replace("INFILE", "").replace("IFILE", "").replace("(", "").replace(")", "")
                    IO判定 = "INPUT"
                    if 応用_UTL_STEP別_IO情報_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                    else:
                        UTL_STEP別_IO情報_追加_CNT = UTL_STEP別_IO情報_追加_CNT + 1
                elif "INDATASET" in 分割文字列[i]:
                    # '---------------------------------
                    # 'Operand : INDATASET
                    # '---------------------------------
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + " KQCAMS/EXPORT/INDATASET使用 : ツール改修が必要"
                elif "OUTDATASET" in 分割文字列[i]:
                    # '---------------------------------
                    # 'Operand : OUTDATASET
                    # '---------------------------------
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + " KQCAMS/EXPORT/OUTDATASET使用 : ツール改修が必要"
                    
            ActSheet_x[16] = UTL_STEP別_IO情報_追加_CNT
            if UTL_STEP別_IO情報_追加_CNT != 2 and UTL_STEP別_IO情報_追加_CNT != 0:
                ActSheet_x[12] = ActSheet_x[12] + " 要確認"
                
        elif "IMPORT " in SYSIN:
            # '=============================================================
            # 'コマンド : IMPORT'
            # '=============================================================
            ActSheet_x[12] = "IMPORT"
            for i in range(len(分割文字列)):
                
                if "OUTFILE" in 分割文字列[i] or  "OFILE" in 分割文字列[i]:
                    # '---------------------------------
                    # 'Operand : OUTFILE
                    # '---------------------------------
                    判定DD = 分割文字列[i].replace("OUTFILE", "").replace("OFILE", "").replace("(", "").replace(")", "")
                    IO判定 = "OUTPUT"
                    if 応用_UTL_STEP別_IO情報_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                    else:
                        UTL_STEP別_IO情報_追加_CNT = UTL_STEP別_IO情報_追加_CNT + 1
                elif "INFILE" in 分割文字列[i] or "IFILE" in 分割文字列[i]:
                    # '---------------------------------
                    # 'Operand : INFILE
                    # '---------------------------------
                    判定DD = 分割文字列[i].replace("INFILE", "").replace("IFILE", "").replace("(", "").replace(")", "")
                    IO判定 = "INPUT"
                    if 応用_UTL_STEP別_IO情報_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                    else:
                        UTL_STEP別_IO情報_追加_CNT = UTL_STEP別_IO情報_追加_CNT + 1
                elif "INDATASET" in 分割文字列[i]:
                    # '---------------------------------
                    # 'Operand : INDATASET
                    # '---------------------------------
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + " KQCAMS/IMPORT/INDATASET使用 : ツール改修が必要"
                elif "OUTDATASET" in 分割文字列[i]:
                    # '---------------------------------
                    # 'Operand : OUTDATASET
                    # '---------------------------------
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + " KQCAMS/IMPORT/OUTDATASET使用 : ツール改修が必要"
            ActSheet_x[16] = UTL_STEP別_IO情報_追加_CNT
            # import元とimport先で2件更新されるはず
            if UTL_STEP別_IO情報_追加_CNT != 2:
                ActSheet_x[12] = ActSheet_x[12] + " 要確認"
                
        elif "LISTCAT " in SYSIN:
            # '=============================================================
            # 'コマンド : LISTCAT'
            # '=============================================================
            ActSheet_x[12] = "LISTCAT"
            判定DD = "SYSPRINT"
            IO判定 = "OUTPUT"
            for i in range(len(分割文字列)):
                if "OUTFILE" in 分割文字列[i] or "OFILE" in 分割文字列[i]:
                    判定DD = 分割文字列[i].replace("OUTFILE", "").replace("OFILE", "").replace("(", "").replace(")", "")
                    
            #UTL_STEP別_IO情報 出力
            if 応用_UTL_STEP別_IO情報_.insert() == False:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
            else:
                UTL_STEP別_IO情報_追加_CNT = UTL_STEP別_IO情報_追加_CNT + 1
            ActSheet_x[16] = UTL_STEP別_IO情報_追加_CNT
            if UTL_STEP別_IO情報_追加_CNT != 1:
                ActSheet_x[12] = ActSheet_x[12] + " 要確認"
        elif "DEFINE " in SYSIN or "DEF " in SYSIN:
            # '=============================================================
            # 'コマンド : DEFINE'
            # '=============================================================
            
            if " NOVSAM" in SYSIN or "NVSAM" in SYSIN:
                ###====コマンド : DEFINE NOVSAM ===='
                ActSheet_x[12] = "DEF-NVSAM"
                DD_CNT = DD_CNT + 1
                判定DD = "_SYSD" + str(DD_CNT).zfill(3)
                IO判定 = "OUTPUT"
                ###UTL_STEP別_IO情報 出力
                if 応用_UTL_STEP別_IO情報_.insert():
                    ActSheet_x[16] = 1
                else:
                    if 応用_UTL_STEP別_IO情報_.update():
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "STEP-IO更新(OUTPUT)"
                        ActSheet_x[16] = 1
                    else:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                        ActSheet_x[16] = 0
                
                if "NAME" in SYSIN:     ###1行で完結するかどうか
                    for i in range(len(分割文字列)):
                        if "NAME" in 分割文字列[i]:
                            追加DSN = 分割文字列[i].replace("NONVSAM", "").replace("NVSAM", "").replace("NAME", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
                    ###顧客別_JCL_PGM_DSN 出力    '注：ブレイク後なので1行前に出力する（仮）
                    if 応用_顧客別_JCL_PGM_DSN_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                        ActSheet_x[14] = 0
                    else:
                        ActSheet_x[14] = 1
                    ActSheet_x[17] = 追加DSN
                else:
                    DEFNVSAM継続 = True  ###判定条件は同じなので流用する
            elif " PATH" in SYSIN:
                ###====コマンド : DEFINE PATH ===='
                ActSheet_x[12] = "DEF-PATH"
                DD_CNT = DD_CNT + 1
                判定DD = "_SYSD" + str(DD_CNT).zfill(3)
                IO判定 = "OUTPUT"
                ###UTL_STEP別_IO情報 出力
                if 応用_UTL_STEP別_IO情報_.insert():
                    ActSheet_x[16] = 1
                else:
                    if 応用_UTL_STEP別_IO情報_.update():
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "STEP-IO更新(OUTPUT)"
                        ActSheet_x[16] = 1
                    else:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                        ActSheet_x[16] = 0
                    
                if "NAME" in SYSIN:     ###1行で完結するかどうか
                    for i in range(len(分割文字列)):
                        if "NAME" in 分割文字列[i]:
                            追加DSN = 分割文字列[i].replace("PATH", "").replace("NAME", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
                    ###顧客別_JCL_PGM_DSN 出力    '注：ブレイク後なので1行前に出力する（仮）
                    if 応用_顧客別_JCL_PGM_DSN_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                        ActSheet_x[14] = 0
                    else:
                        ActSheet_x[14] = 1
                    ActSheet_x[17] = 追加DSN
                else:
                    DEFPATH継続 = True  ###判定条件は同じなので流用する
            elif " SPACE" in SYSIN or " SPC" in SYSIN:
                ###====コマンド : DEFINE SPACE ===='
                ActSheet_x[12] = "DEF-SPC"
                ###DEFINE SPACEはアクセス装置上にスペースを確保する処理なので、入出力情報に特に関係はない
                
            elif " USERCATALOG" in SYSIN or " UCAT" in SYSIN:
                ###====コマンド : DEFINE USERCATALOG / DEF UCAT ===='
                ActSheet_x[12] = "DEF-UCAT"
                DD_CNT = DD_CNT + 1
                判定DD = "_SYSD" + str(DD_CNT).zfill(3)
                IO判定 = "OUTPUT"
                ###UTL_STEP別_IO情報 出力
                if 応用_UTL_STEP別_IO情報_.insert():
                    ActSheet_x[16] = 1
                else:
                    if 応用_UTL_STEP別_IO情報_.update():
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "STEP-IO更新(OUTPUT)"
                        ActSheet_x[16] = 1
                    else:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                        ActSheet_x[16] = 0
                    
                if "NAME" in SYSIN:     ###1行で完結するかどうか
                    for i in range(len(分割文字列)):
                        if "NAME" in 分割文字列[i]:
                            追加DSN = 分割文字列[i].replace("USERCATALOG", "").replace("UCAT", "").replace("NAME", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
        
                    ###顧客別_JCL_PGM_DSN 出力    '注：ブレイク後なので1行前に出力する（仮）
                    if 応用_顧客別_JCL_PGM_DSN_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                        ActSheet_x[14] = 0
                    else:
                        ActSheet_x[14] = 1
                    ActSheet_x[17] = 追加DSN
                else:
                    DEFUCAT継続 = True
            elif " AIX" in SYSIN or "ALTERNATEINDEX" in SYSIN:
                ###====コマンド : DEFINE AIX / DEFINE ALTERNATEINDEX===='
                ActSheet_x[12] = "DEF-AIX"
                DD_CNT = DD_CNT + 1
                判定DD = "_SYSD" + str(DD_CNT).zfill(3)
                IO判定 = "OUTPUT"
                ###UTL_STEP別_IO情報 出力
                if 応用_UTL_STEP別_IO情報_.insert():
                    ActSheet_x[16] = 1
                else:
                    if 応用_UTL_STEP別_IO情報_.update():
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "STEP-IO更新(OUTPUT)"
                        ActSheet_x[16] = 1
                    else:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                        ActSheet_x[16] = 0
                    
                if "NAME" in SYSIN:     ###1行で完結するかどうか
                    for i in range(len(分割文字列)):
                        if "NAME" in 分割文字列[i]:
                            追加DSN = 分割文字列[i].replace("ALTERNATEINDEX", "").replace("AIX", "").replace("NAME", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
        
                    ###顧客別_JCL_PGM_DSN 出力    '注：ブレイク後なので1行前に出力する（仮）
                    if 応用_顧客別_JCL_PGM_DSN_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                        ActSheet_x[14] = 0
                    else:
                        ActSheet_x[14] = 1
                    ActSheet_x[17] = 追加DSN
                else:
                    DEFAIX継続 = True
            elif " CLUSTER" in SYSIN or " CL" in SYSIN:
                ###====コマンド : DEFINE CLUSTER / DEF CL ===='
                ActSheet_x[12] = "DEF-CL"
                DD_CNT = DD_CNT + 1
                判定DD = "_SYSD" + str(DD_CNT).zfill(3)
                IO判定 = "OUTPUT"
                ###UTL_STEP別_IO情報 出力
                if 応用_UTL_STEP別_IO情報_.insert():
                    ActSheet_x[16] = 1
                else:
                    if 応用_UTL_STEP別_IO情報_.update():
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "STEP-IO更新(OUTPUT)"
                        ActSheet_x[16] = 1
                    else:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                        ActSheet_x[16] = 0
                    
                if "NAME" in SYSIN:     ###1行で完結するかどうか
                    for i in range(len(分割文字列)):
                        if "NAME" in 分割文字列[i]:
                            追加DSN = 分割文字列[i].replace("CLUSTER", "").replace("CL", "").replace("NAME", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
        
                    ###顧客別_JCL_PGM_DSN 出力    '注：ブレイク後なので1行前に出力する（仮）
                    if 応用_顧客別_JCL_PGM_DSN_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                        ActSheet_x[14] = 0
                    else:
                        ActSheet_x[14] = 1
                    ActSheet_x[17] = 追加DSN
                else:
                    DEFCL継続 = True
            else:
                ###未対応DEFINE文
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "未対応DEFINE文"
                
        elif "VERIFY " in SYSIN:
            # '=============================================================
            # 'コマンド : VERIFY'
            # '=============================================================
            # '他のコマンドにもVERIFYオペランドがあるため、最後に判定する。
            # 'VERIFYは入出力をするコマンドでないためスルー
            ActSheet_x[12] = "VERIFY"
    # '=== IEBGENER ===
    elif PGM_NAME == "IEBGENER":             ###  'データコピー
        if "COPY " in SYSIN:
            ActSheet_x[12] = "COPY"
        elif "FIELD" in SYSIN:
              ###※スペース入れるか？
            ActSheet_x[12] = "レコード長変化?"
        
        ###いまのところ処理しない。DD名はSYSUT1,SYSUT2で固定
    
    ###=== SORT ===
    elif PGM_NAME == "SORT":             ###      'ソート
        if "OUTREC" in SYSIN:
            ActSheet_x[12] = "レコード長変化?"
        elif "FNAMES=" in SYSIN:
            for i in range(len(分割文字列)):
                if "FNAMES=" in 分割文字列[i]:
                    判定DD = 分割文字列[i].replace("FNAMES=", "")
           
           ###UTL_STEP別_IO情報 出力
            IO判定 = "OUTPUT"
           
            if 応用_UTL_STEP別_IO情報_.insert() == False:
                ActSheet_x[12] = ActSheet_x[11] + vbCrLf + "KEY重複の為処理SKIP" #### 間違い? 後で確認する
            else:
                ActSheet_x[16] = 1
           
        
    ###=== DSNUTILB ===
    elif PGM_NAME == "DSNUTILB":               ###DB2 Utility データロード
        pass
        ###DSNUPROC内で利用　下のコードで対応済
    elif PGM_NAME == "KBKARCS":
        if "COPY " in SYSIN:
            # '====================
            # 'COPY
            # '====================
            ActSheet_x[12] = "COPY"
            # 'ADRDSSU同様に手動対応
        elif "MIGRATE " in SYSIN:
            ActSheet_x[12] = "MIGRATE"
        elif "RESTORE " in SYSIN:
            # '====================
            # 'RESTORE
            # '====================
            ActSheet_x[12] = "RESTORE"
            RESTOREモード = ""
            
            for i in range(len(分割文字列)):
                if "FROM(DD(" in 分割文字列[i]:
                    判定DD = 分割文字列[i].replace("FROM(DD(", "").replace("))", "")
                    IO判定 = "BK-INPUT"
                    
                    ###UTL_STEP別_IO情報_出力
                    if 応用_UTL_STEP別_IO情報_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                    else:
                        UTL_STEP別_IO情報_追加_CNT = UTL_STEP別_IO情報_追加_CNT + 1
                elif "TO(DD(" in 分割文字列[i]:
                    判定DD = 分割文字列[i].replace("TO(DD(", "").replace("))", "")
                    IO判定 = "OUTPUT"
                    
                    ###UTL_STEP別_IO情報 出力
                    if 応用_UTL_STEP別_IO情報_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                    else:
                        UTL_STEP別_IO情報_追加_CNT = UTL_STEP別_IO情報_追加_CNT + 1
                    ###JCL_PGM_DSNは継続処理判定のところで実施
            
            ActSheet_x[14] = JCL_PGM_DSN_追加_CNT
            ActSheet_x[16] = UTL_STEP別_IO情報_追加_CNT
            
            if UTL_STEP別_IO情報_追加_CNT != 2:
                ActSheet_x[12] = ActSheet_x[12] + " 要確認"
            
            ###リストアDSNの解析
            要素数 = 0
            動的要素 = [""] ###配列要素数は最低値1とする。
            
            ###念のため(1行目にDSNが定義されるかもしれない。
            if "DATASET(" in SYSIN:
                RESTOREモード = "DATASET"
                for i in range(len(分割文字列2)):
                    if "DATASET(" in 分割文字列2[i]:
                        追加DSN = 分割文字列2[i].replace("DATASET(", "").replace(")", "")
                動的要素[0] = 追加DSN
                要素数 += 1
                ActSheet_x[17] = 追加DSN
            
            RESTORE継続 = True
            追加DSN = ""
            JCL_NAME_SV = JCL_NAME ###ブレイク後に利用するので退避する。
            JOB_SEQ_SV = JOB_SEQ
            STEP_SEQ_SV = STEP_SEQ
    ###=== ADRDSSU ===
    elif PGM_NAME == "ADRDSSU":                ###'データバックアップ
        if "COPY " in SYSIN:
            ActSheet_x[12] = "COPY"
           
           ###当面は手動対応
           
        elif "DUMP " in SYSIN:
            ActSheet_x[12] = "DUMP"
            
            追加DSN = SYSIN.replace(" ", "").replace("-", "").replace("DUMP", "").replace("OUTDD", "").replace("(", "").replace(")", "")
            #    '判定DD = "_SYSD001"
            判定DD = "BACKUP"
            IO判定 = "BK-OUTPUT"
           
            ###UTL_STEP別_IO情報 出力
            if 応用_UTL_STEP別_IO情報_.insert() == False:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
            else:
                ActSheet_x[16] = 1
           
            ###DD_CNT = 1
            DD_CNT = DD_CNT + 1
            ###判定DD = "_SYSD" + str(DD_CNT).zfill(3)
            DUMP継続 = True
           
        elif "RESTORE " in SYSIN:
            ActSheet_x[12] = "RESTORE"
            RESTOREモード = ""
                    
            for i in range(len(分割文字列)):
                if "INDD" in 分割文字列[i]:
                    判定DD = 分割文字列[i].replace("INDD", "").replace("(", "").replace(")", "")
                    IO判定 = "BK-INPUT"
                    
                    ###UTL_STEP別_IO情報 出力
                    if 応用_UTL_STEP別_IO情報_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                    else:
                        UTL_STEP別_IO情報_追加_CNT = UTL_STEP別_IO情報_追加_CNT + 1
                    
                elif "IDD" in 分割文字列[i]:
                    判定DD = 分割文字列[i].replace("IDD", "").replace("(", "").replace(")", "")
                    IO判定 = "BK-INPUT"
                    
                    ###UTL_STEP別_IO情報 出力
                    if 応用_UTL_STEP別_IO情報_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                    else:
                        UTL_STEP別_IO情報_追加_CNT = UTL_STEP別_IO情報_追加_CNT + 1
                
                elif "OUTDD" in 分割文字列[i]:
                    判定DD = 分割文字列[i].replace("OUTDD", "").replace("(", "").replace(")", "")
                    判定DD_OUT_SV = 判定DD
                    IO判定 = "OUTPUT"
                    
                    ###UTL_STEP別_IO情報 出力
                    if 応用_UTL_STEP別_IO情報_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                    else:
                        UTL_STEP別_IO情報_追加_CNT = UTL_STEP別_IO情報_追加_CNT + 1
                    
                    ###JCL_PGM_DSNは継続処理判定のところで実施
                    
                elif "ODD" in 分割文字列[i]:
                    判定DD = 分割文字列[i].replace("ODD", "").replace("(", "").replace(")", "")
                    判定DD_OUT_SV = 判定DD
                    IO判定 = "OUTPUT"
                    
                    ###UTL_STEP別_IO情報 出力
                    if 応用_UTL_STEP別_IO情報_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                    else:
                        UTL_STEP別_IO情報_追加_CNT = UTL_STEP別_IO情報_追加_CNT + 1
                    
                    ###JCL_PGM_DSNは継続処理判定のところで実施
                    
            
            ActSheet_x[14] = JCL_PGM_DSN_追加_CNT
            ActSheet_x[16] = UTL_STEP別_IO情報_追加_CNT
            
            if UTL_STEP別_IO情報_追加_CNT != 2:
                ActSheet_x[12] = ActSheet_x[12] + " 要確認"
        
            ###リストアDSNの解析
            
            要素数 = 0           ##初期値は0にする　発生時にカウントアップ
            動的要素 = [""]   ###配列要素数は最低値1とする
            
            ###念のため(1行目にDSNが定義されるかもしれない)
            if "DATASET(" in SYSIN:
                RESTOREモード = "DATASET"
                for i in range(len(分割文字列2)):
                    if 分割文字列2[i] == "DATASET(":
                        追加DSN = SYSIN.replace(" ", "").replace("-", "").replace("INCLUDE", "").replace("DATASET", "").replace("(", "").replace(")", "")
                動的要素[0] = 追加DSN
                ActSheet_x[17] = 追加DSN
            
            RESTORE継続 = True
            追加DSN = ""
            JCL_NAME_SV = JCL_NAME   ###ブレイク後に利用するので退避する
            JOB_SEQ_SV = JOB_SEQ
            STEP_SEQ_SV = STEP_SEQ
            
    elif PGM_NAME == "JQHGEM3":
        ###GEM3を呼び出すユーティリティー
        if " PUT " in SYSIN:
            ActSheet_x[12] = "JQHGEM3-PUT"
            IO判定 = "OUTPUT"
            for i in range(len(分割文字列)):
                if "OUT=" in 分割文字列[i] or "OUT(" in 分割文字列[i]:
                    OUT_PARAMETER = 分割文字列[i].replace("OUT=", "").replace("OUT(", "").replace(")", "")
                    if  "\'" in OUT_PARAMETER:
                        # 'DSN名の指定
                        # 'JFE倉敷案件には存在しないので現状は未対応　ログだけ出す。
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "JQHGEM3 PUTコマンド OUT='DSN' OUT('DSN')指定には未対応"
                    else:
                        # 'DD名の指定
                        判定DD = OUT_PARAMETER
                        # 'UTL_STEP別_IO情報_出力
                        if 応用_UTL_STEP別_IO情報_.insert() == False:
                            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                        else:
                            UTL_STEP別_IO情報_追加_CNT = UTL_STEP別_IO情報_追加_CNT + 1
            
            ActSheet_x[16] = UTL_STEP別_IO情報_追加_CNT
            if UTL_STEP別_IO情報_追加_CNT > 1:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "要確認"
    ###=== IKJEFT01 ===
    elif PGM_NAME == "IKJEFT01":               ###TSOプログラム実行
        if "RUN " in SYSIN:
            ActSheet_x[12] = "RUNPGM"
            for i in range(len(分割文字列)):
                if "PROGRAM(" in 分割文字列[i]:
            
                    呼出方法 = "IKJEFT01-RUN"
                    判定PGM = 分割文字列[i].replace("PROGRAM(", "").replace(")", "").replace("-", "").replace(" ", "")
                    
                    #if 応用_顧客別_資産関連性情報_.insert() == False:
                    #    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                    #else:
                    #    ActSheet_x[13] = 1
                    #    ActSheet_x[9] = 判定PGM
                    #    ActSheet_x[17] = 判定PGM
                    
                    ###関連性TABLEに出力する処理追加
                    
                    if 応用_顧客別_JCL_PGM_DSN_.update() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "更新情報無しの為処理SKIP"
                    else:
                        ActSheet_x[15] = 1
                        ActSheet_x[17] = 判定PGM
                    
                    ###顧客別_JCL_STEP_SYSINを更新する処理追加
                    
                    if 応用_顧客別_JCL_STEP_SYSIN_.update() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "更新情報無しの為処理SKIP"
                    else:
                        ActSheet_x[17] = 判定PGM
                        ActSheet_x[19] = 1
                    
    ###=== UTACH === 暫定対応
    elif PGM_NAME == "UTACH":               ###JFE倉敷　PGM起動UTL
    
        if "TA" in SYSIN and "PGM=" in SYSIN:
            ###SYSIN = Mid(SYSIN, 0, 72) 'とりあえず不要
            ActSheet_x[12] = "UTACH"
            for i in range(len(分割文字列)):
                if "PGM=" in 分割文字列[i]:
            
                    呼出方法 = "UTACH起動"
                    if UTACH継続:
                        判定PGM = 判定PGM + "," + 分割文字列[i].replace("PGM=", "")
                    else:
                        判定PGM = 分割文字列[i].replace("PGM=", "")
                    
                    #if 応用_顧客別_資産関連性情報_.insert() == False:
                    #    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                    #else:
                    #    ActSheet_x[13] = 1
                    #    ActSheet_x[9] = 判定PGM
                    #    ActSheet_x[17] = 判定PGM
                    
                    ###関連性TABLEに出力する処理追加
                    
                    if 応用_顧客別_JCL_PGM_DSN_.update() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "更新情報無しの為処理SKIP"
                    else:
                        ActSheet_x[15] = 1
                        ActSheet_x[17] = 判定PGM
                    
                    ###顧客別_JCL_STEP_SYSINを更新する処理追加
                    
                    if 応用_顧客別_JCL_STEP_SYSIN_.update() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "更新情報無しの為処理SKIP"
                    else:
                        ActSheet_x[17] = 判定PGM
                        ActSheet_x[19] = 1
                    
           
    
        UTACH継続 = True
    
#'20240215 ADD qian.e.wang
    ###=== ADM === 暫定対応
    elif PGM_NAME == "ADM":               ###日産ANPSS　PGM起動UTL
    
        if "ADMBMP" in SYSIN and "PGM=" in SYSIN:
            SYSIN = Mid(SYSIN, 0, 72)
            ActSheet_x[12] = "ADM"
            for i in range(len(分割文字列)):
                if "PGM=" in 分割文字列[i]:
            
                    呼出方法 = "ADM起動"
                    if ADM継続:
                        判定PGM = 判定PGM + "," + 分割文字列[i].replace("PGM=", "")
                    else:
                        判定PGM = 分割文字列[i].replace("PGM=", "")
                    
                    ActSheet_x[13] = 1
                    ActSheet_x[9] = 判定PGM
                    ActSheet_x[17] = 判定PGM
                    
                    ###関連性TABLEに出力する処理追加
                    
                    if 応用_顧客別_JCL_PGM_DSN_.update() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "更新情報無しの為処理SKIP"
                    else:
                        ActSheet_x[15] = 1
                        ActSheet_x[17] = 判定PGM
                    
                    ###顧客別_JCL_STEP_SYSINを更新する処理追加
                    
                    if 応用_顧客別_JCL_STEP_SYSIN_.update() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "更新情報無しの為処理SKIP"
                    else:
                        ActSheet_x[17] = 判定PGM
                        ActSheet_x[19] = 1
                    
        ADM継続 = False
    
    ###=== JYAADP === 暫定対応
    elif PGM_NAME == "JYAADP":               ###日産ANPSS　PGM起動UTL
    
        if "NAME" in SYSIN:
            SYSIN = Mid(SYSIN, 0, 72)
            ActSheet_x[12] = "JYAADP"

            for i in range(len(分割文字列2)):
                if "NAME" == 分割文字列2[i]:
                    continue
                else:
                    呼出方法 = "JYAADP起動"
                    if JYAADP継続:
                        判定PGM = 判定PGM + "," + 分割文字列2[i]
                    else:
                        判定PGM = 分割文字列2[i]
                    
                    ActSheet_x[13] = 1
                    ActSheet_x[9] = 判定PGM
                    ActSheet_x[17] = 判定PGM
                    
                    ###関連性TABLEに出力する処理追加
                    
                    if 応用_顧客別_JCL_PGM_DSN_.update() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "更新情報無しの為処理SKIP"
                    else:
                        ActSheet_x[15] = 1
                        ActSheet_x[17] = 判定PGM
                    
                    ###顧客別_JCL_STEP_SYSINを更新する処理追加
                    
                    if 応用_顧客別_JCL_STEP_SYSIN_.update() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "更新情報無しの為処理SKIP"
                    else:
                        ActSheet_x[17] = 判定PGM
                        ActSheet_x[19] = 1
                    
        JYAADP継続 = False
    
    ###=== ADARUN3V === 暫定対応
    elif PGM_NAME == "ADARUN3V":               ###日産ANPSS　PGM起動UTL
    
        if "ADARUN" in SYSIN and ("PROGRAM=" in SYSIN or "PROG=" in SYSIN):
            SYSIN = Mid(SYSIN, 0, 72)
            ActSheet_x[12] = "ADARUN3V"
            for i in range(len(分割文字列)):
                if "PROGRAM=" in 分割文字列[i] or "PROG=" in 分割文字列[i]:
            
                    呼出方法 = "ADARUN3V起動"
                    if ADARUN3V継続:
                        判定PGM = 判定PGM + "," + 分割文字列[i].replace("PROGRAM=", "").replace("PROG=", "")
                    else:
                        判定PGM = 分割文字列[i].replace("PROGRAM=", "").replace("PROG=", "")
                    
                    ActSheet_x[13] = 1
                    ActSheet_x[9] = 判定PGM
                    ActSheet_x[17] = 判定PGM
                    
                    ###関連性TABLEに出力する処理追加
                    
                    if 応用_顧客別_JCL_PGM_DSN_.update() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "更新情報無しの為処理SKIP"
                    else:
                        ActSheet_x[15] = 1
                        ActSheet_x[17] = 判定PGM
                    
                    ###顧客別_JCL_STEP_SYSINを更新する処理追加
                    
                    if 応用_顧客別_JCL_STEP_SYSIN_.update() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "更新情報無しの為処理SKIP"
                    else:
                        ActSheet_x[17] = 判定PGM
                        ActSheet_x[19] = 1
                    
        ADARUN3V継続 = False
#'ADD END
    
    ### === IEBPTPCH ===
    elif PGM_NAME == "IEBPTPCH":             ###  'ライブラリコピー
        pass
        ###対応保留、必要になったら対応予定

    # '=== FTP ===
    # 'elif PGM_NAME = "FTP":                    'FTPファイル送受信
        
    #     '対応保留、必要になったら対応予定
        
    # '=== XRSNDGO ===
    elif PGM_NAME == "XRSNDGO":               ### 'HULFT送信
        pass
    #     '対応保留、必要になったら対応予定
        
    # '=== IEBASE ===
    elif PGM_NAME == "IEBASE":                ### 'EXPEDITE通信
        pass
    #     '対応保留、必要になったら対応予定
        
    # '=== DFSRRC00 ===
    elif PGM_NAME == "DFSRRC00":              ### 'IMSDB関連UTL
    
        # 'IMSDBバックアップ（DFSUDMP0）
        # 'if "D1 " in SYSIN: '第1要素は"D1"を想定 ⇒誤検知ありのため変更
        if str(SYSIN).startswith("D1 "): ###第1要素は"D1"を想定
            分割文字列2 = ArrayEmptyDelete(SYSIN.split(" "))
            if 分割文字列2[0] == "D1":
                判定DD = 分割文字列2[2]
                IO判定 = "INPUT"
                  
                ###UTL_STEP別_IO情報 出力
                if 応用_UTL_STEP別_IO情報_.insert() == False:
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                else:
                    UTL_STEP別_IO情報_追加_CNT = UTL_STEP別_IO情報_追加_CNT + 1
                    
                判定DD = 分割文字列2[3]
                IO判定 = "BK-OUTPUT"
                  
                ###UTL_STEP別_IO情報 出力
                if 応用_UTL_STEP別_IO情報_.insert() == False:
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                else:
                    UTL_STEP別_IO情報_追加_CNT = UTL_STEP別_IO情報_追加_CNT + 1
                                    
            else:
                ActSheet_x[12] = ActSheet_x[12] + " 配列要素要確認"
    
    # '○PROC対応
    # '=== DSNUPROC ===
    elif PROC_NAME == "DSNUPROC":              ###'DBロード・アンロード
        if "UNLOAD " in SYSIN:
            ActSheet_x[12] = "UNLOAD"
           

           
        #    'UNLOAD元が1行目に記載がなければ継続対応にする
            if "FROM " in SYSIN and " TABLE " in SYSIN:
           
                for i in range(len(分割文字列2)):
                    if 分割文字列2[i] == "TABLE":
                      
                        DD_CNT = DD_CNT + 1
                        判定DD = "_SYSD" + str(DD_CNT).zfill(3)
                        ###判定DD = "_SYSD001"
                        IO判定 = "INPUT"
            
                        ###UTL_STEP別_IO情報 出力
                        if 応用_UTL_STEP別_IO情報_.insert() == False:
                            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                            ActSheet_x[16] = 0
                        else:
                            ActSheet_x[16] = 1
           
                        ###顧客別_JCL_PGM_DSN 出力
                        if i + 1 < len(分割文字列2):
                            追加DSN = 分割文字列2[i + 1]
                            追加DSN = 追加DSN.replace("JBDB2.", "")     ###MHI案件のみ暫定対応
                            if 応用_顧客別_JCL_PGM_DSN_.insert() == False:
                                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                                ActSheet_x[14] = 0
                            else:
                                ActSheet_x[14] = 1
                            ActSheet_x[17] = 追加DSN
                        else:
                            ActSheet_x[12] = ActSheet_x[12] + " 配列要素要確認"     ### 'UNLOAD元情報は1行内に記載がある想定
           
           
            else:
                UNLOAD継続 = True
           
        elif "LOAD " in SYSIN:
            ActSheet_x[12] = "LOAD"
                        
            for i in range(len(分割文字列2)):
                if  "INDDN(" in 分割文字列2[i]:
                    判定DD = 分割文字列2[i].replace("INDDN", "").replace("(", "").replace(")", "")
                    IO判定 = "INPUT"
            
                    ###UTL_STEP別_IO情報 出力
                    if 応用_UTL_STEP別_IO情報_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                        ActSheet_x[16] = 0
                    else:
                        ActSheet_x[16] = 1
            
            
            ###LOAD先が1行目に記載がなければ継続対応にする
            if "INTO " in SYSIN and " TABLE " in SYSIN:
            
                for i in range(len(分割文字列2)):
                    if 分割文字列2[i] == "TABLE":
                        DD_CNT = DD_CNT + 1
                        判定DD = "_SYSD" + str(DD_CNT).zfill(3)
                        ###判定DD = "_SYSD001"
                        IO判定 = "OUTPUT"
            
                        ###UTL_STEP別_IO情報 出力
                        if 応用_UTL_STEP別_IO情報_.insert() == False:
                            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                            ActSheet_x[16] = 0
                        else:
                            ActSheet_x[16] = 1
            
                        ###顧客別_JCL_PGM_DSN 出力
                        if i + 1 < len(分割文字列2):
                            追加DSN = 分割文字列2[i + 1]
                            追加DSN = 追加DSN.replace("JBDB2.", "")     ###MHI案件のみ暫定対応
                            if 応用_顧客別_JCL_PGM_DSN_.insert() == False:
                                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                                ActSheet_x[14] = 0
                            else:
                                ActSheet_x[14] = 1
                            ActSheet_x[17] = 追加DSN
                        else:
                            ActSheet_x[12] = ActSheet_x[12] + " 配列要素要確認"      ###LOAD先情報は1行内に記載がある想定
        
        
            else:
                LOAD継続 = True
           
        elif "COPY " in SYSIN and " TABLESPACE " in SYSIN:
            ActSheet_x[12] = "COPY"
                        
            if COPY継続:
                DD_CNT = DD_CNT + 1
                ActSheet_x[12] = "COPY継続"
            else:
                DD_CNT = DD_CNT + 1
                ###DD_CNT = 1
                COPY継続 = True
                ActSheet_x[12] = "COPY"
                        
            for i in range(len(分割文字列2)):
                if 分割文字列2[i] == "TABLESPACE":
                    判定DD = "_SYSD" + str(DD_CNT).zfill(3)
                    IO判定 = "BK-INPUT"
    
                    ###UTL_STEP別_IO情報 出力
                    if 応用_UTL_STEP別_IO情報_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                    else:
                        UTL_STEP別_IO情報_追加_CNT = UTL_STEP別_IO情報_追加_CNT + 1

                    ###顧客別_JCL_PGM_DSN 出力
                    if i + 1 < len(分割文字列2):
                        追加DSN = 分割文字列2[i + 1]
                        if 応用_顧客別_JCL_PGM_DSN_.insert() == False:
                            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                            ActSheet_x[14] = 0
                        else:
                            ActSheet_x[14] = 1
                        ActSheet_x[17] = 追加DSN
                    else:
                        ActSheet_x[12] = ActSheet_x[12] + " 配列要素要確認"
                
                elif "COPYDDN(" in 分割文字列2[i]:
                    判定DD = 分割文字列2[i].replace("COPYDDN", "").replace("(", "").replace(")", "")
                    IO判定 = "OUTPUT"
    
                    ###UTL_STEP別_IO情報 出力
                    if 応用_UTL_STEP別_IO情報_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                        #ActSheet_x[16] = 0
                    else:
                        #ActSheet_x[16] = 1
                        UTL_STEP別_IO情報_追加_CNT = UTL_STEP別_IO情報_追加_CNT + 1
                    
                    
            ActSheet_x[16] = UTL_STEP別_IO情報_追加_CNT
                   
        elif "MODIFY " in SYSIN and " RECOVERY " in SYSIN and " TABLESPACE " in SYSIN:
           ActSheet_x[12] = "MODIFY-RECOVERY"
           #当面は手動対応
        

    # '=== FTP （MSP）===   2021/12/16 ADD
    # 'JCLサンプル
    # 'FTP A('TISP.FTP.ATTR')
    # 'HOST 172.22.106.41
    # 'SEND IN('USR1.TESTDATA')
    # '     OUT('D:\TESTDATA.bin')
    # '     T(B)
    # '     SYN
    # '     CNVT(NO)
    # '     TYPE(TEXT)
    # '     V(SZIA22)
    # 'RECV IN('D:\Work\IEBGENER.txt')
    # '     OUT('USR1.JCL(IEBGENER)')
    # '     T(T)
    # '     C(Y)
    # '     SYN
    # 'END
    if "FTP " in SYSIN:
        # 'SYSIN = Mid(SYSIN, 0, 72) 'とりあえず不要
        ActSheet_x[12] = "FTP"
        
        ###  20220227 wangqian SYSIN_PGMの値残し問題対応
        判定PGM = "FTP"
        
        for i in range(len(分割文字列)):
            if "HOST" in 分割文字列[i]:
                if PROC_NAME == "":
                    呼出方法 = "FTP起動"
                else:
                    呼出方法 = PROC_NAME + "起動"
                #if 応用_顧客別_資産関連性情報_.insert() == False:
                #    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY重複の為処理SKIP"
                #else:
                #    ActSheet_x[13] = 1
                #    ActSheet_x[9] = 判定PGM
                #    ActSheet_x[17] = 判定PGM
                
        FTP継続 = True
        
    return ActSheet_x
       


def FLAG初期化():
    global JCL_NAME_SV,JOB_SEQ_SV,STEP_SEQ_SV,DELETE継続,DUMP継続,RESTORE継続,DEFCL継続,DEFPATH継続,DEFAIX継続,DEFNVSAM継続,DEFUCAT継続,FTP継続
    global 追加DSN,判定DD,判定PGM,IO判定,要素数,動的要素
    JCL_NAME_SV = ""
    JOB_SEQ_SV = 0
    STEP_SEQ_SV = 0
    DELETE継続 = False
    DUMP継続 = False
    RESTORE継続 = False
    FTP継続 = False
    DEFCL継続 = False
    # '20210312 Add Horiuchi
    DEFPATH継続 = False
    DEFAIX継続 = False
    DEFNVSAM継続 = False
    DEFUCAT継続 = False
    

    追加DSN = ""
    判定DD = ""
    判定PGM = ""
    IO判定 = ""
    要素数 = 0
    動的要素 = [""]



def analysis1_UTL_analysis(db_path,get_conn,get_cursor):
    
    global conn,cursor
    
 
    conn = get_conn
    cursor = get_cursor
   
    ### 顧客別_JCL_STEP_SYSIN　読み込み
    sql =   """\
            SELECT * FROM QRY_顧客別_JCL_STEP_SYSIN
            """
    
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)
    
    #global REPRO_OUTDATASET_利用DD取得_,応用_顧客別_JCL_STEP_SYSIN_,応用_顧客別_資産関連性情報_,応用_顧客別_JCL_PGM_DSN_,応用_UTL_STEP別_IO情報_
    global REPRO_OUTDATASET_利用DD取得_,応用_顧客別_JCL_STEP_SYSIN_,応用_顧客別_JCL_PGM_DSN_,応用_UTL_STEP別_IO情報_
    global ActSheet

    REPRO_OUTDATASET_利用DD取得_ = REPRO_OUTDATASET_利用DD取得(db_path)
    応用_顧客別_JCL_STEP_SYSIN_ = 応用_顧客別_JCL_STEP_SYSIN(db_path)
    #応用_顧客別_資産関連性情報_ = 応用_顧客別_資産関連性情報(db_path)
    応用_顧客別_JCL_PGM_DSN_ = 応用_顧客別_JCL_PGM_DSN(db_path)
    応用_UTL_STEP別_IO情報_ = 応用_UTL_STEP別_IO情報(db_path)
    JCL_NAME_BEFORE = ""
    
    global DELETE継続,DUMP継続,RESTORE継続,FTP継続
 
    ActSheet = []
    print(len(df),"analysis1_UTL_analysis")

    for i in range(len(df)):
        data = df.iloc[i]
        if data["JCL_NAME"] != JCL_NAME_BEFORE:
            if RESTORE継続:
                _ = RESTORE継続処理([],[])
                
            FLAG初期化()
                
            
                
        ActSheet_x = JCL_STEP_SYSIN解析_共通出力(data)
        ActSheet_x = 継続処理解除判定(ActSheet_x,data)
        if DELETE継続 == True:
            ###暫定
            ActSheet_x = DELETE継続処理(ActSheet_x,data)
        elif DUMP継続 == True:
            ###暫定
            ActSheet_x = DUMP継続処理(ActSheet_x,data)
        elif RESTORE継続 == True:
            ###暫定
            ActSheet_x = RESTORE継続処理(ActSheet_x,data)
        elif FTP継続 == True: ###2021/12/16 ADD
            ###暫定
            ActSheet_x = FTP継続処理(ActSheet_x,data)
        else:      
            ###=========================
            ### 特殊UTL対応
            ### =========================
    
            ###暫定
            ###if PGM_NAME = "IKJEFT01":
            ActSheet_x = JCL_STEP_SYSIN解析_特殊UTL判定ロジック(ActSheet_x,data)
 
        ActSheet.append(ActSheet_x)
        JCL_NAME_BEFORE = data["JCL_NAME"]
        
    
    ### 後処理
    if RESTORE継続 == True:
        ###暫定
        ActSheet_x = RESTORE継続処理([],[])
        
    応用_顧客別_JCL_PGM_DSN_.update_all()
    応用_顧客別_JCL_STEP_SYSIN_.update_all()
    応用_UTL_STEP別_IO情報_.update_all()
    print(len(ActSheet),"analysis1_UTL_analysis")
    
 
    return ActSheet,conn,cursor
