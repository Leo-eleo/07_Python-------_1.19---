#!/usr/bin/env python
# -*- coding: cp932 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

���p_�ڋq��_JCL_PGM_DSN_ = None


DB�����o�^��PARM = "�����ݒ�iUTL��́j"

SYSIN_BEFORE = ""

�X�V���key = ["LIBRARY_ID","JCL_NAME","JOB_SEQ","JOB_ID","STEP_SEQ","STEP_NAME","PGM_NAME","PROC_NAME","SYSIN_PGM","DD_NAME",\
                "DSN","GDG","SYSIN","DISP","SYSOUT","WRITER","FORM","UNIT","SPACE_Q","DCB_RECFM","DCB_LRECL","DCB_BLKSIZE","VOL","LABEL","PGM�\��","���s���[�h","�蓮�X�VFLG","�����X�VFLG"]


    

class ���p_�ڋq��_JCL_PGM_DSN:
    
    def __init__(self,conn,cursor):

        self.conn = conn
        self.cursor = cursor
        self.dbname = "�ڋq��_JCL_PGM_DSN"
        # self.db_path = db_path
        
    def setup(self):
        return 

        
    def insert(self,data,split_string,step_seq2):
        if self.conn == None:
            self.setup()

        global DB�����o�^��PARM

        key_list = �X�V���key
        value_list = [data[key] for key in key_list]
        value_list[8] = split_string ### SYSIN_PGM�𕪊�����������ɂ���
        value_list[-2] = step_seq2 ### �蓮�X�VFLG�͓o�^������ݒ�
        value_list[-1] = DB�����o�^��PARM ### �����X�VFLG��DB�����o�^��PARM�ɂ���
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        self.cursor.execute(sql,value)
       
        return True
    
    def update(self,data,split_string):
        if self.conn == None:
            self.setup()


        set_key_list = ["SYSIN_PGM"]
        set_value_list = [split_string]
        
        where_key_list = [key for key in �X�V���key if data[key] != ""]
        where_value_list = [data[key] for key in where_key_list]
        
        sql,value = make_update_sql(self.dbname,set_value_list, set_key_list,where_value_list,where_key_list)
        self.cursor.execute(sql,value)
       
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
        



def UPDATE_OR_INSERT_JCL_PGM_DSN(data):
    global SYSIN_BEFORE
    global ���p_�ڋq��_JCL_PGM_DSN_
    
    SYSIN_BEFORE = data["SYSIN_PGM"]
    
    # ### �������K�v�Ȃ���Ή������Ȃ�
    # if "," not in SYSIN_BEFORE:
    #     return 
    
    ���������� = ArrayEmptyDelete(data["SYSIN_PGM"].split(","))
    
    for i in range(len(����������)):
        # if i == 0:
        #     ###�ŏ���PGM�̏ꍇ
        #     ���p_�ڋq��_JCL_PGM_DSN_.update(data,����������[i])

        # else:
        #     ###��ڈȍ~��PGM
        #     ���p_�ڋq��_JCL_PGM_DSN_.insert(data,����������[i])
            
        ���p_�ڋq��_JCL_PGM_DSN_.insert(data,����������[i], i + 1 )
            


def analysis5_JCL_PGM_SYSIN_SEPARATE(conn,cursor):
    global ���p_�ڋq��_JCL_PGM_DSN_
    sql =   """\
            SELECT * FROM �ڋq��_JCL_PGM_DSN WHERE SYSIN_PGM <> '' AND PGM_NAME IN ( 'UTACH' , 'ADM' , 'JYAADP' )
            """
            
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)
    
    sql = """\
            DELETE * FROM �ڋq��_JCL_PGM_DSN WHERE SYSIN_PGM <> '' AND PGM_NAME IN ( 'UTACH' , 'ADM' , 'JYAADP' )
            """
    cursor.execute(sql)
    conn.commit()
    
    print(len(df),"analysis5_JCL_PGM_SYSIN_SEPARATE")
    ���p_�ڋq��_JCL_PGM_DSN_ = ���p_�ڋq��_JCL_PGM_DSN(conn,cursor)

    for i in range(len(df)):
        data = df.iloc[i]
        UPDATE_OR_INSERT_JCL_PGM_DSN(data)
        
        