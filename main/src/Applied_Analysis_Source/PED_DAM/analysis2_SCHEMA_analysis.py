#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

import pandas as pd
import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


スキーマ解析結果出力処理_ = None
JFE_DATA関連性設定出力処理_ = None


class スキーマ解析結果出力処理:
    
    def __init__(self,conn,cursor,schema_folder):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "スキーマ_DATASET情報"
        # self.db_path = db_path
        self.schema_folder = schema_folder

    def setup(self):
        self.dic = {}
        
        ### スキーマ_DATASET情報はDELETEで初期化されているので最初は空
    
        
    def insert(self,schemaFile, schemaName, datasetName):
        if self.dic == None:
            self.setup()

        FileName,FileLibrary,FileGouki,FlieModule = GetFileInfo(schemaFile)
        FileName = take_extensions(FileName)
        if (FileName,FileLibrary,FileGouki,FlieModule,schemaName, datasetName) in self.dic:
            return False
        
        if schemaName != '':
            key_list = ["FILENAME","LIBRARY","GOUKI","MODULEID","SCHEMANAME","DATASETNAME","SCHEMAKUBUN"]
            value_list = [FileName,FileLibrary,FileGouki,FlieModule,schemaName, datasetName,self.schema_folder]
            
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

def CheckschemaFile(schema_file,schemakubun):
    
    global スキーマ解析結果出力処理_ ,JFE_DATA関連性設定出力処理_
    
    schemaName = ""
    datasetName = ""
    recordList = []
    
    with open(schema_file,errors="ignore") as tf:
        schemaFile = get_filename(schema_file)
        
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
                
                スキーマ解析結果出力処理_.insert(schemaFile, schemaName, datasetName)
                for record in recordList:
                    JFE_DATA関連性設定出力処理_.insert(schemakubun,record,datasetName)
                    
                # recordList = []

def analysis2_SCHEMA_analysis(conn,cursor,schema_folder_path,schema_folder,schemakubun):
    global スキーマ解析結果出力処理_,JFE_DATA関連性設定出力処理_
    
    スキーマ解析結果出力処理_ = スキーマ解析結果出力処理(conn,cursor,schema_folder)
    JFE_DATA関連性設定出力処理_ = JFE_DATA関連性設定出力処理(conn,cursor)
    

    sql = "SELECT * FROM スキーマ_DATASET情報 WHERE SCHEMAKUBUN = '" + schema_folder + "'"
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)
    
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("スキーマ_DATASET情報",values,keys)
        cursor.execute(sql,values)
    
    sql = "SELECT * FROM 【暫定】JFE_DATA関連性設定 WHERE データ分類 = '" + schemakubun + "'"
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("【暫定】JFE_DATA関連性設定",values,keys)
        cursor.execute(sql,values)
        
    schema_files = glob_files(schema_folder_path)
    for schema_file in schema_files:
        CheckschemaFile(schema_file,schemakubun)

