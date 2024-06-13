#!/usr/bin/env python
# -*- coding: cp932 -*-
import sys
import os

import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


DB�����o�^��PARM = "�����ݒ�(DAM���)"
#'���̐ݒ� UTIL��͂��|����K�v�����邽�߁B
DB�����o�^��PARM2 = "�����ݒ�iUTL���)"
    
JCL_PGM_DSN_ = None

class JCL_PGM_DSN:
    
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�ڋq��_JCL_PGM_DSN"
        self.dbname2 = "�ڋq��_JCL_��{���"
        self.jcl_info_dic = {}
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
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
        
    def insert(self,libraryId, jclName, jobSeq, jobId, stepSeq, stepName, pgmName, procName, sysinPgm, ddName, dsn, \
                    handFlg = "DEFAULT", autoFlg = "�����ݒ�(DAM���)"):
        
        if self.dic == None:
            self.setup()
            

        key_list = ["LIBRARY_ID","JCL_NAME","JOB_SEQ","JOB_ID","STEP_SEQ","STEP_NAME","PGM_NAME","PROC_NAME","SYSIN_PGM","DD_NAME","DSN","�蓮�X�VFLG","�����X�VFLG"]
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
    
    sql = "SELECT * FROM �ڋq��_JCL_PGM_DSN WHERE �蓮�X�VFLG = '' AND �����X�VFLG = '�����ݒ�(DAM���)'"
    df = pd.read_sql(sql,conn)
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("�ڋq��_JCL_PGM_DSN",values,keys)
        cursor.execute(sql,values)

    # sql,values = make_delete_sql("�ڋq��_JCL_PGM_DSN",["",DB�����o�^��PARM],["�蓮�X�VFLG","�����X�VFLG"])
    
    
    #  '���̏������I��������Ɖ��pUTL��͂��|����SYSIN_PGM���o�͂���K�v�����邪�A���̍ۂ�FLG�������ݒ�(UTL���)�ɍX�V����Ă��܂��\��������̂ŋ���̍�
    # '    cmd = "DELETE FROM �ڋq��_JCL_PGM_DSN WHERE �蓮�X�VFLG = '' AND �����X�VFLG = '" & DB�����o�^��PARM2 & "';"
    # '    con.Execute cmd
    
    # cursor.execute(sql,values)
    # conn.commit()
    
    ### �ڋq��_JCL_STEP_SYSIN�@�ǂݍ���
    sql =   """\
            SELECT * FROM �ڋq��JCL_PED_DAMDATASET WHERE ���l IS NULL
            """
    
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)
    
    JCL_PGM_DSN_ = JCL_PGM_DSN(conn,cursor)
    
    for i in range(len(df)):
        data = df.iloc[i]
        
        jobId = JCL_PGM_DSN_.getJobId(data["���YID"],data["JOB_SEQ"])
        _,library,_,_ = GetFileInfo(data["���YID"])
        JCL_PGM_DSN_.insert(library, data["���YID"], data["JOB_SEQ"], jobId, \
                               data["STEP_SEQ"], data["STEP_NAME"], data["PGM_NAME"], data["PROC_NAME"], \
                               "", data["DAM_DD_NAME"], data["DATASET_NAME"], "", DB�����o�^��PARM)
    
