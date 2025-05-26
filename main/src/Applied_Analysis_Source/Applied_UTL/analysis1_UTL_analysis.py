#!/usr/bin/env python
# -*- coding: cp932 -*-
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


conn = None
cursor = None

���������� = []
����������2 = []
vbCrLf = "\n"
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
�ďo���@ = ""
����PGM = ""
DB�����o�^��PARM = "�����ݒ�iUTL��́j"
PGM�\�� = ""
����MODE = ""

JCL_NAME_SV = ""
JOB_SEQ_SV = 0
STEP_SEQ_SV = 0
DELETE�p�� = False
DUMP�p�� = False
RESTORE�p�� = False
FTP�p�� = False
DEFCL�p�� = False
### 20210312 Add Horiuchi
DEFPATH�p�� = False
DEFAIX�p�� = False
DEFNVSAM�p�� = False
DEFUCAT�p�� = False
COPY�p�� = False
LOAD�p�� = False
UNLOAD�p�� = False
UTACH�p�� = False
#'20240215 ADD qian.e.wang
ADARUN3V�p�� = False
JYAADP�p�� = False
ADM�p�� = False
#'ADD END
����DD = ""
�ǉ�DSN = ""
IO���� = ""
RESTORE���[�h = ""
�u��DSN = ""
����DD_OUT_SV = ""
���I�v�f = []
REPRO_OUTDATASET_���pDD�擾_ = None
���p_�ڋq��_JCL_STEP_SYSIN_ = None
#���p_�ڋq��_���Y�֘A�����_ = None
���p_�ڋq��_JCL_PGM_DSN_ = None
���p_UTL_STEP��_IO���_ = None
ActSheet = []
�]���p�� = ""


class REPRO_OUTDATASET_���pDD�擾:
    
    def __init__(self,db_path):
        self.dic = None
        # self.conn = None
        # self.cursor = None
        self.dbname = "�ڋq��_JCL_PGM_DSN"
        self.db_path = db_path
        

    def setup(self):
        self.dic = {}
        global conn,cursor
        # self.conn = connect_accdb(self.db_path)
        # self.cursor = self.conn.cursor()
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,conn)
        df.fillna("",inplace=True)
        
        for jcl,job,step,dsn,dd in zip(df["JCL_NAME"],df["JOB_SEQ"],df["STEP_SEQ"],df["DSN"],df["DD_NAME"]):
            self.dic[(jcl,job,step,dsn)] = str(dd)
            
        
    def get(self):
        global JCL_NAME,JOB_SEQ,STEP_SEQ,�ǉ�DSN
           
        if self.dic == None:
            self.setup()
            
        if (JCL_NAME,JOB_SEQ,STEP_SEQ,�ǉ�DSN) in self.dic:
            return self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ,�ǉ�DSN)]
        
        else:
            return ""
        
class ���p_�ڋq��_JCL_STEP_SYSIN:
    
    def __init__(self,db_path):
        self.dic = None
        # self.conn = None
        # self.cursor = None
        self.all_list = None
        self.update_info_dic = {}
        self.db_key_list = None
        self.key_to_index = {}
        self.dbname = "�ڋq��_JCL_STEP_SYSIN"
        self.db_path = db_path
        
        self.step_sysin_update_dic = {}
        
    def setup(self):
        self.dic = {}
        global conn,cursor
        # self.conn = connect_accdb(self.db_path)
        # self.cursor = self.conn.cursor()
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,conn)
        df.fillna("",inplace=True)
        self.all_list = df.values.tolist()
        self.db_key_list = df.columns.tolist()
        self.key_to_index = {key:i for i,key in enumerate(self.db_key_list)}
        
        for i,data in enumerate(self.all_list):
            jcl,job,step = data[self.key_to_index["JCL_NAME"]],data[self.key_to_index["JOB_SEQ"]],data[self.key_to_index["STEP_SEQ"]]
            if (jcl,job,step) not in self.dic:
                self.dic[(jcl,job,step)] = []
            self.dic[(jcl,job,step)].append(i)
            
            if (jcl,job,step) not in self.update_info_dic:
                self.update_info_dic[(jcl,job,step)] = []
            self.update_info_dic[(jcl,job,step)].append(i)
    
        
    def update(self):
        if self.dic == None:
            self.setup()
            
        global JCL_NAME,JOB_SEQ,STEP_SEQ,����PGM,DB�����o�^��PARM
        
        if (JCL_NAME,JOB_SEQ,STEP_SEQ) not in self.dic:
            return False

        for index in self.update_info_dic[(JCL_NAME,JOB_SEQ,STEP_SEQ)]:
            self.all_list[index][self.key_to_index["SYSIN_PGM"]] = ����PGM
            self.all_list[index][self.key_to_index["�����X�VFLG"]] = DB�����o�^��PARM  
        
        self.step_sysin_update_dic[(JCL_NAME,JOB_SEQ,STEP_SEQ)] = ����PGM # VBA�̏ꍇ��DB��UPDATE����� myRS�̓��e���X�V����邪�Apython�ł͈قȂ�̂ōX�V���ꂽ���e�������Ă���
                
        return True
    
    def _close_conn(self):
        global conn
        
        if conn != None:
            conn.close()
            
        # if self.conn != None:
        #     self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
        
        
    def _delete_all(self):
        sql,values = make_delete_sql(self.dbname,[],[])
        global conn,cursor
        cursor.execute(sql,values)
        conn.commit()
        
        
    def update_all(self):
        global conn,cursor
        # self.conn = connect_accdb(self.db_path)
        # self.cursor = self.conn.cursor()
        
        self._delete_all()
        self._close_conn()
        compact_accdb(self.db_path)
        
        conn = connect_accdb(self.db_path)
        cursor = conn.cursor()
        # self.conn = connect_accdb(self.db_path)
        # self.cursor = self.conn.cursor()

        if self.all_list != None:
            for data in self.all_list:

                sql,value = make_insert_sql(self.dbname,data,self.db_key_list)
                cursor.execute(sql,value)
                # self.cursor.execute(sql,value)
                # self.conn.commit()
        conn.commit()
        # self._close_conn()
            
    
#class ���p_�ڋq��_���Y�֘A�����:
#    
#    def __init__(self,db_path):
#        self.dic = None
#        self.conn = None
#        self.cursor = None
#        self.dbname = "�ڋq��_���Y�֘A�����"
#        self.db_path = db_path
#
#    def setup(self):
#        self.dic = {}
#        self.conn = connect_accdb(self.db_path)
#        self.cursor = self.conn.cursor()
#        sql = "SELECT * FROM "+self.dbname
#        
#        df = pd.read_sql(sql,self.conn)
#        df.fillna("",inplace=True)
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
#        self.conn.commit()
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
    
class ���p_�ڋq��_JCL_PGM_DSN:
    def __init__(self,db_path):
        self.dic = None
        # self.conn = None
        # self.cursor = None
        self.all_list = None
        self.update_info_dic = {}
        self.db_key_list = None
        self.key_to_index = {}
        self.dbname = "�ڋq��_JCL_PGM_DSN"
        self.db_path = db_path

    def setup(self):
        self.dic = {}
        global conn,cursor
        # self.conn = connect_accdb(self.db_path)
        # self.cursor = self.conn.cursor()
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,conn)
        df.fillna("",inplace=True)
        self.all_list = df.values.tolist()
        self.db_key_list = df.columns.tolist()
        self.key_to_index = {key:i for i,key in enumerate(self.db_key_list)}
        
        for i,data in enumerate(self.all_list):
            jcl,job,step,dd,dsn = data[self.key_to_index["JCL_NAME"]],data[self.key_to_index["JOB_SEQ"]],data[self.key_to_index["STEP_SEQ"]],data[self.key_to_index["DD_NAME"]],data[self.key_to_index["DSN"]]
                        
            self.dic[(jcl,job,step,dd,dsn)] = 1
            if (jcl,job,step) not in self.dic:
                self.dic[(jcl,job,step)] = []
            self.dic[(jcl,job,step)].append([dd,dsn])


            if (jcl,job,step) not in self.update_info_dic:
                self.update_info_dic[(jcl,job,step)] = []
            self.update_info_dic[(jcl,job,step)].append(i)
        
    def insert(self):
        if self.dic == None:
            self.setup()
        
        global LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME,PROC_NAME
        
        global ����PGM,DB�����o�^��PARM,����DD,�ǉ�DSN

        if (JCL_NAME,JOB_SEQ,STEP_SEQ,����DD,�ǉ�DSN) in self.dic and self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ,����DD,�ǉ�DSN)] == 1:
            return False
        
        insert_list = [""]*len(self.db_key_list)
        
        key_list = ["LIBRARY_ID","JCL_NAME","JOB_SEQ","JOB_ID","STEP_SEQ","STEP_NAME","PGM_NAME","PROC_NAME","SYSIN_PGM","DD_NAME","DSN","�蓮�X�VFLG","�����X�VFLG"]
        value_list = [LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME,PROC_NAME,����PGM,����DD,�ǉ�DSN.replace("\"",""),"",DB�����o�^��PARM]

        for key,value in zip(key_list,value_list):
            insert_list[self.key_to_index[key]] = value
        
        if (JCL_NAME,JOB_SEQ,STEP_SEQ) not in self.update_info_dic:
            self.update_info_dic[(JCL_NAME,JOB_SEQ,STEP_SEQ)] = []
        
        self.update_info_dic[(JCL_NAME,JOB_SEQ,STEP_SEQ)].append(len(self.all_list))
        self.all_list.append(insert_list)

        self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ,����DD,�ǉ�DSN)] = 1
        self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ)] = 1
        
        return True

    def update(self):
        if self.dic == None:
            self.setup()
        
        global JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID
        
        global ����PGM,DB�����o�^��PARM,����DD,�ǉ�DSN

        if (JCL_NAME,JOB_SEQ,STEP_SEQ) not in self.dic:
            return False
        
        for index in self.update_info_dic[(JCL_NAME,JOB_SEQ,STEP_SEQ)]:
            self.all_list[index][self.key_to_index["SYSIN_PGM"]] = ����PGM
            self.all_list[index][self.key_to_index["�����X�VFLG"]] = DB�����o�^��PARM  
            
        for i,v in enumerate(str(self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ)])):
            #pgm,dd = v
            #self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ)][i][0] = ����PGM
            #self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ,pgm,dd)] = 0
            #self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ,����PGM,dd)] = 1
            if len(v) == 2:
                pgm,dd = v
                self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ)][i][0] = ����PGM
                self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ,pgm,dd)] = 0
                self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ,����PGM,dd)] = 1
        
        return True
    
    def _close_conn(self):
        global conn
        
        if conn != None:
            conn.close()
            
        # if self.conn != None:
        #     self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
        
        
    def _delete_all(self):
        sql,values = make_delete_sql(self.dbname,[],[])
        global conn,cursor
        cursor.execute(sql,values)
        conn.commit()
        
        
    def update_all(self):
        global conn,cursor
        # self.conn = connect_accdb(self.db_path)
        # self.cursor = self.conn.cursor()
        
        self._delete_all()
        self._close_conn()
        compact_accdb(self.db_path)
        
        conn = connect_accdb(self.db_path)
        cursor = conn.cursor()
        # self.conn = connect_accdb(self.db_path)
        # self.cursor = self.conn.cursor()

        if self.all_list != None:
            for data in self.all_list:

                sql,value = make_insert_sql(self.dbname,data,self.db_key_list)
                cursor.execute(sql,value)
                # self.cursor.execute(sql,value)
                # self.conn.commit()
        conn.commit()
        # self._close_conn()
    
        

class ���p_UTL_STEP��_IO���:
    def __init__(self,db_path):
        self.dic = None
        # self.conn = None
        # self.cursor = None
        self.all_list = None
        self.update_info_dic = {}
        self.db_key_list = None
        self.key_to_index = {}
        
        self.dbname = "UTL_STEP��_IO���"
        self.db_path= db_path

    def setup(self):
        self.dic = {}
        global conn,cursor
        # self.conn = connect_accdb(self.db_path)
        # self.cursor = self.conn.cursor()
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,conn)
        df.fillna("",inplace=True)
        
        self.all_list = df.values.tolist()
        self.db_key_list = df.columns.tolist()
        self.key_to_index = {key:i for i,key in enumerate(self.db_key_list)}
        
        for i,data in enumerate(self.all_list):
            jcl,job,step,dd,io = data[self.key_to_index["JCL_NAME"]],data[self.key_to_index["JOB_SEQ"]],data[self.key_to_index["STEP_SEQ"]],data[self.key_to_index["DD��"]],data[self.key_to_index["IO"]]
                        
            if io == "DELETE":
                self.dic[(jcl,job,step,dd)] = 1
            else:
                self.dic[(jcl,job,step,dd)] = 0
                
            if (jcl,job,step,dd) not in self.update_info_dic:
                self.update_info_dic[(jcl,job,step,dd)] = []
            self.update_info_dic[(jcl,job,step,dd)].append(i)
    
        
    def update(self):
        if self.dic == None:
            self.setup()
        
        global JCL_NAME,JOB_SEQ,STEP_SEQ
        
        global DB�����o�^��PARM,����DD,IO����

        if (JCL_NAME,JOB_SEQ,STEP_SEQ,����DD) not in self.dic or self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ,����DD)] == 0:
            return False

        for index in self.update_info_dic[(JCL_NAME,JOB_SEQ,STEP_SEQ,����DD)]:
            self.all_list[index][self.key_to_index["IO"]] = IO����
            self.all_list[index][self.key_to_index["�⑫"]] = DB�����o�^��PARM 
        
        if IO���� != "DELETE":
            self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ,����DD)] = 0
            
        
        return True
    
    def insert(self):
        if self.dic == None:
            self.setup()
        
        global JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME
        
        global DB�����o�^��PARM,����DD,IO����

        if (JCL_NAME,JOB_SEQ,STEP_SEQ,����DD) in self.dic:
            return False
        
        insert_list = [""]*len(self.db_key_list)
        
        key_list = ["JCL_NAME","JOB_SEQ","JOB_ID","STEP_SEQ","STEP��","DD��","IO","Utility_ID","�⑫"]
        value_list = [JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,����DD,IO����,PGM_NAME,DB�����o�^��PARM]
        for key,value in zip(key_list,value_list):
            insert_list[self.key_to_index[key]] = value
        
        self.update_info_dic[(JCL_NAME,JOB_SEQ,STEP_SEQ,����DD)] = [len(self.all_list)]
        self.all_list.append(insert_list)
        
        if IO���� == "DELETE":
            self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ,����DD)] = 1
        else:
            self.dic[(JCL_NAME,JOB_SEQ,STEP_SEQ,����DD)] = 0
        
        return True
    
    def _close_conn(self):
        global conn
        
        if conn != None:
            conn.close()
            
        # if self.conn != None:
        #     self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
        
        
    def _delete_all(self):
        sql,values = make_delete_sql(self.dbname,[],[])
        global conn,cursor
        #cursor.execute(sql,values)
        #conn.commit()
        
        
    def update_all(self):
        global conn,cursor
        # self.conn = connect_accdb(self.db_path)
        # self.cursor = self.conn.cursor()
        
        self._delete_all()
        self._close_conn()
        compact_accdb(self.db_path)
        
        conn = connect_accdb(self.db_path)
        cursor = conn.cursor()
        # self.conn = connect_accdb(self.db_path)
        # self.cursor = self.conn.cursor()

        if self.all_list != None:
            for data in self.all_list:

                sql,value = make_insert_sql(self.dbname,data,self.db_key_list)
                cursor.execute(sql,value)
                # self.cursor.execute(sql,value)
                # self.conn.commit()
        conn.commit()
        # self._close_conn()
        
    

def JCL_STEP_SYSIN���_���ʏo��(data):
    
	global ���p_�ڋq��_JCL_STEP_SYSIN_
	global LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME,PROC_NAME,SYSIN_PGM,SYSIN_SEQ,PARM_EXEC,PARM_PROC,SYSIN
	global ����������,����������2,���Y�֘A��_�ǉ�_CNT,JCL_PGM_DSN_�ǉ�_CNT,JCL_PGM_DSN_�X�V_CNT,UTL_STEP��_IO���_�ǉ�_CNT

	ActSheet_x = [""]*20

	ActSheet_x[1]= data["LIBRARY_ID"]
	ActSheet_x[2]= data["JCL_NAME"]
	ActSheet_x[3]= data["JOB_SEQ"]
	ActSheet_x[4]= data["JOB_ID"]
	ActSheet_x[5]= data["STEP_SEQ"]
	ActSheet_x[6]= data["STEP_ID"]
	ActSheet_x[7]= data["PGM_NAME"]
	ActSheet_x[8]= data["PROC_NAME"]
	ActSheet_x[9]= data["SYSIN_PGM"]
	ActSheet_x[10]= data["SYSIN_SEQ"]
	ActSheet_x[11]= data["SYSIN"]
	# ActSheet_x[14]= 0
	LIBRARY_ID = data["LIBRARY_ID"]
	JCL_NAME = data["JCL_NAME"]
	JOB_SEQ = data["JOB_SEQ"]
	JOB_ID = data["JOB_ID"]
	STEP_SEQ = data["STEP_SEQ"]
	STEP_ID = data["STEP_ID"]
	PGM_NAME = data["PGM_NAME"]
	PROC_NAME = data["PROC_NAME"]
	SYSIN_PGM = data["SYSIN_PGM"]
	SYSIN_SEQ = data["SYSIN_SEQ"]
	SYSIN = data["SYSIN"]

	if (JCL_NAME,JOB_SEQ,STEP_SEQ) in ���p_�ڋq��_JCL_STEP_SYSIN_.step_sysin_update_dic:
		SYSIN_PGM =  ���p_�ڋq��_JCL_STEP_SYSIN_.step_sysin_update_dic[(JCL_NAME,JOB_SEQ,STEP_SEQ)]
		ActSheet_x[9] = SYSIN_PGM

#'20240215 UPD qian.e.wang
#	���������� = SYSIN.split(" ")
	���������� = Mid(SYSIN, 0, 72).split(" ")
#	����������2 = ArrayEmptyDelete(SYSIN.split(" "))       ###2020/2/13 �ǉ�
	����������2 = ArrayEmptyDelete(Mid(SYSIN, 0, 72).split(" "))
#'UPD END

	���Y�֘A��_�ǉ�_CNT = 0
	JCL_PGM_DSN_�ǉ�_CNT = 0
	JCL_PGM_DSN_�X�V_CNT = 0
	UTL_STEP��_IO���_�ǉ�_CNT = 0

	return ActSheet_x


def �p��������������(ActSheet_x,data):
    global ���p_�ڋq��_JCL_PGM_DSN_,���p_UTL_STEP��_IO���_
    global SYSIN
    global DELETE�p��,DUMP�p��,RESTORE�p��,FTP�p��,DEFCL�p��,DEFPATH�p��,DEFAIX�p��,DEFNVSAM�p��,DEFUCAT�p��,COPY�p��,LOAD�p��,UNLOAD�p��,UTACH�p��
    global DD_CNT,����DD,IO����,�ǉ�DSN,����DD_OUT_SV,����������,����������2,vbCrLf
#'20240215 ADD qian.e.wang
    global ADARUN3V�p��,JYAADP�p��,ADM�p��
#'ADD END
    
    L_str = ""
    
    
    ###���ʔ���
    if data["SYSIN_SEQ"] == 1:
       DD_CNT = 0

    if DUMP�p��:
        if data["SYSIN_SEQ"] == 1:
            DUMP�p�� = False
            ###DD_CNT = 0
 
    ###if RESTORE�p��:    '�����ł͉������Ȃ�RESTorE�������Ŏ��{
    ###    if data["SYSIN_SEQ = 1:
    ###      RESTORE�p�� = False
    ###      'DD_CNT = 0
       
    if DELETE�p��:
        if data["SYSIN_SEQ"] == 1:
            DELETE�p�� = False
            ###DD_CNT = 0
        elif "DEFINE " in SYSIN or  "DEF " in SYSIN:
            DELETE�p�� = False

    if COPY�p��:
        if data["SYSIN_SEQ"] == 1:
            COPY�p�� = False
            ###DD_CNT = 0
        elif "COPY " not in SYSIN:
            COPY�p�� = False

    if LOAD�p��:
        if data["SYSIN_SEQ"] == 1:
            LOAD�p�� = False
        else:
            ActSheet_x[12] = "LOAD�p��"
            if "INTO " in SYSIN and " TABLE " in SYSIN:
                for i in range(len(����������2)):
                    if ����������2[i] == "TABLE":
                        ����DD = "_SYSD001"
                        IO���� = "OUTPUT"
           
                      ###UTL_STEP��_IO��� �o��
                    if ���p_UTL_STEP��_IO���_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                        ActSheet_x[16] = 0
                    else:
                        ActSheet_x[16] = 1
           
                      ### �ڋq��_JCL_PGM_DSN �o��
                    if i + 1 < len(����������2):
                        �ǉ�DSN = ����������2[i + 1]
                        
                        �ǉ�DSN = �ǉ�DSN.replace("JBDB2.", "")     ###MHI�Č��̂ݎb��Ή�
                        if ���p_�ڋq��_JCL_PGM_DSN_.insert() == False:
                            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                            ActSheet_x[14] = 0
                        else:
                            ActSheet_x[14] = 1
                        ActSheet_x[17] = �ǉ�DSN
                    else:
                        ActSheet_x[12] = ActSheet_x[12] + " �z��v�f�v�m�F"      ###LOAD�����1�s���ɋL�ڂ�����z��


    if UNLOAD�p��:
        if data["SYSIN_SEQ"] == 1:
            UNLOAD�p�� = False
        else:
           ActSheet_x[12] = "UNLOAD�p��"
           if "FROM " in SYSIN and " TABLE " in SYSIN:
           
                for i in range(len(����������2)):
                    if ����������2[i] == "TABLE":
                        ����DD = "_SYSD001"
                        IO���� = "INPUT"
           
                      ###UTL_STEP��_IO��� �o��
                        if ���p_UTL_STEP��_IO���_.insert() == False:
                            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                            ActSheet_x[16] = 0
                        else:
                            ActSheet_x[16] = 1
           
                      ###�ڋq��_JCL_PGM_DSN �o��
                        if i + 1 < len(����������2):
                            �ǉ�DSN = ����������2[i + 1]
                            �ǉ�DSN = �ǉ�DSN.replace("JBDB2.", "")     ###MHI�Č��̂ݎb��Ή�
                            if ���p_�ڋq��_JCL_PGM_DSN_.insert() == False:
                                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                                ActSheet_x[14] = 0
                            else:
                                ActSheet_x[14] = 1
                            ActSheet_x[17] = �ǉ�DSN
                        else:
                            ActSheet_x[12] = ActSheet_x[12] + " �z��v�f�v�m�F"      ###UNLOAD������1�s���ɋL�ڂ�����z��


    if DEFCL�p��:   ###DEFCL�p����DELETE�p���͏d�����邱�Ƃ�����
         
        if "NAME" in SYSIN:     ###1�s�Ŋ������邩�ǂ���
                  
            for i in range(len(����������)):
                if "NAME" in ����������[i]:
                    �ǉ�DSN = ����������[i].replace("CLUSTER", "").replace("NAME", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
         
             ###�ڋq��_JCL_PGM_DSN �o��
             
            if ���p_�ڋq��_JCL_PGM_DSN_.insert() == False:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                ActSheet_x[14] = 0
            else:
                ActSheet_x[14] = 1
            ActSheet_x[17] = �ǉ�DSN     ###CHK�̂��߂ɒǉ� 2020/1/10
                      
            DEFCL�p�� = False
        
        if data["SYSIN_SEQ"] == 1:  ###���NAME��`��������Ȃ������ꍇ�ׂ̈ɔO�̂���
            DEFCL�p�� = False
            ###DD_CNT = 0
    
    ###20210312 Add Horiuchi
    if DEFAIX�p�� or DEFPATH�p�� or DEFNVSAM�p�� or DEFUCAT�p��:   ###DEFCL�p����DELETE�p���͏d�����邱�Ƃ�����
        if "NAME" in SYSIN:     ###1�s�Ŋ������邩�ǂ���
            for i in range(len(����������)):
                if "NAME" in ����������[i]:
                    if DEFAIX�p��:
                        �ǉ�DSN = ����������[i].replace("ALTERNATEINDEX", "").replace("AIX", "").replace("NAME", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
                    elif DEFPATH�p��:
                        �ǉ�DSN = ����������[i].replace("PATH", "").replace("NAME", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
                    elif DEFNVSAM�p��:
                        �ǉ�DSN = ����������[i].replace("NONVSAM", "").replace("NVSAM", "").replace("NAME", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
                    elif DEFUCAT�p��:
                        �ǉ�DSN = ����������[i].replace("USERCATALOG", "").replace("UCAT", "").replace("NAME", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
  
           
             ###�ڋq��_JCL_PGM_DSN �o��
             
            if ���p_�ڋq��_JCL_PGM_DSN_.insert() == False:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                ActSheet_x[14] = 0
            else:
                ActSheet_x[14] = 1
            ActSheet_x[17] = �ǉ�DSN     ###CHK�̂��߂ɒǉ� 2020/1/10
                      
            DEFAIX�p�� = False
            DEFPATH�p�� = False
            DEFNVSAM�p�� = False
            DEFUCAT�p�� = False
        if data["SYSIN_SEQ"] == 1:  ###���NAME��`��������Ȃ������ꍇ�ׂ̈ɔO�̂���
            DEFAIX�p�� = False
            DEFPATH�p�� = False
            DEFNVSAM�p�� = False
            DEFUCAT�p�� = False
   
    if UTACH�p��:
        if data["SYSIN_SEQ"] == 1:
            UTACH�p�� = False
   
#'20240215 ADD qian.e.wang
    if ADARUN3V�p��:
        if data["SYSIN_SEQ"] == 1:
            ADARUN3V�p�� = False
   
    if JYAADP�p��:
        if data["SYSIN_SEQ"] == 1:
            JYAADP�p�� = False
   
    if ADM�p��:
        if data["SYSIN_SEQ"] == 1:
            ADM�p�� = False
#'ADD END

    return ActSheet_x



def DELETE�p������(ActSheet_x,data):
    global ���p_�ڋq��_JCL_PGM_DSN_,���p_UTL_STEP��_IO���_
    global SYSIN
    global DELETE�p��,DEFCL�p��
    global DD_CNT,����DD,IO����,�ǉ�DSN,����PGM,����������,����������2,vbCrLf
    
    
    
    ActSheet_x[12] = "DELETE-�p��"
               
    SYSIN = data["SYSIN"]
    if "DELETE " in SYSIN or "DEL " in SYSIN:
            DD_CNT = DD_CNT + 1
            �ǉ�DSN = SYSIN[:72].replace("  CLUSTER", "").replace("*", "")
            �ǉ�DSN = �ǉ�DSN.replace("DELETE ", "").replace("DEL ", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
            ����DD = "_SYSD" + str(DD_CNT).zfill(3)
            IO���� = "DELETE"
            ����PGM = PGM_NAME

            ### UTL_STEP��_IO��� �o��
            if ���p_UTL_STEP��_IO���_.insert() == False:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                ActSheet_x[16] = 0
            else:
                ActSheet_x[16] = 1
            
            ����PGM = ""     ###
            ActSheet_x[17] = �ǉ�DSN
            
            ### �ڋq��_JCL_PGM_DSN �o��
            if ���p_�ڋq��_JCL_PGM_DSN_.insert() == False:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                ActSheet_x[14] = 0
            else:
                ActSheet_x[14] = 1

    
    ###DELETE�p�����i��j��DEFINE CLUSTER�̃R�}���h�����s�����ꍇ�̑Ή�
    if "DEFINE " in SYSIN or "DEF " in SYSIN:
        DELETE�p�� = False
        ActSheet_x[12] = "DEFCL-�p��"
    
        ����DD = "_SYSD" + str(DD_CNT).zfill(3)
        DD_CNT = DD_CNT + 1
        
        ### UTL_STEP��_IO��� �o��
        if ���p_UTL_STEP��_IO���_.insert() == False:
            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
        else:
            ActSheet_x[16] = 1
    
        if "NAME" in SYSIN:     ###1�s�Ŋ������邩�ǂ���
            
            for i in range(len(����������)):
                if "NAME" in ����������[i]:
                    �ǉ�DSN = ����������[i].replace("CLUSTER", "").replace("NAME", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")

            ### �ڋq��_JCL_PGM_DSN �o��    ���F�u���C�N��Ȃ̂�1�s�O�ɏo�͂���i���j
            if ���p_�ڋq��_JCL_PGM_DSN_.insert() == False:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
            else:
                ActSheet_x[14] = 1
 
        else:
            DEFCL�p�� = True

    return ActSheet_x

def DUMP�p������(ActSheet_x,data):
    global ���p_�ڋq��_JCL_PGM_DSN_,���p_UTL_STEP��_IO���_
    global SYSIN
    global DD_CNT,����DD,IO����,�ǉ�DSN,����PGM,vbCrLf
    
    
    
    ActSheet_x[12] = "DUMP-�p��"
              
    SYSIN = data["SYSIN"]
            
    if "ENQF" in SYSIN:
        pass
    else:
        �ǉ�DSN = SYSIN[:72].replace("DATASET", "").replace("INCLUDE", "").replace("INCL(", "").replace("DS(", "") ###�ǉ��Ή������ɂ����̂ōs����
        �ǉ�DSN = �ǉ�DSN.replace("-", "").replace("(", "").replace(")", "").replace( " ", "")
        DD_CNT = DD_CNT + 1
        ����DD = "_SYSD" + str(DD_CNT).zfill(3)
        ###IO���� = "INPUT"  'MHI�b��Ή��@�o�b�N�A�b�v��INPUT�͎�̔��肵�Ȃ�
        IO���� = "INPUT_���菜�O"
        ����PGM = PGM_NAME
        
        ###�s��OPTION���O
        if �ǉ�DSN == "SHR" or �ǉ�DSN == "SETMAXCC=0" or �ǉ�DSN == "OPT4" or �ǉ�DSN == "DELUNCATPURGE":  ###  '�����̓s�x�ǉ�����
            ActSheet_x[17] = �ǉ�DSN
            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "OPTION�L�[���[�h�̈׏���SKIP"
            return ActSheet_x
    
        
        ### UTL_STEP��_IO��� �o��?A
        if ���p_UTL_STEP��_IO���_.insert() == False:
            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
        else:
            ActSheet_x[16] = 1
        
        ActSheet_x[17] = �ǉ�DSN
        ����PGM = ""     ###'
        
        ### �ڋq��_JCL_PGM_DSN �o��
        if ���p_�ڋq��_JCL_PGM_DSN_.insert() == False:
            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
        else:
            ActSheet_x[14] = 1

    return ActSheet_x
    

def RESTORE�p������(ActSheet_x,data):
    global ���p_�ڋq��_JCL_PGM_DSN_
    global ActSheet 
    global SYSIN

    global DD_CNT,����DD,IO����,�ǉ�DSN,����PGM,�u��DSN,����DD_OUT_SV,vbCrLf
    global ����������,����������2,���I�v�f,�v�f��
    global JCL_NAME,JOB_SEQ,STEP_SEQ,RESTORE�p��
    global L_JCL_NAME_SV, L_JOB_SEQ_SV,L_STEP_SEQ_SV,RESTORE���[�h
    global JCL_NAME_SV,JOB_SEQ_SV,STEP_SEQ_SV 
    
    global PGM_NAME
    
    L_JCL_NAME_SV = ""   ###�u���C�N��ɗ��p����̂őޔ�����
    L_JOB_SEQ_SV = ""
    L_STEP_SEQ_SV = ""
    

    goto_flag = False  ### GO TO ���̑���� flag
    if len(data) == 0:     ###�����s�ɂ܂������ď������������邽�߂����Ŏ��{
        goto_flag = True
    else:
    
        if data["SYSIN_SEQ"] == 1:
           goto_flag = True
        
        if goto_flag == False:
            ### �p������
            
            ActSheet_x[12] = " RESTORE-�p��"
                    
            if RESTORE���[�h == "":
            
                if "DATASET(" in SYSIN:
                    RESTORE���[�h = "DATASET"
                    for i in range(len(����������2)):
                        if "DATASET(" in ����������2[i]:
                            �ǉ�DSN = ����������2[0].replace(" ", "").replace("-", "").replace("INCLUDE", "").replace("DATASET", "").replace("(", "").replace(")", "") ###��Ŋm�F����@���Ԃ� i ��������
                    �v�f�� = 1
                    ���I�v�f = [�ǉ�DSN]
                    ActSheet_x[17] = �ǉ�DSN
                    
            elif RESTORE���[�h == "DATASET":
            
                if "RENAMEU" in SYSIN:
                    RESTORE���[�h = "RENAMEU"
                    �ǉ�DSN = ""
                    �u��DSN = ""
                    for i in range(len(����������2)):
                        if "RENAMEU(" in ����������2[i]:
                            if �ǉ�DSN == "":
                                �ǉ�DSN = ����������2[i].replace("RENAMEU", "").replace("(", "")
                        elif �u��DSN == "":
                            if �ǉ�DSN != "":
                                �u��DSN = ����������2[i].replace("RENAMEU", "").replace("(", "").replace(")", "")
                    
                    if �ǉ�DSN != "" and �u��DSN != "":
                        for j in range(len(���I�v�f)):
                            ���I�v�f[j] = ���I�v�f[j].replace(�ǉ�DSN, �u��DSN)
                        ActSheet_x[17] = �u��DSN
                    
                else: ### '����DATASET�����@�z��Ɋi�[
                                            
                    �ǉ�DSN = ����������2[0].replace(" ", "").replace("-", "").replace("INCLUDE", "").replace("DATASET", "").replace("(", "").replace(")", "")
                    �v�f�� += 1
                    ���I�v�f.append(�ǉ�DSN)
                    ActSheet_x[17] = �ǉ�DSN
                
            elif RESTORE���[�h == "RENAMEU":
            
                if len(����������2) > 1:
                    �ǉ�DSN = ����������2[0].replace("RENAMEU", "").replace("(", "")
                    �u��DSN = ����������2[1].replace("RENAMEU", "").replace("(", "").replace(")", "")
            
                    if �ǉ�DSN != "" and �u��DSN != "":
                        for j in range(len(���I�v�f)):
                            ���I�v�f[j] = ���I�v�f[j].replace(�ǉ�DSN, �u��DSN)
                        ActSheet_x[17] = �u��DSN
                else:
                    ActSheet_x[12] = ActSheet_x[12] + " SKIP"
                

            if data["SYSIN_SEQ"] != 1:
                return ActSheet_x

            
        ###�p����������  ��RENAMEU���Ȃ��ꍇ�͂����ŉ�������� ����������1�s�O����������
        ###�@�u���C�N�������@

   

    L_JCL_NAME_SV = JCL_NAME   ###�ŐV��Ԃ̑ޔ�
    L_JOB_SEQ_SV = JOB_SEQ
    L_STEP_SEQ_SV = STEP_SEQ

    JCL_NAME = JCL_NAME_SV     ### �ޔ����Ă����l�̕���
    JOB_SEQ = JOB_SEQ_SV
    STEP_SEQ = STEP_SEQ_SV

    ����DD = ����DD_OUT_SV
    for j in range(len(���I�v�f)):
        if ���I�v�f[j] == "":
            continue
        
        �ǉ�DSN = ���I�v�f[j]
        ### �ڋq��_JCL_PGM_DSN �o��    '
        if len(ActSheet) > 0:
            if ���p_�ڋq��_JCL_PGM_DSN_.insert() == False:
                ActSheet[-1][12] = ActSheet[-1][12] + vbCrLf + "KEY�d���̈׏���SKIP"
            else:
                if ActSheet[-1][14] == "":
                    ActSheet[-1][14] = 1
                else:
                    ActSheet[-1][14] = ActSheet[-1][14] + 1
        

    �ǉ�DSN = ""
    ����DD = ""
    ����DD_OUT_SV = ""
        
    JCL_NAME_SV = ""
    JOB_SEQ_SV = 0
    STEP_SEQ_SV = 0
        
    JCL_NAME = L_JCL_NAME_SV   ### �ޔ����Ă����l�̕���
    JOB_SEQ = L_JOB_SEQ_SV
    STEP_SEQ = L_STEP_SEQ_SV
        
    RESTORE�p�� = False

    return ActSheet_x
    


def FTP�p������(ActSheet_x,data):
    global ���p_�ڋq��_JCL_PGM_DSN_,���p_UTL_STEP��_IO���_
    global FTP�p��,SYSIN,�]���p��
    global DD_CNT,����DD,IO����,�ǉ�DSN,����PGM
    global UTL_STEP��_IO���_�ǉ�_CNT,JCL_PGM_DSN_�ǉ�_CNT,����������2,vbCrLf
    

    
    # '=== FTP �iMSP�j===   2021/12/16 ADD
    # 'JCL�T���v��
    # 'FTP A('TISP.FTP.ATTR')
    # 'HOST 172.22.106.41
    # 'SEND IN('USR1.TESTDATA')
    # '     OUT('D:\TESTDATA.bin')
    # '     T(B)
    # '     SYN
    # '     CNVT(NO)
    # '     TYPE(TEXT)
    # '     V(SZIA22)
    # 'RECV IN('D:\Work\IEBGENER.txt')
    # '     OUT('USR1.JCL(IEBGENER)')
    # '     T(T)
    # '     C(Y)
    # '     SYN
    # 'END

    if data["SYSIN_SEQ"] == 1:
        FTP�p�� = False
    else:
        ###�]���J�n
        if " SEND " in SYSIN or str(SYSIN).startswith("SEND "):
            �]���p�� = "SEND"
        if " RECV " in SYSIN or str(SYSIN).startswith("RECV "):
            �]���p�� = "RECV"
        ### �]���I��
        
        if " END " in SYSIN or str(SYSIN).startswith("END "):
            FTP�p�� = False
            �]���p�� = ""
       
        if �]���p�� != "" and ( " IN(" in SYSIN or " OUT(" in SYSIN):
            ActSheet_x[12] = " FTP-" + �]���p�� + "-�p��"
            �ǉ�DSN = ""
            
            for i in range(len(����������2)):
                if "IN(" in ����������2[i]:
                    ### UTL_STEP��_IO��� �o��
                    ����DD = "FTP_" + �]���p�� + "_IN"
                    IO���� = "INPUT"
                    if ���p_UTL_STEP��_IO���_.insert() == False:
                       ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                    else:
                       UTL_STEP��_IO���_�ǉ�_CNT = UTL_STEP��_IO���_�ǉ�_CNT + 1
                    
                    ### �ڋq��_JCL_PGM_DSN �o��
                    �ǉ�DSN = ����������2[i].replace("IN(", "").replace(")", "").replace("\'", "").replace("\"", "").rstrip("\+\-")
                    if ���p_�ڋq��_JCL_PGM_DSN_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                    else:
                        JCL_PGM_DSN_�ǉ�_CNT = JCL_PGM_DSN_�ǉ�_CNT + 1
                
                if "OUT(" in ����������2[i]:
                    ### UTL_STEP��_IO��� �o��
                    ����DD = "FTP_" + �]���p�� + "_OUT"
                    IO���� = "OUTPUT"
                    if ���p_UTL_STEP��_IO���_.insert() == False:
                       ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                    else:
                       UTL_STEP��_IO���_�ǉ�_CNT = UTL_STEP��_IO���_�ǉ�_CNT + 1
                    
                    ### �ڋq��_JCL_PGM_DSN �o��
                    �ǉ�DSN = ����������2[i].replace("OUT(", "").replace(")", "").replace("\'", "").replace("\"", "").rstrip("\+\-")
                    if ���p_�ڋq��_JCL_PGM_DSN_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                    else:
                        JCL_PGM_DSN_�ǉ�_CNT = JCL_PGM_DSN_�ǉ�_CNT + 1
                
                ActSheet_x[14] = JCL_PGM_DSN_�ǉ�_CNT
                ActSheet_x[16] = UTL_STEP��_IO���_�ǉ�_CNT
                ActSheet_x[17] = ActSheet_x[17] + vbCrLf + �ǉ�DSN
                
    return ActSheet_x

def JCL_STEP_SYSIN���_����UTL���胍�W�b�N(ActSheet_x,data):
    #global REPRO_OUTDATASET_���pDD�擾_,���p_�ڋq��_JCL_STEP_SYSIN_,���p_�ڋq��_���Y�֘A�����_,���p_�ڋq��_JCL_PGM_DSN_,���p_UTL_STEP��_IO���_
    global REPRO_OUTDATASET_���pDD�擾_,���p_�ڋq��_JCL_STEP_SYSIN_,���p_�ڋq��_JCL_PGM_DSN_,���p_UTL_STEP��_IO���_
    ###��UTL�Ή�
    ### === IDCAMS ===
    global SYSIN
    global LIBRARY_ID,JCL_NAME,JOB_SEQ,JOB_ID,STEP_SEQ,STEP_ID,PGM_NAME,PROC_NAME,SYSIN_PGM,SYSIN_SEQ,PARM_EXEC,PARM_PROC
    global DELETE�p��,DUMP�p��,RESTORE�p��,FTP�p��,DEFCL�p��,DEFPATH�p��,DEFAIX�p��,DEFNVSAM�p��,DEFUCAT�p��,COPY�p��,LOAD�p��,UNLOAD�p��,UTACH�p��
    global DD_CNT,����DD,IO����,�ǉ�DSN,����PGM,RESTORE���[�h,����DD_OUT_SV,�ďo���@,����������,����������2,UTL_STEP��_IO���_�ǉ�_CNT,JCL_PGM_DSN_�ǉ�_CNT
    global �v�f��,���I�v�f
    global JCL_NAME_SV,JOB_SEQ_SV,STEP_SEQ_SV,vbCrLf
#'20240215 ADD qian.e.wang
    global ADARUN3V�p��,JYAADP�p��,ADM�p��
    # DEBUG
    # print("�� JCL_NAME :["+str(JCL_NAME)+"] PGM_NAME :["+str(PGM_NAME)+"]  SYSIN :["+str(SYSIN)+"]\r\n")
#'ADD END
    
    
    if PGM_NAME == "IDCAMS":                     ###SAM,VSAM,�J�^���O����
        if "REPRO " in SYSIN:
            ActSheet_x[12] = "REPRO"
            for i in range(len(����������)):
                if "INFILE" in ����������[i]:
                    ����DD = ����������[i].replace("INFILE", "").replace("(", "").replace(")", "")
                    IO���� = "INPUT"
 
                    ### UTL_STEP��_IO��� �o��
                    if ���p_UTL_STEP��_IO���_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                    else:
                        UTL_STEP��_IO���_�ǉ�_CNT = UTL_STEP��_IO���_�ǉ�_CNT + 1
 
                elif "OUTFILE" in ����������[i]:
                    ����DD = ����������[i].replace("OUTFILE", "").replace("(", "").replace(")", "")
                    IO���� = "OUTPUT"
 
                  ###UTL_STEP��_IO��� �o��
                    if ���p_UTL_STEP��_IO���_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                    else:
                        UTL_STEP��_IO���_�ǉ�_CNT = UTL_STEP��_IO���_�ǉ�_CNT + 1
                  
                elif "OUTDATASET" in ����������[i]:
                    �ǉ�DSN = ����������[i].replace("OUTDATASET(", "").replace(")", "")
                    ActSheet_x[17] = �ǉ�DSN
                    ����DD = REPRO_OUTDATASET_���pDD�擾_.get()
                    IO���� = "OUTPUT"
                    if ����DD != "":
                    
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "OUTDATASET ����DD: " + ����DD
                       ###UTL_STEP��_IO��� �o��
                        if ���p_UTL_STEP��_IO���_.update() == False:
                            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                        else:
                            UTL_STEP��_IO���_�ǉ�_CNT = UTL_STEP��_IO���_�ǉ�_CNT + 1
                    
                    else:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "OUTDATASET ����DD�����˒ǉ�"
                        DD_CNT = DD_CNT + 1
                        ����DD = "_SYSD" + str(DD_CNT).zfill(3)
                        ###UTL_STEP��_IO��� �o��
                        if ���p_UTL_STEP��_IO���_.insert() == False:
                            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                        else:
                            UTL_STEP��_IO���_�ǉ�_CNT = UTL_STEP��_IO���_�ǉ�_CNT + 1
                       
                        ###�ڋq��_JCL_PGM_DSN �o��
                        if ���p_�ڋq��_JCL_PGM_DSN_.insert() == False:
                            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                            ActSheet_x[14] = 0
                        else:
                            ActSheet_x[14] = 1
                  
            ActSheet_x[16] = UTL_STEP��_IO���_�ǉ�_CNT
            if UTL_STEP��_IO���_�ǉ�_CNT != 2:
                ActSheet_x[12] = ActSheet_x[12] + " �v�m�F"
           
        elif "DELETE " in SYSIN or "DEL " in SYSIN:
            ActSheet_x[12] = "DELETE"
        #    'for i in range(len(����������)
        #    '    if InStr(����������[i], "DELETE" in SYSIN Or InStr(����������[i], "DEL" in SYSIN:
                  
                #   '����DD = "_SYSD001"
            DD_CNT = DD_CNT + 1
            ����DD = "_SYSD" + str(DD_CNT).zfill(3)
            IO���� = "DELETE"
            �ǉ�DSN = SYSIN[:72].replace("  CLUSTER", "")
            �ǉ�DSN = �ǉ�DSN.replace("DELETE ", "").replace("DEL ", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
            ����PGM = PGM_NAME
                  
                      
          ###UTL_STEP��_IO��� �o��
            if ���p_UTL_STEP��_IO���_.insert() == False:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                ActSheet_x[16] = 0
            else:
                ActSheet_x[16] = 1
            ActSheet_x[17] = �ǉ�DSN
                   
            ����PGM = ""    ### '
                   
        #    �ڋq��_JCL_PGM_DSN �o��
            if ���p_�ڋq��_JCL_PGM_DSN_.insert() == False:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                ActSheet_x[14] = 0
            else:
                ActSheet_x[14] = 1
                      
           ###DD_CNT = 1
            DD_CNT = DD_CNT + 1
            DELETE�p�� = True

           
        elif "DEFINE " in SYSIN or "DEF " in SYSIN:
            ActSheet_x[12] = "DEF-CL"
           
           ###����DD = "_SYSD001"
            DD_CNT = DD_CNT + 1
            ����DD = "_SYSD" + str(DD_CNT).zfill(3)
           
            IO���� = "OUTPUT"
          
            ###UTL_STEP��_IO��� �o��
            if ���p_UTL_STEP��_IO���_.insert() == False:
                if ���p_UTL_STEP��_IO���_.update() == False:
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                    ActSheet_x[16] = 0
                else:
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "STEP-IO�X�V(OUTPUT)"
                    ActSheet_x[16] = 1
            else:
                ActSheet_x[16] = 1
           
            if "NAME" in SYSIN:     ###1�s�Ŋ������邩�ǂ���
                  
                for i in range(len(����������)):
                    if "NAME" in ����������[i]:
                        �ǉ�DSN = ����������[i].replace("CLUSTER", "").replace("CL(", "").replace("NAME", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
           
                ###�ڋq��_JCL_PGM_DSN �o��    '���F�u���C�N��Ȃ̂�1�s�O�ɏo�͂���i���j
                if ���p_�ڋq��_JCL_PGM_DSN_.insert() == False:
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                    ActSheet_x[14] = 0
                else:
                    ActSheet_x[14] = 1
                ActSheet_x[17] = �ǉ�DSN     ###CHK�̂��߂ɒǉ� 2020/1/10
           
            else:
                DEFCL�p�� = True

    elif PGM_NAME == "KQCAMS":
        if "BLDINDEX " in SYSIN or "BIX " in SYSIN:
            # '=============================================================
            # '�R�}���h : BLDINDEX'
            # '=============================================================
            ActSheet_x[12] = "BIX"
            for i in range(len(����������)):
                
                if ����������[i] == "":
                    pass
                    ###�󕶎��̓X���[
                    
                elif "INFILE" in ����������[i] or "IFILE" in ����������[i]:
                        # '---------------------------------
                        # 'Operand : INFILE
                        # '---------------------------------
                    ����DD = ����������[i].replace("INFILE", "").replace("IFILE", "").replace("(", "").replace(")", "")
                    IO���� = "INPUT"
                    # 'UTL_STEP��_IO��� �o��
                    if ���p_UTL_STEP��_IO���_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                    else:
                        UTL_STEP��_IO���_�ǉ�_CNT = UTL_STEP��_IO���_�ǉ�_CNT + 1
                        
                elif "OUTFILE" in ����������[i] or "OFILE" in ����������[i]:
                        # '---------------------------------
                        # 'Operand : OUTFILE
                        # '---------------------------------
                    ����DD = ����������[i].replace("OUTFILE", "").replace("OFILE", "").replace("(", "").replace(")", "")
                    IO���� = "OUTPUT"
                    # 'UTL_STEP��_IO��� �o��
                    if ���p_UTL_STEP��_IO���_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                    else:
                        UTL_STEP��_IO���_�ǉ�_CNT = UTL_STEP��_IO���_�ǉ�_CNT + 1
                        
                elif "INDATASET" in ����������[i] or "IDS" in ����������[i]:
                    # '---------------------------------
                    # 'Operand : INDATASET
                    # '---------------------------------
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + " KQCAMS/BULDINDEX/INDATASET�g�p : �c�[�����C���K�v"
                elif "OUTDATASET" in ����������[i] or "ODS" in ����������[i]:
                    # '---------------------------------
                    # 'Operand : OUTDATASET
                    # '---------------------------------
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + " KQCAMS/BULDINDEX/OUTDATASET�g�p : �c�[�����C���K�v"
           
            ActSheet_x[16] = UTL_STEP��_IO���_�ǉ�_CNT
            if UTL_STEP��_IO���_�ǉ�_CNT != 2:
                ###IN/OUT��2���ǉ������͂�
                ActSheet_x[12] = ActSheet_x[12] + " �v�m�F"
                
        elif "REPRO " in SYSIN:
            ActSheet_x[12] = "REPRO"
            for i in range(len(����������)):
                if "INFILE" in ����������[i]:
                    ����DD = ����������[i].replace("INFILE", "").replace("(", "").replace(")", "")
                    IO���� = "INPUT"
 
                  ###UTL_STEP��_IO��� �o��
                    if ���p_UTL_STEP��_IO���_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                    else:
                        UTL_STEP��_IO���_�ǉ�_CNT = UTL_STEP��_IO���_�ǉ�_CNT + 1
 
                elif "OUTFILE" in ����������[i]:
                    ����DD = ����������[i].replace("OUTFILE", "").replace("(", "").replace(")", "")
                    IO���� = "OUTPUT"
 
                  ###UTL_STEP��_IO��� �o��
                    if ���p_UTL_STEP��_IO���_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                    else:
                        UTL_STEP��_IO���_�ǉ�_CNT = UTL_STEP��_IO���_�ǉ�_CNT + 1
                  
                elif "OUTDATASET" in ����������[i]:
                    �ǉ�DSN = ����������[i].replace("OUTDATASET(", "").replace(")", "")
                    ActSheet_x[17] = �ǉ�DSN
                    ����DD = REPRO_OUTDATASET_���pDD�擾_.get()
                    IO���� = "OUTPUT"
                    if ����DD != "":
                    
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "OUTDATASET ����DD: " + ����DD
                        ####UTL_STEP��_IO��� �o��
                        if ���p_UTL_STEP��_IO���_.update() == False:
                            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                        else:
                            UTL_STEP��_IO���_�ǉ�_CNT = UTL_STEP��_IO���_�ǉ�_CNT + 1
                    
                    else:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "OUTDATASET ����DD�����˒ǉ�"
                        DD_CNT = DD_CNT + 1
                        ����DD = "_SYSD" + str(DD_CNT).zfill(3)
                        ###UTL_STEP��_IO��� �o��
                        if ���p_UTL_STEP��_IO���_.insert() == False:
                            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                        else:
                            UTL_STEP��_IO���_�ǉ�_CNT = UTL_STEP��_IO���_�ǉ�_CNT + 1
                       
                        ###�ڋq��_JCL_PGM_DSN �o��
                        if ���p_�ڋq��_JCL_PGM_DSN_.insert() == False:
                            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                            ActSheet_x[14] = 0
                        else:
                            ActSheet_x[14] = 1
                  
            ActSheet_x[16] = UTL_STEP��_IO���_�ǉ�_CNT
            if UTL_STEP��_IO���_�ǉ�_CNT != 2:
                ActSheet_x[12] = ActSheet_x[12] + " �v�m�F"
           
        elif "DELETE " in SYSIN or "DEL " in SYSIN:
            # '=============================================================
            # '�R�}���h : DELETE / DEL'
            # '=============================================================
            ActSheet_x[12] = "DELETE"
            DD_CNT = DD_CNT + 1
            ����DD = "_SYSD" + str(DD_CNT).zfill(3)
            IO���� = "DELETE"
            �ǉ�DSN = SYSIN[:72].replace("  CLUSTER", "")
            �ǉ�DSN = �ǉ�DSN.replace("DELETE ", "").replace("DEL ", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
            ����PGM = PGM_NAME
        #   UTL_STEP��_IO��� �o��
            if ���p_UTL_STEP��_IO���_.insert() == False:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                ActSheet_x[16] = 0
            else:
                ActSheet_x[16] = 1
            ActSheet_x[17] = �ǉ�DSN
                   
            ����PGM = ""     ###'
            ###�ڋq��_JCL_PGM_DSN �o��
            if ���p_�ڋq��_JCL_PGM_DSN_.insert() == False:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                ActSheet_x[14] = 0
            else:
                ActSheet_x[14] = 1
                      
            DD_CNT = DD_CNT + 1
            DELETE�p�� = True
        elif "EXPORT " in SYSIN:
            # '=============================================================
            # '�R�}���h : EXPORT'
            # '=============================================================
            # '����͌p���s����͕s�v�Ȃ̂ŁA���Ή�
            ActSheet_x[12] = "EXPORT"
            for i in range(len(����������)):
                
                if "OUTFILE" in ����������[i] or  "OFILE" in ����������[i]:
                    # '---------------------------------
                    # 'Operand : OUTFILE
                    # '---------------------------------
                    ����DD = ����������[i].replace("OUTFILE", "").replace("OFILE", "").replace("(", "").replace(")", "")
                    IO���� = "OUTPUT"
                    if ���p_UTL_STEP��_IO���_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                    else:
                        UTL_STEP��_IO���_�ǉ�_CNT = UTL_STEP��_IO���_�ǉ�_CNT + 1
                elif "INFILE" in ����������[i] or "IFILE" in ����������[i]:
                    # '---------------------------------
                    # 'Operand : INFILE
                    # '---------------------------------
                    ����DD = ����������[i].replace("INFILE", "").replace("IFILE", "").replace("(", "").replace(")", "")
                    IO���� = "INPUT"
                    if ���p_UTL_STEP��_IO���_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                    else:
                        UTL_STEP��_IO���_�ǉ�_CNT = UTL_STEP��_IO���_�ǉ�_CNT + 1
                elif "INDATASET" in ����������[i]:
                    # '---------------------------------
                    # 'Operand : INDATASET
                    # '---------------------------------
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + " KQCAMS/EXPORT/INDATASET�g�p : �c�[�����C���K�v"
                elif "OUTDATASET" in ����������[i]:
                    # '---------------------------------
                    # 'Operand : OUTDATASET
                    # '---------------------------------
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + " KQCAMS/EXPORT/OUTDATASET�g�p : �c�[�����C���K�v"
                    
            ActSheet_x[16] = UTL_STEP��_IO���_�ǉ�_CNT
            if UTL_STEP��_IO���_�ǉ�_CNT != 2 and UTL_STEP��_IO���_�ǉ�_CNT != 0:
                ActSheet_x[12] = ActSheet_x[12] + " �v�m�F"
                
        elif "IMPORT " in SYSIN:
            # '=============================================================
            # '�R�}���h : IMPORT'
            # '=============================================================
            ActSheet_x[12] = "IMPORT"
            for i in range(len(����������)):
                
                if "OUTFILE" in ����������[i] or  "OFILE" in ����������[i]:
                    # '---------------------------------
                    # 'Operand : OUTFILE
                    # '---------------------------------
                    ����DD = ����������[i].replace("OUTFILE", "").replace("OFILE", "").replace("(", "").replace(")", "")
                    IO���� = "OUTPUT"
                    if ���p_UTL_STEP��_IO���_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                    else:
                        UTL_STEP��_IO���_�ǉ�_CNT = UTL_STEP��_IO���_�ǉ�_CNT + 1
                elif "INFILE" in ����������[i] or "IFILE" in ����������[i]:
                    # '---------------------------------
                    # 'Operand : INFILE
                    # '---------------------------------
                    ����DD = ����������[i].replace("INFILE", "").replace("IFILE", "").replace("(", "").replace(")", "")
                    IO���� = "INPUT"
                    if ���p_UTL_STEP��_IO���_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                    else:
                        UTL_STEP��_IO���_�ǉ�_CNT = UTL_STEP��_IO���_�ǉ�_CNT + 1
                elif "INDATASET" in ����������[i]:
                    # '---------------------------------
                    # 'Operand : INDATASET
                    # '---------------------------------
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + " KQCAMS/IMPORT/INDATASET�g�p : �c�[�����C���K�v"
                elif "OUTDATASET" in ����������[i]:
                    # '---------------------------------
                    # 'Operand : OUTDATASET
                    # '---------------------------------
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + " KQCAMS/IMPORT/OUTDATASET�g�p : �c�[�����C���K�v"
            ActSheet_x[16] = UTL_STEP��_IO���_�ǉ�_CNT
            # import����import���2���X�V�����͂�
            if UTL_STEP��_IO���_�ǉ�_CNT != 2:
                ActSheet_x[12] = ActSheet_x[12] + " �v�m�F"
                
        elif "LISTCAT " in SYSIN:
            # '=============================================================
            # '�R�}���h : LISTCAT'
            # '=============================================================
            ActSheet_x[12] = "LISTCAT"
            ����DD = "SYSPRINT"
            IO���� = "OUTPUT"
            for i in range(len(����������)):
                if "OUTFILE" in ����������[i] or "OFILE" in ����������[i]:
                    ����DD = ����������[i].replace("OUTFILE", "").replace("OFILE", "").replace("(", "").replace(")", "")
                    
            #UTL_STEP��_IO��� �o��
            if ���p_UTL_STEP��_IO���_.insert() == False:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
            else:
                UTL_STEP��_IO���_�ǉ�_CNT = UTL_STEP��_IO���_�ǉ�_CNT + 1
            ActSheet_x[16] = UTL_STEP��_IO���_�ǉ�_CNT
            if UTL_STEP��_IO���_�ǉ�_CNT != 1:
                ActSheet_x[12] = ActSheet_x[12] + " �v�m�F"
        elif "DEFINE " in SYSIN or "DEF " in SYSIN:
            # '=============================================================
            # '�R�}���h : DEFINE'
            # '=============================================================
            
            if " NOVSAM" in SYSIN or "NVSAM" in SYSIN:
                ###====�R�}���h : DEFINE NOVSAM ===='
                ActSheet_x[12] = "DEF-NVSAM"
                DD_CNT = DD_CNT + 1
                ����DD = "_SYSD" + str(DD_CNT).zfill(3)
                IO���� = "OUTPUT"
                ###UTL_STEP��_IO��� �o��
                if ���p_UTL_STEP��_IO���_.insert():
                    ActSheet_x[16] = 1
                else:
                    if ���p_UTL_STEP��_IO���_.update():
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "STEP-IO�X�V(OUTPUT)"
                        ActSheet_x[16] = 1
                    else:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                        ActSheet_x[16] = 0
                
                if "NAME" in SYSIN:     ###1�s�Ŋ������邩�ǂ���
                    for i in range(len(����������)):
                        if "NAME" in ����������[i]:
                            �ǉ�DSN = ����������[i].replace("NONVSAM", "").replace("NVSAM", "").replace("NAME", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
                    ###�ڋq��_JCL_PGM_DSN �o��    '���F�u���C�N��Ȃ̂�1�s�O�ɏo�͂���i���j
                    if ���p_�ڋq��_JCL_PGM_DSN_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                        ActSheet_x[14] = 0
                    else:
                        ActSheet_x[14] = 1
                    ActSheet_x[17] = �ǉ�DSN
                else:
                    DEFNVSAM�p�� = True  ###��������͓����Ȃ̂ŗ��p����
            elif " PATH" in SYSIN:
                ###====�R�}���h : DEFINE PATH ===='
                ActSheet_x[12] = "DEF-PATH"
                DD_CNT = DD_CNT + 1
                ����DD = "_SYSD" + str(DD_CNT).zfill(3)
                IO���� = "OUTPUT"
                ###UTL_STEP��_IO��� �o��
                if ���p_UTL_STEP��_IO���_.insert():
                    ActSheet_x[16] = 1
                else:
                    if ���p_UTL_STEP��_IO���_.update():
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "STEP-IO�X�V(OUTPUT)"
                        ActSheet_x[16] = 1
                    else:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                        ActSheet_x[16] = 0
                    
                if "NAME" in SYSIN:     ###1�s�Ŋ������邩�ǂ���
                    for i in range(len(����������)):
                        if "NAME" in ����������[i]:
                            �ǉ�DSN = ����������[i].replace("PATH", "").replace("NAME", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
                    ###�ڋq��_JCL_PGM_DSN �o��    '���F�u���C�N��Ȃ̂�1�s�O�ɏo�͂���i���j
                    if ���p_�ڋq��_JCL_PGM_DSN_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                        ActSheet_x[14] = 0
                    else:
                        ActSheet_x[14] = 1
                    ActSheet_x[17] = �ǉ�DSN
                else:
                    DEFPATH�p�� = True  ###��������͓����Ȃ̂ŗ��p����
            elif " SPACE" in SYSIN or " SPC" in SYSIN:
                ###====�R�}���h : DEFINE SPACE ===='
                ActSheet_x[12] = "DEF-SPC"
                ###DEFINE SPACE�̓A�N�Z�X���u��ɃX�y�[�X���m�ۂ��鏈���Ȃ̂ŁA���o�͏��ɓ��Ɋ֌W�͂Ȃ�
                
            elif " USERCATALOG" in SYSIN or " UCAT" in SYSIN:
                ###====�R�}���h : DEFINE USERCATALOG / DEF UCAT ===='
                ActSheet_x[12] = "DEF-UCAT"
                DD_CNT = DD_CNT + 1
                ����DD = "_SYSD" + str(DD_CNT).zfill(3)
                IO���� = "OUTPUT"
                ###UTL_STEP��_IO��� �o��
                if ���p_UTL_STEP��_IO���_.insert():
                    ActSheet_x[16] = 1
                else:
                    if ���p_UTL_STEP��_IO���_.update():
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "STEP-IO�X�V(OUTPUT)"
                        ActSheet_x[16] = 1
                    else:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                        ActSheet_x[16] = 0
                    
                if "NAME" in SYSIN:     ###1�s�Ŋ������邩�ǂ���
                    for i in range(len(����������)):
                        if "NAME" in ����������[i]:
                            �ǉ�DSN = ����������[i].replace("USERCATALOG", "").replace("UCAT", "").replace("NAME", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
        
                    ###�ڋq��_JCL_PGM_DSN �o��    '���F�u���C�N��Ȃ̂�1�s�O�ɏo�͂���i���j
                    if ���p_�ڋq��_JCL_PGM_DSN_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                        ActSheet_x[14] = 0
                    else:
                        ActSheet_x[14] = 1
                    ActSheet_x[17] = �ǉ�DSN
                else:
                    DEFUCAT�p�� = True
            elif " AIX" in SYSIN or "ALTERNATEINDEX" in SYSIN:
                ###====�R�}���h : DEFINE AIX / DEFINE ALTERNATEINDEX===='
                ActSheet_x[12] = "DEF-AIX"
                DD_CNT = DD_CNT + 1
                ����DD = "_SYSD" + str(DD_CNT).zfill(3)
                IO���� = "OUTPUT"
                ###UTL_STEP��_IO��� �o��
                if ���p_UTL_STEP��_IO���_.insert():
                    ActSheet_x[16] = 1
                else:
                    if ���p_UTL_STEP��_IO���_.update():
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "STEP-IO�X�V(OUTPUT)"
                        ActSheet_x[16] = 1
                    else:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                        ActSheet_x[16] = 0
                    
                if "NAME" in SYSIN:     ###1�s�Ŋ������邩�ǂ���
                    for i in range(len(����������)):
                        if "NAME" in ����������[i]:
                            �ǉ�DSN = ����������[i].replace("ALTERNATEINDEX", "").replace("AIX", "").replace("NAME", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
        
                    ###�ڋq��_JCL_PGM_DSN �o��    '���F�u���C�N��Ȃ̂�1�s�O�ɏo�͂���i���j
                    if ���p_�ڋq��_JCL_PGM_DSN_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                        ActSheet_x[14] = 0
                    else:
                        ActSheet_x[14] = 1
                    ActSheet_x[17] = �ǉ�DSN
                else:
                    DEFAIX�p�� = True
            elif " CLUSTER" in SYSIN or " CL" in SYSIN:
                ###====�R�}���h : DEFINE CLUSTER / DEF CL ===='
                ActSheet_x[12] = "DEF-CL"
                DD_CNT = DD_CNT + 1
                ����DD = "_SYSD" + str(DD_CNT).zfill(3)
                IO���� = "OUTPUT"
                ###UTL_STEP��_IO��� �o��
                if ���p_UTL_STEP��_IO���_.insert():
                    ActSheet_x[16] = 1
                else:
                    if ���p_UTL_STEP��_IO���_.update():
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "STEP-IO�X�V(OUTPUT)"
                        ActSheet_x[16] = 1
                    else:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                        ActSheet_x[16] = 0
                    
                if "NAME" in SYSIN:     ###1�s�Ŋ������邩�ǂ���
                    for i in range(len(����������)):
                        if "NAME" in ����������[i]:
                            �ǉ�DSN = ����������[i].replace("CLUSTER", "").replace("CL", "").replace("NAME", "").replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
        
                    ###�ڋq��_JCL_PGM_DSN �o��    '���F�u���C�N��Ȃ̂�1�s�O�ɏo�͂���i���j
                    if ���p_�ڋq��_JCL_PGM_DSN_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                        ActSheet_x[14] = 0
                    else:
                        ActSheet_x[14] = 1
                    ActSheet_x[17] = �ǉ�DSN
                else:
                    DEFCL�p�� = True
            else:
                ###���Ή�DEFINE��
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "���Ή�DEFINE��"
                
        elif "VERIFY " in SYSIN:
            # '=============================================================
            # '�R�}���h : VERIFY'
            # '=============================================================
            # '���̃R�}���h�ɂ�VERIFY�I�y�����h�����邽�߁A�Ō�ɔ��肷��B
            # 'VERIFY�͓��o�͂�����R�}���h�łȂ����߃X���[
            ActSheet_x[12] = "VERIFY"
    # '=== IEBGENER ===
    elif PGM_NAME == "IEBGENER":             ###  '�f�[�^�R�s�[
        if "COPY " in SYSIN:
            ActSheet_x[12] = "COPY"
        elif "FIELD" in SYSIN:
              ###���X�y�[�X����邩�H
            ActSheet_x[12] = "���R�[�h���ω�?"
        
        ###���܂̂Ƃ��돈�����Ȃ��BDD����SYSUT1,SYSUT2�ŌŒ�
    
    ###=== SORT ===
    elif PGM_NAME == "SORT":             ###      '�\�[�g
        if "OUTREC" in SYSIN:
            ActSheet_x[12] = "���R�[�h���ω�?"
        elif "FNAMES=" in SYSIN:
            for i in range(len(����������)):
                if "FNAMES=" in ����������[i]:
                    ����DD = ����������[i].replace("FNAMES=", "")
           
           ###UTL_STEP��_IO��� �o��
            IO���� = "OUTPUT"
           
            if ���p_UTL_STEP��_IO���_.insert() == False:
                ActSheet_x[12] = ActSheet_x[11] + vbCrLf + "KEY�d���̈׏���SKIP" #### �ԈႢ? ��Ŋm�F����
            else:
                ActSheet_x[16] = 1
           
        
    ###=== DSNUTILB ===
    elif PGM_NAME == "DSNUTILB":               ###DB2 Utility �f�[�^���[�h
        pass
        ###DSNUPROC���ŗ��p�@���̃R�[�h�őΉ���
    elif PGM_NAME == "KBKARCS":
        if "COPY " in SYSIN:
            # '====================
            # 'COPY
            # '====================
            ActSheet_x[12] = "COPY"
            # 'ADRDSSU���l�Ɏ蓮�Ή�
        elif "MIGRATE " in SYSIN:
            ActSheet_x[12] = "MIGRATE"
        elif "RESTORE " in SYSIN:
            # '====================
            # 'RESTORE
            # '====================
            ActSheet_x[12] = "RESTORE"
            RESTORE���[�h = ""
            
            for i in range(len(����������)):
                if "FROM(DD(" in ����������[i]:
                    ����DD = ����������[i].replace("FROM(DD(", "").replace("))", "")
                    IO���� = "BK-INPUT"
                    
                    ###UTL_STEP��_IO���_�o��
                    if ���p_UTL_STEP��_IO���_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                    else:
                        UTL_STEP��_IO���_�ǉ�_CNT = UTL_STEP��_IO���_�ǉ�_CNT + 1
                elif "TO(DD(" in ����������[i]:
                    ����DD = ����������[i].replace("TO(DD(", "").replace("))", "")
                    IO���� = "OUTPUT"
                    
                    ###UTL_STEP��_IO��� �o��
                    if ���p_UTL_STEP��_IO���_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                    else:
                        UTL_STEP��_IO���_�ǉ�_CNT = UTL_STEP��_IO���_�ǉ�_CNT + 1
                    ###JCL_PGM_DSN�͌p����������̂Ƃ���Ŏ��{
            
            ActSheet_x[14] = JCL_PGM_DSN_�ǉ�_CNT
            ActSheet_x[16] = UTL_STEP��_IO���_�ǉ�_CNT
            
            if UTL_STEP��_IO���_�ǉ�_CNT != 2:
                ActSheet_x[12] = ActSheet_x[12] + " �v�m�F"
            
            ###���X�g�ADSN�̉��
            �v�f�� = 0
            ���I�v�f = [""] ###�z��v�f���͍Œ�l1�Ƃ���B
            
            ###�O�̂���(1�s�ڂ�DSN����`����邩������Ȃ��B
            if "DATASET(" in SYSIN:
                RESTORE���[�h = "DATASET"
                for i in range(len(����������2)):
                    if "DATASET(" in ����������2[i]:
                        �ǉ�DSN = ����������2[i].replace("DATASET(", "").replace(")", "")
                ���I�v�f[0] = �ǉ�DSN
                �v�f�� += 1
                ActSheet_x[17] = �ǉ�DSN
            
            RESTORE�p�� = True
            �ǉ�DSN = ""
            JCL_NAME_SV = JCL_NAME ###�u���C�N��ɗ��p����̂őޔ�����B
            JOB_SEQ_SV = JOB_SEQ
            STEP_SEQ_SV = STEP_SEQ
    ###=== ADRDSSU ===
    elif PGM_NAME == "ADRDSSU":                ###'�f�[�^�o�b�N�A�b�v
        if "COPY " in SYSIN:
            ActSheet_x[12] = "COPY"
           
           ###���ʂ͎蓮�Ή�
           
        elif "DUMP " in SYSIN:
            ActSheet_x[12] = "DUMP"
            
            �ǉ�DSN = SYSIN.replace(" ", "").replace("-", "").replace("DUMP", "").replace("OUTDD", "").replace("(", "").replace(")", "")
            #    '����DD = "_SYSD001"
            ����DD = "BACKUP"
            IO���� = "BK-OUTPUT"
           
            ###UTL_STEP��_IO��� �o��
            if ���p_UTL_STEP��_IO���_.insert() == False:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
            else:
                ActSheet_x[16] = 1
           
            ###DD_CNT = 1
            DD_CNT = DD_CNT + 1
            ###����DD = "_SYSD" + str(DD_CNT).zfill(3)
            DUMP�p�� = True
           
        elif "RESTORE " in SYSIN:
            ActSheet_x[12] = "RESTORE"
            RESTORE���[�h = ""
                    
            for i in range(len(����������)):
                if "INDD" in ����������[i]:
                    ����DD = ����������[i].replace("INDD", "").replace("(", "").replace(")", "")
                    IO���� = "BK-INPUT"
                    
                    ###UTL_STEP��_IO��� �o��
                    if ���p_UTL_STEP��_IO���_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                    else:
                        UTL_STEP��_IO���_�ǉ�_CNT = UTL_STEP��_IO���_�ǉ�_CNT + 1
                    
                elif "IDD" in ����������[i]:
                    ����DD = ����������[i].replace("IDD", "").replace("(", "").replace(")", "")
                    IO���� = "BK-INPUT"
                    
                    ###UTL_STEP��_IO��� �o��
                    if ���p_UTL_STEP��_IO���_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                    else:
                        UTL_STEP��_IO���_�ǉ�_CNT = UTL_STEP��_IO���_�ǉ�_CNT + 1
                
                elif "OUTDD" in ����������[i]:
                    ����DD = ����������[i].replace("OUTDD", "").replace("(", "").replace(")", "")
                    ����DD_OUT_SV = ����DD
                    IO���� = "OUTPUT"
                    
                    ###UTL_STEP��_IO��� �o��
                    if ���p_UTL_STEP��_IO���_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                    else:
                        UTL_STEP��_IO���_�ǉ�_CNT = UTL_STEP��_IO���_�ǉ�_CNT + 1
                    
                    ###JCL_PGM_DSN�͌p����������̂Ƃ���Ŏ��{
                    
                elif "ODD" in ����������[i]:
                    ����DD = ����������[i].replace("ODD", "").replace("(", "").replace(")", "")
                    ����DD_OUT_SV = ����DD
                    IO���� = "OUTPUT"
                    
                    ###UTL_STEP��_IO��� �o��
                    if ���p_UTL_STEP��_IO���_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                    else:
                        UTL_STEP��_IO���_�ǉ�_CNT = UTL_STEP��_IO���_�ǉ�_CNT + 1
                    
                    ###JCL_PGM_DSN�͌p����������̂Ƃ���Ŏ��{
                    
            
            ActSheet_x[14] = JCL_PGM_DSN_�ǉ�_CNT
            ActSheet_x[16] = UTL_STEP��_IO���_�ǉ�_CNT
            
            if UTL_STEP��_IO���_�ǉ�_CNT != 2:
                ActSheet_x[12] = ActSheet_x[12] + " �v�m�F"
        
            ###���X�g�ADSN�̉��
            
            �v�f�� = 0           ##�����l��0�ɂ���@�������ɃJ�E���g�A�b�v
            ���I�v�f = [""]   ###�z��v�f���͍Œ�l1�Ƃ���
            
            ###�O�̂���(1�s�ڂ�DSN����`����邩������Ȃ�)
            if "DATASET(" in SYSIN:
                RESTORE���[�h = "DATASET"
                for i in range(len(����������2)):
                    if ����������2[i] == "DATASET(":
                        �ǉ�DSN = SYSIN.replace(" ", "").replace("-", "").replace("INCLUDE", "").replace("DATASET", "").replace("(", "").replace(")", "")
                ���I�v�f[0] = �ǉ�DSN
                ActSheet_x[17] = �ǉ�DSN
            
            RESTORE�p�� = True
            �ǉ�DSN = ""
            JCL_NAME_SV = JCL_NAME   ###�u���C�N��ɗ��p����̂őޔ�����
            JOB_SEQ_SV = JOB_SEQ
            STEP_SEQ_SV = STEP_SEQ
            
    elif PGM_NAME == "JQHGEM3":
        ###GEM3���Ăяo�����[�e�B���e�B�[
        if " PUT " in SYSIN:
            ActSheet_x[12] = "JQHGEM3-PUT"
            IO���� = "OUTPUT"
            for i in range(len(����������)):
                if "OUT=" in ����������[i] or "OUT(" in ����������[i]:
                    OUT_PARAMETER = ����������[i].replace("OUT=", "").replace("OUT(", "").replace(")", "")
                    if  "\'" in OUT_PARAMETER:
                        # 'DSN���̎w��
                        # 'JFE�q�~�Č��ɂ͑��݂��Ȃ��̂Ō���͖��Ή��@���O�����o���B
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "JQHGEM3 PUT�R�}���h OUT='DSN' OUT('DSN')�w��ɂ͖��Ή�"
                    else:
                        # 'DD���̎w��
                        ����DD = OUT_PARAMETER
                        # 'UTL_STEP��_IO���_�o��
                        if ���p_UTL_STEP��_IO���_.insert() == False:
                            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                        else:
                            UTL_STEP��_IO���_�ǉ�_CNT = UTL_STEP��_IO���_�ǉ�_CNT + 1
            
            ActSheet_x[16] = UTL_STEP��_IO���_�ǉ�_CNT
            if UTL_STEP��_IO���_�ǉ�_CNT > 1:
                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "�v�m�F"
    ###=== IKJEFT01 ===
    elif PGM_NAME == "IKJEFT01":               ###TSO�v���O�������s
        if "RUN " in SYSIN:
            ActSheet_x[12] = "RUNPGM"
            for i in range(len(����������)):
                if "PROGRAM(" in ����������[i]:
            
                    �ďo���@ = "IKJEFT01-RUN"
                    ����PGM = ����������[i].replace("PROGRAM(", "").replace(")", "").replace("-", "").replace(" ", "")
                    
                    #if ���p_�ڋq��_���Y�֘A�����_.insert() == False:
                    #    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                    #else:
                    #    ActSheet_x[13] = 1
                    #    ActSheet_x[9] = ����PGM
                    #    ActSheet_x[17] = ����PGM
                    
                    ###�֘A��TABLE�ɏo�͂��鏈���ǉ�
                    
                    if ���p_�ڋq��_JCL_PGM_DSN_.update() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "�X�V��񖳂��̈׏���SKIP"
                    else:
                        ActSheet_x[15] = 1
                        ActSheet_x[17] = ����PGM
                    
                    ###�ڋq��_JCL_STEP_SYSIN���X�V���鏈���ǉ�
                    
                    if ���p_�ڋq��_JCL_STEP_SYSIN_.update() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "�X�V��񖳂��̈׏���SKIP"
                    else:
                        ActSheet_x[17] = ����PGM
                        ActSheet_x[19] = 1
                    
    ###=== UTACH === �b��Ή�
    elif PGM_NAME == "UTACH":               ###JFE�q�~�@PGM�N��UTL
    
        if "TA" in SYSIN and "PGM=" in SYSIN:
            ###SYSIN = Mid(SYSIN, 0, 72) '�Ƃ肠�����s�v
            ActSheet_x[12] = "UTACH"
            for i in range(len(����������)):
                if "PGM=" in ����������[i]:
            
                    �ďo���@ = "UTACH�N��"
                    if UTACH�p��:
                        ����PGM = ����PGM + "," + ����������[i].replace("PGM=", "")
                    else:
                        ����PGM = ����������[i].replace("PGM=", "")
                    
                    #if ���p_�ڋq��_���Y�֘A�����_.insert() == False:
                    #    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                    #else:
                    #    ActSheet_x[13] = 1
                    #    ActSheet_x[9] = ����PGM
                    #    ActSheet_x[17] = ����PGM
                    
                    ###�֘A��TABLE�ɏo�͂��鏈���ǉ�
                    
                    if ���p_�ڋq��_JCL_PGM_DSN_.update() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "�X�V��񖳂��̈׏���SKIP"
                    else:
                        ActSheet_x[15] = 1
                        ActSheet_x[17] = ����PGM
                    
                    ###�ڋq��_JCL_STEP_SYSIN���X�V���鏈���ǉ�
                    
                    if ���p_�ڋq��_JCL_STEP_SYSIN_.update() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "�X�V��񖳂��̈׏���SKIP"
                    else:
                        ActSheet_x[17] = ����PGM
                        ActSheet_x[19] = 1
                    
           
    
        UTACH�p�� = True
    
#'20240215 ADD qian.e.wang
    ###=== ADM === �b��Ή�
    elif PGM_NAME == "ADM":               ###���YANPSS�@PGM�N��UTL
    
        if "ADMBMP" in SYSIN and "PGM=" in SYSIN:
            SYSIN = Mid(SYSIN, 0, 72)
            ActSheet_x[12] = "ADM"
            for i in range(len(����������)):
                if "PGM=" in ����������[i]:
            
                    �ďo���@ = "ADM�N��"
                    if ADM�p��:
                        ����PGM = ����PGM + "," + ����������[i].replace("PGM=", "")
                    else:
                        ����PGM = ����������[i].replace("PGM=", "")
                    
                    ActSheet_x[13] = 1
                    ActSheet_x[9] = ����PGM
                    ActSheet_x[17] = ����PGM
                    
                    ###�֘A��TABLE�ɏo�͂��鏈���ǉ�
                    
                    if ���p_�ڋq��_JCL_PGM_DSN_.update() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "�X�V��񖳂��̈׏���SKIP"
                    else:
                        ActSheet_x[15] = 1
                        ActSheet_x[17] = ����PGM
                    
                    ###�ڋq��_JCL_STEP_SYSIN���X�V���鏈���ǉ�
                    
                    if ���p_�ڋq��_JCL_STEP_SYSIN_.update() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "�X�V��񖳂��̈׏���SKIP"
                    else:
                        ActSheet_x[17] = ����PGM
                        ActSheet_x[19] = 1
                    
        ADM�p�� = False
    
    ###=== JYAADP === �b��Ή�
    elif PGM_NAME == "JYAADP":               ###���YANPSS�@PGM�N��UTL
    
        if "NAME" in SYSIN:
            SYSIN = Mid(SYSIN, 0, 72)
            ActSheet_x[12] = "JYAADP"

            for i in range(len(����������2)):
                if "NAME" == ����������2[i]:
                    continue
                else:
                    �ďo���@ = "JYAADP�N��"
                    if JYAADP�p��:
                        ����PGM = ����PGM + "," + ����������2[i]
                    else:
                        ����PGM = ����������2[i]
                    
                    ActSheet_x[13] = 1
                    ActSheet_x[9] = ����PGM
                    ActSheet_x[17] = ����PGM
                    
                    ###�֘A��TABLE�ɏo�͂��鏈���ǉ�
                    
                    if ���p_�ڋq��_JCL_PGM_DSN_.update() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "�X�V��񖳂��̈׏���SKIP"
                    else:
                        ActSheet_x[15] = 1
                        ActSheet_x[17] = ����PGM
                    
                    ###�ڋq��_JCL_STEP_SYSIN���X�V���鏈���ǉ�
                    
                    if ���p_�ڋq��_JCL_STEP_SYSIN_.update() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "�X�V��񖳂��̈׏���SKIP"
                    else:
                        ActSheet_x[17] = ����PGM
                        ActSheet_x[19] = 1
                    
        JYAADP�p�� = False
    
    ###=== ADARUN3V === �b��Ή�
    elif PGM_NAME == "ADARUN3V":               ###���YANPSS�@PGM�N��UTL
    
        if "ADARUN" in SYSIN and ("PROGRAM=" in SYSIN or "PROG=" in SYSIN):
            SYSIN = Mid(SYSIN, 0, 72)
            ActSheet_x[12] = "ADARUN3V"
            for i in range(len(����������)):
                if "PROGRAM=" in ����������[i] or "PROG=" in ����������[i]:
            
                    �ďo���@ = "ADARUN3V�N��"
                    if ADARUN3V�p��:
                        ����PGM = ����PGM + "," + ����������[i].replace("PROGRAM=", "").replace("PROG=", "")
                    else:
                        ����PGM = ����������[i].replace("PROGRAM=", "").replace("PROG=", "")
                    
                    ActSheet_x[13] = 1
                    ActSheet_x[9] = ����PGM
                    ActSheet_x[17] = ����PGM
                    
                    ###�֘A��TABLE�ɏo�͂��鏈���ǉ�
                    
                    if ���p_�ڋq��_JCL_PGM_DSN_.update() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "�X�V��񖳂��̈׏���SKIP"
                    else:
                        ActSheet_x[15] = 1
                        ActSheet_x[17] = ����PGM
                    
                    ###�ڋq��_JCL_STEP_SYSIN���X�V���鏈���ǉ�
                    
                    if ���p_�ڋq��_JCL_STEP_SYSIN_.update() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "�X�V��񖳂��̈׏���SKIP"
                    else:
                        ActSheet_x[17] = ����PGM
                        ActSheet_x[19] = 1
                    
        ADARUN3V�p�� = False
#'ADD END
    
    ### === IEBPTPCH ===
    elif PGM_NAME == "IEBPTPCH":             ###  '���C�u�����R�s�[
        pass
        ###�Ή��ۗ��A�K�v�ɂȂ�����Ή��\��

    # '=== FTP ===
    # 'elif PGM_NAME = "FTP":                    'FTP�t�@�C������M
        
    #     '�Ή��ۗ��A�K�v�ɂȂ�����Ή��\��
        
    # '=== XRSNDGO ===
    elif PGM_NAME == "XRSNDGO":               ### 'HULFT���M
        pass
    #     '�Ή��ۗ��A�K�v�ɂȂ�����Ή��\��
        
    # '=== IEBASE ===
    elif PGM_NAME == "IEBASE":                ### 'EXPEDITE�ʐM
        pass
    #     '�Ή��ۗ��A�K�v�ɂȂ�����Ή��\��
        
    # '=== DFSRRC00 ===
    elif PGM_NAME == "DFSRRC00":              ### 'IMSDB�֘AUTL
    
        # 'IMSDB�o�b�N�A�b�v�iDFSUDMP0�j
        # 'if "D1 " in SYSIN: '��1�v�f��"D1"��z�� �ˌ댟�m����̂��ߕύX
        if str(SYSIN).startswith("D1 "): ###��1�v�f��"D1"��z��
            ����������2 = ArrayEmptyDelete(SYSIN.split(" "))
            if ����������2[0] == "D1":
                ����DD = ����������2[2]
                IO���� = "INPUT"
                  
                ###UTL_STEP��_IO��� �o��
                if ���p_UTL_STEP��_IO���_.insert() == False:
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                else:
                    UTL_STEP��_IO���_�ǉ�_CNT = UTL_STEP��_IO���_�ǉ�_CNT + 1
                    
                ����DD = ����������2[3]
                IO���� = "BK-OUTPUT"
                  
                ###UTL_STEP��_IO��� �o��
                if ���p_UTL_STEP��_IO���_.insert() == False:
                    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                else:
                    UTL_STEP��_IO���_�ǉ�_CNT = UTL_STEP��_IO���_�ǉ�_CNT + 1
                                    
            else:
                ActSheet_x[12] = ActSheet_x[12] + " �z��v�f�v�m�F"
    
    # '��PROC�Ή�
    # '=== DSNUPROC ===
    elif PROC_NAME == "DSNUPROC":              ###'DB���[�h�E�A�����[�h
        if "UNLOAD " in SYSIN:
            ActSheet_x[12] = "UNLOAD"
           

           
        #    'UNLOAD����1�s�ڂɋL�ڂ��Ȃ���Όp���Ή��ɂ���
            if "FROM " in SYSIN and " TABLE " in SYSIN:
           
                for i in range(len(����������2)):
                    if ����������2[i] == "TABLE":
                      
                        DD_CNT = DD_CNT + 1
                        ����DD = "_SYSD" + str(DD_CNT).zfill(3)
                        ###����DD = "_SYSD001"
                        IO���� = "INPUT"
            
                        ###UTL_STEP��_IO��� �o��
                        if ���p_UTL_STEP��_IO���_.insert() == False:
                            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                            ActSheet_x[16] = 0
                        else:
                            ActSheet_x[16] = 1
           
                        ###�ڋq��_JCL_PGM_DSN �o��
                        if i + 1 < len(����������2):
                            �ǉ�DSN = ����������2[i + 1]
                            �ǉ�DSN = �ǉ�DSN.replace("JBDB2.", "")     ###MHI�Č��̂ݎb��Ή�
                            if ���p_�ڋq��_JCL_PGM_DSN_.insert() == False:
                                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                                ActSheet_x[14] = 0
                            else:
                                ActSheet_x[14] = 1
                            ActSheet_x[17] = �ǉ�DSN
                        else:
                            ActSheet_x[12] = ActSheet_x[12] + " �z��v�f�v�m�F"     ### 'UNLOAD������1�s���ɋL�ڂ�����z��
           
           
            else:
                UNLOAD�p�� = True
           
        elif "LOAD " in SYSIN:
            ActSheet_x[12] = "LOAD"
                        
            for i in range(len(����������2)):
                if  "INDDN(" in ����������2[i]:
                    ����DD = ����������2[i].replace("INDDN", "").replace("(", "").replace(")", "")
                    IO���� = "INPUT"
            
                    ###UTL_STEP��_IO��� �o��
                    if ���p_UTL_STEP��_IO���_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                        ActSheet_x[16] = 0
                    else:
                        ActSheet_x[16] = 1
            
            
            ###LOAD�悪1�s�ڂɋL�ڂ��Ȃ���Όp���Ή��ɂ���
            if "INTO " in SYSIN and " TABLE " in SYSIN:
            
                for i in range(len(����������2)):
                    if ����������2[i] == "TABLE":
                        DD_CNT = DD_CNT + 1
                        ����DD = "_SYSD" + str(DD_CNT).zfill(3)
                        ###����DD = "_SYSD001"
                        IO���� = "OUTPUT"
            
                        ###UTL_STEP��_IO��� �o��
                        if ���p_UTL_STEP��_IO���_.insert() == False:
                            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                            ActSheet_x[16] = 0
                        else:
                            ActSheet_x[16] = 1
            
                        ###�ڋq��_JCL_PGM_DSN �o��
                        if i + 1 < len(����������2):
                            �ǉ�DSN = ����������2[i + 1]
                            �ǉ�DSN = �ǉ�DSN.replace("JBDB2.", "")     ###MHI�Č��̂ݎb��Ή�
                            if ���p_�ڋq��_JCL_PGM_DSN_.insert() == False:
                                ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                                ActSheet_x[14] = 0
                            else:
                                ActSheet_x[14] = 1
                            ActSheet_x[17] = �ǉ�DSN
                        else:
                            ActSheet_x[12] = ActSheet_x[12] + " �z��v�f�v�m�F"      ###LOAD�����1�s���ɋL�ڂ�����z��
        
        
            else:
                LOAD�p�� = True
           
        elif "COPY " in SYSIN and " TABLESPACE " in SYSIN:
            ActSheet_x[12] = "COPY"
                        
            if COPY�p��:
                DD_CNT = DD_CNT + 1
                ActSheet_x[12] = "COPY�p��"
            else:
                DD_CNT = DD_CNT + 1
                ###DD_CNT = 1
                COPY�p�� = True
                ActSheet_x[12] = "COPY"
                        
            for i in range(len(����������2)):
                if ����������2[i] == "TABLESPACE":
                    ����DD = "_SYSD" + str(DD_CNT).zfill(3)
                    IO���� = "BK-INPUT"
    
                    ###UTL_STEP��_IO��� �o��
                    if ���p_UTL_STEP��_IO���_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                    else:
                        UTL_STEP��_IO���_�ǉ�_CNT = UTL_STEP��_IO���_�ǉ�_CNT + 1

                    ###�ڋq��_JCL_PGM_DSN �o��
                    if i + 1 < len(����������2):
                        �ǉ�DSN = ����������2[i + 1]
                        if ���p_�ڋq��_JCL_PGM_DSN_.insert() == False:
                            ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                            ActSheet_x[14] = 0
                        else:
                            ActSheet_x[14] = 1
                        ActSheet_x[17] = �ǉ�DSN
                    else:
                        ActSheet_x[12] = ActSheet_x[12] + " �z��v�f�v�m�F"
                
                elif "COPYDDN(" in ����������2[i]:
                    ����DD = ����������2[i].replace("COPYDDN", "").replace("(", "").replace(")", "")
                    IO���� = "OUTPUT"
    
                    ###UTL_STEP��_IO��� �o��
                    if ���p_UTL_STEP��_IO���_.insert() == False:
                        ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                        #ActSheet_x[16] = 0
                    else:
                        #ActSheet_x[16] = 1
                        UTL_STEP��_IO���_�ǉ�_CNT = UTL_STEP��_IO���_�ǉ�_CNT + 1
                    
                    
            ActSheet_x[16] = UTL_STEP��_IO���_�ǉ�_CNT
                   
        elif "MODIFY " in SYSIN and " RECOVERY " in SYSIN and " TABLESPACE " in SYSIN:
           ActSheet_x[12] = "MODIFY-RECOVERY"
           #���ʂ͎蓮�Ή�
        

    # '=== FTP �iMSP�j===   2021/12/16 ADD
    # 'JCL�T���v��
    # 'FTP A('TISP.FTP.ATTR')
    # 'HOST 172.22.106.41
    # 'SEND IN('USR1.TESTDATA')
    # '     OUT('D:\TESTDATA.bin')
    # '     T(B)
    # '     SYN
    # '     CNVT(NO)
    # '     TYPE(TEXT)
    # '     V(SZIA22)
    # 'RECV IN('D:\Work\IEBGENER.txt')
    # '     OUT('USR1.JCL(IEBGENER)')
    # '     T(T)
    # '     C(Y)
    # '     SYN
    # 'END
    if "FTP " in SYSIN:
        # 'SYSIN = Mid(SYSIN, 0, 72) '�Ƃ肠�����s�v
        ActSheet_x[12] = "FTP"
        
        ###  20220227 wangqian SYSIN_PGM�̒l�c�����Ή�
        ����PGM = "FTP"
        
        for i in range(len(����������)):
            if "HOST" in ����������[i]:
                if PROC_NAME == "":
                    �ďo���@ = "FTP�N��"
                else:
                    �ďo���@ = PROC_NAME + "�N��"
                #if ���p_�ڋq��_���Y�֘A�����_.insert() == False:
                #    ActSheet_x[12] = ActSheet_x[12] + vbCrLf + "KEY�d���̈׏���SKIP"
                #else:
                #    ActSheet_x[13] = 1
                #    ActSheet_x[9] = ����PGM
                #    ActSheet_x[17] = ����PGM
                
        FTP�p�� = True
        
    return ActSheet_x
       


def FLAG������():
    global JCL_NAME_SV,JOB_SEQ_SV,STEP_SEQ_SV,DELETE�p��,DUMP�p��,RESTORE�p��,DEFCL�p��,DEFPATH�p��,DEFAIX�p��,DEFNVSAM�p��,DEFUCAT�p��,FTP�p��
    global �ǉ�DSN,����DD,����PGM,IO����,�v�f��,���I�v�f
    JCL_NAME_SV = ""
    JOB_SEQ_SV = 0
    STEP_SEQ_SV = 0
    DELETE�p�� = False
    DUMP�p�� = False
    RESTORE�p�� = False
    FTP�p�� = False
    DEFCL�p�� = False
    # '20210312 Add Horiuchi
    DEFPATH�p�� = False
    DEFAIX�p�� = False
    DEFNVSAM�p�� = False
    DEFUCAT�p�� = False
    

    �ǉ�DSN = ""
    ����DD = ""
    ����PGM = ""
    IO���� = ""
    �v�f�� = 0
    ���I�v�f = [""]



def analysis1_UTL_analysis(db_path,get_conn,get_cursor):
    
    global conn,cursor
    
 
    conn = get_conn
    cursor = get_cursor
   
    ### �ڋq��_JCL_STEP_SYSIN�@�ǂݍ���
    sql =   """\
            SELECT * FROM QRY_�ڋq��_JCL_STEP_SYSIN
            """
    
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)
    
    #global REPRO_OUTDATASET_���pDD�擾_,���p_�ڋq��_JCL_STEP_SYSIN_,���p_�ڋq��_���Y�֘A�����_,���p_�ڋq��_JCL_PGM_DSN_,���p_UTL_STEP��_IO���_
    global REPRO_OUTDATASET_���pDD�擾_,���p_�ڋq��_JCL_STEP_SYSIN_,���p_�ڋq��_JCL_PGM_DSN_,���p_UTL_STEP��_IO���_
    global ActSheet

    REPRO_OUTDATASET_���pDD�擾_ = REPRO_OUTDATASET_���pDD�擾(db_path)
    ���p_�ڋq��_JCL_STEP_SYSIN_ = ���p_�ڋq��_JCL_STEP_SYSIN(db_path)
    #���p_�ڋq��_���Y�֘A�����_ = ���p_�ڋq��_���Y�֘A�����(db_path)
    ���p_�ڋq��_JCL_PGM_DSN_ = ���p_�ڋq��_JCL_PGM_DSN(db_path)
    ���p_UTL_STEP��_IO���_ = ���p_UTL_STEP��_IO���(db_path)
    JCL_NAME_BEFORE = ""
    
    global DELETE�p��,DUMP�p��,RESTORE�p��,FTP�p��
 
    ActSheet = []
    print(len(df),"analysis1_UTL_analysis")

    for i in range(len(df)):
        data = df.iloc[i]
        if data["JCL_NAME"] != JCL_NAME_BEFORE:
            if RESTORE�p��:
                _ = RESTORE�p������([],[])
                
            FLAG������()
                
            
                
        ActSheet_x = JCL_STEP_SYSIN���_���ʏo��(data)
        ActSheet_x = �p��������������(ActSheet_x,data)
        if DELETE�p�� == True:
            ###�b��
            ActSheet_x = DELETE�p������(ActSheet_x,data)
        elif DUMP�p�� == True:
            ###�b��
            ActSheet_x = DUMP�p������(ActSheet_x,data)
        elif RESTORE�p�� == True:
            ###�b��
            ActSheet_x = RESTORE�p������(ActSheet_x,data)
        elif FTP�p�� == True: ###2021/12/16 ADD
            ###�b��
            ActSheet_x = FTP�p������(ActSheet_x,data)
        else:      
            ###=========================
            ### ����UTL�Ή�
            ### =========================
    
            ###�b��
            ###if PGM_NAME = "IKJEFT01":
            ActSheet_x = JCL_STEP_SYSIN���_����UTL���胍�W�b�N(ActSheet_x,data)
 
        ActSheet.append(ActSheet_x)
        JCL_NAME_BEFORE = data["JCL_NAME"]
        
    
    ### �㏈��
    if RESTORE�p�� == True:
        ###�b��
        ActSheet_x = RESTORE�p������([],[])
        
    ���p_�ڋq��_JCL_PGM_DSN_.update_all()
    ���p_�ڋq��_JCL_STEP_SYSIN_.update_all()
    ���p_UTL_STEP��_IO���_.update_all()
    print(len(ActSheet),"analysis1_UTL_analysis")
    
 
    return ActSheet,conn,cursor
