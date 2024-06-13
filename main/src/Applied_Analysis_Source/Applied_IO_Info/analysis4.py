#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


class ���p_���o�͏�񌋉ʏo��:
    def __init__(self,conn,cursor):
        self.conn = conn
        self.cursor = cursor
        self.dbname = "TEST_���o�͏��"
        self.key_list = ["TEST_ID","���s����","JCL_ID","LIBRARY","JOB_SEQ","JOB_ID","STEP_SEQ","STEP_SEQ2","STEP_NAME","PGM_NAME","PROC_NAME","PGM_SYSIN","DD_NAME","DSN","GDG","SYSIN","DBNAME","�f�[�^���","�f�[�^���2","���o�͏��","���o�͏��_DISP������","��̔���", \
                        "DISP","SYSOUT","WRITER","FORM","UNIT","VOL","SPACE_Q","RECFM","LRECL","BLKSIZE","LABEL","JCL_MBR","���R�[�h��","�e�X�g�p��̔���","������","�������W�b�N","���ϐ��l","PGM�\��","���s���[�h","�R�����g","������"\
                        ]

    def insert(self,ActSheet_x,x):
        
        value_list = ActSheet_x[1:13]+ActSheet_x[14:44]+[x]  ### ActSheet_x[13] BMCP_PGM �� insert �Ɋ܂߂Ȃ�
        
        sql,value = make_insert_sql(self.dbname,value_list,self.key_list)
        
        self.cursor.execute(sql,value)
        
    def _close_conn(self):
        self.conn.close()
        
    
    def close_conn(self):
        self._close_conn()


def analysis4(ActSheet,conn,cursor):
    
    sql = "SELECT * FROM TEST_���o�͏��"
    df = pd.read_sql(sql,conn)
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("TEST_���o�͏��",values,keys)
        cursor.execute(sql,values)
        
    # sql,values = make_delete_sql("TEST_���o�͏��",[],[])
    # cursor.execute(sql,values)
    # conn.commit()
    
    ���p_���o�͏�񌋉ʏo��_ = ���p_���o�͏�񌋉ʏo��(conn,cursor)
    
    for x,ActSheet_x in enumerate(ActSheet):
        ���p_���o�͏�񌋉ʏo��_.insert(ActSheet_x,x)
        
    
        