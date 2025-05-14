#!/usr/bin/env python
# -*- coding: cp932 -*-

import os
import re
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


SUB_SQL����_JCL_1_ = None
SUB_SQL����_JCL_3_ = None
SUB_SQL����_JCL_4_ = None



def reset_all():
    global ���C�u����ID,�t�@�C����,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_NAME,STEP_PGM,STEP_PROC,DD_NAME,SYSIN_SEQ,SYSIN_LINE, \
            PROC_ID,JCL����,JOB_�R�����g,JOB_CLASS,JOB_MSGCLASS,JOB_MSGLEVEL,JOB_COND,�����s������,���͍sTYPE,�sCHK,CMD_SEQ,�����Y�s,\
            DD_DSN,DD_GDG,DD_SYSIN,DD_DISP,DD_SYSOUT,DD_WRITER,DD_FORM,DD_UNIT,DD_SPACE,DD_RECFM,DD_LRECL,DD_BLKSIZE,DD_VOL,DD_LABEL,DD_AAUTO����,\
            PGM_CMD_����,DB�o�͔���_JCL1,re_flg,STEP_PARM1,STEP_PARM2
            
    ���C�u����ID = ""
    �t�@�C���� = ""
    JOB_SEQ = 0
    JOB_ID = ""
    STEP_SEQ = 0
    STEP_NAME = ""
    STEP_PGM = ""
    STEP_PROC = "" 
    DD_NAME = "" 
    SYSIN_SEQ = 0
    SYSIN_LINE = ""

    PROC_ID = ""
    JCL���� = ""
    JOB_�R�����g = ""
    JOB_CLASS = ""
    JOB_MSGCLASS = ""
    JOB_MSGLEVEL = ""
    JOB_COND = ""

    �����s������ = ""
    ���͍sTYPE = ""
    �sCHK = False
    CMD_SEQ = 0
    �����Y�s = 0

    DD_DSN = ""
    DD_GDG = ""
    DD_SYSIN = ""
    DD_DISP = ""
    DD_SYSOUT = ""
    DD_WRITER = ""
    DD_FORM = ""
    DD_UNIT = ""
    DD_SPACE = ""
    DD_RECFM = ""
    DD_LRECL = ""
    DD_BLKSIZE = ""
    DD_VOL = ""
    DD_LABEL = ""
    DD_AAUTO���� = ""  # '2020/4/14 ADD
    PGM_CMD_���� = False
    DB�o�͔���_JCL1 = False
    re_flg = False

    STEP_PARM1 = ""
    STEP_PARM2 = ""
    
    
class SUB_SQL����_JCL_1:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�@JCL_��{���"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
    def insert(self):
        if self.dic == None:
            self.setup()
            
        global �t�@�C����,���C�u����ID,JOB_SEQ ,JOB_ID,PROC_ID,JCL����,JOB_�R�����g,JOB_CLASS,JOB_MSGCLASS,JOB_MSGLEVEL,JOB_COND
  
        key_list = ["JCL��","LIBRARY_ID","JOB_SEQ","JOB_ID","PROC_ID","JCL����","JOB_�R�����g","CLASS","MSGCLASS","MSGLEVEL","COND" ]
        value_list = [�t�@�C����,���C�u����ID,JOB_SEQ ,JOB_ID,PROC_ID,JCL����,DB����(JOB_�R�����g),JOB_CLASS,JOB_MSGCLASS,JOB_MSGLEVEL,JOB_COND]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
        

class SUB_SQL����_JCL_2:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�@JCL_STEP_SYSIN"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
    def insert(self):
        if self.dic == None:
            self.setup()
            
        global ���C�u����ID,�t�@�C����,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_NAME,STEP_PGM,STEP_PROC, DD_NAME, SYSIN_SEQ,SYSIN_LINE

        # ADD 20240618 yi.a.qian
        # PROC_NAME Setting
        # if JOB_SEQ == 0:
        #     if STEP_PROC == "":
        #         global PROC_ID
        #         STEP_PROC = PROC_ID
        # ADD END
        key_list = ["LIBRARY_ID","JCL_NAME","JOB_SEQ","JOB_ID","STEP_SEQ","STEP_ID","PGM_NAME","PROC_NAME","SYSIN_PGM","SYSIN_DD","SYSIN_SEQ","SYSIN"]
        value_list = [���C�u����ID,�t�@�C����,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_NAME,STEP_PGM,STEP_PROC,"", DD_NAME, SYSIN_SEQ,DB����(SYSIN_LINE)]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()



class SUB_SQL����_JCL_3:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�@JCL_STEP���"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
    def insert(self):
        if self.dic == None:
            self.setup()
            
        global ���C�u����ID,�t�@�C����,JOB_SEQ, JOB_ID,PROC_ID,STEP_SEQ,STEP_NAME,STEP_PGM,STEP_PROC,STEP_PARM1,STEP_PARM2

        STEP_SEQ += 1
        # ADD 20240618 yi.a.qian
        # PROC_NAME Setting
        # if JOB_SEQ == 0:
        #     if STEP_PROC == "":
        #         # global PROC_ID
        #         STEP_PROC = PROC_ID
        # ADD END
        key_list = ["LIBRARY_ID","JCL_NAME","JOB_SEQ","JOB_ID","PROC_ID","STEP_SEQ","STEP_NAME","PGM_NAME","PROC_NAME","PARM_VAR_LIST","PARM_VALUE_LIST"]
        value_list = [���C�u����ID,�t�@�C����,JOB_SEQ, JOB_ID,PROC_ID,STEP_SEQ,STEP_NAME,STEP_PGM,STEP_PROC,STEP_PARM1,DB����(STEP_PARM2)]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
        
        
class SUB_SQL����_JCL_4:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�@JCL_PGM_DSN"
        # self.db_path = db_path
        
    def setup(self):
        self.dic = {}
        
    def insert(self):
        if self.dic == None:
            self.setup()
            
        global ���C�u����ID,�t�@�C����,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_NAME,STEP_PGM,STEP_PROC,DD_NAME,DD_DSN,DD_GDG,DD_AAUTO����,DD_SYSIN,DD_DISP,DD_SYSOUT,DD_WRITER,DD_FORM,DD_UNIT,DD_SPACE,DD_RECFM,DD_LRECL,DD_BLKSIZE,DD_VOL,DD_LABEL
        
        # ADD 20240618 yi.a.qian
        # PROC_NAME Setting
        # if JOB_SEQ == 0:
        #     if STEP_PROC == "":
        #         global PROC_ID
        #         STEP_PROC = PROC_ID
        # ADD END
        key_list = ["LIBRARY_ID","JCL_NAME","JOB_SEQ","JOB_ID","STEP_SEQ","STEP_NAME","PGM_NAME","PROC_NAME","SYSIN_PGM","DD_NAME","DSN","GDG","SYSIN","DISP","SYSOUT","WRITER","FORM","UNIT","SPACE_Q","DCB_RECFM","DCB_LRECL","DCB_BLKSIZE","VOL","LABEL"]
        value_list = [���C�u����ID,�t�@�C����,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_NAME,STEP_PGM,STEP_PROC,"",DD_NAME,DD_DSN,DD_GDG + DD_AAUTO����,DD_SYSIN,DD_DISP,DD_SYSOUT,DD_WRITER,DD_FORM,DD_UNIT,DD_SPACE,DD_RECFM,DD_LRECL,DD_BLKSIZE,DD_VOL,DD_LABEL]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
       
        
class SUB_SQL����_JCL_5:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�@JCL_CMD���"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
    def insert(self):
        if self.dic == None:
            self.setup()
            
        global �t�@�C����,JOB_SEQ,JOB_ID,L_STEP_SEQ,STEP_NAME,STEP_PGM,STEP_PROC,DD_NAME,CMD_SEQ,�����Y�s,���͍sTYPE,�����s������,�sCHK
        
        if ���͍sTYPE == "EXEC":
           L_STEP_SEQ = STEP_SEQ + 1
        else:
           L_STEP_SEQ = STEP_SEQ

        CMD_SEQ = CMD_SEQ + 1
        # ADD 20240618 yi.a.qian
        # PROC_NAME Setting
        # if JOB_SEQ == 0:
        #     if STEP_PROC == "":
        #         global PROC_ID
        #         STEP_PROC = PROC_ID
        # ADD END
        key_list = ["���YID","JOB_SEQ","JCL_ID","STEP_SEQ","STEP_NAME","PGM_NAME","PROC_NAME","DD_NAME","CMD_SEQ","�����Y�s���","CMD����","PARM","�sCHK����"]
        value_list = [�t�@�C����,JOB_SEQ,JOB_ID,L_STEP_SEQ,STEP_NAME,STEP_PGM,STEP_PROC,DD_NAME,CMD_SEQ,�����Y�s,���͍sTYPE,�����s������,�sCHK]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()

class SUB_SQL����_JCL_6:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�@PROC_PARM"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
    def insert(self,�J�n��,TokenSheet2_GYO):
        if self.dic == None:
            self.setup()
            
        global �t�@�C����,PROC_ID,JCL����
        
        L_������1 = ""
        L_������2 = ""
        L_������3 = ""
        L_PARM_KEY = ""
        L_PARM_VALUE = ""

        �J�n�� = �J�n�� + 1

        for i in range(�J�n��,len(TokenSheet2_GYO)):
            L_PARM_KEY = ""
            L_PARM_VALUE = ""
            L_������1 = TokenSheet2_GYO[i]
            L_������2 = ""
            if i+1 < len(TokenSheet2_GYO):
                L_������2 = TokenSheet2_GYO[i + 1]
            L_������3 = ""
            if i+2 < len(TokenSheet2_GYO):
                L_������3 = TokenSheet2_GYO[i + 2]
            
            
            if L_������1 != "" and L_������2 == "=":
            
                L_PARM_KEY = L_������1
                if L_������3 == "," or L_������3 == "":
                    L_PARM_VALUE = ""
                else:
                    L_PARM_VALUE = L_������3.replace("'", "")
  
                key_list = ["���YID","PROC_ID","PROC_TYPE","PARM_KEY","PARM_VALUE"]
                value_list = [�t�@�C����,PROC_ID,JCL����,L_PARM_KEY,L_PARM_VALUE]
                
                sql,value = make_insert_sql(self.dbname,value_list,key_list)
                
                self.cursor.execute(sql,value)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
        
class SUB_SQL����_����_1:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "����_���Y���_�֘A���"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
    def insert(self,info1, lib2, id3, row4 , key5, hit6):
        if self.dic == None:
            self.setup()
            
  
        key_list = ["���ރL�[","LIBRARY_ID","���YID","�ŏI�s�ԍ�","�ݒ���L�[","���Y�s���"]
        value_list = [info1, lib2, id3, row4 , key5, hit6]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
    
class SUB_SQL����_����_2:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "����_���Y���_NG���"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
    def insert(self,info1, lib2, id3, row4 , str5):
        if self.dic == None:
            self.setup()
            
  
        key_list = ["���s����","LIBRARY_ID","���YID","�ŏI�s�ԍ�","���Y�s���"]
        value_list = [info1, lib2, id3, row4 , str5]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
          
    
def �ݒ�l���l�`�F�b�N(parm_str):
    
    if IsNumeric(parm_str):
        return  "���l"
    else:
        return "������"

def �ݒ�l�\���ȊO�`�F�b�N(parm_str):

    #'CHECK�Ώۂ̗\�����w��@�@�Ƃ肠�����͕��R�ʉ^��JOB���Ή�
    if parm_str in ("CLASS ","MSGCLASS "):
        return False
    else:
        return True

def �ݒ�l�^�C�v�`�F�b�N(parm_str):

    if "'" in str(parm_str):
       return "�萔"
    else:
        return "�ϐ�"

def �ݒ�l��v�`�F�b�N(parm_val,code_val):
    
    parm_val,code_val = str(parm_val),str(code_val)
    Rtn_Cd = False
    �ݒ�l�^�C�v = �ݒ�l�^�C�v�`�F�b�N(code_val)
    
    #'�ϐ�_�\���ȊO                                    '20140226ADD
    if parm_val == "�ϐ�_�\���ȊO" and \
       �ݒ�l�\���ȊO�`�F�b�N(code_val) and \
       �ݒ�l�^�C�v== "�ϐ�":
       return  True
    #'�ϐ�
    elif "�ϐ�" in parm_val and \
       �ݒ�l�^�C�v == "�ϐ�":
       return True
    #'�萔
    elif "�萔" in parm_val and \
       �ݒ�l�^�C�v == "�萔":
       return True
    #'���l
    elif "���l" in parm_val and \
       �ݒ�l���l�`�F�b�N(code_val) == "���l":
       return True
    #'DSN��
    elif "DSN��" in parm_val and \
       �ݒ�l�^�C�v == "�ϐ�":
       return True
    #'PGM��
    elif "PGM��" in parm_val and \
       �ݒ�l�^�C�v == "�ϐ�":
       return True
    #'PROC��
    elif "PROC��" in parm_val and \
       �ݒ�l�^�C�v== "�ϐ�":
       return True
    #'MACRO��
    elif "MACRO��" in parm_val and \
       �ݒ�l�^�C�v== "�ϐ�":
        if "MACRO_" in code_val:
           return True
        else:
           return False
       
    #'SYSIN��
    elif "SYSIN��" in parm_val and \
       �ݒ�l�^�C�v == "�ϐ�":
       return True
    #'�\���i��L�����ȊO�j
    elif parm_val == code_val:
       return True
    else:
       return False
    
    return Rtn_Cd


def �����s�����񐶐�����(TokenSheet_str):

    TokenSheet_str = [str(s) for s in TokenSheet_str if s != "'"]
    �����s������ = " ".join(TokenSheet_str)
    return DB����(�����s������)

  
def DISP�ϊ�(STR):
    if STR == "SHR":
        return "S"
    elif STR == "RNW":
        return "R"
    elif STR == "NEW":
        return "N"
    elif STR == "CATLG":
        return "C"
    elif STR == "DELETE":
        return "D"
    elif STR == "KEEP":
        return "K"
    elif STR == "OLD":
        return "O"
    elif STR == "PASS":
        return "P"
    elif STR == "MOD":
        return "M"
    elif STR == ",":
        return ""
    elif STR == "(":
        return ""
    elif STR == ")":
        return "END"
    else:
        return "END"

    return ""

def �ݒ�l��v�F��������(parm_val,code_val,dd_name_cand):
    ### �Z���̐F�����͑�ςɂȂ�̂�python�łł͈�U��߂�

    global re_flg,DD_DSN,STEP_PGM,STEP_PROC,DD_SYSIN
    global JOB_�R�����g,JOB_CLASS,JOB_MSGCLASS,JOB_MSGLEVEL,JOB_MSGLEVEL,JOB_COND
    global DD_GDG,DD_DISP,DD_SYSOUT,DD_NAME,DD_WRITER,DD_UNIT,DD_SPACE,DD_RECFM,DD_LRECL,DD_BLKSIZE,DD_VOL,DD_LABEL,DD_FORM
# 'ADD(20111128-takei)
#     '���K�\��
    if re_flg:
        pass
#        TokenSheet2_GYO[������ + i).Select
#        �Z���F���� ("�Z��")
# 'ADD END(����elif �� else���O��)
#     '�ϐ�
    elif "�ϐ�" in parm_val:
        pass
    #    TokenSheet2_GYO[������ + i).Select
    #    �Z���F���� ("����")
    # '�萔
    elif "�萔" in parm_val: 
        pass
    #    TokenSheet2_GYO[������ + i).Select
    #    �Z���F���� ("�I�����W")
    # '���l
    elif "���l" in parm_val: 
        pass
    #    TokenSheet2_GYO[������ + i).Select
    #    �Z���F���� ("�I�����W")
    # 'DSN��
    elif "DSN��" in parm_val:
    #    TokenSheet2_GYO[������ + i).Select
    #    �Z���F���� ("��")
       
    #    'DD_NAME = TokenSheet2_GYO[2]
        DD_DSN = code_val
       
    # 'PGM��
    elif "PGM��"in parm_val:
    #    TokenSheet2_GYO[������ + i).Select
    #    �Z���F���� ("��")
       
    #    'STEP_NAME = TokenSheet2_GYO[2]
       STEP_PGM = code_val
       
    # 'PROC��
    elif "PROC��" in parm_val:
    #    TokenSheet2_GYO[������ + i).Select
    #    �Z���F���� ("��")
       
    #    'STEP_NAME = TokenSheet2_GYO[2]
       STEP_PROC = code_val
       
    # 'SYSIN��
    elif "SYSIN��" in parm_val:
    #    TokenSheet2_GYO[������ + i).Select
       
       DD_SYSIN = code_val
       
    #    �Z���F���� ("��")
    # '�\���i��L�����ȊO�j
    elif parm_val == code_val:
        pass
    #    TokenSheet2_GYO[������ + i).Select
    #    �Z���F���� ("��")
    # else
    # End if
    
    # '�ϐ��Z�b�g����
    
    # '       elif parm_val ==  "JOB"
    # '            JOB_ID = TokenSheet2_GYO[2]
    if parm_val ==  "�萔_�R�����g":
        JOB_�R�����g = code_val
    elif parm_val ==  "�ϐ�_CLASS":
        JOB_CLASS = code_val
    elif parm_val ==  "�ϐ�_MSGCLASS":
        JOB_MSGCLASS = code_val
    elif parm_val ==  "�ϐ�_MSGLEVEL�@":
        JOB_MSGLEVEL = code_val
    elif parm_val ==  "�ϐ�_MSGLEVEL�A":
        JOB_MSGLEVEL = JOB_MSGLEVEL + "," + code_val
    elif parm_val ==  "�ϐ�_COND�@":
        JOB_COND = code_val
    elif parm_val ==  "�ϐ�_COND�A":
        JOB_COND = JOB_COND + "," + code_val
    elif parm_val ==  "���l_GDG":
        DD_GDG = code_val
    elif parm_val ==  "�ϐ�_DISP�@":
        DD_DISP = DISP�ϊ�(code_val)
    elif parm_val ==  "�ϐ�_DISP�A":
        DD_DISP = DD_DISP + "," + DISP�ϊ�(code_val)
    elif parm_val ==  "�ϐ�_SYSOUT":
        DD_SYSOUT = code_val
        DD_NAME = dd_name_cand
    elif parm_val ==  "�ϐ�_WTR":
        DD_WRITER = code_val
# '           elif parm_val ==  "�ϐ�_FORM"
# '                DD_FORM = code_val
    elif parm_val ==  "�ϐ�_FLASH":
        DD_FORM = code_val
    elif parm_val ==  "�ϐ�_UNIT":
        DD_UNIT = code_val
    # 'UNIT_AFF �p�^���ǉ�
    elif parm_val ==  "�ϐ�_UNITAFF":
        DD_UNIT = "AFF_" + code_val
    elif parm_val ==  "�ϐ�_SPACE�@":
        DD_SPACE = code_val
    elif parm_val ==  "�ϐ�_SPACE�A":
        DD_SPACE = DD_SPACE + "," + code_val
    elif parm_val ==  "�ϐ�_RECFM":
        DD_RECFM = code_val
    elif parm_val ==  "�ϐ�_LRECL":
        DD_LRECL = code_val
    elif parm_val ==  "�ϐ�_BLKSIZE":
        DD_BLKSIZE = code_val
    elif parm_val ==  "�ϐ�_VOL��":
        if DD_VOL == "":
            DD_VOL = code_val
        else:
            DD_VOL = DD_VOL + "," + code_val
        
    # '20140716�ǉ�
    elif parm_val ==  "�ϐ�_LABEL":
        if DD_LABEL == "":
            DD_LABEL = code_val
        else:
            DD_LABEL = DD_LABEL + "," + code_val
    elif parm_val ==  "�萔_LABEL":
        if DD_LABEL == "":
            DD_LABEL = code_val
        else:
            DD_LABEL = DD_LABEL + "," + code_val
    elif parm_val ==  "DUMMY":
        DD_DSN = "DUMMY"
                
     
def PARMLIST����_JCL(TokenSheet2_GYO):
    
         
    global STEP_PARM1,STEP_PARM2
    
    STEP_PARM1 = ""
    STEP_PARM2 = ""

    TokenSheet2_GYO += [""]*10
    #'EXEC���߂���ŏ��́u,�v�܂ł̓X�L�b�v
    tmp_row = 4  #'4��ڂ́uEXEC�v�ł���O��
    while True:
        tmp_row = tmp_row + 1
        if TokenSheet2_GYO[tmp_row] == "," or TokenSheet2_GYO[tmp_row] == "":
            break

    #'PARMLIST�̐���
    if TokenSheet2_GYO[tmp_row] == ",":
        tmp_row = tmp_row + 1
        
        while True:
            # 'MSG = TokenSheet2_GYO[tmp_row] + TokenSheet2_GYO[tmp_row + 1] + TokenSheet2_GYO[tmp_row + 2]
        
            # '�z�肵�Ă���PARM�`���ł���΃��X�g���X�V
            #     'EXEC���߂̃p�����[�^�iCOND=�j�ɂ��Ă͐������O���郍�W�b�N��ǉ�
            if TokenSheet2_GYO[tmp_row] == "COND":
               # '�����X�L�b�v
                return  # '�������ۑ�F�b��I�ɉ�͏������I���iPARMLIST�̕����̋L�q�͊������Ă���z��j
            elif TokenSheet2_GYO[tmp_row] != "" and TokenSheet2_GYO[tmp_row + 1] == "=" and TokenSheet2_GYO[tmp_row + 2] != "":
               # '�ŏ��̒l���ǂ���
                if STEP_PARM1 != "":
                    STEP_PARM1 = STEP_PARM1 + " " + TokenSheet2_GYO[tmp_row]
                    STEP_PARM2 = STEP_PARM2 + " " + TokenSheet2_GYO[tmp_row + 2]
                else:
                    STEP_PARM1 = TokenSheet2_GYO[tmp_row]
                    STEP_PARM2 = TokenSheet2_GYO[tmp_row + 2]
                tmp_row = tmp_row + 4   #'4��
            else:
                tmp_row = tmp_row + 1   #'1��

            if TokenSheet2_GYO[tmp_row] == "":
                break
            
    return 

def DB�o�͔���_JCL(TokenSheet2_GYO):
    global SUB_SQL����_JCL_1_,SUB_SQL����_JCL_3_,SUB_SQL����_JCL_4_
    
    global ���͍sTYPE
    global DD_DSN,DD_GDG,DD_SYSIN,DD_DISP,DD_SYSOUT,DD_WRITER,DD_FORM,DD_UNIT,DD_SPACE,DD_RECFM,DD_LRECL,DD_BLKSIZE,DD_VOL,DD_LABEL,DD_AAUTO����
    global PGM_CMD_����,STEP_SEQ,DB�o�͔���_JCL1
    #'DB�o�͔���(�ϐ��ăZ�b�g�O�ɏo��)
    if ���͍sTYPE == "JOB":
        SUB_SQL����_JCL_1_.insert()
        STEP_SEQ = 0
        DB�o�͔���_JCL1 = True
            
    elif ���͍sTYPE == "PROC":
        SUB_SQL����_JCL_1_.insert()
        STEP_SEQ = 0   #'�����͌��������K�v����
        DB�o�͔���_JCL1 = True
                
    elif ���͍sTYPE == "EXEC":
        # '�������@�Z�R���Č����Ή��@������
        # '�p�����[�^���X�g�̐���
        PARMLIST����_JCL(TokenSheet2_GYO)

        SUB_SQL����_JCL_3_.insert()
        # '�o�͌�ϐ�������
        # 'STEP_NAME = ""    'DD�ŗ��p����
        # 'STEP_PGM = ""     'DD�ŗ��p����
        # 'STEP_SYSIN = ""
        PGM_CMD_���� = ""
    elif ���͍sTYPE == "DD":
        # 'DD_NAME = Name_fld
        SUB_SQL����_JCL_4_.insert()
        # 'DD_NAME = ""
        DD_DSN = ""
        DD_GDG = ""
        DD_SYSIN = ""
        DD_DISP = ""
        DD_SYSOUT = ""
        DD_WRITER = ""
        DD_FORM = ""
        DD_UNIT = ""
        DD_SPACE = ""
        DD_RECFM = ""
        DD_LRECL = ""
        DD_BLKSIZE = ""
        DD_VOL = ""
        DD_LABEL = ""
        DD_AAUTO���� = ""  # '2020/4/14 ADD
                
    
def analysis1_5_structure_JCL(TokenSheet2,JCLSheet,fileName,conn,cursor, �ݒ����HIT���o�� = False,���͏���HIT���o�� = False,�݌v����HIT���o�� = False,�ݒ����HIT_NG���o�� = True):
    global SUB_SQL����_JCL_1_,SUB_SQL����_JCL_3_,SUB_SQL����_JCL_4_
    
    global ���C�u����ID,�t�@�C����,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_NAME,STEP_PGM,STEP_PROC, DD_NAME, SYSIN_SEQ,SYSIN_LINE
    global PROC_ID,JCL����,JOB_�R�����g,JOB_CLASS,JOB_MSGCLASS,JOB_MSGLEVEL,JOB_COND
    global �����s������,���͍sTYPE,�sCHK,CMD_SEQ,�����Y�s,DB�o�͔���_JCL1,ID_fld,Name_fld,CMD_fld,PARM_fld,�sCHK
    global re_flg
    global DD_DSN,DD_GDG,DD_SYSIN,DD_DISP,DD_SYSOUT,DD_WRITER,DD_FORM,DD_UNIT,DD_SPACE,DD_RECFM,DD_LRECL,DD_BLKSIZE,DD_VOL,DD_LABEL,DD_AAUTO����
    global PGM_CMD_����,STEP_PARM1,STEP_PARM2
    
    reset_all()
    
    SUB_SQL����_JCL_1_ = SUB_SQL����_JCL_1(conn,cursor)
    SUB_SQL����_JCL_2_ = SUB_SQL����_JCL_2(conn,cursor)
    SUB_SQL����_JCL_3_ = SUB_SQL����_JCL_3(conn,cursor)
    SUB_SQL����_JCL_4_ = SUB_SQL����_JCL_4(conn,cursor)
    SUB_SQL����_JCL_5_ = SUB_SQL����_JCL_5(conn,cursor)
    SUB_SQL����_JCL_6_ = SUB_SQL����_JCL_6(conn,cursor)
    
    SUB_SQL����_����_1_ = SUB_SQL����_����_1(conn,cursor)
    SUB_SQL����_����_2_ = SUB_SQL����_����_2(conn,cursor)
    

    #�\����̓V�[�g������_JCL
    ��� = 5       #'TokenSheet2�@��|�C���^ 2020/4/14 4��5
    ���2 = 6      # 'JCLSheet�@��|�C���^
   
   
    ALL_chk_ok = True   # '�V�[�g�P�ʂőS�Ă̐ݒ�p�^�[�����o�^����Ă��邩�ǂ����i�����lTrue�j
    �����s = 2           #'TokenSheet2�@�s�|�C���^
    ���͍sTYPE = ""      #'
    CMD_SEQ = 0
    

   
    #'���̓t�@�C���P�ʂŏ�����
    # UPD 20240618 yi.a.qian
    �t�@�C����,���C�u����ID,_,member = GetFileInfo(fileName)
    
    JOB_ID = member
    JOB_SEQ = 0
    PROC_ID = member
    # UPD END
    #'JCL���� = "�O��PROC" '�p�����[�^���Ȃ��ꍇ�APROC�L�[���[�h���Ȃ��ꍇ������ 201911MHI�Ή��ŕs����o�邽�߃R�����g��
    JCL���� = ""
    DD_NAME = ""
    DB�o�͔���_JCL1 = False
   
   #'Todo��t�@�C������U.LB.JCL%A%CYDOBJ.txt
    for i in range(len(TokenSheet2)):
        ������ = ���
        TokenSheet2_GYO = TokenSheet2[i]
    
        �����Y�s = TokenSheet2_GYO[1]
        ID_fld = TokenSheet2_GYO[2]
        DD_AAUTO���� = TokenSheet2_GYO[3]
        Name_fld = TokenSheet2_GYO[4]
        CMD_fld = TokenSheet2_GYO[5]
        ���͍sTYPE = CMD_fld
        PARM_fld = TokenSheet2_GYO[������]
     
        #'*****
        if Name_fld != "":
            DD_NAME = Name_fld
        # '*****
        
        # 'if TokenSheet2_GYO[2] != "":
        # '   DD_NAME = TokenSheet2_GYO[2]
     
        if CMD_fld ==  "JOB":
            JOB_ID = Name_fld
            JOB_SEQ = JOB_SEQ + 1
            # ADD 20240618 yi.a.qian
            PROC_ID = ""
            # ADD END
            JCL���� = "JCL"
            DD_NAME = ""
          #  '������ = 3         'TokenSheet2�@��|�C���^
            ������ = ���       #  'TokenSheet2�@��|�C���^
        elif CMD_fld == "EXEC":
            STEP_NAME = Name_fld
            STEP_PGM = ""
            STEP_PROC = ""
            STEP_PARM1 = ""
            STEP_PARM2 = ""
            DD_NAME = ""
            #'������ = 3         'TokenSheet2�@��|�C���^
            ������ = ���       #  'TokenSheet2�@��|�C���^
        elif CMD_fld == "DD":
          #  '������ = 3         'TokenSheet2�@��|�C���^
            ������ = ���       #  'TokenSheet2�@��|�C���^
        elif CMD_fld == "JCLLIB":
           # '������ = 3         'TokenSheet2�@��|�C���^
            ������ = ���      #   'TokenSheet2�@��|�C���^
        elif CMD_fld == "PROC":
            if JCL���� == "JCL":
                PROC_ID = Name_fld
                JCL���� = "����PROC"
                DD_NAME = ""
            elif JCL���� ==  "":
                #'JOB_ID = Name_fld
                PROC_ID = Name_fld
                JCL���� = "�O��PROC"
                DD_NAME = ""
                # ADD 20241008 j.d.lin
                JOB_ID = ""
                STEP_PROC = ""
                # ADD END
            #'������ = 3         'TokenSheet2�@��|�C���^
            ������ = ���      #   'TokenSheet2�@��|�C���^
        elif CMD_fld == "PEND":
            PROC_ID = ""
            JCL���� = "JCL"
            #'������ = 3         #'TokenSheet2�@��|�C���^
            ������ = ���      #   'TokenSheet2�@��|�C���^
#'20240131 ADD qian.e.wang
        elif CMD_fld == "INCLUDE":
            PROC_ID = ""
            JCL���� = "JCL"
            #'������ = 3         #'TokenSheet2�@��|�C���^
            ������ = ���      #   'TokenSheet2�@��|�C���^
#'ADD END
        
#'ADD
        elif CMD_fld == "IF":
           # '������ = 3      #   'TokenSheet2�@��|�C���^
            ������ = ���   #      'TokenSheet2�@��|�C���^
        elif CMD_fld == "ELSE":
           # '������ = 3        # 'TokenSheet2�@��|�C���^
            ������ = ���     #    'TokenSheet2�@��|�C���^
        elif CMD_fld == "ENDIF":
            #'������ = 3         #'TokenSheet2�@��|�C���^
            ������ = ���      #   'TokenSheet2�@��|�C���^
#'ADD END
        else:
            #'������ = 4         'TokenSheet2�@��|�C���^
            ������ = ��� + 1      #  'TokenSheet2�@��|�C���^

     
        # '�����J�n��̑ޔ��@����������o�͎��ɗ��p
        �����J�n�� = ������
        �sCHK = "OK" #'CMD�s�P�ʂł̃`�F�b�N����
     

        if ID_fld == "SYSIN�s":
#      '   DD_NAME = "SYSIN"
# '            DD_NAME = Name_fld
            SYSIN_SEQ = 0
            while ������ < len(TokenSheet2_GYO):
                SYSIN_SEQ = SYSIN_SEQ + 1
                SYSIN_LINE = TokenSheet2_GYO[������]  #  'SYSIN����
                SUB_SQL����_JCL_2_.insert()
                ������ = ������ + 1
                 #'Loop Until TokenSheet2_GYO[������] = "" #   'SYSIN�s�ɋ󔒍s������ꍇ�o�͂����f����ꍇ�̑Ή��i3�s�ȏ�A�����Ȃ��z��j
        
        elif ID_fld == "NET�s":    #'SYSIN�pTABLE�ɏo��
            SYSIN_SEQ = 0
            SYSIN_��ʒu_FROM = 0
            SYSIN_��ʒu_TO = len(TokenSheet2_GYO[������])*2
            
            while True:
                SYSIN_SEQ = SYSIN_SEQ + 1
                SYSIN_TEMP = Mid(TokenSheet2_GYO[������], SYSIN_��ʒu_FROM, len(TokenSheet2_GYO[������])*2)
                if len(SYSIN_TEMP)*2 < 255:
                   SYSIN_��ʒu_FROM = SYSIN_��ʒu_FROM + 255  #'���[�v�I������
                else:
                   SYSIN_��ʒu_TO = Mid(SYSIN_TEMP, 0, 255).rfind(",")
                   SYSIN_TEMP = Mid(SYSIN_TEMP, SYSIN_��ʒu_FROM, SYSIN_��ʒu_TO+1)
                   SYSIN_��ʒu_FROM = SYSIN_��ʒu_TO + 1
                
                SYSIN_LINE = SYSIN_TEMP   # 'SYSIN����
                STEP_NAME = "NET"
                STEP_PGM = "NET"
                STEP_PROC = ""
                SUB_SQL����_JCL_2_.insert()
                
                if SYSIN_��ʒu_FROM >= len(TokenSheet2_GYO[������])*2:
                    break
                
            # '    ������ = ������ + 1

            
        elif ID_fld == "�ʏ�s":
            while True:
         
                #'PARM���J�E���g
                PARM�s = 0     #'Parm�s�|�C���^
                parm_hit = False
                while True:
                    #'PARM�� = 6      'Parm��|�C���^
                    PARM�� = ���2     # 'Parm��|�C���^
                    hit_flg = True
                    parm_cnt = 0
                    re_flg = False
                
                    #'�擪�̃g�[�N����r(�ŏ����Ⴄ�ꍇ�͗�̃J�E���g�A�b�v�s�v)
                
                    if len(TokenSheet2_GYO) > ������ and TokenSheet2_GYO[������] == JCLSheet[PARM�s][PARM��]:
                      
                        while True:
                            if JCLSheet[PARM�s][PARM��] != "":
                                parm_cnt = parm_cnt + 1

                            parm_val = JCLSheet[PARM�s][���2+parm_cnt-1]
                            code_val = ""
                            if ������+parm_cnt-1 < len(TokenSheet2_GYO):
                                code_val = TokenSheet2_GYO[������+parm_cnt-1]
                            parm_chk = �ݒ�l��v�`�F�b�N(parm_val,code_val)
                            if parm_chk == False:
                                hit_flg = False
                            PARM�� = PARM�� + 1
                            
                        
                            if PARM�� >= len(JCLSheet[PARM�s]) or JCLSheet[PARM�s][PARM��] == "" or hit_flg == False:
                                break
# 'ADD(20111128-takei)
                    # '�擪�g�[�N�������K�\���̏ꍇ
                    elif str(JCLSheet[PARM�s][PARM��]).startswith("���K�\��_"):
                        # '�����Ώە�����č\��
                        tokenstr = ""
                        tokencnt = ������
                        re_flg = True
                        while tokencnt < len(TokenSheet2_GYO):
                            tokenstr = tokenstr + TokenSheet2_GYO[tokencnt] + " "
                            tokencnt = tokencnt + 1
                    
                        re_pattern = JCLSheet[PARM�s][PARM��].replace("���K�\��_", "")
                        mc = re.search(re_pattern,tokenstr)
                        if mc:
                            matchstr = str(mc.group(0)) # '�ŏ��Ɉ�v��������������
                           # '�擪�̕����񂩂��v���Ă���ꍇ�̂�(�擪�̕�����̈ꕔ�����K�\����HIT���Ă�����̂͑ΏۊO)
                            if tokenstr.startswith(matchstr) and \
                               len(TokenSheet2_GYO[������]) <= len(matchstr):
                        
                                # '��v�����p�����[�^���J�E���g
                                tokencnt = ������
                                re_exit = False #'���Ұ������S��v���Ȃ���Ώ����𔲂���
                                while True:
                                    if str(TokenSheet2_GYO[tokencnt]) in matchstr:
                                        matchstr = matchstr.replace(str(TokenSheet2_GYO[tokencnt]), "",1) ### �擪����}�b�`�����P������replace����
                                        tokencnt = tokencnt + 1
                                        parm_cnt = parm_cnt + 1
                                    else:
                                        re_exit = True
                                     #'���O�̈ז������[�v���Ȃ��悤�ɔz����
                                    if matchstr.replace(" ","") == "" or re_exit == True:
                                        break
                        
                            else:
                                hit_flg = False
                        
                        else:
                            hit_flg = False

# 'ADD END
                    else:
                        hit_flg = False
            
                    # '�`�F�b�N����
                    if hit_flg:

                        parm_hit = True
                        # JCLSheet[PARM�s][4] = JCLSheet[PARM�s][4] + 1 #  '�ݒ�l�J�E���g�A�b�v
                    #     'MsgBox ("�����l�F " + TokenSheet2_GYO[������] + " PARM-Key�F " + JCLSheet[PARM�s][1])
                    #     '���͍sTYPE = JCLSheet[PARM�s][5]       '�����ł̓Z�b�g���Ȃ�
                
                    #    '�����s������쐬
                        �����s������ = �����s�����񐶐�����(TokenSheet2_GYO[�����J�n��:])   #'�����J�n��i������������ɂ���j       '20120208 ADD
                
                        if �ݒ����HIT���o��:
                        #  'HIT���֘A���o��
                            SUB_SQL����_����_1_.insert("�L�[ID", ���C�u����ID, �t�@�C����, �����Y�s, JCLSheet[PARM�s][1], �����s������)
                
                        if ���͏���HIT���o�� and JCLSheet[PARM�s][2] != "":
                            
                            # '���������R�ʉ^�b��Ή�������
                            if JCLSheet[PARM�s][2] == "VOL":  #'VOL�̏ꍇ
                                �����s������ = JOB_ID + "-" + STEP_NAME + "-" + DD_NAME + ": " + �����s������
                            
                            # '���������R�ʉ^�b��Ή�������
                            if JCLSheet[PARM�s][2] == "LABEL":  #'LABEL�̏ꍇ
                                �����s������ = JOB_ID + "-" + STEP_NAME + "-" + DD_NAME + ": " + �����s������
                            
                            SUB_SQL����_����_1_.insert("����ID", ���C�u����ID, �t�@�C����, �����Y�s, JCLSheet[PARM�s][2], �����s������)
                
                        if �݌v����HIT���o�� and JCLSheet[PARM�s][3] != "":
                            #    'HIT���֘A���o��
                            SUB_SQL����_����_1_.insert("�݌vID", ���C�u����ID, �t�@�C����, �����Y�s, JCLSheet[PARM�s][3], �����s������)
                    
                    else:
                        PARM�s = PARM�s + 1

                    if PARM�s >= len(JCLSheet) or parm_hit == True:
                        break
           
                # '������X�V
                
                # '�s�P�ʂ̏����o�͂���̂ł����ł������i20150810 takei�j
                �����s������ = �����s�����񐶐�����(TokenSheet2_GYO[�����J�n��:]) 
                if parm_hit:
                    PARM�� = ���2
                    for i in range(parm_cnt):
                        parm_val = ""
                        if PARM�� + i < len(JCLSheet[PARM�s]):
                            parm_val = JCLSheet[PARM�s][PARM�� + i]
                        code_val = ""
                        if ������+i < len(TokenSheet2_GYO):
                            code_val = TokenSheet2_GYO[������+i]
                        �ݒ�l��v�F��������(parm_val,code_val,TokenSheet2_GYO[4])
                    re_flg = False
                    ������ = ������ + parm_cnt
                else:
                    # '����NG����
                    ALL_chk_ok = False      #    '�ЂƂł�NG������ƃV�[�g�P�ʂ�NG
                    �sCHK = "NG"
            
                    if �ݒ����HIT_NG���o��:
                       # '�����s������쐬
                        �����s������ = �����s�����񐶐�����(TokenSheet2_GYO[�����J�n��:])    #'�����J�n��i������������ɂ���j       '20120208 ADD
                        # 'NG���֘A���o��
                        SUB_SQL����_����_2_.insert("JCL", ���C�u����ID, �t�@�C����, �����Y�s, �����s������)

                    ������ = ������ + 1
             
                if ������ >= len(TokenSheet2_GYO):
                    break
                
        
        elif ID_fld == "��؍s":
            pass
            # '�������Ȃ�
        
    
    #  'JCL_CMD���̏o�́i2015/08/10�ǉ��j
        if ID_fld == "�ʏ�s":
            SUB_SQL����_JCL_5_.insert()
            
            # 'PROC_PARM�̏o�́i2019/10/8�ǉ��j
            # 'if PROC_ID != "" and CMD_fld = "PROC":  'PROC���Y����PROC�R�}���h�s���o��
            if CMD_fld == "PROC":  # 'PROC_ID�͂��̎��_�ŃZ�b�g����Ă��Ȃ��B
            
                SUB_SQL����_JCL_6_.insert(�����J�n��,TokenSheet2_GYO)
        
        # 'DB�o�͔���(�ϐ��ăZ�b�g�O�ɏo��)
        DB�o�͔���_JCL(TokenSheet2_GYO)
  
     

    # 'SUB_SQL����_JCL_1 �����s����Ă��Ȃ��ꍇ�́u�O��PROC�Ƃ��ďo�͂���v
    if not (DB�o�͔���_JCL1):
       SUB_SQL����_JCL_1_.insert()

    
    return ALL_chk_ok
    