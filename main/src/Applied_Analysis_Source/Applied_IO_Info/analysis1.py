#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


���p_�ڋq��_JCL_PGM_DSN_ = None
���o�͔���_IMSDB_ = None
#'20240214 ADD qian.e.wang
���o�͔���_ADABAS_ = None
#'ADD END
GET_PROC_PGM_ = None
DATA_DSN�ʃf�[�^���ޏ��_ = None
�ϐ��l�␳_ = None
Select_BMCP_PGM_ = None
���o�͔���_ = None
ActSheet = []
ActSheet_x = []
JCL_NAME_WK = ""
PGM_NAME = ""
STEP_SEQ = 0
JCL_NAME_SV = ""
JOB_SEQ_SV = ""
STEP_SEQ_SV = 0
PROC_ID = ""
���������� = []
����������2 = []

PGM_SYSIN = ""
L_GDG = ""
L_DISP = ""
L_SYSIN = ""
L_DSN = ""
L_SCHEMAKUBUN = ""
P_�f�[�^��� = ""
#'20240614 DELETE jiaqi.chen
# P_���o�͔��� = ""
#'20240614 DELETE 
TMP_DSN = ""
PGM_PROC = ""
BMCP_PGM = ""
parm = ""
vbCrLf = "\n"

class ���p_�ڋq��_JCL_PGM_DSN:
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
        keys = df.columns.tolist()
        for i in range(len(df)):
            data = df.iloc[i]
            jcl,job,step = data["JCL_NAME"],data["JOB_SEQ"],data["STEP_SEQ"]
            dic = {key:data[key] for key in keys}
            
            if (jcl,job,step) not in self.dic:
                self.dic[(jcl,job,step)] = []
            self.dic[(jcl,job,step)].append(dic)
            
            if (jcl,job) not in self.dic:
                self.dic[(jcl,job)] = []
            self.dic[(jcl,job)].append(dic)
        
            

    def get(self,JCL_NAME,JOB_SEQ,STEP_SEQ=None):
        if self.dic == None:
            self.setup()
        
        
        if STEP_SEQ == None:
            if (JCL_NAME,JOB_SEQ) in self.dic:
                return self.dic[(JCL_NAME,JOB_SEQ)]
            else:
                return []
            
        if (JCL_NAME,JOB_SEQ,STEP_SEQ) in self.dic:
            return self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ)]
        else:
            return []
        

class ���o�͔���_IMSDB:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "QRY_JCL_PGM_DSN_IMSDB_SEG���p��"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for jcl,job,step,sysin_pgm,dsn2,io in zip(df["JCL_NAME"],df["JOB_SEQ"],df["STEP_SEQ"],df["SYSIN_PGM"],df["DSN2"],df["���o�͋敪"]):
            if (jcl,job,step,sysin_pgm,dsn2) not in self.dic:
                self.dic[(jcl,job,step,sysin_pgm,dsn2)] = 0
            if io == "DLI_I-O":
                self.dic[(jcl,job,step,sysin_pgm,dsn2)] = 1
                


    def get(self,P_PGM, P_JCL, JOB_SEQ, STEP_SEQ, DSN):
        if self.dic == None:
            self.setup()
        
        
        if (P_JCL,JOB_SEQ,STEP_SEQ,P_PGM,DSN) in self.dic:
            update = self.dic[(P_JCL,JOB_SEQ,STEP_SEQ,P_PGM,DSN)]
            if update == 1:
                return "I-O" # SEGMENT���p�L�ASEGMENT�X�V�����L
            else:
                return "INPUT" # SEGMENT���p�L�ASEGMENT�X�V������
        else:
            return "���g�p" # SEGMENT���p��
   
#'20240214 ADD qian.e.wang
class ���o�͔���_ADABAS:
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
        
        for sub,pgm,dsn,io in zip(df["�f�[�^����"],df["�f�[�^ID"],df["DSN"],df["IO����"]):
            self.dic[(sub,pgm,dsn)] = io

    def get(self,P_�f�[�^���, P_PGM, DSN):
        if self.dic == None:
            self.setup()
        
        if (P_�f�[�^���,P_PGM,DSN) in self.dic:
            update = self.dic[(P_�f�[�^���,P_PGM,DSN)]
            if update == "":
                return "���ݒ�"  # ADABAS���p�L
            else:
                return update    # ADABAS���p�L
        else:
            return "���g�p"      # ADABAS���p��
#'ADD END
   
class GET_PROC_PGM:
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
        df.fillna("",inplace=True)
        
        for jcl,job,step,pgm in zip(df["JCL_NAME"],df["JOB_SEQ"],df["STEP_SEQ"],df["PGM_NAME"]):
            if pgm != "":
                self.dic[(jcl,job,step)] = pgm
                


    def get(self,P_JCL,P_JOB_SEQ,P_STEP_SEQ):
        if self.dic == None:
            self.setup()
        
        if (P_JCL,P_JOB_SEQ,P_STEP_SEQ) in self.dic:
            return self.dic[(P_JCL,P_JOB_SEQ,P_STEP_SEQ)]
        else:
            return ""
    
    
class DATA_DSN�ʃf�[�^���ޏ��:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "DATA_DSN�ʃf�[�^���ޏ��"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for dsn,data,sub_info in zip(df["DSN"],df["�f�[�^����"],df["�⑫"]):
            self.dic[dsn] = [data,sub_info]


    def get(self,P_DSN):
        if self.dic == None:
            self.setup()
        
        if P_DSN in self.dic:
            return self.dic[P_DSN] ### return �f�[�^����,�⑫
        else:
            return "",""
    
    
class �ϐ��l�␳:
    def __init__(self,conn,cursor):
        self.dic = None
        self.dic2 = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�ڋq��_JCL_STEP���"
        self.dbname2 = "�ڋq��_PROC_PARM"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for jcl,job,step,var,value in zip(df["JCL_NAME"],df["JOB_SEQ"],df["STEP_SEQ"],df["PARM_VAR_LIST"],df["PARM_VALUE_LIST"]):
            if var != "":
                self.dic[(jcl,job,step)] = [var,value]
                
        
    def setup2(self):
        self.dic2 = {}
        sql = "SELECT * FROM "+self.dbname2
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for proc,var,value in zip(df["PROC_ID"],df["PARM_KEY"],df["PARM_VALUE"]):
            if proc not in self.dic2:
                self.dic2[proc] = []
            self.dic2[proc].append([var,value])
                

    def get(self,P_DSN, P_JCL, P_JOB_SEQ, P_STEP_SEQ, P_PROC):
        if self.dic == None:
            self.setup()
            
        global ����������,����������2
        
        if (P_JCL, P_JOB_SEQ, P_STEP_SEQ) in self.dic:
            var,value = self.dic[(P_JCL, P_JOB_SEQ, P_STEP_SEQ)]
            ���������� = ArrayEmptyDelete(var.split(" "))
            ����������2 = ArrayEmptyDelete(value.split(" "))
            for i in range(len(����������)):
                L_tmp_str1 = "&" + ����������[i]
                L_tmp_str2 = ����������2[i]
            
                # 'P_DSN = Replace(P_DSN, "&" & ����������(i) & ".", ����������2(i))
                P_DSN = P_DSN.replace(L_tmp_str1, L_tmp_str2)
                
            return P_DSN.replace("\"","")
        
        
        if self.dic2 == None:
            self.setup2()
            
        if P_PROC in self.dic2:
            myRS3 = self.dic2[P_PROC]
            for var,value in myRS3:
                L_tmp_str1 = "&" + var
                L_tmp_str2 = value
                P_DSN = P_DSN.replace(L_tmp_str1, L_tmp_str2)
        
        return P_DSN.replace("\"","")
    
    
class Select_BMCP_PGM:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "BMCP_PGM���"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for jcl,job,ste,pgm,sysin,bmcp in zip(df["JCL_NAME"], df["JOB_SEQ"], df["STEP_SEQ"], df["PGM_NAME"], df["SYSIN_PGM"],df["BMCP_PGM"]):
            if (jcl,job,ste,pgm,sysin) not in self.dic:
                self.dic[(jcl,job,ste,pgm,sysin)] = []
            self.dic[(jcl,job,ste,pgm,sysin)].append(bmcp)


    def get(self,JCL_NAME, JOB_SEQ, STEP_SEQ, PGM_NAME, SYSIN_PGM):
        if (isBMCP_PGM(PGM_NAME) or (PGM_NAME == "UTACH" and isBMCP_PGM(SYSIN_PGM))) == False:
            return ""
        
        if self.dic == None:
            self.setup()
        
        if (JCL_NAME, JOB_SEQ, STEP_SEQ, PGM_NAME, SYSIN_PGM) in self.dic:
            bmcp_name = self.dic[(JCL_NAME, JOB_SEQ, STEP_SEQ, PGM_NAME, SYSIN_PGM)]
            # if len(bmcp_name) > 1:
                # print("����BMCP_PGM������?�v�m�F" + 
                #           "JCL : " + str(JCL_NAME) + vbCrLf +
                #           "JOB_SEQ : " + str(JOB_SEQ) + vbCrLf +
                #           "STEP_SEQ : " + str(STEP_SEQ) + vbCrLf +
                #           "PGM_NAME : " + str(PGM_NAME) + vbCrLf +
                #           "SYSIN_PGM : " + str(SYSIN_PGM))
            return bmcp_name[0]
                
            
        else:
            return "" # �b��Ƃ��ċ󕶎����Ԃ�
    
    
    
class ���o�͔���:
    def __init__(self,conn,cursor):
        self.dic = None
        self.dic2 = None
        self.dic3 = None
        self.dic4 = None
        self.dic5 = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "UTL_Utility_IO���"
        self.dbname2 = "���o�͔���"
        self.dbname3 = "�ڋq��_PGM_IO���"
        self.dbname4 = "UTL_STEP��_IO���"
        self.dbname5 = "UTL_DD��_IO���"
#'20240209 ADD qian.e.wang
        self.dic6 = None
        self.dbname6 = "�y�b��zJFE_DATA�֘A���ݒ�"
#'ADD END
        # self.db_path = db_path

    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
        
    def setup(self):
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname + " ORDER BY IO DESC"
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for util,dd,io in zip(df["Utility_ID"],df["DD��"],df["IO"]):
            if (util,dd) not in self.dic:
                self.dic[(util,dd)] = io
                

                
    def setup2(self):
        self.dic2 = {}

        sql = "SELECT * FROM "+self.dbname2 + " ORDER BY ���o�͋敪 DESC"
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for type,asset,assign,io in zip(df["���Y����"],df["COBOL_ID"],df["ASSIGN_ID"],df["���o�͋敪"]):
            if type != "COBOL":
                continue
            if (asset,assign) not in self.dic2:
                self.dic2[(asset,assign)] = io
 
        
    def setup3(self):
        self.dic3 = {}

        sql = "SELECT * FROM "+self.dbname3 + " ORDER BY ���o�͋敪 DESC"
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for asset,file,io in zip(df["���YID"],df["�t�@�C����"],df["���o�͋敪"]):
            if (asset,file) in self.dic3:
                continue
            self.dic3[(asset,file)] = io
            
    def setup4(self):
        self.dic4 = {}

        sql = "SELECT * FROM "+self.dbname4 + " ORDER BY IO DESC"
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for jcl,job,step,dd,io in zip(df["JCL_NAME"],df["JOB_SEQ"],df["STEP_SEQ"], df["DD��"],df["IO"]):
            if (jcl,job,step,dd) not in self.dic4:
                self.dic4[(jcl,job,step,dd)] = io
            

        
    def setup5(self):
        self.dic5 = {}

        sql = "SELECT * FROM "+self.dbname5 + " ORDER BY IO DESC"
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for dd,io in zip(df["DD��"],df["IO"]):
            if dd not in self.dic5:
                self.dic5[dd] = io
            
#'20240209 ADD qian.e.wang
    def setup6(self):
        self.dic6 = {}

        sql = "SELECT * FROM "+self.dbname6
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
        for asset,file,io in zip(df["�f�[�^ID"],df["DSN"],df["IO����"]):
            if (asset,file) in self.dic6:
                continue
            self.dic6[(asset,file)] = io
#'ADD END
            
    def �b�蔻��(self, ���o��,P_PGM,PGM_SYSIN,P_DD,dsn):
        if ���o�� != "":
            return ���o��
        #Utility�ʌŒ菈��
        if P_PGM == "KDJBR14" or P_PGM == "IEFBR14":
            ���o�� = "�Ή��s�v"
        elif PGM_SYSIN == "DFSURRL0" or PGM_SYSIN == "DFSURRL0":
            ���o�� = "�p�~"
        #   'DD_NAME��"SYSIN"����
        if P_DD == "SYSIN" and dsn != "":
            ���o�� = "INPUT"
            
        return ���o��
        
                


    def get(self,P_PGM, P_DD, P_SYSIN, P_JCL, P_STEP, JOB_SEQ, STEP_SEQ, dsn, PGM��):    
        global ����������,����������2
        global PGM_SYSIN,L_DSN,P_�f�[�^���
        
        if self.dic == None:
            self.setup()
        
        # 1UTL�EASM�EPLI
        if (P_PGM,P_DD) in self.dic: 
            ���o�� = self.dic[(P_PGM,P_DD)]
            return self.�b�蔻��(���o��,P_PGM,PGM_SYSIN,P_DD,dsn)
        
        #     2�N����Utility
        #     P_PGM��SYSIN_PGM���D�悳��邽�߁ASYSIN_PGM�ł̗��p�ł͂Ȃ��N����Utility��DD�̏ꍇ���肳��Ȃ�
        #     ���ׂ̈����ŋN����Utility��DD��IO������s���B
        if (PGM��,P_DD) in self.dic:  
            ���o�� = self.dic[(PGM��,P_DD)]
            return self.�b�蔻��(���o��,P_PGM,PGM_SYSIN,P_DD,dsn)
        
        
        
        # 3 ���C��COBOL�@�T�uCOBOL�@EASY�̃T�u���[�`���Ή�
        #  ���o�͔���̌�TABLE�́u�ڋq��_PGM_IO���v�u�ڋq��_COBOL_���o�͏��1_1�v
        
        if self.dic2 == None:
            self.setup2()
        
        if (P_PGM,P_DD) in self.dic2:
            ���o�� = self.dic2[(P_PGM,P_DD)]
            return self.�b�蔻��(���o��,P_PGM,PGM_SYSIN,P_DD,dsn)
        
        
        # 4 PGM���Y�Ɖ�͍�DD
        ### sql �� like ���̍������͓���̂ŁA������������ sql�𔭍s����
        Cmd_A = """SELECT ���Y����,���YID,ASSIGN_ID,���o�͋敪 
                    FROM ���o�͔��� WHERE ���Y���� = 'COBOL' AND 
                    ���YID LIKE '"""
        
        Cmd_B = """*' AND ASSIGN_ID = '"""
        tempPgmStr = P_PGM 
        sql = Cmd_A + tempPgmStr + Cmd_B + P_DD + """'"""
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        if len(df) > 0:
            ���o�� = df.iloc[0]["���o�͋敪"]
            return self.�b�蔻��(���o��,P_PGM,PGM_SYSIN,P_DD,dsn)
            
        # 5 DB2,IMSDB�Ή�
        if self.dic3 == None:
            self.setup3()
            
            
        if P_�f�[�^��� == "DB2_TABLE" and "." in dsn:
            ���������� = dsn.split(".")
            L_DSN = ����������[1]
        else:
            L_DSN = dsn
                 
        if (P_PGM,L_DSN) in self.dic3:
            ���o�� = self.dic3[(P_PGM,L_DSN)]
            return self.�b�蔻��(���o��,P_PGM,PGM_SYSIN,P_DD,dsn)
        
        
        # 6 STEP�ʂɐݒ肳�ꂽDD
        if self.dic4 == None:
            self.setup4()
        
        if (P_JCL,JOB_SEQ,STEP_SEQ,P_DD) in self.dic4:
            ���o�� = self.dic4[(P_JCL,JOB_SEQ,STEP_SEQ,P_DD)]
            return self.�b�蔻��(���o��,P_PGM,PGM_SYSIN,P_DD,dsn)
        
        
        # 7 DD�ʂɐݒ肳�ꂽIO
        if self.dic5 == None:
            self.setup5()
        
        if P_DD in self.dic5:
            ���o�� = self.dic5[P_DD]
            return self.�b�蔻��(���o��,P_PGM,PGM_SYSIN,P_DD,dsn)
        
#'20240209 ADD qian.e.wang
        # 8 ADABAS�Ή�
        if self.dic6 == None:
            self.setup6()
            
        # DEBUG
        # print("���B �f�[�^��� :["+str(P_�f�[�^���)+"] DSN :["+str(L_DSN)+"]\r\n")
        if P_�f�[�^��� == "ADABAS":
            ���o�� = self.dic6[(P_PGM,L_DSN.replace("ADABAS:", "").replace("(�ݒ薳)", "").replace("(" + P_PGM + ")", ""))]
            return ���o��
#'ADD END
        
        return self.�b�蔻��("",P_PGM,PGM_SYSIN,P_DD,dsn)
        
    
def ���o�͔���_DISP����(P_INOUT, P_DISP):

    ���o�͔���_DISP = P_INOUT
    
    if P_INOUT == "BK-INPUT" or P_INOUT == "INPUT_���菜�O":
       ���o�͔���_DISP = "INPUT"
    elif P_INOUT == "BK-OUTPUT":
       ���o�͔���_DISP = "OUTPUT"
    elif P_DISP == "M,D":
       ���o�͔���_DISP = "DELETE"
    elif P_DISP == "O,D":
       ���o�͔���_DISP = "INPUT-DELETE"
    elif P_INOUT == "�p�~" or P_INOUT == "�Ή��s�v" or P_INOUT == "���g�p":
       ���o�͔���_DISP = "����ΏۊO"
    elif P_DISP == ",K,D":
       ���o�͔���_DISP = "OUTPUT"
    elif P_DISP == ",P":
       ���o�͔���_DISP = "OUTPUT"
    elif P_DISP != "":
        ���������� = P_DISP.split(",")
        if ����������[0] == "M" and P_INOUT == "OUTPUT":
            ���o�͔���_DISP = "I-O"
        elif ����������[0] == "O" and P_INOUT == "OUTPUT":
            ���o�͔���_DISP = "I-O"
        elif ����������[0] == "S" and P_INOUT == "OUTPUT":
            ���o�͔���_DISP = "I-O"
            
    return ���o�͔���_DISP
 
     
def �f�[�^��ʔ���(P_DSN, P_GDG, P_SYSIN,P_SCHEMAKUBUN,P_PGM):
    global DATA_DSN�ʃf�[�^���ޏ��_
    global P_�f�[�^���
    global ActSheet_x
    # '�ڋq���Ƀ��W�b�N�����C����i���݂�LION�b��o�[�W�����j
        
    if P_GDG != "":
        �f�[�^��� = "GDG"
    elif P_SYSIN != "":
        # '���R�ʉ^ SYSIN�������݂���ꍇ�A�f�[�^��ʔ��� = "PAM" HP�� 2013/11/26
        # '�f�[�^��ʔ��� = "SYSIN"
        �f�[�^��� = "PDS"
    else:

#'20240214 UPD qian.e.wang
        #data,sub_info = DATA_DSN�ʃf�[�^���ޏ��_.get(P_DSN)
        data,sub_info = DATA_DSN�ʃf�[�^���ޏ��_.get(P_DSN.replace("ADABAS:", "").replace("(�ݒ薳)", "").replace("(" + P_PGM + ")", ""))
        �f�[�^��� = data
        # DEBUG
        # print("���@ �f�[�^��� :["+str(�f�[�^���)+"] DSN :["+str(P_DSN)+"]\r\n")
#'UPD END

        # 'DSN��"DUMMY"�̏ꍇ �f�[�^��ʔ��� = "DUMMY"
        if �f�[�^��� != "":
            if �f�[�^��� == "IMSDB" or �f�[�^��� == "IMSDB_���g�p":
                ActSheet_x[17] = sub_info
                # 'ActSheet_x[14] = ActSheet_x[14] & " �� " & myRS3!�⑫    'DSN��DB�����t�^
        elif P_DSN == "DUMMY":
            �f�[�^��� = "DUMMY"
        elif "&&" in P_DSN:
            �f�[�^��� = "�ꎞDSN"
        elif "IMSF." in P_DSN:
            �f�[�^��� = "IMS�֘A"
        else:
            if P_SCHEMAKUBUN == "":
                �f�[�^��� = "NON-VSAM"
            else:
                �f�[�^��� = P_SCHEMAKUBUN
                
    if (�f�[�^��� != "�ꎞDSN") and ("&" in P_DSN) and ("�ϐ�" not in �f�[�^���):
        if �f�[�^��� != "NON-VSAM":
            �f�[�^��� = �f�[�^��� + "_�ϐ�"
        else:
            �f�[�^��� = "�ϐ�"
 
    P_�f�[�^��� = �f�[�^���
    
    return �f�[�^���

    
def DSN���Ȃ�������(ActSheet_x,data):
    
    global JCL_NAME_WK,STEP_SEQ_SV,PROC_ID
    global ActSheet
    ### ��{�I�ɂ́A��͏����̍ŏ��ɏ������܂�Ă��ĕs�v
    
    if STEP_SEQ_SV > 0:
        ActSheet_x[11] = PROC_ID
    else:
        ActSheet_x[11] = data["PROC��"]

    ActSheet_x[35] = JCL_NAME_WK ### �ԈႢ?
    ###MHI�p�b�� �I��
    
    ActSheet.append(ActSheet_x)
            
            
def DSN���L�莞����(P_PARAM,data,data2):
    global ActSheet,ActSheet_x
    global JCL_NAME_WK,PGM_NAME,STEP_SEQ,JCL_NAME_SV,JOB_SEQ_SV,STEP_SEQ_SV,PROC_ID
    global PGM_SYSIN,L_GDG,L_DISP,L_SYSIN,L_SCHEMAKUBUN,P_�f�[�^���,TMP_DSN,PGM_PROC,BMCP_PGM,parm
    global ����������
    global ���o�͔���_IMSDB_,GET_PROC_PGM_,�ϐ��l�␳_,Select_BMCP_PGM_,���o�͔���_
    #'20240614 ADD jiaqi.chen
    P_���o�͔��� = ""
    #'ADD END

    #  'step_seq = step_seq + 1
    ActSheet_x = [""]*45
    
    
    # 'JCL-STEP�����]�L
    ActSheet_x[1] = data["TEST_ID"]
    ActSheet_x[2] = data["JCL_SEQ"]
    ActSheet_x[3] = data["JCL_ID"]
    ActSheet_x[4] = data["LIBRARY"]
    ActSheet_x[5] = data["JOB_SEQ"]
    ActSheet_x[6] = data["JOB_ID"]
    ActSheet_x[7] = data["STEP_SEQ"]
    
    ActSheet_x[10] = PGM_NAME              #     '2019/9/13�@�ǉ�
    
    ActSheet_x[12] = data2["SYSIN_PGM"]
    
    #     '20220215��13-44�̈ʒu1�Âړ�
    ActSheet_x[14] = data2["DD_NAME"]  #  '13��14 
    ActSheet_x[15] = data2["DSN"] #                      '14��15
    ActSheet_x[16] = data2["GDG"]#                      '15��16
    ActSheet_x[17] = data2["SYSIN"]#                    '16��17
    
    ActSheet_x[24] = data2["DISP"] #                    '20��23��24
    ActSheet_x[25] = data2["SYSOUT"]#                   '21��24��25
    ActSheet_x[26] = data2["WRITER"]#                   '22��25��26
    ActSheet_x[27] = data2["FORM"]#                     '23��26��27
    ActSheet_x[28] = data2["UNIT"]#                     '24��27��28
    ActSheet_x[29] = data2["VOL"]#   'VOL���o�ǉ�       '25��28��29
    ActSheet_x[30] = data2["SPACE_Q"]#                  '26��29��30
    ActSheet_x[31] = data2["DCB_RECFM"]#                '27��30��31
    ActSheet_x[32] = data2["DCB_LRECL"]#                '28��31��32
    ActSheet_x[33] = data2["DCB_BLKSIZE"]#              '29��32��33
    ActSheet_x[34] = data2["LABEL"] #'LABEL���o�ǉ�  '30��33��34
    
    #'MHI�p�b�� �J�n
    ActSheet_x[35] = JCL_NAME_WK      #  '34��35
    # 'MHI�p�b�� �I��
    
    # '�Ԋu������������̈Č��Œ�������
    ActSheet_x[41] = data2["PGM�\��"]   #               '2020/4/30 ADD��41
    ActSheet_x[42] = data2["���s���[�h"] #              '2020/4/30 ADD��42
                
    PGM_SYSIN = data2["SYSIN_PGM"]#                                          '12
    L_GDG = data2["GDG"]
    L_SYSIN = data2["SYSIN"]
    L_DISP = data2["DISP"]
    
    # '���������@�b�蒲�����W�b�N�@��������
    # 'if data2["DSN = "DUMMY":
    # '   err_msg = ""
    # 'End if
    # '���������@�b�蒲�����W�b�N�@��������
    if data2["�蓮�X�VFLG"] == "DEFAULT":
        L_SCHEMAKUBUN = ""
    elif data2["�蓮�X�VFLG"].startswith("DAM"):
        L_SCHEMAKUBUN = "DAM"
    elif data2["�蓮�X�VFLG"].startswith("DB"):
        L_SCHEMAKUBUN = "NDB"
    elif data2["�蓮�X�VFLG"].startswith("AIM"):
        L_SCHEMAKUBUN = "AIM"
    elif data2["�蓮�X�VFLG"].startswith("VICS") or data2["�蓮�X�VFLG"].startswith("�VVICS"):
        L_SCHEMAKUBUN = "VICS"
    elif data2["�蓮�X�VFLG"].startswith("���̑���"):
        L_SCHEMAKUBUN = "���̑���"
    else:
        L_SCHEMAKUBUN = ""
    

    if data2["DSN"] != "":
        ##'�f�[�^��ʔ��� & �f�[�^�������擾
        P_�f�[�^��� = ""          #             '������
        if data2["DD_NAME"] == "_SYSI001":
            ActSheet_x[19] = "IMSDB_SEGMENT"   #     '18��19
            P_�f�[�^��� = "IMSDB_SEGMENT"
        # 'elif data2["DD_NAME = "_SYSM001":             '�f�[�^��ʔ���̒���DB�̃Z�b�g���s���Ă���̂Œ��ڎw��͂��Ȃ�
        # '   ActSheet_x[18] = "IMSDB"
        # '   P_�f�[�^��� = "IMSDB"
        # '
        elif data2["DD_NAME"] == "_SYST001" or data2["DD_NAME"] == "_SYST002":
            ActSheet_x[19] = "DB2_TABLE"         #   '18��19
            if "." in data2["DSN"]:   # '�X�L�[�}�t���̏ꍇ�̓X�L�[�}�͏���
                
                ���������� = data2["DSN"].split(".")
                ActSheet_x[15] = ����������[1]    #   '14��15
            P_�f�[�^��� = "DB2_TABLE"         #                      '���o�͔��莞�ɗ��p����̂őޔ�
        elif data2["DD_NAME"] == "STEPLIB":
            ActSheet_x[19] = "PDS"              #   '18��19
        else:
            ActSheet_x[19] = �f�[�^��ʔ���(data2["DSN"], L_GDG, L_SYSIN,L_SCHEMAKUBUN, data2["PGM_NAME"])

        # '�ϐ��l�␳����
        if "�ϐ�" in P_�f�[�^���:
            ActSheet_x[40] = data2["DSN"] #  '���̒l��ޔ��i�m�F�p�j39��40
            TMP_DSN = �ϐ��l�␳_.get(data2["DSN"], data["JCL_ID"], data["JOB_SEQ"], data["STEP_SEQ"], data["PROC��"])# '������PROC_ID�ǉ�
            ActSheet_x[15] = TMP_DSN         #       '14��15
        
            #'�f�[�^��ʍĔ���i��������j
            if "&" not in TMP_DSN: # '�ϐ��l���Ȃ��Ȃ��Ă����ꍇ,�Ĕ���
                ActSheet_x[19] = �f�[�^��ʔ���(TMP_DSN, L_GDG, L_SYSIN,L_SCHEMAKUBUN, data2["PGM_NAME"])   #  '18��19

        #'PROC��PGM���␳����
        if PGM_SYSIN == "" and data["PGM��"] == "":
            #'PGM_PROC = GET_PROC_PGM(data["JCL_ID, data["JOB_SEQ, data["STEP_SEQ)
            PGM_PROC = GET_PROC_PGM_.get(JCL_NAME_SV, JOB_SEQ_SV, STEP_SEQ_SV)
            ActSheet_x[11] = PGM_PROC   #  '���o�͗�̂��ς�����ꍇ�ɒ��ӂ��邱��
        else:
            ActSheet_x[11] = data["PGM��"]
            
        # '=========================================================
        # '20210607 Add Horiuchi
        # 'Batch Module Control Program�Ή�
        # '=========================================================
        BMCP_PGM = Select_BMCP_PGM_.get(JCL_NAME_SV, JOB_SEQ_SV, STEP_SEQ_SV, data2["PGM_NAME"], PGM_SYSIN)
        
        if BMCP_PGM != "":
            ActSheet_x[13] = BMCP_PGM                        # '44��13
        else:
            pass
            #'ActSheet_x[13] = "����Ɏ��s"
            
        # 'End Add


        # '=========================================================
        # '20210607 Add Horiuchi
        # 'Batch Module Control Program�Ή�
        # '=========================================================
        if BMCP_PGM != "":
            parm = BMCP_PGM
        #'���o�͔���pPARM����
        elif PGM_SYSIN != "":
            parm = PGM_SYSIN
        elif data["PGM��"] != "":
            parm = data["PGM��"]
        elif PGM_PROC != "":
            parm = PGM_PROC
        else:
            parm = data["PROC��"]
        
#'20240219 ADD qian.e.wang
        if "ADABAS:" in data2["DSN"]:
            P_�f�[�^��� = "ADABAS"
        # DEBUG
        # print("���A �f�[�^��� :["+str(P_�f�[�^���)+"] ���o�͔���pPARM :["+str(parm)+"] DSN :["+str(data2["DSN"])+"]\r\n")
        if P_�f�[�^��� == "ADABAS":                
            # 'P_���o�͔���
            P_���o�͔��� = ���o�͔���_ADABAS_.get(P_�f�[�^���, parm, data2["DSN"].replace("ADABAS:", "").replace("(�ݒ薳)", "").replace("(" + parm + ")", ""))
            ActSheet_x[43] = "ADABAS�L������"  #'�R�����g��      '42��43
#'ADD END

        #'P_���o�͔��� = ���o�͔���(PARM, data2["DD_NAME, L_SYSIN, data["JCL_ID, data["STEP��, data["JOB_SEQ, data["STEP_SEQ, data2["DSN)
        if P_���o�͔��� == "":
            P_���o�͔��� = ���o�͔���_.get(parm, data2["DD_NAME"], L_SYSIN, JCL_NAME_SV, data["STEP��"], JOB_SEQ_SV, STEP_SEQ_SV, data2["DSN"],data["PGM��"])

        # DEBUG
        # print(parm, data2["DD_NAME"], L_SYSIN, JCL_NAME_SV, data["STEP��"], JOB_SEQ_SV, STEP_SEQ_SV, data2["DSN"],data["PGM��"],P_���o�͔���)

        # '�f�[�^��ʂɂ����o�͔���␳
        # 'if P_�f�[�^��� = "IMSDB" and P_���o�͔��� != "DELETE":     'DELETE����ꍇ������̂ł���͗�O�ɂ���
        if P_�f�[�^��� == "IMSDB" and P_���o�͔��� == "":
            # 'P_���o�͔��� = "I-O"
            P_���o�͔��� = ���o�͔���_IMSDB_.get(PGM_SYSIN, JCL_NAME_SV, JOB_SEQ_SV, STEP_SEQ_SV, data2["DSN"])
            ActSheet_x[43] = "SEGMENT�L������"  #'�R�����g��      '42��43
        elif P_�f�[�^��� == "IMSDB_INDEX" or P_�f�[�^��� == "IMSDB_�v�m�F":   #    'MHI�Č��݂̗̂\��
            P_���o�͔��� = "�Ή��s�v"                                            #                '���肵�Ȃ�
            
        ActSheet_x[21] = P_���o�͔���                  #         '20��21
        
        # 'MHI�b��Ή� �uEASYTREV�v�uEZTPA00�v�̏ꍇ��DISP�Ŕ��肷��
        # 'if P_���o�͔��� = "" and L_DISP != "" and (PGM_NAME = "EASYTREV" or PGM_NAME = "EZTPA00" or PGM_SYSIN = "EASYTREV" or PGM_SYSIN = "EZTPA00"):
        if P_���o�͔��� == "": # '�S�Ă̏����Ŗ�����̓��o�͔����DISP�Ŕ��肷��B�����ՂŎ��ʂł���悤��DISP������̔��茋�ʂ̂ݐݒ肷��
            # ' 20220227 wangqian DISP�S�p�^�[���Ή� START
            # 'if L_DISP = "S" or L_DISP = "O":
            # '   'P_���o�͔��� = "INPUT"
            # '   ActSheet_x[22] = "INPUT"                          '21��22
            # 'elif L_DISP = "S,D" or L_DISP = "O,D" or L_DISP = "M,D":
            # '   'P_���o�͔��� = "DELETE"
            # '   ActSheet_x[22] = "DELETE"                         '21��22
            # 'elif InStr(L_DISP, "M") > 0:
            # '   'P_���o�͔��� = "I-O"
            # '   ActSheet_x[22] = "I-O"                            '21��22
            # 'elif InStr(L_DISP, "N") > 0 or InStr(L_DISP, "C") > 0:
            # '   'P_���o�͔��� = "OUTPUT"
            # '   ActSheet_x[22] = "OUTPUT"                         '21��22
            # 'elif InStr(L_DISP, "O") > 0 or InStr(L_DISP, "S") > 0:
            # '   ActSheet_x[22] = "INPUT"                          '21��22
            # 'End if
            # ' *******************************************************************
            # ' DISP=(aaa,bbb,ccc)
            # ' aaa�c�f�[�^�Z�b�g�̑O����
            # '        NEW or SHR or OLD or MOD
            # '        �ȗ������߂�NEW�ł��
            # ' bbb�c�f�[�^�Z�b�g�̌㏈���i����I�����j
            # '        DELETE or KEEP or PASS or CATLG or UNCALTG
            # '        �ȗ������߂�aaa��NEW�̏ꍇDELETE�Aaaa��OLD/SHR/MOD�̏ꍇKEEP�ł��B
            # ' ccc�c�f�[�^�Z�b�g�̌㏈���i�ُ�I�����j
            # '        DELETE or KEEP or CALTG or UNCALTG
            # '        �ȗ������߂�aaa��NEW�̏ꍇDELETE�Aaaa��OLD/SHR/MOD�̏ꍇKEEP�ł��B
            # '
            # ' N�FNEW �@ �V�K
            # ' O�FOLD�@  �����Ɛ�ǎ�
            # ' S�FSHR�@  �������L�ǎ�
            # ' M�FMOD�@  �ǉ����[�h
            # ' K�FKEEP   �ۑ�
            # ' D�FDELETE �폜
            # ' C�FCATLG  �J�^���O
            # ' U�FUNCATLG�A���J�^���O�����Ή� �� �����_��END�ɕϊ�
            # ' P�FPASS�@ �㑱���p
            # ' ��JFE202112���SGr���Y�ɂēZ�߂��p�^�[����
            # ' INPUT   �� "S","O"
            # '            "O,END","O,K","O,P","S,K","S,P","END"
            # ' DELETE  �� "S,D","O,D",",D",",D,D",",K,D","M,D","N,D",",P,D"
            # ' I-O     �� "M","M,C","M,K","M,P"
            # ' OUTPUT  �� "N","N,C","N,K","N,P",",C",",C,D","O,C",",END",",K",",P",
            # '            "N,END"(//OUTDD    DD   DSN=ARCSBP&SL,UNIT=AFF=CMT,DISP=(NEW,&DSP)),
            # '            "END,END"(//KUTOUT   DD   DSN=_____,DISP=(___,____)),
            # '            "END,K"(//OLOG      DD   &OUT.UNIT=&U,VOL=SER=&V,DSN=&D,DISP=(&DP,KEEP))
            # ' *******************************************************************
            if L_DISP in  ("S", "O"):
                ActSheet_x[22] = "INPUT"
            elif L_DISP in ("S,D", "O,D", ",D", ",D,D", ",K,D", "M,D", "N,D", ",P,D","R,D"):
                ActSheet_x[22] = "DELETE"
            elif L_DISP in ("M", "M,C", "M,K", "M,P"):
                ActSheet_x[22] = "I-O"
            elif L_DISP in ("N", "N,C", "N,K", "N,P", "R", "R,C", "R,K", "R,P",",C", ",C,D", "O,C", ",END", ",K", ",P", "N,END", "END,END", "END,K","R,END"):
                ActSheet_x[22] = "OUTPUT"
            else:
                #' "O,END","O,K","O,P","S,K","S,P","END"
                ActSheet_x[22] = "INPUT"
            ##' 20220227 wangqian DISP�S�p�^�[���Ή� END
        
        
        if P_���o�͔��� != "":
            ActSheet_x[22] = ���o�͔���_DISP����(P_���o�͔���, L_DISP) #'21��22
        
        # '�f�[�^���2���� ���e�X�g�c�[���ŗ��p���邽�߂̑Ή�
        if P_�f�[�^��� == "DB2_TABLE":
            ActSheet_x[20] = "DB2_TABLE" #                        '19��20
        elif P_�f�[�^��� == "DUMMY":
            ActSheet_x[20] = ""           #                      '19��20
            ActSheet_x[22] = "����ΏۊO"  #                     '21��22
        elif P_�f�[�^��� == "ENTRY-DATA":
            ActSheet_x[20] = "SAM"        #                      '19��20
        elif P_�f�[�^��� == "IMSDB":
            ActSheet_x[20] = "IMSDB_TABLE"#                      '19��20
        elif P_�f�[�^��� == "IMSDB_INDEX":
            ActSheet_x[20] = ""            #                     '19��20�ȉ���
            ActSheet_x[22] = "����ΏۊO"   #                    '21��22�ȉ���
        elif P_�f�[�^��� == "IMSDB_���g�p":
            ActSheet_x[20] = ""
            ActSheet_x[22] = "����ΏۊO"
        elif P_�f�[�^��� == "IMSDB_SEGMENT":
            ActSheet_x[20] = "IMSDB_SEGMENT"
            # 'ActSheet_x[22] = "����ΏۊO"
        elif P_�f�[�^��� == "IMSDB_�v�m�F":
            ActSheet_x[20] = ""
        elif P_�f�[�^��� == "IMS�֘A":
            ActSheet_x[20] = ""
        # '    ActSheet_x[22] = "����ۗ�"
        elif P_�f�[�^��� == "NON-VSAM":
            ActSheet_x[20] = "SAM"
        elif P_�f�[�^��� == "NON-VSAM(���[�U�[�p)":
            ActSheet_x[20] = "SAM"
        elif P_�f�[�^��� == "PDS":
            ActSheet_x[20] = "PDS"
            ActSheet_x[22] = "����ΏۊO"
        elif P_�f�[�^��� == "PDS_�ϐ�":
            ActSheet_x[20] = "PDS"
            ActSheet_x[22] = "����ΏۊO"
        elif P_�f�[�^��� == "VSAM":
            ActSheet_x[20] = "VSAM"
        elif P_�f�[�^��� == "�_���v�t�@�C��":
            ActSheet_x[20] = "SAM"
        elif P_�f�[�^��� == "�t�@�C���`���p":
            ActSheet_x[20] = "SAM"
        elif P_�f�[�^��� == "�v�����g�f�[�^":
            ActSheet_x[20] = "SAM"
        elif P_�f�[�^��� == "���[�U�[�p":
            ActSheet_x[20] = "SAM"
        elif P_�f�[�^��� == "�ꎞDSN":
            ActSheet_x[20] = ""
        elif P_�f�[�^��� == "�ϐ��tDSN_�v����":
            ActSheet_x[20] = "�v����"
        elif P_�f�[�^��� == "����p�_�~�[":
            ActSheet_x[20] = "��t�@�C��"
            ActSheet_x[22] = "INPUT"
        else:
            ActSheet_x[20] = P_�f�[�^���
        
        if data2["DD_NAME"] == "STEPLIB":
            ActSheet_x[22] = "����ΏۊO"
        
#'20240209 DEL qian.e.wang
        # ' 20220302 wangqian DSN�ɂ��f�[�^���2����̒ǉ��@START
        if data2["DSN"] == "�ϐ��l�v�m�F":
            ActSheet_x[20] = "�Ǝ�DAM"
        elif len(data2["DSN"].replace("(�ݒ薳)", "")) == 4:
            ActSheet_x[20] = "�"
        # ' 20220302 wangqian DSN�ɂ��f�[�^���2����̒ǉ��@END
#' DEL END
    else:
        
        # 'PROC��PGM���␳�����@���@�������x���l������DSN��NULL�̂��̂͑Ή�����K�v�͖������o�͌��ʂɈ�a��������̂Ŏ��{����B�i�x����΃R�����g�A�E�g���Ă��悢�j
        if PGM_SYSIN == "" and data["PGM��"] == "":
            # 'PGM_PROC = GET_PROC_PGM(data["JCL_ID, data["JOB_SEQ, data["STEP_SEQ)
            PGM_PROC = GET_PROC_PGM_.get(JCL_NAME_SV, JOB_SEQ_SV, STEP_SEQ_SV)
            ActSheet_x[10] = PGM_PROC    # '���o�͗�̂��ς�����ꍇ�ɒ��ӂ��邱��    '��9��10�ɕύX�i�v�m�F�j
        else:
            ActSheet_x[10] = data["PGM��"]
    
    
    # '========================================================================
    # 'JFE�q�~�b��Ή�
    if "NDB:" in data2["DSN"]:   # '14��15,17��18,19��20
        ActSheet_x[15] = ActSheet_x[15].replace("NDB:", "").replace("(�ݒ薳)", "")
        ActSheet_x[18] = "�m�F��"
        ActSheet_x[20] = "NDB"
    elif "DAM:" in data2["DSN"]:
        ActSheet_x[15] = ActSheet_x[15].replace("DAM:", "").replace("(�ݒ薳)", "")
        ActSheet_x[18] = "�m�F��"
        ActSheet_x[20] = "DAM"
    elif "�:" in data2["DSN"]:
        ActSheet_x[15] = ActSheet_x[15].replace("�:", "").replace("(�ݒ薳)", "")
        ActSheet_x[18] = "�m�F��"
        ActSheet_x[20] = "�"
#'20240209 ADD qian.e.wang
    # '���YANPSS�b��Ή�
    if "ADABAS:" in data2["DSN"]:   # '14��15,17��18,19��20
        ActSheet_x[15] = ActSheet_x[15].replace("ADABAS:", "").replace("(�ݒ薳)", "")
        ActSheet_x[18] = "�m�F��"
        ActSheet_x[19] = "ADABAS"
        ActSheet_x[20] = "ADABAS"
#' ADD END
    # '========================================================================
    
    
    
    if data2["STEP_SEQ"] != "" and P_PARAM == "PROC":
        ActSheet_x[8] = data2["STEP_SEQ"]
        ActSheet_x[9] = data2["STEP_NAME"]#  '20161021 Takei
        ActSheet_x[11] = PROC_ID
        ActSheet_x[39] = "�@"           # '��38��39
    elif P_PARAM == "JCL" and STEP_SEQ_SV > 0:       #      '20161021 Takei
        # 'ActSheet_x[8] = data["STEP_SEQ2   '20161021 Takei�@20190914�ύX
        ActSheet_x[8] = 0  # '20161021 Takei�@20190914�ύX
        ActSheet_x[9] = data2["STEP_NAME"]#   '20161021 Takei
        ActSheet_x[11] = PROC_ID
        ActSheet_x[39] = "�A"       #     '��38��39
    else:
        ActSheet_x[8] = data["STEP_SEQ2"]
        ActSheet_x[9] = data["STEP_NAME"]#   '20161021 Takei
        # 'ActSheet_x[10] = ""
        ActSheet_x[39] = "�B"  #          '��38��39
    
    if data2["PGM_NAME"] == "UTACH" and data2["�����X�VFLG"] == "�����ݒ�iUTL��́j":
        ActSheet_x[8] = int(data2["�蓮�X�VFLG"])

#'20240219 ADD qian.e.wang
    if (data2["PGM_NAME"] == "ADM" or data2["PGM_NAME"] == "JYAADP") and (data2["�����X�VFLG"] == "�����ݒ�iUTL��́j" or data2["�����X�VFLG"] == "�蓮�⑫�iUTL��́j"):
        ActSheet_x[8] = int(data2["�蓮�X�VFLG"])
#'ADD END
    
    # 'ActSheet_x[8] = data["STEP_NAME     '20161021 Takei
    # 'ActSheet_x[9] = data["PGM_NAME  '��ŕ␳���Ă���̂ł����ł͍s��Ȃ�
    
    # 'if P_PARAM = "PROC":
    # '
    # 'else
    #     'ActSheet_x[10] = data["PROC_NAME
    #     'ActSheet_x[10] = PROC_ID
    #     ' PROC_ID
    # 'End if
    
    ActSheet.append(ActSheet_x)


def ��͏���(data):
    global ���p_�ڋq��_JCL_PGM_DSN_
    
    global JCL_NAME_WK,PGM_NAME,STEP_SEQ,JCL_NAME_SV,JOB_SEQ_SV,STEP_SEQ_SV,PROC_ID
    ActSheet_x = [""]*45
    
    ActSheet_x[1] = data["TEST_ID"]
    ActSheet_x[2] = data["JCL_SEQ"]
    ActSheet_x[3] = data["JCL_ID"]
    ActSheet_x[4] = data["LIBRARY"]
    ActSheet_x[5] = data["JOB_SEQ"]
    ActSheet_x[6] = data["JOB_ID"]
    ActSheet_x[7] = data["STEP_SEQ"]
    ActSheet_x[8] = data["STEP_SEQ2"]#  'MHI�Č��Œǉ�
    ActSheet_x[9] = data["STEP��"]
    ActSheet_x[10] = data["PGM��"]
    ActSheet_x[11] = data["PROC��"]
    #'ActSheet_x[12] = ""             'MHI�Č��Œǉ�

    #'MHI�p�b�� �J�n  JCL�̃����o�[���̂ݕK�v
    
    ���������� = data["JCL_ID"].split("%")
    
    # '20220311 ���o�͏��o�͂̃����o�[���擾������START
    if len(����������) > 2:
        ����������2 = ����������[2].split(".")
        if len(����������2) > 0:
            JCL_NAME_WK = ����������2[0]
        else:
            JCL_NAME_WK = ����������[2]
    # 'If len(����������) > 0:
    elif len(����������) > 1:
    # '20220311 ���o�͏��o�͂̃����o�[���擾������END
        ����������2 = ����������[1].split(".")
        if len(����������2) > 0:
            JCL_NAME_WK = ����������2[0]
        else:
            JCL_NAME_WK = ����������[1]
    else:
        JCL_NAME_WK = data["JCL_ID"]
    ActSheet_x[35] = JCL_NAME_WK       #'34��35
    #'MHI�p�b�� �I��
    
    
    
    PGM_NAME = data["PGM��"] # 'PGM���ޔ��@���̒l��PROC����PGM�𔽉f���Ă���

    #'ACOM�ŏ���
    #'STEP���̂ݑ��݂��Ȃ��ꍇ��z��i�����͑��s�j
    #    '���ۂɔ��������猟������

    
    STEP_SEQ = 0

    #'JCL_PGM_DSN�ďo���ʊ֐��ɃZ�b�g�@JCL����PROC�Ńp�����[�^�����ʉ�
    if data["STEP_SEQ2"] > 0:     #'PROC�ďo
        JCL_NAME_SV = data["PROC��"]      #        '�ďo����LIKE�w�肪�K�v
        JOB_SEQ_SV = 0
        STEP_SEQ_SV = data["STEP_SEQ2"]     #       '0�ȏ�̏ꍇ��PROC������ acom�ł��
    else:                        #'JCL�ďo
        JCL_NAME_SV = data["JCL_ID"]       #        '
        JOB_SEQ_SV = data["JOB_SEQ"]
        STEP_SEQ_SV = data["STEP_SEQ"]      #       '

    # 'if data["PROC��"] != "":
    if data["STEP_SEQ2"] > 0:
        PROC_ID = data["PROC��"]
        #'STEP_SEQ_SV = data["STEP_SEQ"]
    
    #'�@JCL��PROC�i����PROC�j
    #'�O��@����PROC�́uJCL_NAME�v���uJCL_ID%PROC���v�ƂȂ閽�����[����z��H

        myRS2 = ���p_�ڋq��_JCL_PGM_DSN_.get(data["JCL_ID"] + "%" + data["PROC��"],data["JOB_SEQ"])
        # DEBUG
        # print("���@JCL��PROC�i����PROC�j\r\n")
        if myRS2 == []:
            #'�A�O��PROC��z��
            # 'myRS2.Source = Cmd1 + data["PROC_NAME"] + Cmd2 + data["STEP_SEQ2"] + Cmd3 + 0 + Cmd4
            # 'myRS2.Source = Cmd1x + data["PROC��"] + Cmd4x
            # 'myRS2.Source = Cmd1x + data["PROC��"] + Cmd2 + data["STEP_SEQ2"] + Cmd4
            # 'myRS2.Source = Cmd1x + JCL_NAME_SV + Cmd2x + STEP_SEQ_SV + Cmd3 + JOB_SEQ_SV + Cmd4
            myRS2 = ���p_�ڋq��_JCL_PGM_DSN_.get(JCL_NAME_SV,JOB_SEQ_SV,STEP_SEQ_SV)
            # DEBUG
            # print("���A�O��PROC\r\n")

            # 'MsgBox (myRS2.Source)
            if myRS2 == []:
                DSN���Ȃ�������(ActSheet_x,data)
            else:
            # '�O��PROC���׏o��
                for data2 in myRS2:
                    DSN���L�莞����("PROC",data,data2)
        else:
            # '����PROC���׏o��
            for data2 in myRS2:
                DSN���L�莞����("PROC",data,data2)
    else:
    # '�BJCL��PGM
        PROC_ID = ""     #'�s��Ή� 2019/12/24
        # 'myRS2.Source = Cmd1 + data["JCL_ID"] + Cmd2 + data["STEP_SEQ"] + Cmd3 + data["JOB_SEQ"] + Cmd4
        
        # 'ActSheet_x, 35] = myRS2.Source   '������
        myRS2 = ���p_�ڋq��_JCL_PGM_DSN_.get(JCL_NAME_SV,JOB_SEQ_SV,STEP_SEQ_SV)
        # DEBUG
        # print("���BJCL��PGM\r\n")
        if myRS2 == []:
            DSN���Ȃ�������(ActSheet_x,data)
        else:

            for data2 in myRS2:
                # DEBUG
                # print("���BJCL_NAME_SV :["+str(JCL_NAME_SV)+"] JOB_SEQ_SV :["+str(JOB_SEQ_SV)+"] STEP_SEQ_SV :["+str(STEP_SEQ_SV)+"]\r\n")
                DSN���L�莞����("JCL",data,data2)



def analysis1(conn,cursor):
    global ���p_�ڋq��_JCL_PGM_DSN_,���o�͔���_IMSDB_,GET_PROC_PGM_,DATA_DSN�ʃf�[�^���ޏ��_,�ϐ��l�␳_,Select_BMCP_PGM_,���o�͔���_
#'20240214 ADD qian.e.wang
    global ���o�͔���_ADABAS_
#'ADD END
    
    sql =   """\
        
            SELECT * FROM TEST_JCL_PROC_PGM�֘A�ݒ�
            """
            
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)
    
    print(len(df),"���1")
    ���p_�ڋq��_JCL_PGM_DSN_ = ���p_�ڋq��_JCL_PGM_DSN(conn,cursor)
    ���o�͔���_IMSDB_ = ���o�͔���_IMSDB(conn,cursor)
#'20240214 ADD qian.e.wang
    ���o�͔���_ADABAS_ = ���o�͔���_ADABAS(conn,cursor)
#'ADD END
    GET_PROC_PGM_ = GET_PROC_PGM(conn,cursor)
    DATA_DSN�ʃf�[�^���ޏ��_ = DATA_DSN�ʃf�[�^���ޏ��(conn,cursor)
    �ϐ��l�␳_ = �ϐ��l�␳(conn,cursor)
    Select_BMCP_PGM_ = Select_BMCP_PGM(conn,cursor)
    ���o�͔���_ = ���o�͔���(conn,cursor)

    for i in range(len(df)):
        data = df.iloc[i]
        ��͏���(data)
    
    global ActSheet
    
    return ActSheet