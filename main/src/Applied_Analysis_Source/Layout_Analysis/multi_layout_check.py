#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

     
class UTL_STEP��_IO���_DSN�e�[�u��:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "UTL_STEP��_IO���_DSN�e�[�u��"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
        sql = "SELECT * FROM "+self.dbname + " ORDER BY JCL_NAME,JOB_SEQ,STEP_SEQ,IO DESC"
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        keys = df.columns.tolist()
        
        for i in range(len(df)):
            data = df.iloc[i]
            
            jcl_name = data["JCL_NAME"]
            job_seq = data["JOB_SEQ"]
            job_id = data["JOB_ID"]
            step_seq = data["STEP_SEQ"]
            step_name = data["STEP��"]
            utility_id = data["Utility_ID"]
            
            if (jcl_name,job_seq,job_id,step_seq,step_name,utility_id) not in self.dic:
                self.dic[(jcl_name,job_seq,job_id,step_seq,step_name,utility_id)] = []
                
            dic = {key:data[key] for key in keys}
            self.dic[(jcl_name,job_seq,job_id,step_seq,step_name,utility_id)].append(dic)
        
        
    def get(self, jcl_name,job_seq,job_id,step_seq,step_name,utility_id):
        if self.dic == None:
            self.setup()
            
            
        if (jcl_name,job_seq,job_id,step_seq,step_name,utility_id) in self.dic:
            return self.dic[(jcl_name,job_seq,job_id,step_seq,step_name,utility_id)]
        else:
            return []
            
    def _close_conn(self):
        if self.conn != None:
            self.cursor.close()
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
     
     
class QRY_DSN�P��_���C�A�E�g����:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "QRY_DSN�P��_���C�A�E�g����"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
        sql = "SELECT * FROM "+self.dbname + " ORDER BY �f�[�^�Z�b�g�O���[�v�@,DSN��"
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        keys = df.columns.tolist()
        
        for i in range(len(df)):
            data = df.iloc[i]
            
            group_name = data["�f�[�^�Z�b�g�O���[�v�@"]
            dsn = data["DSN��"]
            # print(group_name,dsn)
            if group_name not in self.dic:
                self.dic[group_name] = []
            if dsn not in self.dic:
                self.dic[dsn] = []
                

            dic = {key:data[key] for key in keys}
            self.dic[group_name].append(dic)
            self.dic[dsn].append(dic)
        
        
    def get(self, name):
        if self.dic == None:
            self.setup()
            
            
        if name in self.dic:
            return self.dic[name]
        else:
            return []
            
    def _close_conn(self):
        if self.conn != None:
            self.cursor.close()
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
     
class �X�L�[�}_��{���:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�X�L�[�}_��{���"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        keys = df.columns.tolist()
        
        for i in range(len(df)):
            data = df.iloc[i]
            
            layout = data["���C�A�E�g��"]
            if layout not in self.dic:
                self.dic[layout] = []
                
            dic = {key:data[key] for key in keys}
            self.dic[layout].append(dic)
        
        
    def get(self, name):
        if self.dic == None:
            self.setup()
            
            
        if name in self.dic:
            return self.dic[name]
        else:
            return []
            
    def _close_conn(self):
        if self.conn != None:
            self.cursor.close()
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
     
     
class ���C�A�E�g��͕�����:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "���C�A�E�g��͏��"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        keys = df.columns.tolist()
        
        for layout,layout_string in zip(df["���C�A�E�g��"],df["���C�A�E�g���"]):
            self.dic[layout] = layout_string

    def get(self, name):
        if self.dic == None:
            self.setup()
            
            
        if name in self.dic:
            return self.dic[name]
        else:
            return ""
            
    def _close_conn(self):
        if self.conn != None:
            self.cursor.close()
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
        
  
   
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

      
def �}���`���C�A�E�g��͖��׏���(myRS2,OutSheet_GYO):
    global �X�L�[�}_��{���_,���C�A�E�g��͕�����_
    global OutSheet2,�}���`���C�A�E�g����
    TmpSheet = []
 
    for data in myRS2:
        OutSheet2_GYO = [""]*11
        
        OutSheet2_GYO[1] = data["�f�[�^�Z�b�g�O���[�v�@"]
        OutSheet2_GYO[2] = data["DSN��"]
        OutSheet2_GYO[3] = data["���C�A�E�g��"]

        PARM2 = data["���C�A�E�g��"]

        if PARM2 != "":

            myRS3_all = �X�L�[�}_��{���_.get(PARM2)
            if myRS3_all == []:
                OutSheet_GYO[5] = "��͏��"
                OutSheet2_GYO[10] = "�Y�����郌�C�A�E�g���͑��݂��܂���"
                OutSheet2.append(OutSheet2_GYO)
                
                continue
            
            for myRS3 in myRS3_all:    
                OutSheet2_GYO = [""]*11
        
                OutSheet2_GYO[1] = data["�f�[�^�Z�b�g�O���[�v�@"]
                OutSheet2_GYO[2] = data["DSN��"]
                OutSheet2_GYO[3] = data["���C�A�E�g��"]
                OutSheet2_GYO[4] = myRS3["���R�[�h��"]
                OutSheet2_GYO[5] = myRS3["���R�[�h��"]
                OutSheet2_GYO[6] = myRS3["�}���`���C�A�E�g����"]
                if myRS3["�}���`���C�A�E�g����"] == "YES":
                    OutSheet_GYO[4] = "�L"
                    �}���`���C�A�E�g���� = "YES"
                
                OutSheet2_GYO[7] = myRS3["REDIFINE�L��"]
                OutSheet2_GYO[8] = myRS3["X���ڂ̂�"]
                OutSheet2_GYO[9] = myRS3["���C�A�E�g�s��"]
                if OutSheet2_GYO[10] == "":
                    OutSheet2_GYO[10] = myRS3["�G���[���"]
                TmpSheet.append(���C�A�E�g��͕�����_.get(PARM2))
                OutSheet2.append(OutSheet2_GYO)
                
    return TmpSheet,OutSheet_GYO

        
def muiti_layout_main(db_path,title,�}���`���C�A�E�g�`�F�b�N�P��="�@�f�[�^�Z�b�g�O���[�v"):
    
    global OutSheet2,�}���`���C�A�E�g����
    global �X�L�[�}_��{���_,���C�A�E�g��͕�����_
    conn = connect_accdb(db_path)
    cursor = conn.cursor()
    
    QRY_DSN�P��_���C�A�E�g����_ = QRY_DSN�P��_���C�A�E�g����(conn,cursor)
    �X�L�[�}_��{���_ = �X�L�[�}_��{���(conn,cursor)
    ���C�A�E�g��͕�����_ = ���C�A�E�g��͕�����(conn,cursor)
    OutSheet = []
    OutSheet2 = []
    
    if �}���`���C�A�E�g�`�F�b�N�P�� == "�@�f�[�^�Z�b�g�O���[�v":
        qry = "QRY_DSN�O���[�v�P��_���C�A�E�g����"
    else:
        qry = "QRY_DSN�P��_���C�A�E�g����"
        
    sql = "SELECT * FROM " + qry
    
    df = pd.read_sql(sql,conn)
    for i in range(len(df)):
        data = df.iloc[i]
        
        if �}���`���C�A�E�g�`�F�b�N�P�� == "�@�f�[�^�Z�b�g�O���[�v":
            ��͒P�� = data["�f�[�^�Z�b�g�O���[�v�@"]
        else:
            ��͒P�� = data["DSN��"]
        
        if "&" in ��͒P��:
            continue
            
        OutSheet_GYO = [""]*6
        OutSheet_GYO[1] = ��͒P��
        OutSheet_GYO[2] = data["CNT"]
        
        PARM = ��͒P��
        ���C�A�E�g�� = int(OutSheet_GYO[2])
        �}���`���C�A�E�g���� = "NO"
        
        myRS2 = QRY_DSN�P��_���C�A�E�g����_.get(PARM)
        
        if myRS2 == []:
            OutSheet_GYO[3] = "NO"
            OutSheet_GYO[5] = "��͏��"
            OutSheet.append(OutSheet_GYO)
            continue
        
        TmpSheet,OutSheet_GYO = �}���`���C�A�E�g��͖��׏���(myRS2,OutSheet_GYO)

        if �}���`���C�A�E�g���� == "YES":
            OutSheet_GYO[3] = "YES"
            OutSheet.append(OutSheet_GYO)
            continue
        
        for i in range(len(TmpSheet)-1):
            l_str1 = TmpSheet[i]
            l_str2 = TmpSheet[i+1]
            
            if len(l_str1) != len(l_str2):
                if OutSheet_GYO[5] == "��͏��":
                    OutSheet_GYO[5] == "��͏��" + "\n" + "���R�[�h���s����"
                # elif "���R�[�h��" in OutSheet_GYO[5]:
                #     pass
                else:
                    OutSheet_GYO[5] = "���R�[�h���s����"

                �}���`���C�A�E�g���� = "YES"
                break
                
            for j in range(len(l_str1)):
                if ����_�}���`���C�A�E�g����(l_str1[j] + l_str2[j]):
                    �}���`���C�A�E�g���� = "YES"
            if �}���`���C�A�E�g���� == "YES":
                break
        
        OutSheet_GYO[3] = �}���`���C�A�E�g����
        OutSheet.append(OutSheet_GYO)
                    
                

            
    ActSheet_all = [actSheet[1:] for actSheet in OutSheet]
    output_header = ["��͒P��","��̓��C�A�E�g��","�}���`���C�A�E�g����","�P�̃��x���}���`���C�A�E�g�L��","�G���[���"]
    write_excel_multi_sheet("�}���`���C�A�E�g��͌���(�T�}��).xlsx",ActSheet_all,"�}���`���C�A�E�g��͌���(�T�}��)",title,output_header)
    
    ActSheet_all = [actSheet[1:] for actSheet in OutSheet2]
    output_header = ["�f�[�^�Z�b�g�O���[�v�@","DSN��","���C�A�E�g���","���R�[�h��","���R�[�h��","�}���`���C�A�E�g����","�Ē�`�L��","�w���ڂ̂�","���C�A�E�g�s��","�G���[���"]
    write_excel_multi_sheet("�}���`���C�A�E�g��͌���(����).xlsx",ActSheet_all,"�}���`���C�A�E�g��͌���(����)",title,output_header)
    
if __name__ == "__main__":
    muiti_layout_main(sys.argv[1],sys.argv[2])