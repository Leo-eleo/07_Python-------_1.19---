#!/usr/bin/env python
# -*- coding: cp932 -*-
import sys
import os

import pandas as pd
import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


PED解析結果出力処理_ = None
GetDSN_ = None

class PED解析結果出力処理:
    
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "PED_DAMデータセット情報"
        # self.db_path = db_path
    def setup(self):
        self.dic = {}

        ### PED_DAMデータセット情報はDELETEで初期化されているので最初は空
    
        
    def insert(self,pedFile, pedName, schemaName, ddName, accessMode,schemaKubunList,dsnList):
        if self.dic == None:
            self.setup()
            
        FileName,FileLibrary,FileGouki,FlieModule = GetFileInfo(pedFile)
        FileName = take_extensions(FileName)
        
        if (FileName,FileLibrary,FileGouki,FlieModule,pedName, schemaName, ddName, accessMode) in self.dic:
            return False
        
        for dsn in dsnList:
            for schemaKubun in schemaKubunList:
            
                key_list = ["PEDFILENAME","LIBRARY","GOUKI","MODULEID","PEDNAME","SCHEMANAME","DDNAME","ACCESSMODE","SCHEMAKUBUN","DSN"]
                value_list = [FileName,FileLibrary,FileGouki,FlieModule,pedName, schemaName, ddName, accessMode,schemaKubun,dsn]
                
                sql,value = make_insert_sql(self.dbname,value_list,key_list)
                self.cursor.execute(sql,value)
        self.dic[(FileName,FileLibrary,FileGouki,FlieModule,pedName, schemaName, ddName, accessMode)] = 1
        
        return True
    
    def _close_conn(self):
        if self.conn != None:
            self.conn.close() 
    
    def close_conn(self):
        self._close_conn()
 
 
class GetDSN:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "スキーマ_DATASET情報"
        # self.db_path = db_path
        

    def setup(self):
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
  
        for schemaName,datasetName in zip(df["SCHEMANAME"],df["DATASETNAME"]):
            if schemaName not in self.dic:
                self.dic[schemaName] = set()
            self.dic[schemaName].add(datasetName)
    
        
    def get(self,schemaName):

        if self.dic == None:
            self.setup()
            
        if schemaName in self.dic:
            return self.dic[schemaName]
        
        else:
            return ["スキーマ定義（" + schemaName + "）未受領のためDATASET名不明"]
        
 
class GetSCHEMAKUBUN:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "スキーマ_DATASET情報"
        # self.db_path = db_path
        

    def setup(self):
        self.dic = {}
        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        
  
        for schemaName,schemaKubun in zip(df["SCHEMANAME"],df["SCHEMAKUBUN"]):
            if schemaName not in self.dic:
                self.dic[schemaName] = set()
            self.dic[schemaName].add(schemaKubun)
    
        
    def get(self,schemaName):

        if self.dic == None:
            self.setup()
            
        if schemaName in self.dic:
            return self.dic[schemaName]
        
        else:
            return [""]

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

def CheckPedFile(ped_file):
    
    global PED解析結果出力処理_, GetDSN_, GetSCHEMAKUBUN_
    pedName = ""
    schemaName = ""
    ddName = ""
    accessMode = ""
    with open(ped_file,errors="ignore") as tf:
        pedFile = get_filename(ped_file)
        
        data= []
        for i in tf:
            if i[0] !='*':
                data.append(i[0:72])
        
        # data1 = ','.join(data)
        data1 = re.split(';|\\.\s', ' '.join(data))
             
        for line in data1:
            
            tokenList = ArrayEmptyDelete(line.split(" "))
            
            if "PED" in line:
                for i in range(len(tokenList)):
                    if tokenList[i] != "PED":
                        continue
                    if len(tokenList) > i+3 and tokenList[i+1] == "NAME" and tokenList[i+2] == "IS":
                        pedName = tokenList[i+3]      
                        
            elif "DATASET" in line:
                for i in range(len(tokenList)):
                    if tokenList[i] != "DATASET":
                        continue
                    if len(tokenList) > i+5 and tokenList[i+1] == "NAME" and tokenList[i+2] == "IS" and tokenList[i+4] == "FOR":
                        schemaName = tokenList[i + 3]
                        ddName = tokenList[i + 5]    
                
            elif "ACCESS" in line and schemaName != "":
                for i in range(len(tokenList)):
                    if tokenList[i] != "ACCESS":
                        continue
                    if len(tokenList) > i+3 and tokenList[i+1] == "MODE" and tokenList[i+2] == "IS":
                        accessMode = tokenList[i+3]   
                    
                    if CheckAccessMode(accessMode) == True:
                        break
                    
                    if len(tokenList) > i+4:
                        accessMode = tokenList[i+4]
                    if CheckAccessMode(accessMode) == False:
                        print("【要確認】 適切なACCESS MODEの取得に失敗。 PED定義体名=" + pedFile)
                
                PED解析結果出力処理_.insert(pedFile, pedName, schemaName, ddName, accessMode,GetSCHEMAKUBUN_.get(schemaName),GetDSN_.get(schemaName))
                schemaName = ""
                ddName = ""
                accessMode = ""
        
        if schemaName != "":
            print("【要確認】 ACCESS MODEの指定がされていない。 PED定義体名=" + pedFile)


def analysis1_PED2_analysis(conn,cursor,ped_file_path):
    global PED解析結果出力処理_,GetDSN_,GetSCHEMAKUBUN_
    
    PED解析結果出力処理_ = PED解析結果出力処理(conn,cursor)
    GetDSN_ = GetDSN(conn,cursor)
    GetSCHEMAKUBUN_ = GetSCHEMAKUBUN(conn,cursor)
    
    sql = "SELECT * FROM PED_DAMデータセット情報"
    df = pd.read_sql(sql,conn)
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("PED_DAMデータセット情報",values,keys)
        cursor.execute(sql,values)
        
    # sql,values = make_delete_sql("PED_DAMデータセット情報",[],[])
    # cursor.execute(sql,values)
    
    ped_files = glob_files(ped_file_path)
    for ped_file in ped_files:
        CheckPedFile(ped_file)
    
    
    