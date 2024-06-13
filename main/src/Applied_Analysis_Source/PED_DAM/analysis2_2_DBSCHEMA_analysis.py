#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

import pandas as pd
import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

DBスキーマ解析結果出力処理_ = None


    
class DBスキーマ解析結果出力処理:
    
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "スキーマ_DATASET情報"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        ### DAMスキーマとファイル名が異なるので空とみなしても問題ないが
    
        
    def insert(self,dbSchemaFile, schemaName, datasetName):
        if self.dic == None:
            self.setup()

        FileName,FileLibrary,FileGouki,FlieModule = GetFileInfo(dbSchemaFile)
        FileName = take_extensions(FileName)
        if (FileName,FileLibrary,FileGouki,FlieModule,schemaName, datasetName) in self.dic:
            return False
        
        key_list = ["FILENAME","LIBRARY","GOUKI","MODULEID","SCHEMANAME","DATASETNAME","SCHEMAKUBUN"]
        value_list = [FileName,FileLibrary,FileGouki,FlieModule,schemaName, datasetName,"NDB"]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        self.dic[(FileName,FileLibrary,FileGouki,FlieModule,schemaName, datasetName)] = 1
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
 
class JFE_DATA関連性設定出力処理:
    
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "【暫定】JFE_DATA関連性設定"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}

        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        for type,id,dsn in zip(df["データ分類"],df["データID"],df["DSN"]):
            self.dic[(type,id,dsn)] = 1
        
    def insert(self,schemakubun, recordName, datasetName):
        if self.dic == None:
            self.setup()
        if (schemakubun, recordName, datasetName) in self.dic:
            return False
        
        key_list = ["データ分類","データID","DSN"]
        value_list = [schemakubun, recordName, datasetName]
        
        sql,value = make_insert_sql(self.dbname,value_list,key_list)
        
        self.cursor.execute(sql,value)
        self.dic[(schemakubun, recordName, datasetName)] = 1
        
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

def CheckDbSchemaFile(dbSchema_file):
    
    global DBスキーマ解析結果出力処理_ ,JFE_DATA関連性設定出力処理_
    
    schemaName = ""
    datasetName = ""
    recordList = []
    
    with open(dbSchema_file,errors="ignore") as tf:
        dbSchemafile = get_filename(dbSchema_file)
        
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
                        
            elif "RECORD" in line:
                for i in range(len(tokenList)):
                    if tokenList[i] != "RECORD":
                        continue
                    if len(tokenList) > i+3 and tokenList[i+1] == "NAME" and tokenList[i+2] == "IS":
                        record = tokenList[i+3]
                        record = take_suffix(record,",")
                        recordList.append(record)   
                        
            elif "DATASET" in line:
                for i in range(len(tokenList)):
                    if tokenList[i] != "DATASET":
                        continue
                    if len(tokenList) > i+3 and tokenList[i+1] == "NAME" and tokenList[i+2] == "IS":
                        datasetName = tokenList[i + 3]
   

                
                DBスキーマ解析結果出力処理_.insert(dbSchemafile, schemaName, datasetName)
                for record in recordList:
                    JFE_DATA関連性設定出力処理_.insert("NDB",record,datasetName)
                    
                # recordList = []
                    
        
                         
                        
            


def analysis2_2_DBSCHEMA_analysis(conn,cursor,dbSchema_file_path):
    global DBスキーマ解析結果出力処理_,JFE_DATA関連性設定出力処理_
    
    DBスキーマ解析結果出力処理_ = DBスキーマ解析結果出力処理(conn,cursor)
    JFE_DATA関連性設定出力処理_ = JFE_DATA関連性設定出力処理(conn,cursor)
    
    dbSchema_files = glob_files(dbSchema_file_path)

    sql = "SELECT * FROM スキーマ_DATASET情報 WHERE SCHEMAKUBUN = 'NDB'"
    df = pd.read_sql(sql,conn)
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("スキーマ_DATASET情報",values,keys)
        cursor.execute(sql,values)
    
    # sql,values = make_delete_sql("スキーマ_DATASET情報",["NDB"],["SCHEMAKUBUN"])
    # cursor.execute(sql,values)
    
    sql = "SELECT * FROM 【暫定】JFE_DATA関連性設定 WHERE データ分類 = 'NDB'"
    df = pd.read_sql(sql,conn)
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("【暫定】JFE_DATA関連性設定",values,keys)
        cursor.execute(sql,values)
        
    # sql,values = make_delete_sql("【暫定】JFE_DATA関連性設定",["NDB"],["データ分類"])
    # cursor.execute(sql,values)
    
    for dbSchema_file in dbSchema_files:
        CheckDbSchemaFile(dbSchema_file)

