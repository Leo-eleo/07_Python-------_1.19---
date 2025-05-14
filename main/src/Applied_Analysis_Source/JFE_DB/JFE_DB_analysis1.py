#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
# sys.path.append(os.path.dirname(__file__))
import pandas as pd
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


DB�����o�^��PARM = "�����ݒ�iJFE_DB����j" 
�֘A���Y = ""
JFE_�f�[�^���� = ""
JFE_���R�[�h�֘A�����ʒu = 0
JFE_CRUD���� = ""
JFE_IO���� = ""
���������� = []
JFE_DATA�֘APGM����_ = None

ActSheet = []
ActSheet_x = []

output_header = ["���YID","COBOL_ID","�����Ώ�PGM��","�����f�[�^����","�����Y�s���","PARM_ALL",\
                "�������R�[�h�@","�������R�[�h�A","�������R�[�h�B","�������R�[�h�C","�������R�[�h�D","�p�����[�^","CRUD����","IO����",\
                "�֘ADSN","�֘A���ݒ�","PGM-IO","JCL_PGM_DSN","�֘APGM�i�e�܂ށj","�⑫","JSI�pXDBREF"
]

class JFE_DATA�֘APGM����:
    
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�y�b��zJFE_DATA�֘APGM�ݒ�"
        # self.db_path = db_path

    def setup(self):
        
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        
        for module,data,record,crud,io in zip(df["�֘A���W���[��"],df["�f�[�^����"],df["���R�[�h�֘A�����ʒu"],df["CRUD����"],df["IO����"]):
            self.dic[module] = [data,record,crud,io]
            
        
    def get(self):
        global �֘A���Y
        global JFE_�f�[�^����,JFE_���R�[�h�֘A�����ʒu,JFE_CRUD����,JFE_IO����
        
        if self.dic == None:
            self.setup()
            
        �֘A���Y = �֘A���Y.replace("\"","")
        
        if �֘A���Y in self.dic:
            JFE_�f�[�^����,JFE_���R�[�h�֘A�����ʒu,JFE_CRUD����,JFE_IO���� = self.dic[�֘A���Y]
            return True
        
        else:
            return False
   
   
def reformat_record(record):
    
#'20240209 UPD qian.e.wang
    #record = str(record)
    record = str(record).replace("\"","")
#'UPD END
    
    if "-" not in record:
        return record
    
    split_record = record.split("-")
    m = max([len(rec) for rec in split_record])
    if m < 4:
        return record
    
    for rec in split_record:
        if len(rec) == m:
            return rec
        
   
def NDB����(P_PARM,ActSheet_x):     
    global ����������,JFE_���R�[�h�֘A�����ʒu
    if len(����������) > 7:
        ActSheet_x[7] = reformat_record(����������[JFE_���R�[�h�֘A�����ʒu])
    ActSheet_x[12] = P_PARM

    if "MODIFY" in P_PARM:
        ActSheet_x[13] = "U"
        ActSheet_x[14] = "I-O"
    elif "STORE" in P_PARM or "STR" in P_PARM:
        ActSheet_x[13] = "C"
        ActSheet_x[14] = "I-O"
    elif "ERASE" in P_PARM or "ERS" in P_PARM:
        ActSheet_x[13] = "D"
        ActSheet_x[14] = "I-O"
    elif "GET" in P_PARM or "FIND" in P_PARM:
        ActSheet_x[13] = "R"
        ActSheet_x[14] = "INPUT"
    elif "CON" in P_PARM or "DCN" in P_PARM or "TEST" in P_PARM:
        ActSheet_x[13] = "NA"
        ActSheet_x[14] = "NA"
    return ActSheet_x
    
def ACSAPI����(P_PARM, ActSheet_x):
    global ����������

    if len(����������) > 3:
        ActSheet_x[12] = ����������[3]

    if  " DSREAD " in P_PARM:
        ActSheet_x[13] = "R"
        ActSheet_x[14] = "INPUT"
    elif  " DSWRITE " in P_PARM:
        ActSheet_x[13] = "C"
        ActSheet_x[14] = "I-O"
    elif  " DSFREE " in P_PARM:
        ActSheet_x[13] = "NA"
        ActSheet_x[14] = "NA"
        
    return ActSheet_x    


### VBA�ł͍s�ԍ��𑝂₵�Ă������A�����nActSheet_x �ɍs�ԍ��𑝂₵����̏�����͂��� ActSheet_x �͑S�̂ɒǉ����āAnActSheet_x��V���� ActSheet_x�Ƃ���
### ActSheet.Cells(x, �� nActSheet_x
### ActSheet.Cells(x - 1, ��ActSheet_x �̂悤�Ȋ֌W
def XDBREF����(ActSheet_x):
    global ActSheet,����������
    
    if len(����������) > 6:
       if ����������[6] != ".":
            ActSheet_x[7] = reformat_record(����������[6])
            ActSheet_x[13] = "R"
            ActSheet_x[14] = "INPUT"
            ActSheet_x[21] = ����������[5]
    
    
    if len(����������) > 7:
       if ����������[7] != ".":
            nActSheet_x = [""]*22
            for i in range(1,7):
                nActSheet_x[i] = ActSheet_x[i]
            
            nActSheet_x[7] = reformat_record(����������[7])
            nActSheet_x[13] = "R"
            nActSheet_x[14] = "INPUT"
            ActSheet.append(ActSheet_x)
            ActSheet_x = nActSheet_x
    
    if len(����������) > 8:
       if ����������[8] != ".":            
            nActSheet_x = [""]*22
            for i in range(1,7):
                nActSheet_x[i] = ActSheet_x[i]
            
            nActSheet_x[7] = reformat_record(����������[8])
            nActSheet_x[13] = "R"
            nActSheet_x[14] = "INPUT"
            ActSheet.append(ActSheet_x)
            ActSheet_x = nActSheet_x

    if len(����������) > 9:
       if ����������[9] != ".":
            nActSheet_x = [""]*22
            for i in range(1,7):
                nActSheet_x[i] = ActSheet_x[i]
            
            nActSheet_x[7] = reformat_record(����������[9])
            nActSheet_x[13] = "R"
            nActSheet_x[14] = "INPUT"
            ActSheet.append(ActSheet_x)
            ActSheet_x = nActSheet_x

    if len(����������) > 10:
       if ����������[10] != ".":
            nActSheet_x = [""]*22
            for i in range(1,7):
                nActSheet_x[i] = ActSheet_x[i]
            
            nActSheet_x[7] = reformat_record(����������[10])
            nActSheet_x[13] = "R"
            nActSheet_x[14] = "INPUT"
            ActSheet.append(ActSheet_x)
            ActSheet_x = nActSheet_x
    
    return ActSheet_x    
    
    
    
def COBOL_CALL���߉��(data):
    
    global JFE_DATA�֘APGM����_
    global �֘A���Y,JFE_�f�[�^����,JFE_���R�[�h�֘A�����ʒu,JFE_CRUD����,JFE_IO����
    global ���YID,COBOL_ID,�����Y�s���,PARM_CMD
    global ����������
    global ActSheet_x
    
    ActSheet_x = [""]*22
    ���YID = data["���YID"]
    COBOL_ID = data["COBOL_ID"]
    �����Y�s��� = data["�����Y�s���"]
    PARM_CMD = data["PARM"]
    
    ���������� = ArrayEmptyDelete(PARM_CMD.split(" "))     ###�኱�ł��邪��؂蕶�����X�y�[�X1�łȂ��ꍇ������

    ActSheet_x[1] = ���YID
    ActSheet_x[2] = COBOL_ID
    ActSheet_x[5] = �����Y�s���
    ActSheet_x[6] = PARM_CMD
    
    if len(����������) > 1: ###��͌��ʂ��u.�v�݂̂̏ꍇ������̂őΏۊO�Ƃ���
        �֘A���Y = ����������[1]
        if  "\"" not in �֘A���Y:
            ActSheet_x[3] = "�ΏۊO(�ϐ�)"
        elif JFE_DATA�֘APGM����_.get() == False:
            ActSheet_x[3] = "�ΏۊO"
        else:
            ActSheet_x[3] = �֘A���Y
            ActSheet_x[4] = JFE_�f�[�^����
    
            ###DAMIR���
            if JFE_�f�[�^���� == "DAM" and �֘A���Y == "XXDAMDL":
    
                if len(����������) > 6:
                    if ����������[6] != ".":
                        ActSheet_x[7] = reformat_record(����������[6])
                    else:
                        ActSheet_x[7] = "�v�Ē���"
                else:
                    ActSheet_x[7] = "�v�Ē���"
                    
                ActSheet_x[13] = JFE_CRUD����
                ActSheet_x[14] = JFE_IO����

    
            ###DAMIR�g���b�L���O
            elif JFE_�f�[�^���� == "DAM" and �֘A���Y in ("XXTFRD","XXTFDL","XXTFAD","XXTFMDF","XXTFMV"):
        
                if len(����������) > 7:
                    ActSheet_x[7] = reformat_record(����������[6])
                    if ����������[7] != ".":
                        ActSheet_x[8] = reformat_record(����������[7])
                elif len(����������) > 6:
                    if ����������[6] != ".":
                        ActSheet_x[7] = reformat_record(����������[6])
                    else:
                        ActSheet_x[7] = "�v�Ē���"
                else:
                    ActSheet_x[7] = "�v�Ē���"
                ActSheet_x[13] = JFE_CRUD����
                ActSheet_x[14] = JFE_IO����

    
            elif JFE_�f�[�^���� == "NDB" and �֘A���Y == "XDBMCR":
                if len(����������) > 5:
                    JFE_NDB_PARM = ����������[5]
                    ActSheet_x = NDB����(JFE_NDB_PARM,ActSheet_x)
                
            elif JFE_�f�[�^���� == "NDB" and �֘A���Y == "XDBREF":
            
                ActSheet_x = XDBREF����(ActSheet_x)
                
                ###�s�J�E���g�A�b�v�͍s��Ȃ��uXDBREF����v���Ŏ��{
        
            elif JFE_�f�[�^���� == "�Ǝ�DAM" and �֘A���Y == "ACSAPI":
        
                JFE_ACSAPI_PARM = PARM_CMD
                ActSheet_x = ACSAPI����(JFE_ACSAPI_PARM,ActSheet_x)
        
            ####�f�ތn���� �Ǝ�DAM
            elif JFE_�f�[�^���� == "�Ǝ�DAM" and �֘A���Y in ("SXDAMRD","SXDAMWT","SXDAMAD","SXDAMDL","SXDAMKSR","SXDAMCAD","SXDAMCDL","SXDAMACT"):
        
                if len(����������) > 5:
                    ActSheet_x[7] = reformat_record(����������[3])
                    ActSheet_x[8] = reformat_record(����������[5])
                ActSheet_x[13] = JFE_CRUD����
                ActSheet_x[14] = JFE_IO����

    
    
            elif JFE_�f�[�^���� == "�Ǝ�DAM" and �֘A���Y in ("XEDAERD","XEDAEWT","XEDARLX","XEDAOPN","XEDACLS","XEDCB","XODAOPN","XODACLS"):
                        
                ActSheet_x[7] = "�����ۗ�"   ###�����\�������_�ł͕s��
                ActSheet_x[13] = JFE_CRUD����
                ActSheet_x[14] = JFE_IO����
    
            
            elif JFE_�f�[�^���� == "�Ǝ�DAM" and �֘A���Y in ("XPDARED","XPDAWRT","XPDAOPN","XPDACLS","XPDAFRE"):
                        
                ActSheet_x[7] = "�����ۗ�"   ###�����\�������_�ł͕s��
                ActSheet_x[13] = JFE_CRUD����
                ActSheet_x[14] = JFE_IO����
                        

            
            ###�_���n���� �Ǝ�DAM
            elif JFE_�f�[�^���� == "�Ǝ�DAM" and �֘A���Y == "RXDAMDL":
                        
                if len(����������) > 6:
                    if ����������[6] != ".":
                        ActSheet_x[7] = reformat_record(����������[6])
                    else:
                        ActSheet_x[7] = "�v�Ē���"
                else:
                    ActSheet_x[7] = "�v�Ē���"
                ActSheet_x[13] = JFE_CRUD����
                ActSheet_x[14] = JFE_IO����

                        
            ###�_���n���� �Ǝ�DAM
            elif JFE_�f�[�^���� == "�Ǝ�DAM" and �֘A���Y in ("RXTFRD","RXTFAD","RXTFDL","RXTFMDF","RXTFMV"):
        
                if len(����������) > 7:
                    ActSheet_x[7] = reformat_record(����������[6])
                    if ����������[7] != ".":
                        ActSheet_x[8] = reformat_record(����������[7])
                elif len(����������) > 6:
                    
                    if ����������[6] != ".":
                        ActSheet_x[7] = reformat_record(����������[6])
                    else:
                        ActSheet_x[7] = "�v�Ē���"
                else:
                    ActSheet_x[7] = "�v�Ē���"
                ActSheet_x[13] = JFE_CRUD����
                ActSheet_x[14] = JFE_IO����

                                                    
            else:
            
                if len(����������) > JFE_���R�[�h�֘A�����ʒu:
                    JFE_�������R�[�h = ����������[JFE_���R�[�h�֘A�����ʒu]
                    ActSheet_x[7] = reformat_record(JFE_�������R�[�h)
                    ActSheet_x[13] = JFE_CRUD����
                    ActSheet_x[14] = JFE_IO����
                 
            
            if ActSheet_x[7] == "":
                ActSheet_x[7] = "�v�Ē���"
                
    return ActSheet_x

#'20240214 ADD qian.e.wang
def COBOL_EXEC���߉��(data):
    
    global JFE_DATA�֘APGM����_
    global �֘A���Y,JFE_�f�[�^����,JFE_���R�[�h�֘A�����ʒu,JFE_CRUD����,JFE_IO����
    global ���YID,COBOL_ID,�����Y�s���,PARM_CMD
    global ActSheet_x
    
    ActSheet_x = [""]*22
    ���YID = data["���YID"]
    if data["PGM_NAME"] == "UTACH" or data["PGM_NAME"] == "ADM" or data["PGM_NAME"] == "JYAADP":
        COBOL_ID = data["SYSIN_PGM"]
    else:
        COBOL_ID = data["PGM_NAME"]
    �����Y�s��� = data["�����Y�s���"]
    PARM_CMD = data["PARM"]
    
    ActSheet_x[1] = ���YID
    ActSheet_x[2] = COBOL_ID
    ActSheet_x[5] = �����Y�s���
    ActSheet_x[6] = PARM_CMD
    
    �֘A���Y = COBOL_ID
    if JFE_DATA�֘APGM����_.get() == False:
        ActSheet_x[3] = "�ΏۊO"
    else:
        # DEBUG
        # print("�֘A���Y�@ :["+str(�֘A���Y)+"] JFE_�f�[�^���އ@ :["+str(JFE_�f�[�^����)+"]\r\n")
        ###���YANPSS��� ADABAS
        if JFE_�f�[�^���� == "ADABAS":
            ActSheet_x[3] = �֘A���Y
            ActSheet_x[4] = JFE_�f�[�^����
            
            JFE_�������R�[�h = �֘A���Y
            ActSheet_x[7] = reformat_record(JFE_�������R�[�h)
            ActSheet_x[13] = JFE_CRUD����
            ActSheet_x[14] = JFE_IO����
            
            
    if ActSheet_x[7] == "":
        ActSheet_x[7] = "�v�Ē���"
    
    return ActSheet_x
#'ADD END
    
def analysis1(db_path,title):
    global JFE_DATA�֘APGM����_
    global ActSheet, ActSheet_x,DB�����o�^��PARM
    start = time.time()

    if os.path.isdir(title) == False:
        os.makedirs(title)
        
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
    
    
    # sql,values = make_delete_sql("�ڋq��_JCL_PGM_DSN",["",DB�����o�^��PARM],["�蓮�X�VFLG","�����X�VFLG"])
    # cursor.execute(sql,values)
    # sql,values = make_delete_sql("�ڋq��_���Y�֘A�����",[DB�����o�^��PARM],["�o�^����"])
    # cursor.execute(sql,values)
    # sql,values = make_delete_sql("�ڋq��_PGM_IO���",["COBOL_����"],["���Y����"])
    # cursor.execute(sql,values)
    
    conn.commit()
    print("DB�폜����", time.time()-start)
    
#'20240214 ADD qian.e.wang
    JFE_DATA�֘APGM����_ = JFE_DATA�֘APGM����(conn,cursor)
    ActSheet = []
    
    
    ###���YANPSS ADABAS����
    sql =   """\
            SELECT tbl1.*, tbl2.SYSIN_PGM FROM �ڋq��_JCL_CMD��� tbl1 
            INNER JOIN (SELECT DISTINCT JCL_NAME, STEP_SEQ, PGM_NAME, SYSIN_PGM FROM �ڋq��_JCL_PGM_DSN) AS tbl2 
            ON tbl1.���YID = tbl2.JCL_NAME AND tbl1.STEP_SEQ = tbl2.STEP_SEQ AND tbl1.PGM_NAME = tbl2.PGM_NAME
            WHERE tbl1.PGM_NAME <> '' AND tbl1.CMD���� = 'EXEC'
            """
            
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)
    df.sort_values(["���YID","CMD_SEQ","�����Y�s���"],inplace=True)
    
    for i in range(len(df)):
        data = df.iloc[i]
        ActSheet_x = COBOL_EXEC���߉��(data)
        ActSheet.append(ActSheet_x)
#'ADD END
    
    
    sql =   """\
            SELECT * FROM �ڋq��_COBOL_CMD���
            """
            
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)
    df.sort_values(["���YID","CMD_SEQ","�����Y�s���"],inplace=True)
    
#'20240214 DEL qian.e.wang
    #JFE_DATA�֘APGM����_ = JFE_DATA�֘APGM����(conn,cursor)
    #ActSheet = []
#'DEL END
    
    for i in range(len(df)):
        data = df.iloc[i]
        ActSheet_x = COBOL_CALL���߉��(data)
        ActSheet.append(ActSheet_x)
    ActSheet_all = [actSheet[1:] for actSheet in ActSheet]
    write_excel_multi_sheet("JFE-DB���p�ӏ�����1.xlsx",ActSheet_all,"JFE_DB���p������",title,output_header)
    
    conn.close()


# analysis1(sys.argv[1],sys.argv[2])