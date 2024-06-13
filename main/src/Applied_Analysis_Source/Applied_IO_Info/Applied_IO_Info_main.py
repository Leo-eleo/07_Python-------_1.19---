#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
sys.path.append(os.path.dirname(__file__))
import time
from analysis0 import analysis0
from analysis1 import analysis1
from analysis3 import analysis3
from analysis4 import analysis4

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *


def main(db_path,title):
    
    start = time.time()

    if os.path.isdir(title) == False:
        os.makedirs(title)
        
        
    conn = connect_accdb(db_path)
    cursor = conn.cursor()
    
    
    output_header = analysis0()[1:]
    
    ActSheet_all = analysis1(conn,cursor)
    print("���1����", time.time()-start)
    
    ### ���p_���o�͏��o��_2
    
    # ActSheet_all.sort(key=lambda x: (x[1],x[2],x[5],x[7],x[8],x[21]))
    ActSheet_all.sort(key=lambda x: (x[1],x[2],x[5],x[7],x[8],x[22]))
    
    ActSheet_all = analysis3(ActSheet_all,conn,cursor)
    print("���3����", time.time()-start)
   
    analysis4(ActSheet_all,conn,cursor)
    print("���4����", time.time()-start)
    
    ActSheet_all = [ActSheet[1:] for ActSheet in ActSheet_all]
    print(len(ActSheet_all))
    write_excel_multi_sheet("���p���o�͉��.xlsx",ActSheet_all,"���p���o��",title,output_header)
    
    conn.close()
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])