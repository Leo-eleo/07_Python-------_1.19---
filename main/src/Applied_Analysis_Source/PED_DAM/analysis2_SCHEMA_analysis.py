#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

import pandas as pd
import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


�X�L�[�}��͌��ʏo�͏���_ = None
JFE_DATA�֘A���ݒ�o�͏���_ = None


class �X�L�[�}��͌��ʏo�͏���:
    
    def __init__(self,conn,cursor,schema_folder):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�X�L�[�}_DATASET���"
        # self.db_path = db_path
        self.schema_folder = schema_folder

    def setup(self):
        self.dic = {}
        
        ### �X�L�[�}_DATASET����DELETE�ŏ���������Ă���̂ōŏ��͋�
    
        
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
 
class JFE_DATA�֘A���ݒ�o�͏���:
    
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�y�b��zJFE_DATA�֘A���ݒ�"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}

        sql = "SELECT * FROM "+self.dbname
        
        df = pd.read_sql(sql,self.conn)
        df.fillna("",inplace=True)
        for type,id,dsn in zip(df["�f�[�^����"],df["�f�[�^ID"],df["DSN"]):
            self.dic[(type,id,dsn)] = 1
        
    def insert(self,schemakubun, recordName, datasetName):
        if self.dic == None:
            self.setup()
        if (schemakubun, recordName, datasetName) in self.dic:
            return False
        
        key_list = ["�f�[�^����","�f�[�^ID","DSN"]
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
        #'�r���I�ǂݎ���p���[�h
        return True
    elif value == "MODIFY":
        #'�f�[�^���R�[�h�X�V���[�h
        return True
    elif value == "READ-ONLY":
        #'�ǂݎ���p
        return True
    elif value == "UPDATE":
        #'�f�[�^�\���X�V���[�h
        return True
    elif value == "WRITE-ONLY":
        #'�����o����p���[�h
        return True
    
    else:
        return False

def CheckschemaFile(schema_file,schemakubun):
    
    global �X�L�[�}��͌��ʏo�͏���_ ,JFE_DATA�֘A���ݒ�o�͏���_
    
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
                
                �X�L�[�}��͌��ʏo�͏���_.insert(schemaFile, schemaName, datasetName)
                for record in recordList:
                    JFE_DATA�֘A���ݒ�o�͏���_.insert(schemakubun,record,datasetName)
                    
                # recordList = []

def analysis2_SCHEMA_analysis(conn,cursor,schema_folder_path,schema_folder,schemakubun):
    global �X�L�[�}��͌��ʏo�͏���_,JFE_DATA�֘A���ݒ�o�͏���_
    
    �X�L�[�}��͌��ʏo�͏���_ = �X�L�[�}��͌��ʏo�͏���(conn,cursor,schema_folder)
    JFE_DATA�֘A���ݒ�o�͏���_ = JFE_DATA�֘A���ݒ�o�͏���(conn,cursor)
    

    sql = "SELECT * FROM �X�L�[�}_DATASET��� WHERE SCHEMAKUBUN = '" + schema_folder + "'"
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)
    
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("�X�L�[�}_DATASET���",values,keys)
        cursor.execute(sql,values)
    
    sql = "SELECT * FROM �y�b��zJFE_DATA�֘A���ݒ� WHERE �f�[�^���� = '" + schemakubun + "'"
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("�y�b��zJFE_DATA�֘A���ݒ�",values,keys)
        cursor.execute(sql,values)
        
    schema_files = glob_files(schema_folder_path)
    for schema_file in schema_files:
        CheckschemaFile(schema_file,schemakubun)

