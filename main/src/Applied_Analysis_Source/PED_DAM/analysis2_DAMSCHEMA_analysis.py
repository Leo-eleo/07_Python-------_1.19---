#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


DAM�X�L�[�}��͌��ʏo�͏���_ = None



    
class DAM�X�L�[�}��͌��ʏo�͏���:
    
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�X�L�[�}_DATASET���"
        # self.db_path = db_path

    def setup(self):
        self.dic = {}
        
        ### �X�L�[�}_DATASET����DELETE�ŏ���������Ă���̂ōŏ��͋�
    
        
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

def CheckDamSchemaFile(dam_file):
    
    global DAM�X�L�[�}��͌��ʏo�͏���_ 
    
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
                

                
                DAM�X�L�[�}��͌��ʏo�͏���_.insert(damSchemaFile, schemaName, datasetName)


def analysis2_DAMSCHEMA_analysis(conn,cursor,dam_file_path):
    global DAM�X�L�[�}��͌��ʏo�͏���_
    
    DAM�X�L�[�}��͌��ʏo�͏���_ = DAM�X�L�[�}��͌��ʏo�͏���(conn,cursor)
    
    sql = "SELECT * FROM �X�L�[�}_DATASET��� WHERE SCHEMAKUBUN = 'DAM'"
    df = pd.read_sql(sql,conn)
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("�X�L�[�}_DATASET���",values,keys)
        cursor.execute(sql,values)
    
    # sql,values = make_delete_sql("�X�L�[�}_DATASET���",["DAM"],["SCHEMAKUBUN"])
    # cursor.execute(sql,values)
        
    dam_files = glob_files(dam_file_path)
    for dam_file in dam_files:
        CheckDamSchemaFile(dam_file)
