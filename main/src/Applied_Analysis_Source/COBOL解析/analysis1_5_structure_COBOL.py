#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

SUB_SQL����_COBOL_0_ = None
SUB_SQL����_COBOL_3_ = None
SUB_SQL����_COBOL_4_ = None



def reset_all():            
    global �t�@�C����,COBOL_ID,CMD_SEQ,�����Y�s,COBOL�̈敪��,COBOL�K�w���,COBOL���򔻒�,���͍sTYPE,�����s������,�sCHK, \
            ���C�u����ID,PGM_ID,�t�@�C��IO�L��,PARM�L��,�T�u���[�`���L��,SQL�L��,��ʗL��,ALL_chk_ok, \
            COBOL_�֘A�敪,COBOL_�֘A���Y,COBOL_�֘A���Y_TRANID,\
            P_�t�@�C����,P_CBL_ID,P_CMD����,P_�ďo���Y,P_�ďoPARM, \
            re_flg
            
    re_flg = False
    ���C�u����ID = ""
    �t�@�C���� = ""
    COBOL_ID = ""
    COBOL�̈敪�� = ""
    COBOL�K�w��� = ""
    COBOL���򔻒� = ""
    �����s������ = ""
    ���͍sTYPE = ""
    �sCHK = False
    CMD_SEQ = 0
    �����Y�s = 0
    PGM_ID = ""
    �t�@�C��IO�L�� = ""
    PARM�L�� = ""
    �T�u���[�`���L�� = ""
    SQL�L�� = ""
    ��ʗL�� = ""
    ALL_chk_ok = True
    COBOL_�֘A�敪 = ""
    COBOL_�֘A���Y = ""
    COBOL_�֘A���Y_TRANID = ""

    
    P_�t�@�C���� = ""
    P_CBL_ID = ""
    P_CMD���� = ""
    P_�ďo���Y = ""
    P_�ďoPARM = ""

    
    
    
class SUB_SQL����_COBOL_0:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�ACOBOL_��{���"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
    def insert(self):
        if self.dic == None:
            self.setup()
            
        global �t�@�C����,���C�u����ID,COBOL_ID,PGM_ID,CMD_SEQ ,�t�@�C��IO�L��,PARM�L��,�T�u���[�`���L��,SQL�L��,��ʗL��,ALL_chk_ok
        
        if ALL_chk_ok == True:
            L_CHK = "OK"
        else:
            L_CHK = "NG"
        
      
        key_list = ["���YID","LIBRARY_ID","�����o��","���W���[����","CMD�s��","��͌���","�t�@�C��IO�L��","PARM�L��","�T�u���[�`���L��","SQL�L��","��ʗL��"]
        value_list = [�t�@�C����,���C�u����ID,COBOL_ID,PGM_ID,CMD_SEQ ,L_CHK,�t�@�C��IO�L��,PARM�L��,�T�u���[�`���L��,SQL�L��,��ʗL��]
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        self.cursor.execute(sql,value)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.cursor.close()
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()


class SUB_SQL����_COBOL_3:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�ACOBOL_�֘A���Y"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
    def insert(self):
        if self.dic == None:
            self.setup()
            
        global �t�@�C����,COBOL_ID,COBOL_�֘A�敪,COBOL_�֘A���Y,COBOL_�֘A���Y_TRANID
        
        key_list = ["���YID","COBOL_ID","�֘A�敪","�֘A���Y","�֘A���Y_TRANID"]
        value_list = [�t�@�C����,COBOL_ID,COBOL_�֘A�敪,COBOL_�֘A���Y,COBOL_�֘A���Y_TRANID.replace("'", "")]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.cursor.close()
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
        
        
class SUB_SQL����_COBOL_4:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�ACOBOL_CMD���"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
    def insert(self):
        if self.dic == None:
            self.setup()
            
        global �t�@�C����,COBOL_ID,CMD_SEQ,�����Y�s,COBOL�̈敪��,COBOL�K�w���,COBOL���򔻒�,���͍sTYPE,�����s������,�sCHK
        
        CMD_SEQ = CMD_SEQ + 1
      
        key_list = ["���YID","COBOL_ID","CMD_SEQ","�����Y�s���","�L�q�̈�","�i��","���򔻒�","CMD����","PARM","�sCHK����"]
        value_list = [�t�@�C����,COBOL_ID,CMD_SEQ,�����Y�s,COBOL�̈敪��,COBOL�K�w���,COBOL���򔻒�,���͍sTYPE,�����s������,�sCHK]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.cursor.close()
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
       
        

class SUB_SQL����_COBOL_6:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�ACOBOL_�֘A���Y"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
    def insert(self,�J�n��,TokenSheet2_GYO):
        if self.dic == None:
            self.setup()
            
        global  P_�t�@�C����,P_CBL_ID,P_CMD����,P_�ďo���Y,P_�ďoPARM
        
  
        key_list = ["���YID","COBOL_ID","�֘A�敪","�֘A���Y","�֘A���Y_TRANID"]
        value_list = [P_�t�@�C����,P_CBL_ID,DB����(P_CMD����),DB����(P_�ďo���Y),DB����(P_�ďoPARM)]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.cursor.close()
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
            self.cursor.close()
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
            self.cursor.close()
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
   
   
def PARM�`����񔻒�_COBOL_AREA(cbl_area, parm_area):
    

    if cbl_area == "�̈�A����":
        if parm_area == "�C��" or parm_area == "�̈�A":
            return True
        else:
            return False
    if cbl_area == "�̈�B�̂�":
        if parm_area == "�C��" or parm_area == "�̈�B":
            return True
        else:
            return False
    else:
        MSG = "�z��O�̏���"
        return False       
    
def PARM�`����񔻒�_COBOL_DIVISION(cbl_div, parm_div):

    if cbl_div == parm_div or parm_div == "����":
       return True
    else:
       return False

def ��O�L�[_COBOL(key):

    if key == "���x��" or key == "�ϐ�_SECTION��" or key == "�ϐ�_�i����":
        return True
    else:
        return False
    
def �ݒ�l���l�`�F�b�N_COBOL(parm_str):
    # 'if parm_str = "0":
    # '   MsgBox (parm_str & " : " & IsNumeric(parm_str))
    if IsNumeric(parm_str):
        return  "���l"
    else:
        return "������"



def �ݒ�l�^�C�v�`�F�b�N_COBOL(parm_str):

    if "'" in str(parm_str) or "==" in str(parm_str) or "\"" in str(parm_str):
       return "�萔"
    else:
        return "�ϐ�"

def �ݒ�l��v�`�F�b�N_COBOL(parm_val,code_val):
    
    parm_val,code_val = str(parm_val),str(code_val)
    Rtn_Cd = False
    �ݒ�l�^�C�v = �ݒ�l�^�C�v�`�F�b�N_COBOL(code_val)
    
    #     '���̔���͏������d���̂œ��ʂɕ�����
    # '    if "��\��" in parm_val:
    # '       if not (�\��ꔻ��(code_val, 1)):
    # '            return True
    # '    else
    
    # '���x��
    if "���x��" in parm_val and \
        �ݒ�l���l�`�F�b�N_COBOL(code_val) == "���l":
        return True
    # '�R�s�[��
    elif "�R�s�[��" in parm_val and \
        �ݒ�l�^�C�v == "�ϐ�":
        return True
    # '�T�u���[�`��
    elif "�T�u���[�`��" in parm_val and \
        �ݒ�l�^�C�v == "�ϐ�":
        return True
    # '�ϐ�
    elif "�ϐ�" in parm_val:
        # '�ϐ���     '20130919 �x�m�ʑΉ��i���R�ʉ^�Č��j
        if parm_val == "�ϐ���":
            if �ݒ�l�^�C�v == "�ϐ�" and \
                code_val != "PIC" and code_val != "REDEFINES" and code_val != ")":
                return True
        else:
            if �ݒ�l�^�C�v == "�ϐ�":
                return True
    # '�萔
    elif "�萔" in parm_val and \
        �ݒ�l�^�C�v == "�萔":
        return True
    # '���l
    elif "���l" in parm_val and \
        �ݒ�l���l�`�F�b�N_COBOL(code_val) == "���l":
        return True
    # '�\���i��L�����ȊO�j
    elif parm_val == code_val:
        return True
    else:
        return False

    return Rtn_Cd


def �����s�����񐶐�����(TokenSheet_str):

    TokenSheet_str = [str(s) for s in TokenSheet_str]
    �����s������ = " ".join(TokenSheet_str)
     
    return DB����(�����s������)



def �ݒ�l��v�F��������_COBOL(parm_val,code_val,proc_cond):
    global SUB_SQL����_COBOL_3_
    global COBOL_�֘A�敪,COBOL_�֘A���Y,COBOL_�֘A���Y_TRANID,COPY_�ϐ�,�T�u���[�`���L��,COPY_���x��, re_flg
    ### �Z���̐F�����͑�ςɂȂ�̂�python�łł͈�U��߂�

    if re_flg:
        pass

    # '�Z�N�V����
    elif "SECTION��" in parm_val:
        pass

    # '�i��
    elif "�i����" in parm_val:
        pass

    
    # '�R�s�[��
    elif "�R�s�[��" in parm_val:
       COBOL_�֘A�敪 = "COPY"
       COBOL_�֘A���Y = code_val
       COBOL_�֘A���Y_TRANID = ""
       SUB_SQL����_COBOL_3_.insert()
    
    # '�T�u���[�`��
    elif "�T�u���[�`��" in parm_val:
       COBOL_�֘A�敪 = "CALL"
       COBOL_�֘A���Y = code_val
       COBOL_�֘A���Y_TRANID = ""
       SUB_SQL����_COBOL_3_.insert()
    #    '�T�u���[�`���L���ݒ�
       �T�u���[�`���L�� = "��"
    
    # 'EXEC CICS LINK PROGRAM
    elif "ECLP" in parm_val:
       COBOL_�֘A�敪 = "ECLP"
       COBOL_�֘A���Y = code_val
       COBOL_�֘A���Y_TRANID = ""
       SUB_SQL����_COBOL_3_.insert()
    
    # 'EXEC CICS START TRANSID
    elif "ECST" in parm_val:
       COBOL_�֘A�敪 = "ECST"
       COBOL_�֘A���Y = ""
       COBOL_�֘A���Y_TRANID = code_val
       SUB_SQL����_COBOL_3_.insert()
    
    # 'EXEC CICS SEND MAP
    elif "ECSM" in parm_val:
       COBOL_�֘A�敪 = "ECSM"
       COBOL_�֘A���Y = code_val
       COBOL_�֘A���Y_TRANID = ""
       SUB_SQL����_COBOL_3_.insert()
    
    # 'EXEC CICS HANDLE ABEND PROGRAM
    elif "ECHA" in parm_val:
       COBOL_�֘A�敪 = "ECHA"
       COBOL_�֘A���Y = code_val
       COBOL_�֘A���Y_TRANID = ""
       SUB_SQL����_COBOL_3_.insert()
    
    # 'EXEC CICS WRITEQ TD QUEUE
    elif "ECWTQ" in parm_val:
       COBOL_�֘A�敪 = "ECWTQ"
       COBOL_�֘A���Y = code_val
       COBOL_�֘A���Y_TRANID = ""
       SUB_SQL����_COBOL_3_.insert()
    
    # 'EXEC CICS READ TRANSACTION
    elif "ECRT" in parm_val:
       COBOL_�֘A�敪 = "ECRT"
       COBOL_�֘A���Y = ""
       COBOL_�֘A���Y_TRANID = code_val
       SUB_SQL����_COBOL_3_.insert()
    
    # 'EXEC CICS READ UPDATE DATASET
    elif "ECRUD" in parm_val:
       COBOL_�֘A�敪 = "ECRUD"
       COBOL_�֘A���Y = code_val
       COBOL_�֘A���Y_TRANID = ""
       SUB_SQL����_COBOL_3_.insert()
    
    # 'EXEC CICS READ DATASET
    elif "ECRD" in parm_val:
       COBOL_�֘A�敪 = "ECRD"
       COBOL_�֘A���Y = code_val
       COBOL_�֘A���Y_TRANID = ""
       SUB_SQL����_COBOL_3_.insert()
    
    # '�ϐ���
    elif parm_val == "�ϐ���":
       COPY_�ϐ� = code_val
    # '�ϐ�
    elif "�ϐ�" in parm_val:
        pass

    # '�萔
    elif "�萔" in parm_val:
        pass

    # '���l
    elif "���l" in parm_val:
        pass

    # '���x����
    elif "���x��" in parm_val:
       COPY_���x�� = code_val
       
    # '������
    elif proc_cond == "PROC-����":
        pass
 
        
    # '�\���i��L�����ȊO�j
    elif parm_val == code_val:
        pass

    else:
        pass
    
#     '�ϐ��Z�b�g����
# '    Select Case parm_val
# '           Case "JOB"
# '                JOB_ID = TokenSheet2.Cells(�����s, 2).Value
# '           Case "�萔_�R�����g"
# '                JOB_�R�����g = code_val
# '           Case "�ϐ�_�^�C�v�@"
# '                COPY_�^�C�v = code_val
# '           Case "����_���l"
# '                COPY_���� = code_val
# '                COPY_����_������ = code_val
# '           Case "�����⏕_���l"
# '                COPY_���� = code_val
# '                COPY_����_������ = COPY_����_������ & "," & code_val
# '           Case "�ϐ�_REDEFINES"
# '                COPY_REDIFINE = code_val
# '                REDIFINE_����_���x�� = COPY_���x��
# '           Case "OCCURS_���l"
# '                COPY_OCCURS = code_val
# '                OCCOURS_����_���x�� = COPY_���x��
# '                OCCOURS_�� = COPY_OCCURS
# '           Case "COMP-3"
# '                COPY_�^�C�v2 = "COMP-3"
# '           Case "�ϐ�_�^�C�v�A"     '�uCOMP-3�v�ȂǗD�悵�Đ��䂵�������̂�����ΑO�ɐݒ肷��
# '                COPY_�^�C�v2 = code_val

  
def analysis1_5_structure_COBOL(TokenSheet2,CobolSheet,fileName,db_path, �ݒ����HIT���o�� = False,���͏���HIT���o�� = False,�݌v����HIT���o�� = False,�ݒ����HIT_NG���o�� = True, conn=None, cursor=None):
    global SUB_SQL����_COBOL_3_
    
    global �t�@�C����,COBOL_ID,CMD_SEQ,�����Y�s,COBOL�̈敪��,COBOL�K�w���,COBOL���򔻒�,���͍sTYPE,�����s������,�sCHK, \
            ���C�u����ID,PGM_ID,�t�@�C��IO�L��,PARM�L��,�T�u���[�`���L��,SQL�L��,��ʗL��,ALL_chk_ok, \
            COBOL_�֘A�敪,COBOL_�֘A���Y,COBOL_�֘A���Y_TRANID,\
            P_�t�@�C����,P_CBL_ID,P_CMD����,P_�ďo���Y,P_�ďoPARM, \
            re_flg
    

    reset_all()
    SUB_SQL����_COBOL_0_ = SUB_SQL����_COBOL_0(conn,cursor)
    SUB_SQL����_COBOL_3_ = SUB_SQL����_COBOL_3(conn,cursor)
    SUB_SQL����_COBOL_4_ = SUB_SQL����_COBOL_4(conn,cursor)
    SUB_SQL����_COBOL_6_ = SUB_SQL����_COBOL_6(conn,cursor)
    
    SUB_SQL����_����_1_ = SUB_SQL����_����_1(conn,cursor)
    SUB_SQL����_����_2_ = SUB_SQL����_����_2(conn,cursor)


    ALL_chk_ok = True    #'�V�[�g�P�ʂőS�Ă̐ݒ�p�^�[�����o�^����Ă��邩�ǂ����i�����lTrue�j
   
#    '�ϐ�������
#    'COBOL_ID = Replace(Replace(�t�@�C����, ".cob", ""), ".cbl", "") '�g���q�ɍ��킹�Đݒ�
#    'COBOL_ID = Replace(Replace(���W���[��ID, ".cob", ""), ".cbl", "") '�g���q�ɍ��킹�Đݒ� TODO ���@�Ƃ̂���Ή�
    �t�@�C����,���C�u����ID,_,COBOL_ID = GetFileInfo(fileName)

    PGM_ID = "��"
   
    FILE_SEQ = 0
    CMD_SEQ = 0
    
    
    �t�@�C��IO�L�� = ""
    PARM�L�� = ""
    �T�u���[�`���L�� = ""
    SQL�L�� = ""
    ��ʗL�� = ""
    
    �����s = 0      #'TokenSheet�@�s�|�C���^
    ��� = 6       #   'TokenSheet2 ��|�C���^
    ���2 = 7       #   'CobolSheet ��|�C���^
    #'���͍sTYPE = ""     '�s�P�ʏ��Ȃ̂ł����ł͂Ȃ�
    
    while �����s < len(TokenSheet2):

        TokenSheet2_GYO = TokenSheet2[�����s]

        #   '������ = 5         'TokenSheet2�@��|�C���^
        ������ = ���         #'TokenSheet2�@��|�C���^
        �sCHK = "OK" #'CMD�s�P�ʂł̃`�F�b�N����
        
        #   '��{�I�ɂ��̃^�C�~���O�ōs��
        �����Y�s = TokenSheet2_GYO[1]
        COBOL�̈敪�� = TokenSheet2_GYO[3]
        COBOL�K�w��� = TokenSheet2_GYO[4]
        COBOL���򔻒� = TokenSheet2_GYO[5]
        # print(TokenSheet2_GYO)
        while True:
        
            # ' "."�͋��ʂŏ����ΏۊO�Ƃ���
            
            if ������ >=len(TokenSheet2_GYO) or (������+1 >= len(TokenSheet2_GYO) and (TokenSheet2_GYO[������] == ".")):
                
                # '�s���ς��O�ɍs�P�ʏ��������{
                if len(TokenSheet2_GYO) >= 7:
                    �����s������ = �����s�����񐶐�����(TokenSheet2_GYO[6:])
                    SUB_SQL����_COBOL_4_.insert()
                
                �����s = �����s + 1
                if �����s >= len(TokenSheet2):
                    SUB_SQL����_COBOL_0_.insert()
                    return ALL_chk_ok
                
                TokenSheet2_GYO = TokenSheet2[�����s]
                # print(TokenSheet2_GYO)
                # '������ = 5
                ������ = ���
                �sCHK = "OK" #'CMD�s�P�ʂł̃`�F�b�N����

                �����Y�s = TokenSheet2_GYO[1]
                COBOL�̈敪�� = TokenSheet2_GYO[3]
                COBOL�K�w��� = TokenSheet2_GYO[4]
                COBOL���򔻒� = TokenSheet2_GYO[5]
  
                

            # '�s���x���̏����ł��邪�s���Z���������O�Ŏ��{����Ă��肱���ōs���K�v������
            # '���R�}���h���ݒ�i�ڍ׉��̗]�n����j
            if IsNumeric(TokenSheet2_GYO[���]):
                ���͍sTYPE = "�f�[�^��`"
            elif COBOL�̈敪�� == "�̈�A����":
                if ��� + 1 < len(TokenSheet2_GYO) and TokenSheet2_GYO[��� + 1]  == "DIVISION":
                    ���͍sTYPE = "DIVISION"
                elif  ��� + 1 < len(TokenSheet2_GYO) and TokenSheet2_GYO[��� + 1] == "SECTION":
                    ���͍sTYPE = "SECTION"
                    if TokenSheet2_GYO[���] == "LINKAGE": #'PARM�L���ݒ�
                        PARM�L�� = "��"
                else:
                    if COBOL�K�w��� == "�葱����":
                        ���͍sTYPE = "���x��"
                    else:
                        ���͍sTYPE = TokenSheet2_GYO[���]
                        
                        if ���͍sTYPE == "PROGRAM-ID":
                            if ��� + 1 < len(TokenSheet2_GYO)  and TokenSheet2_GYO[��� + 1] == ".":
                                if ��� + 2 < len(TokenSheet2_GYO):
                                    PGM_ID = TokenSheet2_GYO[��� + 2]
                                else:
                                    PGM_ID = "" 
                            else:
                                if ��� + 1 < len(TokenSheet2_GYO):
                                    PGM_ID = TokenSheet2_GYO[��� + 1]
                                else:
                                    PGM_ID = "" 
   
            else:
                ���͍sTYPE = TokenSheet2_GYO[���]

                if ���͍sTYPE == "EXEC" and TokenSheet2_GYO[��� + 1] == "SQL":
                    ���͍sTYPE = "SQL"
                    SQL�L�� = "��"
                elif ���͍sTYPE == "OPEN":
                    �t�@�C��IO�L�� = "��"
    
            # 'PARM���J�E���g
            PARM�s = 0     # 'Parm�s�|�C���^
            parm_hit = False
            
            # '�������ԉ��P�Ή��i����SQL���߂Ȃǂ�����ꍇ�ɏ������Ԃ��ُ�ɂ����邽�߂̉��P�j
            �����s������ = �����s�����񐶐�����(TokenSheet2_GYO[6:])   #'�����J�n��i6��ڂ������ɂ���j'�����s�����񂪑傫������ꍇ�͏������X�L�b�v���� 2016/02/26
            # '������10000�����𒴂���ꍇ�̓`�F�b�N���Ȃ�
            if len(�����s������) < 10000:
        
                while True:
                    # 'PARM�� = 7      'Parm��|�C���^
                    PARM�� = ���2      #'Parm��|�C���^
                    hit_flg = True
                    parm_cnt = 0
                    re_flg = False

                    # 'PARM�`����񔻒�
                    #     '�ݒ�����̊K�w���i�u���o�����v�u�葱�����v���j����v���Ă�����̂̂ݏ�������
                    #     '�ݒ�����̋L�q�̈���i�u�̈�A�v�u�̈�B�v�j����v���Ă�����̂̂ݏ�������
                    # '�����Y�s = TokenSheet2_GYO[1]
                    # 'COBOL�̈敪�� = TokenSheet2_GYO[3]
                    # 'COBOL�K�w��� = TokenSheet2_GYO[4]
                    PARM�̈敪�� = CobolSheet[PARM�s][5]
                    PARM�K�w��� = CobolSheet[PARM�s][6]
            
          
                    if PARM�`����񔻒�_COBOL_AREA(COBOL�̈敪��, PARM�̈敪��) and \
                        PARM�`����񔻒�_COBOL_DIVISION(COBOL�K�w���, PARM�K�w���):
                    
                        # '�擪�̃g�[�N����r(�ŏ����Ⴄ�ꍇ�͗�̃J�E���g�A�b�v�s�v)
                        if TokenSheet2_GYO[������] == CobolSheet[PARM�s][PARM��] or \
                            ��O�L�[_COBOL(CobolSheet[PARM�s][PARM��]):
                            while True:
                                if CobolSheet[PARM�s][PARM��] != "":
                                    parm_cnt = parm_cnt + 1
                                parm_val = CobolSheet[PARM�s][���2+parm_cnt-1]
                                code_val = ""
                                if ������+parm_cnt-1 < len(TokenSheet2_GYO):
                                    code_val = TokenSheet2_GYO[������+parm_cnt-1]
                                parm_chk = �ݒ�l��v�`�F�b�N_COBOL(parm_val,code_val)
                                if parm_chk == False:
                                    hit_flg = False
                                PARM�� = PARM�� + 1
                            
                                if PARM�� >= len(CobolSheet[PARM�s]) or CobolSheet[PARM�s][PARM��] == "" or hit_flg == False:
                                    break
                        
                        # '�擪�g�[�N�������K�\���̏ꍇ
                        elif str(CobolSheet[PARM�s][PARM��]).startswith("���K�\��_"):
                            # '�����Ώە�����č\��
                            tokenstr = ""
                            tokencnt = ������
                            re_flg = True
                            word_set = CobolSheet[PARM�s][-1]
                            start_word_check = False
                            while tokencnt < len(TokenSheet2_GYO):
                                s = TokenSheet2_GYO[tokencnt]
                                if s in word_set:
                                    start_word_check = True
                                tokenstr = tokenstr + s + " "
                                tokencnt = tokencnt + 1

                            if start_word_check == False:
                                for s in word_set:
                                    if tokenstr.startswith(s):
                                        start_word_check = True
                                        break
                                
                            if start_word_check == False:
                                hit_flg = False
                            else:
                            
                                re_pattern = CobolSheet[PARM�s][PARM��].replace("���K�\��_", "")
 
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

                        else:
                            hit_flg = False
                    else:
                        hit_flg = False
                

            
                    # '�`�F�b�N����
                    if hit_flg:
                        parm_hit = True
                        CobolSheet[PARM�s][4] = CobolSheet[PARM�s][4] + 1  # '�ݒ�l�J�E���g�A�b�v
                        #'���͍sTYPE = CobolSheet[PARM�s][6]
                    
                        if �ݒ����HIT���o�� or ���͏���HIT���o�� or �݌v����HIT���o��:
                    
                            # '�����s������쐬
                            # 'SUB_�����s�����񐶐����� (5)   '�����J�n��i5��ڂ������ɂ���j       '20120208 ADD
                            �����s������ = �����s�����񐶐�����(TokenSheet2_GYO[6:])  # '�����J�n��i6��ڂ������ɂ���j       '20120411 UPD
                    
                            if �ݒ����HIT���o��:
                                # 'HIT���֘A���o��
                                SUB_SQL����_����_1_.insert("�L�[ID", ���C�u����ID, COBOL_ID, �����Y�s, CobolSheet[PARM�s][1], �����s������)
                    
                            if ���͏���HIT���o�� and CobolSheet[PARM�s][2] != "":
                                # 'HIT���֘A���o��
                                SUB_SQL����_����_1_.insert("����ID", ���C�u����ID, COBOL_ID, �����Y�s, CobolSheet[PARM�s][2], �����s������)
                    
                            if �݌v����HIT���o�� and CobolSheet[PARM�s][3] != "":
                                # 'HIT���֘A���o��
                                SUB_SQL����_����_1_.insert("�݌vID", ���C�u����ID, COBOL_ID, �����Y�s, CobolSheet[PARM�s][3], �����s������)
                    
                    
                    else:
                        PARM�s = PARM�s + 1

                    if PARM�s >= len(CobolSheet) or parm_hit == True:
                        break
            
            else:  # '�������ԉ��P�Ή��i�����s�����񂪈��̒����𒴂���ꍇ�͏����X�L�b�v�j
                ������ = 16000 #'����ȏ�̗񂪂������炿����Ə��������������Ȃ邩��
            
        
        # '        '�`�F�b�N���ʂɂ�����炸�s�P�ʂ̏����o�͂���̂ł����Ő����i20150326 takei�j
        # '        �����s������ = �����s�����񐶐�����(TokenSheet2_GYO[6:])
        # '        'Call SUB_�����s�����񐶐�����(���)  'CALL�ŌĂԂƊ�񂪉��Z�����H�l�Q�ƁH
        
            # '������X�V
            if parm_hit:

                PARM�� = ���2
                for i in range(parm_cnt):
                    parm_val = ""
                    if PARM�� + i < len(CobolSheet[PARM�s]):
                        parm_val = CobolSheet[PARM�s][PARM�� + i]
                    code_val = ""
                    if ������+i < len(TokenSheet2_GYO):
                        code_val = TokenSheet2_GYO[������+i]
                    �ݒ�l��v�F��������_COBOL(parm_val,code_val,CobolSheet[PARM�s][5])
                re_flg = False
                ������ = ������ + parm_cnt
            else:
                # '����NG����
                ALL_chk_ok = False      #    '�ЂƂł�NG������ƃV�[�g�P�ʂ�NG
                �sCHK = "NG"
        
                if �ݒ����HIT_NG���o��:
                    #    '�����s������쐬
                    # ' �� CHK���ʂɊ֌W�Ȃ��s������𐶐�����̂�IF���̊O�ɏo���B'20150309 takei
                    # 'SUB_�����s�����񐶐����� (���)   '�����J�n��i6��ڂ������ɂ���j       '20120411 UPD
                    # 'NG���֘A���o��
                    SUB_SQL����_����_2_.insert("COBOL", ���C�u����ID, COBOL_ID, �����Y�s, �����s������)

                ������ = ������ + 1

            if ������ >= len(TokenSheet2_GYO):
                    break
 
 
        # '�`�F�b�N���ʂɂ�����炸�s�P�ʂ̏����o�͂���̂ł����Ő����i20150326 takei�j
        �����s������ = �����s�����񐶐�����(TokenSheet2_GYO[6:])
        # 'Call SUB_�����s�����񐶐�����(���)  'CALL�ŌĂԂƊ�񂪉��Z�����H�l�Q�ƁH
        SUB_SQL����_COBOL_4_.insert()
    
    
        �����s = �����s + 1
        
        
        
        if �����s >= len(TokenSheet2):
            break
    
    SUB_SQL����_COBOL_0_.insert() #'��{��񂾂��ǌォ��ǉ������̂Łu0�v�ɂ���

    return ALL_chk_ok
    