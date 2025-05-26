#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
# sys.path.append(os.path.dirname(__file__))

import pandas as pd
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

output_header = ["���YID","COBOL_ID","�����Ώ�PGM��","�����f�[�^����","�����Y�s���","PARM_ALL",\
                "�������R�[�h�@","�������R�[�h�A","�������R�[�h�B","�������R�[�h�C","�������R�[�h�D","�p�����[�^","CRUD����","IO����",\
                "�֘ADSN","�֘A���ݒ�","PGM-IO","JCL_PGM_DSN","�֘APGM�i�e�܂ށj","�⑫","JSI�pXDBREF"
]

vbLf = "\n"

DB�����o�^��PARM = "�����ݒ�iJFE_DB����j" 
�֘A���Y = ""
JFE_���R�[�h�֘A�����ʒu = 0
���������� = []
JFE_�֘ADSN����_ = None
���p_�ڋq��_���Y�֘A�����_INSERT_FOR_COBOL_ = None
���p_�ڋq��_PGM_IO���_ = None
�ڋq��_JCL_PGM_DSN_BMCP�ȊO_ = None
QRY_JCL_PGM_DSN_BMCP_ = None
���p_�ڋq��_JCL_PGM_DSN_FOR_DB_JFE_ = None

ActSheet = []
ActSheet_x = []
DD_CNT = 0
���YID = ""
COBOL_ID = ""
�֘A���Y = ""
JFE_�f�[�^���� = ""
JFE_DSN = ""
JFE_�������R�[�h = ""
JFE_�������R�[�h1 = ""
JFE_�������R�[�h2 = ""
JFE_�������R�[�h3 = ""
JFE_�������R�[�h4 = ""
JFE_�������R�[�h5 = ""
JFE_CRUD���� = ""
JFE_IO���� = ""
�ďo���@ = ""
����PGM = ""
IO���� = ""
JFE_�֘ADSN = ""
#'20240215 ADD qian.e.wang
����_�֘ADSN = []
#'ADD END
�֘A�f�[�^ = ""

LIBRARY_ID = ""
JCL_NAME = ""
JOB_SEQ = ""
JOB_ID = ""
STEP_SEQ = ""
STEP_ID = ""
PGM_NAME = ""
PROC_NAME = ""
SYSIN_PGM = ""
����DD = ""
�ǉ�DSN = ""

# �^����ꂽ�����Ɋ�Â��Ċ֘ADSN�i�f�[�^�Z�b�g���j�����
class JFE_�֘ADSN����:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�y�b��zJFE_DATA�֘A���ݒ�"
        # self.db_path = db_path

    def setup(self):
        
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for type,id,dsn in zip(df["�f�[�^����"],df["�f�[�^ID"],df["DSN"]):
            if (type,id) not in self.dic:
#'20240215 UPD qian.e.wang
            #    self.dic[(type,id)] = dsn
                self.dic[(type, id)] = []
            self.dic[(type, id)].append(dsn)
#'UPD END
        
    def get(self):
        global JFE_�f�[�^����,JFE_�������R�[�h
        
        if self.dic == None:
            self.setup()
        
        if (JFE_�f�[�^����,JFE_�������R�[�h) in self.dic:
#'20240215 UPD qian.e.wang
        #    JFE_�֘ADSN = JFE_�f�[�^���� + ":" + self.dic[(JFE_�f�[�^����,JFE_�������R�[�h)] + "(" + JFE_�������R�[�h + ")"
            JFE_�֘ADSN = ""
            for dsn in self.dic[(JFE_�f�[�^����, JFE_�������R�[�h)]:
                JFE_�֘ADSN += JFE_�f�[�^���� + ":"
                JFE_�֘ADSN += dsn + "(" + JFE_�������R�[�h + ")" + ";"
            return JFE_�֘ADSN
        else:
        #    JFE_�֘ADSN = JFE_�f�[�^���� + ":" + JFE_�������R�[�h + "(�ݒ薳)"
            return JFE_�f�[�^���� + ":" + JFE_�������R�[�h + "(�ݒ薳)"
        #return JFE_�֘ADSN

# �^����ꂽ�����Ɋ�Â��Ĕ���IO�����
class JFE_����IO����:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�y�b��zJFE_DATA�֘A���ݒ�"
        # self.db_path = db_path

    def setup(self):
        
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for type,id,dsn,io in zip(df["�f�[�^����"],df["�f�[�^ID"],df["DSN"],df["IO����"]):
            if (type,id,dsn) not in self.dic:
                self.dic[(type, id, dsn)] = []
            self.dic[(type, id, dsn)].append(io)

    def get(self):
        global JFE_�f�[�^����,JFE_�������R�[�h,JFE_DSN
        
        if self.dic == None:
            self.setup()
        
        # DEBUG
        # print("���A JFE_�������R�[�h :["+str(JFE_�������R�[�h)+"] JFE_DSN :["+str(JFE_DSN)+"]\r\n")
        
        if (JFE_�f�[�^����,JFE_�������R�[�h,JFE_DSN) in self.dic:
            IO���� = ""
            for io in self.dic[(JFE_�f�[�^����,JFE_�������R�[�h,JFE_DSN)]:
                if IO���� == "":
                    IO���� = io
                elif io == "NA":
                    pass
                else:
                    if IO���� == io:
                        pass
                    else:
                        IO���� = "I-O"
            # DEBUG
            # print("���A IO���� :["+str(IO����)+"]\r\n")
            return IO����
        else:
            return ""
#'UPD END


# COBOL�v���O�����Ɋ֘A���鎑�Y�̏����f�[�^�x�[�X�ɑ}��
class ���p_�ڋq��_���Y�֘A�����_INSERT_FOR_COBOL:
    
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�ڋq��_���Y�֘A�����"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for from_source,type,to_source in zip(df["�ďo�����Y"],df["�ďo���@"],df["�ďo�掑�Y"]):
            self.dic[(from_source,type,to_source)] = 1
    
        
    def insert(self):
        if self.dic == None:
            self.setup()
            
        global COBOL_ID,�ďo���@,����PGM
        global DB�����o�^��PARM
        if (COBOL_ID,�ďo���@,����PGM) in self.dic:
            return False
        
        key_list = ["�ďo�����Y","�ďo���@","�ďo�掑�Y","�o�^����"]
        value_list = [COBOL_ID,�ďo���@,����PGM,DB�����o�^��PARM]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        self.dic[(COBOL_ID,�ďo���@,����PGM)] = 1
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
    
 
class ���p_�ڋq��_JCL_PGM_DSN_FOR_DB_JFE:
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
        df.fillna("",inplace=True)
        
        for jcl,job,step,dd,dsn in zip(df["JCL_NAME"],df["JOB_SEQ"],df["STEP_SEQ"],df["DD_NAME"],df["DSN"]):
            self.dic[(jcl,job,step,dd,dsn)] = 1
    
        
    def insert(self):
        if self.dic == None:
            self.setup()
            
        global DB�����o�^��PARM
        global LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME,PROC_NAME,SYSIN_PGM,����DD,�ǉ�DSN,����PGM
        if (JCL_NAME,JOB_SEQ,STEP_SEQ,����DD,�ǉ�DSN) in self.dic:
            return False

        key_list = ["LIBRARY_ID","JCL_NAME","JOB_SEQ","JOB_ID","STEP_SEQ","STEP_NAME","PGM_NAME","PROC_NAME","SYSIN_PGM","DD_NAME","DSN","�蓮�X�VFLG","�����X�VFLG"]
        value_list = [LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME,PROC_NAME,SYSIN_PGM,����DD,�ǉ�DSN,"",DB�����o�^��PARM]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ,����DD,�ǉ�DSN)] = 1
        
   
        ### �ڋq��_JCL_PGM_DSN���X�V����̂� �ڋq��_JCL_PGM_DSN_BMCP�ȊO��dic ���X�V����
        global �ڋq��_JCL_PGM_DSN_BMCP�ȊO_
        temp_dic = {key:value for key,value in zip(key_list,value_list)}
        pgm_name = temp_dic["PGM_NAME"]
        if pgm_name not in �ڋq��_JCL_PGM_DSN_BMCP�ȊO_.dic:
            �ڋq��_JCL_PGM_DSN_BMCP�ȊO_.dic[pgm_name] = []
        �ڋq��_JCL_PGM_DSN_BMCP�ȊO_.dic[pgm_name].append(temp_dic)
        
        sysin_pgm = temp_dic["SYSIN_PGM"]
        if sysin_pgm not in �ڋq��_JCL_PGM_DSN_BMCP�ȊO_.dic:
            �ڋq��_JCL_PGM_DSN_BMCP�ȊO_.dic[sysin_pgm] = []
        �ڋq��_JCL_PGM_DSN_BMCP�ȊO_.dic[sysin_pgm].append(temp_dic)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
    
    
# �v���O�����̓��o�͏����f�[�^�x�[�X�ɑ}��
class ���p_�ڋq��_PGM_IO���:
    
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�ڋq��_PGM_IO���"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for type, id, io, file in zip(df["���Y����"],df["���YID"],df["���o�͋敪"],df["�t�@�C����"]):
            if type != "COBOL_����":
                continue
            self.dic[(id, io, file)] = 1
    
        
    def insert(self):
        if self.dic == None:
            self.setup()
            
        global ����PGM,IO����,�֘A�f�[�^
        global DB�����o�^��PARM
        if (����PGM,IO����,�֘A�f�[�^) in self.dic:
            return False
        
        key_list = ["���Y����","LIBRARY_ID","���YID","���o�͋敪","�t�@�C����"]
        ### 'LIBRARY_ID �͎b��[�u
        
        value_list = ["COBOL_����","TEST",����PGM,IO����,�֘A�f�[�^]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        self.dic[(����PGM,IO����,�֘A�f�[�^)] = 1
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
    
# ����̏���������JCL�APGM�ADSN�̏�������
class �ڋq��_JCL_PGM_DSN_BMCP�ȊO:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�ڋq��_JCL_PGM_DSN"
        self.key_list = ["LIBRARY_ID","JCL_NAME","JOB_SEQ","JOB_ID","STEP_SEQ","STEP_NAME","PGM_NAME","PROC_NAME","SYSIN_PGM"]
        # self.db_path = db_path

    def setup(self):
        
        self.dic = {}
        sql = "SELECT DISTINCT LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_NAME,PGM_NAME,PROC_NAME,SYSIN_PGM FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        ### ���̏����� distinct �ȃf�[�^�����o��
        
        
        ###
        
        for i in range(len(df)):
            data = df.iloc[i]
            temp_dic = {key:data[key] for key in self.key_list}
            pgm_name = temp_dic["PGM_NAME"]
            if pgm_name not in self.dic:
                self.dic[pgm_name] = []
            self.dic[pgm_name].append(temp_dic)
            
            sysin_pgm = temp_dic["SYSIN_PGM"]
            if sysin_pgm not in self.dic:
                self.dic[sysin_pgm] = []
            self.dic[sysin_pgm].append(temp_dic)
        
        
    def get(self):
        global ����PGM
        
        if self.dic == None:
            self.setup()
                
        if ����PGM in self.dic:
            return self.dic[����PGM]
        
        else:
            return []
            
# ����̏����i�����炭BMCP�Ɋ֘A����j������JCL�APGM�ADSN�̏�������
class QRY_JCL_PGM_DSN_BMCP:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "QRY_JCL_PGM_DSN_BMCP"
        self.key_list = ["BMCP_PGM","LIBRARY_ID","JCL_NAME","JOB_SEQ","JOB_ID","STEP_SEQ","STEP_NAME","PGM_NAME","PROC_NAME","SYSIN_PGM"]
        # self.db_path = db_path

    def setup(self):
        
        self.dic = {}
        sql = "SELECT DISTINCT LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_NAME,PGM_NAME,PROC_NAME,SYSIN_PGM,BMCP_PGM FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        keys = df.columns.tolist()
        df.sort_values(keys,inplace=True)

        for i in range(len(df)):
            data = df.iloc[i]
            temp_dic = {key:data[key] for key in self.key_list[1:]}
            bmcp_pgm = data["BMCP_PGM"]
            if bmcp_pgm not in self.dic:
                self.dic[bmcp_pgm] = []
            self.dic[bmcp_pgm].append(temp_dic)
            
        
    def get(self):
        global ����PGM
        
        if self.dic == None:
            self.setup()
                
        if ����PGM in self.dic:
            return self.dic[����PGM]
        
        else:
            return []
            
   
   
#�֐��̒�`:BMCP�ȊO����
def BMCP�ȊO����():
    global �ڋq��_JCL_PGM_DSN_BMCP�ȊO_,���p_�ڋq��_JCL_PGM_DSN_FOR_DB_JFE_
    global ����PGM, DD_CNT,�֘A�f�[�^
    global LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME,PROC_NAME,SYSIN_PGM,����DD,�ǉ�DSN
    
    DD_CNT = 0

    df = �ڋq��_JCL_PGM_DSN_BMCP�ȊO_.get()
    lis = []
    
    ### get �Ńf�[�^�̏d�������邽�߁A�d�����폜����
    for data in df:
        LIBRARY_ID = data["LIBRARY_ID"]
        JCL_NAME = data["JCL_NAME"]
        JOB_SEQ = data["JOB_SEQ"]
        JOB_ID = data["JOB_ID"]
        STEP_SEQ = data["STEP_SEQ"]
        STEP_ID = data["STEP_NAME"]
        PGM_NAME = data["PGM_NAME"]
        PROC_NAME = data["PROC_NAME"]
        SYSIN_PGM = data["SYSIN_PGM"]
        lis.append((LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME,PROC_NAME,SYSIN_PGM))
    df = set(lis)
    
    ################################################
    
    for data in df:
     
        LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME,PROC_NAME,SYSIN_PGM = data
                            
        ����DD = "_SYSJ001"                # '�������Ⴄ
        �ǉ�DSN = �֘A�f�[�^
    
        if ���p_�ڋq��_JCL_PGM_DSN_FOR_DB_JFE_.insert() == False:
            pass
        else:
            DD_CNT = DD_CNT + 1
        
#�֐��̒�`:BMCP����
def BMCP����():    
    global QRY_JCL_PGM_DSN_BMCP_,���p_�ڋq��_JCL_PGM_DSN_FOR_DB_JFE_
    global ����PGM, DD_CNT,�֘A�f�[�^
    global LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME,PROC_NAME,SYSIN_PGM,����DD,�ǉ�DSN


    df = QRY_JCL_PGM_DSN_BMCP_.get()
    for data in df:
        
        # 'LIBRARY_ID = data["LIBRARY_ID"]
        LIBRARY_ID = data["LIBRARY_ID"]
        JCL_NAME = data["JCL_NAME"]
        JOB_SEQ = data["JOB_SEQ"]
        JOB_ID = data["JOB_ID"]
        STEP_SEQ = data["STEP_SEQ"]
        STEP_ID = data["STEP_NAME"]
        PGM_NAME = data["PGM_NAME"]
        PROC_NAME = data["PROC_NAME"]
        SYSIN_PGM = data["SYSIN_PGM"]
                            
        ����DD = "_SYSB001"                # '�������Ⴄ
        �ǉ�DSN = �֘A�f�[�^
    
        if ���p_�ڋq��_JCL_PGM_DSN_FOR_DB_JFE_.insert() == False:
            pass
        else:
            DD_CNT = DD_CNT + 1
                                     
#�֐��̒�`: ����̏����Ɋ�Â��ăf�[�^�x�[�X���X�V���邽�߂̊֐�
#'20240215 UPD qian.e.wang
#def �e��o�^DB�X�V(P_���s�J�E���g,ActSheet_x):
def �e��o�^DB�X�V(P_���s�J�E���g,ActSheet_x,JFE_�֘ADSN):
#    global JFE_�֘ADSN����_,���p_�ڋq��_���Y�֘A�����_INSERT_FOR_COBOL_,���p_�ڋq��_PGM_IO���_
    global JFE_����IO����_,���p_�ڋq��_���Y�֘A�����_INSERT_FOR_COBOL_,���p_�ڋq��_PGM_IO���_
#    global ���YID,COBOL_ID,�֘A���Y,JFE_�f�[�^����,JFE_�������R�[�h,JFE_CRUD����,JFE_IO����,DD_CNT,�ďo���@,����PGM,IO����,JFE_�֘ADSN,�֘A�f�[�^
    global ���YID,COBOL_ID,�֘A���Y,JFE_�f�[�^����,JFE_�������R�[�h,JFE_CRUD����,JFE_IO����,DD_CNT,�ďo���@,����PGM,IO����,�֘A�f�[�^,JFE_DSN
#'UPD END
    
    if JFE_�f�[�^���� != "" and JFE_�������R�[�h != "":
        
#'20240215 DEL qian.e.wang
#        if  "-" in JFE_�������R�[�h:
#            JFE_�֘ADSN = "�ϐ��l�v�m�F"
#        else:
#            JFE_�֘ADSN = JFE_�֘ADSN����_.get()
#'DEL END
           
        #    '===�b��Ή��i�֘A���ݒ肳���܂Łj===
        #    'if JFE_�֘ADSN = "�ݒ薳":
        #    '   JFE_�֘ADSN = JFE_�������R�[�h + "(�m�F��)"
        #    'End If
        #    '======================================
        
        if ActSheet_x[15] == "":
            ActSheet_x[15] = JFE_�֘ADSN
        else:
            ActSheet_x[15] = ActSheet_x[15] + vbLf + JFE_�֘ADSN
        
           #2-2 ���Y�֘A�����o��
        DD_CNT = 0
           
        if COBOL_ID != "":
            if JFE_CRUD���� != "" and JFE_CRUD���� != "NA":
                if JFE_�f�[�^���� == "DAM":
                    �ďo���@ = "COBOL-DAM-" + JFE_CRUD����
                    ����PGM = JFE_�֘ADSN                       #'�����̏����́u����PGM�v�͌ďo��PGM�@����̏ꍇ�̓f�[�^
                if JFE_�f�[�^���� == "�Ǝ�DAM":
                    �ďo���@ = "COBOL-DAM-" + JFE_CRUD����
                    ����PGM = JFE_�֘ADSN                       #'�����̏����́u����PGM�v�͌ďo��PGM�@����̏ꍇ�̓f�[�^
                if JFE_�f�[�^���� == "NDB":
                    �ďo���@ = "COBOL-NDB-" + JFE_CRUD����
                    ����PGM = JFE_�������R�[�h
#'20240213 ADD qian.e.wang
                if JFE_�f�[�^���� == "ADABAS":
                    �ďo���@ = "COBOL-ADABAS-" + JFE_CRUD����
                    ����PGM = JFE_�������R�[�h
                if JFE_�f�[�^���� == "DB2":
                    �ďo���@ = "COBOL-DB2-" + JFE_CRUD����
                    ����PGM = JFE_�������R�[�h
#'END ADD
#'20240611 ADD qian.e.wang ���쌧�M�e�X�gIO�o�͑Ή�
                if JFE_�f�[�^���� == "SUP":
                    �ďo���@ = "COBOL-SUP-" + JFE_CRUD����
                    ����PGM = JFE_�������R�[�h
#'ADD END
                if JFE_�f�[�^���� == "�":
                    �ďo���@ = "COBOL-�"
                    ����PGM = JFE_�֘ADSN
           
                if ���p_�ڋq��_���Y�֘A�����_INSERT_FOR_COBOL_.insert() == False:
                    ActSheet_x[16] = "����SKIP"
                else:
                    #'ActSheet_x[16] = ActSheet_x[16] + 1
                    DD_CNT = DD_CNT + 1
        else:
            ActSheet_x[16] = "�G���["
        
        #'JSI�pXDBREF��͏���
        if P_���s�J�E���g == 1:
            if ActSheet_x[21] != "":
                �ďo���@ = "COBOL-NDB(JSI)-" + JFE_CRUD����
                ����PGM = ActSheet_x[21]
    
                if ���p_�ڋq��_���Y�֘A�����_INSERT_FOR_COBOL_.insert() == False:
                    ActSheet_x[16] = "����SKIP"
                else:
                    #'ActSheet_x[16] = ActSheet_x[16] + 1
                    DD_CNT = DD_CNT + 1
    
    
        if ActSheet_x[16] == "":
            ActSheet_x[16] = DD_CNT
        else:
            ActSheet_x[16] = str(ActSheet_x[16]) + str(DD_CNT)
        
#            '2-3 �ŏ��PGM����i�o����΃o�b�`�̂݁j
           
# '�������d���׈�U�ۗ�
# '           ����PGM = COBOL_ID   '
# '           Call �ŏ��PGM���   'MHI�Č��̏����𗬗p�A�������W�b�N�́u�ڋq��_���Y�֘A�����v���x�[�X�ɉ�͂���悤�ɉ��C
# '           ����PGM = ""         '���͖h�~�̂��ߏ�����
# '           �֘A�f�[�^ = JFE_�֘ADSN

        #    '2-4 PGM-IO���o��
#'20240213 UPD qian.e.wang
#        if P_���s�J�E���g == 1:
#            IO���� = JFE_IO����
#            ����PGM = COBOL_ID
#            �֘A�f�[�^ = JFE_�֘ADSN
#            if �֘A�f�[�^ != "":
#                if ���p_�ڋq��_PGM_IO���_.insert() == False:
#                    pass
#                else:
#                    ActSheet_x[17] = 1
#        ����PGM = COBOL_ID

        ����PGM = �֘A���Y
        �֘A�f�[�^ = JFE_�֘ADSN
        
        if JFE_�f�[�^���� == "DAM":
            JFE_DSN = �֘A�f�[�^.replace("DAM:", "").replace("(�ݒ薳)", "").replace("(" + ����PGM + ")", "")
        if JFE_�f�[�^���� == "�Ǝ�DAM":
            JFE_DSN = �֘A�f�[�^.replace("�Ǝ�DAM:", "").replace("(�ݒ薳)", "").replace("(" + ����PGM + ")", "")
        if JFE_�f�[�^���� == "NDB":
            JFE_DSN = �֘A�f�[�^.replace("NDB:", "").replace("(�ݒ薳)", "").replace("(" + ����PGM + ")", "")
        if JFE_�f�[�^���� == "ADABAS":
            JFE_DSN = �֘A�f�[�^.replace("ADABAS:", "").replace("(�ݒ薳)", "").replace("(" + ����PGM + ")", "")
        if JFE_�f�[�^���� == "DB2":
            JFE_DSN = �֘A�f�[�^.replace("DB2:", "").replace("(�ݒ薳)", "").replace("(" + ����PGM + ")", "")
#'20240611 ADD qian.e.wang ���쌧�M�e�X�gIO�o�͑Ή�
        if JFE_�f�[�^���� == "SUP":
            JFE_DSN = �֘A�f�[�^.replace("SUP:", "").replace("(�ݒ薳)", "").replace("(" + ����PGM + ")", "")
#'ADD END
        if JFE_�f�[�^���� == "�":
            JFE_DSN = �֘A�f�[�^.replace("�:", "").replace("(�ݒ薳)", "").replace("(" + ����PGM + ")", "")
        
        IO���� = JFE_����IO����_.get()
        if IO���� == "":
            IO���� = JFE_IO����

        if �֘A�f�[�^ != "":
            if ���p_�ڋq��_PGM_IO���_.insert() == False:
                pass
            else:
                ActSheet_x[17] = 1

        # DEBUG
        # print("���B IO���� :["+str(IO����)+"] ����PGM :["+str(����PGM)+"] �֘A�f�[�^ :["+str(�֘A�f�[�^)+"]\r\n")
#'UPD END

        BMCP�ȊO����()

        BMCP����()

        ActSheet_x[18] = DD_CNT

    else:
        if JFE_�f�[�^���� != "" and JFE_�������R�[�h == "":
            ActSheet_x[20] = "CALL���ߕ��@�v�m�F"
            
    return ActSheet_x


def analysis2(db_path,title,excel_path):
    global JFE_�֘ADSN����_,���p_�ڋq��_���Y�֘A�����_INSERT_FOR_COBOL_,���p_�ڋq��_PGM_IO���_,�ڋq��_JCL_PGM_DSN_BMCP�ȊO_,QRY_JCL_PGM_DSN_BMCP_,���p_�ڋq��_JCL_PGM_DSN_FOR_DB_JFE_
#'20240215 ADD qian.e.wang
    global JFE_����IO����_
#'ADD END
    global ActSheet, ActSheet_x
    global ���YID,COBOL_ID,�֘A���Y,JFE_�f�[�^����,JFE_�������R�[�h,JFE_CRUD����,JFE_IO����
    
    if os.path.isdir(title) == False:
        os.makedirs(title)
         
        
    start = time.time()
    ### ����DB�폜
    conn = connect_accdb(db_path)
    cursor = conn.cursor()
    
    sql = "SELECT * FROM �ڋq��_���Y�֘A����� WHERE �o�^���� = '�����ݒ�iJFE_DB����j'"
    df = pd.read_sql(sql,conn)
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("�ڋq��_���Y�֘A�����",values,keys)
        cursor.execute(sql,values)

    sql = "SELECT * FROM �ڋq��_JCL_PGM_DSN WHERE �蓮�X�VFLG = '' AND �����X�VFLG = '�����ݒ�iJFE_DB����j'"
    df = pd.read_sql(sql,conn)
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("�ڋq��_JCL_PGM_DSN",values,keys)
        cursor.execute(sql,values)
      
    sql = "SELECT * FROM �ڋq��_PGM_IO��� WHERE ���Y���� = 'COBOL_����'"
    df = pd.read_sql(sql,conn)
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("�ڋq��_PGM_IO���",values,keys)
        cursor.execute(sql,values)
    
    # sql,values = make_delete_sql("�ڋq��_PGM_IO���",["COBOL_����"],["���Y����"])    
    # cursor.execute(sql,values)
    
    # sql,values = make_delete_sql("�ڋq��_JCL_PGM_DSN",["",DB�����o�^��PARM],["�蓮�X�VFLG","�����X�VFLG"])
    # cursor.execute(sql,values)
    
    # sql,values = make_delete_sql("�ڋq��_���Y�֘A�����",[DB�����o�^��PARM],["�o�^����"])
    # cursor.execute(sql,values)
    
    conn.commit()
    print("DB�폜����", time.time()-start)
    
    ## CRUD����� "NA" �Ƃ���Ă���ӏ���pandas���� nan �ɂȂ��Ă��܂����߁A "NA" �̃P�[�X�������O����B
    na_values = ["", 
             "#N/A", 
             "#N/A N/A", 
             "#NA", 
             "-1.#IND", 
             "-1.#QNAN", 
             "-NaN", 
             "-nan", 
             "1.#IND", 
             "1.#QNAN", 
             "<NA>", 
             "N/A", 
#              "NA", 
             "NULL", 
             "NaN", 
             "n/a", 
             "nan", 
             "null"
             ]

    df = pd.read_excel(excel_path,sheet_name="JFE_DB���p������",na_values=na_values,keep_default_na=False)
    df.fillna("",inplace=True)

    
    JFE_�֘ADSN����_ = JFE_�֘ADSN����(conn,cursor)
    ���p_�ڋq��_���Y�֘A�����_INSERT_FOR_COBOL_ = ���p_�ڋq��_���Y�֘A�����_INSERT_FOR_COBOL(conn,cursor)
    ���p_�ڋq��_PGM_IO���_ = ���p_�ڋq��_PGM_IO���(conn,cursor)
    �ڋq��_JCL_PGM_DSN_BMCP�ȊO_ = �ڋq��_JCL_PGM_DSN_BMCP�ȊO(conn,cursor)
    QRY_JCL_PGM_DSN_BMCP_ = QRY_JCL_PGM_DSN_BMCP(conn,cursor)
    ���p_�ڋq��_JCL_PGM_DSN_FOR_DB_JFE_ = ���p_�ڋq��_JCL_PGM_DSN_FOR_DB_JFE(conn,cursor)
    
    ActSheet = []
#'20240215 ADD qian.e.wang
    ����_�֘ADSN = []
    JFE_����IO����_ = JFE_����IO����(conn,cursor)
#'ADD END
    
    for i in range(len(df)):
        data = df.iloc[i]
        ActSheet_x = [""]+list(data)
        ���YID = ActSheet_x[1]
        COBOL_ID = ActSheet_x[2]
        �֘A���Y = ActSheet_x[3]
        JFE_�f�[�^���� = ActSheet_x[4]
        JFE_�������R�[�h_1_5 = ActSheet_x[7:12]
        JFE_CRUD���� = ActSheet_x[13]
        JFE_IO���� = ActSheet_x[14]

        for i in range(5):
            if JFE_�������R�[�h_1_5[i] != "":
                JFE_�������R�[�h = JFE_�������R�[�h_1_5[i]
#'20240215 UPD qian.e.wang
#                ActSheet_x = �e��o�^DB�X�V(i+1,ActSheet_x)
                if  "-" in JFE_�������R�[�h:
                    JFE_�֘ADSN = "�ϐ��l�v�m�F"
                    ActSheet_x = �e��o�^DB�X�V(i+1,ActSheet_x,JFE_�֘ADSN)
                    
                    ActSheet.append(ActSheet_x)
                else:
                    JFE_�֘ADSN = ""
                    ����_�֘ADSN = JFE_�֘ADSN����_.get().split(";")
                    for j in range(len(����_�֘ADSN)):
                        JFE_�֘ADSN = ����_�֘ADSN[j]

                        ActSheet_x = [""]+list(data)
                        ���YID = ActSheet_x[1]
                        COBOL_ID = ActSheet_x[2]
                        �֘A���Y = ActSheet_x[3]
                        JFE_�f�[�^���� = ActSheet_x[4]
                        JFE_�������R�[�h_1_5 = ActSheet_x[7:12]
                        JFE_CRUD���� = ActSheet_x[13]
                        JFE_IO���� = ActSheet_x[14]

                        # DEBUG
                        # print("���@ JFE_�f�[�^���� :["+str(JFE_�f�[�^����)+"] JFE_�������R�[�h :["+str(JFE_�������R�[�h)+"]  JFE_�֘ADSN :["+str(JFE_�֘ADSN)+"]\r\n")

                        if JFE_�֘ADSN != "":
                            ActSheet_x = �e��o�^DB�X�V(i+j+1,ActSheet_x,JFE_�֘ADSN)
                            ActSheet.append(ActSheet_x)
            else:
                ActSheet.append(ActSheet_x)

#        ActSheet.append(ActSheet_x)
#'UPD END
        
    ActSheet_all = [actSheet[1:] for actSheet in ActSheet]
    print("��͊���", time.time()-start)
    write_excel_multi_sheet("JFE-DB���p�ӏ�����2.xlsx",ActSheet_all,"JFE_DB���p������",title,output_header)
    
    conn.close()
    
    # return ActSheet
        
        
        
# analysis2(sys.argv[1],sys.argv[2],sys.argv[3])
