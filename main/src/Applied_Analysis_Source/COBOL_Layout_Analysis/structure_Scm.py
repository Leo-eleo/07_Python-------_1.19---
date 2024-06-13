#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

     
class SUB_SQL����_����_1:
    def __init__(self,conn,cursor):
        self.dic = {}
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
        self.dic = {}
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
   
   
class �X�L�[�}_��{���:
    def __init__(self,conn,cursor):
        self.dic = {}
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�X�L�[�}_��{���"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
    def insert(self,err_info):
        if self.dic == None:
            self.setup()
            
        global ���C�A�E�g��,COPY_���R�[�h��,COPY_���R�[�h��,�}���`���C�A�E�g����,REDIFINE_�L��,X���ڂ̂�,���C�A�E�g�s��,ALL_chk_ok
  
        # if ALL_chk_ok == False:
        #     l_err = "�G���[�L"
        # else:
        #     l_err = ""
        if COPY_���R�[�h�� == "":
            COPY_���R�[�h�� = 0
            
        key_list = ["���C�A�E�g��","���R�[�h��","���R�[�h��","�}���`���C�A�E�g����","REDIFINE�L��","X���ڂ̂�","���C�A�E�g�s��","�G���[���"]
        value_list = [���C�A�E�g��,COPY_���R�[�h��,COPY_���R�[�h��,�}���`���C�A�E�g����,REDIFINE_�L��,X���ڂ̂�,���C�A�E�g�s��,err_info]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.cursor.close()
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
        
class ���C�A�E�g��͏��:
    def __init__(self,conn,cursor):
        self.dic = {}
        self.conn = conn
        self.cursor = cursor
        self.dbname = "���C�A�E�g��͏��"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
    def insert(self,layout_string):
        if self.dic == None:
            self.setup()
            
        global ���C�A�E�g��

        key_list = ["���C�A�E�g��","���C�A�E�g���"]
        value_list = [���C�A�E�g��,layout_string]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.cursor.close()
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
        
def �����s�����񐶐�����(TokenSheet_str):
    
    TokenSheet_str = [str(s) for s in TokenSheet_str]
    �����s������ = " ".join(TokenSheet_str)
     
    return DB����(�����s������)

def �ݒ�l��v�F��������_COPY(parm_val,code_val,code_val2):

    global COPY_�ϐ�,COPY_���R�[�h��,REDIFINE_����_���x��,OCCOURS_����_���x��,OCCOURS_��,OCCOURS_�o�C�g�J�E���g,COPY_�^�C�v2,X���ڂ̂�,COPY_�T�C��,N���ڗL��,\
            COPY_����,COPY_����_������,COPY_REDIFINE,REDIFINE_�L��,�}���`���C�A�E�g����,VALUE�L��,COPY_���x��,COPY_�^�C�v,COPY_OCCURS
    
    parm_val = str(parm_val)
    code_val = str(code_val)
    code_val2 = str(code_val2)
    # '�ϐ���
    if parm_val == "�ϐ���":
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
       
        COPY_���x�� = int(code_val)
        if IsNumeric(code_val) and int(code_val) == 1 and COPY_���R�[�h�� == "":
            COPY_���R�[�h�� = code_val2   # '���̃g�[�N�����ǂ�

# '       if �擪���x�� = "":
# '          �擪���x�� = code_val
# '       
       
    #    'Redifine��������
        if COPY_���x�� <= REDIFINE_����_���x��:
            REDIFINE_����_���x�� = 0
    #    'OCCOURS_����_���x������
        if COPY_���x�� <= OCCOURS_����_���x��:
    # '          COPY_���R�[�h�� = COPY_���R�[�h�� + OCCOURS_�o�C�g�J�E���g * OCCOURS_��
    # '          COPY_���Έʒu = COPY_���Έʒu + OCCOURS_�o�C�g�J�E���g * OCCOURS_��
            OCCOURS_����_���x�� = 0
            OCCOURS_�� = 0
            OCCOURS_�o�C�g�J�E���g = 0
    # 'USAGE
    elif "USAGE" in parm_val: 
        COPY_�^�C�v2 = code_val
    
    
    # '�\���i��L�����ȊO�j
    elif parm_val == code_val:
        pass

    # '�ϐ��Z�b�g����

    if parm_val == "�ϐ�_�^�C�v�@":
        
        
        if code_val == "." and code_val2 == "":
            return
        
        COPY_���� += len(code_val.replace("V","").replace("S","").replace("P",""))-1
        
        COPY_�^�C�v = code_val.replace("+","").replace("\\","").replace("-","").replace("V","")
        
        # if COPY_�^�C�v.replace("X", ""):
        #     X���ڂ̂� = ""
        if COPY_�^�C�v.replace("X", "") != "" and COPY_�^�C�v.replace("9","") != "":
            X���ڂ̂� = ""
        
        if "+" in code_val:
            COPY_�T�C�� = "+"
            
        if "S" in COPY_�^�C�v:
            COPY_�T�C�� = "S"
        
    # '���ǉ��@20150714�@Takei
        if "N" in COPY_�^�C�v:
            N���ڗL�� = "��"
         
    elif parm_val == "�ϐ�_�^�C�v�A":
        if code_val == "." and code_val2 == "":
            return
        
        COPY_���� += len(code_val.replace("V","").replace("S","").replace("P",""))-1
        
        if code_val2 == "(":
            pass
        else:
            if "9" not in code_val and "P" not in code_val:
                print("PIC��`�̑z��O�p�^�[��",code_val,"�ϐ�_�^�C�v�A")
            COPY_����_������ = COPY_����_������ + " " + str(len(code_val.replace("V","").replace("+","").replace("-","")))
            COPY_���� += len(code_val.replace("V","").replace("P",""))
            
    elif parm_val == "�ϐ�_�^�C�v�B":
        if code_val == "." and code_val2 == "":
            return
        
        COPY_���� += len(code_val.replace("V","").replace("S","").replace("P",""))-1
        if code_val2 == "(":
            pass
        else:
            if "9" not in code_val and "P" not in code_val:
                print("PIC��`�̑z��O�p�^�[��",code_val,"�ϐ�_�^�C�v�A")
            COPY_����_������ = COPY_����_������ + " " + str(len(code_val.replace("V","").replace("+","").replace("-","")))
            COPY_���� += len(code_val.replace("V","").replace("P",""))

            
    elif parm_val == "����_���l":
        COPY_���� += int(code_val)
        COPY_����_������ = code_val
 
    elif parm_val == "��������_���l":
        COPY_���� = COPY_���� + int(code_val)
        COPY_����_������ = COPY_����_������ + " " + code_val
    elif parm_val == "�����⏕_���l":
        COPY_���� += int(code_val)
        COPY_����_������ = COPY_����_������ + "," + code_val
    elif parm_val == "�ϐ�_REDEFINES":
        COPY_REDIFINE = code_val
        REDIFINE_����_���x�� = COPY_���x��
        REDIFINE_�L�� = "��"
        �}���`���C�A�E�g���� = ""
    elif parm_val == "OCCURS_���l":
            COPY_OCCURS = int(code_val)
            OCCOURS_����_���x�� = COPY_���x��
            OCCOURS_�� = COPY_OCCURS
    elif parm_val == "�ϐ�_�^�C�v�s��":
        # if str(code_val).startswith("\\"):
        #     code_val = code_val[1:]
        
        code_val = code_val.replace("V","").replace("P","")
        if "CR" in code_val or "DB" in code_val:
            code_val = code_val.replace("CR","").replace("DB","")
            COPY_���� += 1
            
        COPY_���� += len(code_val.replace("V", ""))
        COPY_����_������ = str(len(code_val.replace("V", "")))
    
        
        if "X" in code_val:
            COPY_�^�C�v = "X"
        elif "9" in code_val:
            COPY_�^�C�v = "9"
            
        elif "Z" in code_val or "0" in code_val or "P" in code_val or "*" in code_val:
            if COPY_�^�C�v == "":
                COPY_�^�C�v = "9"
                if "Z" in code_val:
                    COPY_�T�C�� = "Z"
                elif "P" in code_val:
                    COPY_�T�C�� = "P"
                elif "*" in code_val:
                    COPY_�T�C�� = "*"
                elif "0" in code_val:
                    COPY_�T�C�� = "0"

            else:
                pass
        elif "\\" in code_val:
            if COPY_�^�C�v == "":
                COPY_�^�C�v = "X"
                COPY_�T�C�� = "\\"
        else:
            print("�z��O��COPY_�^�C�v",code_val)
            COPY_�^�C�v = code_val
            
    elif parm_val == "�ϐ�_�^�C�v�s��2":

        # if str(code_val).startswith("\\"):
        #     code_val = code_val[1:]
        
        code_val = code_val.replace("V","").replace("P","")
        if "CR" in code_val or "DB" in code_val:
            code_val = code_val.replace("CR","").replace("DB","")
            COPY_���� += 1
            
        COPY_���� += len(code_val.replace("V", ""))
        COPY_����_������ += " " + str(len(code_val.replace("V", "")))
    # '���ǉ��@20140708�@Takei
    elif parm_val == "�⑫�^�C�v":
        COPY_�^�C�v = COPY_�^�C�v + code_val.replace("V", "")  #'P�͂ǂ����邩���߂Ă��Ȃ�
        COPY_���� = COPY_���� + len(code_val.replace("V", "").replace("P",""))
    # '���ǉ��@20150714�@Takei
    elif parm_val == "VALUE":
        VALUE�L�� = "��"
    else:
        pass

 
def �ݒ�lUSAGE�`�F�b�N_COPY(parm_str):
    
    global �o�C�i�����ڗL��
    
    if parm_str =="BINARY":
        �o�C�i�����ڗL�� = "��"
        return True
    elif parm_str =="COMP":
        �o�C�i�����ڗL�� = "��"
        return True
    elif parm_str =="COMP-1":
        �o�C�i�����ڗL�� = "��"
        return True
    elif parm_str =="COMP-2":
        �o�C�i�����ڗL�� = "��"
        return True
    elif parm_str =="COMP-3":
        �o�C�i�����ڗL�� = "��"
        return True
    elif parm_str =="COMP-4":
        �o�C�i�����ڗL�� = "��"
        return True
    elif parm_str =="COMP-5":
        �o�C�i�����ڗL�� = "��"
        return True
    elif parm_str =="PACKED-DECIMAL":
        �o�C�i�����ڗL�� = "��"
        return True
    elif parm_str =="BIT":
        �o�C�i�����ڗL�� = "��"
        return True
    else:
        return False


def �ݒ�l���l�`�F�b�N_COPY(parm_str):
    if IsNumeric(parm_str):
        return  "���l"
    else:
        return "������"



def �ݒ�l�^�C�v�`�F�b�N_COPY(parm_str):

    if "'" in parm_str:
       return "�萔"
    else:
       return "�ϐ�"

def �ݒ�l��v�`�F�b�N(parm_val,code_val):
    
    global COPY_���x��
    
    parm_val,code_val = str(parm_val),str(code_val)    
    code_val = code_val.replace("PICTURE", "PIC")  #'PICTURE�w��͋����I��PIC�ɕϊ�
    
    global MODE�w��L��
    
    �ݒ�l�^�C�v = �ݒ�l�^�C�v�`�F�b�N_COPY(code_val)
    
    # '���x��
    if "���x��" in parm_val and \
        �ݒ�l���l�`�F�b�N_COPY(code_val) == "���l" and COPY_���x�� == 0:
        if int(code_val) < 50:                               #    'COPY��Ƃ��Ẵ��x����1�`49��z��
            return True
       
    # '�ϐ�
    if "�ϐ�" in parm_val and \
        �ݒ�l�^�C�v == "�ϐ�":
        return True
    # '�萔
    elif "�萔" in parm_val and \
        �ݒ�l�^�C�v == "�萔":
        return True
    # '���l
    elif "���l" in parm_val and \
        �ݒ�l���l�`�F�b�N_COPY(code_val) == "���l":
        return True
    # 'USAGE
    elif "USAGE" in parm_val and \
        �ݒ�l�^�C�v == "�ϐ�" and \
        �ݒ�lUSAGE�`�F�b�N_COPY(code_val) == True:
        return True
    # '�ϐ��s��
    elif parm_val == "�ϐ�_�^�C�v�s��" and \
        code_val.replace("X", "").replace("9", "").replace("V", "") == "":
        return True
    # '���[�h�^�C�v MODE-1,MODE-2,MODE-3,MODE-4.....
    elif parm_val == "���[�h�^�C�v":
        if code_val == "MODE-1" or code_val == "MODE-2" or code_val == "MODE-3" or code_val == "MODE-4":
            MODE�w��L�� = "��"
            return True
            
    # '�⑫�^�C�v
    elif parm_val == "�⑫�^�C�v" and \
        code_val.replace("P", "").replace("9", "").replace("V", "").replace("+", "").replace("-", "") == "":
        return True
    # '�ϐ�_NotKeyWord [VALUE, CHARACTER, PRINTING]
    elif parm_val == "NotKeyWord":
        if code_val == "VALUE" or code_val == "CHARACTER" or code_val == "PRINTING":
            return False
        else:
            return True
    elif parm_val == code_val:
       return True
    else:
       return False


def �����s�����񐶐�����(TokenSheet_str):

    TokenSheet_str = [str(s) for s in TokenSheet_str]
    �����s������ = " ".join(TokenSheet_str)
     
    return DB����(�����s������)


def �o�C�i��������():
    global COPY_����,COPY_�o�C�g��
    
    if COPY_���� <= 4:
       COPY_�o�C�g�� = 2
    elif COPY_���� <= 9:
       COPY_�o�C�g�� = 4
    else:                      # '10�`18����z��
       COPY_�o�C�g�� = 8
       
       
def �o�C�g�����Z_COPY():
    global COPY_�^�C�v2,COPY_�o�C�g��,COPY_����,COPY_�^�C�v,OCCOURS_�o�C�g�J�E���g
    

    if COPY_�^�C�v2 == "BINARY":
        �o�C�i��������()
    elif COPY_�^�C�v2 == "COMP":
        �o�C�i��������()
    elif COPY_�^�C�v2 == "COMP-1":
        COPY_�o�C�g�� = 4
    elif COPY_�^�C�v2 == "COMP-2":
        COPY_�o�C�g�� = 8
    elif COPY_�^�C�v2 == "PACKED-DECIMAL":
        temp_num = (COPY_���� + 2) // 2
        COPY_�o�C�g�� = temp_num
    elif COPY_�^�C�v2 == "COMP-3":
        temp_num = (COPY_���� + 2) // 2
        COPY_�o�C�g�� = temp_num
        # 'RoundUp(temp_num, 0)
    elif COPY_�^�C�v2 == "COMP-4":
        �o�C�i��������()
    elif COPY_�^�C�v2 == "COMP-5":
        �o�C�i��������()
    elif COPY_�^�C�v2 == "BIT":
        temp_num = COPY_���� // 8
        COPY_�o�C�g�� = temp_num
    else:
        if COPY_�^�C�v == "N":
            COPY_�o�C�g�� = COPY_���� * 2
        elif COPY_�^�C�v == "G":
            COPY_�o�C�g�� = COPY_���� * 2
        else:
            COPY_�o�C�g�� = COPY_����   
       
    if REDIFINE_����_���x�� > 0:
        return 0
    else:
        if OCCOURS_����_���x�� > 0:
            OCCOURS_�o�C�g�J�E���g = OCCOURS_�o�C�g�J�E���g + COPY_�o�C�g��
            return 0
        else:
            return COPY_�o�C�g��

def MC�����񖾍�(m_sigh,m_type,m_type2,m_byte): #�l�b���}���`���C�A�E�g�`�F�b�N

    m_type = str(m_type).replace("S", "").replace("V", "")
    m_type2 = str(m_type2)
    
    if "X" in m_type:
       r_str = "X"
    elif "A" in m_type:
        r_str = "X"
    elif "N" in m_type or "G" in m_type:
       r_str = "N"
    elif "9" in m_type:
        if m_type2 == "COMP":
            r_str = "B"
        elif m_type2 == "COMP-1":
            r_str = "?"
        elif m_type2 == "COMP-2":
            r_str = "?"
        elif m_type2 == "COMP-3":
            r_str = "P"
        elif m_type2 == "COMP-4":
            r_str = "B"
        elif m_type2 == "COMP-5":
            r_str = "B"
        elif m_type2 == "PACKED-DECIMAL":
            r_str = "P"
        elif m_type2 == "BINARY":
            r_str = "B"
        elif m_type2 == "":
            if m_sigh == "S":
                r_str = "Z"
            else:
                r_str = "9"
        else:
            r_str = "?"
            
    elif "1" in m_type:
        r_str = "B"             #    '�b��Ή��i�v�m�F�j
    else:
        r_str = "?"
        MSG = "�z��O�̓��e"
        # print(MSG,"MC������ڍ�",m_type,m_sigh)
    
    global X���ڂ̂�
    if r_str != "X" and r_str != "9":
        X���ڂ̂� = ""
        
    return r_str*int(m_byte)
    
    
def ����_�}���`���C�A�E�g����(P_STR):

    if  " " in P_STR:
       return False
    elif "?" in P_STR:
       return True
    elif P_STR == "XX":
       return False
    elif P_STR == "99":
       return False
    elif P_STR == "ZZ":
       return False
    elif P_STR == "BB":
       return False
    elif P_STR == "PP":
       return False
    elif P_STR == "NN":
       return False
    elif P_STR == "X9" or P_STR == "9X":
       return False
    elif P_STR == "XZ" or P_STR == "ZX":
       return True
    elif P_STR == "XB" or P_STR == "BX":
       return True
    elif P_STR == "XP" or P_STR == "PX":
       return True
    elif P_STR == "XN" or P_STR == "NX":
       return True
    elif P_STR == "9Z" or P_STR == "Z9":
       return True
    elif P_STR == "9B" or P_STR == "B9":
       return True
    elif P_STR == "9P" or P_STR == "P9":
       return True
    elif P_STR == "9N" or P_STR == "N9":
       return True
    elif P_STR == "ZB" or P_STR == "BZ":
       return True
    elif P_STR == "ZP" or P_STR == "PZ":
       return True
    elif P_STR == "ZN" or P_STR == "NZ":
       return True
    elif P_STR == "BP" or P_STR == "PB":   # '�}���`���C�A�E�g�ł͂Ȃ�
       return False
    elif P_STR == "PN" or P_STR == "NP":
       return True
    else:
       return True

def G���ڃo�C�g���v�Z����(AnalyzeSheet):
    
    global byte_each_rows,occurs_each_rows,group_end_each_rows
    global g0byte_flag
    
    row_num = len(AnalyzeSheet)
    byte_each_rows = [0]*row_num
    occurs_each_rows = [1]*row_num
    group_end_each_rows = [row_num]*row_num
    
    row_data_queue = []
    
    now_occurs = 1
    for i in range(row_num):
        level = int(AnalyzeSheet[i][3])
        byte = int(AnalyzeSheet[i][10])
        occurs = int(AnalyzeSheet[i][12])
        
        occurs = max(occurs,1)
        
        while row_data_queue and level <= row_data_queue[-1][0]:
            b_level,b_occurs,b_index = row_data_queue.pop()
            group_end_each_rows[b_index] = i
            now_occurs //= b_occurs
        now_occurs *= occurs
        occurs_each_rows[i] = now_occurs
        byte_each_rows[i] = now_occurs * byte
        row_data_queue.append([level,occurs,i])
            

    child_group = [[] for i in range(row_num)]
    
    row_levels = [[] for i in range(100)]
    for i in range(row_num):
        row_levels[AnalyzeSheet[i][3]].append(i)
        
    level_queue = []
    for i in range(row_num)[::-1]:
  
        
        level = AnalyzeSheet[i][3]
        while level_queue and level_queue[-1][0] > level:
            b_level,b_index = level_queue.pop()
            child_group[i].append(b_index)
        
        if AnalyzeSheet[i][11] != "":
            continue
        level_queue.append([level,i])
    
    
    layout_chk_string_list = [0]*row_num
    layout_chk_string_list_bef_occurs = [0]*row_num
    for i in range(100)[::-1]:
        for index in row_levels[i]:
            tmp_str = 0
            if AnalyzeSheet[index][9] == "":
                tmp_str += int(AnalyzeSheet[index][10])
            for child_index in child_group[index]:
                tmp_str += layout_chk_string_list[child_index]
            layout_chk_string_list_bef_occurs[index] = tmp_str
            if AnalyzeSheet[index][12] > 0:
                tmp_str *= AnalyzeSheet[index][12]
            layout_chk_string_list[index] = tmp_str
        
    
    for i in range(row_num):
        if group_end_each_rows[i] != i+1:
            AnalyzeSheet[i][9] = layout_chk_string_list_bef_occurs[i]
        
        if AnalyzeSheet[i][9] == "" and int(AnalyzeSheet[i][10]) == 0:
            g0byte_flag = True
            
   
       
        
    
    return AnalyzeSheet
    
    
    
def ���׍s���Έʒu��͏���(AnalyzeSheet):
    global byte_each_rows,occurs_each_rows,group_end_each_rows
    global ALL_chk_ok,redefine_flg
    position = 1
    now_occurs = 1
    size_val_dic = {}
    left_byte_size = [0]
    row_num = len(AnalyzeSheet)
    
    occurs_que = []
    for i in range(row_num):
        occurs = occurs_each_rows[i]
        size = AnalyzeSheet[i][10]
        level = int(AnalyzeSheet[i][3])
        def_occurs = int(AnalyzeSheet[i][12])
        val = AnalyzeSheet[i][11]
        # print(i,level,size,def_occurs,val,position,left_byte_size,occurs_que)
        # print(occurs_que)
        while occurs_que and occurs_que[-1][0] >= level:
            blevel,mul = occurs_que.pop()
            last_size = left_byte_size.pop()
            position += last_size * (mul - 1) 
            left_byte_size[-1] += last_size * mul  
        # print(left_byte_size,occurs_que)
        if def_occurs > 1:
            left_byte_size.append(0)
            occurs_que.append([level,def_occurs])
        # elif now_occurs > occurs:
        #     mul = now_occurs // occurs
        #     last_size = left_byte_size.pop()
        #     position += last_size * (mul - 1)
        #     left_byte_size[-1] += last_size * (mul - 1)
        
        if val != "":
            if val not in size_val_dic:
                
                ALL_chk_ok = False
                redefine_flg = True
                print("REDEFINE�ϐ�",val,"�͑��݂��܂���")
            else:
                
                mul = occurs //occurs_each_rows[i] 
                # print(val,size_val_dic[val],mul)
                bsize,bposition = size_val_dic[val]
                position -= bsize * mul
                left_byte_size[-1] -= bsize * mul
                less = bposition - position
                if less > 0:
                    # print(less,"�T�C�Y�s����")
                    position += less
                    left_byte_size[-1] += less
                elif less < 0:
                    print("REDEFINE�T�C�Y�s��")
                    redefine_flg = True
                    ALL_chk_ok = False
                 
        AnalyzeSheet[i][13] = position
        if AnalyzeSheet[i][9] != "":
            size_val_dic[AnalyzeSheet[i][4]] = [AnalyzeSheet[i][9],position]
        else:
            size_val_dic[AnalyzeSheet[i][4]] = [AnalyzeSheet[i][10],position]
        position += size
        left_byte_size[-1] += size
        
        # size_val_dic[AnalyzeSheet[i][4]] = [AnalyzeSheet[i][10]
        
            
            
        now_occurs = occurs
            
    return AnalyzeSheet
            
    
def �P�ƃ}���`���C�A�E�g����(AnalyzeSheet,multicheck_folder):
    
    global ALL_chk_ok,�}���`���C�A�E�g����
    global ���C�A�E�g��͏��_
    global ���C�A�E�g��
    
    row_num = len(AnalyzeSheet)
    child_group = [[] for i in range(row_num)]
    
    row_levels = [[] for i in range(100)]
    for i in range(row_num):
        row_levels[AnalyzeSheet[i][3]].append(i)
        
    level_queue = []
    for i in range(row_num)[::-1]:
  
        
        level = AnalyzeSheet[i][3]
        while level_queue and level_queue[-1][0] > level:
            b_level,b_index = level_queue.pop()
            child_group[i].append(b_index)
        
        if AnalyzeSheet[i][11] != "":
            continue
        level_queue.append([level,i])
    
    
    layout_chk_string_list = [""]*row_num
    layout_chk_string_list_bef_occurs = [""]*row_num
    for i in range(100)[::-1]:
        for index in row_levels[i]:
            tmp_str = ""
            if AnalyzeSheet[index][9] == "":
                tmp_str += MC�����񖾍�(AnalyzeSheet[index][5],AnalyzeSheet[index][6],AnalyzeSheet[index][7],AnalyzeSheet[index][10])
            for child_index in child_group[index]:
                tmp_str += layout_chk_string_list[child_index]
            layout_chk_string_list_bef_occurs[index] = tmp_str
            if AnalyzeSheet[index][12] > 0:
                tmp_str *= AnalyzeSheet[index][12]
            layout_chk_string_list[index] = tmp_str
            
    
    if len(layout_chk_string_list_bef_occurs[0]) != AnalyzeSheet[0][9] and len(layout_chk_string_list_bef_occurs[0]) != int(AnalyzeSheet[0][10]) :
        ALL_chk_ok = False  
        return
    
    redefine_flag = 0
    chk_str1 = layout_chk_string_list[0]
    
    multicheck_list = []
    if multicheck_folder != None:
        multicheck_list.append(chk_str1)
    for i in range(row_num):
        if AnalyzeSheet[i][11] == "":
            continue
        redefine_flag = 1
        pos_start = AnalyzeSheet[i][13]-1
        chk_str2 = layout_chk_string_list_bef_occurs[i]
        # print(AnalyzeSheet[i][4])
        # print(chk_str2)
        # print(pos_start)
        if len(chk_str2)+pos_start > len(chk_str1) or pos_start < 0:
            ALL_chk_ok = False
            # print(pos_start,len(chk_str1),len(chk_str2),chk_str1,chk_str2)
            # print("���R�[�h�����s�����Ă��܂��Bscm�t�@�C�����m�F���Ă��������B",���C�A�E�g��)
            continue
        
        if multicheck_folder != None:
            chk_str2_full = " "*pos_start + chk_str2 + " " * (len(chk_str1) - len(chk_str2) - pos_start)
            multicheck_list.append(chk_str2_full)
        for j in range(len(chk_str2)):
            try:
                if ����_�}���`���C�A�E�g����(chk_str1[pos_start+j]+chk_str2[j]) == True:
                    �}���`���C�A�E�g���� = "YES"
            except:
                print(pos_start)
                print(chk_str2)
                print(chk_str1)
                # exit()
      
    ���C�A�E�g��͏��_.insert(layout_chk_string_list[0])
    if �}���`���C�A�E�g���� != "YES" and redefine_flag:
        �}���`���C�A�E�g���� = "NO"    
    
    if multicheck_folder != None and redefine_flag:
        multicheck_out_path = os.path.join(multicheck_folder,���C�A�E�g�� + "_�P��CHK.txt")
        with open(multicheck_out_path,"w") as f:
            for line in multicheck_list:
                f.write(line + "\n")
    
    return 


# def check_PIC_definition(TokenSheet2_GYO,������):
#     ������ += 1
#     if ������ >= len(TokenSheet2_GYO):
#         print("PIC��`������������܂���B�X�L�[�}�t�@�C�����m�F���Ă��������B")
#         return ������
    
#     global X���ڂ̂�,COPY_�o�C�g��,COPY_�^�C�v,COPY_�T�C��,COPY_����
    
#     while ������ < len(TokenSheet2_GYO):
#         code_val = TokenSheet2_GYO[������]
        
#         ### ���Ԃ��l�� or �ǂꂩ������Ă͂܂�Ƃ��ׂ�����
#         if str(code_val).startswith("V"):
#             code_val = code_val[1:] # V �̓��R�[�h���Ȃǂɂ͊֌W���Ȃ�
        
#         if str(code_val).startswith("."):
#             code_val = code_val[1:]
            
#         if str(code_val).startswith("B"):
#             code_val = code_val[1:]
            
#         #################################
        
#         if ������ + 1 < len(TokenSheet2_GYO) and TokenSheet2_GYO[������ + 1] == "(":
#             code_val = str(code_val).replace("+","").replace("-","").replace("\\","")  ### ( ) ��������`�̂����̋L���̓��R�[�h���Ȃǂɂ͊֌W���Ȃ�
            
#             if code_val not in ("X","A","9","S9"):
#                 print("�z��O��PIC��`",code_val)
#                 print(TokenSheet2_GYO)
                
#             if code_val != "X":
#                 X���ڂ̂� = ""
                
#         else:
            
        
        
        
#         # if code_val in ("USAGE","REDEFINES","RENAMES","OCCURS")
        


    

def structure_Scm(TokenSheet2,ScmSheet,���C�A�E�g, ���O��͗L = True,conn=None, cursor=None,���C�A�E�g_len=0,multicheck_folder=None):

    global COPY_�ϐ�,COPY_���R�[�h��,REDIFINE_����_���x��,OCCOURS_����_���x��,OCCOURS_��,OCCOURS_�o�C�g�J�E���g,COPY_�^�C�v2,X���ڂ̂�,COPY_�T�C��,N���ڗL��,\
            COPY_����,COPY_����_������,COPY_REDIFINE,REDIFINE_�L��,�}���`���C�A�E�g����,VALUE�L��,COPY_���C�u����,�擪���x��,COPY�啪�� ,COPY_�^�C�v,COPY_���x��,COPY_�o�C�g��,COPY_OCCURS,ALL_chk_ok
    
    global ���C�A�E�g��,COPY_���R�[�h��,���C�A�E�g�s��
    global ���C�A�E�g��͏��_
    global depending_on_flag,indexed_by_flag,g0byte_flag,redefine_flg
    
    
    err_info = ""
    depending_on_flag = False
    indexed_by_flag = False
    g0byte_flag = False
    redefine_flg = False
    ���C�A�E�g�� = ���C�A�E�g
    ���C�A�E�g�s�� = ���C�A�E�g_len
    SUB_SQL����_����_1_ = SUB_SQL����_����_1(conn,cursor)
    SUB_SQL����_����_2_ = SUB_SQL����_����_2(conn,cursor)
    �X�L�[�}_��{���_ = �X�L�[�}_��{���(conn,cursor)
    ���C�A�E�g��͏��_ = ���C�A�E�g��͏��(conn,cursor)
    
    ALL_chk_ok = True    #'�V�[�g�P�ʂőS�Ă̐ݒ�p�^�[�����o�^����Ă��邩�ǂ����i�����lTrue�j
    REDIFINE_�L�� = ""
    �}���`���C�A�E�g���� = ""
    X���ڂ̂� = "��"
    N���ڗL�� = ""
    �o�C�i�����ڗL�� = ""   #'�p�~�i20140527�j
    
    # '�ϐ�������
    # 'COPY�� = Replace(���C�A�E�g��, ".scm", "") '�g���q�ɍ��킹�Đݒ�
    COPY�� = ���C�A�E�g��
    COPY_���C�u���� = ""
    COPY_���R�[�h�� = ""
    COPY_���R�[�h�� = 0
    
    REDIFINE_����_���x�� = 0
    OCCOURS_����_���x�� = 0
    
    OCCOURS_�� = 0
    OCCOURS_�o�C�g�J�E���g = 0
    �擪���x�� = ""
    # 'COPY_���Έʒu = 1       '���̌v�Z�����Őݒ肷��

    �����s = 0    #  'TokenSheet2�@�s�|�C���^
    # '���͍sTYPE = "COBOL"  '�uCOBOL�v�uPL/I�v�Ȃ�
    COPY�啪�� = "copy-data" #'�f�t�H���g�l
   
    AnalyzeSheet = []
    
    while �����s < len(TokenSheet2):

        TokenSheet2_GYO = TokenSheet2[�����s]
        if "DEPENDING" in TokenSheet2_GYO:
            depending_on_flag = True
            
        if "INDEXED" in TokenSheet2_GYO:
            indexed_by_flag = True
            
            
        # '�ϐ�������
        COPY_�Ώۍs = �����s
        COPY_���x�� = 0
        COPY_�ϐ� = ""
        COPY_�T�C�� = ""
        COPY_�^�C�v = ""
        COPY_�^�C�v2 = ""
        COPY_���� = 0
        COPY_����_������ = "" #'�ǉ�
        COPY_�o�C�g�� = 0
        COPY_REDIFINE = ""
        COPY_OCCURS = 0
        
        # '20150714 ADD
        �o�C�i�����ڗL�� = "" #'20140527�p�~ ���@201507�����i�W�c���ڂɐݒ�A�z����BINARY�APAC���ڂ����邩�j
        N���ڗL�� = "" #'201507�ǉ��i�W�c���ڂɐݒ�A�z����N���ڂ����邩�j
        VALUE�L�� = "" #'201507�ǉ��i��{���ڂɐݒ�AVALUE�傪���邩�j
        MODE�w��L�� = "" #'201507�ǉ��i��{�E�W�c���ڂɐݒ�A�x�m��COBOL��mode�w��̉e�����󂯂Ă��鍀�ڂɐݒ�j
        # '20150714 ADD END
        
        ������ = 1
        
        while True:
            PARM�s = 0      #'Parm�s�|�C���^
            parm_hit = False
            
            # if ������ < len(TokenSheet2_GYO) and TokenSheet2_GYO[������] == "PIC":
            #     ������ = check_PIC_definition(TokenSheet2_GYO,������)
                
            #     if ������ >= len(TokenSheet2_GYO):
            #         break
                
            while True:
                
                PARM�� = 4     # 'Parm��|�C���^
                hit_flg = True
                parm_cnt = 0
                here = 0
                while PARM�� < len(ScmSheet[PARM�s]):
                    
                    if ScmSheet[PARM�s][1] == "Key101":
                        if ������ >= len(TokenSheet2_GYO):
                            hit_flg = False
                            break
                        code_val = TokenSheet2_GYO[������].replace("V","").replace("9","").replace("S","").replace("Z","").replace("P","").replace(",","").replace("*","").replace(".","").replace("\\","").replace("A","").replace("B","").replace("X","").replace("0","") 
                        if code_val != "" or TokenSheet2_GYO[������] == ".":
                            hit_flg = False
                            break
                        
                        if ������ == 1 or TokenSheet2_GYO[������-1] != ")":
                            hit_flg = False
                            break
                        
                        here = 1
                        
                
                        
                    if ScmSheet[PARM�s][PARM��] != "":
                        parm_cnt = parm_cnt + 1
                    
                    parm_val = ScmSheet[PARM�s][PARM��]
                    code_val = ""
                    if ������+parm_cnt-1 < len(TokenSheet2_GYO):
                        code_val = TokenSheet2_GYO[������+parm_cnt-1]
                        
                    parm_chk = �ݒ�l��v�`�F�b�N(parm_val,code_val)
                    if not (parm_chk):
                        hit_flg = False
                    PARM�� = PARM�� + 1
                    
                    if PARM�� >= len(ScmSheet[PARM�s]) or ScmSheet[PARM�s][PARM��] == "" or hit_flg == False:
                        break
            
                # '�`�F�b�N����
                if hit_flg:
                    parm_hit = True
                    ����ID = ScmSheet[PARM�s][2]
                
                    if ���O��͗L and ����ID != "":
                        �����s������ = �����s�����񐶐�����(TokenSheet2_GYO[1:])  #  '�����J�n��i2��ڂ������ɂ���j
                        SUB_SQL����_����_1_.insert("����ID", "", ���C�A�E�g��, �����s+2, ����ID, �����s������)
                
                else:
                    PARM�s = PARM�s + 1
                
                if PARM�s >= len(ScmSheet) or ScmSheet[PARM�s][1] == "" or parm_hit == True:
                    break
            # '������X�V
            if parm_hit:
                # 'PARM�� = 6
                PARM�� = 4
                # print(TokenSheet2_GYO)
                # print(ScmSheet[PARM�s])
                for i in range(parm_cnt):
                    parm_val = ""
                    if PARM�� + i < len(ScmSheet[PARM�s]):
                        parm_val = ScmSheet[PARM�s][PARM�� + i]
                    code_val = ""
                    if ������+i < len(TokenSheet2_GYO):
                        code_val = TokenSheet2_GYO[������+i]
                        
                    code_val2 = ""
                    if ������+i+1 < len(TokenSheet2_GYO):
                        code_val2 = TokenSheet2_GYO[������+i+1]
                        
                    �ݒ�l��v�F��������_COPY(parm_val,code_val,code_val2)
                
                ������ = ������ + parm_cnt
            else:
                # '����NG����
                ALL_chk_ok = False         # '�ЂƂł�NG������ƃV�[�g�P�ʂ�NG
         
                COPY�啪�� = "copy-source"
            
                if ���O��͗L:
                    # '�����s������쐬
                    �����s������ = �����s�����񐶐�����(TokenSheet2_GYO[1:])   # '�����J�n��i2��ڂ������ɂ���j
                    # 'NG���֘A���o��
                    SUB_SQL����_����_2_.insert("COPY", "", COPY��, �����s+2, �����s������)
                                

                ������ = ������ + 1
            
            if ������ >= len(TokenSheet2_GYO):
                break
        
        # '�o�C�g��
        
        COPY_���R�[�h�� = COPY_���R�[�h�� + �o�C�g�����Z_COPY()
        
        AnalyzeSheet_GYO = [""]*18
        
        AnalyzeSheet_GYO[1] = COPY��
        AnalyzeSheet_GYO[2] = COPY_�Ώۍs
        AnalyzeSheet_GYO[3] = COPY_���x��
        AnalyzeSheet_GYO[4] = COPY_�ϐ�
        AnalyzeSheet_GYO[5] = COPY_�T�C��
        AnalyzeSheet_GYO[6] = COPY_�^�C�v
        AnalyzeSheet_GYO[7] = COPY_�^�C�v2
        AnalyzeSheet_GYO[8] = COPY_����_������
        AnalyzeSheet_GYO[10] = COPY_�o�C�g��
        AnalyzeSheet_GYO[11] = COPY_REDIFINE
        AnalyzeSheet_GYO[12] = COPY_OCCURS
        # AnalyzeSheet_GYO[13] = COPY_���Έʒu  '���̍ĉ�͏������Ōv�Z�E�o��

        AnalyzeSheet_GYO[14] = �o�C�i�����ڗL��
        AnalyzeSheet_GYO[15] = N���ڗL��
        AnalyzeSheet_GYO[16] = VALUE�L��
        AnalyzeSheet_GYO[17] = MODE�w��L��
        AnalyzeSheet.append(AnalyzeSheet_GYO)
        
        �����s = �����s + 1
       
        # 'debug
        # 'if �����s = 4:
        # '    �����s = 4
    
    err_before = False
    if ALL_chk_ok == False:
        err_before = True
        
    AnalyzeSheet = G���ڃo�C�g���v�Z����(AnalyzeSheet)
    AnalyzeSheet = ���׍s���Έʒu��͏���(AnalyzeSheet)
    
    # if REDIFINE_�L�� == "��":
    �P�ƃ}���`���C�A�E�g����(AnalyzeSheet,multicheck_folder)
    
    COPY_���R�[�h�� = AnalyzeSheet[0][9]
    if COPY_���R�[�h�� == "":
        COPY_���R�[�h�� = AnalyzeSheet[0][10]
        
    if err_before:
        err_info = "�G���[: ���@�p�^�[���ΏۊO"
    else:
        err_info = ""
    if depending_on_flag:
        if err_info == "":
            err_info = "�G���[: DEPENDING ON �g�p"
        else:
            err_info += ", DEPENDING ON �g�p"
    
    if indexed_by_flag:
        if err_info == "":
            err_info = "�G���[: INDEXED BY �g�p"
        else:
            err_info += ", INDEXED BY �g�p"
            
    if g0byte_flag:
        if err_info == "":
            err_info = "�G���[: 0byte��G���ڂ���"
        else:
            err_info += ", 0byte��G���ڂ���"
    
    if redefine_flg:
        if err_info == "":
            err_info = "�G���[: REDEFINE�� ��`�Ȃ� or �T�C�Y�s��"
        else:
            err_info += ",  REDEFINE�� ��`�Ȃ� or �T�C�Y�s��"
            
        
    �X�L�[�}_��{���_.insert(err_info)
    
    return AnalyzeSheet
    