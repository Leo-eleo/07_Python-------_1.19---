#!/usr/bin/env python
# -*- coding: cp932 -*-
import sys
import os

import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


DB�����o�^��PARM = "�����ݒ�(DAM���)"
utilityId = ""

UTL_STEP��_IO���_ = None

class UTL_STEP��_IO���:
    
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "UTL_STEP��_IO���"
        self.dbname2 = "�ڋq��_JCL_��{���"
        self.jcl_info_dic = {}
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for jclName,jobSeq,stepSeq,ddName,io in zip(df["JCL_NAME"],df["JOB_SEQ"],df["STEP_SEQ"],df["DD��"],df["IO"]):
            if (jclName,jobSeq,stepSeq,ddName) in self.dic:
                self.dic[(jclName,jobSeq,stepSeq,ddName)].append(io)
            else:
                self.dic[(jclName,jobSeq,stepSeq,ddName)] = [io]

        
        sql = "SELECT * FROM "+self.dbname2
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for jclName,jobSeq,jclId in zip(df["JCL��"],df["JOB_SEQ"],df["JOB_ID"]):
            if (jclName,jobSeq) in self.jcl_info_dic:
                if self.jcl_info_dic[(jclName,jobSeq)] != jclId:
                    self.jcl_info_dic[(jclName,jobSeq)] = "������₪���� �v�m�F"
            else:
                self.jcl_info_dic[(jclName,jobSeq)] = jclId
                
    def getJobId(self, jclId, jobSeq):
        if self.dic == None:
            self.setup()
            
        if (jclId,jobSeq) in self.jcl_info_dic:
            return self.jcl_info_dic[(jclId,jobSeq)]
        else:
            return "JOB-ID�s�� �v�m�F"
        
    def insert(self,jclName,jobSeq,jclId,stepSeq,stepName,ddName,jobId,io,utilityId, hosoku):
        
        if self.dic == None:
            self.setup()
            
        if (jclName,jobSeq,stepSeq,ddName) in self.dic:
            if len(self.dic[(jclName,jobSeq,stepSeq,ddName)]) > 1:
                print("InsertUTL_STEP��_IO���", "�d���f�[�^�����݂��Ă��܂��BJCL_NAME=" + jclName + " JOB_SEQ=" + jobSeq + " STEP_SEQ=" + stepSeq + " DD��=" + ddName)
            ioTemp = self.dic[(jclName,jobSeq,stepSeq,ddName)][0]
            if io in ioTemp:
                pass
            else:
                io = io + "/" + ioTemp
                
                set_key_list = ["IO"]
                set_value_list = [io]
                
                where_key_list = ["JCL_NAME","JOB_SEQ","STEP_SEQ","�⑫","DD��"]
                where_value_list = [jclName,jobSeq,stepSeq,hosoku,"P_"+ddName]
                
                sql,value = make_update_sql(self.dbname,set_value_list, set_key_list,where_value_list,where_key_list)
                self.cursor.execute(sql,value)
                
                self.dic[(jclName,jobSeq,stepSeq,ddName)][0] = io
                
            
        else:

            key_list = ["JCL_NAME","JOB_SEQ","JOB_ID","STEP_SEQ","STEP��","DD��","IO","Utility_ID","�⑫"]
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
        print("�EUTL_STEP��_IO���", "�s���ȃA�N�Z�X���[�h���w�肳��Ă��܂��B�l=" + accessMode)
        io = "�s���ȃA�N�Z�X���[�h"
    
    return io

def analysis6_update_UTL_STEP_IO(conn,cursor):
    

    global UTL_STEP��_IO���_
    
    sql = "SELECT * FROM UTL_STEP��_IO��� WHERE �⑫ = '�����ݒ�(DAM���)'"
    df = pd.read_sql(sql,conn)
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("UTL_STEP��_IO���",values,keys)
        cursor.execute(sql,values)
        
    # sql,values = make_delete_sql("UTL_STEP��_IO���",[DB�����o�^��PARM],["�⑫"])
    # cursor.execute(sql,values)
    
    ### �ڋq��_JCL_STEP_SYSIN�@�ǂݍ���
    sql =   """\
            SELECT * FROM �ڋq��JCL_PED_DAMDATASET WHERE ACCESS_MODE <> ''
            """
    
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)
    
    UTL_STEP��_IO���_ = UTL_STEP��_IO���(conn,cursor)
    
    for i in range(len(df)):
        data = df.iloc[i]
        
        jclName = data["���YID"]
        jobSeq = data["JOB_SEQ"]
        jclId = data["JCL_ID"]
        stepSeq = data["STEP_SEQ"]
        stepName = data["STEP_NAME"]
        ddName = data["DAM_DD_NAME"]
        jobId = UTL_STEP��_IO���_.getJobId(data["���YID"],data["JOB_SEQ"])
        io = GetIO(data["ACCESS_MODE"])
        
        UTL_STEP��_IO���_.insert(jclName, jobSeq, jclId, stepSeq, stepName, ddName, jobId, io, utilityId, DB�����o�^��PARM)
