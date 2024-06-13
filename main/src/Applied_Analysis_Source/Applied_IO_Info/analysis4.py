#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


class 応用_入出力情報結果出力:
    def __init__(self,conn,cursor):
        self.conn = conn
        self.cursor = cursor
        self.dbname = "TEST_入出力情報"
        self.key_list = ["TEST_ID","実行順序","JCL_ID","LIBRARY","JOB_SEQ","JOB_ID","STEP_SEQ","STEP_SEQ2","STEP_NAME","PGM_NAME","PROC_NAME","PGM_SYSIN","DD_NAME","DSN","GDG","SYSIN","DBNAME","データ種別","データ種別2","入出力情報","入出力情報_DISP調整後","受領判定", \
                        "DISP","SYSOUT","WRITER","FORM","UNIT","VOL","SPACE_Q","RECFM","LRECL","BLKSIZE","LABEL","JCL_MBR","レコード長","テスト用受領判定","発生順","内部ロジック","元変数値","PGM予備","実行モード","コメント","元順序"\
                        ]

    def insert(self,ActSheet_x,x):
        
        value_list = ActSheet_x[1:13]+ActSheet_x[14:44]+[x]  ### ActSheet_x[13] BMCP_PGM は insert に含めない
        
        sql,value = make_insert_sql(self.dbname,value_list,self.key_list)
        
        self.cursor.execute(sql,value)
        
    def _close_conn(self):
        self.conn.close()
        
    
    def close_conn(self):
        self._close_conn()


def analysis4(ActSheet,conn,cursor):
    
    sql = "SELECT * FROM TEST_入出力情報"
    df = pd.read_sql(sql,conn)
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("TEST_入出力情報",values,keys)
        cursor.execute(sql,values)
        
    # sql,values = make_delete_sql("TEST_入出力情報",[],[])
    # cursor.execute(sql,values)
    # conn.commit()
    
    応用_入出力情報結果出力_ = 応用_入出力情報結果出力(conn,cursor)
    
    for x,ActSheet_x in enumerate(ActSheet):
        応用_入出力情報結果出力_.insert(ActSheet_x,x)
        
    
        