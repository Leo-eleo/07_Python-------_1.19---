#!/usr/bin/env python
# -*- coding: cp932 -*-
import os
import sys

import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


���p_�ڋq��_JCL_STEP_SYSIN_ = None
���p_�ڋq��_JCL_STEP���_ = None

class ���p_�ڋq��_JCL_STEP_SYSIN:
    
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�ڋq��_JCL_STEP_SYSIN"
        # self.db_path = db_path
        
    def setup(self):
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        
        for jcl,pgm,job,step,sysin,sysin_pgm in zip(df["JCL_NAME"],df["PGM_NAME"],df["JOB_SEQ"],df["STEP_SEQ"],df["SYSIN"],df["SYSIN_PGM"]):
            if pgm != "UTACH":
                continue
            if (jcl,job,step) not in self.dic:
                self.dic[(jcl,job,step)] = []
            dic = {"SYSIN":sysin,"SYSIN_PGM":sysin_pgm}
            self.dic[(jcl,job,step)].append(dic)
            
    
        
    def get(self,JCL_NAME,JOB_SEQ,STEP_SEQ):
        if self.dic == None:
            self.setup()
            
        
        if (JCL_NAME,JOB_SEQ,STEP_SEQ) not in self.dic:
            return []
        
        return self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ)]
    

class ���p_�ڋq��_JCL_STEP���:
    
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�ڋq��_JCL_STEP���"
        # self.db_path = db_path
        
    def setup(self):
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        
        for jcl,pgm,job,step,key,value in zip(df["JCL_NAME"],df["PGM_NAME"],df["JOB_SEQ"],df["STEP_SEQ"],df["PARM_VAR_LIST"],df["PARM_VALUE_LIST"]):
            if (jcl,pgm,job,step) not in self.dic:
                self.dic[(jcl,pgm,job,step)] = []
            dic = {"PARM_VAR_LIST":key,"PARM_VALUE_LIST":value}
            self.dic[(jcl,pgm,job,step)].append(dic)
            
        
    def get(self,JCL_NAME,BMCP_PGM_NAME,JOB_SEQ,STEP_SEQ):
        if self.dic == None:
            self.setup()
            
        
        if (JCL_NAME,BMCP_PGM_NAME,JOB_SEQ,STEP_SEQ) not in self.dic:
            return []
        
        return self.dic[(JCL_NAME,BMCP_PGM_NAME,JOB_SEQ,STEP_SEQ)]
       
    


def GetBatchPGM_ExecUTACH(JCL_NAME, JOB_SEQ, STEP_SEQ, BMCP_PGM_NAME):
    global ���p_�ڋq��_JCL_STEP_SYSIN_
    
    
    myRS = ���p_�ڋq��_JCL_STEP_SYSIN_.get(JCL_NAME,JOB_SEQ,STEP_SEQ)
    if myRS == []:
        return "SYSIN���s�� �v�m�F"
    
    SYSIN_PGM = ""
    SYSIN = ""
    SYSIN_PGM_ARRAY = []
    SYSIN_ARRAY = []
    ArrCount = 0
    isFind = False
    ���������� = []
    ����������2 = []
    GetBatchPGM = "SYSIN���s�� �v�m�F2"
    ArrCount = 0
    
    ###SYSIN�s�𒊏o����B
    
    for i in range(len(myRS)):
        data = myRS[i]
        SYSIN_PGM = data["SYSIN_PGM"]
        if "," in SYSIN_PGM:
            SYSIN_PGM_ARRAY = SYSIN_PGM.split(",")
            for j in range(len(SYSIN_PGM_ARRAY)):
                if SYSIN_PGM_ARRAY[j] == BMCP_PGM_NAME:
                    ArrCount = ArrCount + 1
                    SYSIN_ARRAY.append(data["SYSIN"])
            
        else:
            if SYSIN_PGM == BMCP_PGM_NAME:
                ArrCount = ArrCount + 1
                SYSIN_ARRAY.append(data["SYSIN"])
    
    
    #���o����SYSIN�s����͂���
    if ArrCount > 0:
        for j in range(len(SYSIN_ARRAY)):
            SYSIN = SYSIN_ARRAY[j]
            if "TA" in SYSIN and "PGM=" + BMCP_PGM_NAME in SYSIN:
                ���������� = SYSIN.split(" ")
                
                for k in range(len(����������)):
                    
                    if "PARM=" in ����������[k]:
                        if ����������[k] == "PARM=":
                            ###PARM= 4=KS28�̂悤�ȃp�^�[���Ή�
                            ����������2 = ����������[k + 1].split("=")
                        else:
                            ����������2 = ����������[k].split("=")
                        
                        GetBatchPGM = ����������2[-1]

    return GetBatchPGM
    

def GetBatchPGM_ExecBMCP(JCL_NAME, BMCP_PGM_NAME, JOB_SEQ, STEP_SEQ):
    global ���p_�ڋq��_JCL_STEP���_
    
    myRS = ���p_�ڋq��_JCL_STEP���_.get(JCL_NAME,BMCP_PGM_NAME,JOB_SEQ,STEP_SEQ)
    if myRS == []:
        return "Parm���s�� �v�m�F"
    
    
    VAR_LIST = ""
    VALUE_LIST = ""
    PARM_VAR_ARRAY = []
    PARM_INDEX = 0
    
    
    for i in range(len(myRS)):
        data = myRS[i]
        VAR_LIST = data["PARM_VAR_LIST"]
        VALUE_LIST = data["PARM_VALUE_LIST"]
        
        if " PARM" in VAR_LIST or "PARM " in VAR_LIST or VAR_LIST == "PARM":
            PARM_VAR_ARRAY = ArrayEmptyDelete(VAR_LIST.split(" "))
            for j in range(len(PARM_VAR_ARRAY)):
                if PARM_VAR_ARRAY[j] == "PARM":
                    PARM_INDEX = j
                    break
            return  ArrayEmptyDelete(VALUE_LIST.split(" "))[PARM_INDEX].replace("\"", "")
        
    return "Parm���s�� �v�m�F2"
    
        

def analysis2_Get_BMCP_PGM(BMCP_Sheet,conn,cursor):
    global ���p_�ڋq��_JCL_STEP_SYSIN_
    global ���p_�ڋq��_JCL_STEP���_
    
    ���p_�ڋq��_JCL_STEP_SYSIN_ = ���p_�ڋq��_JCL_STEP_SYSIN(conn,cursor)
    ���p_�ڋq��_JCL_STEP���_ = ���p_�ڋq��_JCL_STEP���(conn,cursor)
    
    for i in range(len(BMCP_Sheet)):
        
        JCL_NAME = BMCP_Sheet[i][1]
        JOB_SEQ = BMCP_Sheet[i][2]
        STEP_SEQ = BMCP_Sheet[i][3]
        PGM_NAME = BMCP_Sheet[i][4]
        SYSIN_PGM = BMCP_Sheet[i][5]
        
        if PGM_NAME == "UTACH":
            BMCP_Sheet[i][6] = GetBatchPGM_ExecUTACH(JCL_NAME=JCL_NAME, JOB_SEQ=JOB_SEQ, STEP_SEQ=STEP_SEQ, BMCP_PGM_NAME=SYSIN_PGM)
        else:
            BMCP_Sheet[i][6] = GetBatchPGM_ExecBMCP(JCL_NAME=JCL_NAME, BMCP_PGM_NAME=PGM_NAME, JOB_SEQ=JOB_SEQ, STEP_SEQ=STEP_SEQ)
            

    return BMCP_Sheet
