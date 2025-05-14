#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

     
def DD_joint_main(db_path,title):
    
    
    conn = connect_accdb(db_path)
    cursor = conn.cursor()

    sql = "SELECT * FROM QRY_DD連結候補"
    
    df = pd.read_sql(sql,conn)
    df.fillna("", inplace=True)
    
    ActSheet = []            
    
    KEY_old = ""
    for i in range(len(df)):
        data = df.iloc[i]
        KEY = data["JCL_NAME"] + "-" + str(data["JOB_SEQ"]) + "-" + str(data["STEP_SEQ"]) + "-" + str(data["DD_NAME"])
        
        if KEY != KEY_old:        
            ActSheet_GYO = [""]*13
            ActSheet_GYO[1] = data["JCL_NAME"]
            ActSheet_GYO[2] = data["JOB_SEQ"]
            ActSheet_GYO[3] = data["JOB_ID"]
            ActSheet_GYO[4] = data["STEP_SEQ"]
            ActSheet_GYO[5] = data["STEP_NAME"]
            ActSheet_GYO[6] = data["PGM_NAME"]
            ActSheet_GYO[7] = data["PROC_NAME"]
            ActSheet_GYO[8] = data["SYSIN_PGM"]
            ActSheet_GYO[9] = data["DD_NAME"]
            ActSheet_GYO[10] = data["DSN"]
            KEY_old = KEY
            
        else:
            ActSheet_GYO[11] = data["DSN"]
    
            ActSheet.append(ActSheet_GYO[:])
        
            
    identify_resolution_set = set()
    for i in range(len(ActSheet)):
        
        if ActSheet[i][10] == "DUMMY" or ActSheet[i][11] == "DUMMY":
            ActSheet[i][12] = "NG : DUMMYあり"
        elif ActSheet[i][10] == ActSheet[i][11]:
            ActSheet[i][12] = "NG : 同一DSN"
        elif ActSheet[i][10] == "" or ActSheet[i][11] == "":
            ActSheet[i][12] = "NG : 想定外のエラー"
        else:
            ActSheet[i][12] = "OK"
            identify_resolution_set.add((ActSheet[i][10],ActSheet[i][11]))
            
            
    ActSheet_all = [actSheet[1:] for actSheet in ActSheet]
    output_header = ["JCL_NAME","JOB_SEQ","JOB_ID","STEP_SEQ","STEP_NAME","PGM_NAME","PROC_NAME","SYSIN_PGM","DD_NAME","DSN ①","DSN ②","判定結果"]
    write_excel_multi_sheet("QRY_DD連結候補.xlsx",ActSheet_all,"QRY_DD連結候補",title,output_header)
    
    return identify_resolution_set

if __name__ == "__main__":
    DD_joint_main(sys.argv[1],sys.argv[2])