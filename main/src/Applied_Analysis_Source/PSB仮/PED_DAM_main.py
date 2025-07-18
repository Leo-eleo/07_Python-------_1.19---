#!/usr/bin/env python
# -*- coding: cp932 -*-

import os
import sys
import time

from analysis1_PED_analysis import analysis1_PED_analysis
from analysis2_2_DBSCHEMA_analysis import analysis2_2_DBSCHEMA_analysis
from analysis2_DAMSCHEMA_analysis import analysis2_DAMSCHEMA_analysis
from analysis4_JCL_DAM import analysis4_JCL_DAM
from analysis5_update_JCL_PGM_DSN import analysis5_update_JCL_PGM_DSN
from analysis6_update_UTL_STEP_IO import analysis6_update_UTL_STEP_IO

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

def main(db_path,title,damSchema_file_path,dbSchema_file_path,ped_file_path):
    
    if os.path.isdir(title) == False:
        os.makedirs(title)

    conn = connect_accdb(db_path)
    cursor = conn.cursor()
    
    start = time.time()
    analysis2_DAMSCHEMA_analysis(conn,cursor,damSchema_file_path)
    print("DAMXL[}ðÍ®¹", time.time()-start)
    
    analysis2_2_DBSCHEMA_analysis(conn,cursor,dbSchema_file_path)
    print("DBXL[}ðÍ®¹", time.time()-start)
    
    analysis1_PED_analysis(conn,cursor,ped_file_path)
    print("PEDè`ðÍ®¹", time.time()-start)
    
    ActSheet_all = analysis4_JCL_DAM(conn,cursor)
    
    print("ðÍ4 f[^ZbgÁè®¹", time.time()-start)
    
    analysis5_update_JCL_PGM_DSN(conn,cursor)
    print("ðÍ5®¹", time.time()-start)
    
    analysis6_update_UTL_STEP_IO(conn,cursor)
    print("ðÍ6®¹", time.time()-start)
    
    ActSheet_all = [ActSheet[1:] for ActSheet in ActSheet_all]
    output_header = ["YID","JOB_SEQ","JCL_ID","STEP_SEQ","STEP_NAME","PGM_NAME","PROC_NAME","DD_NAME(AIMPED)","CMD_SEQ","PED_NAME","SCHEMA_NAME","DAM_DD_NAME","DATASET_NAME","ACCESS_MODE","õl"]
    print(len(ActSheet_all))
    
    write_excel_multi_sheet("PED_DAMðÍ.xlsx",ActSheet_all,"PED_DAMf[^ZbgðÍÊ",title,output_header)
    
    conn.close()
    
if __name__ == "__main__":     
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])