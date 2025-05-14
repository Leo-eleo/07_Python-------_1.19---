#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


DAMスキーマ解析結果出力処理_ = None



    
class DAMスキーマ解析結果出力処理:
    
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "スキーマ_DATASET情報"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
        ### スキーマ_DATASET情報はDELETEで初期化されているので最初は空
    
        
    def insert(self,damSchemaFile, schemaName, datasetName):
        if self.dic == None:
            self.setup()

        FileName,FileLibrary,FileGouki,FlieModule = GetFileInfo(damSchemaFile)
        FileName = take_extensions(FileName)
        if (FileName,FileLibrary,FileGouki,FlieModule,schemaName, datasetName) in self.dic:
            return False
        
        key_list = ["FILENAME","LIBRARY","GOUKI","MODULEID","SCHEMANAME","DATASETNAME","SCHEMAKUBUN"]
        value_list = [FileName,FileLibrary,FileGouki,FlieModule,schemaName, datasetName,"DAM"]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        self.dic[(FileName,FileLibrary,FileGouki,FlieModule,schemaName, datasetName)] = 1
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
 
 
def CheckAccessMode(value):
    
    if value == "EXCLUSIVE-READ":
        #'排他的読み取り専用モード
        return True
    elif value == "MODIFY":
        #'データレコード更新モード
        return True
    elif value == "READ-ONLY":
        #'読み取り専用
        return True
    elif value == "UPDATE":
        #'データ構造更新モード
        return True
    elif value == "WRITE-ONLY":
        #'書き出し専用モード
        return True
    
    else:
        return False

def CheckDamSchemaFile(dam_file):
    
    global DAMスキーマ解析結果出力処理_ 
    
    schemaName = ""
    datasetName = ""
    
    with open(dam_file,errors="ignore") as tf:
        damSchemaFile = get_filename(dam_file)
        
        data= []
        for i in tf:
            if i[0] !='*':
                data.append(i[0:72])
        
        # data1 = ','.join(data)
        data1 = re.split(';|\\.\s', ' '.join(data))
             
        for line in data1:
            
            tokenList = ArrayEmptyDelete(line.split(" "))
            
            if "SCHEMA" in line:
                for i in range(len(tokenList)):
                    if tokenList[i] != "SCHEMA":
                        continue
                    if len(tokenList) > i+3 and tokenList[i+1] == "NAME" and tokenList[i+2] == "IS":
                        schemaName = tokenList[i+3]      
                        
            elif "DATASET" in line:
                for i in range(len(tokenList)):
                    if tokenList[i] != "DATASET":
                        continue
                    if len(tokenList) > i+3 and tokenList[i+1] == "NAME" and tokenList[i+2] == "IS":
                        datasetName = tokenList[i + 3]
                

                
                DAMスキーマ解析結果出力処理_.insert(damSchemaFile, schemaName, datasetName)


def analysis2_DAMSCHEMA_analysis(conn,cursor,dam_file_path):
    global DAMスキーマ解析結果出力処理_
    
    DAMスキーマ解析結果出力処理_ = DAMスキーマ解析結果出力処理(conn,cursor)
    
    sql = "SELECT * FROM スキーマ_DATASET情報 WHERE SCHEMAKUBUN = 'DAM'"
    df = pd.read_sql(sql,conn)
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("スキーマ_DATASET情報",values,keys)
        cursor.execute(sql,values)
    
    # sql,values = make_delete_sql("スキーマ_DATASET情報",["DAM"],["SCHEMAKUBUN"])
    # cursor.execute(sql,values)
        
    dam_files = glob_files(dam_file_path)
    for dam_file in dam_files:
        CheckDamSchemaFile(dam_file)
