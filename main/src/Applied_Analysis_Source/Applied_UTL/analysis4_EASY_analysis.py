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

���Y�֘A��_�ǉ�_CNT = 0
JCL_PGM_DSN_�ǉ�_CNT = 0
JCL_PGM_DSN_�X�V_CNT = 0
UTL_STEP��_IO���_�ǉ�_CNT = 0

���p_�ڋq��_JCL_STEP_SYSIN_ = None
#���p_�ڋq��_���Y�֘A�����_ = None
���p_�ڋq��_JCL_PGM_DSN3_ = None


#class ���p_�ڋq��_���Y�֘A�����:
#    
#    def __init__(self,conn,cursor):
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
    


def EASY���p�����_���ʏo��(data):
       
       
    global LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME,PROC_NAME,SYSIN_PGM,SYSIN_SEQ,SYSIN

    global ���Y�֘A��_�ǉ�_CNT,JCL_PGM_DSN_�ǉ�_CNT,JCL_PGM_DSN_�X�V_CNT,UTL_STEP��_IO���_�ǉ�_CNT
    
    ActSheet_x = [""]*20
    ActSheet_x[1] = data["LIBRARY_ID"]
    ActSheet_x[2] = data["JCL_NAME"]
    ActSheet_x[3] = data["JOB_SEQ"]
    ActSheet_x[4] = data["JOB_ID"]
    ActSheet_x[5] = data["STEP_SEQ"]
    ActSheet_x[6] = data["STEP_NAME"]
    ActSheet_x[7] = data["PGM_NAME"]
    ActSheet_x[8] = data["PROC_NAME"]
    ActSheet_x[9] = data["SYSIN_PGM"]
    ActSheet_x[10] = ""
    ActSheet_x[11] = data["SYSIN"]
    
    LIBRARY_ID = data["LIBRARY_ID"]
    JCL_NAME = data["JCL_NAME"]
    JOB_SEQ = data["JOB_SEQ"]
    JOB_ID = data["JOB_ID"]
    STEP_SEQ = data["STEP_SEQ"]
    STEP_ID = data["STEP_NAME"]
    PGM_NAME = data["PGM_NAME"]
    PROC_NAME = data["PROC_NAME"]
    SYSIN_PGM = data["SYSIN_PGM"]
    ###SYSIN_SEQ = data["SYSIN_SEQ"]
    SYSIN = data["SYSIN"]


    ���Y�֘A��_�ǉ�_CNT = 0
    JCL_PGM_DSN_�ǉ�_CNT = 0
    JCL_PGM_DSN_�X�V_CNT = 0
    UTL_STEP��_IO���_�ǉ�_CNT = 0
        
    return ActSheet_x


def EASY���p�����_��͏���(ActSheet_x):
    #global ���p_�ڋq��_JCL_STEP_SYSIN_,���p_�ڋq��_���Y�֘A�����_,���p_�ڋq��_JCL_PGM_DSN3_
    global ���p_�ڋq��_JCL_STEP_SYSIN_,���p_�ڋq��_JCL_PGM_DSN3_
    global LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME,PROC_NAME,SYSIN_PGM,SYSIN_SEQ,SYSIN,�ďo���@,����PGM,PGM�\��,����MODE
    global ����������,����������2,vbCrLf
    

    
    
    ###��UTL�Ή�
    ###=== DFSRRC00 ===
    if PGM_NAME == "EZTPA00" or PGM_NAME == "EASYTREV" or PGM_NAME == "DFSRRC00" or PROC_NAME == "IMSEASY":  ###QRY�ł���ȊO��PGM�͗��Ȃ��͂�
        
        if SYSIN_PGM == "EZTPA00" or PGM_NAME == "EZTPA00" :
            if SYSIN != "":
                ActSheet_x[12] = "EZTPA00-LIB"
                �ďo���@ = "EZTPA00-LIB"
                ����PGM = SYSIN
                PGM�\�� = "EZTPA00"
                ����MODE = "EASYP-LIB"
            else:
                ActSheet_x[12] = "EZTPA00-JCL ��PGM���v�蓮�C��"
                �ďo���@ = "EZTPA00-JCL"
                ����PGM = JOB_ID + "EA"
                PGM�\�� = "EZTPA00"
                ����MODE = "EASYP-JCL"
           
        
        elif SYSIN_PGM == "EASYTREV" or PGM_NAME == "EASYTREV" :
            if SYSIN != "" :
                ActSheet_x[12] = "EASYTREV-LIB"
                �ďo���@ = "EASYTREV-LIB"
                ����PGM = SYSIN
                PGM�\�� = "EASYTREV"
                ����MODE = "EASY-LIB"
            else:
                ActSheet_x[12] = "EASYTREV-JCL ��PGM���v�蓮�C��"
                �ďo���@ = "EASYTREV-JCL"
                ����PGM = JOB_ID + "EA"
                PGM�\�� = "EASYTREV"
                ����MODE = "EASY-JCL"
           
                
        elif PROC_NAME == "IMSEASY" :
            if SYSIN != "" :
                ActSheet_x[12] = "EASYTREV-LIB"
                �ďo���@ = "EASYTREV-LIB"
                ����PGM = SYSIN
                PGM�\�� = "EASYTREV"
                ����MODE = "EASY-LIB"
            else:
                ActSheet_x[12] = "EASYTREV-JCL ��PGM���v�蓮�C��"
                �ďo���@ = "EASYTREV-JCL"
                ����PGM = JOB_ID + "EA"
                PGM�\�� = "EASYTREV"
                ����MODE = "EASY-JCL"
           
                
        else:
            ActSheet_x[12] = "EASY ���z��O��PGM���"
            �ďo���@ = ""
            ����PGM = ""
        
            
        if ����PGM != "" :
        
            ###�������֘A��TABLE�ɏo�͂��鏈���ǉ�
            #if ���p_�ڋq��_���Y�֘A�����_.insert() == False:
            #    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
            #else:
            #    ActSheet_x[13] = 1
            #    ActSheet_x[9]= ����PGM
            #
            #    ### ===�b��Ή�
            #    ActSheet_x[17] = ����PGM
            #    ### ===
 
                ###�������ڋq��_JCL_STEP_SYSIN���X�V���鏈���ǉ�
    
            if ���p_�ڋq��_JCL_STEP_SYSIN_.update() == False:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "�X�V��񖳂��̈׏���SKIP"
            else:
                ActSheet_x[17] = ����PGM
                ActSheet_x[19] = 1

                    
        if ����PGM != "":
                   
            if ���p_�ڋq��_JCL_PGM_DSN3_.update() == False:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "�X�V��񖳂��̈׏���SKIP"
            else:
                ActSheet_x[15] = 1
                
        
    return ActSheet_x                  
     
    

    
    
def analysis4_EASY_analysis(conn,cursor):
    
    ### �ύX20191011
    sql =   """\
            SELECT * FROM QRY_EASY���o_UNION
            """
            
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)
    print(len(df),"analysis4_EASY_analysis")
    #global ���p_�ڋq��_JCL_STEP_SYSIN_,���p_�ڋq��_���Y�֘A�����_,���p_�ڋq��_JCL_PGM_DSN3_
    global ���p_�ڋq��_JCL_STEP_SYSIN_,���p_�ڋq��_JCL_PGM_DSN3_
   
    ���p_�ڋq��_JCL_STEP_SYSIN_ = ���p_�ڋq��_JCL_STEP_SYSIN(conn,cursor)
    #���p_�ڋq��_���Y�֘A�����_ = ���p_�ڋq��_���Y�֘A�����(conn,cursor)
    ���p_�ڋq��_JCL_PGM_DSN3_ = ���p_�ڋq��_JCL_PGM_DSN3(conn,cursor)
 
    ### VBA�ŃV�[�g�ɏ�������ł������ɂ��̃��X�g�ɒǉ����čŌ�ɂ܂Ƃ߂ď�������
    ActSheet = []
    for i in range(len(df)):
        data = df.iloc[i]
        ActSheet_x = EASY���p�����_���ʏo��(data)
        ActSheet_x = EASY���p�����_��͏���(ActSheet_x)
        ActSheet.append(ActSheet_x)
    print(len(ActSheet),"analysis4")

    return ActSheet
