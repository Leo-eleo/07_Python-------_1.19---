#!/usr/bin/env python
# -*- coding: cp932 -*-
import sys
import os

import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


ActSheet = []
�ڋq��_JCL_PED_DAM�f�[�^�Z�b�g_ = None

class �ڋq��_JCL_PED_DAM�f�[�^�Z�b�g:
    
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�ڋq��JCL_PED_DAMDATASET"
        self.dbname2 = "PED_DAM�f�[�^�Z�b�g���"
        self.ped_dam_dic = {}
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        ### �ڋq��JCL_PED_DAMDATASET��DELETE�ŏ���������Ă���̂ōŏ��͋�
        
        sql = "SELECT * FROM "+self.dbname2
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        self.db_key_list = df.columns.tolist()
        for i in range(len(df)):
            data = df.iloc[i]
            dic = {key:data[key] for key in self.db_key_list}
            pedName = dic["PEDNAME"]
            if pedName not in self.ped_dam_dic:
                self.ped_dam_dic[pedName] = []
            self.ped_dam_dic[pedName].append(dic)
    
        
    def insert(self,assetID,jobSeq ,jclId,stepSeq ,stepName,pgmName,procName,ddName,cmdSeq ,pedName):
        
        if self.dic == None:
            self.setup()
            
        global ActSheet
        
        if pedName in self.ped_dam_dic:
            df = self.ped_dam_dic[pedName]
            for data in df:
                ActSheet_x = [""]*16
                key_list = ["���YID","JOB_SEQ","JCL_ID","STEP_SEQ","STEP_NAME","PGM_NAME","PROC_NAME","DD_NAME","CMD_SEQ","PED_NAME","SCHEMA_NAME","DAM_DD_NAME","DATASET_NAME","ACCESS_MODE","���l"]
                value_list = [assetID,jobSeq,jclId,stepSeq,stepName,pgmName,procName,ddName,cmdSeq,pedName,data["SCHEMANAME"],data["DDNAME"],data["DSN"],data["ACCESSMODE"],data["SCHEMAKUBUN"]]
                
                sql,value = make_insert_sql(self.dbname,value_list,key_list)
                
                self.cursor.execute(sql,value)
                
                ActSheet_x[1]= assetID
                ActSheet_x[2]= jobSeq
                ActSheet_x[3]= jclId
                ActSheet_x[4]= stepSeq
                ActSheet_x[5]= stepName
                ActSheet_x[6]= pgmName
                ActSheet_x[7]= procName
                ActSheet_x[8]= ddName
                ActSheet_x[9]= cmdSeq
                ActSheet_x[10] = pedName
                ActSheet_x[11] = data["SCHEMANAME"]
                ActSheet_x[12] = data["DDNAME"]
                ActSheet_x[13] = data["DSN"]
                ActSheet_x[14] = data["ACCESSMODE"]
                ActSheet_x[15] = data["SCHEMAKUBUN"]
                ActSheet.append(ActSheet_x)
                
        else:
            ActSheet_x = [""]*16
            key_list = ["���YID","JOB_SEQ","JCL_ID","STEP_SEQ","STEP_NAME","PGM_NAME","PROC_NAME","DD_NAME","CMD_SEQ","PED_NAME","���l"]
            value_list = [assetID,jobSeq,jclId,stepSeq,stepName,pgmName,procName,ddName,cmdSeq,pedName,"PED��`�����"]
            
            sql,value = make_insert_sql(self.dbname,value_list,key_list)
            
            self.cursor.execute(sql,value)
            
            ActSheet_x[1]= assetID
            ActSheet_x[2]= jobSeq
            ActSheet_x[3]= jclId
            ActSheet_x[4]= stepSeq
            ActSheet_x[5]= stepName
            ActSheet_x[6]= pgmName
            ActSheet_x[7]= procName
            ActSheet_x[8]= ddName
            ActSheet_x[9]= cmdSeq
            ActSheet_x[10] = pedName
            ActSheet_x[15] = "PED��`�����"
        
            ActSheet.append(ActSheet_x)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
 
 
def JCL�g�pDAM�f�[�^�Z�b�g���菈��(data):
    if "SUBSYS" not in data["PARM"]:
        return
    
    global �ڋq��_JCL_PED_DAM�f�[�^�Z�b�g_
    
    tokenList = ArrayEmptyDelete(data["PARM"].split(" "))
    for i in range(len(tokenList)):
        if tokenList[i] != "SUBSYS":
            continue
        if len(tokenList) > i+4 and tokenList[i+1] == "=" and tokenList[i+2] == "(" and tokenList[i+3] == "AIM":
            pedName = tokenList[i+4]  
            �ڋq��_JCL_PED_DAM�f�[�^�Z�b�g_.insert(data["���YID"],data["JOB_SEQ"], data["JCL_ID"], data["STEP_SEQ"], data["STEP_NAME"], data["PGM_NAME"], data["PROC_NAME"], data["DD_NAME"], data["CMD_SEQ"], pedName)
    

def analysis4_JCL_DAM2(conn,cursor):
    global �ڋq��_JCL_PED_DAM�f�[�^�Z�b�g_ 
    global ActSheet
    
    �ڋq��_JCL_PED_DAM�f�[�^�Z�b�g_ = �ڋq��_JCL_PED_DAM�f�[�^�Z�b�g(conn,cursor)
    
    
    sql = "SELECT * FROM �ڋq��JCL_PED_DAMDATASET"
    df = pd.read_sql(sql,conn)
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("�ڋq��JCL_PED_DAMDATASET",values,keys)
        cursor.execute(sql,values)
        
    # sql,values = make_delete_sql("�ڋq��JCL_PED_DAMDATASET",[],[])
    # cursor.execute(sql,values)
  
    sql =   """\
            SELECT * FROM �ڋq��_JCL_CMD��� WHERE DD_NAME='AIMPED'
            """
    
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)
    
    for i in range(len(df)):
        data = df.iloc[i]
        JCL�g�pDAM�f�[�^�Z�b�g���菈��(data)
    
    return ActSheet
        
    
