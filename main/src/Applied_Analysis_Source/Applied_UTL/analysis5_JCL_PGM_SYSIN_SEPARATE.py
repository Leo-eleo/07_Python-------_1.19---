#!/usr/bin/env python
# -*- coding: cp932 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

応用_顧客別_JCL_PGM_DSN_ = None


DB自動登録時PARM = "自動設定（UTL解析）"

SYSIN_BEFORE = ""

更新情報key = ["LIBRARY_ID","JCL_NAME","JOB_SEQ","JOB_ID","STEP_SEQ","STEP_NAME","PGM_NAME","PROC_NAME","SYSIN_PGM","DD_NAME",\
                "DSN","GDG","SYSIN","DISP","SYSOUT","WRITER","FORM","UNIT","SPACE_Q","DCB_RECFM","DCB_LRECL","DCB_BLKSIZE","VOL","LABEL","PGM予備","実行モード","手動更新FLG","自動更新FLG"]


    

class 応用_顧客別_JCL_PGM_DSN:
    
    def __init__(self,conn,cursor):

        self.conn = conn
        self.cursor = cursor
        self.dbname = "顧客別_JCL_PGM_DSN"
        # self.db_path = db_path
        
    def setup(self):
        return 

        
    def insert(self,data,split_string,step_seq2):
        if self.conn == None:
            self.setup()

        global DB自動登録時PARM

        key_list = 更新情報key
        value_list = [data[key] for key in key_list]
        value_list[8] = split_string ### SYSIN_PGMを分割した文字列にする
        value_list[-2] = step_seq2 ### 手動更新FLGは登録順序を設定
        value_list[-1] = DB自動登録時PARM ### 自動更新FLGはDB自動登録時PARMにする
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        self.cursor.execute(sql,value)
       
        return True
    
    def update(self,data,split_string):
        if self.conn == None:
            self.setup()


        set_key_list = ["SYSIN_PGM"]
        set_value_list = [split_string]
        
        where_key_list = [key for key in 更新情報key if data[key] != ""]
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
    global 応用_顧客別_JCL_PGM_DSN_
    
    SYSIN_BEFORE = data["SYSIN_PGM"]
    
    # ### 分割が必要なければ何もしない
    # if "," not in SYSIN_BEFORE:
    #     return 
    
    分割文字列 = ArrayEmptyDelete(data["SYSIN_PGM"].split(","))
    
    for i in range(len(分割文字列)):
        # if i == 0:
        #     ###最初のPGMの場合
        #     応用_顧客別_JCL_PGM_DSN_.update(data,分割文字列[i])

        # else:
        #     ###二つ目以降のPGM
        #     応用_顧客別_JCL_PGM_DSN_.insert(data,分割文字列[i])
            
        応用_顧客別_JCL_PGM_DSN_.insert(data,分割文字列[i], i + 1 )
            


def analysis5_JCL_PGM_SYSIN_SEPARATE(conn,cursor):
    global 応用_顧客別_JCL_PGM_DSN_
    sql =   """\
            SELECT * FROM 顧客別_JCL_PGM_DSN WHERE SYSIN_PGM <> '' AND PGM_NAME IN ( 'UTACH' , 'ADM' , 'JYAADP' )
            """
            
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)
    
    sql = """\
            DELETE * FROM 顧客別_JCL_PGM_DSN WHERE SYSIN_PGM <> '' AND PGM_NAME IN ( 'UTACH' , 'ADM' , 'JYAADP' )
            """
    cursor.execute(sql)
    conn.commit()
    
    print(len(df),"analysis5_JCL_PGM_SYSIN_SEPARATE")
    応用_顧客別_JCL_PGM_DSN_ = 応用_顧客別_JCL_PGM_DSN(conn,cursor)

    for i in range(len(df)):
        data = df.iloc[i]
        UPDATE_OR_INSERT_JCL_PGM_DSN(data)
        
        