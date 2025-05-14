#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
sys.path.append(os.path.dirname(__file__))
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *



output_header = ["TEST_ID","���s����","JCL��","LIBRARY","JOB_SEQ","JOB_ID","STEP-SEQ",\
                "STEP��","PGM-ID","PROC-ID","PROC-STEP-SEQ","PROC-STEP","PROC-PGM","NEXT-PROC"
]

class �e�X�g�Ώ�STEP���:
    
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
#'20240214 UPD qian.e.wang
#        self.dbname = "�ڋq��_JCL_STEP���"
        self.dbname = "�ڋq��_JCL_PGM_DSN"
#'UPD END
        # self.db_path = db_path

    def setup(self):
        
        self.dic = {}
#'20240214 UPD qian.e.wang
#        sql = "SELECT * FROM "+self.dbname + " ORDER BY STEP_SEQ"
        sql = "SELECT DISTINCT LIBRARY_ID, JCL_NAME, JOB_SEQ, JOB_ID, STEP_SEQ, STEP_NAME, PGM_NAME, PROC_NAME, SYSIN_PGM FROM "+self.dbname + " WHERE PGM_NAME <> '' ORDER BY STEP_SEQ"
#'UPD END
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        keys = df.columns.tolist()
        
        for i in range(len(df)):
            data = df.iloc[i]
            jcl_name = data["JCL_NAME"]
            if jcl_name not in self.dic:
                self.dic[jcl_name] = []
            dic = {key:data[key] for key in keys}
            self.dic[jcl_name].append(dic)
            
        
    def get(self,JCL_NAME):

        if self.dic == None:
            self.setup()
            
        if JCL_NAME in self.dic:
            return self.dic[JCL_NAME]
        
        else:
            return []
   
 

    
def analysis1_main(db_path,title):
    
    if os.path.isdir(title) == False:
        os.makedirs(title)
    ### ����DB�폜
    conn = connect_accdb(db_path)
    cursor = conn.cursor()
    
    
    sql =   """\
            SELECT * FROM �����p_�e�X�g�Ώ�STEP�ꗗ
            """
            
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)
    df.drop_duplicates(inplace=True)

    �e�X�g�Ώ�STEP���_ = �e�X�g�Ώ�STEP���(conn,cursor)
    ActSheet = []

    for i in range(len(df)):
        data = df.iloc[i]
        STEP_SEQ = 0
        
        ActSheet_x = [""]*15
        ActSheet_x[1] = data["TEST_ID"]
        ActSheet_x[2] = data["���s����"]
        ActSheet_x[3] = data["���sJOB"]
        ActSheet_x[4] = data["LIBRARY_ID"]
        ActSheet_x[5] = data["JOB_SEQ"]  #'���R�ʉ^�Ή��Œǉ�
        ActSheet_x[6] = data["JOB_ID"]
        ActSheet_x[7] = data["STEP_SEQ"]
        ActSheet_x[8] = data["STEP_NAME"]
#'20240214 UPD qian.e.wang
#        ActSheet_x[9] = data["PGM_NAME"]
        if data["SYSIN_PGM"] == "":
            ActSheet_x[9] = data["PGM_NAME"]
        else:
            ActSheet_x[9] = data["SYSIN_PGM"]
#'UPD END
        ActSheet_x[10] = data["PROC_NAME"]
        ActSheet_x[11] = 0
        parm = data["PROC_NAME"]
        
        if parm == "":
            ActSheet.append(ActSheet_x)
            continue
        
        
        
        myRS2 = �e�X�g�Ώ�STEP���_.get(parm)
        
        if myRS2 == []:
            ActSheet_x[12] = "�Y������PROC�͑��݂��܂���"
            ActSheet.append(ActSheet_x)
            
        else:
            for dic in myRS2:
                ActSheet_x = [""]*15
                ActSheet_x[1] = data["TEST_ID"]
                ActSheet_x[2] = data["���s����"]
                ActSheet_x[3] = data["���sJOB"]
                ActSheet_x[4] = data["LIBRARY_ID"]
                ActSheet_x[5] = data["JOB_SEQ"]  #'���R�ʉ^�Ή��Œǉ�
                ActSheet_x[6] = data["JOB_ID"]
                ActSheet_x[7] = data["STEP_SEQ"]
                ActSheet_x[8] = data["STEP_NAME"]
#'20240214 UPD qian.e.wang
#                ActSheet_x[9] = data["PGM_NAME"]
                if data["SYSIN_PGM"] == "":
                    ActSheet_x[9] = data["PGM_NAME"]
                else:
                    ActSheet_x[9] = data["SYSIN_PGM"]
#'UPD END
                ActSheet_x[10] = data["PROC_NAME"]
                
                ActSheet_x[11] = dic["STEP_SEQ"]
                ActSheet_x[12] = dic["STEP_NAME"]
#'20240214 UPD qian.e.wang
#                ActSheet_x[13] = dic["PGM_NAME"]
                if dic["SYSIN_PGM"] == "":
                    ActSheet_x[13] = dic["PGM_NAME"]
                else:
                    ActSheet_x[13] = dic["SYSIN_PGM"]
#'UPD END
                ActSheet_x[14] = dic["PROC_NAME"]
                ActSheet.append(ActSheet_x)
     
    # sql = "SELECT * FROM TEST_JCL_PROC_PGM�֘A�ݒ�"
    # df = pd.read_sql(sql,conn)
    # keys = df.columns.tolist()
    # for i in range(len(df)):
    #     data = df.iloc[i]
    #     values = [data[key] for key in keys]
        
    #     sql,values = make_delete_sql("TEST_JCL_PROC_PGM�֘A�ݒ�",values,keys)
    #     cursor.execute(sql,values)
    #     conn.commit()
        
    sql,_ = make_delete_sql("TEST_JCL_PROC_PGM�֘A�ݒ�",[],[])
    
    cursor.execute(sql)
    conn.commit()
    
    for i in range(len(ActSheet)):
        if ActSheet[i][4] == "":
            continue
        
        sql,values = make_insert_sql("TEST_JCL_PROC_PGM�֘A�ݒ�",ActSheet[i][1:],["TEST_ID","JCL_SEQ","JCL_ID","LIBRARY","JOB_SEQ","JOB_ID","STEP_SEQ","STEP��","PGM��","PROC��","STEP_SEQ2","PROC_STEP","PROC_PGM","NEXT_PROC"])
        cursor.execute(sql,values)
 
    conn.commit()
    conn.close()
        
        
    ActSheet_all = [actSheet[1:] for actSheet in ActSheet]
    write_excel_multi_sheet("��{_�����p_�e�X�g�Ώ�STEP�ꗗ.xlsx",ActSheet_all,"��{_�����p_�e�X�g�Ώ�STEP�ꗗ",title,output_header)
    
    
# analysis1_main(sys.argv[1],sys.argv[2])