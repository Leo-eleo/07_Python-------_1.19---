#!/usr/bin/env python
# -*- coding: cp932 -*-
import os
import re
import sys

import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


PED��͌��ʏo�͏���_ = None
GetDSN_ = None

class PED��͌��ʏo�͏���:
    
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "PED_DAM�f�[�^�Z�b�g���"
        # self.db_path = db_path
    def setup(self):
        self.dic = {}

        ### PED_DAM�f�[�^�Z�b�g����DELETE�ŏ���������Ă���̂ōŏ��͋�
    
        
    def insert(self,pedFile, pedName, schemaName, ddName, accessMode,schemaKubunList,dsnList):
        if self.dic == None:
            self.setup()
            
        FileName = FlieModule = take_extensions(pedFile)
        FileLibrary = FileGouki = ""
        
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
        self.dbname = "�X�L�[�}_DATASET���"
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
            return ["�X�L�[�}��`�i" + schemaName + "�j����̂̂���DATASET���s��"]
        
 
class GetSCHEMAKUBUN:
    def __init__(self,conn,cursor):
        self.dic = None
        self.conn = conn
        self.cursor = cursor
        self.dbname = "�X�L�[�}_DATASET���"
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
    
    ### ��ōX�V���� TODO
    
    return True

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

def CheckPedFile(ped_file):
    
    global PED��͌��ʏo�͏���_, GetDSN_, GetSCHEMAKUBUN_
    pedName = ""
    schemaName = ""
    ddName = ""
    accessMode = ""
    with open(ped_file,errors="ignore") as tf:
        pedFile = get_filename(ped_file)
        
        data1= []
        for i in tf:
            if i[0] !='*':
                data1.append(i[0:72])
        
        # data1 = ','.join(data)
        # data1 = re.split('[;|\\.\n]', ' '.join(data))
        schemaName_list = []
        for line in data1:
            
            tokenList = ArrayEmptyDelete(re.split('[, =]',line))
            
            if "DBDNAME" in line:
                for i in range(len(tokenList)):
                    if tokenList[i] != "DBDNAME":
                        continue
                    if len(tokenList) > i+1:
                        ddName = tokenList[i+1]   
                        #print("�yDBDNAME�z ddName=" + tokenList[i+1] + " i=" + str(i))
                        
            if "PROCOPT" in line:
                for i in range(len(tokenList)):
                    if tokenList[i] != "PROCOPT":
                        continue
                    if len(tokenList) > i+1:
                        accessMode = tokenList[i+1]   
                        #print("�yPROCOPT�z accessMode=" + tokenList[i+1] + " i=" + str(i))
                        
            if "SENSEG" in line:
                for i in range(len(tokenList)):
                    if tokenList[i] != "SENSEG":
                        continue
                    if len(tokenList) > i+2 and tokenList[i+1] == "NAME":
                        schemaName = tokenList[i+2]  
                        #print("�ySENSEG�z schemaName=" + tokenList[i+2] + " i=" + str(i))
                        schemaName_list.append((ddName,schemaName,accessMode))
                        
                
            if "PSBNAME" in line and schemaName != "":
                for i in range(len(tokenList)):
                    if tokenList[i] != "PSBNAME":
                        continue
                    if len(tokenList) > i+1:
                        pedName = tokenList[i+1]   
                        #print("�yPSBNAME�z tokenList[i]=" + tokenList[i] + " i=" + str(i))
                    
                
                for ddName,schemaName,accessMode in schemaName_list:
                    print("�yPSB��͌��ʏo�͏����z PSBFile=" + pedFile + " PSBNAME=" + pedName + " SENSEG=" + schemaName + " DBDNAME=" + ddName + " PROCOPT=" + accessMode)
                    PED��͌��ʏo�͏���_.insert(pedFile, pedName, schemaName, ddName, accessMode,GetSCHEMAKUBUN_.get(schemaName),"")
                schemaName = ""
                ddName = ""
                accessMode = ""
                schemaName_list = []
        
        if schemaName != "":
            for ddName,schemaName,accessMode in schemaName_list:
                print("�yPSB��͌��ʏo�͏����z PSBFile=" + pedFile + " PSBNAME=" + "" + " SENSEG=" + schemaName + " DBDNAME=" + ddName + " PROCOPT=" + accessMode)
            #print("�y�v�m�F�z ACCESS MODE�̎w�肪����Ă��Ȃ��B PED��`�̖�=" + pedFile)


def analysis1_PED2_analysis(conn,cursor,ped_file_path):
    global PED��͌��ʏo�͏���_,GetDSN_,GetSCHEMAKUBUN_
    
    PED��͌��ʏo�͏���_ = PED��͌��ʏo�͏���(conn,cursor)
    GetDSN_ = GetDSN(conn,cursor)
    GetSCHEMAKUBUN_ = GetSCHEMAKUBUN(conn,cursor)
    
    sql = "SELECT * FROM PED_DAM�f�[�^�Z�b�g���"
    df = pd.read_sql(sql,conn)
    keys = df.columns.tolist()
    for i in range(len(df)):
        data = df.iloc[i]
        values = [data[key] for key in keys]
        
        sql,values = make_delete_sql("PED_DAM�f�[�^�Z�b�g���",values,keys)
        cursor.execute(sql,values)
        
    # sql,values = make_delete_sql("PED_DAM�f�[�^�Z�b�g���",[],[])
    # cursor.execute(sql,values)
    
    ped_files = glob_files(ped_file_path)
    for ped_file in ped_files:
        CheckPedFile(ped_file)
    
    
    