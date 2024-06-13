#!/usr/bin/env python
# -*- coding: cp932 -*-
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


vbCrLf = "\n"
���������� = []
����������2 = []

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
�ďo���@ = ""
����PGM = ""
DB�����o�^��PARM = "�����ݒ�iUTL��́j"
PGM�\�� = ""
����MODE = ""


���p_�ڋq��_JCL_STEP_SYSIN_ = None
#���p_�ڋq��_���Y�֘A�����_ = None
���p_�ڋq��_JCL_PGM_DSN3_ = None
���p_UTL_STEP��_IO���_ = None
DSNMTV01���pPGM�擾_ = None

#class ���p_�ڋq��_���Y�֘A�����:
#    
#    def __init__(self,conn):
#        self.dic = None
#        self.conn = conn
#        self.cursor = cursor
#        self.dbname = "�ڋq��_���Y�֘A�����"
    #    self.db_path = db_path
#
#    def setup(self):
#        self.dic = {}
#        sql = "SELECT * FROM "+self.dbname
#        
#        df = pd.read_sql(sql,self.conn)
#        
#        for from_source,type,to_source in zip(df["�ďo�����Y"],df["�ďo���@"],df["�ďo�掑�Y"]):
#            self.dic[(from_source,type,to_source)] = 1
#    
#        
#    def insert(self):
#        if self.dic == None:
#            self.setup()
#            
#        global JCL_NAME,�ďo���@,����PGM,DB�����o�^��PARM
#        if (JCL_NAME,�ďo���@,����PGM) in self.dic:
#            return False
#        
#        key_list = ["�ďo�����Y","�ďo���@","�ďo�掑�Y","�o�^����"]
#        value_list = [JCL_NAME,�ďo���@,����PGM,DB�����o�^��PARM]
#        
#        sql,value = make_insert_sql(self.dbname,value_list,key_list)
#        
#        self.cursor.execute(sql,value)
#        self.dic[(JCL_NAME,�ďo���@,����PGM)] = 1
#        
#        return True
#    
#    def _close_conn(self):
#        if self.conn != None:
#            self.conn.close() 
#    
#    def close_conn(self):
#        self._close_conn()
    
    
class ���p_�ڋq��_JCL_PGM_DSN3:
    
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�ڋq��_JCL_PGM_DSN"
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
            
        global JCL_NAME,JOB_SEQ,STEP_SEQ,����PGM,PGM�\��,����MODE,DB�����o�^��PARM
        
        if (JCL_NAME,JOB_SEQ,STEP_SEQ) not in self.dic:
            return False
        

        set_key_list = ["SYSIN_PGM","PGM�\��","���s���[�h","�����X�VFLG"]
        set_value_list = [����PGM,PGM�\��,����MODE,DB�����o�^��PARM]
        
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
        
        for jcl,job,step in zip(df["JCL_NAME"],df["JOB_SEQ"],df["STEP_SEQ"]):
            self.dic[(jcl,job,step)] = 1
    
        
    def update(self):
        if self.dic == None:
            self.setup()
            
        global JCL_NAME,JOB_SEQ,STEP_SEQ,����PGM,DB�����o�^��PARM
        
        if (JCL_NAME,JOB_SEQ,STEP_SEQ) not in self.dic:
            return False
        

        set_key_list = ["SYSIN_PGM","�����X�VFLG"]
        set_value_list = [����PGM,DB�����o�^��PARM]
        
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
    
class DSNMTV01���pPGM�擾:
    
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "QRY_DFSRRC00_DSNMTV01"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        
        for jcl,job,step,sysin in zip(df["JCL_NAME"],df["JOB_SEQ"],df["STEP_SEQ"],df["SYSIN"]):
            self.dic[(jcl,job,step)] = str(sysin)
        
    
        
    def get(self):
        global JCL_NAME,JOB_SEQ,STEP_SEQ
           
        if self.dic == None:
            self.setup()
            
        if (JCL_NAME,JOB_SEQ,STEP_SEQ) in self.dic:
            return self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ)]
        
        else:
            return ""


def DFSRRC00_BMP_DLI_���ʏo��(data):
       
       
    global LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME,PROC_NAME,SYSIN_PGM,SYSIN_SEQ,PARM_EXEC,PARM_PROC
    global ����������,����������2,vbCrLf
    
     
    
    ActSheet_x = [""]*20
    ActSheet_x[1] = ""                 ###JCL_CMD���ɓ��Y���ڂ��Ȃ��̂ŉ��ݒ�
    ActSheet_x[2] = data["���YID"]
    ActSheet_x[3] = data["JOB_SEQ"]       ###�Ή���
    ActSheet_x[4] = data["JCL_ID"]
    ActSheet_x[5] = data["STEP_SEQ"]
    ActSheet_x[6] = data["STEP_NAME"]
    ActSheet_x[7] = data["PGM_NAME"]
    ActSheet_x[8] = data["PROC_NAME"]
    ActSheet_x[9] = ""                 ###JCL_CMD���ɓ��Y���ڂ��Ȃ��̂ŉ��ݒ�
    ActSheet_x[10] = 0                  ###�g��Ȃ�
    ActSheet_x[11] = str(data["PARM_EXEC"]) + vbCrLf + str(data["PARM_PROC"])
    
    
    
    ###LIBRARY_ID = data["LIBRARY_ID"]
    JCL_NAME = data["���YID"]
    JOB_SEQ = data["JOB_SEQ"]
    JOB_ID = data["JCL_ID"]
    STEP_SEQ = data["STEP_SEQ"]
    STEP_ID = data["STEP_NAME"]
    PGM_NAME = data["PGM_NAME"]
    PROC_NAME = data["PROC_NAME"]
    SYSIN_PGM = ""
    ###SYSIN_SEQ = data["SYSIN_SEQ"]
    PARM_EXEC = data["PARM_EXEC"]
    PARM_PROC = data["PARM_PROC"]
    
    
    ���������� = ArrayEmptyDelete(data["PARM_EXEC"].split(" "))    
    ����������2 = ArrayEmptyDelete(data["PARM_PROC"].split(" "))
    
    
    return ActSheet_x


def DFSRRC00_BMP_DLI_��͏���(ActSheet_x):
    #global ���p_�ڋq��_JCL_STEP_SYSIN_,���p_�ڋq��_���Y�֘A�����_,���p_�ڋq��_JCL_PGM_DSN3_,DSNMTV01���pPGM�擾_
    global ���p_�ڋq��_JCL_STEP_SYSIN_,���p_�ڋq��_JCL_PGM_DSN3_,DSNMTV01���pPGM�擾_
    global LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME,PROC_NAME,SYSIN_PGM,SYSIN_SEQ,PARM_EXEC,PARM_PROC,�ďo���@,����PGM
    global ����������,����������2,����MODE,PGM�\��,vbCrLf,SYSIN
    
    L_DLI_TYPE = ""
    L_DLI_MBR = ""

    
    ###��UTL�Ή�
    ###=== DFSRRC00 ===
    if PGM_NAME == "DFSRRC00":
        L_DLI_TYPE = ""
        L_DLI_MBR = ""
        for i in range(len(����������)):
            if ����������[i] == "PARM":
                
                if  (i + 4) >= len(����������):
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "DFSRRC00-BMP_DLI �z��v�f�s��"
                    continue
                
                if ����������[i + 1] == "=" and ����������[i + 2] == "(":
                    L_DLI_TYPE = ����������[i + 3]
                    L_DLI_MBR = ����������[i + 4]
                    
                    if L_DLI_TYPE == "BMP":
                        ActSheet_x[12] = "DFSRRC00-BMP"
                        �ďo���@ = "DFSRRC00-BMP"
                        ����MODE = "BMP"
                    elif L_DLI_TYPE =="DLI":
                        ActSheet_x[12] = "DFSRRC00-DLI"
                        �ďo���@ = "DFSRRC00-DLI"
                        ����MODE = "DLI"
                    elif L_DLI_TYPE =="ULU":
                        ActSheet_x[12] = "DFSRRC00-ULU"
                        �ďo���@ = "DFSRRC00-ULU"
                        ����MODE = "ULU"
                    else:
                        ActSheet_x[12] = "DFSRRC00-OTHER"
                        �ďo���@ = "DFSRRC00-" + L_DLI_TYPE
                        ����MODE = "OTHER"
                    
                    
                    if "&" in L_DLI_MBR:
                        L_DLI_MBR = ����������[i + 4].replace("&", "")
                    
                        for j in range(len(����������2)):
                            if ����������2[j] == L_DLI_MBR:
                                if (j + 2) < len(����������2):
                                    if ����������2[j + 1] == "=":
                                        ����PGM = ����������2[j + 2]
                                    else:
                                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "DFSRRC00-BMP_DLI �z��v�f�s��"
                                    
                                else:
                                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "DFSRRC00-BMP_DLI �z��v�f�s��"
                    
                        
                        if ����PGM == "":
                            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "DFSRRC00-BMP_DLI PGM�s��"
                    
                        
                    else:
                        ����PGM = L_DLI_MBR
            
                ###ULU���[�h�̏ꍇ�u(�v���Ȃ��ꍇ������
                elif ����������[i + 1] == "=" and ����������[i + 2] == "ULU":
                    if i + 3 < len(����������):
                        L_DLI_TYPE = ����������[i + 2]
                        ����PGM = ����������[i + 3].replace("&","").replace("\"", "")
                        ActSheet_x[12] = "DFSRRC00-ULU"
                        �ďo���@ = "DFSRRC00-ULU"
                        ����MODE = "ULU"
                        
                    else:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "DFSRRC00-ULU �z��v�f�s��"
                    
                else:
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "DFSRRC00-BMP_DLI �z��v�f�s��"
                

    if ����PGM != "" and ����PGM != "DSNMTV01":     ### DSNMTV01 �́@�uDFSRRC00_DSNMTV01_��͏����v�ŏ�������
        #if ���p_�ڋq��_���Y�֘A�����_.insert() == False:
        #    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
        #else:
        #    ActSheet_x[13] = 1
        #    
        #    ActSheet_x[9]= ����PGM
        #
        #    ### ===�b��Ή�
        #    ActSheet_x[17] = ����PGM
        #    ### ===
   
                      
        PGM�\�� = ""     ###�ݒ肵�Ȃ��̂ŏ���������
        if  ���p_�ڋq��_JCL_PGM_DSN3_.update() == False:
            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "�X�V��񖳂��̈׏���SKIP"
        else:
            ActSheet_x[15] = 1
       
        ### �������ڋq��_JCL_STEP_SYSIN���X�V���鏈���ǉ�
       
        if ���p_�ڋq��_JCL_STEP_SYSIN_.update() == False:
            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "�X�V��񖳂��̈׏���SKIP"
        else:
            ActSheet_x[17] = ����PGM
            ActSheet_x[19] = 1
              
    ### ������DSNMTV01 �Ή�
    elif ����PGM == "DSNMTV01":
        �ďo���@ = �ďo���@ + "-DSNMTV01"
        ActSheet_x[12] = �ďo���@
        SYSIN = DSNMTV01���pPGM�擾_.get()
        ����������3 = SYSIN.split(" ")
        ActSheet_x[11] = ActSheet_x[11] + vbCrLf + SYSIN ### �Ԉ���Ă��� 12�ł�?
        if len(����������3) > 7:
           
            ����PGM = ����������3[7]  ### ��Ŋm�F
            
            if ����PGM != "":
                #if ���p_�ڋq��_���Y�֘A�����_.insert() == False:
                #    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                #else:
                #    ActSheet_x[13] = 1
                #    ActSheet_x[9]= ����PGM
                #
                #    ### ===�b��Ή�
                #    ActSheet_x[17] = ����PGM
                #    ### ===
                                
                      
                ### �������ڋq��_JCL_STEP_SYSIN���X�V���鏈���ǉ�
       
                if ���p_�ڋq��_JCL_STEP_SYSIN_.update() == False:
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "�X�V��񖳂��̈׏���SKIP"
                else:
                    ActSheet_x[17] = ����PGM
                    ActSheet_x[19] = 1

            else:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "DFSRRC00-DSNMTV01 �z��v�f��"
 
            if ����PGM != "":
           
                PGM�\�� = "DSNMTV01"
                if ���p_�ڋq��_JCL_PGM_DSN3_.update() == False:
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "�X�V��񖳂��̈׏���SKIP"
                else:
                    ActSheet_x[15] = 1

        else:
            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "DFSRRC00-DSNMTV01 PGM���擾�G���["
           
    else:
        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "DFSRRC00-BMP_DLI �z��v�f��"
        
    return ActSheet_x


def analysis2_DFSRRC00(conn,cursor):
    
    ### �ύX20191011
    sql =   """\
            SELECT * FROM QRY_DFSRRC00_BMP_DLI_ULU
            """
            
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)

    #global ���p_�ڋq��_JCL_STEP_SYSIN_,���p_�ڋq��_���Y�֘A�����_,���p_�ڋq��_JCL_PGM_DSN3_,DSNMTV01���pPGM�擾_
    global ���p_�ڋq��_JCL_STEP_SYSIN_,���p_�ڋq��_JCL_PGM_DSN3_,DSNMTV01���pPGM�擾_
    
    ���p_�ڋq��_JCL_STEP_SYSIN_ = ���p_�ڋq��_JCL_STEP_SYSIN(conn,cursor)
    #���p_�ڋq��_���Y�֘A�����_ = ���p_�ڋq��_���Y�֘A�����(conn,cursor)
    ���p_�ڋq��_JCL_PGM_DSN3_ = ���p_�ڋq��_JCL_PGM_DSN3(conn,cursor)
    DSNMTV01���pPGM�擾_ = DSNMTV01���pPGM�擾(conn,cursor)
  

    ### VBA�ŃV�[�g�ɏ�������ł������ɂ��̃��X�g�ɒǉ����čŌ�ɂ܂Ƃ߂ď�������
    ActSheet = []
    print(len(df),"analysis2_DFSRRC00")
    for i in range(len(df)):
        data = df.iloc[i]
        ActSheet_x = DFSRRC00_BMP_DLI_���ʏo��(data)
        ActSheet_x = DFSRRC00_BMP_DLI_��͏���(ActSheet_x)
        ActSheet.append(ActSheet_x)
        
    print(len(ActSheet),"analysis2")
    
    
    return ActSheet
    

    