#!/usr/bin/env python
# -*- coding: cp932 -*-
import os
import sys

import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *
    
def analysis1_Read_JCL_PGM_DSN(conn,cursor):
    
    ### 変更20191011
    sql =   """\
            SELECT DISTINCT JCL_NAME,JOB_SEQ,STEP_SEQ,PGM_NAME,SYSIN_PGM FROM 顧客別_JCL_PGM_DSN WHERE PGM_NAME IS NOT NULL
            """
            
    df = pd.read_sql(sql,conn)
    df.fillna("",inplace=True)
    
    BMCP_Sheet = []
    
    for i in range(len(df)):
        data = df.iloc[i]
        BMCP_Sheet_x = [""]*7
        
        if isBMCP_PGM(data["PGM_NAME"]):
            BMCP_Sheet_x[1] = data["JCL_NAME"]
            BMCP_Sheet_x[2] = data["JOB_SEQ"]
            BMCP_Sheet_x[3] = data["STEP_SEQ"]
            BMCP_Sheet_x[4] = data["PGM_NAME"]
            BMCP_Sheet_x[5] = data["SYSIN_PGM"]
            BMCP_Sheet.append(BMCP_Sheet_x)
        elif data["PGM_NAME"] == "UTACH" and isBMCP_PGM(data["SYSIN_PGM"]):
            BMCP_Sheet_x[1] = data["JCL_NAME"]
            BMCP_Sheet_x[2] = data["JOB_SEQ"]
            BMCP_Sheet_x[3] = data["STEP_SEQ"]
            BMCP_Sheet_x[4] = data["PGM_NAME"]
            BMCP_Sheet_x[5] = data["SYSIN_PGM"]
            BMCP_Sheet.append(BMCP_Sheet_x)
        
    return BMCP_Sheet

