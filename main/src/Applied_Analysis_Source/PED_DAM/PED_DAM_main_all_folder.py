#!/usr/bin/env python
# -*- coding: cp932 -*-

import sys
import os
sys.path.append(os.path.dirname(__file__))
import time

from analysis1_PED2_analysis import analysis1_PED2_analysis
from analysis2_SCHEMA_analysis import analysis2_SCHEMA_analysis

from analysis3_add_DATASET import analysis3_add_DATASET
from analysis4_JCL_DAM2 import analysis4_JCL_DAM2
from analysis5_update_JCL_PGM_DSN2 import analysis5_update_JCL_PGM_DSN2
from analysis6_update_UTL_STEP_IO import analysis6_update_UTL_STEP_IO

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Common_analysis import *

def main(db_path,title,folder_Schema_path,ped_file_path):
    
    if os.path.isdir(title) == False:
        os.makedirs(title)

    print("finish preparation and start analysis.")
    
    conn = connect_accdb(db_path)
    cursor = conn.cursor()
    
    Schema_Folders = glob_files(folder_Schema_path,recursive=False,type="folder")


    start = time.time()

    for Schema_Folder in Schema_Folders:
        Folder_name = os.path.split(Schema_Folder)[-1]
        if Folder_name.startswith("DAM"):
            schemakubun = "DAM"
        elif Folder_name.startswith("DB"):
            schemakubun = "NDB"
        elif Folder_name.startswith("AIM"):
            schemakubun = "AIM"
        elif Folder_name.startswith("VICS") or Folder_name.startswith("新VICS"):
            schemakubun = "VICS"
        else:
            schemakubun = "その他環境"
        
        print("start analysis the folder of ",Folder_name)
        analysis2_SCHEMA_analysis(conn,cursor,Schema_Folder,Folder_name,schemakubun)
        print(Folder_name, "スキーマ解析完了", time.time()-start)


    analysis1_PED2_analysis(conn,cursor,ped_file_path)
    print("PED定義解析完了", time.time()-start)
    
    ActSheet_all = analysis4_JCL_DAM2(conn,cursor)
    print("解析4 データセット特定完了", time.time()-start)
    
    analysis5_update_JCL_PGM_DSN2(conn,cursor)
    print("解析5完了", time.time()-start)
    
    analysis6_update_UTL_STEP_IO(conn,cursor)
    print("解析6完了", time.time()-start)
    
    ActSheet_all = [ActSheet[1:] for ActSheet in ActSheet_all]
    output_header = ["資産ID","JOB_SEQ","JCL_ID","STEP_SEQ","STEP_NAME","PGM_NAME","PROC_NAME","DD_NAME(AIMPED)","CMD_SEQ","PED_NAME","SCHEMA_NAME","DAM_DD_NAME","DATASET_NAME","ACCESS_MODE","備考"]
    print(len(ActSheet_all))
    
    write_excel_multi_sheet("PED_DAM解析.xlsx",ActSheet_all,"PED_DAMデータセット解析結果",title,output_header)
    
    conn.close()
    
if __name__ == "__main__":     
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])