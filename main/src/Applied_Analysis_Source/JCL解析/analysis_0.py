#!/usr/bin/env python
# -*- coding: cp932 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


class SUB_SQL生成_SYSIN_1:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "①JCL_STEP_SYSIN2"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
    def insert(self):
        if self.dic == None:
            self.setup()
            
        global ライブラリID,ファイル名,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_NAME,STEP_PGM,STEP_PROC,DD_NAME,SYSIN_SEQ,SYSIN_LINE
  
        key_list = ["LIBRARY_ID","JCL_NAME","JOB_SEQ","JOB_ID","STEP_SEQ","STEP_ID","PGM_NAME","PROC_NAME","SYSIN_PGM","SYSIN_DD","SYSIN_SEQ","SYSIN"]
        value_list = [ライブラリID,ファイル名,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_NAME,STEP_PGM,STEP_PROC,"",DD_NAME,SYSIN_SEQ,DB文字(SYSIN_LINE)]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
        
def analysis_0(SYSINSheet_GYO,file_path,conn,cursor):
    global ライブラリID,ファイル名,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_NAME,STEP_PGM,STEP_PROC,DD_NAME,SYSIN_SEQ,SYSIN_LINE
    
    ライブラリID = SYSINSheet_GYO[1]
    ファイル名 = SYSINSheet_GYO[2]
    JOB_SEQ = SYSINSheet_GYO[3]
    JOB_ID = SYSINSheet_GYO[4]
    STEP_SEQ = SYSINSheet_GYO[5]
    STEP_NAME = SYSINSheet_GYO[6]
    STEP_PGM = SYSINSheet_GYO[7]
    STEP_PROC = SYSINSheet_GYO[8]
    SYSIN_PGM = SYSINSheet_GYO[9]   #'値はないはず
    DD_NAME = SYSINSheet_GYO[10]
    SYSIN_SEQ = 0
    SYSIN_LINE = ""
    
    SUB_SQL生成_SYSIN_1_ = SUB_SQL生成_SYSIN_1(conn,cursor)
    
 
    if STEP_PGM == "EZTPA00" or STEP_PGM == "EASYTREV":
        SYSINSheet_GYO[14] = "EASY関連PARM SKIP"
        return SYSINSheet_GYO
    
    with open(file_path,errors="ignore") as TS:
        
        for strREC in TS:
            strREC = strREC.replace("\n","")
            SYSIN_LINE = strREC
            SYSIN_SEQ += 1
            SUB_SQL生成_SYSIN_1_.insert()
            
    
    return SYSINSheet_GYO
            