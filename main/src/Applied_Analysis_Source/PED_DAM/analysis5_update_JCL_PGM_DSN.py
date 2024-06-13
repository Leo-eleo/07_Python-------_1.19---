#!/usr/bin/env python
# -*- coding: cp932 -*-
import sys
import os

import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


DB自動登録時PARM = "自動設定(DAM解析)"
#'仮の設定 UTIL解析を掛ける必要があるため。
DB自動登録時PARM2 = "自動設定（UTL解析)"
    
JCL_PGM_DSN_ = None

class JCL_PGM_DSN:
    
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "顧客別_JCL_PGM_DSN"
        self.dbname2 = "顧客別_JCL_基本情報"
        self.jcl_info_dic = {}
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
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
        
    def insert(self,libraryId, jclName, jobSeq, jobId, stepSeq, stepName, pgmName, procName, sysinPgm, ddName, dsn, \
                    handFlg = "DEFAULT", autoFlg = "自動設定(DAM解析)"):
        
        if self.dic == None:
            self.setup()
            

        key_list = ["LIBRARY_ID","JCL_NAME","JOB_SEQ","JOB_ID","STEP_SEQ","STEP_NAME","PGM_NAME","PROC_NAME","SYSIN_PGM","DD_NAME","DSN","手動更新FLG","自動更新FLG"]
        value_list = [libraryId,jclName,jobSeq,jobId,stepSeq,stepName,pgmName,procName,sysinPgm,"P_" + ddName,dsn,handFlg,autoFlg]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)

        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
 
 

def analysis5_update_JCL_PGM_DSN(conn,cursor):
    global JCL_PGM_DSN_
    
    sql = "SELECT * FROM 顧客別_JCL_PGM_DSN WHERE 手動更新FLG = '' AND 自動更新FLG = '自動設定(DAM解析)'"
    df = pd.read_sql(sql,conn)
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("顧客別_JCL_PGM_DSN",values,keys)
        cursor.execute(sql,values)

    # sql,values = make_delete_sql("顧客別_JCL_PGM_DSN",["",DB自動登録時PARM],["手動更新FLG","自動更新FLG"])
    
    
    #  'この処理が終わったあと応用UTL解析を掛けてSYSIN_PGMを出力する必要があるが、その際にFLGが自動設定(UTL解析)に更新されてしまう可能性があるので苦肉の策
    # '    cmd = "DELETE FROM 顧客別_JCL_PGM_DSN WHERE 手動更新FLG = '' AND 自動更新FLG = '" & DB自動登録時PARM2 & "';"
    # '    con.Execute cmd
    
    # cursor.execute(sql,values)
    # conn.commit()
    
    ### 顧客別_JCL_STEP_SYSIN　読み込み
    sql =   """\
            SELECT * FROM 顧客別JCL_PED_DAMDATASET WHERE 備考 IS NULL
            """
    
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)
    
    JCL_PGM_DSN_ = JCL_PGM_DSN(conn,cursor)
    
    for i in range(len(df)):
        data = df.iloc[i]
        
        jobId = JCL_PGM_DSN_.getJobId(data["資産ID"],data["JOB_SEQ"])
        _,library,_,_ = GetFileInfo(data["資産ID"])
        JCL_PGM_DSN_.insert(library, data["資産ID"], data["JOB_SEQ"], jobId, \
                               data["STEP_SEQ"], data["STEP_NAME"], data["PGM_NAME"], data["PROC_NAME"], \
                               "", data["DAM_DD_NAME"], data["DATASET_NAME"], "", DB自動登録時PARM)
    
