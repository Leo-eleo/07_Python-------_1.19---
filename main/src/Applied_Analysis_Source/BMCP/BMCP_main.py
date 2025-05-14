#!/usr/bin/env python
# -*- coding: cp932 -*-

import os
import sys

sys.path.append(os.path.dirname(__file__))
import time

from analysis1_Read_JCL_PGM_DSN import analysis1_Read_JCL_PGM_DSN
from analysis2_Get_BMCP_PGM import analysis2_Get_BMCP_PGM
from analysis3_Load import analysis3_Load

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

def main(db_path,title):
    
    start = time.time()
    if os.path.isdir(title) == False:
        os.makedirs(title)
    
    conn = connect_accdb(db_path)
    cursor = conn.cursor()
    ActSheet_all = []
    
    BMCP_Sheet = analysis1_Read_JCL_PGM_DSN(conn,cursor)
    print("���1����", time.time()-start)
    
    BMCP_Sheet = analysis2_Get_BMCP_PGM(BMCP_Sheet,conn,cursor)
    print("���2����", time.time()-start)
    
    analysis3_Load(BMCP_Sheet,conn,cursor)
    print("���3����", time.time()-start)

    ActSheet_all = [BMCP_Sheet_x[1:] for BMCP_Sheet_x in BMCP_Sheet]

    output_header = ["JCL_NAME","JOB_SEQ","STEP_SEQ","PGM_NAME","SYSIN_PGM","BMCP_PGM"]
    write_excel_multi_sheet("BMCP���.xlsx",ActSheet_all,"BMCP���",title,output_header)
    
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])
        
