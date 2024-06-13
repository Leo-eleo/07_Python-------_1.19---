#!/usr/bin/env python
# -*- coding: cp932 -*-
import sys
import os

import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


DB自動登録時PARM = "自動設定(DAM解析)"
utilityId = ""

UTL_STEP別_IO情報_ = None

class UTL_STEP別_IO情報:
    
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "UTL_STEP別_IO情報"
        self.dbname2 = "顧客別_JCL_基本情報"
        self.jcl_info_dic = {}
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for jclName,jobSeq,stepSeq,ddName,io in zip(df["JCL_NAME"],df["JOB_SEQ"],df["STEP_SEQ"],df["DD名"],df["IO"]):
            if (jclName,jobSeq,stepSeq,ddName) in self.dic:
                self.dic[(jclName,jobSeq,stepSeq,ddName)].append(io)
            else:
                self.dic[(jclName,jobSeq,stepSeq,ddName)] = [io]

        
        sql = "SELECT * FROM "+self.dbname2
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for jclName,jobSeq,jclId in zip(df["JCL名"],df["JOB_SEQ"],df["JOB_ID"]):
            if (jclName,jobSeq) in self.jcl_info_dic:
                if self.jcl_info_dic[(jclName,jobSeq)] != jclId:
                    self.jcl_info_dic[(jclName,jobSeq)] = "複数候補が存在 要確認"
            else:
                self.jcl_info_dic[(jclName,jobSeq)] = jclId
                
    def getJobId(self, jclId, jobSeq):
        if self.dic == None:
            self.setup()
            
        if (jclId,jobSeq) in self.jcl_info_dic:
            return self.jcl_info_dic[(jclId,jobSeq)]
        else:
            return "JOB-ID不明 要確認"
        
    def insert(self,jclName,jobSeq,jclId,stepSeq,stepName,ddName,jobId,io,utilityId, hosoku):
        
        if self.dic == None:
            self.setup()
            
        if (jclName,jobSeq,stepSeq,ddName) in self.dic:
            if len(self.dic[(jclName,jobSeq,stepSeq,ddName)]) > 1:
                print("InsertUTL_STEP別_IO情報", "重複データが存在しています。JCL_NAME=" + jclName + " JOB_SEQ=" + jobSeq + " STEP_SEQ=" + stepSeq + " DD名=" + ddName)
            ioTemp = self.dic[(jclName,jobSeq,stepSeq,ddName)][0]
            if io in ioTemp:
                pass
            else:
                io = io + "/" + ioTemp
                
                set_key_list = ["IO"]
                set_value_list = [io]
                
                where_key_list = ["JCL_NAME","JOB_SEQ","STEP_SEQ","補足","DD名"]
                where_value_list = [jclName,jobSeq,stepSeq,hosoku,"P_"+ddName]
                
                sql,value = make_update_sql(self.dbname,set_value_list, set_key_list,where_value_list,where_key_list)
                self.cursor.execute(sql,value)
                
                self.dic[(jclName,jobSeq,stepSeq,ddName)][0] = io
                
            
        else:

            key_list = ["JCL_NAME","JOB_SEQ","JOB_ID","STEP_SEQ","STEP名","DD名","IO","Utility_ID","補足"]
            value_list = [jclName,jobSeq,jobId,stepSeq,stepName,"P_"+ddName,io,utilityId, hosoku]
            
            sql,value = make_insert_sql(self.dbname,value_list,key_list)
            
            self.cursor.execute(sql,value)
            self.dic[(jclName,jobSeq,stepSeq,ddName)] = [io]
            

        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
        

def GetIO(accessMode):

    if accessMode == "READ-ONLY":
        io = "INPUT"
    elif accessMode == "MODIFY":
        io = "I-O"
    elif accessMode == "UPDATE":
        io = "I-O"
    elif accessMode == "WRITE-ONLY":
        io = "OUTPUT"
    elif accessMode == "EXCLUSIVE-READ":
        io = "INPUT"
    else:
        print("⑥UTL_STEP別_IO情報", "不明なアクセスモードが指定されています。値=" + accessMode)
        io = "不明なアクセスモード"
    
    return io

def analysis6_update_UTL_STEP_IO(conn,cursor):
    

    global UTL_STEP別_IO情報_
    
    sql = "SELECT * FROM UTL_STEP別_IO情報 WHERE 補足 = '自動設定(DAM解析)'"
    df = pd.read_sql(sql,conn)
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("UTL_STEP別_IO情報",values,keys)
        cursor.execute(sql,values)
        
    # sql,values = make_delete_sql("UTL_STEP別_IO情報",[DB自動登録時PARM],["補足"])
    # cursor.execute(sql,values)
    
    ### 顧客別_JCL_STEP_SYSIN　読み込み
    sql =   """\
            SELECT * FROM 顧客別JCL_PED_DAMDATASET WHERE ACCESS_MODE <> ''
            """
    
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)
    
    UTL_STEP別_IO情報_ = UTL_STEP別_IO情報(conn,cursor)
    
    for i in range(len(df)):
        data = df.iloc[i]
        
        jclName = data["資産ID"]
        jobSeq = data["JOB_SEQ"]
        jclId = data["JCL_ID"]
        stepSeq = data["STEP_SEQ"]
        stepName = data["STEP_NAME"]
        ddName = data["DAM_DD_NAME"]
        jobId = UTL_STEP別_IO情報_.getJobId(data["資産ID"],data["JOB_SEQ"])
        io = GetIO(data["ACCESS_MODE"])
        
        UTL_STEP別_IO情報_.insert(jclName, jobSeq, jclId, stepSeq, stepName, ddName, jobId, io, utilityId, DB自動登録時PARM)
